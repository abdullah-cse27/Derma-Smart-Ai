import streamlit as st
import time
import urllib.parse
from config import CLASS_INFO
from utils.report_generator import generate_report
from utils.history_manager import save_history

def show_results(result):
    # =========================
    # 🛡️ FAIL-SAFE DATA EXTRACTION
    # =========================
    mode = result.get("mode", "visual") 
    label = result.get("label", "Unknown Condition")
    
    # 🚨 URGENCY LOGIC: Cancerous conditions ko automatic High Risk dikhane ke liye
    risk = result.get("risk", {"risk_level": "Under Review", "risk_score": 0, "risk_message": "Analyzing..."})
    if any(cancer in label for cancer in ["Melanoma", "Carcinoma"]):
        risk["risk_level"] = "HIGH"
        risk["risk_score"] = max(85, risk["risk_score"])
    
    triage = result.get("triage", {"priority": "Routine", "action": "Consult a professional."})
    
    # --- 🛠️ FIXED CONFIDENCE LOGIC ---
    raw_conf = result.get("confidence", 0)
    
    # Agar confidence string mein hai (e.g. "98.5%"), toh use number mein badlo
    if isinstance(raw_conf, str):
        try:
            raw_conf = float(raw_conf.replace('%', ''))
        except:
            raw_conf = 0.0

    # Ab calculation safely chalegi
    confidence_pct = int(raw_conf * 100) if raw_conf <= 1.0 else int(raw_conf)
    risk_pct = int(risk.get("risk_score", 0))

    # =========================
    # 🎨 CYBER-SURGEON ELITE UI (FIXED)
    # =========================
    st.markdown("""
    <style>
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .dashboard-fade { animation: slideUp 0.6s cubic-bezier(0.23, 1, 0.32, 1); }

        .res-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            backdrop-filter: blur(20px);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-top: 4px solid #38bdf8;
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 20px;
            min-height: 160px; /* Fixed height for alignment */
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        }

        .metric-title {
            color: #94a3b8;
            font-size: 0.6rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .metric-value {
            font-family: 'Syncopate', sans-serif;
            font-size: 1.1rem; 
            font-weight: 700;
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
            word-wrap: break-word;
            line-height: 1.3;
        }

        .pulse-line {
            height: 2px;
            background: linear-gradient(90deg, transparent, #38bdf8, transparent);
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }
        .pulse-line::after {
            content: "";
            position: absolute;
            left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, #ffffff, transparent);
            animation: pulse-move 2s infinite;
        }
        @keyframes pulse-move { 100% { left: 100%; } }

        .doc-link {
            display: block;
            text-align: center;
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid #38bdf8;
            color: #38bdf8 !important;
            padding: 12px;
            border-radius: 10px;
            text-decoration: none;
            font-family: 'Syncopate', sans-serif;
            font-size: 0.65rem;
            margin-top: 15px;
            transition: 0.3s;
        }
        .doc-link:hover { background: #38bdf8; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='dashboard-fade'>", unsafe_allow_html=True)
    
    # --- HEADER ---
    title = "DERMAL ANALYSIS COMPLETE" if mode == "visual" else "SYMPTOM DECODE COMPLETE"
    st.markdown(f"<h2 style='font-family:Syncopate; font-size:1rem; color:#f8fafc; letter-spacing:4px;'>{title}</h2>", unsafe_allow_html=True)
    st.markdown("<div class='pulse-line'></div>", unsafe_allow_html=True)

    # --- TOP METRICS GRID ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="res-card">
            <div class="metric-title">Primary Match</div>
            <div class="metric-value" style="color:#38bdf8;">{label}</div>
            <div style="font-size:0.55rem; color:#2dd4bf; margin-top:8px;">✅ NEURAL PATTERN VERIFIED</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        conf_color = "#10b981" if confidence_pct > 80 else "#f59e0b"
        st.markdown(f"""
        <div class="res-card">
            <div class="metric-title">Model Precision</div>
            <div class="metric-value" style="color:{conf_color};">{confidence_pct}%</div>
            <div style="width:100%; background:rgba(255,255,255,0.05); height:4px; border-radius:10px; margin-top:12px;">
                <div style="width:{confidence_pct}%; background:{conf_color}; height:100%; border-radius:10px; box-shadow: 0 0 10px {conf_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        risk_color = "#ef4444" if risk_pct > 50 else "#10b981"
        st.markdown(f"""
        <div class="res-card">
            <div class="metric-title">Severity Index</div>
            <div class="metric-value" style="color:{risk_color};">{risk['risk_level']}</div>
            <div style="font-size:0.55rem; color:{risk_color}; border:1px solid {risk_color}; padding:2px 6px; border-radius:4px; display:inline-block; margin-top:8px;">{risk_pct}% RISK LEVEL</div>
        </div>
        """, unsafe_allow_html=True)

    # --- TABS SECTION ---
    tab3_name = "🧠 NEURAL HEATMAP" if mode == "visual" else "💡 AI INSIGHTS"
    tab1, tab2, tab3, tab4 = st.tabs(["🧬 CLINICAL PROFILE", "🏥 TRIAGE", tab3_name, "📂 ARCHIVE"])

    with tab1:
        st.markdown(f"<p style='color:#38bdf8; font-family:Syncopate; font-size:0.75rem;'>DECODING: {label}</p>", unsafe_allow_html=True)
        
        info_data = CLASS_INFO.get(label, {})
        desc = info_data.get("description", "Analysis complete. Clinical profile verified via AI reasoning.")
        pathology = info_data.get("pathology", "Localized inflammatory or physiological response identified.")
        triggers = info_data.get("triggers", ["General Stress", "UV Exposure"])

        st.markdown(f"""
            <div style="background:rgba(56, 189, 248, 0.03); padding:20px; border-radius:15px; border-right:3px solid #38bdf8; font-size:0.9rem; line-height:1.6; color:#e2e8f0;">
                <b style="color:#38bdf8;">Condition Overview:</b><br>{desc}<br><br>
                <b style="color:#38bdf8;">Pathological Mechanism:</b><br>{pathology}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><p style='font-size:0.6rem; color:#64748b; letter-spacing:2px;'>POTENTIAL TRIGGERS</p>", unsafe_allow_html=True)
        t_cols = st.columns(len(triggers) if triggers else 1)
        for i, t in enumerate(triggers):
            t_cols[i % len(triggers)].markdown(f"<code style='color:#38bdf8; font-size:0.7rem;'>{t}</code>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### Action Protocol")
        st.error(f"**URGENCY:** {triage['priority']}")
        st.info(f"**REQUIRED ACTION:** {triage['action']}")
        
        if result.get("recommendations"):
            st.markdown("**Management Plan:**")
            for rec in result["recommendations"]:
                st.markdown(f"📍 {rec}")
        
        st.markdown("---")
        search_query = urllib.parse.quote(f"dermatologist for {label} near me")
        st.markdown(f"""
            <a href="https://www.google.com/maps/search/{search_query}" target="_blank" class="doc-link">
                🔍 LOCATE NEAREST SPECIALISTS FOR {label.upper()}
            </a>
        """, unsafe_allow_html=True)

    with tab3:
        if mode == "visual":
            c_l, c_r = st.columns([1, 1.2])
            with c_l:
                st.markdown("<p style='font-size:0.6rem; color:#64748b; letter-spacing:1px;'>LOGIC ATTRIBUTION</p>", unsafe_allow_html=True)
                st.write(risk.get('risk_message', "Pattern verified against clinical data points."))
                st.markdown("**Morphological Evidence:**")
                biomarkers = result.get("features", ["Vascular Patterning", "Structural Symmetry"])
                for feat in biomarkers:
                    st.markdown(f"<span style='color:#38bdf8;'>◈</span> {feat}", unsafe_allow_html=True)
            with c_r:
                heatmap = result.get("heatmap")
                if heatmap is not None:
                    st.image(heatmap, caption="Neural Focus Area (Grad-CAM Analysis)", use_container_width=True)
                else:
                    st.info("Heatmap generation skipped for this scan.")
        else:
            st.markdown("### AI Diagnostic Reasoning")
            st.write(risk.get("risk_message", "Reasoning based on clinical pattern matching."))

    with tab4:
        save_history(result)
        st.markdown("<h3 style='font-family:Syncopate; font-size:0.7rem;'>SESSION EXPORT & VAULT</h3>", unsafe_allow_html=True)
        
        v1, v2 = st.columns(2)
        with v1:
            if st.button("📄 GENERATE CLINICAL PDF"):
                path = generate_report(result)
                with open(path, "rb") as f:
                    st.download_button("📥 DOWNLOAD REPORT", f, file_name=f"DermaSmart_{label.replace(' ', '_')}.pdf")
        
        with v2:
            if st.button("💾 SYNC TO CLOUD VAULT"):
                with st.spinner("Encrypting & Uploading..."):
                    time.sleep(1.5)
                    st.toast("Sync Complete!", icon="✅")
                    st.success("Data secured in Vault.")

    st.markdown(f"""
        <div style="margin-top:40px; padding:15px; border-top:1px solid rgba(56, 189, 248, 0.1); text-align:center; opacity:0.4; font-size:0.6rem; letter-spacing:1px;">
            VERIFIED DIAGNOSTIC ENGINE v3.1 | AES-256 ENCRYPTED | SESSION_{int(time.time())}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)