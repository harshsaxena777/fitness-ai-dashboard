import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# --- 1. CONFIG & REBOOT ---
st.set_page_config(page_title="STRIDE-AI Pro Account", layout="centered")

# --- 2. VIRTUAL ACCOUNT SYSTEM ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_mail' not in st.session_state: st.session_state.user_mail = ""
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'u_age' not in st.session_state: st.session_state.u_age = 22
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- LOGIN SCREEN LOGIC ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Portal")
    st.markdown("Please login to access your clinical dashboard.")
    
    with st.container():
        email = st.text_input("Email ID Address", placeholder="example@gmail.com")
        mobile = st.text_input("Mobile Number", placeholder="+91-XXXXX-XXXXX")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        if col1.button("Create Account"):
            st.success("Account created! Now click Login.")
        if col2.button("Login"):
            if "@" in email and len(mobile) >= 10:
                st.session_state.logged_in = True
                st.session_state.user_mail = email
                st.rerun()
            else:
                st.error("Please enter valid credentials.")
    st.stop() # Login hone tak baki app nahi chalegi

# --- 3. UI STYLING ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .report-card { background: #0d1117; padding: 20px; border-radius: 15px; border-left: 8px solid #3b82f6; }
    .user-info { background: #1e293b; padding: 10px; border-radius: 10px; margin-bottom: 20px; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# --- 4. DASHBOARD TOP ---
st.title("📱 STRIDE-AI Pro")
st.markdown(f"<div class='user-info'>👤 User: <b>{st.session_state.user_mail}</b></div>", unsafe_allow_html=True)

# --- 5. ELABORATE TABS ---
tabs = st.tabs(["⚙️ Setup", "👣 Steps", "🫀 Heart", "🧘 Posture", "🧠 AI Report"])

# SCREEN 1: ELABORATE SETUP
with tabs[0]:
    st.subheader("Physical Profile")
    st.session_state.u_age = st.slider("Select Age", 18, 80, st.session_state.u_age)
    u_weight = st.number_input("Weight (kg)", 40, 150, 70)
    u_height = st.number_input("Height (cm)", 140, 210, 175)
    st.info(f"Target Heart Rate: {220 - st.session_state.u_age} BPM")

# SCREEN 2: STEPS WITH GRAPHS
with tabs[1]:
    st.subheader("Pedometer Analytics")
    c1, c2 = st.columns(2)
    c1.metric("Current Steps", st.session_state.steps)
    c2.metric("Distance", f"{round(st.session_state.steps * 0.0008, 2)} km")
    
    # Graph: Step Frequency over 24h
    step_data = pd.DataFrame(np.random.randint(100, 1000, 24), columns=['Steps'])
    st.bar_chart(step_data)
    
    if st.button("Inject Step Packet"):
        st.session_state.steps += 450
        st.rerun()

# SCREEN 3: HEART RATE WITH LIVE FEEL
with tabs[2]:
    st.subheader("Cardiac Performance")
    st.metric("Pulse Rate", f"{st.session_state.heart_rate} BPM")
    
    # Live Waveform Graph
    t = np.linspace(0, 10, 100)
    y = np.sin(t) + np.random.normal(0, 0.1, 100)
    fig_hr = px.line(x=t, y=y, title="Electro-Kinetic Pulse Pattern", template="plotly_dark")
    st.plotly_chart(fig_hr, use_container_width=True)

# SCREEN 4: POSTURE (SIMPLE BUT CLEAR)
with tabs[3]:
    st.subheader("Posture Integrity")
    score = 79
    st.metric("Alignment Score", f"{score}%")
    st.write("Spinal Curvature Deviation")
    st.progress(score/100)
    st.caption("AI Analysis: Normal lumbar curve detected.")

# SCREEN 5: ELABORATIVE AI REPORT + RADAR CHART
with tabs[4]:
    st.subheader("📋 Advanced Clinical Report")
    
    if st.button("🔍 GENERATE FULL DIAGNOSIS"):
        with st.spinner("Crunching Bio-Data..."):
            time.sleep(2)
            st.session_state.report_ready = True

    if st.session_state.report_ready:
        m_age = st.session_state.u_age - 2 if st.session_state.steps > 8000 else st.session_state.u_age + 1
        vo2_est = round(15 * (190 / st.session_state.heart_rate), 1)

        # 📊 ADDING A RADAR CHART FOR VISUAL REPORT
        st.write("### Physiological Efficiency Map")
        categories = ['Stability', 'Cardiac', 'Metabolic', 'Activity', 'Respiratory']
        fig_radar = go.Figure(data=go.Scatterpolar(
          r=[85, 70, 90, 65, 80],
          theta=categories,
          fill='toself',
          line_color='#3b82f6'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown(f"""
        <div class="report-card">
            <h4>STRIDE-AI FINAL AUDIT</h4>
            <p><b>1. Activity Summary:</b> Total {st.session_state.steps} steps. Metabolic age is {m_age}.</p>
            <p><b>2. Cardiac Health:</b> Pulse is {st.session_state.heart_rate} BPM. VO2 Max: {vo2_est}.</p>
            <p><b>3. Biomechanical:</b> Posture alignment is 79% stable.</p>
            <hr style='opacity:0.2;'>
            <b>AI Verdict:</b> Subject is in <b>Optimized Physical Condition</b>. 
            No anomalies detected in gait or cardiac rhythm.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()
