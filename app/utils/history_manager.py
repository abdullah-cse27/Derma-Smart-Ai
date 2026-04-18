import json
import os
from datetime import datetime

HISTORY_FILE = "data/logs/history.json"

def save_history(result):
    os.makedirs("data/logs", exist_ok=True)

    history = []

    # Read existing history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []

    # 🛡️ Safe Extraction (taaki key missing hone par crash na ho)
    label = result.get("label", "Unknown")
    
    raw_conf = result.get("confidence", 0)
    confidence_pct = int(raw_conf * 100) if raw_conf <= 1.0 else int(raw_conf)
    
    risk_data = result.get("risk", {})
    risk_level = risk_data.get("risk_level", "N/A")
    
    # Check severity (Symptom mode mein ho sakta hai, Visual mein nahi)
    severity_data = result.get("severity", {})
    severity_level = severity_data.get("severity_level", "Standard")

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disease": label,
        "confidence": confidence_pct,
        "risk": risk_level,
        "severity": severity_level
    }

    # Add to list and keep only last 50 entries (Cleanup logic)
    history.append(entry)
    if len(history) > 50:
        history = history[-50:]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)