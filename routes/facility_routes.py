from flask import Blueprint, request
from utils.helpers import success_response, error_response
from utils.india_locations import get_all_states, get_districts_by_state, get_cities_by_district
from utils.medical_systems import get_medical_systems_list, get_system_by_code_or_name
from database.db import mongo
from bson.objectid import ObjectId
import re

facility_bp = Blueprint('facility', __name__)

@facility_bp.route('/medical-systems', methods=['GET'])
def get_medical_systems():
    """Returns all 8 recognized Indian medical systems with live facility counts."""
    systems = get_medical_systems_list(mongo.db)
    return success_response(data=systems)

@facility_bp.route('/states', methods=['GET'])
def get_states():
    """Returns all 28 states and 8 Union Territories in India."""
    states = get_all_states()
    return success_response(data=states)

@facility_bp.route('/districts', methods=['GET'])
def get_districts():
    """Returns districts for the given state query parameter."""
    state = request.args.get('state', '').strip()
    if not state:
        return error_response("State parameter is required", status=400)
    districts = get_districts_by_state(state)
    return success_response(data=districts)

@facility_bp.route('/cities', methods=['GET'])
def get_cities():
    """Returns cities/towns for the given state and district."""
    state = request.args.get('state', '').strip()
    district = request.args.get('district', '').strip()
    if not state or not district:
        return error_response("State and district parameters are required", status=400)
    cities = get_cities_by_district(state, district)
    return success_response(data=cities)

@facility_bp.route('/facilities', methods=['GET'])
def get_facilities():
    """
    Fetch facilities matching filters:
    medical_system, state, district, city, facility_type, search, sort.
    Server-side filtering with debounced search query support.
    """
    medical_system = request.args.get('medical_system', '').strip()
    state = request.args.get('state', '').strip()
    district = request.args.get('district', '').strip()
    city = request.args.get('city', '').strip()
    facility_type = request.args.get('facility_type', '').strip()
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'name').strip()

    query = {}

    if medical_system and medical_system.lower() != 'all':
        # Match either exact name or code
        sys_info = get_system_by_code_or_name(medical_system)
        if sys_info:
            query["$or"] = [
                {"medical_system": sys_info["name"]},
                {"medical_system": sys_info["code"]},
                {"medical_system": {"$regex": f"^{re.escape(sys_info['name'])}$", "$options": "i"}}
            ]
        else:
            query["medical_system"] = {"$regex": f"^{re.escape(medical_system)}$", "$options": "i"}

    if state and state.lower() != 'all':
        query["state"] = {"$regex": f"^{re.escape(state)}$", "$options": "i"}

    if district and district.lower() != 'all':
        query["district"] = {"$regex": f"^{re.escape(district)}$", "$options": "i"}

    if city and city.lower() != 'all':
        query["city"] = {"$regex": f"^{re.escape(city)}$", "$options": "i"}

    if facility_type and facility_type.lower() != 'all':
        query["facility_type"] = {"$regex": f".*{re.escape(facility_type)}.*", "$options": "i"}

    if search_query:
        reg = re.compile(f".*{re.escape(search_query)}.*", re.IGNORECASE)
        search_filter = {
            "$or": [
                {"name": reg},
                {"address": reg},
                {"city": reg},
                {"district": reg},
                {"departments": reg}
            ]
        }
        if "$or" in query:
            query = {"$and": [query, search_filter]}
        else:
            query.update(search_filter)

    # Sort order
    sort_field = [("name", 1)]
    if sort_by == 'availability':
        sort_field = [("availability", 1), ("name", 1)]

    facilities = list(mongo.db.clinics.find(query).sort(sort_field).limit(50))
    for fac in facilities:
        fac['_id'] = str(fac['_id'])
        if 'password' in fac:
            del fac['password']
        if 'departments' not in fac or not fac['departments']:
            fac['departments'] = ["General Medicine"]
        if 'verification_status' not in fac:
            fac['verification_status'] = "Demo Facility"

    return success_response(data=facilities)

@facility_bp.route('/facilities/<facility_id>', methods=['GET'])
def get_facility_by_id(facility_id):
    """Retrieve details for a single healthcare facility."""
    try:
        obj_id = ObjectId(facility_id)
        fac = mongo.db.clinics.find_one({"_id": obj_id})
    except Exception:
        fac = mongo.db.clinics.find_one({"_id": facility_id})

    if not fac:
        return error_response("Facility not found", status=404)

    fac['_id'] = str(fac['_id'])
    if 'password' in fac:
        del fac['password']
    return success_response(data=fac)

@facility_bp.route('/facilities/<facility_id>/departments', methods=['GET'])
def get_facility_departments(facility_id):
    """
    Return ONLY the departments configured for this healthcare facility.
    Does NOT return departments from other facilities.
    """
    try:
        obj_id = ObjectId(facility_id)
        fac = mongo.db.clinics.find_one({"_id": obj_id})
    except Exception:
        fac = mongo.db.clinics.find_one({"_id": facility_id})

    if not fac:
        return error_response("Facility not found", status=404)

    departments = fac.get('departments', [])
    if not departments:
        # Fallback to doctor departments linked to this facility
        doctor_depts = mongo.db.doctors.distinct("department", {"clinic_id": str(fac['_id'])})
        departments = doctor_depts or ["General Medicine"]

    return success_response(data={
        "facility_id": str(fac['_id']),
        "facility_name": fac.get('name', ''),
        "medical_system": fac.get('medical_system', 'Modern / Conventional Medicine'),
        "departments": departments
    })

@facility_bp.route('/facilities/<facility_id>/departments/<path:dept_name>/doctors', methods=['GET'])
def get_facility_department_doctors(facility_id, dept_name):
    """
    Return ONLY doctors associated with the selected facility and department.
    """
    try:
        obj_id = ObjectId(facility_id)
        fac = mongo.db.clinics.find_one({"_id": obj_id})
    except Exception:
        fac = mongo.db.clinics.find_one({"_id": facility_id})

    if not fac:
        return error_response("Facility not found", status=404)

    # Search doctors matching clinic_id (either ObjectId or string) or facility_name
    fac_id_str = str(fac['_id'])
    fac_name = fac.get('name', '')

    dept_regex = re.compile(f"^{re.escape(dept_name.strip())}$", re.IGNORECASE)

    query = {
        "$and": [
            {
                "$or": [
                    {"clinic_id": fac_id_str},
                    {"facility_name": fac_name},
                    {"facility_name": {"$regex": f".*{re.escape(fac_name)}.*", "$options": "i"}}
                ]
            },
            {"department": dept_regex}
        ]
    }

    doctors = list(mongo.db.doctors.find(query, {"password": 0}))
    for doc in doctors:
        doc['_id'] = str(doc['_id'])
        if 'clinic_id' in doc and isinstance(doc['clinic_id'], ObjectId):
            doc['clinic_id'] = str(doc['clinic_id'])
        doc['facility_name'] = fac_name
        doc['facility_id'] = fac_id_str
        if 'qualification' not in doc:
            doc['qualification'] = "MBBS" if "Modern" in fac.get('medical_system', '') else "Certified Practitioner"
        if 'experience' not in doc:
            doc['experience'] = "8 years"
        if 'verification_status' not in doc:
            doc['verification_status'] = "Demo Facility Doctor"
        if 'available_today' not in doc:
            doc['available_today'] = True
        if 'next_token' not in doc:
            doc['next_token'] = "A-024"

    return success_response(data=doctors)

@facility_bp.route('/doctors/<doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    """Retrieve detailed doctor profile."""
    try:
        obj_id = ObjectId(doctor_id)
        doc = mongo.db.doctors.find_one({"_id": obj_id}, {"password": 0})
    except Exception:
        doc = mongo.db.doctors.find_one({"_id": doctor_id}, {"password": 0})

    if not doc:
        return error_response("Doctor not found", status=404)

    doc['_id'] = str(doc['_id'])
    return success_response(data=doc)
