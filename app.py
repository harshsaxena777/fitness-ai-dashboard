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
    st.toast("Hard Resetting... Sensors Recalibrated", icon="🔥")
    time.sleep(1)
    st.rerun()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'history' not in st.session_state: st.session_state.history = []
if 'report_generated' not in st.session_state: st.session_state.report_generated = False

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Portal")
    email = st.text_input("User Email", placeholder="harsh.saxena@srms.ac.in")
    if st.button("Access Dashboard"):
        if "@" in email:
            st.session_state.logged_in = True
            st.session_state.user_mail = email
            st.rerun()
    st.stop()

# --- 3. UI STYLING ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.8em; font-weight: bold; background: #3b82f6; color: white; border: none; }
    .report-box { background: #0d1117; padding: 25px; border-radius: 18px; border-left: 10px solid #3b82f6; }
    .metric-card { background: #1e293b; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #334155; }
    .profile-card { background: #0f172a; padding: 15px; border-radius: 12px; border: 1px dashed #3b82f6; }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP NAV ---
c_title, c_reboot = st.columns([5, 1])
with c_title:
    st.title("📱 STRIDE-AI Pro")
with c_reboot:
    if st.button("🔄"): reboot_system()

# --- 5. MODULAR TABS ---
tabs = st.tabs(["⚙️ Profiling", "👣 Stride", "🫀 Cardiac", "🧘 Posture", "🧠 AI Analytics"])

# SCREEN 1: DETAILED PROFILING (Upgraded)
with tabs[0]:
    st.subheader("🧬 Advanced Medical Profiling")
    
    with st.container():
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            u_age = st.slider("Current Age", 18, 90, 22, key="u_age")
            u_gender = st.selectbox("Biological Gender", ["Male", "Female", "Other"])
            u_weight = st.number_input("Weight (kg)", 40.0, 150.0, 70.0)
        with col_p2:
            u_height = st.number_input("Height (cm)", 120.0, 220.0, 175.0)
            u_goal = st.selectbox("Clinical Objective", ["Recovery", "Fat Loss", "Elite Conditioning", "Strength"])
            u_activity = st.select_slider("Baseline Activity Level", options=["Sedentary", "Moderate", "Active", "Athlete"])
        
        # Real-time BMI Calculation
        bmi = round(u_weight / ((u_height/100)**2), 1)
        st.markdown(f"**Current BMI:** `{bmi}` | **Health Category:** `{'Normal' if 18.5 <= bmi <= 24.9 else 'Seek Advice'}`")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.write("### 🎯 Physiological Targets")
    t_min = int((220 - u_age) * 0.6)
    t_max = int((220 - u_age) * 0.8)
    st.info(f"Based on your profile, your **Optimal Aerobic Zone** is {t_min} - {t_max} BPM. System calibrated for {u_goal}.")

# SCREEN 2: INTERACTIVE STRIDE (Upgraded)
with tabs[1]:
    st.subheader("👣 Live Kinetic Telemetry")
    
    # Progress towards a dynamic goal
    daily_goal = 10000 if u_goal != "Recovery" else 5000
    progress = min(st.session_state.steps / daily_goal, 1.0)
    
    # Big Animated Metric
    st.markdown(f"""<div class='metric-card'>
        <p style='margin:0; opacity:0.6; font-size: 0.9rem;'>SESSION KINETIC VOLUME</p>
        <h1 style='color: #60a5fa; margin:0; font-size: 3.5rem;'>{st.session_state.steps}</h1>
        <p style='margin:0; font-size: 0.8rem;'>Goal Progress: {int(progress*100)}%</p>
    </div>""", unsafe_allow_html=True)
    st.progress(progress)

    st.write("### Movement Diagnostics")
    c_m1, c_m2, c_m3 = st.columns(3)
    dist = round(st.session_state.steps * 0.00076, 2)
    kcal = int(st.session_state.steps * 0.04)
    c_m1.metric("Distance (km)", dist)
    c_m2.metric("Energy (kcal)", kcal)
    c_m3.metric("Cadence (spm)", "114" if st.session_state.steps > 0 else "0")

    # Inject Sensor Data
    if st.button("🛰️ INJECT SENSOR PACKET"):
        st.session_state.steps += np.random.choice([7, 12, 18])
        st.session_state.heart_rate = np.random.randint(105, 150)
        st.session_state.history.append({
            "steps": st.session_state.steps, 
            "hr": st.session_state.heart_rate,
            "dist": dist,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        st.session_state.report_generated = False
        st.rerun()

# SCREEN 3: CARDIAC
with tabs[2]:
    st.subheader("🫀 Cardiac Telemetry")
    st.metric("Live Pulse", f"{st.session_state.heart_rate} BPM")
    st.line_chart(pd.DataFrame(np.random.normal(st.session_state.heart_rate, 2, 20)), color="#ef4444")

# SCREEN 4: POSTURE
with tabs[3]:
    st.subheader("🧘 Biomechanical Integrity")
    base_alignment = 96 - (u_age * 0.25)
    p_score = int(base_alignment + np.random.randint(-2, 2))
    st.metric("Spinal Alignment Score", f"{p_score}%")
    st.progress(p_score/100)
    
    st.write("### Joint Segment Analysis")
    joint_data = pd.DataFrame({
        'Segment': ['Cervical', 'Thoracic', 'Lumbar', 'Pelvic'],
        'Deviation': [1.2, 2.5 + (u_age*0.04), 1.8 + (u_age*0.06), 2.1]
    })
    st.bar_chart(joint_data, x='Segment', y='Deviation', color="#3b82f6")

# SCREEN 5: AI ANALYTICS
with tabs[4]:
    st.subheader("🧠 Clinical Decision Support System")
    
    if st.button("🔍 CONDUCT FULL KINETIC AUDIT"):
        with st.spinner("Analyzing Bio-Kinetic History..."):
            time.sleep(2)
            st.session_state.report_generated = True

    if st.session_state.report_generated:
        vo2_est = round((45 if u_gender == "Male" else 38) - (u_age * 0.15), 1)
        m_age = u_age - 3 if st.session_state.steps > 8000 else u_age + 2
        
        st.markdown(f"""
### 🛡️ STRIDE-AI: CLINICAL AUDIT REPORT
**Identification:** {u_gender} | {u_age}Y | BMI: {bmi}  
**Goal:** {u_goal} | **Packets Analyzed:** {len(st.session_state.history)}

---

#### 1. Activity Trends & Metabolic Health
- **Total Volume:** {st.session_state.steps} steps. Trend is **{'Optimal' if progress > 0.5 else 'Sub-Optimal'}**.
- **Metabolic Age:** Current cellular efficiency matches a **{m_age} year old**.

#### 2. Cardiovascular Intelligence
- **Observed Pulse:** {st.session_state.heart_rate} BPM.  
- **VO2 Max:** **{vo2_est} mL/kg/min** (Predicted).

#### 3. Verdict & Future Plan
- **Posture:** {p_score}% stability. No immediate risk.
- **AI Recommendation:** Based on your {u_goal} goal, keep heart rate between {t_min}-{t_max} BPM.
- **Verdict:** Subject is **Physiologically Optimized**.

---
        """)
        
        report_txt = f"STRIDE-AI AUDIT\nSteps: {st.session_state.steps}\nBMI: {bmi}\nVerdict: Optimized"
        st.download_button("📥 DOWNLOAD CLINICAL AUDIT", report_txt, file_name=f"Audit_{u_age}Y.txt")
    else:
        st.info("System Standby. Click 'Conduct Full Kinetic Audit' for diagnosis.")
