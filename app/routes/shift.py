from datetime import time
from flask import Blueprint, request, jsonify
from app import db
from app.models import Shift
from app.utils import token_required

shift_bp = Blueprint('shift', __name__)

# Create Shift
@shift_bp.route('/api/shifts', methods=['POST'])
@token_required
def create_shift(user_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'start_time', 'end_time', 'allowed_delay_minutes', 
                       'allowed_exit_minutes', 'absence_minutes', 'extra_minutes']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    shift = Shift(
        name=data['name'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        allowed_delay_minutes=data['allowed_delay_minutes'],
        allowed_exit_minutes=data['allowed_exit_minutes'],
        note=data.get('note'),
        absence_minutes=data['absence_minutes'],
        extra_minutes=data['extra_minutes']
    )
    db.session.add(shift)
    db.session.commit()

    return jsonify({'message': 'Shift created', 'shift': {
        'id': shift.id,
        'name': shift.name
    }}), 201


# Get All Shifts

@shift_bp.route('/api/shifts', methods=['GET'])
@token_required
def get_all_shifts(user_id):
    shifts = Shift.query.all()  # Assuming you're using SQLAlchemy
    return jsonify([{
        key: (value.strftime('%H:%M:%S') if isinstance(value, time) else value)
        for key, value in shift.__dict__.items()
        if not key.startswith('_')  # Exclude internal attributes like _sa_instance_state
    } for shift in shifts]), 200


# Get Shift by ID
@shift_bp.route('/api/shifts/<int:id>', methods=['GET'])
@token_required
def get_shift(user_id, id):
    shift = Shift.query.get(id)

    if not shift:
        return jsonify({'message': 'Shift not found'}), 404

    return jsonify({
        'id': shift.id,
        'name': shift.name,
         'start_time': shift.start_time.strftime('%H:%M:%S') if shift.start_time else None,
        'end_time': shift.end_time.strftime('%H:%M:%S') if shift.end_time else None,
        'allowed_delay_minutes': shift.allowed_delay_minutes,
        'allowed_exit_minutes': shift.allowed_exit_minutes,
        'note': shift.note,
        'absence_minutes': shift.absence_minutes,
        'extra_minutes': shift.extra_minutes
    }), 200


# Update Shift
@shift_bp.route('/api/shifts/<int:id>', methods=['PUT'])
@token_required
def update_shift(user_id, id):
    shift = Shift.query.get(id)

    if not shift:
        return jsonify({'message': 'Shift not found'}), 404

    data = request.get_json()

    for key, value in data.items():
        if hasattr(shift, key):
            setattr(shift, key, value)

    db.session.commit()

    return jsonify({'message': 'Shift updated', 'shift': {
        'id': shift.id,
        'name': shift.name
    }}), 200


# Delete Shift
@shift_bp.route('/api/shifts/<int:id>', methods=['DELETE'])
@token_required
def delete_shift(user_id, id):
    shift = Shift.query.get(id)

    if not shift:
        return jsonify({'message': 'Shift not found'}), 404

    db.session.delete(shift)
    db.session.commit()

    return jsonify({'message': 'Shift deleted'}), 200
