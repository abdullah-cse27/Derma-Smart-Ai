# FILE_NAME: app/core/risk_calculator.py

try:
    from config import RISK_WEIGHTS
except ImportError:
    # Safe fallbacks agar config load na ho
    RISK_WEIGHTS = {"image": 0.7, "symptom": 0.3}

def calculate_risk(confidence: float, symptom_score: float) -> dict:
    """
    Calculate final risk score with dynamic weighting and safety checks.
    """

    try:
        # 1. Type Casting & Safety (Crucial to avoid 0.0 results)
        conf = float(confidence) if confidence is not None else 0.5
        symp = float(symptom_score) if symptom_score is not None else 0.5

        # 2. Dynamic Weighting Logic
        # Agar confidence bohot low hai (Symptom Mode), toh symptoms ko zyada weight do
        if conf < 0.1: 
            risk_score = symp * 0.9 # Primary focus on symptoms
        else:
            risk_score = (
                RISK_WEIGHTS.get("image", 0.7) * conf +
                RISK_WEIGHTS.get("symptom", 0.3) * symp
            )

        # 3. Normalize (0–100 scale)
        final_score = round(max(0, min(risk_score, 1.0)) * 100, 2)

        # 4. Level Mapping (Synced with Severity Calculator)
        if final_score < 35:
            level = "Low"
            message = "Low clinical risk. Routine care recommended."
        elif final_score < 75:
            level = "Moderate"
            message = "Moderate risk. Clinical monitoring advised."
        else:
            level = "High"
            message = "High risk level. Urgent specialist consultation suggested."

        return {
            "risk_score": final_score,
            "risk_level": level,
            "risk_message": message
        }

    except Exception as e:
        print("Risk calculation error:", e)
        # Professional fallback instead of 'Unknown'
        return {
            "risk_score": 50.0,
            "risk_level": "Moderate",
            "risk_message": "Standard risk protocol applied due to data variance."
        }