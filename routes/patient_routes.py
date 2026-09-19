import os
from flask import Blueprint, request, jsonify, current_app, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from database.db import mongo
from models.health_record import HealthDocument, LinkedFacility, SharedRecord
from models.patient import Patient
from utils.helpers import success_response, error_response
from utils.qr_generator import get_patient_qr_payload, generate_qr_svg, generate_qr_png_bytes, generate_qr_data_url
from datetime import datetime
from bson.objectid import ObjectId
import json

patient_bp = Blueprint('patient', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@patient_bp.route('/profile', methods=['GET'])
@jwt_required(optional=True)
def get_profile():
    patient = None
    identity_raw = get_jwt_identity()
    if identity_raw:
        try:
            identity = json.loads(identity_raw) if isinstance(identity_raw, str) else identity_raw
            if isinstance(identity, dict) and identity.get('role') == 'patient' and identity.get('id'):
                patient = mongo.db.patients.find_one({"_id": ObjectId(identity['id'])})
        except Exception:
            patient = None

    if not patient:
        patient = mongo.db.patients.find_one({"email": "sajilbinu@example.com"}) or mongo.db.patients.find_one({})
    if not patient:
        return error_response("Patient not found", status=404)
    
    patient['_id'] = str(patient['_id'])
    if 'password' in patient: del patient['password']
    return success_response(data=patient)

@patient_bp.route('/profile', methods=['PUT'])
@jwt_required(optional=True)
def update_profile():
    data = request.get_json() or {}
    identity_raw = get_jwt_identity()
    patient = None
    if identity_raw:
        try:
            identity = json.loads(identity_raw) if isinstance(identity_raw, str) else identity_raw
            if isinstance(identity, dict) and identity.get('role') == 'patient' and identity.get('id'):
                patient = mongo.db.patients.find_one({"_id": ObjectId(identity['id'])})
        except Exception:
            pass

    email = data.get('email') or (patient.get('email') if patient else 'sajilbinu@example.com')
    
    update_fields = {}
    for key in ['name', 'phone', 'address', 'language_preference', 'emergency_contact', 'occupation']:
        if key in data and data[key] is not None:
            update_fields[key] = data[key]
            
    if update_fields:
        mongo.db.patients.update_one({"email": email}, {"$set": update_fields})
    
    updated = mongo.db.patients.find_one({"email": email}) or {}
    if '_id' in updated: updated['_id'] = str(updated['_id'])
    if 'password' in updated: del updated['password']
    return success_response(data=updated, message="Profile updated successfully")

@patient_bp.route('/health-records', methods=['GET'])
def get_health_records():
    category = request.args.get('category')
    search = request.args.get('search')
    records = HealthDocument.get_by_patient(None, category=category, search=search)
    counts = HealthDocument.count_by_category()
    return success_response(data={"records": records, "counts": counts})

@patient_bp.route('/upload-document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        # Fallback for JSON demo upload if triggered via modal
        data = request.form or request.get_json() or {}
        filename = data.get('filename', 'Medical Document.pdf')
        category = data.get('category', 'Lab Reports')
        hospital = data.get('hospital', 'Govt. District Hospital, Kannur')
        file_type = filename.split('.')[-1] if '.' in filename else 'pdf'
        
        result = HealthDocument.create(
            patient_id="sajil_binu",
            name=filename,
            category=category,
            hospital=hospital,
            file_type=file_type,
            status="Uploaded"
        )
        return success_response(data={"id": str(result.inserted_id), "name": filename}, message="Document uploaded successfully", status=201)

    file = request.files['file']
    category = request.form.get('category', 'Lab Reports')
    hospital = request.form.get('hospital', 'Govt. District Hospital, Kannur')

    if file.filename == '':
        return error_response("No file selected")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        file_type = filename.rsplit('.', 1)[1].lower()
        result = HealthDocument.create(
            patient_id="sajil_binu",
            name=filename,
            category=category,
            hospital=hospital,
            file_type=file_type,
            file_url=f"/static/uploads/{filename}",
            status="Uploaded"
        )
        return success_response(data={"id": str(result.inserted_id), "name": filename}, message="File uploaded successfully", status=201)
    
    return error_response("File format not supported. Only PDF, JPG, PNG allowed.")

@patient_bp.route('/facilities', methods=['GET'])
def get_facilities():
    state = request.args.get('state')
    facility_type = request.args.get('type')
    search = request.args.get('search')
    facilities = LinkedFacility.get_by_patient(None, state=state, facility_type=facility_type, search=search)
    return success_response(data=facilities)

@patient_bp.route('/facilities/link', methods=['POST'])
def link_facility():
    data = request.get_json() or {}
    name = data.get('name')
    abdm_id = data.get('abdm_id', 'HOSP' + str(int(datetime.utcnow().timestamp()))[-6:])
    facility_type = data.get('type', 'Government Hospital')
    location = data.get('location', 'Kerala')
    
    if not name:
        return error_response("Facility name is required")
        
    result = LinkedFacility.create(
        patient_id="sajil_binu",
        name=name,
        abdm_id=abdm_id,
        facility_type=facility_type,
        location=location,
        status="Active"
    )
    return success_response(data={"id": str(result.inserted_id)}, message="Facility linked successfully", status=201)

@patient_bp.route('/facilities/unlink/<facility_id>', methods=['DELETE', 'POST'])
def unlink_facility(facility_id):
    LinkedFacility.remove(facility_id)
    return success_response(message="Facility unlinked successfully")

@patient_bp.route('/shared-records', methods=['GET'])
def get_shared_records():
    records = SharedRecord.get_by_patient(None)
    return success_response(data=records)

@patient_bp.route('/shared-records/share', methods=['POST'])
def share_record():
    data = request.get_json() or {}
    name = data.get('name')
    entity_type = data.get('type', 'Doctor')
    records = data.get('records', 'All Records')
    validity = data.get('validity', '6 months')
    
    if not name:
        return error_response("Recipient name or organisation is required")
        
    result = SharedRecord.create(
        patient_id="sajil_binu",
        entity_name=name,
        entity_type=entity_type,
        shared_records=records,
        access_validity=validity,
        status="Active"
    )
    return success_response(data={"id": str(result.inserted_id)}, message="Records shared successfully", status=201)

@patient_bp.route('/shared-records/revoke', methods=['POST'])
def revoke_shared_record():
    data = request.get_json() or {}
    record_id = data.get('id')
    if not record_id:
        return error_response("Record ID required")
    SharedRecord.revoke(record_id)
    return success_response(message="Record sharing access revoked")

@patient_bp.route('/appointments/list', methods=['GET'])
def list_appointments():
    tab = request.args.get('tab', 'upcoming')
    query = {}
    if tab == 'cancelled':
        query["status"] = "cancelled"
    elif tab == 'past':
        query["status"] = "completed"
    else:
        query["status"] = {"$in": ["confirmed", "scheduled", "pending"]}
        
    appointments = list(mongo.db.appointments.find(query).sort("date", 1))
    for a in appointments:
        a['_id'] = str(a['_id'])
        if 'patient_id' in a: a['patient_id'] = str(a['patient_id'])
        if 'doctor_id' in a: a['doctor_id'] = str(a['doctor_id'])
    return success_response(data=appointments)

@patient_bp.route('/timeline', methods=['GET'])
def get_timeline():
    events = [
        {"date": "19 Sep 2026", "title": "Current Case Taking & Triage", "category": "Consultation", "facility": "CareBridge AI Triage", "summary": "Persistent dry cough, mild fever (100.2°F). Triaged as Routine Priority."},
        {"date": "12 Sep 2026", "title": "Comprehensive Blood Test", "category": "Lab Report", "facility": "Govt. District Hospital, Kannur", "summary": "CBC, ESR, Fasting Blood Sugar. Hemoglobin 14.2 g/dL, normal platelet count."},
        {"date": "05 Sep 2026", "title": "General Consultation & Prescription", "category": "Prescription", "facility": "KPHC Thalassery", "doctor": "Dr. Meera Nair", "summary": "Amoxicillin 500mg, Paracetamol 650mg prescribed for upper respiratory tract symptoms."},
        {"date": "21 Aug 2026", "title": "Chest X-Ray PA View", "category": "Imaging", "facility": "Govt. Medical College, Kannur", "summary": "Clear lung fields, normal cardiothoracic ratio, no infiltrates."},
        {"date": "15 Jul 2026", "title": "Inpatient Discharge", "category": "Discharge", "facility": "Govt. District Hospital, Kannur", "summary": "Admitted for acute gastroenteritis, discharged fully recovered after 48h observation."},
        {"date": "10 Jan 2022", "title": "COVID-19 Vaccination (Precaution Dose)", "category": "Vaccination", "facility": "CoWIN / Community Health Centre", "summary": "Covishield Dose 3 batch #44091 verified."}
    ]
    return success_response(data=events)

@patient_bp.route('/qr', methods=['GET'])
@jwt_required(optional=True)
def get_qr_code():
    """
    Generates authentic ABDM scannable QR Code for the patient.
    Supports ?format=svg, ?format=png, ?format=json, and ?download=1
    """
    patient = None
    identity_raw = get_jwt_identity()
    if identity_raw:
        try:
            identity = json.loads(identity_raw) if isinstance(identity_raw, str) else identity_raw
            if isinstance(identity, dict) and identity.get('role') == 'patient' and identity.get('id'):
                patient = mongo.db.patients.find_one({"_id": ObjectId(identity['id'])})
        except Exception:
            patient = None

    if not patient:
        email = request.args.get('email', 'sajilbinu@example.com')
        patient = mongo.db.patients.find_one({"email": email})
    if not patient:
        patient = mongo.db.patients.find_one({}) or {}
    
    fmt = request.args.get('format', 'svg').lower()
    download = request.args.get('download', '0') == '1'
    payload = get_patient_qr_payload(patient)

    if fmt == 'png':
        png_bytes = generate_qr_png_bytes(payload)
        response = Response(png_bytes, mimetype='image/png')
        if download:
            response.headers['Content-Disposition'] = f'attachment; filename="ABHA_QR_{payload.get("hidn", "card")}.png"'
        return response
    elif fmt == 'json':
        data_url = generate_qr_data_url(payload)
        svg_content = generate_qr_svg(payload)
        return success_response(data={
            "qr_data_url": data_url,
            "svg": svg_content,
            "payload": payload
        })
    else:
        # Default SVG format
        svg_content = generate_qr_svg(payload)
        response = Response(svg_content, mimetype='image/svg+xml')
        if download:
            response.headers['Content-Disposition'] = f'attachment; filename="ABHA_QR_{payload.get("hidn", "card")}.svg"'
        return response

