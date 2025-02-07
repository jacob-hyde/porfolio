from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from functools import wraps
import logging

from ..models.models import User

jwt = JWTManager()
logger = logging.getLogger(__name__)

def init_jwt_handlers(jwt):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({"message": "Invalid token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({"message": "Missing token"}), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Fresh token required"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has been revoked"}), 401

def debug_jwt_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            logger.debug(f"Auth header: {auth_header}")
            
            try:
                verify_jwt_in_request()
                current_user = get_jwt_identity()
                logger.debug(f"Current user: {current_user}")
                return fn(*args, **kwargs)
            except Exception as e:
                logger.error(f"JWT verification failed: {str(e)}")
                return jsonify({"message": "Authentication failed", "error": str(e)}), 401
        return decorated
    return wrapper
