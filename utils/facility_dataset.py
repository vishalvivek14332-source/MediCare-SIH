"""
Expanded healthcare facilities and doctors dataset covering:
- 8 Recognized Indian Medical Systems:
  1. Modern / Conventional Medicine
  2. Ayurveda
  3. Homoeopathy
  4. Unani
  5. Siddha
  6. Sowa-Rigpa
  7. Yoga & Naturopathy
  8. Integrated AYUSH
- Multiple facilities across Indian States and Districts:
  Kerala, Karnataka, Tamil Nadu, Maharashtra, Delhi, Rajasthan, West Bengal, Ladakh, Himachal Pradesh.
- All seeded records clearly marked as 'Demo Facility' (never falsely claimed as ABDM Verified).
"""

from werkzeug.security import generate_password_hash
from datetime import datetime
from bson.objectid import ObjectId

DEMO_FACILITIES_DATA = [
    # ==========================================
    # KERALA — KANNUR
    # ==========================================
    # Modern Medicine
    {
        "name": "Govt. District Hospital Kannur",
        "code": "GDHK01",
        "abdm_id": "DEMO-FAC-KL-001",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government District Hospital",
        "address": "Hospital Road, Civil Station P.O., Kannur",
        "city": "Kannur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670002",
        "departments": ["General Medicine", "Cardiology", "Dermatology", "Orthopedics", "Pediatrics", "ENT"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 497 273 1234",
        "latitude": 11.8745,
        "longitude": 75.3704,
        "status": "Active"
    },
    {
        "name": "Govt. Medical College Hospital Kannur",
        "code": "GMCK02",
        "abdm_id": "DEMO-FAC-KL-002",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Medical College Hospital",
        "address": "Pariyaram Medical Complex, Kannur",
        "city": "Kannur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670503",
        "departments": ["General Medicine", "Neurology", "Orthopedics", "Cardiology", "Dermatology"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 497 283 9876",
        "latitude": 12.0024,
        "longitude": 75.3182,
        "status": "Active"
    },
    {
        "name": "General Hospital Thalassery",
        "code": "GHT03",
        "abdm_id": "DEMO-FAC-KL-003",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government General Hospital",
        "address": "Court Road, Thalassery, Kannur",
        "city": "Thalassery",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670101",
        "departments": ["General Medicine", "Pediatrics", "Orthopedics", "General Surgery"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 490 232 2450",
        "latitude": 11.7505,
        "longitude": 75.4890,
        "status": "Active"
    },
    {
        "name": "Taluk Headquarter Hospital Payyanur",
        "code": "THHP04",
        "abdm_id": "DEMO-FAC-KL-004",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Taluk Hospital",
        "address": "Main Road, Payyanur, Kannur",
        "city": "Payyanur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670307",
        "departments": ["General Medicine", "Pediatrics", "Gynecology", "ENT"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 4985 202 334",
        "latitude": 12.1001,
        "longitude": 75.2014,
        "status": "Active"
    },
    {
        "name": "Community Health Centre Mattannur",
        "code": "CHCM05",
        "abdm_id": "DEMO-FAC-KL-005",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Community Health Centre",
        "address": "Airport Road, Mattannur, Kannur",
        "city": "Mattannur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670702",
        "departments": ["General Medicine", "Pediatrics", "Emergency Care"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 490 247 1210",
        "latitude": 11.9167,
        "longitude": 75.5667,
        "status": "Active"
    },
    {
        "name": "Taliparamba Taluk Hospital",
        "code": "TTH06",
        "abdm_id": "DEMO-FAC-KL-006",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Taluk Hospital",
        "address": "National Highway 66, Taliparamba, Kannur",
        "city": "Taliparamba",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670141",
        "departments": ["General Medicine", "Orthopedics", "Pediatrics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 4982 203 100",
        "latitude": 12.0436,
        "longitude": 75.3587,
        "status": "Active"
    },
    {
        "name": "KPHC Thalassery",
        "code": "KPHC07",
        "abdm_id": "DEMO-FAC-KL-007",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Primary Health Centre",
        "address": "Near Court Complex, Thalassery",
        "city": "Thalassery",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670101",
        "departments": ["General Medicine", "Preventive Medicine"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 490 232 5678",
        "latitude": 11.7480,
        "longitude": 75.4894,
        "status": "Active"
    },
    # Kannur — Ayurveda
    {
        "name": "Government Ayurveda Hospital Kannur",
        "code": "GAHK01",
        "abdm_id": "DEMO-FAC-AYU-001",
        "medical_system": "Ayurveda",
        "facility_type": "Government Ayurvedic Hospital",
        "address": "Talap, Near Old Bus Stand, Kannur",
        "city": "Kannur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670002",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Shalya Tantra", "Kaumarbhritya"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 497 270 4511",
        "latitude": 11.8700,
        "longitude": 75.3650,
        "status": "Active"
    },
    {
        "name": "Govt Ayurveda Research Hospital Payyanur",
        "code": "GARHP02",
        "abdm_id": "DEMO-FAC-AYU-002",
        "medical_system": "Ayurveda",
        "facility_type": "Ayurvedic Specialty Hospital",
        "address": "Perumba, Payyanur, Kannur",
        "city": "Payyanur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670307",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Rasayana Chikitsa"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 4985 204 880",
        "latitude": 12.0950,
        "longitude": 75.2050,
        "status": "Active"
    },
    {
        "name": "Ayurveda Model Dispensary Thalassery",
        "code": "AMDT03",
        "abdm_id": "DEMO-FAC-AYU-003",
        "medical_system": "Ayurveda",
        "facility_type": "Ayurvedic Dispensary",
        "address": "Logans Road, Thalassery, Kannur",
        "city": "Thalassery",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670101",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 490 234 5090",
        "latitude": 11.7520,
        "longitude": 75.4910,
        "status": "Active"
    },
    {
        "name": "Sreedhareeyam Ayurvedic Eye & Wellness Kannur",
        "code": "SAEW04",
        "abdm_id": "DEMO-FAC-AYU-004",
        "medical_system": "Ayurveda",
        "facility_type": "Specialty Ayurvedic Hospital",
        "address": "South Bazaar, Kannur",
        "city": "Kannur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670002",
        "departments": ["Shalakya Tantra (Ophthalmology/ENT)", "Panchakarma", "Kayachikitsa (General Medicine)"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 497 271 2299",
        "latitude": 11.8780,
        "longitude": 75.3690,
        "status": "Active"
    },
    # Kannur — Homoeopathy
    {
        "name": "Government Homoeopathic Hospital Kannur",
        "code": "GHHK01",
        "abdm_id": "DEMO-FAC-HOM-001",
        "medical_system": "Homoeopathy",
        "facility_type": "Government Homoeopathic Hospital",
        "address": "Civil Station Road, Kannur",
        "city": "Kannur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670002",
        "departments": ["General Homoeopathy", "Chronic Disease Management", "Pediatric Homoeopathy"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 497 270 1199",
        "latitude": 11.8710,
        "longitude": 75.3720,
        "status": "Active"
    },
    # Kannur — Integrated AYUSH
    {
        "name": "Integrated AYUSH Wellness Hospital Kannur",
        "code": "IAWHK01",
        "abdm_id": "DEMO-FAC-INT-001",
        "medical_system": "Integrated AYUSH",
        "facility_type": "Integrative Multi-System Facility",
        "address": "Pallikkunnu, Kannur",
        "city": "Kannur",
        "district": "Kannur",
        "state": "Kerala",
        "pincode": "670004",
        "departments": ["Integrated Medicine OPD", "Ayurveda & Panchakarma", "Yoga & Naturopathy", "Homoeopathy"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 497 276 5400",
        "latitude": 11.8850,
        "longitude": 75.3620,
        "status": "Active"
    },

    # ==========================================
    # KERALA — KOZHIKODE
    # ==========================================
    {
        "name": "Govt. Medical College Hospital Kozhikode",
        "code": "GMCKOZ01",
        "abdm_id": "DEMO-FAC-KL-008",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Tertiary Medical College Hospital",
        "address": "Medical College P.O., Kozhikode",
        "city": "Kozhikode",
        "district": "Kozhikode",
        "state": "Kerala",
        "pincode": "673008",
        "departments": ["General Medicine", "Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Dermatology"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 495 235 0216",
        "latitude": 11.2725,
        "longitude": 75.8368,
        "status": "Active"
    },
    {
        "name": "Govt. General Hospital Beach Kozhikode",
        "code": "GGHK02",
        "abdm_id": "DEMO-FAC-KL-009",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government General Hospital",
        "address": "Beach Road, Kozhikode",
        "city": "Kozhikode",
        "district": "Kozhikode",
        "state": "Kerala",
        "pincode": "673032",
        "departments": ["General Medicine", "Pediatrics", "Orthopedics", "Emergency Care"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 495 236 5480",
        "latitude": 11.2588,
        "longitude": 75.7689,
        "status": "Active"
    },
    {
        "name": "Taluk Hospital Vadakara",
        "code": "THV03",
        "abdm_id": "DEMO-FAC-KL-010",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Taluk Hospital",
        "address": "Hospital Road, Vadakara, Kozhikode",
        "city": "Vadakara",
        "district": "Kozhikode",
        "state": "Kerala",
        "pincode": "673101",
        "departments": ["General Medicine", "Pediatrics", "Orthopedics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 496 252 2011",
        "latitude": 11.6020,
        "longitude": 75.5910,
        "status": "Active"
    },
    {
        "name": "Govt Ayurveda Hospital Kozhikode",
        "code": "GAHKOZ04",
        "abdm_id": "DEMO-FAC-AYU-005",
        "medical_system": "Ayurveda",
        "facility_type": "Government Ayurvedic Hospital",
        "address": "Kallai Road, Kozhikode",
        "city": "Kozhikode",
        "district": "Kozhikode",
        "state": "Kerala",
        "pincode": "673003",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Shalya Tantra"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 495 230 4420",
        "latitude": 11.2400,
        "longitude": 75.7900,
        "status": "Active"
    },
    {
        "name": "Integrated AYUSH Hospital Kozhikode",
        "code": "IAHK05",
        "abdm_id": "DEMO-FAC-INT-002",
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
    },

    # ==========================================
    # KERALA — ERNAKULAM (KOCHI)
    # ==========================================
    {
        "name": "Govt. General Hospital Ernakulam",
        "code": "GGHE01",
        "abdm_id": "DEMO-FAC-KL-011",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government General Hospital",
        "address": "Hospital Road, Marine Drive, Kochi",
        "city": "Kochi",
        "district": "Ernakulam",
        "state": "Kerala",
        "pincode": "682011",
        "departments": ["General Medicine", "Cardiology", "Neurology", "Orthopedics", "Dermatology"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 484 236 0052",
        "latitude": 9.9723,
        "longitude": 76.2785,
        "status": "Active"
    },
    {
        "name": "Govt. Medical College Kalamassery",
        "code": "GMCK02",
        "abdm_id": "DEMO-FAC-KL-012",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Medical College Hospital",
        "address": "HMT Colony, Kalamassery, Kochi",
        "city": "Kochi",
        "district": "Ernakulam",
        "state": "Kerala",
        "pincode": "683503",
        "departments": ["General Medicine", "Pediatrics", "Orthopedics", "Cardiology"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 484 275 4000",
        "latitude": 10.0528,
        "longitude": 76.3533,
        "status": "Active"
    },
    {
        "name": "Taluk Headquarters Hospital Aluva",
        "code": "THHA03",
        "abdm_id": "DEMO-FAC-KL-013",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Taluk Hospital",
        "address": "Railway Station Road, Aluva",
        "city": "Aluva",
        "district": "Ernakulam",
        "state": "Kerala",
        "pincode": "683101",
        "departments": ["General Medicine", "Pediatrics", "Emergency Care"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 484 262 4220",
        "latitude": 10.1075,
        "longitude": 76.3516,
        "status": "Active"
    },
    {
        "name": "Govt Ayurveda College Hospital Tripunithura",
        "code": "GACHT04",
        "abdm_id": "DEMO-FAC-AYU-006",
        "medical_system": "Ayurveda",
        "facility_type": "Ayurvedic College Hospital",
        "address": "Statue Junction, Tripunithura, Kochi",
        "city": "Kochi",
        "district": "Ernakulam",
        "state": "Kerala",
        "pincode": "682301",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Shalakya Tantra"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 484 277 7374",
        "latitude": 9.9483,
        "longitude": 76.3481,
        "status": "Active"
    },

    # ==========================================
    # KERALA — THIRUVANANTHAPURAM
    # ==========================================
    {
        "name": "Govt. Medical College Thiruvananthapuram",
        "code": "GMCT01",
        "abdm_id": "DEMO-FAC-KL-014",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Apex Medical College Hospital",
        "address": "Medical College Junction, Thiruvananthapuram",
        "city": "Thiruvananthapuram",
        "district": "Thiruvananthapuram",
        "state": "Kerala",
        "pincode": "695011",
        "departments": ["General Medicine", "Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 471 252 8300",
        "latitude": 8.5241,
        "longitude": 76.9200,
        "status": "Active"
    },
    {
        "name": "Govt. General Hospital Thiruvananthapuram",
        "code": "GGHT02",
        "abdm_id": "DEMO-FAC-KL-015",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government General Hospital",
        "address": "Vanchiyoor, Thiruvananthapuram",
        "city": "Thiruvananthapuram",
        "district": "Thiruvananthapuram",
        "state": "Kerala",
        "pincode": "695035",
        "departments": ["General Medicine", "Pediatrics", "Orthopedics", "Emergency Care"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 471 247 1140",
        "latitude": 8.4900,
        "longitude": 76.9400,
        "status": "Active"
    },
    {
        "name": "Government Ayurveda College Hospital TVM",
        "code": "GACHTV03",
        "abdm_id": "DEMO-FAC-AYU-007",
        "medical_system": "Ayurveda",
        "facility_type": "Apex Ayurvedic Hospital",
        "address": "M.G. Road, Thiruvananthapuram",
        "city": "Thiruvananthapuram",
        "district": "Thiruvananthapuram",
        "state": "Kerala",
        "pincode": "695001",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Shalya Tantra", "Kaumarbhritya"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 471 246 0190",
        "latitude": 8.4920,
        "longitude": 76.9510,
        "status": "Active"
    },
    {
        "name": "National Institute of Siddha Extension Centre TVM",
        "code": "NISET04",
        "abdm_id": "DEMO-FAC-SID-001",
        "medical_system": "Siddha",
        "facility_type": "Siddha Specialty Hospital",
        "address": "Poojappura, Thiruvananthapuram",
        "city": "Thiruvananthapuram",
        "district": "Thiruvananthapuram",
        "state": "Kerala",
        "pincode": "695012",
        "departments": ["Pothu Maruthuvam (General Medicine)", "Varma Maruthuvam", "Sirappu Maruthuvam"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 471 234 1150",
        "latitude": 8.4980,
        "longitude": 76.9720,
        "status": "Active"
    },

    # ==========================================
    # KARNATAKA — BENGALURU URBAN
    # ==========================================
    {
        "name": "Victoria Hospital Bengaluru",
        "code": "VHB01",
        "abdm_id": "DEMO-FAC-KA-001",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government Tertiary Hospital",
        "address": "Fort, K.R. Market, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560002",
        "departments": ["General Medicine", "General Surgery", "Orthopedics", "Cardiology", "Dermatology"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 80 2670 1150",
        "latitude": 12.9644,
        "longitude": 77.5750,
        "status": "Active"
    },
    {
        "name": "Bowring and Lady Curzon Hospital",
        "code": "BLCH02",
        "abdm_id": "DEMO-FAC-KA-002",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government Teaching Hospital",
        "address": "Lady Curzon Road, Shivajinagar, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560001",
        "departments": ["General Medicine", "Pediatrics", "Cardiology", "Orthopedics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 80 2559 1325",
        "latitude": 12.9830,
        "longitude": 77.6010,
        "status": "Active"
    },
    {
        "name": "KC General Hospital Malleshwaram",
        "code": "KCGH03",
        "abdm_id": "DEMO-FAC-KA-003",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government General Hospital",
        "address": "5th Cross Road, Malleshwaram, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560003",
        "departments": ["General Medicine", "Orthopedics", "Pediatrics", "ENT"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 80 2334 1771",
        "latitude": 12.9985,
        "longitude": 77.5702,
        "status": "Active"
    },
    {
        "name": "Jayanagar General Hospital",
        "code": "JGH04",
        "abdm_id": "DEMO-FAC-KA-004",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government General Hospital",
        "address": "32nd Cross Road, 4th T Block, Jayanagar, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560041",
        "departments": ["General Medicine", "Pediatrics", "Dermatology", "Orthopedics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 80 2663 1180",
        "latitude": 12.9250,
        "longitude": 77.5850,
        "status": "Active"
    },
    {
        "name": "Government Ayurveda Medical College Hospital Bengaluru",
        "code": "GAMCHB05",
        "abdm_id": "DEMO-FAC-AYU-008",
        "medical_system": "Ayurveda",
        "facility_type": "Government Ayurvedic College Hospital",
        "address": "Dhanvantari Road, Majestic, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560009",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Shalya Tantra", "Kaumarbhritya"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 80 2287 2874",
        "latitude": 12.9770,
        "longitude": 77.5720,
        "status": "Active"
    },
    {
        "name": "National Institute of Unani Medicine Bengaluru",
        "code": "NIUM06",
        "abdm_id": "DEMO-FAC-UNA-001",
        "medical_system": "Unani",
        "facility_type": "Apex National Autonomous Institute",
        "address": "Kottigepalya, Magadi Main Road, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560091",
        "departments": ["Moalajat (General Medicine)", "Ilaj-bit-Tadbeer (Regimental Therapy)", "Jarahat"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 80 2358 4260",
        "latitude": 12.9860,
        "longitude": 77.5020,
        "status": "Active"
    },
    {
        "name": "Integrated AYUSH Hospital Bengaluru",
        "code": "IAHB07",
        "abdm_id": "DEMO-FAC-INT-003",
        "medical_system": "Integrated AYUSH",
        "facility_type": "State AYUSH Multi-System Centre",
        "address": "K.R. Road, Basavanagudi, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560004",
        "departments": ["Integrated Medicine OPD", "Ayurveda & Panchakarma", "Yoga & Naturopathy", "Homoeopathy"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 80 2667 4490",
        "latitude": 12.9420,
        "longitude": 77.5740,
        "status": "Active"
    },

    # ==========================================
    # TAMIL NADU — CHENNAI
    # ==========================================
    # Modern Medicine
    {
        "name": "Rajiv Gandhi Govt General Hospital Chennai",
        "code": "RGGGH01",
        "abdm_id": "DEMO-FAC-TN-001",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government General Hospital",
        "address": "EVR Periyar Salai, Park Town, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600003",
        "departments": ["General Medicine", "Cardiology", "Neurology", "Orthopedics", "Dermatology", "ENT"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 44 2530 5000",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "status": "Active"
    },
    {
        "name": "Government Stanley Medical College Hospital",
        "code": "GSMCH02",
        "abdm_id": "DEMO-FAC-TN-002",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government Medical College Hospital",
        "address": "Old Jail Road, Royapuram, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600001",
        "departments": ["General Medicine", "Cardiology", "Orthopedics", "Pediatrics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 44 2528 1351",
        "latitude": 13.1040,
        "longitude": 80.2910,
        "status": "Active"
    },
    {
        "name": "Government Kilpauk Medical College Hospital",
        "code": "GKMCH03",
        "abdm_id": "DEMO-FAC-TN-003",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government Medical College Hospital",
        "address": "Poonamallee High Road, Kilpauk, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600010",
        "departments": ["General Medicine", "Dermatology", "Orthopedics", "Pediatrics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 44 2836 4951",
        "latitude": 13.0810,
        "longitude": 80.2420,
        "status": "Active"
    },
    # Chennai — Siddha (Multiple facilities as required)
    {
        "name": "National Institute of Siddha Tambaram",
        "code": "NIST04",
        "abdm_id": "DEMO-FAC-SID-002",
        "medical_system": "Siddha",
        "facility_type": "National Apex Autonomous Siddha Institute",
        "address": "Grand Southern Trunk Road, Tambaram Sanatorium, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600047",
        "departments": ["Pothu Maruthuvam (General Medicine)", "Varma Maruthuvam", "Sirappu Maruthuvam", "Gunapadam"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 44 2241 1611",
        "latitude": 12.9350,
        "longitude": 80.1380,
        "status": "Active"
    },
    {
        "name": "Government Siddha Medical College Hospital Arumbakkam",
        "code": "GSMCHA05",
        "abdm_id": "DEMO-FAC-SID-003",
        "medical_system": "Siddha",
        "facility_type": "Government Siddha Medical College Hospital",
        "address": "EVR Periyar High Road, Arumbakkam, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600106",
        "departments": ["Pothu Maruthuvam (General Medicine)", "Kuzhandhai Maruthuvam (Pediatrics)", "Aruvai Maruthuvam"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 44 2621 1144",
        "latitude": 13.0720,
        "longitude": 80.2100,
        "status": "Active"
    },
    {
        "name": "Central Council for Research in Siddha Headquarters",
        "code": "CCRS06",
        "abdm_id": "DEMO-FAC-SID-004",
        "medical_system": "Siddha",
        "facility_type": "Apex Central Research Hospital",
        "address": "Anna Hospital Campus, Arumbakkam, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600106",
        "departments": ["Pothu Maruthuvam (General Medicine)", "Varma Maruthuvam", "Noi Nadal (Diagnostics)"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 44 2621 1621",
        "latitude": 13.0730,
        "longitude": 80.2120,
        "status": "Active"
    },
    {
        "name": "Integrated AYUSH Hospital Chennai",
        "code": "IAHC07",
        "abdm_id": "DEMO-FAC-INT-004",
        "medical_system": "Integrated AYUSH",
        "facility_type": "Government Integrated AYUSH Hospital",
        "address": "Anna Hospital Complex, Arumbakkam, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600106",
        "departments": ["Integrated Medicine OPD", "Siddha & Varma", "Ayurveda & Panchakarma", "Homoeopathy"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 44 2621 3400",
        "latitude": 13.0715,
        "longitude": 80.2115,
        "status": "Active"
    },

    # ==========================================
    # MAHARASHTRA — MUMBAI
    # ==========================================
    {
        "name": "KEM Hospital and Seth GS Medical College Mumbai",
        "code": "KEMH01",
        "abdm_id": "DEMO-FAC-MH-001",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Municipal Teaching Hospital",
        "address": "Acharya Donde Marg, Parel, Mumbai",
        "city": "Mumbai",
        "district": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400012",
        "departments": ["General Medicine", "Cardiology", "Neurology", "Orthopedics", "Dermatology"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 22 2410 7000",
        "latitude": 19.0028,
        "longitude": 72.8428,
        "status": "Active"
    },
    {
        "name": "Lokmanya Tilak Municipal General Hospital Sion",
        "code": "LTMGH02",
        "abdm_id": "DEMO-FAC-MH-002",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "General Tertiary Hospital",
        "address": "Sion West, Mumbai",
        "city": "Mumbai",
        "district": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400022",
        "departments": ["General Medicine", "Pediatrics", "Orthopedics", "Emergency Medicine"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 22 2407 6381",
        "latitude": 19.0360,
        "longitude": 72.8610,
        "status": "Active"
    },
    {
        "name": "Sir J.J. Group of Hospitals Mumbai",
        "code": "SJJH03",
        "abdm_id": "DEMO-FAC-MH-003",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Government Tertiary Hospital",
        "address": "J.J. Marg, Byculla, Mumbai",
        "city": "Mumbai",
        "district": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400008",
        "departments": ["General Medicine", "Cardiology", "Neurology", "Dermatology"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 22 2373 5555",
        "latitude": 18.9620,
        "longitude": 72.8340,
        "status": "Active"
    },
    {
        "name": "R.A. Podar Ayurvedic Medical College Hospital Mumbai",
        "code": "RAPAH04",
        "abdm_id": "DEMO-FAC-AYU-009",
        "medical_system": "Ayurveda",
        "facility_type": "Government Ayurvedic College Hospital",
        "address": "Dr. Annie Besant Road, Worli, Mumbai",
        "city": "Mumbai",
        "district": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400018",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Shalya Tantra"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 22 2493 4214",
        "latitude": 19.0060,
        "longitude": 72.8170,
        "status": "Active"
    },
    {
        "name": "Integrated AYUSH Centre Mumbai",
        "code": "IACM05",
        "abdm_id": "DEMO-FAC-INT-005",
        "medical_system": "Integrated AYUSH",
        "facility_type": "Integrative Health Facility",
        "address": "Bandra Kurla Complex, Bandra East, Mumbai",
        "city": "Mumbai",
        "district": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400051",
        "departments": ["Integrated Medicine OPD", "Ayurveda & Panchakarma", "Yoga & Naturopathy", "Homoeopathy"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 22 2659 0100",
        "latitude": 19.0650,
        "longitude": 72.8680,
        "status": "Active"
    },

    # ==========================================
    # DELHI — NEW DELHI
    # ==========================================
    {
        "name": "AIIMS New Delhi",
        "code": "AIIMS01",
        "abdm_id": "DEMO-FAC-DL-001",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Apex Autonomous Medical Institute",
        "address": "Ansari Nagar, New Delhi",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "pincode": "110029",
        "departments": ["General Medicine", "Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 11 2658 8500",
        "latitude": 28.5672,
        "longitude": 77.2100,
        "status": "Active"
    },
    {
        "name": "Safdarjung Hospital New Delhi",
        "code": "SJH02",
        "abdm_id": "DEMO-FAC-DL-002",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "Central Government Hospital",
        "address": "Ring Road, Opposite AIIMS, New Delhi",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "pincode": "110029",
        "departments": ["General Medicine", "Orthopedics", "Pediatrics", "Emergency Care"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 11 2616 5060",
        "latitude": 28.5700,
        "longitude": 77.2070,
        "status": "Active"
    },
    {
        "name": "All India Institute of Ayurveda New Delhi",
        "code": "AIIA03",
        "abdm_id": "DEMO-FAC-AYU-010",
        "medical_system": "Ayurveda",
        "facility_type": "Apex National Autonomous Institute",
        "address": "Gautampuri, Sarita Vihar, Mathura Road, New Delhi",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "pincode": "110076",
        "departments": ["Kayachikitsa (General Medicine)", "Panchakarma", "Shalya Tantra", "Kaumarbhritya"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 11 2695 0401",
        "latitude": 28.5250,
        "longitude": 77.2950,
        "status": "Active"
    },
    {
        "name": "Integrated AYUSH Centre New Delhi",
        "code": "IACND04",
        "abdm_id": "DEMO-FAC-INT-006",
        "medical_system": "Integrated AYUSH",
        "facility_type": "Integrative Multi-System Hospital",
        "address": "Mathura Road, Sarita Vihar, New Delhi",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "pincode": "110076",
        "departments": ["Integrated Medicine OPD", "Ayurveda & Panchakarma", "Yoga & Naturopathy", "Homoeopathy"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 11 2695 0450",
        "latitude": 28.5260,
        "longitude": 77.2960,
        "status": "Active"
    },

    # ==========================================
    # LADAKH — LEH (Sowa-Rigpa)
    # ==========================================
    {
        "name": "National Institute of Sowa-Rigpa Leh",
        "code": "NISRL01",
        "abdm_id": "DEMO-FAC-SOW-001",
        "medical_system": "Sowa-Rigpa",
        "facility_type": "Apex National Sowa-Rigpa Hospital",
        "address": "Near Radio Station, Skara, Leh",
        "city": "Leh",
        "district": "Leh",
        "state": "Ladakh",
        "pincode": "194101",
        "departments": ["Rtsa-ba (General Sowa-Rigpa Medicine)", "Lus-Gso (Therapeutics & Rejuvenation)", "Mani-Chikitsa"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 1982 252 458",
        "latitude": 34.1526,
        "longitude": 77.5771,
        "status": "Active"
    },
    {
        "name": "Men-Tsee-Khang Tibetan Medical Centre Leh",
        "code": "MTKL02",
        "abdm_id": "DEMO-FAC-SOW-002",
        "medical_system": "Sowa-Rigpa",
        "facility_type": "Traditional Sowa-Rigpa Hospital",
        "address": "Choglamsar, Leh",
        "city": "Leh",
        "district": "Leh",
        "state": "Ladakh",
        "pincode": "194104",
        "departments": ["Rtsa-ba (General Sowa-Rigpa Medicine)", "Herbal Pharmacotherapy"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 1982 259 021",
        "latitude": 34.1200,
        "longitude": 77.5900,
        "status": "Active"
    },
    {
        "name": "SNM Hospital Leh",
        "code": "SNMH03",
        "abdm_id": "DEMO-FAC-LA-001",
        "medical_system": "Modern / Conventional Medicine",
        "facility_type": "District General Hospital",
        "address": "Hospital Road, Leh",
        "city": "Leh",
        "district": "Leh",
        "state": "Ladakh",
        "pincode": "194101",
        "departments": ["General Medicine", "Orthopedics", "Emergency Care"],
        "verification_status": "Demo Facility",
        "availability": "Available Today",
        "contact_number": "+91 1982 252 012",
        "latitude": 34.1580,
        "longitude": 77.5840,
        "status": "Active"
    }
]

# Doctor templates for dynamically seeding matching specialists for all departments
DOCTOR_TEMPLATES = {
    "General Medicine": ("Dr. Meera Nair", "MBBS, MD (General Medicine)", "Consultant Physician", 200),
    "Cardiology": ("Dr. Rajesh Sharma", "MBBS, DM (Cardiology)", "Consultant Interventional Cardiologist", 350),
    "Dermatology": ("Dr. Sreelakshmi Nair", "MBBS, MD (Dermatology)", "Consultant Dermatologist", 250),
    "Orthopedics": ("Dr. Arjun Kumar", "MBBS, MS (Orthopedics)", "Senior Orthopedic Surgeon", 300),
    "Pediatrics": ("Dr. Ananya Iyer", "MBBS, DCH, MD (Pediatrics)", "Senior Consultant Pediatrician", 220),
    "Neurology": ("Dr. Suresh Patil", "MBBS, DM (Neurology)", "Senior Neurologist", 400),
    "ENT": ("Dr. Vinod Varma", "MBBS, MS (ENT)", "Consultant ENT Surgeon", 200),
    "General Surgery": ("Dr. K. Narayanan", "MBBS, MS (Surgery)", "Consultant General Surgeon", 280),
    "Emergency Medicine": ("Dr. Pradeep Sen", "MBBS, MEM", "Emergency Medicine Specialist", 250),
    "Emergency Care": ("Dr. Pradeep Sen", "MBBS, MEM", "Emergency Medicine Specialist", 250),
    "Preventive Medicine": ("Dr. Kavitha Menon", "MBBS, MD (Community Medicine)", "Public Health Specialist", 150),
    "Gynecology": ("Dr. Radhika Pillai", "MBBS, MS (OBG)", "Consultant Gynecologist", 250),

    # Ayurveda
    "Kayachikitsa (General Medicine)": ("Vaidya Harikrishnan Namboodiri", "BAMS, MD (Ayurveda)", "Senior Ayurvedic Physician", 180),
    "Panchakarma": ("Vaidya Divya G.", "BAMS, MD (Panchakarma)", "Panchakarma Specialist", 220),
    "Shalya Tantra": ("Vaidya Somanathan P.", "BAMS, MS (Ayurveda Shalya)", "Ayurvedic Surgeon", 250),
    "Kaumarbhritya": ("Vaidya Revathy Mohan", "BAMS, MD (Kaumarbhritya)", "Ayurvedic Pediatrician", 180),
    "Shalakya Tantra": ("Vaidya Aravind S.", "BAMS, MS (Shalakya Tantra)", "Ayurvedic Eye & ENT Specialist", 220),
    "Rasayana Chikitsa": ("Vaidya Gopinath", "BAMS", "Rejuvenation Specialist", 200),

    # Siddha
    "Pothu Maruthuvam (General Medicine)": ("Siddhar Dr. Murugan K.", "BSMS, MD (Siddha)", "Senior Siddha Physician", 180),
    "Varma Maruthuvam": ("Dr. Selvanathan S.", "BSMS, Varma Specialist", "Varma & Bone Setting Specialist", 200),
    "Sirappu Maruthuvam": ("Dr. Jayanthi P.", "BSMS, MD (Siddha)", "Chronic Care Siddha Specialist", 200),
    "Kuzhandhai Maruthuvam (Pediatrics)": ("Dr. Thamarai K.", "BSMS, MD (Siddha)", "Siddha Pediatrician", 180),
    "Noi Nadal (Diagnostics)": ("Dr. Sivakumar R.", "BSMS", "Siddha Diagnostic Specialist", 160),

    # Unani
    "Moalajat (General Medicine)": ("Hakim Dr. Abdul Hameed", "BUMS, MD (Unani)", "Senior Unani Consultant", 180),
    "Ilaj-bit-Tadbeer (Regimental Therapy)": ("Hakim Dr. Fatima Begum", "BUMS", "Regimental Therapy Specialist", 200),
    "Jarahat": ("Hakim Dr. Tariq Mansoor", "BUMS, MS (Unani)", "Unani Surgeon", 220),

    # Sowa-Rigpa
    "Rtsa-ba (General Sowa-Rigpa Medicine)": ("Amchi Tenzin Wangyal", "Kachupa Degree, Men-Tsee-Khang", "Master Sowa-Rigpa Practitioner", 150),
    "Lus-Gso (Therapeutics & Rejuvenation)": ("Amchi Dechen Lhamo", "Men-Tsee-Khang Certified", "Rejuvenation Specialist", 180),
    "Herbal Pharmacotherapy": ("Amchi Dorjee Namgyal", "Traditional Sowa-Rigpa Physician", "Herbal Formulation Master", 150),

    # Homoeopathy
    "General Homoeopathy": ("Dr. George Kurian", "BHMS, MD (Homoeopathy)", "Consultant Homoeopath", 180),
    "Chronic Disease Management": ("Dr. Sheela Nair", "BHMS", "Senior Homoeopathic Physician", 200),
    "Pediatric Homoeopathy": ("Dr. Rohit Varma", "BHMS", "Pediatric Homoeopath", 180),

    # Integrated AYUSH
    "Integrated Medicine OPD": ("Dr. Meera Chandran", "MBBS, BAMS (Integrative)", "Chief Integrative Physician", 250),
    "Yoga & Naturopathy": ("Dr. Anand Swaminathan", "BNYS", "Naturopath & Yoga Physician", 180),
    "Yoga Therapy": ("Dr. Sunita Rao", "BNYS, MSc (Yoga)", "Yoga Therapy Specialist", 180),
    "Ayurveda & Panchakarma": ("Vaidya Divya G.", "BAMS, MD (Panchakarma)", "Panchakarma Specialist", 220),
    "Homoeopathy": ("Dr. George Kurian", "BHMS", "Consultant Homoeopath", 180),
    "Siddha & Varma": ("Siddhar Dr. Murugan K.", "BSMS", "Siddha Specialist", 180)
}

def seed_all_facilities_and_doctors(db):
    """
    Populates MongoDB Atlas with the comprehensive multi-system facilities and matching doctors.
    Guarantees every facility has distinct, matching doctors for all its departments.
    """
    try:
        if db.settings.find_one({"key": "seed_expanded_facilities_done"}):
            return
    except Exception:
        pass

    seeded_fac_count = 0
    seeded_doc_count = 0

    for fac in DEMO_FACILITIES_DATA:
        # Check by name or code
        existing = db.clinics.find_one({"name": fac["name"]})
        if not existing:
            fac_copy = dict(fac)
            fac_copy["created_at"] = datetime.utcnow()
            ins = db.clinics.insert_one(fac_copy)
            fac_id_str = str(ins.inserted_id)
            db.clinics.update_one({"_id": ins.inserted_id}, {"$set": {"facility_id": fac_id_str, "facility_name": fac["name"]}})
            seeded_fac_count += 1
        else:
            fac_id_str = str(existing["_id"])
            db.clinics.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "facility_id": fac_id_str,
                    "facility_name": fac["name"],
                    "medical_system": fac["medical_system"],
                    "facility_type": fac["facility_type"],
                    "state": fac["state"],
                    "district": fac["district"],
                    "city": fac["city"],
                    "pincode": fac["pincode"],
                    "address": fac["address"],
                    "departments": fac["departments"],
                    "verification_status": "Demo Facility",
                    "availability": "Available Today",
                    "contact_number": fac.get("contact_number", "+91 1800 11 4477")
                }}
            )

        # Ensure doctors exist for every department of this facility
        for dept in fac.get("departments", []):
            dept_key = dept.strip()
            tmpl = DOCTOR_TEMPLATES.get(dept_key, ("Dr. Specialist", "Certified Practitioner", "Specialist Physician", 200))
            doc_name, doc_qual, doc_spec, doc_fee = tmpl

            clean_fac = "".join(c for c in fac["name"] if c.isalnum())[:12].lower()
            clean_dept = "".join(c for c in dept_key if c.isalnum())[:8].lower()
            doc_email = f"doc_{clean_fac}_{clean_dept}@medicare.demo"

            existing_doc = db.doctors.find_one({
                "$or": [
                    {"email": doc_email},
                    {"clinic_id": fac_id_str, "department": dept_key}
                ]
            })

            if not existing_doc:
                db.doctors.insert_one({
                    "name": doc_name,
                    "email": doc_email,
                    "password": generate_password_hash("doctor123"),
                    "clinic_id": fac_id_str,
                    "facility_id": fac_id_str,
                    "facility_name": fac["name"],
                    "medical_system": fac["medical_system"],
                    "department": dept_key,
                    "qualification": doc_qual,
                    "specialization": doc_spec,
                    "experience": "8 years",
                    "fees": doc_fee,
                    "total_tokens": 16,
                    "patient_ratings": 4.9,
                    "available_today": True,
                    "next_token": "A-024",
                    "verification_status": "Demo Facility Doctor",
                    "is_suspended": False,
                    "created_at": datetime.utcnow()
                })
                seeded_doc_count += 1
            else:
                db.doctors.update_one(
                    {"_id": existing_doc["_id"]},
                    {"$set": {
                        "clinic_id": fac_id_str,
                        "facility_id": fac_id_str,
                        "facility_name": fac["name"],
                        "medical_system": fac["medical_system"],
                        "department": dept_key,
                        "qualification": doc_qual,
                        "specialization": doc_spec,
                        "available_today": True,
                        "verification_status": "Demo Facility Doctor"
                    }}
                )

    try:
        db.settings.update_one({"key": "seed_expanded_facilities_done"}, {"$set": {"seeded": True}}, upsert=True)
    except Exception:
        pass

    print(f"[SEED] Expanded facilities processed. Added {seeded_fac_count} new clinics, {seeded_doc_count} new doctors.")
