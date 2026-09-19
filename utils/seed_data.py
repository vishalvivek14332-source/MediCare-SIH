"""
Seed realistic demo data into MongoDB Atlas so that the UI is completely populated
matching the reference screenshots in image_sih immediately.
"""
from database.db import mongo
from werkzeug.security import generate_password_hash
from datetime import datetime

_SEEDED = False

def seed_database():
    global _SEEDED
    if _SEEDED:
        return
    try:
        # Check if already seeded in DB
        if mongo.db.settings.find_one({"key": "seed_completed"}):
            _SEEDED = True
            return

        # 1. Seed or update Demo Patient
        patient = mongo.db.patients.find_one({"email": "sajilbinu@example.com"})
        if not patient:
            patient = {
                "name": "Sajil Binu",
                "email": "sajilbinu@example.com",
                "phone": "+91 98765 43210",
                "password": generate_password_hash("password123"),
                "age": 24,
                "gender": "Male",
                "dob": "12 Mar 2002",
                "blood_group": "O+",
                "address": "Panoor, Kannur, Kerala, 670692",
                "language_preference": "English",
                "emergency_contact": "Biju Mathew (Father) +91 98987 65432",
                "occupation": "Student",
                "state": "Kerala",
                "district": "Kannur",
                "pincode": "670692",
                "health_id": "91-XXXX-XXXX-1234",
                "abdm_id": "CB-2026-001245",
                "is_verified": True
            }
            patient_id = mongo.db.patients.insert_one(patient).inserted_id
        else:
            patient_id = patient['_id']
            # update profile fields if missing
            mongo.db.patients.update_one(
                {"_id": patient_id},
                {"$set": {
                    "health_id": "91-XXXX-XXXX-1234",
                    "abdm_id": "CB-2026-001245",
                    "dob": "12 Mar 2002",
                    "blood_group": "O+",
                    "address": "Panoor, Kannur, Kerala, 670692",
                    "language_preference": "English",
                    "emergency_contact": "Biju Mathew (Father) +91 98987 65432",
                    "occupation": "Student",
                    "state": "Kerala",
                    "district": "Kannur",
                    "pincode": "670692",
                    "is_verified": True
                }}
            )

        # 2. Seed Reference Doctors from screenshots
        doctors_data = [
            {
                "name": "Dr. Meera Nair",
                "email": "meera.nair@example.com",
                "password": generate_password_hash("doctor123"),
                "department": "General Medicine",
                "specialization": "Consultant Physician",
                "facility_name": "KPHC Thalassery",
                "fees": 200,
                "total_tokens": 16,
                "patient_ratings": 4.9,
                "is_suspended": False
            },
            {
                "name": "Dr. Arjun Kumar",
                "email": "arjun.kumar@example.com",
                "password": generate_password_hash("doctor123"),
                "department": "Orthopedics",
                "specialization": "Orthopedic Surgeon",
                "facility_name": "Govt. District Hospital Kannur",
                "fees": 250,
                "total_tokens": 14,
                "patient_ratings": 4.8,
                "is_suspended": False
            },
            {
                "name": "Dr. Sreelakshmi Nair",
                "email": "sreelakshmi.nair@example.com",
                "password": generate_password_hash("doctor123"),
                "department": "Dermatology",
                "specialization": "Dermatologist & Cosmetologist",
                "facility_name": "Govt. Medical College Kannur",
                "fees": 300,
                "total_tokens": 12,
                "patient_ratings": 4.9,
                "is_suspended": False
            },
            {
                "name": "Dr. Faisal Rahman",
                "email": "faisal.rahman@example.com",
                "password": generate_password_hash("doctor123"),
                "department": "Radiology",
                "specialization": "Senior Radiologist",
                "facility_name": "Sun Diagnostics Thalassery",
                "fees": 250,
                "total_tokens": 12,
                "patient_ratings": 4.7,
                "is_suspended": False
            }
        ]

        for doc in doctors_data:
            if not mongo.db.doctors.find_one({"email": doc["email"]}):
                mongo.db.doctors.insert_one(doc)

        # 3. Seed Reference Clinics & Linked Facilities
        facilities_data = [
            {
                "name": "Govt. District Hospital Kannur",
                "code": "GDHK01",
                "abdm_id": "HOSP001234",
                "type": "Government Hospital",
                "location": "Kannur, Kerala",
                "city": "Kannur",
                "state": "Kerala",
                "latitude": "11.8745",
                "longitude": "75.3704",
                "contact_number": "+91 497 273 1234",
                "status": "Active",
                "linked_on": "12 Aug 2025"
            },
            {
                "name": "KPHC Thalassery",
                "code": "KPHC02",
                "abdm_id": "HOSP005678",
                "type": "Primary Health Centre",
                "location": "Thalassery, Kerala",
                "city": "Thalassery",
                "state": "Kerala",
                "latitude": "11.7480",
                "longitude": "75.4894",
                "contact_number": "+91 490 232 5678",
                "status": "Active",
                "linked_on": "05 Sep 2025"
            },
            {
                "name": "Govt. Medical College Kannur",
                "code": "GMCK03",
                "abdm_id": "HOSP009876",
                "type": "Medical College",
                "location": "Kannur, Kerala",
                "city": "Kannur",
                "state": "Kerala",
                "latitude": "12.0024",
                "longitude": "75.3182",
                "contact_number": "+91 497 283 9876",
                "status": "Active",
                "linked_on": "21 Jul 2025"
            },
            {
                "name": "Sun Diagnostics",
                "code": "SUND04",
                "abdm_id": "DIAG003214",
                "type": "Diagnostic Centre",
                "location": "Thalassery, Kerala",
                "city": "Thalassery",
                "state": "Kerala",
                "latitude": "11.7510",
                "longitude": "75.4920",
                "contact_number": "+91 490 234 3214",
                "status": "Active",
                "linked_on": "10 Jun 2025"
            },
            {
                "name": "Apollo Hospitals Kochi",
                "code": "APOL05",
                "abdm_id": "HOSP007654",
                "type": "Private Hospital",
                "location": "Kochi, Kerala",
                "city": "Kochi",
                "state": "Kerala",
                "latitude": "9.9312",
                "longitude": "76.2673",
                "contact_number": "+91 484 290 7654",
                "status": "Pending",
                "linked_on": "15 Jun 2025"
            }
        ]

        for fac in facilities_data:
            if not mongo.db.clinics.find_one({"name": fac["name"]}):
                mongo.db.clinics.insert_one(fac)
            if not mongo.db.linked_facilities.find_one({"abdm_id": fac["abdm_id"]}):
                mongo.db.linked_facilities.insert_one({
                    "patient_id": str(patient_id),
                    "name": fac["name"],
                    "abdm_id": fac["abdm_id"],
                    "type": fac["type"],
                    "location": fac["location"],
                    "status": fac["status"],
                    "linked_on": fac["linked_on"],
                    "created_at": datetime.utcnow()
                })

        # 4. Seed Reference Documents matching MyHealthRecords.png & UploadDocuments.png
        documents_data = [
            {
                "name": "Blood Test Report.pdf",
                "category": "Lab Reports",
                "date": "12 Sep 2025",
                "time_uploaded": "10:24 AM",
                "hospital": "Govt. District Hospital, Kannur",
                "file_type": "pdf",
                "status": "Uploaded"
            },
            {
                "name": "Prescription - Dr. Meera.pdf",
                "category": "Prescriptions",
                "date": "05 Sep 2025",
                "time_uploaded": "11:30 AM",
                "hospital": "KPHC Thalassery",
                "file_type": "pdf",
                "status": "Uploaded"
            },
            {
                "name": "X-Ray Chest.jpg",
                "category": "Imaging Reports",
                "date": "21 Aug 2025",
                "time_uploaded": "02:15 PM",
                "hospital": "Govt. Medical College, Kannur",
                "file_type": "jpg",
                "status": "Uploaded"
            },
            {
                "name": "Discharge Summary.pdf",
                "category": "Discharge Summaries",
                "date": "15 Jul 2025",
                "time_uploaded": "04:20 PM",
                "hospital": "Govt. District Hospital, Kannur",
                "file_type": "pdf",
                "status": "Uploaded"
            },
            {
                "name": "COVID-19 Vaccination Certificate.pdf",
                "category": "Vaccination Records",
                "date": "10 Jan 2022",
                "time_uploaded": "09:45 AM",
                "hospital": "CoWIN / Government of India",
                "file_type": "pdf",
                "status": "Uploaded"
            }
        ]

        if mongo.db.health_documents.count_documents({}) < 5:
            for doc in documents_data:
                mongo.db.health_documents.insert_one({
                    "patient_id": str(patient_id),
                    "name": doc["name"],
                    "category": doc["category"],
                    "date": doc["date"],
                    "time_uploaded": doc.get("time_uploaded", "10:00 AM"),
                    "hospital": doc["hospital"],
                    "file_type": doc["file_type"],
                    "status": doc["status"],
                    "created_at": datetime.utcnow()
                })

        # 5. Seed Reference Shared Records matching SharedRecords.png
        shared_records_data = [
            {
                "name": "Dr. Meera Nair",
                "type": "Doctor",
                "shared_records": "Lab Reports, Prescriptions",
                "shared_on": "05 Sep 2025",
                "access_validity": "6 months (Valid till 05 Mar 2026)",
                "status": "Active"
            },
            {
                "name": "Govt. District Hospital Kannur",
                "type": "Hospital",
                "shared_records": "All Records",
                "shared_on": "12 Aug 2025",
                "access_validity": "1 year (Valid till 12 Aug 2026)",
                "status": "Active"
            },
            {
                "name": "Sun Diagnostics Thalassery",
                "type": "Diagnostic Centre",
                "shared_records": "Imaging Reports",
                "shared_on": "21 Jul 2025",
                "access_validity": "3 months (Valid till 21 Oct 2025)",
                "status": "Active"
            },
            {
                "name": "My Family (Parent) - Biju Mathew",
                "type": "Family Member",
                "shared_records": "Selected Records",
                "shared_on": "01 Jul 2025",
                "access_validity": "Permanent",
                "status": "Active"
            },
            {
                "name": "National Health Authority (ABDM)",
                "type": "Government",
                "shared_records": "Vaccination Records",
                "shared_on": "10 Jan 2025",
                "access_validity": "Permanent",
                "status": "Active"
            },
            {
                "name": "Apollo Hospitals Kochi",
                "type": "Hospital",
                "shared_records": "Discharge Summary, Lab Reports",
                "shared_on": "15 Jun 2025",
                "access_validity": "6 months (Valid till 15 Dec 2025)",
                "status": "Expired"
            }
        ]

        if mongo.db.shared_records.count_documents({}) < 6:
            for share in shared_records_data:
                mongo.db.shared_records.insert_one({
                    "patient_id": str(patient_id),
                    "name": share["name"],
                    "type": share["type"],
                    "shared_records": share["shared_records"],
                    "shared_on": share["shared_on"],
                    "access_validity": share["access_validity"],
                    "status": share["status"],
                    "created_at": datetime.utcnow()
                })

        # 6. Seed Appointments matching Appointments.png
        appointments_data = [
            {
                "date": "20 Sep 2026",
                "time": "10:00 AM",
                "day": "Saturday",
                "doctor_name": "Dr. Meera Nair",
                "facility": "KPHC Thalassery",
                "department": "General Medicine",
                "purpose": "Regular Checkup",
                "status": "Confirmed",
                "token_number": "A-026",
                "indicator_color": "#16A05D"
            },
            {
                "date": "05 Oct 2026",
                "time": "11:30 AM",
                "day": "Sunday",
                "doctor_name": "Dr. Arjun Kumar",
                "facility": "Govt. District Hospital Kannur",
                "department": "Orthopedics",
                "purpose": "Knee Pain Consultation",
                "status": "Scheduled",
                "token_number": "O-014",
                "indicator_color": "#D97706"
            },
            {
                "date": "18 Oct 2026",
                "time": "09:45 AM",
                "day": "Saturday",
                "doctor_name": "Dr. Sreelakshmi Nair",
                "facility": "Govt. Medical College Kannur",
                "department": "Dermatology",
                "purpose": "Skin Allergy",
                "status": "Scheduled",
                "token_number": "D-008",
                "indicator_color": "#3B82F6"
            },
            {
                "date": "02 Nov 2026",
                "time": "11:00 AM",
                "day": "Sunday",
                "doctor_name": "Dr. Faisal Rahman",
                "facility": "Sun Diagnostics Thalassery",
                "department": "Radiology",
                "purpose": "X-Ray Follow-up",
                "status": "Scheduled",
                "token_number": "R-004",
                "indicator_color": "#10B981"
            }
        ]

        if mongo.db.appointments.count_documents({}) < 4:
            for app in appointments_data:
                mongo.db.appointments.insert_one({
                    "patient_id": patient_id,
                    "date": app["date"],
                    "time": app["time"],
                    "day": app["day"],
                    "doctor_name": app["doctor_name"],
                    "facility": app["facility"],
                    "department": app["department"],
                    "purpose": app["purpose"],
                    "slot": f"{app['time']}",
                    "status": app["status"].lower(),
                    "token_number": app["token_number"],
                    "indicator_color": app["indicator_color"],
                    "created_at": datetime.utcnow()
                })

        mongo.db.settings.update_one({"key": "seed_completed"}, {"$set": {"seeded": True}}, upsert=True)
        _SEEDED = True
        print("Demo seed data initialization complete.")
    except Exception as e:
        print(f"Seed data error: {e}")
