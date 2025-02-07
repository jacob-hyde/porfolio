from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..models.models import User, db
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"message": "Missing username or password"}), 400

        username = data['username']
        password = data['password']
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            logger.warning(f"Failed login attempt for user: {username}")
            return jsonify({"message": "Invalid username or password"}), 401

        access_token = create_access_token(identity=username)
        logger.info(f"Successful login for user: {username}")
        
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": {"username": username}
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"message": "An error occurred during login"}), 500

@auth_bp.route('/api/check-auth', methods=['GET'])
@jwt_required()
def check_auth():
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        
        if not user:
            return jsonify({
                "authenticated": False,
                "message": "User not found"
            }), 401

        return jsonify({
            "authenticated": True,
            "user": {"username": current_user}
        }), 200
        
    except Exception as e:
        logger.error(f"Auth check error: {str(e)}")
        return jsonify({
            "authenticated": False,
            "message": "Authentication failed"
        }), 401
