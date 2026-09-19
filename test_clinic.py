import requests

payload = {
    "name": "",
    "code": "",
    "contact_number": "",
    "email": "",
    "password": "",
    "address": "",
    "city": "chittarikkal",
    "state": "Kerala",
    "latitude": "12.3213171",
    "longitude": "75.3590275",
    "booking_enabled": True,
    "queue_enabled": True,
    "emergency_support": True
}

try:
    # Get token first
    res = requests.post('http://127.0.0.1:5000/api/auth/login', json={"email": "admin@network.com", "password": "admin123", "role": "main_admin"})
    token = res.json().get('data', {}).get('access_token')

    if not token:
        print("Login failed:", res.json())
    else:
        headers = {"Authorization": f"Bearer {token}"}
        res2 = requests.post('http://127.0.0.1:5000/api/admin/clinics', json=payload, headers=headers)
        print("Status:", res2.status_code)
        print("Response:", res2.text)
except Exception as e:
    print(f"Error connecting to server: {e}")
