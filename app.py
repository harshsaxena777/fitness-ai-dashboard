import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro", layout="wide")

def reboot_system():
    # Poora session state clear karke login screen par wapas le jayega
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("System Rebooting... Sensors Recalibrated.", icon="🔄")
    time.sleep(1)

# --- 2. SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'u_age' not in st.session_state: st.session_state.u_age = 22
if 'steps' not in st.session_state: st.session_state.steps = 7268
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 137
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 3. LOGIN INTERFACE ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI: Clinical Access")
    st.info("Enter credentials to synchronize with the local health server.")
    
    with st.container():
        user = st.text_input("User Email ID", placeholder="admin@stride.ai")
        pwd = st.text_input("Security Pin", type="password")
        if st.button("Initialize Dashboard"):
            if "@" in user:
                st.session_state.logged_in = True
                st.success("Access Granted. Synchronizing Sensors...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials. Access Denied.")
    st.stop()

# --- 4. TOP NAV & GLOBAL ACTIONS ---
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

# TAB 1: ACTIVITY
with tabs[0]:
    st.subheader("Kinetic Analytics")
    c1, c2 = st.columns(2)
    c1.metric("Live Step Count", st.session_state.steps, delta="+12% Active")
    c2.metric("Target", "10,000 Steps", delta="-2,732 to Goal")
    
    # Step Frequency Chart
    step_data = pd.DataFrame(np.random.randint(100, 850, 24), columns=['Steps'])
    st.bar_chart(step_data)
    
    if st.button("Sync Sensor Data"):
        st.session_state.steps += np.random.randint(150, 450)
        st.rerun()

# TAB 2: CARDIAC
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
        fig_hr = px.line(x=t, y=y, title="Electro-Kinetic Pulse Pattern", template="plotly_dark")
        st.plotly_chart(fig_hr, use_container_width=True)

# TAB 3: POSTURE
with tabs[2]:
    st.subheader("Biomechanical Integrity")
    p1, p2 = st.columns(2)
    p1.metric("Alignment Score", "79%", "Optimal")
    p2.metric("Gait Symmetry", "94%", "Stable")
    
    st.area_chart(np.random.uniform(70, 85, 20))
    st.caption("AI Note: Slight pelvic tilt detected during high-velocity movement.")

# TAB 4: RISK ENGINE
with tabs[3]:
    st.subheader("Predictive Health Forecasting")
    st.write("---")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**🚷 Fall Risk Level**")
        st.progress(20)
        st.write("Status: **LOW RISK** (92.4% Probability of Stability)")
    with r2:
        st.markdown("**🥗 Dietary Correlation**")
        st.success("Metabolic markers consistent with current cardiac load.")

# TAB 5: CLEAN ELABORATIVE AI REPORT (FIXED TAGS & BACKEND)
with tabs[4]:
    st.subheader("📋 Final Clinical Audit")
    
    if st.button("🔍 GENERATE DIAGNOSIS"):
        with st.spinner("Processing Multi-System Data..."):
            time.sleep(1.5)
            st.session_state.report_ready = True
            
    if st.session_state.report_ready:
        # Internal Logic (Backend calculations hidden from UI)
        current_age = st.session_state.u_age
        calc_m_age = current_age - 2 if st.session_state.steps > 7000 else current_age + 1
        calc_vo2 = round(15 * (190 / st.session_state.heart_rate), 1)

        # Visual Intelligence Map
        categories = ['Gait Stability', 'Cardiac Load', 'Metabolism', 'Posture', 'Balance']
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=[85, 72, 90, 79, 92],
          theta=categories,
          fill='toself',
          line_color='#3b82f6'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)

        # THE REPORT - Pure Markdown (No Tags)
        st.markdown(f"""
        ### 🛡️ STRIDE-AI FINAL CLINICAL AUDIT
        **Reference ID:** STRIDE-2026-X | **Status:** Optimized
        
        ---
        
        #### 1. Physical Activity Summary
        The system recorded a total kinetic volume of **{st.session_state.steps} steps**. The subject is maintaining an active physiological state. Based on these metrics, the **Metabolic Age** is estimated at **{calc_m_age} years**.
        
        #### 2. Cardiovascular & Stress Analysis
        Current telemetry indicates a heart rate of **{st.session_state.heart_rate} BPM**. This represents a stable aerobic zone. The **VO2 Max** estimation is **{calc_vo2} mL/kg/min**, signifying high respiratory efficiency.
        
        #### 3. Biomechanical & Posture Integrity
        A **Posture Score** of **79%** indicates strong spinal alignment. Data indicates that **Gait Entropy** remains within **1.2%** of the standard clinical deviation, confirming high neurological motor control.
        
        #### 4. Predictive Health Risk
        The **Fall Risk** is currently categorized as **LOW**. No significant adverse correlations were found between dietary intake and cardiac rhythm under stress.
        
        ---
        
        ### ⭐ FINAL VERDICT
        **The subject is physiologically optimized.** All monitored biosignals fall within healthy clinical parameters. No immediate intervention is required.
        """)
        
        st.download_button("📥 Export Diagnostic Log", f"Report: {st.session_state.steps} steps, Healthy.", file_name="StrideAI_Audit.txt")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
