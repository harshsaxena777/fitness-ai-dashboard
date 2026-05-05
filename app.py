import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro", layout="wide")

def reboot_system():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("System Rebooting... Sensors Recalibrated.", icon="🔄")
    time.sleep(1)

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'u_age' not in st.session_state: st.session_state.u_age = 22
if 'steps' not in st.session_state: st.session_state.steps = 7268
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 137
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 3. LOGIN INTERFACE ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI: Clinical Access")
    with st.container():
        user = st.text_input("User Email ID", placeholder="admin@stride.ai")
        pwd = st.text_input("Security Pin", type="password")
        if st.button("Initialize Dashboard"):
            if "@" in user:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 4. TOP NAV ---
header_col, reboot_col = st.columns([5, 1])
with header_col:
    st.title("🏥 STRIDE-AI: Professional Diagnostic Suite")
with reboot_col:
    if st.button("🔄 Reboot System"):
        reboot_system()
        st.rerun()

st.divider()

# --- 5. FUNCTIONAL TABS ---
tabs = st.tabs(["👣 Activity", "🫀 Cardiac", "🧘 Posture Analysis", "🔮 Risk Engine", "🧠 AI Clinical Audit"])

# --- TAB 1: ACTIVITY (RANDOMIZED REFRESH LOGIC) ---
with tabs[0]:
    st.subheader("Kinetic Analytics")
    c1, c2 = st.columns(2)
    c1.metric("Live Step Count", st.session_state.steps)
    
    # Random steps logic: Pick exactly from 10, 20, or 30
    if st.button("Sync Sensor Data"):
        random_increment = np.random.choice([10, 20, 30]) # Yeh line difference control karegi
        st.session_state.steps += random_increment
        st.toast(f"Synchronized! +{random_increment} steps detected.")
        time.sleep(0.5)
        st.rerun()

    step_data = pd.DataFrame(np.random.randint(100, 850, 24), columns=['Steps'])
    st.bar_chart(step_data)

# --- TAB 2: CARDIAC ---
with tabs[1]:
    st.subheader("Cardiovascular Telemetry")
    h1, h2 = st.columns([1, 2])
    with h1:
        st.metric("Current BPM", f"{st.session_state.heart_rate}")
        if st.button("⚡ Live Sync Pulse"):
            st.session_state.heart_rate = np.random.randint(110, 160)
            st.rerun()
    with h2:
        t = np.linspace(0, 10, 100)
        y = np.sin(t) + np.random.normal(0, 0.05, 100)
        fig_hr = px.line(x=t, y=y, title="Pulse Waveform", template="plotly_dark")
        st.plotly_chart(fig_hr, use_container_width=True)

# --- TAB 3: POSTURE ---
with tabs[2]:
    st.subheader("Biomechanical Integrity")
    st.metric("Alignment Score", "79%", "Optimal")
    st.area_chart(np.random.uniform(70, 85, 20))

# --- TAB 4: RISK ---
with tabs[3]:
    st.subheader("Predictive Health Forecasting")
    st.markdown("**🚷 Fall Risk Level: LOW**")
    st.progress(20)

# --- TAB 5: AI CLINICAL AUDIT (CLEAN MARKDOWN) ---
with tabs[4]:
    st.subheader("📋 Final Clinical Audit")
    if st.button("🔍 GENERATE DIAGNOSIS"):
        st.session_state.report_ready = True
            
    if st.session_state.report_ready:
        calc_m_age = st.session_state.u_age - 2 if st.session_state.steps > 7500 else st.session_state.u_age + 1
        
        st.markdown(f"""
        ### 🛡️ STRIDE-AI FINAL CLINICAL AUDIT
        ---
        #### 1. Physical Activity Summary
        The system recorded a total kinetic volume of **{st.session_state.steps} steps**. 
        The **Metabolic Age** is estimated at **{calc_m_age} years**.
        
        #### 2. Cardiovascular Analysis
        Current heart rate is **{st.session_state.heart_rate} BPM**. 
        Respiratory efficiency is within expected parameters.
        
        #### 3. Biomechanical Integrity
        **Posture Score:** 79%. **Gait Entropy:** 1.2% clinical deviation.
        
        #### 4. Predictive Risk
        **Fall Risk:** LOW. No dietary-cardiac distress found.
        
        ---
        ### ⭐ FINAL VERDICT
        **Subject is physiologically optimized.** No clinical intervention required.
        """)

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
