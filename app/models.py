from enum import Enum
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
    position = db.Column(db.String(100), nullable=False)  # الوظيفة
    salary = db.Column(db.Numeric(10, 2), default=0)  # المرتب
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
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=True)  # رقم الوردية (ربط مع جدول الورديات)
    insurance_deduction = db.Column(db.Numeric(10, 2), default=0)  # خصم التأمينات
    allowances = db.Column(db.Numeric(10, 2), default=0)  # البدلات
    date_of_joining = db.Column(db.Date, nullable=True)  # موعد التعيين
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # تاريخ الإضافة
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # تاريخ التحديث

    # Relationship with Shifts (Optional)

    def __repr__(self):
        return f"<Employee {self.full_name} - {self.position}>"
from app import db
from datetime import time

class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # اسم الوردية
    start_time = db.Column(db.Time, nullable=False)  # ساعة الدخول
    end_time = db.Column(db.Time, nullable=False)  # ساعة الخروج
    description = db.Column(db.Text, nullable=True)  # وصف اختياري


    def __init__(self, name, start_time, end_time, description=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.description = description

    def __repr__(self):
        return f"<Shift {self.name} ({self.start_time} - {self.end_time})>"

