# FILE_NAME: app/core/predictor.py

import numpy as np
from models.loader import load_model
from utils.image import preprocess_image
import streamlit as st

# ================================
# 📋 HARD-SYNCED CLASSES (From classes.json)
# ================================
try:
    from config import CLASSES, DISEASE_TYPES
except ImportError:
    # AGAR CONFIG FAIL HO JAYE, TOH YE LIST HI CHALNI CHAHIYE (0 to 7)
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
    DISEASE_TYPES = {"VISUAL": CLASSES, "INTERNAL": ["Stomach Pain", "Headache"]}

from transformers import pipeline

# ================================
# 🧠 SMART NLP ENGINE
# ================================
@st.cache_resource
def load_nlp():
    try:
        return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    except:
        return None

nlp_classifier = load_nlp()

def predict_symptoms(text):
    labels = DISEASE_TYPES.get("INTERNAL", ["Stomach Pain", "Headache"])
    if nlp_classifier:
        try:
            result = nlp_classifier(text, labels)
            return result['labels'][0], round(result['scores'][0], 2)
        except: pass
    
    text = text.lower()
    if any(w in text for w in ["stomach", "pet", "acidity"]): return "Stomach Pain", 0.90
    if any(w in text for w in ["head", "sar", "migraine"]): return "Headache", 0.90
    return "General Condition", 0.80

def predict(image=None, text=None, mode="visual"):
    """
    Hybrid Predictor: Image + Text
    """
    # 🔵 MODE 1: SYMPTOMS
    if mode == "symptom" and text:
        label, confidence = predict_symptoms(text)
        return label, confidence, [(label, confidence)]

    # 🔴 MODE 2: VISUAL (CNN)
    model = load_model()
    if model is None or image is None:
        return "Normal", 0.0, []

    try:
        # Preprocess
        img = preprocess_image(image)
        if img is None: return "Error", 0.0, []

        # Raw Prediction
        preds = model.predict(img, verbose=0)[0]
        
        # 🎯 THE FIX: Direct Index Mapping
        # np.argmax(preds) hume 0 se 7 ke beech ka sahi index dega
        best_idx = np.argmax(preds)
        label = CLASSES[best_idx]
        confidence = float(preds[best_idx])

        # Top 2 results for UI
        sorted_indices = np.argsort(preds)[::-1]
        top_results = []
        for i in sorted_indices[:2]:
            top_results.append((CLASSES[i], float(preds[i])))

        return label, round(confidence, 2), top_results

    except Exception as e:
        print(f"Prediction error: {e}")
        return "Error", 0.0, []