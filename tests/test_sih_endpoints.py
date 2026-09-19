import unittest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

class SIHEndpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_frontend_routes_render(self):
        routes = [
            '/',
            '/dashboard',
            '/health-records',
            '/upload-documents',
            '/shared-records',
            '/linked-facilities',
            '/appointments',
            '/profile',
            '/settings',
            '/ai-case-taking',
            '/ai-case-taking/follow-up',
            '/ai-case-taking/summary',
            '/ai-case-taking/triage',
            '/booking',
            '/queue',
            '/doctor',
            '/doctor/patient-brief/A-026',
            '/health-timeline',
            '/health-id'
        ]
        for r in routes:
            response = self.client.get(r)
            self.assertEqual(response.status_code, 200, f"Route {r} failed to render")

    def test_patient_apis(self):
        # Health records API
        res = self.client.get('/api/patient/health-records')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))
        self.assertIn('records', data['data'])

        # Facilities API
        res2 = self.client.get('/api/patient/facilities')
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)
        self.assertTrue(data2.get('success'))

        # Shared records API
        res3 = self.client.get('/api/patient/shared-records')
        self.assertEqual(res3.status_code, 200)
        data3 = json.loads(res3.data)
        self.assertTrue(data3.get('success'))

    def test_ai_apis(self):
        # AI complaint analysis
        res = self.client.post('/api/ai/analyze-complaint', json={
            'complaint': 'I have had a dry cough and mild fever for 3 days',
            'language': 'English'
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))
        self.assertEqual(len(data['data']['questions']), 2)

        # AI summary & triage
        res2 = self.client.post('/api/ai/generate-summary', json={
            'complaint': 'I have had a dry cough and mild fever for 3 days',
            'answers': {'Onset': '2 to 3 days ago', 'Progression': 'Getting worse'}
        })
        self.assertEqual(res2.status_code, 200)
        data2 = json.loads(res2.data)
        self.assertTrue(data2.get('success'))
        self.assertIn(data2['data']['triage_priority'], ['Routine', 'Priority', 'Urgent', 'Emergency'])

    def test_booking_doctor_apis(self):
        res = self.client.get('/api/booking/doctors')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))

if __name__ == '__main__':
    unittest.main()
