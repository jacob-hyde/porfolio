from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

# Configure CORS
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
         "allow_headers": ["Content-Type", "Authorization"],
         "expose_headers": ["Content-Range", "X-Content-Range"],
         "supports_credentials": True,
         "max_age": 86400
     }})

# Security configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'portfolio_user')}:{os.getenv('MYSQL_PASSWORD', 'portfolio_pass')}@"
    f"{os.getenv('MYSQL_HOST', 'db')}/{os.getenv('MYSQL_DATABASE', 'portfolio_db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify({"error": "Invalid token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return jsonify({"error": "No token provided"}), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Fresh token required"}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has been revoked"}), 401

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    logger.debug("Checking token in blocklist")
    return False  # For now, we're not implementing a token blocklist

def debug_jwt_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            logger.debug("Headers received: %s", dict(request.headers))
            auth_header = request.headers.get('Authorization')
            logger.debug("Authorization header: %s", auth_header)
            
            if not auth_header:
                logger.error("No Authorization header found")
                return jsonify({"error": "No Authorization header"}), 401
                
            try:
                # Split header into parts for more detailed logging
                parts = auth_header.split()
                if len(parts) != 2 or parts[0] != 'Bearer':
                    logger.error("Invalid Authorization header format")
                    return jsonify({"error": "Invalid Authorization header format"}), 401
                    
                token = parts[1]
                logger.debug("Token extracted from header: %s", token)
                
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                logger.debug("JWT verified successfully. User ID: %s", current_user_id)
                return fn(*args, **kwargs)
            except Exception as e:
                logger.error("JWT verification failed: %s", str(e), exc_info=True)
                return jsonify({"error": "Invalid or missing token"}), 401
        return decorator
    return wrapper

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(512))
    github_url = db.Column(db.String(512))
    live_url = db.Column(db.String(512))
    tech_stack = db.Column(db.JSON)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.TIMESTAMP, 
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Error handlers
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized"}), 401

# Authentication endpoints
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Convert user.id to string for JWT subject
            access_token = create_access_token(identity=str(user.id))
            logger.info(f"Successful login for user: {username}")
            logger.debug(f"Generated token: {access_token}")
            
            response = jsonify({
                'message': 'Login successful',
                'token': access_token,
                'user': {'username': user.username}
            })
            return response
        
        logger.warning(f"Failed login attempt for user: {username}")
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    try:
        # Log headers for debugging
        logger.info("Auth check headers:")
        for header, value in request.headers.items():
            logger.info(f"{header}: {value}")
            
        # Try to verify the JWT token
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            logger.info(f"JWT verification passed. User ID: {current_user_id}")
            
            user = User.query.get(current_user_id)
            if user:
                return jsonify({
                    'authenticated': True,
                    'user': {'username': user.username}
                })
            return jsonify({'authenticated': False}), 401
            
        except Exception as jwt_error:
            logger.info(f"JWT verification failed: {str(jwt_error)}")
            return jsonify({'authenticated': False, 'error': str(jwt_error)}), 401
            
    except Exception as e:
        logger.error(f"Auth check error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# API routes for database management
@app.route('/api/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        try:
            projects = Project.query.order_by(Project.created_at.desc()).all()
            return jsonify([{
                'id': p.id,
                'title': p.title,
                'description': p.description,
                'image_url': p.image_url,
                'github_url': p.github_url,
                'live_url': p.live_url,
                'tech_stack': p.tech_stack,
                'created_at': p.created_at.isoformat() if p.created_at else None
            } for p in projects])
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
    
    @debug_jwt_required()
    def create_project():
        try:
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return jsonify({'error': 'Unauthorized'}), 401
                
            data = request.get_json()
            project = Project(
                title=data['title'],
                description=data['description'],
                image_url=data.get('image_url'),
                github_url=data.get('github_url'),
                live_url=data.get('live_url'),
                tech_stack=data.get('tech_stack', [])
            )
            db.session.add(project)
            db.session.commit()
            logger.info(f"Project created: {project.title}")
            return jsonify({
                'id': project.id,
                'message': 'Project created successfully'
            }), 201
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
    
    return create_project()

@app.route('/api/projects/<int:id>', methods=['DELETE'])
@debug_jwt_required()
def delete_project(id):
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'Unauthorized'}), 401
            
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        logger.info(f"Project deleted: {id}")
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/skills', methods=['GET', 'POST'])
def skills():
    if request.method == 'GET':
        try:
            skills = Skill.query.order_by(Skill.category, Skill.name).all()
            return jsonify([{
                'id': s.id,
                'name': s.name,
                'category': s.category,
                'proficiency': s.proficiency,
                'created_at': s.created_at.isoformat() if s.created_at else None
            } for s in skills])
        except Exception as e:
            logger.error(f"Error fetching skills: {str(e)}", exc_info=True)
            return jsonify({'error': 'Internal server error'}), 500
    
    # POST method requires authentication
    try:
        # Log headers for debugging
        logger.info("Request headers:")
        for header, value in request.headers.items():
            logger.info(f"{header}: {value}")
            
        logger.info("Verifying JWT token...")
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        logger.info(f"JWT verification passed. User ID: {current_user_id}")
        
        logger.info("Getting request data...")
        data = request.get_json()
        logger.info(f"Received skill data: {data}")
        
        if not data:
            logger.error("No data provided in request")
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['name', 'category', 'proficiency']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400

        logger.info("Creating new skill...")
        skill = Skill(
            name=data['name'],
            category=data['category'],
            proficiency=data['proficiency']
        )
        logger.info("Adding skill to session...")
        db.session.add(skill)
        logger.info("Committing to database...")
        db.session.commit()
        logger.info(f"New skill added successfully: {skill.name}")
        
        return jsonify({
            'id': skill.id,
            'name': skill.name,
            'category': skill.category,
            'proficiency': skill.proficiency,
            'created_at': skill.created_at.isoformat() if skill.created_at else None
        }), 201
    except Exception as e:
        logger.error(f"Error adding skill: {str(e)}", exc_info=True)
        if 'Missing Authorization Header' in str(e):
            return jsonify({'error': 'Missing Authorization header'}), 401
        elif 'Invalid header string' in str(e):
            return jsonify({'error': 'Invalid Authorization header format'}), 401
        elif 'token_type_claim' in str(e):
            return jsonify({'error': 'Invalid token type'}), 401
        elif 'expired_token' in str(e):
            return jsonify({'error': 'Token has expired'}), 401
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills/<int:id>', methods=['DELETE'])
@debug_jwt_required()
def delete_skill(id):
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': 'Unauthorized'}), 401
            
        skill = Skill.query.get_or_404(id)
        db.session.delete(skill)
        db.session.commit()
        logger.info(f"Skill deleted: {id}")
        return '', 204
    except Exception as e:
        logger.error(f"Error deleting skill: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/profile', methods=['GET'])
def get_profile():
    try:
        return jsonify({
            'name': 'Jacob Hyde',
            'title': 'Full Stack Developer',
            'bio': 'Passionate about building web applications and solving complex problems.'
        })
    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
