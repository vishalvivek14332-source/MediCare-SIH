import unittest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database.db import mongo

class HospitalTokenWorkflowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_medical_systems(self):
        """1. GET /api/medical-systems returns exactly 8 systems with metadata."""
        res = self.client.get('/api/medical-systems')
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertTrue(json_data.get('success'))
        systems = json_data.get('data', [])
        self.assertEqual(len(systems), 8, f"Expected 8 medical systems, got {len(systems)}")
        names = [s['name'] for s in systems]
        self.assertIn("Modern / Conventional Medicine", names)
        self.assertIn("Ayurveda", names)
        self.assertIn("Homoeopathy", names)
        self.assertIn("Unani", names)
        self.assertIn("Siddha", names)
        self.assertIn("Sowa-Rigpa", names)
        self.assertIn("Yoga & Naturopathy", names)
        self.assertIn("Integrated AYUSH", names)

    def test_02_states(self):
        """2. GET /api/states returns 28 states + 8 UTs (36 total)."""
        res = self.client.get('/api/states')
        self.assertEqual(res.status_code, 200)
        states = res.get_json().get('data', [])
        self.assertEqual(len(states), 36, f"Expected 36 states and UTs, got {len(states)}")
        self.assertIn("Kerala", states)
        self.assertIn("Karnataka", states)
        self.assertIn("Tamil Nadu", states)
        self.assertIn("Delhi", states)
        self.assertIn("Ladakh", states)

    def test_03_districts(self):
        """3. GET /api/districts?state=Kerala returns Kerala districts."""
        res = self.client.get('/api/districts?state=Kerala')
        self.assertEqual(res.status_code, 200)
        districts = res.get_json().get('data', [])
        self.assertIn("Kannur", districts)
        self.assertIn("Kozhikode", districts)
        self.assertIn("Ernakulam", districts)

    def test_04_facilities_filtering(self):
        """4-8. GET /api/facilities with filters: medical_system, state, district, city."""
        # 5. Filter medical_system
        res_ayu = self.client.get('/api/facilities?medical_system=ayurveda')
        self.assertEqual(res_ayu.status_code, 200)
        ayu_facs = res_ayu.get_json().get('data', [])
        self.assertGreater(len(ayu_facs), 0)
        for f in ayu_facs:
            self.assertEqual(f['medical_system'], 'Ayurveda')

        # 6. Filter state
        res_state = self.client.get('/api/facilities?state=Kerala')
        self.assertEqual(res_state.status_code, 200)
        kerala_facs = res_state.get_json().get('data', [])
        for f in kerala_facs:
            self.assertEqual(f['state'], 'Kerala')

        # 7. Filter district
        res_dist = self.client.get('/api/facilities?state=Kerala&district=Kannur')
        self.assertEqual(res_dist.status_code, 200)
        kannur_facs = res_dist.get_json().get('data', [])
        for f in kannur_facs:
            self.assertEqual(f['district'], 'Kannur')

        # 8. Filter city
        res_city = self.client.get('/api/facilities?state=Kerala&district=Kannur&city=Thalassery')
        self.assertEqual(res_city.status_code, 200)

        # 9. Search keyword
        res_search = self.client.get('/api/facilities?search=District%20Hospital')
        self.assertEqual(res_search.status_code, 200)
        search_facs = res_search.get_json().get('data', [])
        self.assertGreater(len(search_facs), 0)

    def test_10_facility_departments(self):
        """10. GET /api/facilities/<id>/departments returns ONLY that facility's departments."""
        fac = mongo.db.clinics.find_one({"medical_system": "Ayurveda", "district": "Kannur"})
        self.assertIsNotNone(fac, "Ayurveda facility in Kannur should exist")
        fac_id = str(fac['_id'])

        res = self.client.get(f'/api/facilities/{fac_id}/departments')
        self.assertEqual(res.status_code, 200)
        depts = res.get_json().get('data', {}).get('departments', [])
        self.assertIn("Kayachikitsa", depts)
        self.assertIn("Panchakarma", depts)
        # Should not include allopathic cardiology in an ayurvedic center
        self.assertNotIn("Emergency Medicine", depts)

    def test_11_facility_department_doctors(self):
        """11. GET /api/facilities/<id>/departments/<dept>/doctors returns only matching doctors."""
        fac = mongo.db.clinics.find_one({"name": "Government Ayurveda Hospital Kannur"})
        self.assertIsNotNone(fac)
        fac_id = str(fac['_id'])

        res = self.client.get(f'/api/facilities/{fac_id}/departments/Kayachikitsa/doctors')
        self.assertEqual(res.status_code, 200)
        docs = res.get_json().get('data', [])
        self.assertGreater(len(docs), 0)
        for d in docs:
            self.assertEqual(d['department'], 'Kayachikitsa')

    def test_12_13_ai_complaint_and_questions(self):
        """12 & 13. AI complaint analysis generates exactly TWO questions."""
        res = self.client.post('/api/ai/analyze-complaint', json={
            'complaint': 'Severe knee joint pain and swelling for 4 days',
            'department': 'Kayachikitsa',
            'medical_system': 'Ayurveda'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json().get('data', {})
        self.assertIn('session_id', data)
        questions = data.get('questions', [])
        self.assertEqual(len(questions), 2, "AI must return exactly TWO follow-up questions")

    def test_14_15_ai_summary_triage_and_disclaimer(self):
        """14 & 15. AI summary produces validated triage priority and mandatory disclaimer."""
        res = self.client.post('/api/ai/generate-summary', json={
            'complaint': 'Severe knee joint pain and swelling for 4 days',
            'answers': {'q1': 'Severe (7 - 10)', 'q2': 'Gradually developed'},
            'medical_system': 'Ayurveda',
            'facility_name': 'Government Ayurveda Hospital Kannur',
            'department': 'Kayachikitsa',
            'doctor_name': 'Dr. Meera K. Warrier'
        })
        self.assertEqual(res.status_code, 200)
        summary = res.get_json().get('data', {})
        self.assertIn(summary.get('triage_priority'), ['Routine', 'Priority', 'Urgent', 'Emergency'])
        # Mandatory disclaimer check
        self.assertIn("clinician review required", summary.get('clinical_disclaimer', '').lower())
        self.assertIn("qualified healthcare professional", summary.get('clinical_disclaimer', '').lower())

    def test_16_to_22_booking_creation_and_persistence(self):
        """16-22. Booking persists priority, medical_system, facility, department, doctor, AI case."""
        doc = mongo.db.doctors.find_one({"name": "Dr. Meera K. Warrier"})
        self.assertIsNotNone(doc)
        fac = mongo.db.clinics.find_one({"name": "Government Ayurveda Hospital Kannur"})
        self.assertIsNotNone(fac)

        # Clean up any test appointment for this slot so test is idempotent
        mongo.db.appointments.delete_many({
            "doctor_id": doc['_id'],
            "date": '2026-09-30'
        })

        booking_payload = {
            'doctor_id': str(doc['_id']),
            'date': '2026-09-30',
            'slot': '10:00 AM - 10:15 AM',
            'priority': 'Priority',
            'medical_system': 'Ayurveda',
            'facility_id': str(fac['_id']),
            'facility_name': fac['name'],
            'department': 'Kayachikitsa',
            'ai_case_id': 'demo_session_123'
        }

        res = self.client.post('/api/booking/create', json=booking_payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json().get('data', {})
        self.assertIn('token_number', data)
        self.assertEqual(data.get('priority'), 'Priority')
        self.assertEqual(data.get('medical_system'), 'Ayurveda')
        self.assertEqual(data.get('department'), 'Kayachikitsa')

        # 23. Duplicate token slot booking for same doctor and date should be rejected (409)
        res_dup = self.client.post('/api/booking/create', json=booking_payload)
        self.assertEqual(res_dup.status_code, 409, "Duplicate slot booking must return 409 Conflict")

    def test_26_27_doctor_views(self):
        """26 & 27. Doctor queue and patient brief render with live records and disclaimers."""
        res_doc = self.client.get('/doctor')
        self.assertEqual(res_doc.status_code, 200)
        self.assertIn(b"Medical System", res_doc.data)
        self.assertIn(b"Chief Complaint", res_doc.data)

        res_brief = self.client.get('/doctor/patient-brief/A-026')
        self.assertEqual(res_brief.status_code, 200)
        self.assertIn(b"AI-assisted summary", res_brief.data)
        self.assertIn(b"clinician review required", res_brief.data)

if __name__ == '__main__':
    unittest.main()
