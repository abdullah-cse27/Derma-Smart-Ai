# FILE_NAME: app/core/symptom_analyzer.py

import os
import json
from groq import Groq
from dotenv import load_dotenv

try:
    from config import SYMPTOM_WEIGHTS, DURATION_SCORES, SEVERITY_LEVELS
except ImportError:
    SYMPTOM_WEIGHTS = {"Itching": 0.2, "Burning": 0.3}
    DURATION_SCORES = {"short": 0.1, "long": 0.3}
    SEVERITY_LEVELS = {"Low": 0.1, "High": 0.5}

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_symptoms(symptoms, mode="visual"):
    """
    Analyzes symptoms with JSON enforcement for Symptom Mode.
    """
    
    # ==========================================
    # 🧴 MODE 1: VISUAL (Skin Symptoms Math)
    # ==========================================
    if mode == "visual":
        try:
            score = 0.0
            if isinstance(symptoms, dict):
                for symptom, weight in SYMPTOM_WEIGHTS.items():
                    if symptoms.get(symptom):
                        score += weight
                
                duration = symptoms.get("duration", "short")
                score += DURATION_SCORES.get(duration, 0)

            return round(min(score, 1.0), 2)
        except Exception as e:
            print("Skin Symptom Error:", e)
            return 0.0

    # ==========================================
    # 🩺 MODE 2: SYMPTOM (Strict JSON AI Mode)
    # ==========================================
    else:
        try:
            # AI Prompt strictly requesting JSON
            prompt = f"""
            Analyze these medical symptoms: "{symptoms}"
            
            Return ONLY a JSON object with this exact structure:
            {{
                "label": "Specific Disease Name",
                "symptom_score": 0.0 to 1.0,
                "recommendations": ["Action 1", "Action 2", "Action 3"],
                "message": "Short risk summary"
            }}
            """

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a diagnostic expert. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}, # Strictly JSON
                temperature=0.2,
            )
            
            # Parse the JSON response
            raw_res = json.loads(completion.choices[0].message.content)
            
            return {
                "label": raw_res.get("label", "General Condition"),
                "symptom_score": float(raw_res.get("symptom_score", 0.5)),
                "recommendations": raw_res.get("recommendations", ["Consult a doctor"]),
                "top_results": [] # Placeholder for UI consistency
            }

        except Exception as e:
            print("AI Symptom Analysis Error:", e)
            return {
                "label": "General Discomfort",
                "symptom_score": 0.4,
                "recommendations": ["Rest and hydrate", "Consult a GP if pain persists"],
                "top_results": []
            }