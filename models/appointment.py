from database.db import mongo
from bson.objectid import ObjectId

class Appointment:
    @staticmethod
    def create(patient_id, doctor_id, date, slot, token_number):
        appointment_data = {
            "patient_id": ObjectId(patient_id) if isinstance(patient_id, str) else patient_id,
            "doctor_id": ObjectId(doctor_id) if isinstance(doctor_id, str) else doctor_id,
            "date": date,
            "slot": slot,
            "token_number": token_number,
            "status": "pending" # pending, completed, cancelled
        }
        return mongo.db.appointments.insert_one(appointment_data)
        
    @staticmethod
    def get_by_patient(patient_id):
        return list(mongo.db.appointments.find({"patient_id": ObjectId(patient_id) if isinstance(patient_id, str) else patient_id}))

    @staticmethod
    def get_by_doctor(doctor_id, date=None):
        query = {"doctor_id": ObjectId(doctor_id) if isinstance(doctor_id, str) else doctor_id}
        if date:
            query["date"] = date
        return list(mongo.db.appointments.find(query))

    @staticmethod
    def update_status(appointment_id, status):
        return mongo.db.appointments.update_one(
            {"_id": ObjectId(appointment_id) if isinstance(appointment_id, str) else appointment_id},
            {"$set": {"status": status}}
        )
