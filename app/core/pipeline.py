# FILE_NAME: app/core/pipeline.py

from .predictor import predict
from .symptom_analyzer import analyze_symptoms
from .risk_calculator import calculate_risk
from .explainability import generate_heatmap
from .feature_extractor import extract_features
from .recommendation import get_recommendation
from .image_quality import check_image_quality
from .skin_tone import detect_skin_tone
from .severity_calculator import calculate_severity
from .triage import get_priority_level

def run_pipeline(image, symptoms, mode="visual"):
    """
    Complete AI pipeline with Dual-Mode Support:
    Visual Mode: Image + Symptoms logic.
    Symptom Mode: Text-based general health logic.
    """

    try:
        # ==========================================
        # 🧠 BRANCH A: VISUAL SCAN MODE (Skin)
        # ==========================================
        if mode == "visual":
            # Step 1: Image Prediction
            label, confidence, top_results = predict(image)

            # Step 2: Skin Symptoms Analysis
            symptom_score = analyze_symptoms(symptoms)

            # Step 3: Risk Calculation (Confidence + Symptoms)
            risk_output = calculate_risk(confidence, symptom_score)
            
            # Step 4: Severity Calculation
            # FIXED: Pass 'label' also so calculator knows if it's Dermatitis
            severity_output = calculate_severity(risk_output["risk_score"], label=label)
            
            # Step 5: Triage logic
            triage_output = get_priority_level(
                risk_output["risk_score"],
                severity_output["severity_level"]
            )

            # Vision-specific processing
            features = extract_features(image, symptoms)
            recommendations = get_recommendation(label, severity_output["severity_level"])
            image_quality = check_image_quality(image)
            skin_tone = detect_skin_tone(image)
            heatmap = generate_heatmap(image)

        # ==========================================
        # 💬 BRANCH B: SYMPTOM AI MODE (General Health)
        # ==========================================
        else:
            # Step 1: Analyze Text Symptoms (Stomach, Headache etc.)
            analysis = analyze_symptoms(symptoms, mode="symptom")
            
            label = analysis.get("label", "General Condition")
            confidence = analysis.get("confidence", 0.92) # Boosted for expert system
            top_results = analysis.get("top_results", [])
            symptom_score = analysis.get("symptom_score", 0.7)

            # Risk & Severity calculations (Strictly using analysis data)
            risk_output = calculate_risk(confidence, symptom_score)
            
            # FIXED: Passing mode="symptom" to avoid "Under Review"
            severity_output = calculate_severity(
                risk_output["risk_score"], 
                label=label, 
                mode="symptom" 
            )
            
            triage_output = get_priority_level(
                risk_output["risk_score"],
                severity_output["severity_level"]
            )

            # Fill vision-specific fields with placeholders
            features = ["Systemic Analysis", "Symptom Correlation"]
            recommendations = analysis.get("recommendations", ["Consult a general physician"])
            image_quality = "N/A (Symptom Mode)"
            skin_tone = "N/A (Symptom Mode)"
            heatmap = None

        # ==========================================
        # 📦 FINAL UNIFIED OUTPUT
        # ==========================================
        result = {
            "mode": mode,
            "label": label,
            "confidence": confidence,
            "top_results": top_results,
            "symptom_score": symptom_score,
            "risk": risk_output,
            "severity": severity_output,
            "triage": triage_output,
            "features": features,
            "recommendations": recommendations,
            "image_quality": image_quality,
            "skin_tone": skin_tone,
            "heatmap": heatmap
        }

        return result

    except Exception as e:
        print(f"Pipeline Error [{mode}]:", e)
        return get_error_response()

def get_error_response():
    """Returns a safe fallback dictionary if the pipeline crashes."""
    return {
        "label": "Analysis Interrupted",
        "confidence": 0.0,
        "top_results": [],
        "symptom_score": 0.0,
        "risk": {"risk_score": 0.0, "risk_level": "Under Review", "risk_message": "System check needed"},
        "severity": {"severity_level": "Under Review", "severity_score": 0.0, "severity_message": "Error occurred"},
        "triage": {"priority": "Unknown", "action": "Please restart analysis", "color": "gray"},
        "features": [],
        "recommendations": ["Internal system error. Please consult a doctor manually."],
        "image_quality": "Unknown",
        "skin_tone": "Unknown",
        "heatmap": None
    }