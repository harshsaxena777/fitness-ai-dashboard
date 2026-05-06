import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro", layout="centered")

def reboot_system():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("Rebooting System... Recalibrating Sensors", icon="🔄")
    time.sleep(1)
    st.rerun()

# --- 2. SESSION STATE (Initialization) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'steps' not in st.session_state: st.session_state.steps = 0 # Start from Zero
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'history' not in st.session_state: st.session_state.history = [] # For History Tracking
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Portal")
    email = st.text_input("User Email")
    mobile = st.text_input("Mobile No.")
    if st.button("Login"):
        if "@" in email:
            st.session_state.logged_in = True
            st.session_state.user_mail = email
            st.rerun()
    st.stop()

# --- 3. UI STYLING ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .report-box { background: #0d1117; padding: 20px; border-radius: 15px; border-left: 8px solid #3b82f6; }
    .metric-container { background: #1e293b; padding: 15px; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP NAV ---
c_title, c_reboot = st.columns([4, 1])
with c_title:
    st.title("📱 STRIDE-AI Pro")
with c_reboot:
    if st.button("🔄"): reboot_system()

# --- 5. TABS ---
tabs = st.tabs(["⚙️ Profiling", "👣 Stride", "🫀 Cardiac", "🧘 Posture", "🧠 AI Analytics"])

# SCREEN 1: DETAILED SETUP (Profiling)
with tabs[0]:
    st.subheader("Medical Setup & Profiling")
    col_a, col_b = st.columns(2)
    with col_a:
        u_age = st.slider("Age", 18, 90, 22, key="age_slider")
        u_weight = st.number_input("Weight (kg)", 40, 150, 70)
    with col_b:
        u_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        u_goal = st.selectbox("Daily Goal", ["Recovery", "Fat Loss", "Elite Athlete"])
    
    st.info(f"Target Zone: {int((220-u_age)*0.7)} - {int((220-u_age)*0.85)} BPM")

# SCREEN 2: INTERACTIVE STRIDE (Steps)
with tabs[1]:
    st.subheader("Interactive Pedometer")
    
    # Big Step Counter
    st.markdown(f"""<div class='metric-container'>
        <h1 style='color: #3b82f6; font-size: 3rem;'>{st.session_state.steps}</h1>
        <p>TOTAL STEPS TODAY</p>
    </div>""", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Distance", f"{round(st.session_state.steps * 0.0008, 2)} km")
    c2.metric("Speed", "5.2 km/h" if st.session_state.steps > 0 else "0 km/h")
    c3.metric("Cadence", "110 spm" if st.session_state.steps > 100 else "0")

    # Inject Data with 7, 12, 18 Logic
    if st.button("🛰️ INJECT SENSOR PACKET"):
        inc = np.random.choice([7, 12, 18])
        st.session_state.steps += inc
        st.session_state.heart_rate = np.random.randint(90, 150)
        # Store in history for AI analysis
        st.session_state.history.append({"steps": st.session_state.steps, "hr": st.session_state.heart_rate, "time": datetime.now()})
        st.rerun()

# SCREEN 3: CARDIAC SECTION
with tabs[2]:
    st.subheader("Cardiovascular Intelligence")
    st.metric("Live Pulse", f"{st.session_state.heart_rate} BPM")
    
    # Real-time Waveform Chart
    chart_data = pd.DataFrame(np.random.normal(st.session_state.heart_rate, 2, 20), columns=['Pulse'])
    st.line_chart(chart_data)
    
    st.markdown("---")
    st.write("⏱️ **HRV (Heart Rate Variability):** 45ms (Optimal Recovery)")

# SCREEN 4: POSTURE (Age Significant Changes)
with tabs[3]:
    st.subheader("Biomechanical Posture Analysis")
    
    # Age-based logic: Older age = more curvature risk
    base_score = 95
    age_penalty = (u_age - 20) * 0.4 if u_age > 20 else 0
    p_score = int(base_score - age_penalty + np.random.randint(-3, 3))
    
    col_p1, col_p2 = st.columns(2)
    col_p1.metric("Alignment Score", f"{p_score}%")
    
    if p_score < 80:
        col_p2.warning("Kyphosis Risk Detected")
    else:
        col_p2.success("Neutral Spine Confirmed")
    
    # Pose Viz (Simple Bar Chart)
    angles = pd.DataFrame({'Joint': ['Neck', 'Shoulder', 'Hips', 'Knee'], 'Angle Deviation': [2, 5, 1, 3]})
    st.bar_chart(angles, x='Joint', y='Angle Deviation')

# SCREEN 5: ADVANCED AI REPORT (History + Future Plan)
with tabs[4]:
    st.subheader("📋 Advanced Clinical Diagnosis")
    
    if st.button("🔍 ANALYZE HISTORY & GENERATE REPORT"):
        with st.spinner("Processing Longitudinal Data..."):
            time.sleep(2)
            st.session_state.report_ready = True

    if st.session_state.report_ready:
        # History Analysis
        avg_hr = np.mean([h['hr'] for h in st.session_state.history]) if st.session_state.history else st.session_state.heart_rate
        trend = "Improving" if st.session_state.steps > 5000 else "Sedentary"
        
        st.markdown(f"""
        <div class='report-box'>
            <h3 style='color:#3b82f6;'>STRIDE-AI CLINICAL AUDIT v18.0</h3>
            
            **1. HISTORICAL DATA ASSESSMENT:**
            - **Activity Trend:** Based on previous {len(st.session_state.history)} packets, your trend is **{trend}**.
            - **Cardiac Baseline:** Your average heart rate under load is **{int(avg_hr)} BPM**.
            
            **2. CURRENT BIOMETRICS:**
            - **Steps:** {st.session_state.steps} | **Posture Score:** {p_score}%
            - **VO2 Max:** {round(15 * (190/st.session_state.heart_rate), 1)} (Predicted)
            
            **3. AI FUTURE RECOMMENDATION:**
            - **Short-term:** Your steps are currently {st.session_state.steps}/10000. Increase frequency to avoid metabolic stagnation.
            - **Posture Fix:** Since your Alignment is {p_score}%, we suggest 5 mins of lumbar stretching every 2 hours.
            - **Caution:** Your {u_age} year old physiology shows spikes in BPM. Avoid heavy caffeine before next sync.
            
            <hr style='opacity:0.2;'>
            <p style='color:#00ffbd; font-weight:bold;'>VERDICT: Subject is physiologically stable but requires increased kinetic volume.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # DOWNLOAD LOGIC
        report_text = f"STRIDE-AI CLINICAL REPORT\nDate: {datetime.now()}\nSteps: {st.session_state.steps}\nBPM: {st.session_state.heart_rate}\nVerdict: Stable"
        st.download_button("📥 DOWNLOAD AUDIT REPORT", report_text, file_name="StrideAI_Clinical_Report.txt")
