import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time

# --- 1. SYSTEM CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro", layout="wide") # Standard wide layout

def reboot_system():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.toast("System Rebooting... All sensor states cleared.", icon="🔄")
    time.sleep(1)

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'u_age' not in st.session_state: st.session_state.u_age = 22
if 'steps' not in st.session_state: st.session_state.steps = 7268
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 137
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 3. CUSTOM STYLING (Minimal & Clean) ---
st.markdown("""
    <style>
    .report-card { 
        background-color: #111; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 10px solid #3b82f6; 
        margin-top: 20px;
    }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Clinical Portal")
    col1, col2 = st.columns([1, 1])
    with col1:
        user = st.text_input("Clinical Email ID")
        pwd = st.text_input("Access Password", type="password")
        if st.button("Initialize System"):
            if "@" in user:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 5. HEADER & GLOBAL ACTIONS ---
c1, c2 = st.columns([5, 1])
with c1:
    st.title("🏥 STRIDE-AI: Advanced Health Suite")
with c2:
    if st.button("🔄 Reboot System"):
        reboot_system()
        st.rerun()

st.divider()

# --- 6. CORE TABS ---
tabs = st.tabs(["📊 Activity", "🫀 Cardiac", "🧘 Posture Analysis", "🔮 Risk Engine", "🧠 AI Clinical Audit"])

# --- TAB 1: ACTIVITY ---
with tabs[0]:
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Total Kinetic Volume", st.session_state.steps, "Steps")
    col_m2.metric("Metabolic Status", "Active")
    
    st.subheader("Step Frequency (24h)")
    step_data = pd.DataFrame(np.random.randint(100, 1000, 24), columns=['Steps'])
    st.bar_chart(step_data)
    
    if st.button("Sync Sensor Data"):
        st.session_state.steps += np.random.randint(200, 500)
        st.rerun()

# --- TAB 2: CARDIAC ---
with tabs[1]:
    col_h1, col_h2 = st.columns([1, 2])
    with col_h1:
        st.metric("Current Pulse", f"{st.session_state.heart_rate} BPM")
        if st.button("⚡ Live BPM Sync"):
            st.session_state.heart_rate = np.random.randint(110, 160)
            st.rerun()
    with col_h2:
        t = np.linspace(0, 10, 100)
        y = np.sin(t) + np.random.normal(0, 0.05, 100)
        fig_hr = px.line(x=t, y=y, title="Electro-Kinetic Pulse Pattern", template="plotly_dark")
        st.plotly_chart(fig_hr, use_container_width=True)

# --- TAB 3: POSTURE (Detailed) ---
with tabs[2]:
    st.subheader("Biomechanical Posture Analysis")
    p1, p2 = st.columns(2)
    p1.metric("Spinal Alignment Score", "79%")
    p2.metric("Gait Symmetry", "94.2%")
    
    st.write("### Joint Angle Variance")
    posture_history = pd.DataFrame(np.random.uniform(70, 85, 20), columns=['Alignment'])
    st.area_chart(posture_history)
    st.info("AI Analysis: Normal lumbar curvature detected. Slight pelvic tilt observed during high-velocity strides.")

# --- TAB 4: RISK ---
with tabs[3]:
    st.subheader("Predictive Risk Assessment")
    st.write("---")
    r1, r2 = st.columns(2)
    with r1:
        st.write("🚷 **Fall Risk Assessment**")
        st.progress(0.20)
        st.write("Status: **LOW RISK**")
    with r2:
        st.write("🥗 **Metabolic Correlation**")
        st.success("No cardiac distress detected post-caloric intake.")

# --- TAB 5: ELABORATIVE AI REPORT (The Good One) ---
with tabs[4]:
    st.subheader("📋 Comprehensive Clinical Audit")
    if st.button("🔍 GENERATE FINAL DIAGNOSIS"):
        with st.spinner("Compiling Multi-System Analytics..."):
            time.sleep(2)
            st.session_state.report_ready = True
            
    if st.session_state.report_ready:
        # Calculations
        m_age = st.session_state.u_age - 2 if st.session_state.steps > 7000 else st.session_state.u_age + 1
        vo2_est = round(15 * (190 / st.session_state.heart_rate), 1)

        # Radar Visualization
        categories = ['Gait Stability', 'Cardiac Load', 'Metabolism', 'Posture', 'Balance']
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=[85, 72, 90, 79, 92],
          theta=categories,
          fill='toself',
          line_color='#3b82f6'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)

        # Elaborative Report
        st.markdown(f"""
        <div class="report-card">
            <h2 style="color:#3b82f6; margin-top:0;">STRIDE-AI FINAL CLINICAL AUDIT</h2>
            
            <p><b>1. Physical Activity Summary:</b><br>
            Total volume of <b>{st.session_state.steps} steps</b> executed. Subject is maintaining an active lifestyle. 
            Metabolic age is estimated at <b>{m_age} years</b>.</p>
            
            <p><b>2. Cardiovascular & Stress Analysis:</b><br>
            Current BPM (<b>{st.session_state.heart_rate}</b>) indicates a stable aerobic state. 
            VO2 Max estimation stands at <b>{vo2_est} mL/kg/min</b>, showing elite respiratory efficiency.</p>
            
            <p><b>3. Biomechanical & Posture Integrity:</b><br>
            Posture Score of <b>79%</b> suggests no immediate musculoskeletal risk. 
            Gait entropy remains within 1.2% of the standard clinical deviation.</p>
            
            <p><b>4. Predictive Health Risk:</b><br>
            Fall risk is minimized (Level: <b>LOW</b>). No significant correlation between diet and cardiac distress found.</p>
            
            <hr style="opacity:0.2;">
            <h3 style="color:#00ffbd; margin-bottom:0;">Final Verdict: Subject is physiologically optimized.</h3>
            <p>No clinical intervention required based on current sensor telemetry.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.download_button("📥 Export Audit Log", "Full Clinical Data...", file_name="StrideAI_Full_Audit.txt")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
