from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.doctor import Doctor
from models.appointment import Appointment
from utils.helpers import success_response, error_response
from database.db import mongo
from bson.objectid import ObjectId

admin_bp = Blueprint('admin', __name__)

def is_main_admin():
    import json
    identity = json.loads(get_jwt_identity())
    return identity.get('role') == 'main_admin'

def is_clinic_admin():
    import json
    identity = json.loads(get_jwt_identity())
    return identity.get('role') == 'clinic_admin'

@admin_bp.route('/doctors', methods=['POST'])
@jwt_required()
def add_doctor():
    import json
    identity = json.loads(get_jwt_identity())
    if not (is_main_admin() or is_clinic_admin()): 
        return error_response("Unauthorized", status=403)
    
    data = request.get_json()
    if Doctor.find_by_email(data.get('email')):
        return error_response("Doctor email already exists")
        
    clinic_id = identity.get('clinic_id')
    
    Doctor.create(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        department=data['department'],
        specialization=data['specialization'],
        fees=data.get('fees', 0),
        total_tokens=data.get('total_tokens', 12),
        availability=data.get('availability', [])
    )
    
    if clinic_id:
        doc = mongo.db.doctors.find_one({"email": data['email']})
        if doc:
            mongo.db.doctors.update_one({"_id": doc['_id']}, {"$set": {"clinic_id": clinic_id}})

    from models.event import EventLog
    EventLog.log("DOCTOR_ADDED", f"Doctor {data['name']} added to the network.", role=identity.get('role'), clinic_id=clinic_id)

    return success_response(message="Doctor added successfully", status=201)

@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    import json
    identity = json.loads(get_jwt_identity())
    role = identity.get('role')
    
    if role not in ['main_admin', 'clinic_admin']:
        return error_response("Unauthorized", status=403)
        
    clinic_id = identity.get('clinic_id')
    
    if role == 'clinic_admin' and clinic_id:
        clinic_doctors = list(mongo.db.doctors.find({"clinic_id": clinic_id}, {"_id": 1}))
        doc_ids = [str(d['_id']) for d in clinic_doctors]
        
        total_patients = mongo.db.patients.count_documents({})
        total_doctors = len(doc_ids)
        total_appointments = mongo.db.appointments.count_documents({"doctor_id": {"$in": doc_ids}})
        completed_appointments = mongo.db.appointments.count_documents({"doctor_id": {"$in": doc_ids}, "status": "completed"})
    else:
        total_patients = mongo.db.patients.count_documents({})
        total_doctors = mongo.db.doctors.count_documents({})
        total_appointments = mongo.db.appointments.count_documents({})
        completed_appointments = mongo.db.appointments.count_documents({"status": "completed"})
        
    data = {
        "role": role,
        "patients": total_patients,
        "doctors": total_doctors,
        "appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "revenue": completed_appointments * 50
    }
    
    return success_response(data=data)

@admin_bp.route('/clinics', methods=['POST'])
@jwt_required()
def create_clinic():
    if not is_main_admin():
        return error_response("Only Main Admin can create clinics", status=403)
        
    data = request.get_json()
    from models.clinic import Clinic
    from models.event import EventLog
    
    result = Clinic.create(
        name=data['name'],
        address=data['address'],
        latitude=float(data['latitude']),
        longitude=float(data['longitude']),
        contact_number=data['contact_number'],
        code=data.get('code'),
        email=data.get('email'),
        password=data.get('password'),
        city=data.get('city'),
        state=data.get('state'),
        pincode=data.get('pincode'),
        booking_enabled=data.get('booking_enabled', True),
        queue_enabled=data.get('queue_enabled', True),
        emergency_support=data.get('emergency_support', False),
        max_doctors=data.get('max_doctors', 50)
    )
    
    EventLog.log("CLINIC_CREATED", f"Clinic {data['name']} created successfully", role="main_admin")
    return success_response(message="Clinic registered successfully", status=201)

@admin_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    if not is_main_admin():
        return error_response("Only Main Admin can view global events", status=403)
        
    from models.event import EventLog
    events = EventLog.get_recent(50)
    return success_response(data=events)

@admin_bp.route('/clinics/list', methods=['GET'])
@jwt_required()
def get_clinics_list():
    if not is_main_admin():
        return error_response("Unauthorized", status=403)
    from models.clinic import Clinic
    clinics = Clinic.get_all()
    # attach doctor counts
    for c in clinics:
        c['doctor_count'] = mongo.db.doctors.count_documents({"clinic_id": str(c['_id'])})
    return success_response(data=clinics)

@admin_bp.route('/occupancy', methods=['GET'])
@jwt_required()
def get_occupancy():
    if not (is_main_admin() or is_clinic_admin()):
        return error_response("Unauthorized", status=403)
    import json
    identity = json.loads(get_jwt_identity())
    
    if identity.get('role') == 'clinic_admin' and identity.get('clinic_id'):
        clinic_doctors = list(mongo.db.doctors.find({"clinic_id": identity.get('clinic_id')}))
    else:
        clinic_doctors = list(mongo.db.doctors.find())
        
    results = []
    for doc in clinic_doctors:
        # count pending appointments for this doctor today
        # We can just count all pending for now to match old logic
        count = mongo.db.appointments.count_documents({
            "doctor_id": str(doc['_id']), 
            "status": "pending"
        })
        
        clinic = mongo.db.clinics.find_one({"_id": ObjectId(doc.get("clinic_id"))}) if doc.get("clinic_id") else None
        
        results.append({
            "doctor_name": doc['name'],
            "clinic_name": clinic['name'] if clinic else "Unassigned",
            "department": doc['department'],
            "waiting": count,
            "max_tokens": doc.get('total_tokens', 12)
        })
        
    return success_response(data=results)

@admin_bp.route('/doctor/<doctor_id>/suspend', methods=['PATCH'])
@jwt_required()
def suspend_doctor(doctor_id):
    if not is_main_admin():
        return error_response("Only Main Admin can suspend", status=403)
    data = request.get_json()
    mongo.db.doctors.update_one({"_id": ObjectId(doctor_id)}, {"$set": {"is_suspended": data.get('suspend', True)}})
    return success_response(message="Doctor suspension updated")

@admin_bp.route('/doctors_list', methods=['GET'])
@jwt_required()
def get_doctors_list():
    if not (is_main_admin() or is_clinic_admin()):
        return error_response("Unauthorized", status=403)
        
    import json
    identity = json.loads(get_jwt_identity())
    
    query = {}
    if is_clinic_admin():
        query['clinic_id'] = identity.get('clinic_id')
        
    doctors = list(mongo.db.doctors.find(query))
    for d in doctors:
        d['_id'] = str(d['_id'])
        # Avoid exposing password hashes
        if 'password' in d:
            del d['password']
            
    return success_response(data=doctors)

@admin_bp.route('/clinic/me', methods=['GET'])
@jwt_required()
def get_my_clinic():
    if not is_clinic_admin():
        return error_response("Unauthorized", status=403)
        
    import json
    identity = json.loads(get_jwt_identity())
    clinic_id = identity.get('clinic_id')
    
    clinic = mongo.db.clinics.find_one({"_id": ObjectId(clinic_id)})
    if not clinic:
        return error_response("Clinic not found", status=404)
        
    clinic['_id'] = str(clinic['_id'])
    if 'password' in clinic:
        del clinic['password']
        
    return success_response(data=clinic)

@admin_bp.route('/clinic/me', methods=['PATCH'])
@jwt_required()
def update_my_clinic():
    if not is_clinic_admin():
        return error_response("Unauthorized", status=403)
        
    import json
    identity = json.loads(get_jwt_identity())
    clinic_id = identity.get('clinic_id')
    
    data = request.get_json()
    
    update_fields = {}
    if 'name' in data: update_fields['name'] = data['name']
    if 'contact_number' in data: update_fields['contact_number'] = data['contact_number']
    if 'booking_enabled' in data: update_fields['booking_enabled'] = data['booking_enabled']
    if 'queue_enabled' in data: update_fields['queue_enabled'] = data['queue_enabled']
    if 'emergency_support' in data: update_fields['emergency_support'] = data['emergency_support']
    
    if not update_fields:
        return error_response("No valid fields to update")
        
    mongo.db.clinics.update_one({"_id": ObjectId(clinic_id)}, {"$set": update_fields})
    
    from models.event import EventLog
    EventLog.log("CLINIC_UPDATED", f"Clinic updated settings", role="clinic_admin", clinic_id=clinic_id)
    
    return success_response(message="Clinic settings updated successfully")

@admin_bp.route('/doctor/<doctor_id>', methods=['PATCH'])
@jwt_required()
def update_doctor(doctor_id):
    if not (is_main_admin() or is_clinic_admin()):
        return error_response("Unauthorized", status=403)
        
    import json
    identity = json.loads(get_jwt_identity())
    
    query = {"_id": ObjectId(doctor_id)}
    if is_clinic_admin():
        query['clinic_id'] = identity.get('clinic_id')
        
    doctor = mongo.db.doctors.find_one(query)
    if not doctor:
        return error_response("Doctor not found or unauthorized", status=404)
        
    data = request.get_json()
    update_fields = {}
    if 'name' in data: update_fields['name'] = data['name']
    if 'department' in data: update_fields['department'] = data['department']
    if 'specialization' in data: update_fields['specialization'] = data['specialization']
    if 'fees' in data: update_fields['fees'] = int(data['fees'])
    if 'total_tokens' in data: update_fields['total_tokens'] = int(data['total_tokens'])
    if data.get('password'):
        from werkzeug.security import generate_password_hash
        update_fields['password'] = generate_password_hash(data['password'])
        
    if update_fields:
        mongo.db.doctors.update_one({"_id": ObjectId(doctor_id)}, {"$set": update_fields})
        
    from models.event import EventLog
    EventLog.log("DOCTOR_UPDATED", f"Doctor {doctor.get('name', '')} updated", role=identity.get('role'), clinic_id=identity.get('clinic_id'))
    
    return success_response(message="Doctor updated successfully")

@admin_bp.route('/doctor/<doctor_id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(doctor_id):
    if not (is_main_admin() or is_clinic_admin()):
        return error_response("Unauthorized", status=403)
        
    import json
    identity = json.loads(get_jwt_identity())
    
    query = {"_id": ObjectId(doctor_id)}
    if is_clinic_admin():
        query['clinic_id'] = identity.get('clinic_id')
        
    result = mongo.db.doctors.delete_one(query)
    
    if result.deleted_count == 0:
        return error_response("Doctor not found or unauthorized", status=404)
        
    from models.event import EventLog
    EventLog.log("DOCTOR_DELETED", f"Doctor deleted", role=identity.get('role'), clinic_id=identity.get('clinic_id'))
    
    return success_response(message="Doctor deleted successfully")

@admin_bp.route('/clinic/<clinic_id>', methods=['PATCH'])
@jwt_required()
def update_clinic(clinic_id):
    if not is_main_admin():
        return error_response("Only Main Admin can update clinics", status=403)
        
    data = request.get_json()
    
    update_fields = {}
    if 'name' in data: update_fields['name'] = data['name']
    if 'code' in data: update_fields['code'] = data['code']
    if 'contact_number' in data: update_fields['contact_number'] = data['contact_number']
    if 'address' in data: update_fields['address'] = data['address']
    if 'city' in data: update_fields['city'] = data['city']
    if 'state' in data: update_fields['state'] = data['state']
    if 'status' in data: update_fields['status'] = data['status']
    if 'booking_enabled' in data: update_fields['booking_enabled'] = data['booking_enabled']
    if 'queue_enabled' in data: update_fields['queue_enabled'] = data['queue_enabled']
    if 'emergency_support' in data: update_fields['emergency_support'] = data['emergency_support']
    
    if not update_fields:
        return error_response("No valid fields to update")
        
    mongo.db.clinics.update_one({"_id": ObjectId(clinic_id)}, {"$set": update_fields})
    
    from models.event import EventLog
    EventLog.log("CLINIC_UPDATED", f"Clinic {clinic_id} updated by main admin", role="main_admin")
    
    return success_response(message="Clinic updated successfully")

@admin_bp.route('/clinic/<clinic_id>', methods=['DELETE'])
@jwt_required()
def delete_clinic(clinic_id):
    if not is_main_admin():
        return error_response("Only Main Admin can delete clinics", status=403)
        
    result = mongo.db.clinics.delete_one({"_id": ObjectId(clinic_id)})
    
    if result.deleted_count == 0:
        return error_response("Clinic not found", status=404)
        
    # Also unset clinic_id for associated doctors
    mongo.db.doctors.update_many({"clinic_id": clinic_id}, {"$unset": {"clinic_id": ""}})
        
    from models.event import EventLog
    EventLog.log("CLINIC_DELETED", f"Clinic {clinic_id} deleted", role="main_admin")
    
    return success_response(message="Clinic deleted successfully")
