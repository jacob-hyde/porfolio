from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..models.models import Skill, db
import logging

logger = logging.getLogger(__name__)
skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/api/skills', methods=['GET', 'POST'])
def skills():
    if request.method == 'GET':
        try:
            skills = Skill.query.all()
            return jsonify([{
                'id': s.id,
                'name': s.name,
                'category': s.category,
                'proficiency': s.proficiency,
                'created_at': s.created_at.isoformat() if s.created_at else None
            } for s in skills]), 200
        except Exception as e:
            logger.error(f"Error fetching skills: {str(e)}")
            return jsonify({"message": "Error fetching skills"}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data or 'name' not in data or 'category' not in data:
                return jsonify({"message": "Missing required fields"}), 400
                
            new_skill = Skill(
                name=data['name'],
                category=data['category'],
                proficiency=data.get('proficiency', 0)
            )
            
            db.session.add(new_skill)
            db.session.commit()
            
            return jsonify({
                'id': new_skill.id,
                'name': new_skill.name,
                'category': new_skill.category,
                'proficiency': new_skill.proficiency,
                'created_at': new_skill.created_at.isoformat()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating skill: {str(e)}")
            return jsonify({"message": "Error creating skill"}), 500

@skills_bp.route('/api/skills/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_skill(id):
    try:
        skill = Skill.query.get(id)
        if not skill:
            return jsonify({"message": "Skill not found"}), 404
            
        db.session.delete(skill)
        db.session.commit()
        return jsonify({"message": "Skill deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting skill: {str(e)}")
        return jsonify({"message": "Error deleting skill"}), 500
