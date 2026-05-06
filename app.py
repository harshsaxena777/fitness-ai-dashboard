import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro", layout="centered")

def reboot_system():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("Rebooting System... Sensors Recalibrated", icon="🔄")
    time.sleep(1)
    st.rerun()

# --- 2. SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'history' not in st.session_state: st.session_state.history = []
if 'report_generated' not in st.session_state: st.session_state.report_generated = False # Trigger control

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Portal")
    email = st.text_input("User Email")
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

# SCREEN 1: DETAILED PROFILING
with tabs[0]:
    st.subheader("Medical Setup")
    u_age = st.slider("Age", 18, 90, 22, key="age_input")
    u_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gen_input")
    u_weight = st.number_input("Weight (kg)", 40, 150, 70, key="wt_input")
    u_goal = st.selectbox("Daily Goal", ["Recovery", "Fat Loss", "Elite Training"], key="goal_input")
    st.info(f"System calibrated for {u_gender}, {u_age}y. Current Goal: {u_goal}")

# SCREEN 2: INTERACTIVE STRIDE
with tabs[1]:
    st.subheader("Pedometer")
    st.metric("Steps Today", st.session_state.steps)
    if st.button("🛰️ INJECT SENSOR PACKET"):
        inc = np.random.choice([7, 12, 18])
        st.session_state.steps += inc
        st.session_state.heart_rate = np.random.randint(95, 155)
        st.session_state.history.append({"steps": st.session_state.steps, "hr": st.session_state.heart_rate})
        st.session_state.report_generated = False # Reset report on new data
        st.rerun()

# SCREEN 3: CARDIAC
with tabs[2]:
    st.subheader("Cardiac Performance")
    st.metric("Live Pulse", f"{st.session_state.heart_rate} BPM")
    st.line_chart(np.random.randint(70, 160, 20))

# SCREEN 4: POSTURE
with tabs[3]:
    st.subheader("Posture Analysis")
    # Age-based logic: Older age = lower stability
    p_score = int(95 - (u_age * 0.2)) if u_age < 50 else int(85 - (u_age * 0.3))
    st.metric("Alignment Score", f"{p_score}%")
    st.progress(p_score/100)

# SCREEN 5: AI ANALYTICS (FIXED TRIGGER)
with tabs[4]:
    st.subheader("📋 AI Clinical Engine")
    
    # Ye button trigger banega
    if st.button("🔍 START COMPREHENSIVE DIAGNOSIS"):
        with st.spinner("Analyzing Bio-Kinetic Patterns..."):
            time.sleep(2)
            st.session_state.report_generated = True

    # Report sirf tab dikhegi jab 'report_generated' True hoga
    if st.session_state.report_generated:
        # 1. Custom Advice based on Age
        age_advice = "Focus on mobility and joint health." if u_age > 50 else "High-intensity metabolic conditioning is safe."
        
        # 2. Gender specific VO2 Logic (Simulated)
        vo2_base = 45 if u_gender == "Male" else 38
        vo2_est = round(vo2_base - (u_age * 0.15), 1)

        # 3. Goal based Verdict
        goal_status = "On Track" if (u_goal == "Fat Loss" and st.session_state.steps > 500) else "Incomplete"
        
        st.markdown(f"""
        <div class='report-box'>
            <h3 style='color:#3b82f6;'>STRIDE-AI CLINICAL AUDIT</h3>
            <p><b>User Profile:</b> {u_gender} | {u_age} Years | {u_weight} kg</p>
            <hr style='opacity:0.2;'>
            
            **1. HISTORICAL ASSESSMENT:**
            - **Activity Level:** {st.session_state.steps} steps executed. Trend is <i>{goal_status}</i> for {u_goal}.
            - **Cardiac Baseline:** Estimated VO2 Max for a {u_age}y {u_gender} is **{vo2_est}**.
            
            **2. POSTURE & BIOMECHANICS:**
            - **Current Stability:** {p_score}%. 
            - **Observation:** {age_advice}
            
            **3. AI PROJECTION & HISTORY:**
            - Analysis of pichle {len(st.session_state.history)} sensor packets shows heart rate stabilization at {st.session_state.heart_rate} BPM.
            - **Recommendation:** Increase step cadence by 10% to meet your {u_goal} target.
            
            <hr style='opacity:0.2;'>
            <p style='color:#00ffbd; font-weight:bold;'>FINAL VERDICT: Subject is stable. No immediate clinical risk detected.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download Option
        report_txt = f"STRIDE-AI REPORT\nUser: {u_gender}, {u_age}y\nSteps: {st.session_state.steps}\nVerdict: {goal_status}"
        st.download_button("📥 DOWNLOAD CLINICAL PDF (TXT)", report_txt, file_name=f"Report_{u_gender}_{u_age}.txt")
    else:
        st.info("Please initiate the diagnostic engine to view clinical insights.")
