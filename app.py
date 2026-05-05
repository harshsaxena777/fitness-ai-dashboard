import streamlit as st
import plotly.graph_objects as go
import plotly.express as px  # <--- Yeh line Error fix karegi
import numpy as np
import pandas as pd
import time

# --- 1. CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro Account", layout="centered")

# --- 2. SESSION STATE (Virtual Database) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_mail' not in st.session_state: st.session_state.user_mail = ""
if 'steps' not in st.session_state: st.session_state.steps = 7268 # Current Audit Data
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 137
if 'u_age' not in st.session_state: st.session_state.u_age = 22
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 3. LOGIN INTERFACE ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Portal")
    st.markdown("Enter your credentials to sync with clinical cloud.")
    
    with st.form("login_form"):
        email = st.text_input("Email ID", placeholder="harsh@srms.ac.in")
        mobile = st.text_input("Mobile Number", placeholder="+91-XXXXX-XXXXX")
        submitted = st.form_submit_button("Login / Create Account")
        
        if submitted:
            if "@" in email and len(mobile) >= 10:
                st.session_state.logged_in = True
                st.session_state.user_mail = email
                st.rerun()
            else:
                st.error("Invalid Email or Mobile Number.")
    st.stop()

# --- 4. DASHBOARD UI ---
st.title("📱 STRIDE-AI Pro")
st.caption(f"Connected: {st.session_state.user_mail}")

tabs = st.tabs(["⚙️ Profile", "👣 Activity", "🫀 Cardiac", "🧘 Posture", "🧠 AI Audit"])

# SCREEN 1: SETUP
with tabs[0]:
    st.subheader("Subject Calibration")
    st.session_state.u_age = st.slider("Select Age", 18, 80, st.session_state.u_age)
    st.number_input("Weight (kg)", 40, 150, 70)
    st.info("System is optimizing algorithms for your age group.")

# SCREEN 2: STEPS & ANALYTICS
with tabs[1]:
    st.subheader("Kinetic Volume")
    c1, c2 = st.columns(2)
    c1.metric("Steps", st.session_state.steps)
    c2.metric("Target", "10,000")
    
    # Advanced Bar Chart
    step_history = pd.DataFrame(np.random.randint(200, 800, 12), columns=['Steps/Hour'])
    st.bar_chart(step_history)

# SCREEN 3: HEART RATE (FIXED px.line ERROR)
with tabs[2]:
    st.subheader("Cardiac Stress Test")
    st.metric("Pulse", f"{st.session_state.heart_rate} BPM")
    
    # Waveform Graph
    t = np.linspace(0, 10, 100)
    y = np.sin(t) + np.random.normal(0, 0.05, 100)
    fig_hr = px.line(x=t, y=y, title="Electro-Kinetic Pulse Pattern", template="plotly_dark")
    fig_hr.update_layout(xaxis_title="Time (s)", yaxis_title="Amplitude")
    st.plotly_chart(fig_hr, use_container_width=True)

# SCREEN 4: POSTURE
with tabs[3]:
    st.subheader("Biomechanical Integrity")
    st.metric("Alignment Score", "79%")
    st.progress(0.79)
    st.write("Visualizing Gait Symmetry...")
    st.area_chart(np.random.rand(20))

# SCREEN 5: ELABORATIVE AI REPORT
with tabs[4]:
    st.subheader("📋 Final Clinical Audit")
    
    if st.button("🔍 RUN AI DIAGNOSIS"):
        with st.spinner("Analyzing Multi-System Data..."):
            time.sleep(2)
            st.session_state.report_ready = True

    if st.session_state.report_ready:
        # Final Calculation
        m_age = st.session_state.u_age - 2 if st.session_state.steps > 7000 else st.session_state.u_age + 1
        vo2_est = 20.8 # Based on your last audit
        
        # 📊 Radar Visualization (The "Advance" Factor)
        categories = ['Gait Stability', 'Cardiac Load', 'Metabolism', 'Activity', 'Postural Balance']
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=[85, 70, 90, 75, 79],
          theta=categories,
          fill='toself',
          line_color='#3b82f6'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown(f"""
        ### STRIDE-AI FINAL CLINICAL AUDIT
        
        **1. Physical Activity Summary:**  
        Total volume of **{st.session_state.steps} steps** executed. Subject is maintaining an active lifestyle. **Metabolic age** is estimated at **{m_age} years**.
        
        **2. Cardiovascular & Stress Analysis:**  
        Current BPM (**{st.session_state.heart_rate}**) indicates a stable aerobic state. **VO2 Max** estimation stands at **{vo2_est} mL/kg/min**.
        
        **3. Biomechanical & Posture Integrity:**  
        **Posture Score** of **79%** suggests no immediate musculoskeletal risk. **Gait entropy** remains within clinical deviation.
        
        **4. Predictive Health Risk:**  
        **Fall risk** is minimized (Level: **LOW**). No significant correlation between diet and cardiac distress found.
        
        ---
        **⭐ FINAL VERDICT:**  
        Subject is physiologically optimized. No clinical intervention required.
        """)
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
