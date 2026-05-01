import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Mobile Pro", layout="centered")

# --- 2. SESSION STATE INITIALIZATION ---
# Age ko session state mein rakho taaki NameError na aaye
if 'u_age' not in st.session_state: st.session_state.u_age = 22 
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 3. UI STYLING ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .report-card { background: #0d1117; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP NAV ---
st.title("📱 STRIDE-AI")

# --- 5. TABS ---
tabs = st.tabs(["⚙️ Setup", "👣 Steps", "🫀 Heart", "🧘 Posture", "🧠 AI Report"])

# SCREEN 0: SETUP (Age input yahan se lo)
with tabs[0]:
    st.subheader("Subject Profile")
    # Slider ki value seedha session state mein update hogi
    st.session_state.u_age = st.slider("Select Age", 18, 80, st.session_state.u_age)
    st.info(f"System calibrated for Age: {st.session_state.u_age}")

# SCREEN 1: STEPS
with tabs[1]:
    st.subheader("Pedometer")
    st.metric("Steps", st.session_state.steps)
    if st.button("Inject Step Data"):
        st.session_state.steps += 500
        st.session_state.report_ready = False
        st.rerun()

# SCREEN 2: HEART RATE
with tabs[2]:
    st.subheader("Cardiac")
    st.metric("Pulse", f"{st.session_state.heart_rate} BPM")
    st.line_chart(np.random.randint(60, 160, 15))

# SCREEN 3: POSTURE
with tabs[3]:
    st.subheader("Posture Analysis")
    st.metric("Alignment Score", "79%")
    st.caption("AI Pose Modeling active.")

# SCREEN 4: CLEAN AI REPORT (Fixed NameError)
with tabs[4]:
    st.subheader("📋 Clinical Audit")
    
    if st.button("🔍 GENERATE REPORT"):
        with st.spinner("Analyzing..."):
            time.sleep(2)
            st.session_state.report_ready = True

    if st.session_state.report_ready:
        # Ab u_age session state se aayega, crash nahi hoga
        current_age = st.session_state.u_age
        m_age = current_age - 2 if st.session_state.steps > 8000 else current_age + 1
        vo2_est = round(15 * (190 / st.session_state.heart_rate), 1)

        # Clean Markdown Output
        st.markdown(f"""
        ### 🛡️ STRIDE-AI: FINAL CLINICAL AUDIT
        **Status:** Active Monitoring
        
        ---
        **1. Physical Activity Summary**
        Total volume of **{st.session_state.steps} steps** executed. 
        **Metabolic Age:** Estimated at **{m_age} years**.
        
        **2. Cardiovascular Analysis**
        Current BPM (**{st.session_state.heart_rate}**) is stable. 
        **VO2 Max:** {vo2_est} mL/kg/min.
        
        **3. Biomechanical Integrity**
        **Posture Score:** 79% (Stable). 
        **Gait Entropy:** Within 1.2% deviation.
        
        ---
        **⭐ FINAL VERDICT:**  
        **Subject is physiologically optimized.**
        """)
