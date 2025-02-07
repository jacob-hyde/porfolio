from flask import Blueprint, jsonify
from ..models.models import User, Skill
import logging

logger = logging.getLogger(__name__)
profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
def get_profile():
    try:
        # For now, we'll return a static profile
        # In the future, this could be made dynamic and stored in the database
        skills = Skill.query.all()
        
        return jsonify({
            'name': 'Jacob',
            'title': 'Full Stack Developer',
            'bio': 'Passionate about building beautiful and functional web applications',
            'skills': [{
                'id': s.id,
                'name': s.name,
                'category': s.category,
                'proficiency': s.proficiency
            } for s in skills]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching profile: {str(e)}")
        return jsonify({"message": "Error fetching profile"}), 500
