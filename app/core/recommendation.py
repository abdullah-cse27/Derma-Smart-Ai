def get_recommendation(label, severity_level):
    """
    Provide recommendations based on severity
    """

    if severity_level == "Mild":
        return [
            "Maintain skin hygiene",
            "Use light moisturizer",
            "Avoid harsh products"
        ]

    elif severity_level == "Moderate":
        return [
            "Avoid irritants",
            "Monitor condition closely",
            "Use medicated creams",
            "Consider consulting a doctor if no improvement"
        ]

    elif severity_level == "Severe":
        return [
            "Consult a dermatologist immediately",
            "Avoid self-medication",
            "Follow prescribed treatment strictly"
        ]

    else:
        return [
            "Unable to determine recommendation",
            "Please consult a medical professional"
        ]