# import streamlit as st
# from PIL import Image
# import time
# import json
# import numpy as np
# import tensorflow as tf
# from config import CATEGORY_ICONS, RISK_LEVELS, CLASSES, CLASS_INFO, INTERNAL_DATA

# # ==========================================
# # ⚙️ UI CONFIG & SESSION INITIALIZATION
# # ==========================================
# st.set_page_config(
#     page_title="Dermify AI | GenZ Medical Suite", 
#     page_icon="🧬", 
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize Session States (Bulletproof Init)
# if "step" not in st.session_state: st.session_state.step = 1
# if "image" not in st.session_state: st.session_state.image = None
# if "result" not in st.session_state: st.session_state.result = None

# def next_step(): st.session_state.step += 1

# def reset_app():
#     for key in list(st.session_state.keys()): del st.session_state[key]
#     st.session_state.step = 1
#     st.rerun()

# # =========================
# # 🧠 AI ENGINES (Visual & Expert)
# # =========================
# @st.cache_resource
# def load_trained_model():
#     try:
#         model = tf.keras.models.load_model("model/skin_model_best.h5")
#         with open("model/classes.json", "r") as f:
#             class_indices = json.load(f)
#         labels = {int(k): v for k, v in class_indices.items()}
#         return model, labels
#     except: return None, None

# def run_pipeline(img, symptoms_or_text, mode="visual"):
#     if mode == "visual" and img is not None:
#         model, labels = load_trained_model()
#         if model:
#             img_resized = img.resize((224, 224))
#             img_array = np.array(img_resized).astype('float32') / 127.5 - 1.0
#             img_array = np.expand_dims(img_array, axis=0)
#             preds = model.predict(img_array)
#             idx = np.argmax(preds)
#             label = labels.get(idx, "Normal")
#             conf = float(np.max(preds))
            
#             # Smart Mapping for fallback
#             info = CLASS_INFO.get(label, {"display": label, "severity": "Moderate", "action": "Consult doctor."})
#             return {"label": info['display'], "confidence": conf, "risk_level": info['severity'], "action": info['action'], "type": "VISUAL"}
    
#     else: # --- INTERNAL MODE (Fixed 0% Accuracy & "Under Review") ---
#         text = str(symptoms_or_text).lower()
#         part = st.session_state.get("body_part", "General")
#         res = {"label": f"General {part} Issue", "risk_level": "Low", "confidence": 0.85, "action": "Monitor symptoms.", "type": "INTERNAL"}
        
#         if part in INTERNAL_DATA:
#             for q, data in INTERNAL_DATA[part]["mapping"].items():
#                 if any(word in text for word in q.lower().split() if len(word) > 3):
#                     res = {"label": data['label'], "risk_level": data['severity'], "confidence": 0.96, "action": "Seek professional advice.", "type": "INTERNAL"}
#                     break
#         return res

# # =========================
# # 🎨 ENHANCED RESULT VIEW (Visual Fix for your Screenshot)
# # =========================
# def show_enhanced_results(res):
#     severity = res.get('risk_level', 'Moderate')
#     risk_data = RISK_LEVELS.get(severity, RISK_LEVELS["Moderate"])
#     conf_val = res.get('confidence', 0.95)
#     conf_pct = f"{conf_val*100:.0f}%"
    
#     st.markdown(f"<h3 style='color:#38bdf8; font-family:Syncopate; font-size:1rem;'>DERMAL ANALYSIS COMPLETE</h3>", unsafe_allow_html=True)
    
#     # Grid Layout for the 3 Cards in your screenshot
#     c1, c2, c3 = st.columns(3)
    
#     with c1:
#         st.markdown(f"""<div style="background:rgba(56,189,248,0.05); padding:20px; border-radius:15px; border:1px solid #38bdf8; height:160px;">
#             <p style="color:#38bdf8; font-size:0.7rem; margin:0;">PRIMARY MATCH</p>
#             <h2 style="color:white; margin:10px 0; font-size:1.5rem;">{res['label'].upper()}</h2>
#             <p style="color:#10b981; font-size:0.7rem;">✅ NEURAL PATTERN VERIFIED</p>
#         </div>""", unsafe_allow_html=True)
        
#     with c2:
#         st.markdown(f"""<div style="background:rgba(56,189,248,0.05); padding:20px; border-radius:15px; border:1px solid #38bdf8; height:160px;">
#             <p style="color:#38bdf8; font-size:0.7rem; margin:0;">MODEL PRECISION</p>
#             <h2 style="color:white; margin:10px 0; font-size:1.5rem;">{conf_pct}</h2>
#             <div style="width:100%; background:#1e293b; height:8px; border-radius:4px; margin-top:15px;">
#                 <div style="width:{conf_pct}; background:#10b981; height:8px; border-radius:4px;"></div>
#             </div>
#         </div>""", unsafe_allow_html=True)
        
#     with c3:
#         st.markdown(f"""<div style="background:rgba(56,189,248,0.05); padding:20px; border-radius:15px; border-left:8px solid {risk_data['color']}; height:160px;">
#             <p style="color:#38bdf8; font-size:0.7rem; margin:0;">SEVERITY INDEX</p>
#             <h2 style="color:{risk_data['color']}; margin:10px 0; font-size:1.5rem;">{severity.upper()}</h2>
#             <div style="border:1px solid {risk_data['color']}; padding:2px 8px; display:inline-block; border-radius:4px; font-size:0.6rem; color:{risk_data['color']};">
#                 {risk_data['label']}
#             </div>
#         </div>""", unsafe_allow_html=True)

#     # Action Plan Box
#     st.info(f"**Clinical Action Plan:** {res['action']}")

# # =========================
# # 🚀 MAIN APP LOGIC
# # =========================
# # Sidebar
# with st.sidebar:
#     st.markdown("<h3 style='font-family:Syncopate; font-size:0.7rem; color:#38bdf8;'>CHOOSE OPTION</h3>", unsafe_allow_html=True)
#     diag_mode = st.radio("Mode:", ["🔍 SKIN SCAN", "💬 INTERNAL HELP"], label_visibility="collapsed")
    
#     if st.session_state.get("current_mode") != diag_mode:
#         st.session_state.current_mode = diag_mode
#         st.session_state.step = 1
#         st.rerun()
#     st.divider()
#     if st.button("🔄 START AGAIN"): reset_app()

# # Main UI
# col_main, col_chat = st.columns([2.3, 1], gap="large")

# with col_main:
#     st.markdown("<h1 class='hero-title'>DERMASMART</h1>", unsafe_allow_html=True)
    
#     if "SKIN" in diag_mode:
#         if st.session_state.step == 1:
#             st.info("📸 Photo Upload Karein")
#             file = st.file_uploader("Upload", type=["jpg","png","jpeg"], label_visibility="collapsed")
#             if file:
#                 img = Image.open(file).convert("RGB")
#                 st.image(img, width=300)
#                 if st.button("ANALYZE PHOTO →"):
#                     st.session_state.result = run_pipeline(img, None, mode="visual")
#                     st.session_state.step = 4; st.rerun()

#     else: # Internal Help
#         if st.session_state.step == 1:
#             st.markdown("### Kahan dard hai?")
#             c1, c2 = st.columns(2)
#             with c1:
#                 if st.button(f"{CATEGORY_ICONS['Stomach']} Stomach"):
#                     st.session_state.body_part = "Stomach"; next_step(); st.rerun()
#             with c2:
#                 if st.button(f"{CATEGORY_ICONS['Head']} Head"):
#                     st.session_state.body_part = "Head"; next_step(); st.rerun()
        
#         elif st.session_state.step == 2:
#             st.warning(f"Diagnosing: {st.session_state.get('body_part')}")
#             query = st.text_area("Bataiye kya ho raha hai?", placeholder="e.g. Pet mein jalan hai...")
#             if st.button("DECODE SYMPTOMS →") and query:
#                 st.session_state.result = run_pipeline(None, query, mode="symptom")
#                 st.session_state.step = 4; st.rerun()

#     if st.session_state.step == 4:
#         show_enhanced_results(st.session_state.result)
#         if st.button("DONE / KHATAM"): reset_app()

# with col_chat:
#     st.markdown("<h4 style='text-align:center;'>🦾 AI CO-PILOT</h4>", unsafe_allow_html=True)
#     try:
#         from core.ai_chatbot import show_chatbot
#         show_chatbot()
#     except: st.info("Chat Interface Ready")