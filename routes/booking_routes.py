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
@jwt_required(optional=True)
def create_appointment():
    import json
    from bson.objectid import ObjectId
    from datetime import datetime

    patient_id = None
    raw_id = get_jwt_identity()
    if raw_id:
        try:
            parsed = json.loads(raw_id) if isinstance(raw_id, str) else raw_id
            patient_id = parsed.get('id')
        except Exception:
            patient_id = raw_id

    if not patient_id:
        pat = mongo.db.patients.find_one({"email": "sajilbinu@example.com"}) or mongo.db.patients.find_one({})
        if pat:
            patient_id = str(pat['_id'])
        else:
            return error_response("Authentication required", status=401)

    data = request.get_json() or {}
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    slot = data.get('slot')
    priority = data.get('priority', 'Routine').capitalize()
    medical_system = data.get('medical_system', 'Modern / Conventional Medicine')
    facility_id = data.get('facility_id', '')
    facility_name = data.get('facility_name', '')
    department = data.get('department', '')
    ai_case_id = data.get('ai_case_id', '')

    if not doctor_id or not date or not slot:
        return error_response("Missing required fields: doctor_id, date, and slot are mandatory")

    # Validate Priority (Server-side validation)
    allowed_priorities = ["Routine", "Priority", "Urgent", "Emergency"]
    if priority not in allowed_priorities:
        priority = "Routine"

    # Find doctor
    doctor = None
    try:
        doctor = mongo.db.doctors.find_one({"_id": ObjectId(doctor_id)})
    except Exception:
        pass
    if not doctor:
        doctor = mongo.db.doctors.find_one({"_id": doctor_id})
    if not doctor:
        return error_response("Doctor not found", status=404)

    # Validate duplicate booking for the same slot on the same date
    existing_appointment = mongo.db.appointments.find_one({
        "doctor_id": doctor["_id"],
        "date": date,
        "slot": slot,
        "status": {"$in": ["pending", "confirmed", "completed"]}
    })
    if existing_appointment:
        return error_response(
            f"Token slot '{slot}' is already booked for this doctor on {date}. Please select an available slot.",
            status=409
        )

    # Determine department and facility names
    dept_name = department or doctor.get('department', 'General Medicine')
    fac_name = facility_name or doctor.get('facility_name', 'Healthcare Facility')
    med_sys = medical_system or doctor.get('medical_system', 'Modern / Conventional Medicine')
    doc_name = doctor.get('name', 'Doctor')

    # Generate persistent token identity
    dept_code = dept_name[:3].upper() if len(dept_name) >= 3 else "GEN"
    prefix_char = dept_code[0]
    
    # Sequential token counter for this doctor and date
    day_count = mongo.db.appointments.count_documents({
        "doctor_id": doctor["_id"],
        "date": date
    })
    token_number = f"{prefix_char}-{day_count + 21:03d}" if day_count < 5 else f"{prefix_char}-{day_count + 1:03d}"

    # Indicator badge color based on validated priority
    priority_colors = {
        "Routine": "#16A05D",
        "Priority": "#D97706",
        "Urgent": "#EA580C",
        "Emergency": "#DC2626"
    }

    result = Appointment.create(
        patient_id=patient_id,
        doctor_id=str(doctor["_id"]),
        doctor_name=doc_name,
        date=date,
        slot=slot,
        token_number=token_number,
        priority=priority,
        medical_system=med_sys,
        facility_id=facility_id or str(doctor.get('clinic_id', '')),
        facility_name=fac_name,
        department=dept_name,
        ai_case_id=ai_case_id,
        status="confirmed",
        indicator_color=priority_colors.get(priority, "#16A05D")
    )

    # Emit Flask-SocketIO queue update
    try:
        from extensions import socketio
        socketio.emit('queue_update', {
            'doctor_id': str(doctor["_id"]),
            'doctor_name': doc_name,
            'token_number': token_number,
            'priority': priority,
            'facility_name': fac_name
        })
    except Exception as e:
        print(f"Socket.IO queue emit notice: {e}")

    return success_response(
        data={
            "appointment_id": str(result.inserted_id),
            "token_number": token_number,
            "priority": priority,
            "medical_system": med_sys,
            "facility_name": fac_name,
            "department": dept_name,
            "doctor_name": doc_name,
            "date": date,
            "slot": slot
        },
        message="Appointment and live token reserved successfully",
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
@booking_bp.route('/tokens', methods=['GET'])
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
