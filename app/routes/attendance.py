from datetime import datetime, timedelta,time
from flask import Blueprint, request, jsonify
from app import db
from app.models import Attendance, Employee
from app.utils import token_required

attendance_bp = Blueprint('attendance', __name__)

# Create Attendance
@attendance_bp.route('/api/attendances', methods=['POST'])
@token_required
def create_attendance(user_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['empId']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    attendance = Attendance(
        empId=data['empId'],
        checkInTime=data['checkInTime'],  # تأكد من أن القيمة في الصيغة الصحيحة
        checkOutTime=data['checkOutTime'],  # تأكد من أن القيمة في الصيغة الصحيحة
        productionQuantity=data.get('productionQuantity', 0)
    )
    db.session.add(attendance)
    db.session.commit()

    return jsonify({'message': 'Attendance created', 'attendance': {
        'id': attendance.id,
        'empId': attendance.empId,
        'checkInTime': str(attendance.checkInTime),  # Convert to string
        'checkOutTime': str(attendance.checkOutTime) if attendance.checkOutTime else None,  # Convert to string
        'createdAt': str(attendance.createdAt)  # Ensure it's a string
    }}), 201


# Get All Attendances
@attendance_bp.route('/api/attendances', methods=['GET'])
@token_required
def get_all_attendances(user_id):
    attendances = Attendance.query.all()
    return jsonify([{
        'id': att.id,
        'empId': att.empId,
        'checkInTime': str(att.checkInTime),
        'checkOutTime': str(att.checkOutTime) if att.checkOutTime else None,
        'productionQuantity': att.productionQuantity,
        'createdAt': str(att.createdAt)
    } for att in attendances]), 200


# Get Attendance by ID
@attendance_bp.route('/api/attendances/<int:id>', methods=['GET'])
@token_required
def get_attendance(user_id, id):
    attendance = Attendance.query.get(id)

    if not attendance:
        return jsonify({'message': 'Attendance not found'}), 404

    return jsonify({
        'id': attendance.id,
        'empId': attendance.empId,
        'checkInTime': str(attendance.checkInTime),  # Convert to string
        'checkOutTime': str(attendance.checkOutTime) if attendance.checkOutTime else None,  # Convert to string
        'productionQuantity': attendance.productionQuantity,
        'createdAt': str(attendance.createdAt)  # Ensure it's a string
    }), 200


# Update Attendance
@attendance_bp.route('/api/attendances/<int:id>', methods=['PUT'])
@token_required
def update_attendance(user_id, id):
    attendance = Attendance.query.get(id)

    if not attendance:
        return jsonify({'message': 'Attendance not found'}), 404

    data = request.get_json()

    for key, value in data.items():
        if hasattr(attendance, key):
            setattr(attendance, key, value)

    db.session.commit()

    return jsonify({'message': 'Attendance updated', 'attendance': {
        'id': attendance.id,
        'empId': attendance.empId,
        'checkInTime': str(attendance.checkInTime),  # Convert to string
        'checkOutTime': str(attendance.checkOutTime) if attendance.checkOutTime else None,  # Convert to string
        'createdAt': str(attendance.createdAt)  # Ensure it's a string
    }}), 200


# Delete Attendance
@attendance_bp.route('/api/attendances/<int:id>', methods=['DELETE'])
@token_required
def delete_attendance(user_id, id):
    attendance = Attendance.query.get(id)

    if not attendance:
        return jsonify({'message': 'Attendance not found'}), 404

    db.session.delete(attendance)
    db.session.commit()

    return jsonify({'message': 'Attendance deleted'}), 200

# Check-in Attendance for Employee
@attendance_bp.route('/api/attendances/checkin', methods=['POST'])
@token_required
def check_in(user_id):
    data = request.get_json()

    # Validate required fields
    if 'empId' not in data:
        return jsonify({'message': 'Employee ID is required'}), 400

    # Get employee from empId
    employee = Employee.query.get(data['empId'])
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    # Get current time for check-in
    check_in_time = datetime.now().time()

    # Create Attendance record
    attendance = Attendance(
        empId=data['empId'],
        checkInTime=check_in_time,  # Add the current check-in time
        checkOutTime=None,  # Assuming check-out time will be added later
        productionQuantity=data.get('productionQuantity')  # Optional field
    )
    db.session.add(attendance)
    db.session.commit()

    return jsonify({'message': 'Check-in successful', 'attendance': {
        'id': attendance.id,
        'empId': attendance.empId,
        'createdAt': str(attendance.createdAt),
        'checkInTime': str(attendance.checkInTime),
        'productionQuantity': attendance.productionQuantity
    }}), 201
# Get Attendance by Employee ID (empId)
@attendance_bp.route('/api/attendances/employee/<int:empId>', methods=['GET'])
@token_required
def get_attendance_by_empId(user_id, empId):
    # البحث عن حضور الموظف حسب empId
    attendances = Attendance.query.filter_by(empId=empId).all()

    if not attendances:
        return jsonify({'message': 'No attendance records found for this employee'}), 404

    return jsonify([{
        'id': att.id,
        'empId': att.empId,
        'checkInTime': str(att.checkInTime),
        'checkOutTime': str(att.checkOutTime) if att.checkOutTime else None,
        'productionQuantity': att.productionQuantity,
        'createdAt': str(att.createdAt)
    } for att in attendances]), 200


# Get Attendance within Date Range (startDate to endDate)
@attendance_bp.route('/api/attendances/range', methods=['GET'])
@token_required
def get_attendance_by_date_range(user_id):
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if not start_date or not end_date:
        return jsonify({'message': 'Both startDate and endDate are required'}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD'}), 400

    attendances = Attendance.query.filter(Attendance.createdAt >= start_date, Attendance.createdAt <= end_date).all()

    if not attendances:
        return jsonify({'message': 'No attendance records found for the given date range'}), 404

    return jsonify([{
        'id': att.id,
        'empId': att.empId,
        'checkInTime': str(att.checkInTime),
        'checkOutTime': str(att.checkOutTime) if att.checkOutTime else None,
        'productionQuantity': att.productionQuantity,
        'createdAt': str(att.createdAt)
    } for att in attendances]), 200
# Set Check-Out Time for Latest Attendance and Update Production Quantity
@attendance_bp.route('/api/attendances/checkout', methods=['POST'])
@token_required
def check_out(user_id):
    data = request.get_json()

    # Validate required fields
    if 'empId' not in data:
        return jsonify({'message': 'Employee ID is required'}), 400

    # Get employee from empId
    employee = Employee.query.get(data['empId'])
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    # Get the latest attendance for the employee
    latest_attendance = Attendance.query.filter_by(empId=data['empId']).order_by(Attendance.createdAt.desc()).first()

    if not latest_attendance:
        return jsonify({'message': 'No attendance records found for this employee'}), 404

    # Check if the employee already has a check-out time
    if latest_attendance.checkOutTime:
        return jsonify({'message': 'Check-out time already recorded for the latest attendance'}), 400

    # Get current time for check-out
    check_out_time = datetime.now().time()

    # Update check-out time
    latest_attendance.checkOutTime = check_out_time

    # Update production quantity if provided
    if 'productionQuantity' in data:
        latest_attendance.productionQuantity = data['productionQuantity']

    db.session.commit()

    return jsonify({'message': 'Check-out time set successfully', 'attendance': {
        'id': latest_attendance.id,
        'empId': latest_attendance.empId,
        'createdAt': str(latest_attendance.createdAt),
        'checkInTime': str(latest_attendance.checkInTime),
        'checkOutTime': str(latest_attendance.checkOutTime),
        'productionQuantity': latest_attendance.productionQuantity
    }}), 200
from sqlalchemy import func

# Get Attendance Summary for All Employees on a Specific Date
@attendance_bp.route('/api/attendances/summary', methods=['GET'])
@token_required
def get_all_attendance_summary(user_id):
    # Get date parameter from request
    date_str = request.args.get('startDate')  # Format: YYYY-MM-DD
    if not date_str:
        return jsonify({'message': 'Date parameter is required'}), 400

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD'}), 400

    # Get all attendance records for the given date using SQLAlchemy's func.date to extract the date part
    attendances = Attendance.query.filter(
        Attendance.createdAt== target_date
    ).all()

    if not attendances:
        return jsonify({'message': 'No attendance records found for the given date'}), 404

    result = []

    # Loop through all employees' attendance records
    for empId in set(att.empId for att in attendances):  # Loop through unique empIds
        # Filter attendances for each employee
        employee_attendances = [att for att in attendances if att.empId == empId]

        # Calculate First Check-In Time and Last Check-Out Time
        first_check_in = min(att.checkInTime for att in employee_attendances)
        last_check_out = max(att.checkOutTime for att in employee_attendances if att.checkOutTime)

        # Calculate Total Break Time and Total Work Time
        total_break_time = timedelta()  # Time spent on breaks
        total_work_time = timedelta()  # Time spent working

        for i in range(1, len(employee_attendances)):
            # Calculate break time between check-out and next check-in
            if employee_attendances[i].checkInTime and employee_attendances[i-1].checkOutTime:
                check_in_seconds = time_to_seconds(employee_attendances[i].checkInTime)
                check_out_seconds = time_to_seconds(employee_attendances[i-1].checkOutTime)

                # Calculate the break time in seconds
                break_time_seconds = check_in_seconds - check_out_seconds

                # Convert to timedelta (optional, but useful if you need a readable format)
                break_time = timedelta(seconds=break_time_seconds)                
                total_break_time += break_time

        # Calculate total work time (from first check-in to last check-out)
        if first_check_in and last_check_out:
           first_check_in_seconds = time_to_seconds(first_check_in)
           last_check_out_seconds = time_to_seconds(last_check_out)

                # Calculate the total work time in seconds
           total_work_time_seconds = last_check_out_seconds - first_check_in_seconds

                # Convert to timedelta if needed
           total_work_time = timedelta(seconds=total_work_time_seconds)

        # Format total break time and work time into hours and minutes
        total_break_hours, total_break_minutes = divmod(total_break_time.seconds, 3600)
        total_break_minutes //= 60

        total_work_hours, total_work_minutes = divmod(total_work_time.seconds, 3600)
        total_work_minutes //= 60

        # Add the result for this employee
        result.append({
            'empId': empId,
            'date': date_str,
            'firstCheckIn': str(first_check_in),
            'lastCheckOut': str(last_check_out) if last_check_out else None,
            'totalBreakTime': f"{total_break_hours} hours {total_break_minutes} minutes",
            'totalWorkTime': f"{total_work_hours} hours {total_work_minutes} minutes"
        })

    return jsonify(result), 200
def time_to_seconds(t):
    """Convert a time object to seconds since midnight."""
    return t.hour * 3600 + t.minute * 60 + t.second