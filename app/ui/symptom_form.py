import streamlit as st

def get_symptoms(image_uploaded=False):
    """
    Enhanced Interactive Neural Symptom Form
    """
    if not image_uploaded:
        return {}

    # =========================
    # 🎨 FORM CUSTOM CSS
    # =========================
    st.markdown("""
    <style>
        /* Container for grouping checkboxes */
        .symptom-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }
        
        /* Custom styling for selectbox and radio labels */
        .stSelectbox label, .stRadio label {
            color: #38bdf8 !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.8rem !important;
            letter-spacing: 1px;
        }

        /* Making checkboxes look more integrated */
        .stCheckbox {
            background: rgba(255, 255, 255, 0.03);
            padding: 10px;
            border-radius: 12px;
            border: 1px solid rgba(56, 189, 248, 0.1);
            transition: 0.3s;
        }
        .stCheckbox:hover {
            border-color: #38bdf8;
            background: rgba(56, 189, 248, 0.05);
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color:#38bdf8; font-family:Syncopate; font-size:1.1rem;'>🧬 SENSORY MARKERS</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.8rem; margin-top:-10px;'>Select all physical sensations currently present.</p>", unsafe_allow_html=True)

    # Use columns for a cleaner layout
    col1, col2 = st.columns(2)

    with col1:
        itching = st.checkbox("⚡ Itching", key="itch")
        redness = st.checkbox("🔴 Redness", key="red")
        dryness = st.checkbox("🍂 Dryness", key="dry")

    with col2:
        pain = st.checkbox("💥 Pain", key="pain")
        burning = st.checkbox("🔥 Burning", key="burn")
        swelling = st.checkbox("🛡️ Swelling", key="swell")

    st.markdown("<hr style='border:0.1px solid rgba(255,255,255,0.05); margin:20px 0;'>", unsafe_allow_html=True)

    # Layout for Selectors
    sel_col1, sel_col2 = st.columns(2)

    with sel_col1:
        st.markdown("<h3 style='color:#38bdf8; font-family:Syncopate; font-size:0.9rem;'>⏳ TEMPORAL FLOW</h3>", unsafe_allow_html=True)
        duration = st.selectbox(
            "Condition History:",
            ["Recent (Days)", "Persistent (Weeks/Months)"],
            label_visibility="visible"
        )

    with sel_col2:
        st.markdown("<h3 style='color:#38bdf8; font-family:Syncopate; font-size:0.9rem;'>🎯 INTENSITY</h3>", unsafe_allow_html=True)
        severity = st.select_slider(
            "Neural Severity Level:",
            options=["Mild", "Moderate", "Critical"],
            value="Moderate"
        )

    # Mapping readable values back to logic
    duration_val = "short" if "Recent" in duration else "long"
    severity_val = severity.lower()

    return {
        "itching": itching,
        "pain": pain,
        "redness": redness,
        "dryness": dryness,
        "burning": burning,
        "swelling": swelling,
        "duration": duration_val,
        "severity": severity_val
    }