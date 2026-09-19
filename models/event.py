from database.db import mongo
from datetime import datetime

class EventLog:
    @staticmethod
    def log(event_type, description, user_id=None, role=None, clinic_id=None):
        event_data = {
            "event_type": event_type, # e.g. "CLINIC_CREATED", "BOOKING_MADE"
            "description": description,
            "user_id": user_id,
            "role": role,
            "clinic_id": clinic_id,
            "timestamp": datetime.utcnow()
        }
        return mongo.db.events.insert_one(event_data)

    @staticmethod
    def get_recent(limit=50):
        events = list(mongo.db.events.find().sort("timestamp", -1).limit(limit))
        for e in events:
            e['_id'] = str(e['_id'])
            # format timestamp safely
            e['time_str'] = e['timestamp'].strftime("%Y-%m-%d %H:%M:%S") if 'timestamp' in e else ''
        return events
