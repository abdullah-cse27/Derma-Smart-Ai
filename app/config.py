# ================================
# 📦 MODEL CONFIG
# ================================
MODEL_PATH = "model/skin_model_best.h5"
IMAGE_SIZE = (224, 224)

# ================================
# 🎨 UI & ICONS
# ================================
CATEGORY_ICONS = {
    "Stomach": "🤢", 
    "Head": "🧠", 
    "Skin": "🛡️", 
    "General": "🌡️"
}

# ================================
# 🧠 CLASSES (Hard-Synced with your classes.json)
# ================================
# sequence (0-7) exactly wahi hai jo tune bheja hai
CLASSES = [
    "Acne",                  # 0
    "Basal_Cell_Carcinoma",  # 1
    "Dermatitis",            # 2
    "Eczema",                # 3
    "Melanoma",              # 4
    "Psoriasis",             # 5
    "Vitiligo",              # 6
    "Warts"                  # 7
]

# Required for predictor logical filtering
DISEASE_TYPES = {
    "VISUAL": CLASSES,
    "INTERNAL": ["Stomach Pain", "Headache", "Gastritis", "Migraine", "Indigestion"]
}

# Detailed info for UI display
CLASS_INFO = {
    "Acne": {"display": "Acne / Muhaase", "severity": "Low", "action": "Wash face with mild cleanser and avoid oily food."},
    "Basal_Cell_Carcinoma": {"display": "Basal Cell Carcinoma", "severity": "High", "action": "🚨 Clinical evaluation required. Possible skin cancer."},
    "Dermatitis": {"display": "Dermatitis / Skin Inflammation", "severity": "Moderate", "action": "Identify triggers/allergens and use soothing creams."},
    "Eczema": {"display": "Eczema / Rash", "severity": "Moderate", "action": "Keep skin hydrated with thick moisturizers."},
    "Melanoma": {"display": "Melanoma (Critical)", "severity": "Critical", "action": "🚨 EMERGENCY: Immediate specialist review needed (Potential Cancer)."},
    "Psoriasis": {"display": "Psoriasis", "severity": "Moderate", "action": "Apply prescribed ointments and manage stress."},
    "Vitiligo": {"display": "Vitiligo / White Patches", "severity": "Safe", "action": "Use sunscreen to protect depigmented areas."},
    "Warts": {"display": "Warts / Masse", "severity": "Low", "action": "Consult doctor for removal or OTC treatments."},
    "Normal": {"display": "Healthy Skin", "severity": "Safe", "action": "Looking good! Stay hydrated and use SPF."}
}

# ================================
# 🧠 INTERNAL DIAGNOSIS LOGIC
# ================================
INTERNAL_DATA = {
    "Stomach": {
        "questions": ["Burning sensation in chest (Heartburn/Acidity)", "Severe cramps & Vomiting (Food Poisoning)", "Bloating after eating (Indigestion)"],
        "mapping": {
            "Burning sensation in chest (Heartburn/Acidity)": {"label": "Gastritis/Acidity", "severity": "Moderate"},
            "Severe cramps & Vomiting (Food Poisoning)": {"label": "Food Poisoning", "severity": "High"},
            "Bloating after eating (Indigestion)": {"label": "Indigestion", "severity": "Low"}
        }
    },
    "Head": {
        "questions": ["Pain on one side only (Migraine)", "Pressure like a band around head (Tension)", "Sudden sharp pain with dizziness (Critical)"],
        "mapping": {
            "Pain on one side only (Migraine)": {"label": "Migraine", "severity": "Moderate"},
            "Pressure like a band around head (Tension)": {"label": "Tension Headache", "severity": "Low"},
            "Sudden sharp pain with dizziness (Critical)": {"label": "Clinical Assessment Needed", "severity": "High"}
        }
    }
}

# ================================
# ⚖️ RISK & SEVERITY SETTINGS
# ================================
RISK_WEIGHTS = {
    "image": 0.7, 
    "symptom": 0.3
}

RISK_LEVELS = {
    "Safe": {"color": "#10b981", "label": "🟢 SAFE / SURAKSHIT"},
    "Low": {"color": "#3b82f6", "label": "🔵 LOW RISK / KAM KHATRA"},
    "Moderate": {"color": "#f59e0b", "label": "🟡 MODERATE / SAVDHAN"},
    "High": {"color": "#ef4444", "label": "🔴 HIGH RISK / KHATRA"},
    "Critical": {"color": "#7f1d1d", "label": "🚨 EMERGENCY / TURANT DOCTOR"}
}

# For calculators fallback
SYMPTOM_WEIGHTS = {"Itching": 0.2, "Burning": 0.3, "Redness": 0.2, "Swelling": 0.3}
DURATION_SCORES = {"short": 0.1, "long": 0.4}