from database.db import mongo
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime

class Patient:
    @staticmethod
    def generate_health_id():
        """Generates a unique MediCare Health ID e.g. CB-2026-001245"""
        for _ in range(50):
            num = random.randint(100000, 999999)
            hid = f"CB-2026-{num}"
            if not mongo.db.patients.find_one({"health_id": hid}):
                return hid
        return f"CB-2026-{random.randint(100000, 999999)}"

    @staticmethod
    def create(name, email, phone, password, age=28, gender='Male', **kwargs):
        health_id = kwargs.get('health_id') or Patient.generate_health_id()
        patient_data = {
            "name": name.strip(),
            "email": email.strip().lower() if email else f"patient_{phone}@medicare.local",
            "phone": phone.strip() if phone else "",
            "mobile": phone.strip() if phone else "",
            "mobile_verified": kwargs.get('mobile_verified', True),
            "password": generate_password_hash(password) if password else generate_password_hash("password123"),
            "age": int(age) if age else 28,
            "gender": gender,
            "health_id": health_id,
            "date_of_birth": kwargs.get('date_of_birth', ''),
            "state": kwargs.get('state', 'Kerala'),
            "district": kwargs.get('district', 'Kannur'),
            "preferred_language": kwargs.get('preferred_language', 'en'),
            "address": kwargs.get('address', ''),
            "emergency_contact": kwargs.get('emergency_contact', ''),
            "communication_preferences": kwargs.get('communication_preferences', {
                "email": True,
                "sms": True,
                "appointment_reminders": True,
                "health_updates": False
            }),
            "consent": kwargs.get('consent', {
                "terms": True,
                "privacy": True,
                "health_data_processing": True
            }),
            "role": "patient",
            "created_at": datetime.utcnow()
        }
        res = mongo.db.patients.insert_one(patient_data)
        patient_data['_id'] = res.inserted_id
        return patient_data

    @staticmethod
    def find_by_email(email):
        if not email:
            return None
        return mongo.db.patients.find_one({"email": email.strip().lower()})

    @staticmethod
    def find_by_mobile(phone):
        if not phone:
            return None
        clean_phone = phone.strip().replace(" ", "").replace("-", "")
        if clean_phone.startswith("+91"):
            clean_phone = clean_phone[3:]
        return mongo.db.patients.find_one({
            "$or": [
                {"phone": phone},
                {"mobile": phone},
                {"phone": clean_phone},
                {"mobile": clean_phone},
                {"phone": f"+91{clean_phone}"},
                {"mobile": f"+91{clean_phone}"}
            ]
        })

    @staticmethod
    def find_by_health_id(health_id):
        if not health_id:
            return None
        return mongo.db.patients.find_one({"health_id": health_id.strip()})
        
    @staticmethod
    def find_by_id(patient_id):
        from bson.objectid import ObjectId
        try:
            return mongo.db.patients.find_one({"_id": ObjectId(patient_id)})
        except Exception:
            return None

    @staticmethod
    def verify_password(patient, password):
        if not patient or 'password' not in patient:
            return False
        return check_password_hash(patient['password'], password)
