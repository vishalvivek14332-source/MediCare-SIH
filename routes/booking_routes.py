from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.appointment import Appointment
from models.doctor import Doctor
from utils.helpers import success_response, error_response
from utils.token_generator import generate_token
from database.db import mongo
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/doctors', methods=['GET'])
def get_doctors():
    clinic_id = request.args.get('clinic_id')
    query = {"clinic_id": clinic_id} if clinic_id else {}
    doctors = list(mongo.db.doctors.find(query))
    for doc in doctors:
        doc['_id'] = str(doc['_id'])
    return success_response(data=doctors)

@booking_bp.route('/create', methods=['POST'])
@jwt_required()
def create_appointment():
    import json
    identity = json.loads(get_jwt_identity())
    
    # Removed the restriction so doctors/admins can also book appointments (e.g., for testing or walk-ins)
        
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    slot = data.get('slot')
    
    if not doctor_id or not date or not slot:
        return error_response("Missing required fields")
        
    doctor = mongo.db.doctors.find_one({"_id": Doctor.find_by_email(None) if False else None}) # need to find doctor to check dept
    from bson.objectid import ObjectId
    doctor = mongo.db.doctors.find_one({"_id": ObjectId(doctor_id)})
    if not doctor:
        return error_response("Doctor not found", status=404)
        
    department_code = doctor.get('department', 'GEN')[:3].upper()
    
    # Get last token for today
    today_str = datetime.now().strftime("%Y%m%d")
    last_appointment = mongo.db.appointments.find_one(
        {"token_number": {"$regex": f"{department_code}-{today_str}"}},
        sort=[("token_number", -1)]
    )
    
    last_token = last_appointment['token_number'] if last_appointment else None
    new_token = generate_token(last_token, department_code)
    
    result = Appointment.create(
        patient_id=identity['id'],
        doctor_id=doctor_id,
        date=date,
        slot=slot,
        token_number=new_token
    )
    
    from extensions import socketio
    socketio.emit('queue_update', {'doctor_id': doctor_id})
    
    return success_response(
        data={"appointment_id": str(result.inserted_id), "token_number": new_token}, 
        message="Appointment booked successfully",
        status=201
    )

@booking_bp.route('/my-appointments', methods=['GET'])
@jwt_required()
def my_appointments():
    import json
    identity = json.loads(get_jwt_identity())
    if identity['role'] != 'patient':
        return error_response("Unauthorized", status=403)
        
    appointments = Appointment.get_by_patient(identity['id'])
    for app in appointments:
        app['_id'] = str(app['_id'])
        app['doctor_id'] = str(app['doctor_id'])
        app['patient_id'] = str(app['patient_id'])
    return success_response(data=appointments)

@booking_bp.route('/queue-status', methods=['GET'])
def get_queue_status():
    pending = list(mongo.db.appointments.find({"status": "pending"}).sort("token_number", 1).limit(5))
    for p in pending: p['_id'] = str(p['_id'])
    
    completed = list(mongo.db.appointments.find({"status": "completed"}).sort("token_number", -1).limit(1))
    for c in completed: c['_id'] = str(c['_id'])
    
    return success_response(data={
        "current": completed[0]['token_number'] if completed else "N/A",
        "next": pending[0]['token_number'] if pending else "N/A",
        "waiting_count": mongo.db.appointments.count_documents({"status": "pending"})
    })

@booking_bp.route('/clinics/nearby', methods=['GET'])
def get_nearby_clinics():
    lat = float(request.args.get('lat', 0))
    lng = float(request.args.get('lng', 0))
    
    from models.clinic import Clinic
    from utils.helpers import calculate_distance
    
    clinics = Clinic.get_all()
    results = []
    
    for c in clinics:
        dist = calculate_distance(lat, lng, c.get('latitude', 0), c.get('longitude', 0))
        if dist <= 100:
            c['distance_km'] = dist
            c['distance_str'] = f"{dist:.1f} km"
            results.append(c)
            
    results.sort(key=lambda x: x['distance_km'])
    return success_response(data=results)

@booking_bp.route('/clinics/search', methods=['GET'])
def search_clinics():
    query = request.args.get('query', '').strip()
    if not query:
        return success_response(data=[])
        
    from models.clinic import Clinic
    import re
    regex = re.compile(f".*{query}.*", re.IGNORECASE)
    
    # Search in name, address, city, state
    search_query = {
        "$or": [
            {"name": regex},
            {"address": regex},
            {"city": regex},
            {"state": regex}
        ]
    }
    
    clinics = list(mongo.db.clinics.find(search_query))
    for c in clinics:
        c['_id'] = str(c['_id'])
        if 'password' in c: del c['password']
        
    return success_response(data=clinics)

@booking_bp.route('/availability', methods=['GET'])
def get_availability():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    
    if not doctor_id or not date:
        return error_response("doctor_id and date are required")
        
    from bson.objectid import ObjectId
    doctor = mongo.db.doctors.find_one({"_id": ObjectId(doctor_id)})
    if not doctor:
        return error_response("Doctor not found", status=404)
        
    total_tokens = doctor.get('total_tokens', 12)
    from utils.helpers import generate_time_slots
    standard_slots = generate_time_slots(total_tokens)
    
    # Find all appointments for this doctor on this date
    appointments = list(mongo.db.appointments.find({
        "doctor_id": ObjectId(doctor_id),
        "date": date
    }))
    
    booked_slots = {app['slot']: {"token": app['token_number'], "status": app['status']} for app in appointments if app['status'] != 'cancelled'}
    
    availability = []
    for i, slot in enumerate(standard_slots):
        slot_data = booked_slots.get(slot)
        if slot_data:
            availability.append({
                "ticket_id": i + 1,
                "slot": slot,
                "status": slot_data['status'], # 'pending' or 'completed'
                "token": slot_data['token']
            })
        else:
            availability.append({
                "ticket_id": i + 1,
                "slot": slot,
                "status": "available",
                "token": None
            })
        
    return success_response(data=availability)
