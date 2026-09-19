from flask import Blueprint, request, jsonify
from utils.helpers import success_response, error_response
from models.health_record import AICaseSession
from database.db import mongo
from datetime import datetime
import json

ai_bp = Blueprint('ai', __name__)

def generate_two_clinical_questions(complaint, medical_system="Modern Medicine", department="General Medicine"):
    """
    Generates exactly TWO context-aware clinical follow-up questions
    based on the chief complaint and selected clinical discipline.
    """
    complaint_lower = complaint.lower() if complaint else ""
    dept_lower = department.lower() if department else ""

    if any(w in complaint_lower for w in ['cough', 'fever', 'cold', 'throat', 'breath', 'chest', 'sneeze', 'phlegm']):
        q1 = {
            "id": "q1",
            "question": "When did this respiratory issue or fever first begin?",
            "type": "choice",
            "options": [
                "Today / Less than 24 hours ago",
                "2 to 3 days ago",
                "1 to 2 weeks ago",
                "More than 2 weeks ago (persistent)"
            ]
        }
        q2 = {
            "id": "q2",
            "question": "Has the condition become better, worse, or stayed about the same?",
            "type": "choice",
            "options": [
                "Progressively getting worse",
                "Staying about the same",
                "Gradually improving",
                "Comes and goes intermittently"
            ]
        }
    elif any(w in complaint_lower for w in ['pain', 'ache', 'knee', 'back', 'joint', 'headache', 'stomach', 'spine', 'muscle']) or any(w in dept_lower for w in ['ortho', 'kayachikitsa', 'panchakarma', 'surgery']):
        q1 = {
            "id": "q1",
            "question": "How would you describe the severity of this pain on a scale of 1 to 10?",
            "type": "choice",
            "options": [
                "Mild (1 - 3): Noticeable but does not restrict normal daily tasks",
                "Moderate (4 - 6): Interferes with tasks, manageable with rest",
                "Severe (7 - 10): Disabling, prevents normal movement and sleep"
            ]
        }
        q2 = {
            "id": "q2",
            "question": "Did this pain start suddenly following an incident or develop gradually?",
            "type": "choice",
            "options": [
                "Sudden acute onset following physical activity or strain",
                "Gradually developed over several days or weeks",
                "Chronic recurring episode over several months"
            ]
        }
    elif any(w in complaint_lower for w in ['skin', 'rash', 'itch', 'allergy', 'redness', 'eczema']) or 'derma' in dept_lower:
        q1 = {
            "id": "q1",
            "question": "Is the skin issue accompanied by severe itching, burning, or spreading?",
            "type": "choice",
            "options": [
                "Moderate to severe itching, spreading across new areas",
                "Mild itching, localised to one area",
                "No itching, primarily redness or discoloration",
                "Painful or burning sensation"
            ]
        }
        q2 = {
            "id": "q2",
            "question": "Have you recently used any new soap, cosmetics, medication, or food?",
            "type": "choice",
            "options": [
                "Yes, noticed symptoms right after using a new product/food",
                "No known new exposures or changes",
                "Seasonal flare-up that recurs annually"
            ]
        }
    elif any(w in complaint_lower for w in ['stress', 'sleep', 'anxiety', 'fatigue', 'tired', 'digestion', 'gas']) or any(w in dept_lower for w in ['yoga', 'naturopathy', 'swasthavritta', 'unani']):
        q1 = {
            "id": "q1",
            "question": "How significantly are these symptoms impacting your sleep and daily routine?",
            "type": "choice",
            "options": [
                "Substantial disruption to sleep and daily energy levels",
                "Moderate impact, managing with effort",
                "Mild impact during specific times of day"
            ]
        }
        q2 = {
            "id": "q2",
            "question": "How long have you been experiencing this fatigue, stress, or digestive discomfort?",
            "type": "choice",
            "options": [
                "Recent onset (last few days to 1 week)",
                "Between 2 to 4 weeks",
                "Ongoing for more than a month"
            ]
        }
    else:
        q1 = {
            "id": "q1",
            "question": "When did you first notice these symptoms starting?",
            "type": "choice",
            "options": [
                "Within the last 24 to 48 hours",
                "3 to 7 days ago",
                "Over 1 to 2 weeks ago",
                "Recurring periodically for several months"
            ]
        }
        q2 = {
            "id": "q2",
            "question": "Has this condition become better, worse, or stayed the same?",
            "type": "choice",
            "options": [
                "Progressively getting worse with time",
                "Constant without noticeable change",
                "Fluctuating / Periodic flare-ups",
                "Slightly improving"
            ]
        }

    return [q1, q2]


@ai_bp.route('/analyze-complaint', methods=['POST'])
def analyze_complaint():
    """
    Analyzes the chief complaint and generates exactly TWO context-aware questions.
    Reuses existing AI session storage.
    """
    data = request.get_json() or {}
    complaint = data.get('complaint', '').strip()
    language = data.get('language', 'English')
    medical_system = data.get('medical_system', 'Modern / Conventional Medicine')
    facility_name = data.get('facility_name', '')
    department = data.get('department', 'General Medicine')
    doctor_name = data.get('doctor_name', '')
    why_consulting_now = data.get('why_consulting_now', '')

    if not complaint:
        return error_response("Please provide your medical concern")

    questions = generate_two_clinical_questions(complaint, medical_system, department)

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
        "medical_system": medical_system,
        "department": department,
        "questions": questions
    })


@ai_bp.route('/follow-up-questions', methods=['POST'])
def follow_up_questions():
    """Returns exactly two context-aware questions for a complaint."""
    data = request.get_json() or {}
    complaint = data.get('complaint', '')
    department = data.get('department', 'General Medicine')
    medical_system = data.get('medical_system', 'Modern / Conventional Medicine')

    questions = generate_two_clinical_questions(complaint, medical_system, department)
    return success_response(data={"questions": questions})


@ai_bp.route('/generate-summary', methods=['POST'])
def generate_summary():
    """
    Generates an AI-assisted clinical summary and preliminary triage priority.
    Includes mandatory clinical safety disclaimers.
    """
    data = request.get_json() or {}
    complaint = data.get('complaint', 'Patient reported ongoing health concerns.').strip()
    why_consulting_now = data.get('why_consulting_now', '').strip()
    answers = data.get('answers', {})
    session_id = data.get('session_id')
    medical_system = data.get('medical_system', 'Modern / Conventional Medicine')
    facility_name = data.get('facility_name', 'Healthcare Facility')
    department = data.get('department', 'General Medicine')
    doctor_name = data.get('doctor_name', 'Attending Physician')

    complaint_lower = complaint.lower()
    answers_text = " ".join([str(v) for v in answers.values()]).lower() if isinstance(answers, dict) else ""

    # Determine Preliminary Safe Clinical Triage Level (Validated server-side)
    if any(w in complaint_lower for w in ['severe breath', 'chest pain', 'unconscious', 'collapse', 'bleeding heavily', 'paralysis', 'stroke', 'cardiac']):
        triage_level = "Emergency"
        triage_badge_color = "#DC2626"
        triage_reason = "High-acuity red-flag symptoms detected. Immediate emergency medical intervention required."
    elif any(w in complaint_lower or w in answers_text for w in ['high fever', 'difficulty breathing', 'worsening', 'cannot walk', 'acute severe', 'severe (7 - 10)']):
        triage_level = "Urgent"
        triage_badge_color = "#EA580C"
        triage_reason = "Acute clinical presentation requiring priority outpatient evaluation within 1 to 2 hours."
    elif any(w in complaint_lower or w in answers_text for w in ['moderate', 'fever', 'cough', 'swelling', 'rash', 'dizziness', 'moderate (4 - 6)']):
        triage_level = "Priority"
        triage_badge_color = "#D97706"
        triage_reason = "Sub-acute presentation suitable for same-day scheduled consultation."
    else:
        triage_level = "Routine"
        triage_badge_color = "#16A05D"
        triage_reason = "Stable presentation suitable for standard outpatient consultation and token queuing."

    if not why_consulting_now:
        why_consulting_now = "Symptoms have persisted and are impacting daily routine; patient seeks specialist clinical evaluation."

    summary = {
        "patient_name": "Sajil Binu",
        "health_id": "91-XXXX-XXXX-1234 / CB-2026-001245",
        "age_gender": "24 Yrs / Male",
        "medical_system": medical_system,
        "facility_name": facility_name,
        "department": department,
        "doctor_name": doctor_name,
        "chief_complaint": complaint,
        "why_consulting_now": why_consulting_now,
        "follow_up_answers": answers,
        "medical_history": "No known drug allergies (NKDA). Mild seasonal rhinitis; resolved gastroenteritis (Jul 2025).",
        "current_medications": "Paracetamol 650mg SOS as reported by patient. No chronic immunosuppressive or maintenance therapy.",
        "recent_documents": "Blood Test Report (12 Sep 2025 - CBC WNL), Chest X-Ray (21 Aug 2025 - Clear lung fields).",
        "triage_priority": triage_level,
        "triage_reason": triage_reason,
        "triage_color": triage_badge_color,
        "clinical_disclaimer": "AI-assisted case summary — clinician review required. Final clinical assessment must be performed by a qualified healthcare professional.",
        "triage_disclaimer": "Preliminary triage recommendation — Final clinical assessment must be performed by a qualified healthcare professional."
    }

    if session_id:
        try:
            AICaseSession.update(session_id, {
                "medical_system": medical_system,
                "facility_name": facility_name,
                "department": department,
                "doctor_name": doctor_name,
                "why_consulting_now": why_consulting_now,
                "summary": summary,
                "triage": {"level": triage_level, "reason": triage_reason}
            })
        except Exception:
            pass

    return success_response(data=summary)


@ai_bp.route('/voice-transcribe', methods=['POST'])
def voice_transcribe():
    """Simulates speech-to-text transcription with fallback and language support."""
    data = request.get_json() or {}
    language = data.get('language', 'English')
    audio_hint = data.get('audio_hint', '')

    sample_transcripts = {
        "English": "I have been experiencing a persistent dry cough and mild fever for the past three days.",
        "Malayalam": "കഴിഞ്ഞ 3 ദിവസമായി എനിക്ക് ചുമയും നേരിയ പനിയും അനുഭവപ്പെടുന്നുണ്ട്.",
        "Hindi": "मुझे पिछले तीन दिनों से लगातार सूखी खांसी और हल्का बुखार महसूस हो रहा है।"
    }

    text = audio_hint or sample_transcripts.get(language, sample_transcripts["English"])

    return success_response(data={
        "transcript": text,
        "language": language,
        "confidence": 0.96
    })
