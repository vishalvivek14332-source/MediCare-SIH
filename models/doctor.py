from database.db import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class Doctor:
    @staticmethod
    def create(name, email, password, department, specialization, fees, availability=None, total_tokens=12, **kwargs):
        doctor_data = {
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "department": department,
            "specialization": specialization,
            "fees": fees,
            "total_tokens": total_tokens,
            "availability": availability or [],
            "total_consultations": kwargs.get("total_consultations", 0),
            "patient_ratings": kwargs.get("patient_ratings", 5.0),
            "avg_completion_time": kwargs.get("avg_completion_time", 15),
            "is_suspended": kwargs.get("is_suspended", False)
        }
        return mongo.db.doctors.insert_one(doctor_data)
        
    @staticmethod
    def find_by_email(email):
        return mongo.db.doctors.find_one({"email": email})
        
    @staticmethod
    def get_all():
        return list(mongo.db.doctors.find({}, {"password": 0}))
        
    @staticmethod
    def verify_password(doctor, password):
        return check_password_hash(doctor['password'], password)
