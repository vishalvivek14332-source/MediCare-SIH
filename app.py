import os
from flask import Flask, render_template, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database.db import init_db, mongo
from extensions import socketio
from utils.qr_generator import get_patient_qr_payload, generate_qr_svg, generate_qr_data_url

# Import routes
from routes.auth_routes import auth_bp
from routes.booking_routes import booking_bp
from routes.admin_routes import admin_bp
from routes.doctor_routes import doctor_bp
from routes.patient_routes import patient_bp
from routes.ai_routes import ai_bp, voice_transcribe
from routes.facility_routes import facility_bp
from database.indexes import init_indexes
from utils.seed_data import seed_database
import gzip
from flask import request

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    CORS(app)
    JWTManager(app)
    init_db(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Seed demo data and initialize MongoDB Atlas indexes
    with app.app_context():
        seed_database()
        init_indexes()

    # Context processor to inject the authenticated user profile into every template
    @app.context_processor
    def inject_user():
        patient = mongo.db.patients.find_one({"email": "sajilbinu@example.com"}) or mongo.db.patients.find_one({}) or {}
        name = patient.get("name", "Sajil Binu")
        initial = (name.strip()[:1] or "S").upper()
        return {
            "current_user": {
                "id": str(patient.get("_id", "")),
                "name": name,
                "initial": initial,
                "email": patient.get("email", "sajilbinu@example.com"),
                "phone": patient.get("phone", "+91 98765 43210"),
                "health_id": patient.get("health_id", "91-XXXX-XXXX-1234"),
                "abdm_id": patient.get("abdm_id", "CB-2026-001245"),
                "dob": patient.get("dob", "12 Mar 2002"),
                "gender": patient.get("gender", "Male"),
                "blood_group": patient.get("blood_group", "O+"),
                "address": patient.get("address", "Panoor, Kannur, Kerala, 670692"),
                "occupation": patient.get("occupation", "Student"),
                "emergency_contact": patient.get("emergency_contact", "Biju Mathew (Father) +91 98987 65432"),
                "state": patient.get("state", "Kerala"),
                "district": patient.get("district", "Kannur"),
                "pincode": patient.get("pincode", "670692")
            }
        }

    # Performance optimization middleware: Gzip compression & Static caching
    @app.after_request
    def optimize_response(response):
        if request.path.startswith('/static/'):
            response.headers['Cache-Control'] = 'public, max-age=86400'
            
        accept_encoding = request.headers.get('Accept-Encoding', '')
        if 'gzip' in accept_encoding.lower() and response.status_code < 300 and not response.headers.get('Content-Encoding'):
            content_type = response.headers.get('Content-Type', '')
            if any(t in content_type for t in ['text/', 'application/json', 'image/svg+xml']):
                try:
                    data = response.get_data()
                    if len(data) > 500:
                        compressed = gzip.compress(data, compresslevel=6)
                        response.set_data(compressed)
                        response.headers['Content-Encoding'] = 'gzip'
                        response.headers['Content-Length'] = len(compressed)
                except Exception:
                    pass
        return response

    # Register Blueprints for API
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(booking_bp, url_prefix='/api/booking')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(facility_bp, url_prefix='/api')

    @app.route('/api/voice/transcribe', methods=['POST'])
    def voice_transcribe_alias():
        return voice_transcribe()

    # Frontend routes (serving templates)
    @app.route('/')
    @app.route('/dashboard')
    def index():
        return render_template('dashboard.html', active_page='dashboard')

    @app.route('/health-records')
    def health_records():
        return render_template('health_records.html', active_page='health_records')

    @app.route('/upload-documents')
    def upload_documents():
        return render_template('upload_documents.html', active_page='upload_documents')

    @app.route('/shared-records')
    def shared_records():
        return render_template('shared_records.html', active_page='shared_records')

    @app.route('/linked-facilities')
    def linked_facilities():
        return render_template('linked_facilities.html', active_page='linked_facilities')

    @app.route('/appointments')
    def appointments():
        return render_template('appointments.html', active_page='appointments')

    @app.route('/profile')
    def profile():
        return render_template('profile.html', active_page='profile')

    @app.route('/settings')
    def settings():
        return render_template('settings.html', active_page='settings')

    @app.route('/ai-case-taking')
    def ai_case_taking():
        return render_template('ai_case_taking.html', active_page='ai_case_taking')

    @app.route('/ai-case-taking/follow-up')
    def ai_follow_up():
        return render_template('ai_follow_up.html', active_page='ai_case_taking')

    @app.route('/ai-case-taking/summary')
    def ai_summary():
        return render_template('ai_summary.html', active_page='ai_case_taking')

    @app.route('/ai-case-taking/triage')
    def ai_triage():
        return render_template('ai_triage.html', active_page='ai_case_taking')

    @app.route('/booking')
    @app.route('/book-token')
    def booking():
        return render_template('booking.html', active_page='booking')

    @app.route('/queue')
    def queue():
        return render_template('queue.html', active_page='queue')

    @app.route('/doctor')
    def doctor():
        from bson.objectid import ObjectId
        appointments = list(mongo.db.appointments.find({"status": {"$in": ["pending", "confirmed", "scheduled", "completed"]}}).sort([("created_at", -1)]).limit(12))
        for a in appointments:
            a['_id'] = str(a['_id'])
        return render_template('doctor.html', active_page='doctor', live_appointments=appointments)

    @app.route('/doctor/patient-brief/<patient_id>')
    def doctor_brief(patient_id):
        from bson.objectid import ObjectId
        # Find matching appointment by token number or id
        app_record = mongo.db.appointments.find_one({"token_number": patient_id})
        if not app_record and len(patient_id) == 24:
            try:
                app_record = mongo.db.appointments.find_one({"_id": ObjectId(patient_id)})
            except Exception:
                pass

        ai_session = None
        if app_record and app_record.get('ai_case_id'):
            try:
                ai_session = mongo.db.ai_case_sessions.find_one({"_id": ObjectId(app_record['ai_case_id'])})
            except Exception:
                pass
        if not ai_session:
            ai_session = mongo.db.ai_case_sessions.find_one(sort=[("created_at", -1)])

        return render_template(
            'doctor_brief.html',
            patient_id=patient_id,
            active_page='doctor',
            appointment=app_record,
            ai_session=ai_session
        )

    @app.route('/health-timeline')
    def health_timeline():
        return render_template('timeline.html', active_page='health_records')

    @app.route('/health-id')
    def health_id():
        import json
        patient = mongo.db.patients.find_one({"email": "sajilbinu@example.com"})
        if not patient:
            patient = mongo.db.patients.find_one({}) or {}
        
        payload = get_patient_qr_payload(patient)
        qr_svg = generate_qr_svg(payload)
        qr_data_url = generate_qr_data_url(payload)
        return render_template(
            'health_id.html',
            active_page='health_id',
            patient=patient,
            qr_svg=qr_svg,
            qr_data_url=qr_data_url,
            qr_payload=payload,
            qr_payload_json=json.dumps(payload, indent=2)
        )

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/admin')
    def admin():
        return render_template('admin.html')

    @app.route('/clinic_dashboard')
    def clinic_dashboard():
        return render_template('clinic_dashboard.html')

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode, use_reloader=False, allow_unsafe_werkzeug=True)

