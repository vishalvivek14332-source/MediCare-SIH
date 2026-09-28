from flask import Blueprint, request, jsonify
from utils.helpers import success_response, error_response
from models.health_record import AICaseSession
from database.db import mongo
from datetime import datetime
import json

ai_bp = Blueprint('ai', __name__)

def generate_two_clinical_questions(complaint, medical_system="Modern Medicine", department="General Medicine", language="English"):
    """
    Generates exactly TWO context-aware clinical follow-up questions
    based on the chief complaint, selected clinical discipline, and patient language (English, Malayalam, Hindi).
    """
    complaint_lower = complaint.lower() if complaint else ""
    dept_lower = department.lower() if department else ""

    lang_str = str(language or "English").lower()
    if 'malayalam' in lang_str or lang_str == 'ml':
        lang = 'ml'
    elif 'hindi' in lang_str or lang_str == 'hi':
        lang = 'hi'
    else:
        lang = 'en'

    # Check category
    is_respiratory = any(w in complaint_lower for w in ['cough', 'fever', 'cold', 'throat', 'breath', 'chest', 'sneeze', 'phlegm', 'ചുമ', 'പനി', 'ശ്വാസം', 'തൊണ്ട', 'खांसी', 'बुखार', 'गले', 'सांस'])
    is_pain = any(w in complaint_lower for w in ['pain', 'ache', 'knee', 'back', 'joint', 'headache', 'stomach', 'spine', 'muscle', 'വേദന', 'മുട്ട്', 'തലവേദന', 'വയറുവേദന', 'दर्द', 'पीठ', 'सिरदर्द', 'घुटने']) or any(w in dept_lower for w in ['ortho', 'kayachikitsa', 'panchakarma', 'surgery'])
    is_skin = any(w in complaint_lower for w in ['skin', 'rash', 'itch', 'allergy', 'redness', 'eczema', 'ത്വക്ക്', 'ചൊറിച്ചിൽ', 'അലർജി', 'त्वचा', 'खुजली', 'एलर्जी']) or 'derma' in dept_lower
    is_lifestyle = any(w in complaint_lower for w in ['stress', 'sleep', 'anxiety', 'fatigue', 'tired', 'digestion', 'gas', 'ക്ഷീണം', 'ഉറക്കം', 'തളർച്ച', 'थकान', 'नींद', 'तनाव']) or any(w in dept_lower for w in ['yoga', 'naturopathy', 'swasthavritta', 'unani'])

    if is_respiratory:
        category = "respiratory"
    elif is_pain:
        category = "pain"
    elif is_skin:
        category = "skin"
    elif is_lifestyle:
        category = "lifestyle"
    else:
        category = "general"

    # Multilingual question definitions
    QUESTIONS_DB = {
        "respiratory": {
            "en": {
                "q1": ("When did this respiratory issue or fever first begin?", [
                    "Today / Less than 24 hours ago",
                    "2 to 3 days ago",
                    "1 to 2 weeks ago",
                    "More than 2 weeks ago (persistent)"
                ]),
                "q2": ("Has the condition become better, worse, or stayed about the same?", [
                    "Progressively getting worse",
                    "Staying about the same",
                    "Gradually improving",
                    "Comes and goes intermittently"
                ])
            },
            "ml": {
                "q1": ("ഈ ശ്വാസകോശ സംബന്ധമായ പ്രശ്നമോ പനിയോ എപ്പോഴാണ് ആരംഭിച്ചത്?", [
                    "ഇന്ന് / 24 മണിക്കൂറിനുള്ളിൽ",
                    "2 മുതൽ 3 ദിവസം മുൻപ്",
                    "1 മുതൽ 2 ആഴ്ച മുൻപ്",
                    "2 ആഴ്ചയിൽ കൂടുതൽ (തുടർച്ചയായി)"
                ]),
                "q2": ("ലക്ഷണങ്ങൾ മെച്ചപ്പെട്ടോ, മോശമായോ, അതോ മാറ്റമില്ലാതെ തുടരുകയാണോ?", [
                    "കൂടുതൽ മോശമായിക്കൊണ്ടിരിക്കുന്നു",
                    "മാറ്റമില്ലാതെ തുടരുന്നു",
                    "പതുക്കെ മെച്ചപ്പെടുന്നുണ്ട്",
                    "ഇടവിട്ട് വന്നുപോകുന്നു"
                ])
            },
            "hi": {
                "q1": ("यह सांस की समस्या या बुखार सबसे पहले कब शुरू हुआ था?", [
                    "आज / 24 घंटे से कम समय पहले",
                    "2 से 3 दिन पहले",
                    "1 से 2 सप्ताह पहले",
                    "2 सप्ताह से अधिक समय से (लगातार)"
                ]),
                "q2": ("क्या स्थिति बेहतर हुई है, बिगड़ी है या लगभग वैसी ही है?", [
                    "लगातार बिगड़ रही है",
                    "लगभग वैसी ही बनी हुई है",
                    "धीरे-धीरे सुधार हो रहा है",
                    "रुक-रुक कर होती है"
                ])
            }
        },
        "pain": {
            "en": {
                "q1": ("How would you describe the severity of this pain on a scale of 1 to 10?", [
                    "Mild (1 - 3): Noticeable but does not restrict normal daily tasks",
                    "Moderate (4 - 6): Interferes with tasks, manageable with rest",
                    "Severe (7 - 10): Disabling, prevents normal movement and sleep"
                ]),
                "q2": ("Did this pain start suddenly following an incident or develop gradually?", [
                    "Sudden acute onset following physical activity or strain",
                    "Gradually developed over several days or weeks",
                    "Chronic recurring episode over several months"
                ])
            },
            "ml": {
                "q1": ("വേദനയുടെ തീവ്രത 1 മുതൽ 10 വരെയുള്ള അളവിൽ എങ്ങനെ വിവരിക്കും?", [
                    "നേരിയത് (1 - 3): അനുഭവപ്പെടുന്നുണ്ടെങ്കിലും ദൈനംദിന കാര്യങ്ങൾക്ക് തടസ്സമില്ല",
                    "മിതമായത് (4 - 6): ജോലികൾക്ക് തടസ്സം, വിശ്രമിച്ചാൽ കുറവുണ്ട്",
                    "കഠിനമായത് (7 - 10): ചലിക്കാനോ ഉറങ്ങാനോ കഴിയാത്ത വിധം അസഹ്യം"
                ]),
                "q2": ("ഈ വേദന പെട്ടെന്ന് തുടങ്ങിയതാണോ അതോ ക്രമേണ വികസിച്ചതാണോ?", [
                    "ആയാസകരമായ പ്രവൃത്തിക്ക് ശേഷം പെട്ടെന്ന് ആരംഭിച്ചത്",
                    "ദിവസങ്ങളോ ആഴ്ചകളോ കൊണ്ട് പതുക്കെ കൂടിയത്",
                    "മാസങ്ങളായി ഇടയ്ക്കിടെ വരുന്നത്"
                ])
            },
            "hi": {
                "q1": ("1 से 10 के पैमाने पर आप इस दर्द की तीव्रता का वर्णन कैसे करेंगे?", [
                    "हल्का (1 - 3): महसूस होता है लेकिन सामान्य दैनिक कार्यों को नहीं रोकता",
                    "मध्यम (4 - 6): काम में बाधा डालता है, आराम करने पर नियंत्रित रहता है",
                    "गंभीर (7 - 10): अत्यधिक, सामान्य हलचल और नींद को रोकता है"
                ]),
                "q2": ("क्या यह दर्द अचानक किसी गतिविधि के बाद शुरू हुआ या धीरे-धीरे विकसित हुआ?", [
                    "शारीरिक परिश्रम या खिंचाव के बाद अचानक तेज शुरुआत",
                    "कई दिनों या हफ्तों में धीरे-धीरे विकसित हुआ",
                    "कई महीनों से बार-बार होने वाली पुरानी समस्या"
                ])
            }
        },
        "skin": {
            "en": {
                "q1": ("Is the skin issue accompanied by severe itching, burning, or spreading?", [
                    "Moderate to severe itching, spreading across new areas",
                    "Mild itching, localised to one area",
                    "No itching, primarily redness or discoloration",
                    "Painful or burning sensation"
                ]),
                "q2": ("Have you recently used any new soap, cosmetics, medication, or food?", [
                    "Yes, noticed symptoms right after using a new product/food",
                    "No known new exposures or changes",
                    "Seasonal flare-up that recurs annually"
                ])
            },
            "ml": {
                "q1": ("ത്വക്കിലെ അസ്വസ്ഥതയോടൊപ്പം കഠിനമായ ചൊറിച്ചിലോ പുകച്ചിലോ പടരുന്നതോ ഉണ്ടോ?", [
                    "കഠിനമായ ചൊറിച്ചിൽ, പുതിയ ഭാഗങ്ങളിലേക്ക് പടരുന്നു",
                    "നേരിയ ചൊറിച്ചിൽ, ഒരു ഭാഗത്ത് മാത്രം",
                    "ചൊറിച്ചിലില്ല, ചുവപ്പ് നിറം മാത്രം",
                    "വേദനയോ പുകച്ചിലോ അനുഭവപ്പെടുന്നു"
                ]),
                "q2": ("അടുത്തിടെ പുതിയ സോപ്പ്, സൗന്ദര്യവർദ്ധക വസ്തുക്കൾ, മരുന്നുകൾ, അല്ലെങ്കിൽ ഭക്ഷണം ഉപയോഗിച്ചിരുന്നോ?", [
                    "അതെ, പുതിയ ഉൽപ്പന്നം/ഭക്ഷണം കഴിച്ചതിന് തൊട്ടുപിന്നാലെ കണ്ടു",
                    "പുതിയ മാറ്റങ്ങളോ സമ്പർക്കങ്ങളോ ഇല്ല",
                    "വർഷം തോറും വരാറുള്ള സീസണൽ അലർജി"
                ])
            },
            "hi": {
                "q1": ("क्या त्वचा की समस्या के साथ तेज खुजली, जलन या फैलाव हो रहा है?", [
                    "मध्यम से तीव्र खुजली, नए क्षेत्रों में फैल रही है",
                    "हल्की खुजली, केवल एक क्षेत्र तक सीमित",
                    "कोई खुजली नहीं, केवल लालिमा या रंग बदलना",
                    "दर्द या जलन का अहसास"
                ]),
                "q2": ("क्या आपने हाल ही में कोई नया साबुन, सौंदर्य प्रसाधन, दवा या खाद्य पदार्थ इस्तेमाल किया है?", [
                    "हां, नए उत्पाद/भोजन के तुरंत बाद लक्षण दिखाई दिए",
                    "कोई नया संपर्क या बदलाव ज्ञात नहीं है",
                    "मौसमी एलर्जी जो हर साल दोबारा होती है"
                ])
            }
        },
        "lifestyle": {
            "en": {
                "q1": ("How significantly are these symptoms impacting your sleep and daily routine?", [
                    "Substantial disruption to sleep and daily energy levels",
                    "Moderate impact, managing with effort",
                    "Mild impact during specific times of day"
                ]),
                "q2": ("How long have you been experiencing this fatigue, stress, or digestive discomfort?", [
                    "Recent onset (last few days to 1 week)",
                    "Between 2 to 4 weeks",
                    "Ongoing for more than a month"
                ])
            },
            "ml": {
                "q1": ("ഈ ലക്ഷണങ്ങൾ നിങ്ങളുടെ ഉറക്കത്തെയും ദിനചര്യകളെയും എത്രത്തോളം ബാധിക്കുന്നുണ്ട്?", [
                    "ഉറക്കത്തെയും ദൈനംദിന ഊർജ്ജത്തെയും സാരമായി ബാധിക്കുന്നു",
                    "മിതമായ സ്വാധീനം, എങ്ങനെയെങ്കിലും മുന്നോട്ടുപോകുന്നു",
                    "ദിവസത്തിലെ ചില സമയങ്ങളിൽ മാത്രം നേരിയ ബുദ്ധിമുട്ട്"
                ]),
                "q2": ("ഈ ക്ഷീണമോ അസ്വാസ്ഥ്യമോ എത്ര നാളായി അനുഭവപ്പെടുന്നു?", [
                    "അടുത്തിടെ ആരംഭിച്ചത് (കഴിഞ്ഞ ഏതാനും ദിവസങ്ങൾ മുതൽ 1 ആഴ്ച വരെ)",
                    "2 മുതൽ 4 ആഴ്ച വരെ",
                    "ഒരു മാസത്തിലേറെയായി തുടരുന്നു"
                ])
            },
            "hi": {
                "q1": ("ये लक्षण आपकी नींद और दिनचर्या को कितना प्रभावित कर रहे हैं?", [
                    "नींद और दैनिक ऊर्जा के स्तर में भारी व्यवधान",
                    "मध्यम प्रभाव, प्रयास के साथ संभल रहा है",
                    "दिन के विशिष्ट समय के दौरान हल्का प्रभाव"
                ]),
                "q2": ("आप इस थकान, तनाव या पाचन संबंधी परेशानी का अनुभव कब से कर रहे हैं?", [
                    "हाल ही में शुरुआत (पिछले कुछ दिनों से 1 सप्ताह तक)",
                    "2 से 4 सप्ताह के बीच",
                    "एक महीने से अधिक समय से जारी"
                ])
            }
        },
        "general": {
            "en": {
                "q1": ("When did you first notice these symptoms starting?", [
                    "Today / Less than 24 hours ago",
                    "2 to 3 days ago",
                    "1 to 2 weeks ago",
                    "More than 2 weeks ago (persistent)"
                ]),
                "q2": ("Have the symptoms improved, worsened, or stayed the same?", [
                    "Progressively getting worse",
                    "Staying about the same",
                    "Gradually improving",
                    "Comes and goes intermittently"
                ])
            },
            "ml": {
                "q1": ("ഈ പ്രശ്നം എപ്പോൾ ആരംഭിച്ചു?", [
                    "ഇന്ന് / 24 മണിക്കൂറിനുള്ളിൽ",
                    "2 മുതൽ 3 ദിവസം മുൻപ്",
                    "1 മുതൽ 2 ആഴ്ച മുൻപ്",
                    "2 ആഴ്ചയിൽ കൂടുതൽ (തുടർച്ചയായി)"
                ]),
                "q2": ("ലക്ഷണങ്ങൾ മെച്ചപ്പെട്ടോ, മോശമായോ, അതേപടി തുടരുകയാണോ?", [
                    "കൂടുതൽ മോശമായിക്കൊണ്ടിരിക്കുന്നു",
                    "മാറ്റമില്ലാതെ തുടരുന്നു",
                    "പതുക്കെ മെച്ചപ്പെടുന്നുണ്ട്",
                    "ഇടവിട്ട് വന്നുപോകുന്നു"
                ])
            },
            "hi": {
                "q1": ("यह समस्या कब शुरू हुई?", [
                    "आज / 24 घंटे से कम समय पहले",
                    "2 से 3 दिन पहले",
                    "1 से 2 सप्ताह पहले",
                    "2 सप्ताह से अधिक समय से"
                ]),
                "q2": ("क्या लक्षण बेहतर हुए हैं, बिगड़े हैं या वैसे ही हैं?", [
                    "लगातार बिगड़ रहे हैं",
                    "बिना किसी बदलाव के बने हुए हैं",
                    "धीरे-धीरे सुधार हो रहा है",
                    "रुक-रुक कर आ रहे हैं"
                ])
            }
        }
    }

    category_dict = QUESTIONS_DB.get(category, QUESTIONS_DB["general"])
    q_data = category_dict.get(lang, category_dict["en"])
    q1_text, q1_opts = q_data["q1"]
    q2_text, q2_opts = q_data["q2"]

    return [
        {
            "id": "q1",
            "question": q1_text,
            "type": "choice",
            "options": q1_opts
        },
        {
            "id": "q2",
            "question": q2_text,
            "type": "choice",
            "options": q2_opts
        }
    ]


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

    questions = generate_two_clinical_questions(complaint, medical_system, department, language=language)

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
    """Returns exactly two context-aware questions for a complaint in the requested language."""
    data = request.get_json() or {}
    complaint = data.get('complaint', '')
    department = data.get('department', 'General Medicine')
    medical_system = data.get('medical_system', 'Modern / Conventional Medicine')
    language = data.get('language', 'English')

    questions = generate_two_clinical_questions(complaint, medical_system, department, language=language)
    return success_response(data={"questions": questions, "language": language})


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
