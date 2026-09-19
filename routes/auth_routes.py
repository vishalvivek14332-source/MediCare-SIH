from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from models.patient import Patient
from models.doctor import Doctor
from utils.helpers import success_response, error_response
from utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return error_response("Missing required fields")
    
    if not validate_email(data.get('email', '')):
        return error_response("Invalid email format")
    if not validate_password(data.get('password', '')):
        return error_response("Password must be at least 6 characters")
        
    if Patient.find_by_email(data['email']):
        return error_response("Email already registered")
        
    Patient.create(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', ''),
        password=data['password'],
        age=data.get('age'),
        gender=data.get('gender')
    )
    
    return success_response(message="Patient registered successfully", status=201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return error_response("Missing email or password")
        
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'patient') # patient, doctor, admin
    
    import json
    if role == 'patient':
        user = Patient.find_by_email(email)
        if user and Patient.verify_password(user, password):
            access_token = create_access_token(identity=json.dumps({"id": str(user['_id']), "role": "patient"}))
            return success_response(data={"access_token": access_token, "name": user['name']}, message="Login successful")
    elif role == 'doctor':
        user = Doctor.find_by_email(email)
        if user and Doctor.verify_password(user, password):
            access_token = create_access_token(identity=json.dumps({"id": str(user['_id']), "role": "doctor"}))
            return success_response(data={"access_token": access_token, "name": user['name']}, message="Login successful")
    elif role == 'main_admin':
        if email == 'admin@network.com' and password == 'admin123':
            access_token = create_access_token(identity=json.dumps({"id": "main_admin", "role": "main_admin"}))
            return success_response(data={"access_token": access_token, "name": "Main Administrator"}, message="Login successful")
    elif role == 'clinic_admin':
        from models.clinic import Clinic
        from database.db import mongo
        clinic = mongo.db.clinics.find_one({"email": email})
        if clinic and Clinic.verify_password(clinic, password):
            access_token = create_access_token(identity=json.dumps({"id": str(clinic['_id']), "role": "clinic_admin", "clinic_id": str(clinic['_id'])}))
            return success_response(data={"access_token": access_token, "name": clinic.get('name', 'Clinic Admin')}, message="Login successful")
    return error_response("Invalid credentials", status=401)
