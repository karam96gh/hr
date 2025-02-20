from flask import Blueprint, request, jsonify
from app import db
from app.models import Profession
from app.utils import token_required

profession_bp = Blueprint('profession', __name__)

# Create Profession
@profession_bp.route('/api/professions', methods=['POST'])
@token_required
def create_profession(user_id):
    data = request.get_json()

    required_fields = ['name', 'hourly_rate', 'daily_rate']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    profession = Profession(
        name=data['name'],
        hourly_rate=data['hourly_rate'],
        daily_rate=data['daily_rate']
    )
    db.session.add(profession)
    db.session.commit()

    return jsonify( {
        'id': profession.id,
        'name': profession.name,
        'hourly_rate': profession.hourly_rate,
        'daily_rate': profession.daily_rate
    }), 201

# Get All Professions
@profession_bp.route('/api/professions', methods=['GET'])
@token_required
def get_all_professions(user_id):
    professions = Profession.query.all()
    return jsonify([{key: value for key, value in profession.__dict__.items() if not key.startswith('_')} for profession in professions]), 200

# Get Profession by ID
@profession_bp.route('/api/professions/<int:id>', methods=['GET'])
@token_required
def get_profession(user_id, id):
    profession = Profession.query.get(id)
    if not profession:
        return jsonify({'message': 'Profession not found'}), 404

    return jsonify({
        'id': profession.id,
        'name': profession.name,
        'hourly_rate': profession.hourly_rate,
        'daily_rate': profession.daily_rate
    }), 200

# Update Profession
@profession_bp.route('/api/professions/<int:id>', methods=['PUT'])
@token_required
def update_profession(user_id, id):
    profession = Profession.query.get(id)
    if not profession:
        return jsonify({'message': 'Profession not found'}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(profession, key):
            setattr(profession, key, value)

    db.session.commit()

    return jsonify({
        'id': profession.id,
        'name': profession.name,
        'hourly_rate': profession.hourly_rate,
        'daily_rate': profession.daily_rate
    }), 200

# Delete Profession
@profession_bp.route('/api/professions/<int:id>', methods=['DELETE'])
@token_required
def delete_profession(user_id, id):
    profession = Profession.query.get(id)
    if not profession:
        return jsonify({'message': 'Profession not found'}), 404
    
    db.session.delete(profession)
    db.session.commit()
    
    return jsonify({'message': 'Profession deleted'}), 200