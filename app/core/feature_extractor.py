import numpy as np

def extract_features(image, symptoms):
    features = []

    # =========================
    # 🔍 SYMPTOM BASED FEATURES
    # =========================

    if symptoms.get("itching"):
        features.append("Itching detected (possible irritation or inflammation)")

    if symptoms.get("pain"):
        features.append("Pain present (possible infection or severity)")

    if symptoms.get("duration") == "long":
        features.append("Chronic condition (long duration)")

    # =========================
    # ⚠️ FALLBACK (IMPORTANT)
    # =========================
    if not features:
        features.append("No significant symptoms detected")

    # =========================
    # 🧪 DEBUG (optional)
    # =========================
    print("Features:", features)

    return features