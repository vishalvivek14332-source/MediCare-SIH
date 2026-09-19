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
    try:
        seed_core_patient_and_base()
        seed_healthcare_facilities_and_doctors()
        _SEEDED = True
    except Exception as e:
        print(f"Seed data error: {e}")

def seed_core_patient_and_base():
    try:
        if mongo.db.settings.find_one({"key": "seed_base_completed"}):
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

        mongo.db.settings.update_one({"key": "seed_base_completed"}, {"$set": {"seeded": True}}, upsert=True)
        print("Base seed data verified.")
    except Exception as e:
        print(f"Base seed data error: {e}")

def seed_healthcare_facilities_and_doctors():
    """
    Seed or update all 8 recognized medical systems facilities and specialist doctors
    across states (Kerala, Karnataka, Tamil Nadu, Delhi, Rajasthan, West Bengal, Ladakh, HP).
    All data is clearly categorized as 'Demo Facility' for sandbox testing unless officially verified.
    """
    facilities = [
        # 1. Modern / Conventional Medicine
        {
            "name": "Govt. District Hospital Kannur",
            "code": "GDHK01",
            "abdm_id": "HOSP001234",
            "medical_system": "Modern / Conventional Medicine",
            "facility_type": "Government Hospital",
            "address": "Hospital Road, Civil Station P.O., Kannur",
            "city": "Kannur",
            "district": "Kannur",
            "state": "Kerala",
            "pincode": "670002",
            "departments": ["General Medicine", "Orthopedics", "Cardiology", "Emergency Medicine", "ENT"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 497 273 1234",
            "latitude": 11.8745,
            "longitude": 75.3704,
            "status": "Active"
        },
        {
            "name": "KPHC Thalassery",
            "code": "KPHC02",
            "abdm_id": "HOSP005678",
            "medical_system": "Modern / Conventional Medicine",
            "facility_type": "Primary Health Centre",
            "address": "Main Road, Near Court Complex, Thalassery",
            "city": "Thalassery",
            "district": "Kannur",
            "state": "Kerala",
            "pincode": "670101",
            "departments": ["General Medicine", "Pediatrics", "Preventive Medicine"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 490 232 5678",
            "latitude": 11.7480,
            "longitude": 75.4894,
            "status": "Active"
        },
        {
            "name": "Govt. Medical College Kannur",
            "code": "GMCK03",
            "abdm_id": "HOSP009876",
            "medical_system": "Modern / Conventional Medicine",
            "facility_type": "Medical College Hospital",
            "address": "Pariyaram, Kannur",
            "city": "Kannur",
            "district": "Kannur",
            "state": "Kerala",
            "pincode": "670503",
            "departments": ["Dermatology", "General Medicine", "Neurology", "Orthopedics"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 497 283 9876",
            "latitude": 12.0024,
            "longitude": 75.3182,
            "status": "Active"
        },
        {
            "name": "Victoria Hospital Bengaluru",
            "code": "VHB01",
            "abdm_id": "HOSP011223",
            "medical_system": "Modern / Conventional Medicine",
            "facility_type": "Government Tertiary Hospital",
            "address": "Fort, K.R. Market, Bengaluru",
            "city": "Bengaluru",
            "district": "Bengaluru Urban",
            "state": "Karnataka",
            "pincode": "560002",
            "departments": ["General Medicine", "General Surgery", "Orthopedics", "Cardiology"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 80 2670 1150",
            "latitude": 12.9644,
            "longitude": 77.5750,
            "status": "Active"
        },
        {
            "name": "Rajiv Gandhi Government General Hospital Chennai",
            "code": "RGGGH01",
            "abdm_id": "HOSP022334",
            "medical_system": "Modern / Conventional Medicine",
            "facility_type": "Government General Hospital",
            "address": "EVR Periyar Salai, Park Town, Chennai",
            "city": "Chennai",
            "district": "Chennai",
            "state": "Tamil Nadu",
            "pincode": "600003",
            "departments": ["General Medicine", "Cardiology", "Neurology", "ENT"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 44 2530 5000",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "status": "Active"
        },
        {
            "name": "AIIMS New Delhi",
            "code": "AIIMS01",
            "abdm_id": "HOSP033445",
            "medical_system": "Modern / Conventional Medicine",
            "facility_type": "Apex Autonomous Institute",
            "address": "Ansari Nagar, New Delhi",
            "city": "New Delhi",
            "district": "New Delhi",
            "state": "Delhi",
            "pincode": "110029",
            "departments": ["General Medicine", "Cardiology", "Neurology", "Orthopedics", "Dermatology"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 11 2658 8500",
            "latitude": 28.5672,
            "longitude": 77.2100,
            "status": "Active"
        },

        # 2. Ayurveda
        {
            "name": "Government Ayurveda Hospital Kannur",
            "code": "GAHK01",
            "abdm_id": "AYU001122",
            "medical_system": "Ayurveda",
            "facility_type": "Government Ayurvedic Hospital",
            "address": "Near Old Bus Stand, Talap, Kannur",
            "city": "Kannur",
            "district": "Kannur",
            "state": "Kerala",
            "pincode": "670001",
            "departments": ["Kayachikitsa", "Panchakarma", "Shalya Tantra", "Swasthavritta"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 497 270 4589",
            "latitude": 11.8720,
            "longitude": 75.3680,
            "status": "Active"
        },
        {
            "name": "Kottakkal Arya Vaidya Sala",
            "code": "AVSK01",
            "abdm_id": "AYU002233",
            "medical_system": "Ayurveda",
            "facility_type": "Ayurvedic Healthcare & Research Centre",
            "address": "Kottakkal Post, Malappuram",
            "city": "Malappuram",
            "district": "Malappuram",
            "state": "Kerala",
            "pincode": "676503",
            "departments": ["Kayachikitsa", "Panchakarma", "Shalakya Tantra", "Prasuti & Stri Roga"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 483 280 8000",
            "latitude": 11.0020,
            "longitude": 75.9980,
            "status": "Active"
        },
        {
            "name": "National Institute of Ayurveda Jaipur",
            "code": "NIAJ01",
            "abdm_id": "AYU003344",
            "medical_system": "Ayurveda",
            "facility_type": "National Apex Ayurvedic Institute",
            "address": "Jorawar Singh Gate, Amer Road, Jaipur",
            "city": "Jaipur",
            "district": "Jaipur",
            "state": "Rajasthan",
            "pincode": "302002",
            "departments": ["Kayachikitsa", "Panchakarma", "Kaumarabhritya", "Shalya Tantra"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 141 263 5816",
            "latitude": 26.9380,
            "longitude": 75.8340,
            "status": "Active"
        },

        # 3. Homoeopathy
        {
            "name": "Govt. Homoeopathic Medical College Kozhikode",
            "code": "GHMCK01",
            "abdm_id": "HOM001122",
            "medical_system": "Homoeopathy",
            "facility_type": "Government Homoeopathic Hospital",
            "address": "Karaparamba, Kozhikode",
            "city": "Kozhikode",
            "district": "Kozhikode",
            "state": "Kerala",
            "pincode": "673010",
            "departments": ["General Homoeopathy", "Pediatrics", "Dermatology", "Chronic Diseases"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 495 237 0843",
            "latitude": 11.2850,
            "longitude": 75.7890,
            "status": "Active"
        },
        {
            "name": "National Institute of Homoeopathy Kolkata",
            "code": "NIHK01",
            "abdm_id": "HOM002233",
            "medical_system": "Homoeopathy",
            "facility_type": "Apex Homoeopathic Teaching Hospital",
            "address": "Block GE, Sector III, Salt Lake, Kolkata",
            "city": "Kolkata",
            "district": "Kolkata",
            "state": "West Bengal",
            "pincode": "700106",
            "departments": ["General Homoeopathy", "Respiratory Medicine", "Mental Health"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 33 2337 0969",
            "latitude": 22.5800,
            "longitude": 88.4100,
            "status": "Active"
        },

        # 4. Unani
        {
            "name": "Govt. Unani Hospital Bengaluru",
            "code": "GUHB01",
            "abdm_id": "UNA001122",
            "medical_system": "Unani",
            "facility_type": "Government Unani Hospital",
            "address": "Magadi Main Road, Agrahara Dasarahalli, Bengaluru",
            "city": "Bengaluru",
            "district": "Bengaluru Urban",
            "state": "Karnataka",
            "pincode": "560079",
            "departments": ["Moalijat (General Medicine)", "Ilaj-bil-Tadbeer (Regimenal Therapy)", "Ilmul Advia"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 80 2315 2345",
            "latitude": 12.9800,
            "longitude": 77.5400,
            "status": "Active"
        },
        {
            "name": "National Institute of Unani Medicine",
            "code": "NIUM01",
            "abdm_id": "UNA002233",
            "medical_system": "Unani",
            "facility_type": "Autonomous Unani Research Hospital",
            "address": "Kottigepalya, Magadi Main Road, Bengaluru",
            "city": "Bengaluru",
            "district": "Bengaluru Urban",
            "state": "Karnataka",
            "pincode": "560091",
            "departments": ["Moalijat (General Medicine)", "Jarahat (Surgery)", "Niswan wa Qabalat"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 80 2358 4260",
            "latitude": 12.9850,
            "longitude": 77.5100,
            "status": "Active"
        },

        # 5. Siddha
        {
            "name": "National Institute of Siddha Chennai",
            "code": "NISC01",
            "abdm_id": "SID001122",
            "medical_system": "Siddha",
            "facility_type": "Apex Siddha Hospital & Institute",
            "address": "Grand Southern Trunk Road, Tambaram Sanatorium, Chennai",
            "city": "Chennai",
            "district": "Chennai",
            "state": "Tamil Nadu",
            "pincode": "600047",
            "departments": ["General Siddha Medicine", "Pothu Maruthuvam", "Sirappu Maruthuvam", "Varma & Thokkanam"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 44 2241 1611",
            "latitude": 12.9350,
            "longitude": 80.1250,
            "status": "Active"
        },
        {
            "name": "Govt. Siddha Hospital Palayamkottai",
            "code": "GSHP01",
            "abdm_id": "SID002233",
            "medical_system": "Siddha",
            "facility_type": "Government Siddha Hospital",
            "address": "Tirunelveli High Road, Palayamkottai, Tirunelveli",
            "city": "Palayamkottai",
            "district": "Tirunelveli",
            "state": "Tamil Nadu",
            "pincode": "627002",
            "departments": ["General Siddha Medicine", "Pothu Maruthuvam", "Kuzhanthai Maruthuvam"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 462 257 2736",
            "latitude": 8.7180,
            "longitude": 77.7400,
            "status": "Active"
        },

        # 6. Sowa-Rigpa
        {
            "name": "Sowa-Rigpa Hospital Leh",
            "code": "SRHL01",
            "abdm_id": "SOW001122",
            "medical_system": "Sowa-Rigpa",
            "facility_type": "Traditional Himalayan Sowa-Rigpa Hospital",
            "address": "Choglamsar, Leh, Union Territory of Ladakh",
            "city": "Leh",
            "district": "Leh",
            "state": "Ladakh",
            "pincode": "194101",
            "departments": ["General Sowa-Rigpa Medicine", "Internal Medicine", "Traditional Moxibustion & Cupping"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 1982 264 437",
            "latitude": 34.1350,
            "longitude": 77.5850,
            "status": "Active"
        },
        {
            "name": "Sowa-Rigpa Health Centre Dharamshala",
            "code": "SRHCD01",
            "abdm_id": "SOW002233",
            "medical_system": "Sowa-Rigpa",
            "facility_type": "Himalayan Herbal Medical Centre",
            "address": "Gangchen Kyishong, Dharamshala",
            "city": "Dharamshala",
            "district": "Kangra",
            "state": "Himachal Pradesh",
            "pincode": "176215",
            "departments": ["General Sowa-Rigpa Medicine", "Himalayan Pharmacotherapy", "Mind-Body Diagnostics"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 1892 222 618",
            "latitude": 32.2200,
            "longitude": 76.3200,
            "status": "Active"
        },

        # 7. Yoga & Naturopathy
        {
            "name": "Morarji Desai National Institute of Yoga New Delhi",
            "code": "MDNIY01",
            "abdm_id": "YOG001122",
            "medical_system": "Yoga & Naturopathy",
            "facility_type": "Autonomous National Yoga & Naturopathy Centre",
            "address": "68, Ashok Road, Near Gole Dak Khana, New Delhi",
            "city": "New Delhi",
            "district": "New Delhi",
            "state": "Delhi",
            "pincode": "110001",
            "departments": ["Therapeutic Yoga", "Naturopathy Clinical OPD", "Stress & Lifestyle Management"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 11 2371 8301",
            "latitude": 28.6250,
            "longitude": 77.2100,
            "status": "Active"
        },
        {
            "name": "Govt. Nature Cure Hospital Bengaluru",
            "code": "GNCHB01",
            "abdm_id": "YOG002233",
            "medical_system": "Yoga & Naturopathy",
            "facility_type": "Government Naturopathy Hospital",
            "address": "P.K.T.B. Sanatorium Compound, Old Madras Road, Bengaluru",
            "city": "Bengaluru",
            "district": "Bengaluru Urban",
            "state": "Karnataka",
            "pincode": "560038",
            "departments": ["Naturopathy Clinical OPD", "Hydrotherapy & Mud Therapy", "Diet & Nutrition Counseling"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 80 2528 1432",
            "latitude": 12.9800,
            "longitude": 77.6500,
            "status": "Active"
        },

        # 8. Integrated AYUSH
        {
            "name": "Integrated AYUSH Centre New Delhi",
            "code": "IACND01",
            "abdm_id": "INT001122",
            "medical_system": "Integrated AYUSH",
            "facility_type": "Integrative Multi-System AYUSH Hospital",
            "address": "Gautampuri, Sarita Vihar, Mathura Road, New Delhi",
            "city": "New Delhi",
            "district": "New Delhi",
            "state": "Delhi",
            "pincode": "110076",
            "departments": ["Integrated Medicine OPD", "Ayurveda & Panchakarma", "Yoga & Naturopathy", "Homoeopathy"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 11 2695 0401",
            "latitude": 28.5250,
            "longitude": 77.2950,
            "status": "Active"
        },
        {
            "name": "Integrated AYUSH Hospital Kozhikode",
            "code": "IAHK01",
            "abdm_id": "INT002233",
            "medical_system": "Integrated AYUSH",
            "facility_type": "Government Integrated AYUSH Hospital",
            "address": "Civil Station Road, Eranjipalam, Kozhikode",
            "city": "Kozhikode",
            "district": "Kozhikode",
            "state": "Kerala",
            "pincode": "673020",
            "departments": ["Integrated Medicine OPD", "Ayurveda & Panchakarma", "Yoga Therapy", "Homoeopathy"],
            "verification_status": "Demo Facility",
            "availability": "Available Today",
            "contact_number": "+91 495 237 8990",
            "latitude": 11.2750,
            "longitude": 75.7950,
            "status": "Active"
        }
    ]

    facility_map = {}
    for fac in facilities:
        existing = mongo.db.clinics.find_one({"name": fac["name"]})
        if not existing:
            fac["created_at"] = datetime.utcnow()
            res = mongo.db.clinics.insert_one(fac)
            facility_map[fac["name"]] = str(res.inserted_id)
        else:
            # Update fields
            mongo.db.clinics.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "medical_system": fac["medical_system"],
                    "facility_type": fac["facility_type"],
                    "address": fac["address"],
                    "city": fac["city"],
                    "district": fac["district"],
                    "state": fac["state"],
                    "pincode": fac["pincode"],
                    "departments": fac["departments"],
                    "verification_status": fac["verification_status"],
                    "availability": fac["availability"],
                    "contact_number": fac["contact_number"]
                }}
            )
            facility_map[fac["name"]] = str(existing["_id"])

    # Specialist Doctors linked to facilities and specific departments
    doctors = [
        # Modern Medicine
        {
            "name": "Dr. Meera Nair",
            "email": "meera.nair@example.com",
            "qualification": "MBBS, MD (General Medicine)",
            "specialization": "Consultant Physician",
            "experience": "12 years",
            "medical_system": "Modern / Conventional Medicine",
            "department": "General Medicine",
            "facility_name": "KPHC Thalassery",
            "verification_status": "Verified ABDM Doctor",
            "fees": 200,
            "total_tokens": 16,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. Arjun Kumar",
            "email": "arjun.kumar@example.com",
            "qualification": "MBBS, MS (Orthopedics)",
            "specialization": "Orthopedic & Joint Surgeon",
            "experience": "11 years",
            "medical_system": "Modern / Conventional Medicine",
            "department": "Orthopedics",
            "facility_name": "Govt. District Hospital Kannur",
            "verification_status": "Verified ABDM Doctor",
            "fees": 250,
            "total_tokens": 14,
            "patient_ratings": 4.8,
            "avatar_url": ""
        },
        {
            "name": "Dr. Priya Sharma",
            "email": "priya.sharma@example.com",
            "qualification": "MBBS, MD (Internal Medicine)",
            "specialization": "Senior Consultant Physician",
            "experience": "8 years",
            "medical_system": "Modern / Conventional Medicine",
            "department": "General Medicine",
            "facility_name": "Govt. District Hospital Kannur",
            "verification_status": "Verified ABDM Doctor",
            "fees": 200,
            "total_tokens": 14,
            "patient_ratings": 4.7,
            "avatar_url": ""
        },
        {
            "name": "Dr. Sreelakshmi Nair",
            "email": "sreelakshmi.nair@example.com",
            "qualification": "MBBS, MD (Dermatology, Venereology & Leprosy)",
            "specialization": "Dermatologist & Cosmetologist",
            "experience": "9 years",
            "medical_system": "Modern / Conventional Medicine",
            "department": "Dermatology",
            "facility_name": "Govt. Medical College Kannur",
            "verification_status": "Verified ABDM Doctor",
            "fees": 300,
            "total_tokens": 12,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. Rajesh Kulkarni",
            "email": "rajesh.kulkarni@example.com",
            "qualification": "MBBS, MD (Internal Medicine)",
            "specialization": "Senior Physician",
            "experience": "14 years",
            "medical_system": "Modern / Conventional Medicine",
            "department": "General Medicine",
            "facility_name": "Victoria Hospital Bengaluru",
            "verification_status": "Verified ABDM Doctor",
            "fees": 250,
            "total_tokens": 16,
            "patient_ratings": 4.8,
            "avatar_url": ""
        },
        {
            "name": "Dr. Sivakumar Ramanathan",
            "email": "sivakumar.r@example.com",
            "qualification": "MBBS, MD, DM (Cardiology)",
            "specialization": "Senior Consultant Cardiologist",
            "experience": "16 years",
            "medical_system": "Modern / Conventional Medicine",
            "department": "Cardiology",
            "facility_name": "Rajiv Gandhi Government General Hospital Chennai",
            "verification_status": "Verified ABDM Doctor",
            "fees": 300,
            "total_tokens": 12,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. Harshavardhan Rao",
            "email": "harshavardhan.rao@example.com",
            "qualification": "MBBS, MD, DM (Neurology)",
            "specialization": "Professor & Head of Clinical OPD",
            "experience": "18 years",
            "medical_system": "Modern / Conventional Medicine",
            "department": "General Medicine",
            "facility_name": "AIIMS New Delhi",
            "verification_status": "Verified ABDM Doctor",
            "fees": 350,
            "total_tokens": 18,
            "patient_ratings": 5.0,
            "avatar_url": ""
        },

        # Ayurveda
        {
            "name": "Dr. Meera K. Warrier",
            "email": "meera.warrier@example.com",
            "qualification": "BAMS, MD (Kayachikitsa)",
            "specialization": "Chief Ayurvedic Physician",
            "experience": "12 years",
            "medical_system": "Ayurveda",
            "department": "Kayachikitsa",
            "facility_name": "Government Ayurveda Hospital Kannur",
            "verification_status": "Demo Facility Doctor",
            "fees": 150,
            "total_tokens": 16,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. Vineeth Nambiar",
            "email": "vineeth.nambiar@example.com",
            "qualification": "BAMS, Fellow in Panchakarma",
            "specialization": "Panchakarma Specialist",
            "experience": "8 years",
            "medical_system": "Ayurveda",
            "department": "Panchakarma",
            "facility_name": "Government Ayurveda Hospital Kannur",
            "verification_status": "Demo Facility Doctor",
            "fees": 150,
            "total_tokens": 14,
            "patient_ratings": 4.8,
            "avatar_url": ""
        },
        {
            "name": "Dr. K. Radhakrishnan",
            "email": "k.radhakrishnan@example.com",
            "qualification": "BAMS, MD (Ayurveda)",
            "specialization": "Senior Physician & Research Specialist",
            "experience": "20 years",
            "medical_system": "Ayurveda",
            "department": "Kayachikitsa",
            "facility_name": "Kottakkal Arya Vaidya Sala",
            "verification_status": "Demo Facility Doctor",
            "fees": 250,
            "total_tokens": 14,
            "patient_ratings": 5.0,
            "avatar_url": ""
        },
        {
            "name": "Dr. Rakesh Sharma",
            "email": "rakesh.sharma.ayu@example.com",
            "qualification": "BAMS, PhD (Ayurveda)",
            "specialization": "Professor of Kayachikitsa",
            "experience": "15 years",
            "medical_system": "Ayurveda",
            "department": "Kayachikitsa",
            "facility_name": "National Institute of Ayurveda Jaipur",
            "verification_status": "Demo Facility Doctor",
            "fees": 200,
            "total_tokens": 16,
            "patient_ratings": 4.8,
            "avatar_url": ""
        },

        # Homoeopathy
        {
            "name": "Dr. Ananya Das",
            "email": "ananya.das@example.com",
            "qualification": "BHMS, MD (Homoeopathy)",
            "specialization": "Senior Homoeopath & Pediatric Specialist",
            "experience": "10 years",
            "medical_system": "Homoeopathy",
            "department": "General Homoeopathy",
            "facility_name": "Govt. Homoeopathic Medical College Kozhikode",
            "verification_status": "Demo Facility Doctor",
            "fees": 150,
            "total_tokens": 15,
            "patient_ratings": 4.8,
            "avatar_url": ""
        },
        {
            "name": "Dr. Subhasish Mukherjee",
            "email": "subhasish.m@example.com",
            "qualification": "BHMS, MD (Homoeopathy)",
            "specialization": "Chronic Diseases & Constitutional Prescribing",
            "experience": "16 years",
            "medical_system": "Homoeopathy",
            "department": "General Homoeopathy",
            "facility_name": "National Institute of Homoeopathy Kolkata",
            "verification_status": "Demo Facility Doctor",
            "fees": 180,
            "total_tokens": 14,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },

        # Unani
        {
            "name": "Dr. Tariq Ahmad Khan",
            "email": "tariq.khan@example.com",
            "qualification": "BUMS, MD (Unani)",
            "specialization": "Moalijat (General Medicine) & Regimenal Therapy",
            "experience": "11 years",
            "medical_system": "Unani",
            "department": "Moalijat (General Medicine)",
            "facility_name": "Govt. Unani Hospital Bengaluru",
            "verification_status": "Demo Facility Doctor",
            "fees": 150,
            "total_tokens": 14,
            "patient_ratings": 4.7,
            "avatar_url": ""
        },
        {
            "name": "Dr. Aslam Farooqui",
            "email": "aslam.farooqui@example.com",
            "qualification": "BUMS, MD (Unani Medicine)",
            "specialization": "Senior Unani Consultant & Pharmacotherapy",
            "experience": "14 years",
            "medical_system": "Unani",
            "department": "Moalijat (General Medicine)",
            "facility_name": "National Institute of Unani Medicine",
            "verification_status": "Demo Facility Doctor",
            "fees": 180,
            "total_tokens": 14,
            "patient_ratings": 4.8,
            "avatar_url": ""
        },

        # Siddha
        {
            "name": "Dr. S. Muthulakshmi",
            "email": "muthulakshmi.s@example.com",
            "qualification": "BSMS, MD (Siddha)",
            "specialization": "General Siddha Medicine & Varma Therapy",
            "experience": "13 years",
            "medical_system": "Siddha",
            "department": "General Siddha Medicine",
            "facility_name": "National Institute of Siddha Chennai",
            "verification_status": "Demo Facility Doctor",
            "fees": 160,
            "total_tokens": 16,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. K. Murugesan",
            "email": "murugesan.k@example.com",
            "qualification": "BSMS",
            "specialization": "Pothu Maruthuvam Consultant",
            "experience": "9 years",
            "medical_system": "Siddha",
            "department": "Pothu Maruthuvam",
            "facility_name": "Govt. Siddha Hospital Palayamkottai",
            "verification_status": "Demo Facility Doctor",
            "fees": 140,
            "total_tokens": 12,
            "patient_ratings": 4.7,
            "avatar_url": ""
        },

        # Sowa-Rigpa
        {
            "name": "Dr. Tenzin Norbu",
            "email": "tenzin.norbu@example.com",
            "qualification": "Kachupa / Menrampa (Sowa-Rigpa)",
            "specialization": "Senior Amchi & Himalayan Herbalist",
            "experience": "15 years",
            "medical_system": "Sowa-Rigpa",
            "department": "General Sowa-Rigpa Medicine",
            "facility_name": "Sowa-Rigpa Hospital Leh",
            "verification_status": "Demo Facility Doctor",
            "fees": 150,
            "total_tokens": 12,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. Lobsang Wangdu",
            "email": "lobsang.wangdu@example.com",
            "qualification": "Menrampa (Traditional Tibetan Medicine)",
            "specialization": "Pulse Diagnostics & Herbal Formulations",
            "experience": "11 years",
            "medical_system": "Sowa-Rigpa",
            "department": "General Sowa-Rigpa Medicine",
            "facility_name": "Sowa-Rigpa Health Centre Dharamshala",
            "verification_status": "Demo Facility Doctor",
            "fees": 140,
            "total_tokens": 12,
            "patient_ratings": 4.8,
            "avatar_url": ""
        },

        # Yoga & Naturopathy
        {
            "name": "Dr. Sunita Verma",
            "email": "sunita.verma@example.com",
            "qualification": "BNYS, MD (Yoga)",
            "specialization": "Therapeutic Yoga & Lifestyle Interventionist",
            "experience": "12 years",
            "medical_system": "Yoga & Naturopathy",
            "department": "Therapeutic Yoga",
            "facility_name": "Morarji Desai National Institute of Yoga New Delhi",
            "verification_status": "Demo Facility Doctor",
            "fees": 160,
            "total_tokens": 14,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. Chetan Gowda",
            "email": "chetan.gowda@example.com",
            "qualification": "BNYS",
            "specialization": "Clinical Naturopath & Hydrotherapist",
            "experience": "9 years",
            "medical_system": "Yoga & Naturopathy",
            "department": "Naturopathy Clinical OPD",
            "facility_name": "Govt. Nature Cure Hospital Bengaluru",
            "verification_status": "Demo Facility Doctor",
            "fees": 140,
            "total_tokens": 12,
            "patient_ratings": 4.7,
            "avatar_url": ""
        },

        # Integrated AYUSH
        {
            "name": "Dr. Arvind Swaminathan",
            "email": "arvind.swami@example.com",
            "qualification": "BAMS, MD (Ayurveda), Fellow in Integrative Medicine",
            "specialization": "Integrative Health Consultant",
            "experience": "17 years",
            "medical_system": "Integrated AYUSH",
            "department": "Integrated Medicine OPD",
            "facility_name": "Integrated AYUSH Centre New Delhi",
            "verification_status": "Demo Facility Doctor",
            "fees": 250,
            "total_tokens": 16,
            "patient_ratings": 4.9,
            "avatar_url": ""
        },
        {
            "name": "Dr. Reshma Menon",
            "email": "reshma.menon@example.com",
            "qualification": "BAMS, PGD in Yoga Therapy",
            "specialization": "Ayurveda & Holistic Lifestyle Physician",
            "experience": "10 years",
            "medical_system": "Integrated AYUSH",
            "department": "Integrated Medicine OPD",
            "facility_name": "Integrated AYUSH Hospital Kozhikode",
            "verification_status": "Demo Facility Doctor",
            "fees": 180,
            "total_tokens": 14,
            "patient_ratings": 4.8,
            "avatar_url": ""
        }
    ]

    for doc in doctors:
        f_id = facility_map.get(doc["facility_name"])
        doc["clinic_id"] = f_id
        existing = mongo.db.doctors.find_one({"email": doc["email"]})
        if not existing:
            doc["password"] = generate_password_hash("doctor123")
            doc["created_at"] = datetime.utcnow()
            mongo.db.doctors.insert_one(doc)
        else:
            mongo.db.doctors.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "qualification": doc["qualification"],
                    "specialization": doc["specialization"],
                    "experience": doc["experience"],
                    "medical_system": doc["medical_system"],
                    "department": doc["department"],
                    "facility_name": doc["facility_name"],
                    "clinic_id": f_id or existing.get("clinic_id"),
                    "verification_status": doc["verification_status"],
                    "fees": doc["fees"],
                    "total_tokens": doc["total_tokens"],
                    "patient_ratings": doc["patient_ratings"]
                }}
            )

    # Create helpful indexes for fast search & server-side filtering
    try:
        mongo.db.clinics.create_index([("medical_system", 1)])
        mongo.db.clinics.create_index([("state", 1), ("district", 1), ("city", 1)])
        mongo.db.clinics.create_index([("name", "text"), ("address", "text")])
        mongo.db.doctors.create_index([("clinic_id", 1), ("department", 1)])
        mongo.db.appointments.create_index([("doctor_id", 1), ("date", 1)])
        mongo.db.appointments.create_index([("patient_id", 1)])
    except Exception:
        pass

    mongo.db.settings.update_one({"key": "seed_ayush_v2_completed"}, {"$set": {"seeded": True}}, upsert=True)
    print("Multi-system facilities and doctors seeding complete.")
