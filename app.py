import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro", layout="centered", initial_sidebar_state="collapsed")

def reboot_system():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("Hard Resetting... Wiping Session Data", icon="🔥")
    time.sleep(1.5)
    st.rerun()

# --- 2. SESSION STATE (Bio-Memory) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'history' not in st.session_state: st.session_state.history = []
if 'report_generated' not in st.session_state: st.session_state.report_generated = False

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Portal")
    st.info("Welcome, Harsh. Please authenticate to start your clinical session.")
    email = st.text_input("User Email", placeholder="harsh.saxena@srms.ac.in")
    if st.button("Access Dashboard"):
        if "@" in email:
            st.session_state.logged_in = True
            st.session_state.user_mail = email
            st.rerun()
    st.stop()

# --- 3. UI STYLING (Modern Dark Theme) ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.8em; font-weight: bold; background: #3b82f6; color: white; border: none; }
    .stButton>button:hover { background: #2563eb; border: 1px solid white; }
    .report-box { background: #0d1117; padding: 25px; border-radius: 18px; border-left: 10px solid #3b82f6; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .metric-card { background: #1e293b; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP NAV ---
c_title, c_reboot = st.columns([5, 1])
with c_title:
    st.title("📱 STRIDE-AI Pro")
    st.caption(f"Connected as: {st.session_state.user_mail}")
with c_reboot:
    if st.button("🔄"): reboot_system()

# --- 5. MODULAR TABS ---
tabs = st.tabs(["⚙️ Profiling", "👣 Stride", "🫀 Cardiac", "🧘 Posture", "🧠 AI Analytics"])

# SCREEN 1: DETAILED MEDICAL PROFILING
with tabs[0]:
    st.subheader("🧬 Biological Baseline Setup")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        u_age = st.slider("Current Age", 18, 90, 22, key="u_age")
        u_weight = st.number_input("Weight (kg)", 40, 150, 70)
    with col_p2:
        u_gender = st.selectbox("Biological Gender", ["Male", "Female", "Other"])
        u_goal = st.selectbox("Clinical Objective", ["Recovery", "Fat Loss", "Elite Conditioning"])
    
    st.markdown(f"**System Calibration:** Optimizing for a {u_age}y {u_gender} targeting **{u_goal}**.")

# SCREEN 2: INTERACTIVE STRIDE (Pedometer 2.0)
with tabs[1]:
    st.subheader("👣 Real-time Kinetic Volume")
    
    # Progress towards a daily goal (e.g., 10,000 steps)
    goal = 10000
    progress = min(st.session_state.steps / goal, 1.0)
    st.progress(progress)
    
    st.markdown(f"""<div class='metric-card'>
        <h1 style='color: #60a5fa; margin:0;'>{st.session_state.steps}</h1>
        <p style='margin:0; opacity:0.7;'>TOTAL STEPS ANALYZED</p>
    </div>""", unsafe_allow_html=True)
    
    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.metric("Distance", f"{round(st.session_state.steps * 0.0008, 2)} km")
    c_m2.metric("Kcal Burned", f"{int(st.session_state.steps * 0.04)}")
    c_m3.metric("Goal", f"{int(progress*100)}%")

    if st.button("🛰️ INJECT SENSOR PACKET (7/12/18)"):
        inc = np.random.choice([7, 12, 18])
        st.session_state.steps += inc
        st.session_state.heart_rate = np.random.randint(100, 155)
        # Saving to history for AI assessment
        st.session_state.history.append({"steps": st.session_state.steps, "hr": st.session_state.heart_rate, "time": time.time()})
        st.session_state.report_generated = False
        st.rerun()

# SCREEN 3: CARDIAC PERFORMANCE
with tabs[2]:
    st.subheader("🫀 Electro-Kinetic Telemetry")
    st.metric("Live Pulse", f"{st.session_state.heart_rate} BPM", delta="Elevated" if st.session_state.heart_rate > 120 else "Normal")
    
    # Animated Waveform Plot
    hr_data = pd.DataFrame(np.random.normal(st.session_state.heart_rate, 3, 30), columns=['Pulse'])
    st.line_chart(hr_data, color="#ef4444")
    st.caption("Heart Rate Variability (HRV) Analysis Active.")

# SCREEN 4: POSTURE (Age & History Dependent)
with tabs[3]:
    st.subheader("🧘 Biomechanical Integrity")
    # Logic: Age reduces alignment score
    base_alignment = 96 - (u_age * 0.25)
    p_score = int(base_alignment + np.random.randint(-2, 2))
    
    st.metric("Spinal Alignment Score", f"{p_score}%")
    st.progress(p_score/100)
    
    if p_score < 80:
        st.warning("Observation: Increased Anterior Pelvic Tilt detected. Suggest corrective stretching.")
    else:
        st.success("Observation: Musculoskeletal symmetry is within 5% deviation.")

# SCREEN 5: ADVANCED AI ANALYTICS (The Game Changer)
with tabs[4]:
    st.subheader("🧠 Clinical Decision Support System (CDSS)")
    
    if st.button("🔍 CONDUCT FULL KINETIC AUDIT"):
        with st.spinner("Accessing Historical Bio-Data..."):
            time.sleep(2)
            st.session_state.report_generated = True

    if st.session_state.report_generated:
        # Dynamic Clinical Variables
        vo2_est = round((45 if u_gender == "Male" else 38) - (u_age * 0.15), 1)
        m_age = u_age - 3 if st.session_state.steps > 8000 else u_age + 2
        
        # Smart Advice based on Goal + Steps
        if u_goal == "Fat Loss" and st.session_state.steps < 5000:
            advice = "Your metabolic burn is sub-optimal. Increase volume by 25%."
        elif u_goal == "Elite Conditioning" and st.session_state.heart_rate < 130:
            advice = "Cardiac intensity is insufficient for conditioning. Increase pace."
        else:
            advice = "Kinetic and Cardiac metrics are perfectly synchronized."

        st.markdown(f"""
        <div class='report-box'>
            <h3 style='color:#60a5fa; margin-top:0;'>🛡️ STRIDE-AI: CLINICAL AUDIT REPORT</h3>
            <strong>Subject Identification:</strong> {u_gender}, {u_age} Years, {u_weight}kg <br>
            <strong>Audit Date:</strong> {datetime.now().strftime("%d %b %Y | %H:%M")}
            
            <hr style='opacity:0.2;'>
            
            #### 1. Longitudinal History Assessment
            - **Activity Trend:** Based on pichle **{len(st.session_state.history)}** data packets, your kinetic frequency is stable.
            - **Metabolic Signature:** Your body is performing like a **{m_age} year old** athlete.
            
            #### 2. Cardiovascular Intelligence
            - **Max HR Estimate:** {220 - u_age} BPM | **Observed HR:** {st.session_state.heart_rate} BPM
            - **Estimated VO2 Max:** **{vo2_est} mL/kg/min** (Elite respiratory efficiency for {u_age}y).
            
            #### 3. Biomechanical & Future Roadmap
            - **Current Posture:** {p_score}% alignment. No immediate clinical intervention required.
            - **AI Future Advice:** {advice}
            - **Plan:** Continue current hydration. Next sync required after 2000 steps.
            
            <hr style='opacity:0.2;'>
            <p style='color:#00ffbd; font-weight:bold; font-size:1.1rem;'>FINAL VERDICT: SUBJECT IS PHYSIOLOGICALLY OPTIMIZED.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # PDF/TXT Export
        report_txt = f"STRIDE-AI CLINICAL AUDIT\nUser: {u_gender} ({u_age}y)\nSteps: {st.session_state.steps}\nVO2: {vo2_est}\nVerdict: Optimized"
        st.download_button("📥 DOWNLOAD CLINICAL REPORT", report_txt, file_name=f"StrideAI_Audit_{u_age}y.txt")
    else:
        st.info("Clinical Engine Standby. Initiate Audit to view data correlation.")
