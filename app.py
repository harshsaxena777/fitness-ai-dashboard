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
    st.toast("Hard Resetting... Wiping Session Data", icon="🔥")
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

# SCREEN 1: PROFILING
with tabs[0]:
    st.subheader("🧬 Biological Baseline Setup")
    u_age = st.slider("Current Age", 18, 90, 22, key="u_age")
    u_gender = st.selectbox("Biological Gender", ["Male", "Female", "Other"])
    u_goal = st.selectbox("Clinical Objective", ["Recovery", "Fat Loss", "Elite Conditioning"])

# SCREEN 2: STRIDE (Steps)
with tabs[1]:
    st.subheader("👣 Real-time Kinetic Volume")
    st.markdown(f"""<div class='metric-card'>
        <h1 style='color: #60a5fa; margin:0;'>{st.session_state.steps}</h1>
        <p style='margin:0; opacity:0.7;'>TOTAL STEPS ANALYZED</p>
    </div>""", unsafe_allow_html=True)
    
    # Button Fixed: No numbers shown
    if st.button("🛰️ INJECT SENSOR PACKET"):
        st.session_state.steps += np.random.choice([7, 12, 18])
        st.session_state.heart_rate = np.random.randint(100, 155)
        st.session_state.history.append({"steps": st.session_state.steps, "hr": st.session_state.heart_rate})
        st.session_state.report_generated = False # New data resets report
        st.rerun()

# SCREEN 3: CARDIAC
with tabs[2]:
    st.subheader("🫀 Cardiac Telemetry")
    st.metric("Live Pulse", f"{st.session_state.heart_rate} BPM")
    st.line_chart(pd.DataFrame(np.random.normal(st.session_state.heart_rate, 2, 20)), color="#ef4444")

# SCREEN 4: POSTURE (Detailed & Interactive)
with tabs[3]:
    st.subheader("🧘 Biomechanical Integrity")
    # Logic: Age-dependent degradation
    base_alignment = 96 - (u_age * 0.25)
    p_score = int(base_alignment + np.random.randint(-2, 2))
    
    st.metric("Spinal Alignment Score", f"{p_score}%")
    st.progress(p_score/100)
    
    # Posture Interactive Visualization
    st.write("### Joint-Angle Deviation Analysis")
    joint_data = pd.DataFrame({
        'Joint Segment': ['Cervical (Neck)', 'Thoracic (Mid-back)', 'Lumbar (Lower-back)', 'Pelvic Tilt'],
        'Deviation (°)': [1.2, 2.5 + (u_age*0.05), 1.8 + (u_age*0.08), 3.1]
    })
    fig_posture = go.Figure(go.Bar(
        x=joint_data['Deviation (°)'], y=joint_data['Joint Segment'], 
        orientation='h', marker_color='#3b82f6'
    ))
    fig_posture.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_posture, use_container_width=True)

# SCREEN 5: AI ANALYTICS (Fixed Tags & Trigger)
with tabs[4]:
    st.subheader("🧠 Clinical Decision Support System")
    
    # Trigger Button
    if st.button("🔍 CONDUCT FULL KINETIC AUDIT"):
        with st.spinner("Analyzing Bio-Kinetic History..."):
            time.sleep(2)
            st.session_state.report_generated = True

    if st.session_state.report_generated:
        # Clinical Calculations
        vo2_est = round((45 if u_gender == "Male" else 38) - (u_age * 0.15), 1)
        m_age = u_age - 3 if st.session_state.steps > 8000 else u_age + 2
        
        # Clean Markdown Display (Fixing HTML Tags)
        st.markdown(f"""
### 🛡️ STRIDE-AI: CLINICAL AUDIT REPORT
**Subject Identification:** {u_gender} | {u_age} Years | {st.session_state.user_mail}
**Audit Date:** {datetime.now().strftime("%d %b %Y | %H:%M")}

---

#### 1. Longitudinal History Assessment
- **Activity Trend:** Analysis of **{len(st.session_state.history)} packets** shows stable kinetic frequency.
- **Metabolic Signature:** Your body is performing like a **{m_age} year old**.

#### 2. Cardiovascular Intelligence
- **Max HR Estimate:** {220 - u_age} BPM | **Observed HR:** {st.session_state.heart_rate} BPM
- **Estimated VO2 Max:** **{vo2_est} mL/kg/min**

#### 3. Biomechanical Roadmap
- **Current Posture:** {p_score}% alignment score.
- **Future Plan:** Given your goal of **{u_goal}**, increase hydration and maintain lumbar support.
- **Verdict:** Subject is **Physiologically Optimized**.

---
        """)
        
        # Download Button
        report_txt = f"STRIDE-AI REPORT\nUser: {u_gender}, {u_age}y\nSteps: {st.session_state.steps}\nVerdict: Optimized"
        st.download_button("📥 DOWNLOAD CLINICAL AUDIT", report_txt, file_name=f"StrideAI_{u_age}y_Audit.txt")
    else:
        st.info("System Standby. Click 'Conduct Full Kinetic Audit' to generate diagnosis.")
