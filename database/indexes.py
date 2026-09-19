"""
MongoDB Atlas Index Initializer
Creates high-performance compound indexes for frequently queried fields.
Uses background=True so index builds do not lock or block database operations.
"""
from database.db import mongo

def init_indexes():
    try:
        # 1. Patients collection
        mongo.db.patients.create_index([("email", 1)], unique=False, background=True)
        mongo.db.patients.create_index([("health_id", 1)], background=True)
        mongo.db.patients.create_index([("abdm_id", 1)], background=True)

        # 2. Appointments collection
        mongo.db.appointments.create_index([("status", 1), ("token_number", 1)], background=True)
        mongo.db.appointments.create_index([("patient_id", 1), ("date", 1)], background=True)
        mongo.db.appointments.create_index([("doctor_id", 1), ("date", 1)], background=True)

        # 3. Health Documents collection
        mongo.db.health_documents.create_index([("patient_id", 1), ("category", 1), ("created_at", -1)], background=True)

        # 4. Linked Facilities collection
        mongo.db.linked_facilities.create_index([("patient_id", 1), ("type", 1), ("created_at", -1)], background=True)

        # 5. Shared Records collection
        mongo.db.shared_records.create_index([("patient_id", 1), ("status", 1)], background=True)

        # 6. Doctors collection
        mongo.db.doctors.create_index([("clinic_id", 1), ("department", 1)], background=True)
        mongo.db.doctors.create_index([("email", 1)], background=True)

        # 7. Clinics collection
        mongo.db.clinics.create_index([("name", 1), ("city", 1)], background=True)

        # 8. AI Case Sessions
        mongo.db.ai_case_sessions.create_index([("patient_id", 1), ("session_id", 1)], background=True)

        print("[PERF] MongoDB Atlas indexes initialized successfully.")
    except Exception as e:
        print(f"[PERF] Note on index creation: {e}")
