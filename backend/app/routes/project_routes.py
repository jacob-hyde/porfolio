from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..models.models import Project, db
import logging

logger = logging.getLogger(__name__)
projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/api/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        try:
            projects = Project.query.all()
            return jsonify([{
                'id': p.id,
                'title': p.title,
                'description': p.description,
                'image_url': p.image_url,
                'github_url': p.github_url,
                'live_url': p.live_url,
                'tech_stack': p.tech_stack,
                'created_at': p.created_at.isoformat() if p.created_at else None
            } for p in projects]), 200
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}")
            return jsonify({"message": "Error fetching projects"}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            new_project = Project(
                title=data['title'],
                description=data.get('description', ''),
                image_url=data.get('image_url', ''),
                github_url=data.get('github_url', ''),
                live_url=data.get('live_url', ''),
                tech_stack=data.get('tech_stack', [])
            )
            
            db.session.add(new_project)
            db.session.commit()
            
            return jsonify({
                'id': new_project.id,
                'title': new_project.title,
                'description': new_project.description,
                'image_url': new_project.image_url,
                'github_url': new_project.github_url,
                'live_url': new_project.live_url,
                'tech_stack': new_project.tech_stack,
                'created_at': new_project.created_at.isoformat()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating project: {str(e)}")
            return jsonify({"message": "Error creating project"}), 500

@projects_bp.route('/api/projects/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_project(id):
    try:
        project = Project.query.get(id)
        if not project:
            return jsonify({"message": "Project not found"}), 404
            
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting project: {str(e)}")
        return jsonify({"message": "Error deleting project"}), 500
