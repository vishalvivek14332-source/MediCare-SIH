from database.db import mongo
from bson.objectid import ObjectId

class Payment:
    @staticmethod
    def create(appointment_id, amount, payment_status, payment_id):
        payment_data = {
            "appointment_id": ObjectId(appointment_id) if isinstance(appointment_id, str) else appointment_id,
            "amount": amount,
            "payment_status": payment_status,
            "payment_id": payment_id
        }
        return mongo.db.payments.insert_one(payment_data)
