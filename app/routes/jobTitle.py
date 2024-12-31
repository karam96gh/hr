from flask import Blueprint, request, jsonify
from app import db
from app.models import JobTitle
from app.utils import token_required

job_title_bp = Blueprint('job_title', __name__)

# Create Job Title
@job_title_bp.route('/api/job_titles', methods=['POST'])
@token_required
def create_job_title(user_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['title_name', 'allowed_break_time', 'overtime_hour_value', 'delay_minute_value']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    job_title = JobTitle(
        title_name=data['title_name'],
        allowed_break_time=data['allowed_break_time'],
        overtime_hour_value=data['overtime_hour_value'],
        delay_minute_value=data['delay_minute_value']
    )
    db.session.add(job_title)
    db.session.commit()

    return jsonify({'message': 'Job Title created', 'job_title': {
        'id': job_title.id,
        'title_name': job_title.title_name
    }}), 201


# Get All Job Titles
@job_title_bp.route('/api/job_titles', methods=['GET'])
@token_required
def get_all_job_titles(user_id):
    job_titles = JobTitle.query.all()
    return jsonify([{
        key: value for key, value in job_title.__dict__.items()
        if not key.startswith('_')  # Exclude internal attributes like _sa_instance_state
    } for job_title in job_titles]), 200


# Get Job Title by ID
@job_title_bp.route('/api/job_titles/<int:id>', methods=['GET'])
@token_required
def get_job_title(user_id, id):
    job_title = JobTitle.query.get(id)

    if not job_title:
        return jsonify({'message': 'Job Title not found'}), 404

    return jsonify({
        'id': job_title.id,
        'title_name': job_title.title_name,
        'allowed_break_time': job_title.allowed_break_time,
        'overtime_hour_value': job_title.overtime_hour_value,
        'delay_minute_value': job_title.delay_minute_value
    }), 200


# Update Job Title
@job_title_bp.route('/api/job_titles/<int:id>', methods=['PUT'])
@token_required
def update_job_title(user_id, id):
    job_title = JobTitle.query.get(id)

    if not job_title:
        return jsonify({'message': 'Job Title not found'}), 404

    data = request.get_json()

    for key, value in data.items():
        if hasattr(job_title, key):
            setattr(job_title, key, value)

    db.session.commit()

    return jsonify({'message': 'Job Title updated', 'job_title': {
        'id': job_title.id,
        'title_name': job_title.title_name
    }}), 200


# Delete Job Title
@job_title_bp.route('/api/job_titles/<int:id>', methods=['DELETE'])
@token_required
def delete_job_title(user_id, id):
    job_title = JobTitle.query.get(id)

    if not job_title:
        return jsonify({'message': 'Job Title not found'}), 404

    db.session.delete(job_title)
    db.session.commit()

    return jsonify({'message': 'Job Title deleted'}), 200