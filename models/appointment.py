from database.db import mongo
from bson.objectid import ObjectId

class Appointment:
    @staticmethod
    def create(patient_id, doctor_id, date, slot, token_number, **kwargs):
        from datetime import datetime
        appointment_data = {
            "patient_id": ObjectId(patient_id) if isinstance(patient_id, str) and len(str(patient_id)) == 24 else patient_id,
            "doctor_id": ObjectId(doctor_id) if isinstance(doctor_id, str) and len(str(doctor_id)) == 24 else doctor_id,
            "date": date,
            "slot": slot,
            "token_number": token_number,
            "status": kwargs.get("status", "pending"), # pending, confirmed, completed, cancelled
            "facility_id": kwargs.get("facility_id", ""),
            "facility_name": kwargs.get("facility_name", kwargs.get("facility", "")),
            "department": kwargs.get("department", "General Medicine"),
            "medical_system": kwargs.get("medical_system", "Modern / Conventional Medicine"),
            "priority": kwargs.get("priority", "Routine"),
            "ai_case_id": kwargs.get("ai_case_id", ""),
            "purpose": kwargs.get("purpose", "Consultation"),
            "doctor_name": kwargs.get("doctor_name", ""),
            "indicator_color": kwargs.get("indicator_color", "#16A05D" if kwargs.get("priority") == "Routine" else ("#D97706" if kwargs.get("priority") == "Priority" else "#EA580C")),
            "created_at": kwargs.get("created_at", datetime.utcnow())
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
