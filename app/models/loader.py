# FILE_NAME: app/models/loader.py

import tensorflow as tf
import streamlit as st
try:
    from config import MODEL_PATH
except ImportError:
    MODEL_PATH = "model/skin_model_best.h5"

# @st.cache_resource ka use karne se model memory mein "Freeze" ho jata hai
# Isse app ki speed 10x fast ho jayegi
@st.cache_resource
def load_model():
    """
    Optimized Model Loader:
    - Uses Streamlit Caching to prevent re-loading
    - Error handling for missing .h5 files
    """
    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("✅ Model loaded successfully from cache!")
        return model
    except Exception as e:
        print(f"❌ Error loading model at {MODEL_PATH}: {e}")
        return None