import os
from flask import Flask, render_template, redirect, make_response
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
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Initialize Extensions
    CORS(app)
    JWTManager(app)
    init_db(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Seed demo data and initialize MongoDB Atlas indexes
    with app.app_context():
        seed_database()
        init_indexes()

    def get_authenticated_user_from_request():
        auth_token = request.cookies.get('auth_token')
        if not auth_token and 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            if auth_header.startswith('Bearer '):
                auth_token = auth_header.split(' ', 1)[1]
                
        if auth_token:
            try:
                from flask_jwt_extended import decode_token
                import json
                decoded = decode_token(auth_token)
                identity = decoded.get('sub')
                data = json.loads(identity) if isinstance(identity, str) else identity
                return data
            except Exception:
                pass

        auth_role = request.cookies.get('auth_role')
        auth_name = request.cookies.get('auth_name')
        auth_pid = request.cookies.get('auth_patient_id')
        if auth_role:
            if auth_role == 'patient':
                patient = None
                if auth_pid:
                    try:
                        from bson.objectid import ObjectId
                        patient = mongo.db.patients.find_one({"_id": ObjectId(auth_pid)})
                    except Exception:
                        pass
                if not patient and auth_name:
                    patient = mongo.db.patients.find_one({"name": auth_name})
                if not patient:
                    patient = mongo.db.patients.find_one({"email": "sajilbinu@example.com"}) or mongo.db.patients.find_one()
                if patient:
                    p_hid = patient.get("health_id") or request.cookies.get('auth_health_id') or "CB-2026-001245"
                    if str(p_hid).startswith("91-"):
                        p_hid = "CB-2026-001245"
                    return {
                        "id": str(patient["_id"]),
                        "role": "patient",
                        "name": patient.get("name", auth_name or "Patient"),
                        "health_id": p_hid
                    }
            return {"role": auth_role, "name": auth_name or "User"}
        return None

    # Context processor to inject the authenticated user profile and navigation into every template
    @app.context_processor
    def inject_user():
        from utils.navigation import get_navigation_context
        user_info = get_authenticated_user_from_request()
        if not user_info:
            nav_ctx = get_navigation_context(is_authenticated=False)
            return {
                "is_authenticated": False,
                "current_user": None,
                **nav_ctx
            }

        role = user_info.get("role", "patient")
        user_id = user_info.get("id")

        db_user = None
        from bson.objectid import ObjectId
        if user_id:
            try:
                if role == 'patient':
                    db_user = mongo.db.patients.find_one({"_id": ObjectId(user_id)})
                elif role == 'doctor':
                    db_user = mongo.db.doctors.find_one({"_id": ObjectId(user_id)})
                elif role in ('clinic_admin', 'hospital', 'facility'):
                    db_user = mongo.db.clinics.find_one({"_id": ObjectId(user_id)})
                elif role in ('main_admin', 'admin'):
                    db_user = {"name": "Main Administrator", "role": "main_admin", "email": "admin@medicare.gov.in"}
            except Exception:
                pass

        if not db_user and user_info.get("email"):
            if role == 'patient':
                db_user = mongo.db.patients.find_one({"email": user_info["email"].lower()})
            elif role == 'doctor':
                db_user = mongo.db.doctors.find_one({"email": user_info["email"].lower()})
            elif role in ('clinic_admin', 'hospital', 'facility'):
                db_user = mongo.db.clinics.find_one({"email": user_info["email"].lower()})

        if not db_user:
            db_user = user_info

        name = db_user.get("name") or user_info.get("name") or "User"
        initial = (name.strip()[:1] or "U").upper()

        nav_ctx = get_navigation_context(is_authenticated=True, role=role)

        actual_hid = user_info.get("health_id") or db_user.get("health_id") or "CB-2026-001245"
        if str(actual_hid).startswith("91-") or not actual_hid:
            actual_hid = "CB-2026-001245"

        return {
            "is_authenticated": True,
            "current_user": {
                "id": str(db_user.get("_id", user_id or "")),
                "name": name,
                "initial": initial,
                "role": role,
                "email": db_user.get("email", ""),
                "phone": db_user.get("phone") or db_user.get("mobile", ""),
                "health_id": actual_hid,
                "abdm_id": db_user.get("abdm_id") or db_user.get("health_id", ""),
                "dob": db_user.get("dob") or db_user.get("date_of_birth", ""),
                "gender": db_user.get("gender", ""),
                "blood_group": db_user.get("blood_group", ""),
                "address": db_user.get("address", ""),
                "state": db_user.get("state", "Kerala"),
                "district": db_user.get("district", "Kannur"),
                "pincode": db_user.get("pincode", "")
            },
            **nav_ctx
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

    @app.route('/api/appointments', methods=['GET'])
    def api_appointments():
        from routes.booking_routes import my_appointments
        return my_appointments()

    # Frontend routes (serving templates)
    @app.route('/')
    def index():
        user = get_authenticated_user_from_request()
        if user and not request.args.get('public') and not request.args.get('home'):
            role = user.get('role')
            if role == 'patient':
                return redirect('/dashboard')
            elif role == 'doctor':
                return redirect('/doctor')
            elif role in ('clinic_admin', 'hospital', 'facility'):
                return redirect('/clinic_dashboard')
            elif role in ('main_admin', 'admin'):
                return redirect('/admin')
        return render_template('index.html', active_page='home')

    @app.route('/auth/test-session')
    def auth_test_session():
        from flask_jwt_extended import create_access_token
        import json
        role = request.args.get('role', 'patient')
        resp = redirect('/dashboard')
        patient = mongo.db.patients.find_one({"email": "sajilbinu@example.com"}) or mongo.db.patients.find_one()
        patient_id = str(patient["_id"]) if patient else "patient-demo-001"
        token = create_access_token(identity=json.dumps({
            "id": patient_id,
            "role": role,
            "name": "Sajil Binu",
            "email": "sajilbinu@example.com",
            "health_id": "CB-2026-001245"
        }))
        resp.set_cookie('auth_token', token, path='/')
        resp.set_cookie('auth_role', role, path='/')
        resp.set_cookie('auth_name', 'Sajil Binu', path='/')
        return resp

    @app.route('/dashboard')
    def patient_dashboard():
        user = get_authenticated_user_from_request()
        if not user:
            return redirect('/login')
        role = user.get('role')
        if role == 'doctor':
            return redirect('/doctor')
        elif role in ('clinic_admin', 'hospital', 'facility'):
            return redirect('/clinic_dashboard')
        elif role in ('main_admin', 'admin'):
            return redirect('/admin')
        return render_template('dashboard.html', active_page='dashboard')

    @app.route('/health-records')
    def health_records():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('health_records.html', active_page='health_records')

    @app.route('/upload-documents')
    def upload_documents():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('upload_documents.html', active_page='upload_documents')

    @app.route('/shared-records')
    def shared_records():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('shared_records.html', active_page='shared_records')

    @app.route('/linked-facilities')
    def linked_facilities():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('linked_facilities.html', active_page='linked_facilities')

    @app.route('/appointments')
    def appointments():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('appointments.html', active_page='appointments')

    @app.route('/profile')
    def profile():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('profile.html', active_page='profile')

    @app.route('/settings')
    def settings():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('settings.html', active_page='settings')

    @app.route('/ai-case-taking')
    def ai_case_taking():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('ai_case_taking.html', active_page='ai_case_taking')

    @app.route('/ai-case-taking/follow-up')
    def ai_follow_up():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('ai_follow_up.html', active_page='ai_case_taking')

    @app.route('/ai-case-taking/summary')
    def ai_summary():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('ai_summary.html', active_page='ai_case_taking')

    @app.route('/ai-case-taking/triage')
    def ai_triage():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('ai_triage.html', active_page='ai_case_taking')

    @app.route('/booking')
    @app.route('/book-token')
    @app.route('/clinic-token')
    def booking():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('booking.html', active_page='booking')

    @app.route('/queue')
    def queue():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('queue.html', active_page='queue')

    @app.route('/doctor')
    def doctor():
        user = get_authenticated_user_from_request()
        if not user:
            return redirect('/login?role=doctor')
        role = user.get('role')
        if role == 'patient':
            return "Forbidden: Patient cannot access Doctor console.", 403
        elif role in ('clinic_admin', 'hospital', 'facility'):
            return redirect('/clinic_dashboard')
        elif role in ('main_admin', 'admin'):
            return redirect('/admin')
        appointments = list(mongo.db.appointments.find({"status": {"$in": ["pending", "confirmed", "scheduled", "completed"]}}).sort([("created_at", -1)]).limit(12))
        for a in appointments:
            a['_id'] = str(a['_id'])
        return render_template('doctor.html', active_page='doctor', live_appointments=appointments)

    @app.route('/doctor/patient-brief/<patient_id>')
    def doctor_brief(patient_id):
        user = get_authenticated_user_from_request()
        if not user:
            return redirect('/login?role=doctor')
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

        patient_record = None
        if app_record and app_record.get('patient_id'):
            p_id = app_record['patient_id']
            try:
                patient_record = mongo.db.patients.find_one({"_id": ObjectId(p_id)})
            except Exception:
                patient_record = mongo.db.patients.find_one({"_id": p_id})
        if not patient_record:
            patient_record = user

        return render_template(
            'doctor_brief.html',
            patient_id=patient_id,
            active_page='doctor',
            appointment=app_record,
            brief_patient=patient_record,
            ai_session=ai_session
        )

    @app.route('/health-timeline')
    def health_timeline():
        if not get_authenticated_user_from_request():
            return redirect('/login')
        return render_template('timeline.html', active_page='health_records')

    @app.route('/health-id')
    def health_id():
        user = get_authenticated_user_from_request() or {}
        import json
        from bson.objectid import ObjectId
        patient = None
        if user.get('role') == 'patient':
            if user.get('id'):
                try:
                    patient = mongo.db.patients.find_one({"_id": ObjectId(user['id'])})
                except Exception:
                    pass
            if not patient and user.get('email'):
                patient = mongo.db.patients.find_one({"email": user['email'].lower()})

        if not patient:
            # Fall back to default patient Sajil Binu so Health ID card renders seamlessly
            patient = mongo.db.patients.find_one({"name": "Sajil Binu"}) or mongo.db.patients.find_one({}) or {
                "name": "Sajil Binu",
                "health_id": "CB-2026-001245@abdm",
                "abdm_id": "91-2026-4589-1234",
                "dob": "12 Mar 2002",
                "gender": "Male",
                "blood_group": "O+",
                "phone": "+91 98765 43210",
                "state": "Kerala"
            }
        
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
        user = get_authenticated_user_from_request()
        if user and not request.args.get('demo'):
            role = user.get('role')
            if role == 'doctor':
                return redirect('/doctor')
            elif role in ('clinic_admin', 'hospital', 'facility'):
                return redirect('/clinic_dashboard')
            elif role in ('main_admin', 'admin'):
                return redirect('/admin')
            return redirect('/dashboard')

        if request.args.get('demo'):
            import json
            patient = mongo.db.patients.find_one({"email": "sajilbinu@example.com"}) or mongo.db.patients.find_one()
            if patient:
                from flask_jwt_extended import create_access_token
                token = create_access_token(identity=json.dumps({
                    "id": str(patient['_id']),
                    "role": "patient",
                    "name": patient.get('name', 'Sajil Binu'),
                    "health_id": patient.get('health_id')
                }))
                resp = make_response(redirect('/dashboard'))
                resp.set_cookie('auth_token', token, max_age=86400 * 7, path='/', httponly=False, samesite='Lax')
                resp.set_cookie('auth_role', 'patient', max_age=86400 * 7, path='/', httponly=False, samesite='Lax')
                resp.set_cookie('auth_name', patient.get('name', 'Sajil Binu'), max_age=86400 * 7, path='/', httponly=False, samesite='Lax')
                return resp
        return render_template('login.html')

    @app.route('/signup')
    @app.route('/register')
    def register():
        user = get_authenticated_user_from_request()
        if user:
            role = user.get('role')
            if role == 'doctor':
                return redirect('/doctor')
            elif role in ('clinic_admin', 'hospital', 'facility'):
                return redirect('/clinic_dashboard')
            elif role in ('main_admin', 'admin'):
                return redirect('/admin')
            return redirect('/dashboard')
        return render_template('register.html')

    @app.route('/admin')
    def admin():
        user = get_authenticated_user_from_request()
        if not user:
            return redirect('/login?role=main_admin')
        role = user.get('role')
        if role == 'patient':
            return "Forbidden: Patient cannot access Main Admin console.", 403
        elif role == 'doctor':
            return "Forbidden: Doctor cannot access Main Admin console.", 403
        elif role in ('clinic_admin', 'hospital', 'facility'):
            return "Forbidden: Hospital cannot access Main Admin console.", 403
        return render_template('admin.html', active_page='admin')

    @app.route('/clinic_dashboard')
    @app.route('/hospital')
    def clinic_dashboard():
        user = get_authenticated_user_from_request()
        if not user:
            return redirect('/login?role=hospital')
        role = user.get('role')
        if role == 'patient':
            return "Forbidden: Patient cannot access Hospital management console.", 403
        elif role == 'doctor':
            return redirect('/doctor')
        elif role in ('main_admin', 'admin'):
            return redirect('/admin')
        return render_template('clinic_dashboard.html', active_page='clinic_dashboard')

    @app.route('/logout')
    def logout():
        resp = make_response(redirect('/login'))
        resp.delete_cookie('auth_token', path='/')
        resp.delete_cookie('auth_role', path='/')
        resp.delete_cookie('auth_name', path='/')
        resp.delete_cookie('auth_patient_id', path='/')
        resp.delete_cookie('auth_health_id', path='/')
        return resp

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode, use_reloader=False, allow_unsafe_werkzeug=True)

