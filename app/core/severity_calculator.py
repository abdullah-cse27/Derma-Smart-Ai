# FILE_NAME: app/core/severity_calculator.py

def calculate_severity(risk_score: float, label: str = "General", mode: str = "visual") -> dict:
    """
    Advanced Severity Calculator with Label-Aware logic.
    Supports both Visual (Skin) and Symptom (Internal) modes.
    """

    # 1. Null Check & Default Handling
    if risk_score is None:
        return {
            "severity_level": "Moderate", # Fallback to Moderate instead of Unknown
            "severity_score": 50,
            "severity_message": "Dermal assessment in progress. Monitoring recommended."
        }

    # Safety clamp (0-100)
    risk_score = max(0, min(100, risk_score))

    # 2. Disease-Specific Severity Boosts (Avoiding "Under Review")
    # Agar label 'Dermatitis' hai toh hum moderate base level rakhenge
    if "Dermatitis" in label or "Eczema" in label:
        risk_score = max(risk_score, 45) 
    
    # Internal mode ke liye thresholds thode sensitive rakhte hain
    if mode == "symptom":
        risk_score = max(risk_score, 30) # Internal pain is rarely 'Low' risk

    # 3. Core Severity Logic
    if risk_score < 35:
        level = "Low"
        message = "Condition appears localized and mild. Standard monitoring advised."

    elif risk_score < 75:
        level = "Moderate"
        message = "Clinical markers suggest moderate activity. Professional consultation recommended."

    else:
        level = "High"
        message = "High clinical priority detected. Immediate specialist review required."

    return {
        "severity_level": level,
        "severity_score": round(risk_score, 2),
        "severity_message": message
    }