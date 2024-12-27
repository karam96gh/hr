from flask import Blueprint, request, jsonify
from app import db
from app.models import Employee
from app.utils import token_required

employee_bp = Blueprint('employee', __name__)

# Create Employee
@employee_bp.route('/api/employees', methods=['POST'])
@token_required
def create_employee(user_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['fingerprint_id', 'full_name', 'position', 'work_system']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    employee = Employee(
        fingerprint_id=data['fingerprint_id'],
        full_name=data['full_name'],
        position=data['position'],
        salary=data.get('salary', 0),
        work_system=data['work_system'],
        certificates=data.get('certificates'),
        date_of_birth=data.get('date_of_birth'),
        place_of_birth=data.get('place_of_birth'),
        id_card_number=data.get('id_card_number'),
        national_id=data.get('national_id'),
        residence=data.get('residence'),
        mobile_1=data.get('mobile_1'),
        mobile_2=data.get('mobile_2'),
        mobile_3=data.get('mobile_3'),
        worker_agreement=data.get('worker_agreement'),
        notes=data.get('notes'),
        shift_id=data.get('shift_id'),
        insurance_deduction=data.get('insurance_deduction', 0),
        allowances=data.get('allowances', 0),
        date_of_joining=data.get('date_of_joining')
    )
    db.session.add(employee)
    db.session.commit()

    return jsonify({'message': 'Employee created', 'employee': {
        'id': employee.id,
        'full_name': employee.full_name,
        'position': employee.position
    }}), 201


# Get All Employees
@employee_bp.route('/api/employees', methods=['GET'])
@token_required
def get_all_employees(user_id):
    employees = Employee.query.all()
    return jsonify([{
        key: value for key, value in emp.__dict__.items() 
        if not key.startswith('_')  # Exclude internal attributes like _sa_instance_state
    } for emp in employees]), 200


# Get Employee by ID
@employee_bp.route('/api/employees/<int:id>', methods=['GET'])
@token_required
def get_employee(user_id, id):
    employee = Employee.query.get(id)

    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    return jsonify({
        'id': employee.id,
        'fingerprint_id': employee.fingerprint_id,
        'full_name': employee.full_name,
        'position': employee.position,
        'salary': employee.salary,
        'work_system': employee.work_system,
        'certificates': employee.certificates,
        'date_of_birth': employee.date_of_birth,
        'place_of_birth': employee.place_of_birth,
        'id_card_number': employee.id_card_number,
        'national_id': employee.national_id,
        'residence': employee.residence,
        'mobile_1': employee.mobile_1,
        'mobile_2': employee.mobile_2,
        'mobile_3': employee.mobile_3,
        'worker_agreement': employee.worker_agreement,
        'notes': employee.notes
    }), 200


# Update Employee
@employee_bp.route('/api/employees/<int:id>', methods=['PUT'])
@token_required
def update_employee(user_id, id):
    employee = Employee.query.get(id)

    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    data = request.get_json()

    for key, value in data.items():
        if hasattr(employee, key):
            setattr(employee, key, value)

    db.session.commit()

    return jsonify({'message': 'Employee updated', 'employee': {
        'id': employee.id,
        'full_name': employee.full_name,
        'position': employee.position
    }}), 200


# Delete Employee
@employee_bp.route('/api/employees/<int:id>', methods=['DELETE'])
@token_required
def delete_employee(user_id, id):
    employee = Employee.query.get(id)

    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({'message': 'Employee deleted'}), 200
