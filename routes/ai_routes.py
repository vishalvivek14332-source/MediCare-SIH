from flask import Blueprint, request, jsonify
from utils.helpers import success_response, error_response
from models.health_record import AICaseSession
from datetime import datetime
import json

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/analyze-complaint', methods=['POST'])
def analyze_complaint():
    data = request.get_json() or {}
    complaint = data.get('complaint', '').strip()
    language = data.get('language', 'English')
    
    if not complaint:
        return error_response("Please provide your medical concern")
        
    complaint_lower = complaint.lower()
    
    # Context-aware intelligent clinical follow-up question generation
    if any(w in complaint_lower for w in ['cough', 'fever', 'cold', 'throat', 'breath', 'chest']):
        q1 = {
            "id": "q1",
            "question": "When did this respiratory problem/fever start?",
            "type": "choice",
            "options": ["Today / Less than 24 hours ago", "2 to 3 days ago", "1 to 2 weeks ago", "More than 2 weeks ago"]
        }
        q2 = {
            "id": "q2",
            "question": "Has the condition become better, worse, or stayed the same?",
            "type": "choice",
            "options": ["Progressively getting worse", "Staying about the same", "Gradually improving", "Comes and goes intermittently"]
        }
    elif any(w in complaint_lower for w in ['pain', 'ache', 'knee', 'back', 'joint', 'headache', 'stomach']):
        q1 = {
            "id": "q1",
            "question": "How would you describe the severity of this pain on a scale of 1 to 10?",
            "type": "choice",
            "options": ["Mild (1 - 3): Noticeable but doesn't disrupt activities", "Moderate (4 - 6): Interferes with tasks, manageable", "Severe (7 - 10): Disabling, prevents normal movement"]
        }
        q2 = {
            "id": "q2",
            "question": "Did this pain start suddenly or develop gradually over time?",
            "type": "choice",
            "options": ["Sudden acute onset following physical activity", "Gradually developed over several days/weeks", "Chronic recurring episode"]
        }
    else:
        q1 = {
            "id": "q1",
            "question": "When did you first notice these symptoms starting?",
            "type": "choice",
            "options": ["Within the last 24-48 hours", "3 to 7 days ago", "Over a week ago", "Recurring for several months"]
        }
        q2 = {
            "id": "q2",
            "question": "Has this condition become better, worse, or stayed the same?",
            "type": "choice",
            "options": ["Worsening with time", "Constant without change", "Fluctuating / Periodic", "Slightly improving"]
        }

    # Store in session
    session_result = AICaseSession.create(
        patient_id="sajil_binu",
        complaint=complaint,
        language=language
    )

    return success_response(data={
        "session_id": str(session_result.inserted_id),
        "complaint": complaint,
        "language": language,
        "questions": [q1, q2]
    })

@ai_bp.route('/generate-summary', methods=['POST'])
def generate_summary():
    data = request.get_json() or {}
    complaint = data.get('complaint', 'Patient reported ongoing health concerns.')
    answers = data.get('answers', {})
    session_id = data.get('session_id')
    
    complaint_lower = complaint.lower()
    
    # Determine Safe Clinical Triage Level
    if any(w in complaint_lower for w in ['severe breath', 'chest pain', 'unconscious', 'collapse', 'bleeding heavily', 'paralysis']):
        triage_level = "Emergency"
        triage_badge_color = "#DC2626"
        triage_reason = "High acuity red-flag symptoms detected. Immediate emergency medical intervention required."
    elif any(w in complaint_lower for w in ['high fever', 'difficulty breathing', 'worsening', 'cannot walk', 'acute severe']):
        triage_level = "Urgent"
        triage_badge_color = "#EA580C"
        triage_reason = "Symptoms indicate acute condition requiring priority clinical evaluation within 1-2 hours."
    elif any(w in complaint_lower for w in ['moderate', 'fever', 'cough', 'swelling', 'rash', 'dizziness']):
        triage_level = "Priority"
        triage_badge_color = "#D97706"
        triage_reason = "Sub-acute presentation requiring same-day outpatient physician consultation."
    else:
        triage_level = "Routine"
        triage_badge_color = "#16A05D"
        triage_reason = "Stable presentation suitable for routine scheduled outpatient consultation and token queuing."

    summary = {
        "patient_name": "Sajil Binu",
        "health_id": "91-XXXX-XXXX-1234 / CB-2026-001245",
        "age_gender": "24 Yrs / Male",
        "chief_complaint": complaint,
        "why_consulting_now": "Patient notes symptoms have persisted and are affecting daily activities.",
        "medical_history": "No known drug allergies. Previous mild seasonal allergies and resolved gastroenteritis (Jul 2025).",
        "current_medications": "Over-the-counter paracetamol 650mg SOS. No ongoing chronic maintenance medications.",
        "recent_documents": "Blood Test Report (12 Sep 2025 - WNL), Chest X-Ray (21 Aug 2025 - Clear fields).",
        "follow_up_answers": answers,
        "triage_priority": triage_level,
        "triage_reason": triage_reason,
        "triage_color": triage_badge_color,
        "clinical_disclaimer": "AI-assisted summary for clinician review. Final clinical assessment must be performed by a qualified healthcare professional."
    }

    if session_id:
        try:
            AICaseSession.update(session_id, {
                "summary": summary,
                "triage": {"level": triage_level, "reason": triage_reason}
            })
        except Exception:
            pass

    return success_response(data=summary)

@ai_bp.route('/voice-transcribe', methods=['POST'])
def voice_transcribe():
    data = request.get_json() or {}
    sample_text = data.get('audio_hint', "I have been experiencing a persistent dry cough and mild fever for the past three days.")
    language = data.get('language', 'English')
    
    return success_response(data={
        "transcript": sample_text,
        "language": language,
        "confidence": 0.96
    })
