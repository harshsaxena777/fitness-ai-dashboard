import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time

# --- 1. SYSTEM CONFIG & REBOOT LOGIC ---
st.set_page_config(page_title="STRIDE-AI Mobile Pro", layout="centered")

# Function to wipe all data and go back to login
def reboot_system():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("System Rebooting... Sensors Cleared.", icon="🔄")
    time.sleep(1)

# --- 2. MOBILE CSS WRAPPER ---
st.markdown("""
    <style>
    .main { max-width: 420px; margin: 0 auto; background-color: #0e1117; }
    header, footer {visibility: hidden;}
    .reboot-container { text-align: right; margin-bottom: -40px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .report-card { background: #161b22; padding: 15px; border-radius: 12px; border-left: 6px solid #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'steps' not in st.session_state: st.session_state.steps = 7268
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 137
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 4. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>🔐 STRIDE-AI</h2>", unsafe_allow_html=True)
    with st.container():
        user = st.text_input("Clinical Email")
        pwd = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            if "@" in user:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 5. MAIN APP HEADER & REBOOT ---
st.markdown('<div class="reboot-container">', unsafe_allow_html=True)
if st.button("🔄", help="System Reboot"):
    reboot_system()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>📱 STRIDE-AI PRO</h3>", unsafe_allow_html=True)

# --- 6. MULTI-SCREEN TABS ---
tabs = st.tabs(["👣 Steps", "🫀 Heart", "🧘 Posture", "🔮 Risk", "🧠 Audit"])

# SCREEN 1: STEPS
with tabs[0]:
    st.metric("Total Steps", st.session_state.steps, delta="+12% Sync")
    st.bar_chart(np.random.randint(200, 800, 10))
    if st.button("🔄 Refresh Step Data"):
        st.session_state.steps += np.random.randint(100, 300)
        st.toast("Steps Updated!")
        st.rerun()

# SCREEN 2: HEART RATE
with tabs[1]:
    st.metric("Current Pulse", f"{st.session_state.heart_rate} BPM")
    t = np.linspace(0, 10, 50)
    y = np.sin(t) + np.random.normal(0, 0.1, 50)
    fig_hr = px.line(x=t, y=y, template="plotly_dark")
    fig_hr.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_hr, use_container_width=True)
    if st.button("⚡ Live Pulse Sync"):
        st.session_state.heart_rate = np.random.randint(110, 155)
        st.rerun()

# SCREEN 3: POSTURE
with tabs[3]:
    st.subheader("Posture Analysis")
    st.metric("Alignment Score", "79%")
    st.progress(0.79)
    st.caption("AI Pose Modeling Synchronized.")

# SCREEN 4: RISK
with tabs[3]:
    st.subheader("Predictive Risk")
    st.write("Fall Risk: **LOW**")
    st.write("Cardiac Stress: **NORMAL**")

# SCREEN 5: AI AUDIT REPORT
with tabs[4]:
    if st.button("🔍 GENERATE CLINICAL AUDIT"):
        with st.spinner("Analyzing Multi-Screen Data..."):
            time.sleep(1.5)
            st.session_state.report_ready = True
            
    if st.session_state.report_ready:
        # Radar Chart
        categories = ['Stability', 'Cardiac', 'Metabolism', 'Posture']
        fig_radar = go.Figure(data=go.Scatterpolar(r=[85, 70, 90, 79], theta=categories, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), height=250, margin=dict(l=40,r=40,t=20,b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.markdown(f"""
        <div class="report-card">
        **Audit Results:**  
        - **Total Steps:** {st.session_state.steps}  
        - **Pulse:** {st.session_state.heart_rate} BPM  
        - **Verdict:** Subject is Optimized.
        </div>
        """, unsafe_allow_html=True)

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
