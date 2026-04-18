import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def groq_chatbot_response(user_input, result):
    # FIX: Safety check for nested keys
    label = result.get('label', 'Unknown Specimen')
    # Humne main.py mein risk ko string rakha tha, isliye direct access use karenge
    risk = result.get('risk', 'Moderate') 
    
    prompt = f"""
    Context:
    - Condition Identified: {label}
    - Risk Level: {risk}
    Assistant Protocol: Concise (max 2 lines), professional, cyber-medic persona. 
    Safety fallback: "Consult a professional if symptoms persist."
    
    User: {user_input}
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are DermaSmart AI, a high-precision medical diagnostic co-pilot."},
                      {"role": "user", "content": prompt}],
            temperature=0.4, max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "⚠️ LINK_ERROR: Secure connection interrupted. Seek physical medical advice."

def handle_chat():
    if st.session_state.chat_input_widget and st.session_state.get("result"):
        u_input = st.session_state.chat_input_widget
        result_data = st.session_state.result
        
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": u_input})
        
        # Get AI Response
        response = groq_chatbot_response(u_input, result_data)
        st.session_state.chat_history.append({"role": "bot", "content": response})
        
        # Clear input
        st.session_state.chat_input_widget = ""

def show_chatbot():
    # --- ULTRA-ENHANCED CYBER UI ---
    st.markdown("""
    <style>
        .chat-container {
            background: rgba(2, 6, 23, 0.8);
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-top: 4px solid #0ea5e9;
            border-radius: 20px;
            padding: 20px;
            margin-top: 5px;
            width: 100%;
            backdrop-filter: blur(15px);
            box-shadow: 0 0 25px rgba(14, 165, 233, 0.15);
        }
        
        .chat-history-log {
            max-height: 380px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding-right: 5px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-history-log::-webkit-scrollbar { width: 3px; }
        .chat-history-log::-webkit-scrollbar-thumb { background: #0ea5e9; border-radius: 10px; }
        
        .user-box {
            align-self: flex-end;
            background: rgba(14, 165, 233, 0.15);
            border: 1px solid rgba(14, 165, 233, 0.4);
            padding: 12px;
            border-radius: 15px 15px 0px 15px;
            margin-bottom: 12px;
            max-width: 85%;
            animation: slideInRight 0.3s ease-out;
        }
        
        .bot-box {
            align-self: flex-start;
            background: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px;
            border-radius: 15px 15px 15px 0px;
            margin-bottom: 12px;
            max-width: 85%;
            border-left: 3px solid #10b981;
            animation: slideInLeft 0.3s ease-out;
        }

        @keyframes slideInRight { from { transform: translateX(20px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        @keyframes slideInLeft { from { transform: translateX(-20px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

        .meta-txt { 
            font-family: 'Syncopate', sans-serif; 
            font-size: 0.55rem; 
            letter-spacing: 1.5px; 
            margin-bottom: 5px; 
            display: block;
            opacity: 0.7;
        }
        
        .content-txt { 
            color: #e2e8f0; 
            font-size: 0.85rem; 
            font-family: 'Space Grotesk', sans-serif;
            line-height: 1.4;
        }

        .stTextInput input {
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(14, 165, 233, 0.5) !important;
            color: #38bdf8 !important;
            border-radius: 12px !important;
            padding: 12px !important;
            font-family: 'JetBrains Mono', monospace !important;
            box-shadow: inset 0 0 10px rgba(14, 165, 233, 0.1) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    result = st.session_state.get("result", None)
    if result is None:
        st.info("Awaiting scan results to initialize Co-Pilot...")
        st.stop()

    # --- RENDER TERMINAL ---
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid rgba(14, 165, 233, 0.2); padding-bottom:10px;">
            <span style="font-family:Syncopate; font-size:0.7rem; color:#0ea5e9; font-weight:700;">🤖 CO-PILOT v4.0</span>
            <div style="height:8px; width:8px; background:#10b981; border-radius:50%; box-shadow: 0 0 10px #10b981;"></div>
        </div>
    """, unsafe_allow_html=True)

    # 1. History
    st.markdown('<div class="chat-history-log">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="user-box">
                    <span class="meta-txt" style="color:#38bdf8; text-align:right;">USER_AUTH_QUERY</span>
                    <div class="content-txt">{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="bot-box">
                    <span class="meta-txt" style="color:#10b981;">NEURAL_RESPONSE</span>
                    <div class="content-txt">{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Input
    st.text_input(
        "", 
        placeholder="Type clinical inquiry...", 
        label_visibility="collapsed",
        key="chat_input_widget",
        on_change=handle_chat
    )
    
    st.markdown('</div>', unsafe_allow_html=True)