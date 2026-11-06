import re

def analyze_project_context(idea: str):
    text = idea.lower()
    
    # 1. Specialized domains
    is_waste = any(k in text for k in ["waste", "trash", "bin", "garbage", "litter", "recycle", "segregat"])
    is_attendance = any(k in text for k in ["attendance", "face", "facial", "recognition", "classroom", "student attendance"])
    is_disaster = any(k in text for k in ["disaster", "flood", "earthquake", "hazard", "fire", "emergency", "wildfire", "tsunami"])
    is_medical = any(k in text for k in ["prescription", "drug", "doctor", "medical", "health", "clinical", "patient", "disease", "medicine"])
    is_finance = any(k in text for k in ["fraud", "transaction", "bank", "credit card", "money", "laundering", "market", "stock", "trading"])
    is_vision = is_waste or is_attendance or any(k in text for k in ["vision", "image", "video", "detect", "cnn", "camera", "photo", "ocr", "yolo"])
    is_iot = is_waste or is_disaster or any(k in text for k in ["iot", "sensor", "hardware", "arduino", "raspberry", "embedded", "drone", "uav"])
    is_nlp = is_medical or any(k in text for k in ["nlp", "text", "language", "sentiment", "summariz", "chat", "llm", "translate"])

    return {
        "is_waste": is_waste,
        "is_attendance": is_attendance,
        "is_disaster": is_disaster,
        "is_medical": is_medical,
        "is_finance": is_finance,
        "is_vision": is_vision,
        "is_iot": is_iot,
        "is_nlp": is_nlp,
    }

print("Smart Waste:", analyze_project_context("Smart Waste Management. Computer vision and IoT sensor bin fill-level and sorting."))
print("Attendance:", analyze_project_context("AI-Based Attendance System with facial recognition"))
print("Disaster:", analyze_project_context("Ai based disaster detection and risk assessment"))
