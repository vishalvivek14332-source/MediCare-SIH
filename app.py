import os
from flask import Flask, render_template, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database.db import init_db
from database.db import init_db
from extensions import socketio

# Import routes
from routes.auth_routes import auth_bp
from routes.booking_routes import booking_bp
from routes.admin_routes import admin_bp
from routes.doctor_routes import doctor_bp
from routes.patient_routes import patient_bp
from routes.ai_routes import ai_bp
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
        return render_template('doctor.html', active_page='doctor')

    @app.route('/doctor/patient-brief/<patient_id>')
    def doctor_brief(patient_id):
        return render_template('doctor_brief.html', patient_id=patient_id, active_page='doctor')

    @app.route('/health-timeline')
    def health_timeline():
        return render_template('timeline.html', active_page='health_records')

    @app.route('/health-id')
    def health_id():
        return render_template('health_id.html', active_page='health_id')

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
    socketio.run(app, host='0.0.0.0', port=port, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

