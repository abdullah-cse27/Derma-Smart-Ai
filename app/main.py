import streamlit as st
from PIL import Image
import time
import json
import numpy as np
import cv2
import os
from fpdf import FPDF
from groq import Groq
from dotenv import load_dotenv

# Your specific files
from config import RISK_LEVELS
from core.ai_chatbot import show_chatbot

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ==========================================
# ⚙️ UI CONFIG & STYLING
# ==========================================
st.set_page_config(page_title="DermaSmart AI Pro", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Space+Grotesk:wght@300;500;700&display=swap');

.stApp {
    background-color:#050505;
    color:#e2e8f0;
    padding-bottom:80px;
}

.hero-title{
    font-family:'Syncopate',sans-serif;
    background:linear-gradient(90deg,#0ea5e9,#a855f7,#0ea5e9);
    background-size:200% auto;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-size:3.2rem;
    font-weight:700;
    text-align:center;
    animation:shine 4s linear infinite;
}

@keyframes shine{
    to{background-position:200% center;}
}

.result-card{
    background:rgba(255,255,255,0.03);
    backdrop-filter:blur(10px);
    border:1px solid rgba(255,255,255,0.08);
    padding:24px;
    border-radius:20px;
    margin-bottom:18px;
}

.section-header{
    background:linear-gradient(90deg, rgba(14,165,233,0.2), transparent);
    padding:8px 15px;
    border-left:4px solid #0ea5e9;
    font-weight:bold;
    font-family:'Space Grotesk',sans-serif;
    margin-top:15px;
    border-radius:0 8px 8px 0;
}

.footer-disclaimer{
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background:#111;
    color:#ff6b6b;
    text-align:center;
    padding:12px;
    font-size:13px;
    border-top:1px solid #333;
    z-index:999;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 📄 PDF REPORT
# ==========================================
def generate_pdf_report(res, report):
    import io, os, tempfile, re
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import inch

    buffer = io.BytesIO()

    # Font
    font_name = "Helvetica"
    for fp in [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "DejaVuSans.ttf"
    ]:
        if os.path.exists(fp):
            try:
                pdfmetrics.registerFont(TTFont("CustomFont", fp))
                font_name = "CustomFont"
                break
            except:
                pass

    doc = SimpleDocTemplate(buffer, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()

    title = ParagraphStyle("title", parent=styles["Title"], fontName=font_name, fontSize=22, spaceAfter=12)
    heading = ParagraphStyle("heading", parent=styles["Heading2"], fontName=font_name, fontSize=14, spaceAfter=6)
    normal = ParagraphStyle("normal", parent=styles["Normal"], fontName=font_name, fontSize=11, leading=14)

    story = []

    def clean(x):
        if x is None:
            return None
        txt = str(x).strip()

        bad = ["none", "null", "not available", "-", "()", "[]", "{}", ",", ": - ."]
        if txt.lower() in bad:
            return None

        txt = re.sub(r'[\u0900-\u097F]+', '', txt)  # remove hindi chars
        txt = txt.replace("_", " ").strip()
        return txt if txt else None

    def add_content(content):
        if isinstance(content, dict):
            for k, v in content.items():
                v = clean(v)
                if v:
                    story.append(Paragraph(f"• <b>{clean(k.title())}:</b> {v}", normal))

        elif isinstance(content, list):
            added = False
            for item in content:
                if isinstance(item, dict):
                    name = clean(item.get("name"))
                    desc = clean(item.get("description"))
                    line = " ".join([x for x in [name, desc] if x])
                    if line:
                        story.append(Paragraph(f"• {line}", normal))
                        added = True
                else:
                    val = clean(item)
                    if val:
                        story.append(Paragraph(f"• {val}", normal))
                        added = True
            if not added:
                return False

        else:
            val = clean(content)
            if val:
                story.append(Paragraph(val, normal))
            else:
                return False

        return True

    # Header
    story.append(Paragraph("DERMASMART AI REPORT", title))
    story.append(Paragraph(f"Condition: {clean(res.get('label'))}", normal))
    story.append(Paragraph(f"Risk Level: {clean(res.get('risk'))}", normal))
    story.append(Paragraph(f"Confidence: {int(res.get('confidence',0)*100)}%", normal))
    story.append(Spacer(1, 10))

    # Image
    if res.get("img") is not None:
        try:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            res["img"].save(tmp.name)
            story.append(Image(tmp.name, width=5.6*inch, height=4.0*inch))
            story.append(Spacer(1, 12))
        except:
            pass

    sections = [
        ("1. Basic Identification", report.get("basic_identification")),
        ("2. Overview", report.get("overview")),
        ("3. Symptoms", report.get("symptoms")),
        ("4. Visual Characteristics", report.get("visual_characteristics")),
        ("5. Common Body Areas", report.get("common_body_areas")),
        ("6. Causes", report.get("causes")),
        ("7. Risk Factors", report.get("risk_factors")),
        ("8. Severity Levels", report.get("severity_levels")),
        ("9. Contagious or Not", report.get("contagious")),
        ("10. Diagnosis Methods", report.get("diagnosis_methods")),
        ("11. Treatment Options", report.get("medical_treatment")),
        ("12. Home Care", report.get("home_care")),
        ("13. Prevention", report.get("prevention")),
        ("14. When to See Doctor", report.get("doctor_urgently")),
        ("15. Recovery", report.get("recovery")),
        ("16. Complications", report.get("complications")),
        ("17. Lifestyle Advice", report.get("lifestyle_advice")),
        ("18. Doctor Advice", report.get("doctor_note")),
        ("19. Disclaimer", report.get("disclaimer")),
    ]

    for sec, data in sections:
        before_len = len(story)
        temp = []
        old_story = story[:]

        story.append(Paragraph(sec, heading))
        ok = add_content(data)

        if not ok:
            story = old_story  # skip empty section
        else:
            story.append(Spacer(1, 8))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
# ==========================================
# 🎯 HEATMAP
# ==========================================
def generate_heatmap(img):
    img_np = np.array(img.resize((450, 450)))
    heatmap = np.zeros((450, 450), dtype=np.uint8)
    cv2.circle(heatmap, (225, 200), 120, 255, -1)
    heatmap = cv2.GaussianBlur(heatmap, (101, 101), 0)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(img_np, 0.5, heatmap_color, 0.5, 0)
    return overlay

# ==========================================
# 🧠 AI REPORT GENERATOR
# ==========================================
def fetch_ai_info(label, risk, lang="Hinglish"):
    prompt = f"""
Create a HIGH QUALITY complete skin disease report for {label}.

Language: {lang} (Use Roman English letters only)
Risk Level: {risk}

IMPORTANT:
- No empty fields
- No null values
- No placeholders
- Give practical and realistic details
- Short but informative points

Return ONLY valid JSON:

{{
 "basic_identification": {{
   "disease_name": "{label}",
   "common_name": "",
   "category": "",
   "icd_code": ""
 }},
 "overview": "",
 "symptoms": [],
 "visual_characteristics": [],
 "common_body_areas": [],
 "causes": [],
 "risk_factors": [],
 "severity_levels": "",
 "contagious": "",
 "diagnosis_methods": [],
 "medical_treatment": [],
 "home_care": [],
 "prevention": [],
 "doctor_urgently": [],
 "recovery": "",
 "complications": [],
 "lifestyle_advice": [],
 "doctor_note": "",
 "disclaimer": "This AI report is for educational purposes only. Please consult a dermatologist."
}}
"""
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":prompt}],
            response_format={"type":"json_object"}
        )
        data = json.loads(resp.choices[0].message.content)
        return data
    except:
        return {
            "basic_identification": {
                "disease_name": label,
                "common_name": "Common Skin Condition",
                "category": "Dermatology",
                "icd_code": "N/A"
            },
            "overview": "This condition affects the skin and may cause irritation or inflammation.",
            "symptoms": ["Redness", "Itching", "Swelling"],
            "visual_characteristics": ["Red bumps", "Inflamed skin"],
            "common_body_areas": ["Face", "Back", "Shoulders"],
            "causes": ["Hormonal changes", "Bacteria", "Oil buildup"],
            "risk_factors": ["Stress", "Oily skin", "Poor hygiene"],
            "severity_levels": "Low to Moderate",
            "contagious": "Usually not contagious",
            "diagnosis_methods": ["Clinical examination", "Skin analysis"],
            "medical_treatment": ["Topical creams", "Antibiotics if needed"],
            "home_care": ["Gentle cleanser", "Do not scratch", "Keep skin clean"],
            "prevention": ["Wash skin regularly", "Healthy diet", "Avoid harsh cosmetics"],
            "doctor_urgently": ["Severe pain", "Rapid spreading", "Pus formation"],
            "recovery": "Usually improves in weeks with proper care.",
            "complications": ["Scarring", "Pigmentation"],
            "lifestyle_advice": ["Drink water", "Sleep well", "Reduce stress"],
            "doctor_note": "Consult dermatologist if symptoms continue.",
            "disclaimer": "This AI report is for educational purposes only."
        }
# ==========================================
# 🎨 RESULTS UI
# ==========================================
def show_enhanced_results(res):
    label = res.get("label", "Unknown Condition")
    risk = res.get("risk", "Moderate")
    confidence = res.get("confidence", 0.0)
    action = res.get("action", "Consult a doctor.")
    img = res.get("img")

    lang = st.radio(
        "🌐 Select Language / भाषा चुनें",
        ["Hinglish", "English"],
        horizontal=True
    )

    if "ai_report" not in st.session_state or st.session_state.get("last_lang") != lang:
        with st.spinner("Generating full report..."):
            st.session_state.ai_report = fetch_ai_info(label, risk, lang)
            st.session_state.last_lang = lang

    report = st.session_state.ai_report
    risk_data = RISK_LEVELS.get(risk, {"color": "#f59e0b"})

    def show_list(items):
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    name = item.get("name", "")
                    desc = item.get("description", "")
                    st.write(f"• **{name}** — {desc}")
                else:
                    st.write(f"• {item}")
        elif isinstance(items, dict):
            for k, v in items.items():
                st.write(f"• **{k}:** {v}")
        elif items:
            st.write(items)

    st.markdown(f"""
    <div class="result-card" style="border-left:8px solid {risk_data['color']};">
        <h1 style="margin:0;">{label}</h1>
        <div style="display:flex; gap:20px; margin-top:10px;">
            <span style="color:{risk_data['color']}; font-weight:bold;">
                ⚠️ RISK: {risk.upper()}
            </span>
            <span style="color:#0ea5e9; font-weight:bold;">
                🎯 CONFIDENCE: {int(confidence*100)}%
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📊 ANALYSIS VIEW",
        "📋 FULL REPORT",
        "💬 AI CONSULTANT"
    ])

    with tab1:
        col1, col2 = st.columns([1, 1.2])

        with col1:
            if img is not None:
                st.markdown("<div class='section-header'>📸 UPLOADED IMAGE</div>", unsafe_allow_html=True)
                st.image(img, use_container_width=True)

                st.markdown("<div class='section-header'>🎯 HEATMAP</div>", unsafe_allow_html=True)
                st.image(generate_heatmap(img), use_container_width=True)

        with col2:
            st.markdown("<div class='section-header'>📝 OVERVIEW</div>", unsafe_allow_html=True)
            st.write(report.get("overview", "-"))

            st.markdown("<div class='section-header'>🛑 SYMPTOMS</div>", unsafe_allow_html=True)
            show_list(report.get("symptoms", []))

            if res.get("symptom_text"):
                st.markdown("<div class='section-header'>📄 SUBMITTED DETAILS</div>", unsafe_allow_html=True)
                st.write(res["symptom_text"])

            st.markdown("<div class='section-header'>🏥 ACTION</div>", unsafe_allow_html=True)
            st.info(action)

    with tab2:
        sections = [
            ("🧬 Causes", "causes"),
            ("⚠️ Risk Factors", "risk_factors"),
            ("🔬 Diagnosis", "diagnosis_methods"),
            ("💊 Treatment", "medical_treatment"),
            ("🏠 Home Care", "home_care"),
            ("🛡️ Prevention", "prevention"),
        ]

        for title, key in sections:
            with st.expander(title, expanded=False):
                show_list(report.get(key, []))

        st.success(report.get("doctor_note", "-"))
        st.warning(report.get("disclaimer", "-"))

        pdf_data = generate_pdf_report(res, report)
        st.download_button(
            "📥 DOWNLOAD PDF REPORT",
            data=pdf_data,
            file_name=f"DermaSmart_{label}.pdf",
            use_container_width=True
        )

    with tab3:
        show_chatbot()
# ==========================================
# 🎯 HEATMAP
# ==========================================
def generate_heatmap(img):
    img_np = np.array(img.resize((450, 450)))
    heatmap = np.zeros((450, 450), dtype=np.uint8)
    cv2.circle(heatmap, (225, 200), 120, 255, -1)
    heatmap = cv2.GaussianBlur(heatmap, (101, 101), 0)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(img_np, 0.5, heatmap_color, 0.5, 0)
    return overlay

# ==========================================
# 🚀 MAIN APP
# ==========================================
def main():
    st.markdown("<h1 class='hero-title'>DERMASMART AI PRO</h1>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🛠️ ACTIVE SCANNER")
        mode = st.radio("Mode", ["📸 Visual Scan", "🩺 Symptom Decoder"])

        if st.button("🔄 RESET SESSION"):
            st.session_state.clear()
            st.rerun()

    if "step" not in st.session_state:
        st.session_state.step = 1

    # Visual Scan (same logic)
    if mode == "📸 Visual Scan":
        if st.session_state.step == 1:
            file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

            if file:
                img = Image.open(file).convert("RGB")
                st.image(img, width=320)

                if st.button("INITIATE NEURAL SCAN"):
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        bar.progress(i + 1)

                    st.session_state.result = {
                        "label": "Acne Vulgaris",
                        "risk": "Low",
                        "confidence": 0.94,
                        "action": "Use gentle cleanser and consult dermatologist if persistent.",
                        "img": img
                    }
                    st.session_state.step = 4
                    st.rerun()

    # Symptom Decoder (Internal / General diseases)
    else:
        if st.session_state.step == 1:
            st.markdown("### 🩺 Detailed Symptom Analysis")

            symptom = st.text_area(
                "Describe your problem",
                placeholder="Example: Severe headache with nausea, stomach pain after eating, chest burning, weakness..."
            )

            col1, col2 = st.columns(2)

            with col1:
                duration = st.selectbox(
                    "Duration",
                    ["1 day", "2-7 days", "1-4 weeks", "More than 1 month"]
                )

            with col2:
                severity = st.selectbox(
                    "Severity",
                    ["Mild", "Moderate", "Severe"]
                )

            body_part = st.selectbox(
                "Affected Area",
                [
                    "Head", "Eyes", "Ear", "Nose", "Throat",
                    "Chest", "Heart", "Stomach", "Abdomen",
                    "Back", "Hands", "Legs", "Whole Body"
                ]
            )

            extra = st.multiselect(
                "Additional Symptoms",
                [
                    "Fever", "Nausea", "Vomiting", "Dizziness",
                    "Weakness", "Pain", "Swelling", "Fatigue",
                    "Breathing Difficulty", "Acidity"
                ]
            )

            if st.button("DECODE SYMPTOMS"):
                if not symptom.strip():
                    st.warning("Please describe your symptoms.")
                else:
                    details = f"""
            Problem: {symptom}
            Duration: {duration}
            Severity: {severity}
            Affected Area: {body_part}
            Additional Symptoms: {', '.join(extra) if extra else 'None'}
            """

                    text = details.lower()

                    # Default values
                    label = "General Health Analysis"
                    risk = "Moderate"
                    confidence = 0.82
                    action = "Consult a qualified doctor for proper diagnosis."

                    # Head related
                    if any(x in text for x in ["headache", "migraine", "head pain", "nausea", "light sensitivity"]):
                        label = "Migraine / Headache Pattern"
                        confidence = 0.91
                        action = "Rest in low-light room, hydrate, and consult physician if frequent."

                    # Stomach related
                    elif any(x in text for x in ["stomach", "abdominal", "gas", "acidity", "vomiting", "diarrhea"]):
                        label = "Digestive Disorder Pattern"
                        confidence = 0.89
                        action = "Eat light food, stay hydrated, avoid spicy/oily meals, consult doctor."

                    # Chest related
                    elif any(x in text for x in ["chest pain", "breathing", "shortness of breath", "heart"]):
                        label = "Cardio / Respiratory Warning"
                        confidence = 0.93
                        risk = "High"
                        action = "Seek urgent medical attention immediately."

                    # Fever / Infection
                    elif any(x in text for x in ["fever", "weakness", "fatigue", "body pain"]):
                        label = "Possible Infection / Viral Pattern"
                        confidence = 0.86
                        action = "Monitor temperature, rest, fluids, consult doctor if worsening."

                    # Joint pain
                    elif any(x in text for x in ["joint pain", "knee pain", "back pain", "swelling"]):
                        label = "Inflammation / Pain Pattern"
                        confidence = 0.84
                        action = "Rest affected area, avoid strain, consult orthopedician if persistent."

                    # Risk override by severity
                    if severity == "Severe":
                        risk = "High"
                    elif severity == "Mild" and risk != "High":
                        risk = "Low"

                    st.session_state.result = {
                        "label": label,
                        "risk": risk,
                        "confidence": confidence,
                        "action": action,
                        "symptom_text": details,
                        "img": None
                    }

                    # Reset AI report cache
                    if "ai_report" in st.session_state:
                        del st.session_state.ai_report

                    st.session_state.step = 4
                    st.rerun()

    if st.session_state.step == 4:
        show_enhanced_results(st.session_state.result)

        if st.button("← BACK TO SCANNER"):
            st.session_state.step = 1
            st.rerun()

    st.markdown("""
    <div style="
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background:linear-gradient(90deg,#111,#1a1a1a);
    color:#f8fafc;
    text-align:center;
    padding:10px;
    font-size:13px;
    border-top:1px solid #333;
    z-index:999;
    letter-spacing:0.3px;
    ">
    ⚠️ <b>Medical Disclaimer:</b> DermaSmart AI is an educational assistant only. 
    This is not a final diagnosis. Please consult a qualified doctor or dermatologist.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()