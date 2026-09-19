from database.db import mongo
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Clinic:
    @staticmethod
    def create(name, address, latitude, longitude, contact_number, **kwargs):
        clinic_data = {
            "name": name,
            "code": kwargs.get("code", ""),
            "email": kwargs.get("email", ""),
            "password": generate_password_hash(kwargs.get("password", "")) if kwargs.get("password") else "",
            "address": address,
            "city": kwargs.get("city", ""),
            "state": kwargs.get("state", ""),
            "pincode": kwargs.get("pincode", ""),
            "latitude": latitude,
            "longitude": longitude,
            "map_link": kwargs.get("map_link", ""),
            "contact_number": contact_number,
            "status": kwargs.get("status", "Active"),
            "booking_enabled": kwargs.get("booking_enabled", True),
            "queue_enabled": kwargs.get("queue_enabled", True),
            "emergency_support": kwargs.get("emergency_support", False),
            "max_doctors": kwargs.get("max_doctors", 50),
            "logo_url": kwargs.get("logo_url", ""),
            "theme_color": kwargs.get("theme_color", "#2563eb"),
            "created_at": datetime.utcnow()
        }
        return mongo.db.clinics.insert_one(clinic_data)

    @staticmethod
    def get_all():
        clinics = list(mongo.db.clinics.find())
        for c in clinics:
            c['_id'] = str(c['_id'])
        return clinics

    @staticmethod
    def verify_password(clinic, password):
        return check_password_hash(clinic.get('password', ''), password)
