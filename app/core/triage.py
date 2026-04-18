def get_priority_level(risk_score: float, severity_level: str) -> dict:
    """
    Determine priority level based on risk + severity
    """

    if risk_score >= 80 or severity_level == "Severe":
        return {
            "priority": "Critical",
            "action": "Seek immediate medical attention",
            "color": "red"
        }

    elif risk_score >= 60:
        return {
            "priority": "High",
            "action": "Consult a doctor soon",
            "color": "orange"
        }

    elif risk_score >= 40:
        return {
            "priority": "Medium",
            "action": "Monitor symptoms carefully",
            "color": "yellow"
        }

    else:
        return {
            "priority": "Low",
            "action": "Basic care is sufficient",
            "color": "green"
        }