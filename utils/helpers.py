from flask import jsonify

def success_response(data=None, message="Success", status=200):
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status

def error_response(message="Error", status=400):
    return jsonify({
        "success": False,
        "message": message
    }), status

import math
def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 
    return round(c * r, 2)

def generate_time_slots(total_tokens):
    from datetime import datetime, timedelta
    slots = []
    current_time = datetime.strptime("09:00 AM", "%I:%M %p")
    for _ in range(total_tokens):
        if current_time.hour >= 12 and current_time.hour < 14:
            current_time = current_time.replace(hour=14, minute=0)
        slots.append(current_time.strftime("%I:%M %p"))
        current_time += timedelta(minutes=30)
    return slots
