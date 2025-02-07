from flask import Flask
from flask_cors import CORS
import logging

from .config.config import Config
from .models.models import db
from .auth.auth import jwt, init_jwt_handlers
from .routes.auth_routes import auth_bp
from .routes.project_routes import projects_bp
from .routes.skill_routes import skills_bp
from .routes.profile_routes import profile_bp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app, resources=app.config['CORS_RESOURCES'])
    db.init_app(app)
    jwt.init_app(app)
    init_jwt_handlers(jwt)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(profile_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {"message": "Resource not found"}, 404

    @app.errorhandler(401)
    def unauthorized_error(error):
        return {"message": "Unauthorized"}, 401

    @app.errorhandler(500)
    def handle_error(error):
        logger.error(f"Server error: {str(error)}")
        return {"message": "Internal server error"}, 500

    return app
