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

# SCREEN 5: AI ANALYTICS (FIXED FORMATTING)
with tabs[4]:
    st.subheader("📋 AI Clinical Engine")
    
    # Diagnosis Trigger Button
    if st.button("🔍 START COMPREHENSIVE DIAGNOSIS"):
        with st.spinner("Analyzing Bio-Kinetic Patterns..."):
            time.sleep(2)
            st.session_state.report_generated = True

    # Report logic - Sirf tab chalegi jab button click ho
    if st.session_state.report_generated:
        # --- 1. DYNAMIC CALCULATIONS ---
        # VO2 Max Estimate based on Gender & Age
        vo2_base = 45 if u_gender == "Male" else 38
        vo2_est = round(vo2_base - (u_age * 0.15), 1)
        
        # Metabolic Age logic
        m_age = u_age - 2 if st.session_state.steps > 7000 else u_age + 1
        
        # Posture Advice based on Score & Age
        if p_score < 80:
            posture_advice = "High risk of lumbar strain. Suggest immediate ergonomic adjustments."
        else:
            posture_advice = "Posture is within optimal clinical range for your age group."

        # Goal Progress logic
        if u_goal == "Fat Loss" and st.session_state.steps < 5000:
            goal_verdict = "Low activity detected for Fat Loss goal. Increase step count."
        elif u_goal == "Elite Training" and st.session_state.heart_rate < 120:
            goal_verdict = "Cardiac intensity is below elite threshold. Increase pace."
        else:
            goal_verdict = "Activity metrics are aligning well with your stated objective."

        # --- 2. CLEAN MARKDOWN DISPLAY (No HTML Tags) ---
        st.markdown(f"""
        ### 🛡️ STRIDE-AI: CLINICAL AUDIT REPORT
        **User Profile:** {u_gender} | {u_age} Years | {u_weight} kg  
        **Status:** {goal_verdict}
        
        ---
        
        #### 1. 👣 Activity & Metabolic Analysis
        - **Total Steps:** {st.session_state.steps} 
        - **Metabolic Age:** Your body is functioning like a **{m_age} year old**.
        - **Trend:** Analysis of previous sensor packets shows a steady kinetic volume.
        
        #### 2. 🫀 Cardiovascular Intelligence
        - **Current Heart Rate:** {st.session_state.heart_rate} BPM
        - **Estimated VO2 Max:** **{vo2_est} mL/kg/min**
        - **Cardiac Risk:** LOW (Stable sinus rhythm simulated).
        
        #### 3. 🧘 Biomechanical Integrity
        - **Posture Score:** {p_score}%
        - **AI Observation:** {posture_advice}
        - **History Check:** Spinal alignment has been consistent across your last {len(st.session_state.history)} syncs.
        
        ---
        
        **⭐ FINAL CLINICAL VERDICT:**  
        **Subject is physiologically stable.** No anomalies detected in gait or cardiac rhythm. Maintain current hydration and step frequency.
        """)
        
        # --- 3. DOWNLOAD OPTION ---
        report_txt = f"STRIDE-AI CLINICAL REPORT\n" \
                     f"User: {u_gender}, {u_age}y\n" \
                     f"Steps: {st.session_state.steps}\n" \
                     f"VO2 Max: {vo2_est}\n" \
                     f"Verdict: Optimized"
        
        st.download_button(
            label="📥 DOWNLOAD CLINICAL REPORT (.TXT)",
            data=report_txt,
            file_name=f"StrideAI_{u_gender}_{u_age}.txt",
            mime="text/plain"
        )
    else:
        st.info("System Ready. Please initiate diagnosis to generate the clinical audit.")
