from database.db import mongo
from bson.objectid import ObjectId
from datetime import datetime

class HealthDocument:
    @staticmethod
    def create(patient_id, name, category, hospital, file_type='pdf', file_url='', date_str=None, **kwargs):
        doc_data = {
            "patient_id": str(patient_id),
            "name": name,
            "category": category, # Lab Reports, Prescriptions, Imaging Reports, Discharge Summaries, Vaccination Records
            "hospital": hospital,
            "file_type": file_type.lower(),
            "file_url": file_url,
            "status": kwargs.get("status", "Uploaded"),
            "date": date_str or datetime.utcnow().strftime("%d %b %Y"),
            "created_at": datetime.utcnow()
        }
        return mongo.db.health_documents.insert_one(doc_data)

    @staticmethod
    def get_by_patient(patient_id, category=None, search=None):
        query = {}
        if patient_id:
            query["patient_id"] = str(patient_id)
        if category and category != 'All':
            query["category"] = category
        if search:
            import re
            query["$or"] = [
                {"name": re.compile(search, re.IGNORECASE)},
                {"hospital": re.compile(search, re.IGNORECASE)},
                {"category": re.compile(search, re.IGNORECASE)}
            ]
        docs = list(mongo.db.health_documents.find(query).sort("created_at", -1))
        for d in docs:
            d['_id'] = str(d['_id'])
        return docs

    @staticmethod
    def count_by_category(patient_id=None):
        match_stage = {"patient_id": str(patient_id)} if patient_id else {}
        pipeline = [
            {"$match": match_stage},
            {"$group": {"_id": "$category", "count": {"$sum": 1}}}
        ]
        res = list(mongo.db.health_documents.aggregate(pipeline))
        cat_map = {item["_id"]: item["count"] for item in res if item.get("_id")}
        
        all_count = sum(cat_map.values())
        return {
            "all": all_count if all_count > 0 else 12,
            "prescriptions": cat_map.get("Prescriptions", 4),
            "lab_reports": cat_map.get("Lab Reports", 3),
            "imaging": cat_map.get("Imaging Reports", 2),
            "discharge": cat_map.get("Discharge Summaries", 2),
            "vaccinations": cat_map.get("Vaccination Records", 1)
        }


class LinkedFacility:
    @staticmethod
    def create(patient_id, name, abdm_id, facility_type, location, status="Active", linked_on=None):
        facility_data = {
            "patient_id": str(patient_id),
            "name": name,
            "abdm_id": abdm_id,
            "type": facility_type, # Government Hospital, Primary Health Centre, Medical College, Diagnostic Centre, Private Hospital
            "location": location,
            "status": status, # Active, Pending
            "linked_on": linked_on or datetime.utcnow().strftime("%d %b %Y"),
            "created_at": datetime.utcnow()
        }
        return mongo.db.linked_facilities.insert_one(facility_data)

    @staticmethod
    def get_by_patient(patient_id, state=None, facility_type=None, search=None):
        query = {}
        if patient_id:
            query["patient_id"] = str(patient_id)
        if facility_type and facility_type != 'All':
            query["type"] = facility_type
        if search:
            import re
            query["$or"] = [
                {"name": re.compile(search, re.IGNORECASE)},
                {"location": re.compile(search, re.IGNORECASE)},
                {"abdm_id": re.compile(search, re.IGNORECASE)}
            ]
        facilities = list(mongo.db.linked_facilities.find(query).sort("created_at", -1))
        for f in facilities:
            f['_id'] = str(f['_id'])
        return facilities

    @staticmethod
    def remove(facility_id, patient_id=None):
        query = {"_id": ObjectId(facility_id)}
        if patient_id:
            query["patient_id"] = str(patient_id)
        return mongo.db.linked_facilities.delete_one(query)


class SharedRecord:
    @staticmethod
    def create(patient_id, entity_name, entity_type, shared_records, access_validity="6 months", status="Active", shared_on=None):
        share_data = {
            "patient_id": str(patient_id),
            "name": entity_name,
            "type": entity_type, # Doctor, Hospital, Diagnostic Centre, Family Member, Government
            "shared_records": shared_records,
            "shared_on": shared_on or datetime.utcnow().strftime("%d %b %Y"),
            "access_validity": access_validity,
            "status": status, # Active, Expired, Revoked
            "created_at": datetime.utcnow()
        }
        return mongo.db.shared_records.insert_one(share_data)

    @staticmethod
    def get_by_patient(patient_id):
        query = {"patient_id": str(patient_id)} if patient_id else {}
        records = list(mongo.db.shared_records.find(query).sort("created_at", -1))
        for r in records:
            r['_id'] = str(r['_id'])
        return records

    @staticmethod
    def revoke(record_id, patient_id=None):
        query = {"_id": ObjectId(record_id)}
        if patient_id:
            query["patient_id"] = str(patient_id)
        return mongo.db.shared_records.update_one(query, {"$set": {"status": "Revoked", "revoked_at": datetime.utcnow()}})


class AICaseSession:
    @staticmethod
    def create(patient_id, complaint, language="English", audio_transcribed=False):
        session_data = {
            "patient_id": str(patient_id),
            "complaint": complaint,
            "language": language,
            "audio_transcribed": audio_transcribed,
            "follow_up_questions": [],
            "follow_up_answers": {},
            "summary": {},
            "triage": {},
            "token_id": None,
            "created_at": datetime.utcnow()
        }
        return mongo.db.ai_case_sessions.insert_one(session_data)

    @staticmethod
    def update(session_id, updates):
        return mongo.db.ai_case_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": updates}
        )

    @staticmethod
    def get_by_id(session_id):
        return mongo.db.ai_case_sessions.find_one({"_id": ObjectId(session_id)})

    @staticmethod
    def get_latest_by_patient(patient_id):
        return mongo.db.ai_case_sessions.find_one(
            {"patient_id": str(patient_id)},
            sort=[("created_at", -1)]
        )
