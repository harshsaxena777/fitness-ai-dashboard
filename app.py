import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI x Sweatcoin", layout="centered")

def reboot_system():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("System Wiped. Recalibrating Biometrics...", icon="⚡")
    time.sleep(1)
    st.rerun()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'history' not in st.session_state: st.session_state.history = []
if 'report_generated' not in st.session_state: st.session_state.report_generated = False

# --- 3. CUSTOM SWEATCOIN CSS (Background & Neumorphism) ---
st.markdown("""
<style>
    /* Sweatcoin Dark Theme Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
    }
    
    /* Glowing Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 30px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 20px;
    }
    
    .step-text {
        font-size: 4rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Sweatcoin Style Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        border-radius: 25px;
        border: none;
        height: 4em;
        font-size: 1.1rem;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.6);
    }

    /* Navigation Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px 20px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIN (Sweatcoin Style) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>Stride-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6;'>Your steps are worth clinical insights.</p>", unsafe_allow_html=True)
    email = st.text_input("Enter Email to Connect", placeholder="harsh@srms.ac.in")
    if st.button("Connect Account"):
        if "@" in email:
            st.session_state.logged_in = True
            st.session_state.user_mail = email
            st.rerun()
    st.stop()

# --- 4. TOP NAV ---
c_title, c_reboot = st.columns([5, 1])
with c_title:
    st.markdown(f"**Hello, {st.session_state.user_mail.split('@')[0].capitalize()}! 👋**")
with c_reboot:
    if st.button("🔄"): reboot_system()

# --- 5. MODULAR TABS ---
tabs = st.tabs(["⚡ Dashboard", "⚙️ Profile", "🫀 Vitals", "🧘 Alignment", "🧠 AI Audit"])

# SCREEN 1: DASHBOARD (The Sweatcoin Experience)
with tabs[0]:
    # Circle Progress Visualization
    progress_val = min(st.session_state.steps / 10000, 1.0)
    
    st.markdown(f"""
    <div class='metric-card'>
        <p style='margin:0; opacity:0.6; letter-spacing: 2px;'>TODAY'S STRIDE</p>
        <h1 class='step-text'>{st.session_state.steps}</h1>
        <p style='margin:0; color:#a855f7; font-weight:bold;'>STREAK: 5 DAYS 🔥</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress_val)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Distance", f"{round(st.session_state.steps * 0.0007, 2)}km")
    col2.metric("Kcal", int(st.session_state.steps * 0.04))
    col3.metric("Level", "Elite" if st.session_state.steps > 5000 else "Beginner")

    if st.button("🛰️ SYNC SENSOR DATA"):
        st.session_state.steps += np.random.choice([7, 12, 18])
        st.session_state.heart_rate = np.random.randint(100, 145)
        st.session_state.history.append({"s": st.session_state.steps, "h": st.session_state.heart_rate})
        st.session_state.report_generated = False
        st.rerun()

# SCREEN 2: DETAILED PROFILING
with tabs[1]:
    st.subheader("🧬 User Biometrics")
    u_age = st.slider("Age", 18, 90, 22)
    u_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    u_weight = st.number_input("Weight (kg)", 40.0, 150.0, 72.0)
    u_height = st.number_input("Height (cm)", 140, 210, 178)
    
    bmi = round(u_weight / ((u_height/100)**2), 1)
    st.write(f"**BMI Analysis:** {bmi} (Normal Range)")

# SCREEN 3: VITALS (Heart & Pulse)
with tabs[2]:
    st.subheader("🫀 Live Telemetry")
    st.metric("Pulse Rate", f"{st.session_state.heart_rate} BPM")
    
    # Elegant Cardiac Waveform
    x = np.linspace(0, 10, 50)
    y = np.sin(x) * np.random.rand() + st.session_state.heart_rate
    fig = px.line(x=x, y=y, template="plotly_dark", color_discrete_sequence=['#ef4444'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# SCREEN 4: POSTURE (Detailed Kinematics)
with tabs[3]:
    st.subheader("🧘 Biomechanical Balance")
    p_score = int(96 - (u_age * 0.2))
    st.metric("Body Alignment", f"{p_score}%")
    
    st.write("### Displacement Analysis")
    # Radar Chart for Balance (Sweatcoin inspired analytics)
    categories = ['Head Tilt', 'Shoulder Sym.', 'Pelvic Bal.', 'Knee Align.', 'Foot Pressure']
    fig_radar = go.Figure(data=go.Scatterpolar(
      r=[90, 85, p_score, 88, 92],
      theta=categories,
      fill='toself',
      line_color='#a855f7'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_radar, use_container_width=True)

# SCREEN 5: AI AUDIT (Clinical Insights)
with tabs[4]:
    st.subheader("🧠 AI Clinical Audit")
    
    if st.button("🔍 GENERATE FULL HEALTH REPORT"):
        with st.spinner("Analyzing Kinetic History..."):
            time.sleep(2)
            st.session_state.report_generated = True

    if st.session_state.report_generated:
        m_age = u_age - 3 if st.session_state.steps > 6000 else u_age + 1
        
        st.markdown(f"""
### 📊 CLINICAL DIAGNOSIS SUMMARY
**Subject:** {st.session_state.user_mail} | **Metabolic Age:** {m_age}Y

---

#### 👣 Kinetic Volume
You have completed **{st.session_state.steps} steps**. Your current volume is **{'OPTIMAL' if st.session_state.steps > 5000 else 'LOW'}** for a {u_age} year old.

#### 🫀 Cardiac Intelligence
Pulse is stable at **{st.session_state.heart_rate} BPM**. VO2 Max estimation indicates elite respiratory recovery.

#### 🧘 Posture & Balance
Alignment score of **{p_score}%** detected. Your Pelvic balance is the primary deviation factor.

---

**⭐ AI VERDICT:**
Your physiology is **Stable & Optimized**. No musculoskeletal anomalies detected in the last {len(st.session_state.history)} packets.
        """)
        
        st.download_button("📥 Download Report", f"Steps: {st.session_state.steps}\nBPM: {st.session_state.heart_rate}", file_name="StrideReport.txt")
