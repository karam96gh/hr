import datetime
from enum import Enum

from sqlalchemy import JSON
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    fingerprint_id = db.Column(db.String(50), nullable=False)  # رقم الموظف على جهاز البصمة
    full_name = db.Column(db.String(255), nullable=False)  # الاسم الرباعي
    position = db.Column(db.Integer, db.ForeignKey('job_titles.id'), nullable=False)  # ربط مع جدول المسمى الوظيفي
    salary = db.Column(db.Numeric(10, 2), default=0)  # المرتب
    advancePercentage = db.Column(db.Numeric(5, 2), nullable=True)  # حقل نسبة السلفة
    work_system = db.Column(db.String(100), nullable=True)  # نظام العمل
    certificates = db.Column(db.Text, nullable=True)  # الشهادات الحاصل عليها
    date_of_birth = db.Column(db.Date, nullable=True)  # تاريخ الولادة
    place_of_birth = db.Column(db.String(255), nullable=True)  # مكان الولادة
    id_card_number = db.Column(db.String(50), nullable=True)  # رقم البطاقة
    national_id = db.Column(db.String(50), nullable=True)  # الرقم الوطني
    residence = db.Column(db.String(255), nullable=True)  # مكان الإقامة
    mobile_1 = db.Column(db.String(15), nullable=True)  # رقم الموبايل 1
    mobile_2 = db.Column(db.String(15), nullable=True)  # رقم الموبايل 2
    mobile_3 = db.Column(db.String(15), nullable=True)  # رقم الموبايل 3
    worker_agreement = db.Column(db.Text, nullable=True)  # اتفاق العامل
    notes = db.Column(db.Text, nullable=True)  # ملاحظات
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=True)  # رقم الوردية (ربط مع جدول الورديات)
    insurance_deduction = db.Column(db.Numeric(10, 2), default=0)  # خصم التأمينات
    allowances = db.Column(db.Numeric(10, 2), default=0)  # البدلات
    date_of_joining = db.Column(db.Date, nullable=True)  # موعد التعيين
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # تاريخ الإضافة
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # تاريخ التحديث

    # Relationship with Shifts (Optional)
    job_title = db.relationship('JobTitle', backref='employees', lazy=True)

    def __repr__(self):
        return f"<Employee {self.full_name} - {self.position}>"


from app import db
from datetime import date, time

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID تلقائي
    name = db.Column(db.String(100), nullable=False)  # اسم الوردية
    start_time = db.Column(db.Time, nullable=False)  # وقت البداية
    end_time = db.Column(db.Time, nullable=False)  # وقت النهاية
    allowed_delay_minutes = db.Column(db.Integer, nullable=False, default=0)  # فترة التأخير المسموحة بالدقائق
    allowed_exit_minutes = db.Column(db.Integer, nullable=False, default=0)  # فترة الخروج المسموحة
    note = db.Column(db.Text, nullable=True)  # ملاحظة
    absence_minutes = db.Column(db.Integer, nullable=False, default=0)  # فترة الغياب بالدقائق
    extra_minutes = db.Column(db.Integer, nullable=False, default=0)  # فترة الإضافي بالدقائق

    def __repr__(self):
        return f"<Shift {self.name}>"
    
class JobTitle(db.Model):
    __tablename__ = 'job_titles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID تلقائي
    title_name = db.Column(db.String(100), nullable=False)  # اسم المسمى الوظيفي
    allowed_break_time = db.Column(db.String(5), nullable=True)  # عدد ساعات الاستراحة (صيغة HH:MM)
    overtime_hour_value = db.Column(db.Numeric(10, 2), nullable=True)  # قيمة ساعة الإضافي
    delay_minute_value = db.Column(db.Numeric(10, 2), nullable=True)  # قيمة دقيقة التأخير
    production_system = db.Column(db.Boolean, nullable=False, default=False)  # نظام كمية الإنتاج
    shift_system = db.Column(db.Boolean, nullable=False, default=False)  # نظام الورديات
    production_piece_value = db.Column(db.Numeric(10, 2), nullable=True)  # سعر قطعة الإنتاج
    
    def __repr__(self):
        return f"<JobTitle {self.title_name}>"
    
class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID تلقائي
    empId = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)  # ForeignKey من جدول Employee
    createdAt = db.Column(db.Date, default=date.today)  # تاريخ التسجيل فقط
    checkInTime = db.Column(db.Time, nullable=True)  # وقت الحضور فقط (صيغة الوقت)
    checkOutTime = db.Column(db.Time, nullable=True)  # وقت الانصراف فقط (صيغة الوقت)
    # علاقات بين الجداول (لمزيد من التفاعل مع جدول Employee)
    employee = db.relationship('Employee', backref='attendances', lazy=True)

    def __repr__(self):
        return f"<Attendance {self.id}, Employee {self.empId}>"
    
class Advance(db.Model):
    __tablename__ = 'advances'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    document_number = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # Relationship
    employee = db.relationship('Employee', backref='advances', lazy=True)

    def __repr__(self):
        return f"<Advance {self.id}, Employee {self.employee_id}>"


class ProductionPiece(db.Model):
    __tablename__ = 'production_pieces'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    piece_number = db.Column(db.String(50), unique=True, nullable=False)  # رقم القطعة
    piece_name = db.Column(db.String(255), nullable=False)  # اسم القطعة
    price_levels = db.Column(JSON, nullable=False)  # تخزين أسعار المستويات كـ JSON
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<ProductionPiece {self.piece_name}>"
    

class ProductionMonitoring(db.Model):
    __tablename__ = 'production_monitoring'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    piece_id = db.Column(db.Integer, db.ForeignKey('production_pieces.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    quantity = db.Column(db.Integer, nullable=False)  # عدد القطع
    quality_grade = db.Column(db.String(1), nullable=False)  # مستوى الجودة (A, B, C, D, E)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    notes = db.Column(db.Text, nullable=True)  # ملاحظات إضافية

    # العلاقات
    employee = db.relationship('Employee', backref='production_monitoring', lazy=True)
    piece = db.relationship('ProductionPiece', backref='production_monitoring', lazy=True)

    def __repr__(self):
        return f"<ProductionMonitoring Employee: {self.employee_id}, Piece: {self.piece_id}, Quantity: {self.quantity}, Grade: {self.quality_grade}>"