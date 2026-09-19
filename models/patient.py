from database.db import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class Patient:
    @staticmethod
    def create(name, email, phone, password, age, gender):
        patient_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": generate_password_hash(password),
            "age": age,
            "gender": gender
        }
        return mongo.db.patients.insert_one(patient_data)

    @staticmethod
    def find_by_email(email):
        return mongo.db.patients.find_one({"email": email})
        
    @staticmethod
    def find_by_id(patient_id):
        from bson.objectid import ObjectId
        return mongo.db.patients.find_one({"_id": ObjectId(patient_id)})

    @staticmethod
    def verify_password(patient, password):
        return check_password_hash(patient['password'], password)
