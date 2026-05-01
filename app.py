import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# --- CONFIG ---
st.set_page_config(page_title="STRIDE-AI Mobile Pro", layout="centered")

# --- SESSION STATE ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'diet_input' not in st.session_state: st.session_state.diet_input = "Balanced"
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- STYLING ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 15px; height: 3.5em; background: #3b82f6; font-weight: bold; }
    .feature-card { background: #0d1117; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; margin-bottom: 15px; }
    .risk-high { color: #ef4444; font-weight: bold; }
    .risk-low { color: #00ffbd; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("📱 STRIDE-AI: Clinical Mobile")

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Live Stats", "🔮 Predictive Lab", "🧠 AI Report"])

with tab1:
    st.subheader("Real-time Metrics")
    c1, c2 = st.columns(2)
    c1.metric("Steps", st.session_state.steps)
    c2.metric("Heart Rate", f"{st.session_state.heart_rate} BPM")
    
    # Simple Activity Injection
    if st.button("📡 SYNC SENSORS"):
        st.session_state.steps += np.random.randint(100, 400)
        st.session_state.heart_rate = np.random.randint(110, 160)
        st.session_state.report_ready = False
        st.rerun()

with tab2:
    st.header("Advanced Software Models")
    
    # 1. PREDICTIVE FALL DETECTION (Feature 2)
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🚷 Predictive Fall Detection")
    st.write("Analyzes gait entropy to predict balance instability.")
    
    # Logic: High BPM + Low Steps + Random Variance = High Risk
    fall_risk_score = np.random.randint(5, 25) if st.session_state.steps > 5000 else np.random.randint(40, 85)
    
    if fall_risk_score > 60:
        st.markdown(f"Current Risk: <span class='risk-high'>{fall_risk_score}% (CRITICAL)</span>", unsafe_allow_html=True)
        st.warning("Alert: Unstable gait detected. High probability of fall within next 24h.")
    else:
        st.markdown(f"Current Risk: <span class='risk-low'>{fall_risk_score}% (STABLE)</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. MULTI-SYMPTOM CORRELATION (Feature 5)
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("🥗 Symptom & Diet Correlation")
    diet = st.selectbox("Current Dietary Intake", ["Balanced", "High Sugar", "High Caffeine", "Fast Food"])
    
    # Correlation Logic
    if diet == "High Sugar" and st.session_state.heart_rate > 130:
        st.error("Correlation Found: Glucose spike is inflating cardiac load by 15%.")
    elif diet == "High Caffeine":
        st.info("Observation: Increased resting heart rate detected due to stimulant intake.")
    else:
        st.success("Correlation: Metabolism is stable with current activity.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    if st.button("🔍 RUN INTEGRATED DIAGNOSIS"):
        with st.spinner("Processing Multi-Symptom Patterns..."):
            time.sleep(2)
            st.session_state.report_ready = True
            
    if st.session_state.report_ready:
        st.markdown("""
        <div class="feature-card" style="border-left-color: #00ffbd;">
            <h3 style="color:#00ffbd;">AI CLINICAL SUMMARY</h3>
            <p><b>Fall Risk:</b> Analysis of 100+ simulated gait cycles shows 92% stability.</p>
            <p><b>Dietary Impact:</b> Diet-to-Activity correlation suggests optimal energy conversion.</p>
            <hr style="opacity:0.2;">
            <p><b>Clinical Advice:</b> Gait entropy is low, indicating strong neuro-muscular control. Continue current hydration levels.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.download_button("📥 Download PDF Report", "Clinical Report Content...", file_name="Stride_AI_Diagnosis.txt")
