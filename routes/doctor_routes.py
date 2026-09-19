from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.appointment import Appointment
from utils.helpers import success_response, error_response

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    import json
    identity = json.loads(get_jwt_identity())
    if identity['role'] != 'doctor':
        return error_response("Unauthorized", status=403)
        
    date_filter = request.args.get('date')
    appointments = Appointment.get_by_doctor(identity['id'], date=date_filter)
    
    for app in appointments:
        app['_id'] = str(app['_id'])
        if 'doctor_id' in app:
            app['doctor_id'] = str(app['doctor_id'])
        if 'patient_id' in app:
            app['patient_id'] = str(app['patient_id'])
        
    return success_response(data=appointments)

@doctor_bp.route('/appointment/<appointment_id>/status', methods=['PATCH'])
@jwt_required()
def update_appointment_status(appointment_id):
    import json
    identity = json.loads(get_jwt_identity())
    if identity['role'] != 'doctor':
        return error_response("Unauthorized", status=403)
        
    data = request.get_json()
    status = data.get('status')
    if status not in ['completed', 'cancelled']:
        return error_response("Invalid status")
        
    Appointment.update_status(appointment_id, status)
    
    from extensions import socketio
    socketio.emit('queue_update', {'doctor_id': identity['id']})
    
    return success_response(message=f"Appointment marked as {status}")

@doctor_bp.route('/my-availability', methods=['GET'])
@jwt_required()
def get_my_availability():
    import json
    identity = json.loads(get_jwt_identity())
    if identity['role'] != 'doctor':
        return error_response("Unauthorized", status=403)
        
    date = request.args.get('date')
    if not date:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
        
    from database.db import mongo
    from bson.objectid import ObjectId
    
    doctor = mongo.db.doctors.find_one({"_id": ObjectId(identity['id'])})
    total_tokens = doctor.get('total_tokens', 12) if doctor else 12
    
    from utils.helpers import generate_time_slots
    standard_slots = generate_time_slots(total_tokens)
    
    appointments = list(mongo.db.appointments.find({
        "doctor_id": ObjectId(identity['id']),
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
