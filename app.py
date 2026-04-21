import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Professional Workstation", layout="wide")

# --- 2. SESSION STATE ENGINE ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 145.0
if 'entropy_history' not in st.session_state: st.session_state.entropy_history = list(np.random.uniform(0.3, 0.5, 10))
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 3. SIDEBAR & CALCULATIONS ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6;'>STRIDE-AI PRO</h1>", unsafe_allow_html=True)
    u_age = st.slider("Subject Age", 18, 80, 22)
    u_weight = st.slider("Weight (kg)", 40, 150, 70)
    
    st.markdown("---")
    if st.button("🚀 INJECT KINETIC DATA"):
        st.session_state.steps += np.random.randint(300, 800)
        st.session_state.heart_rate = np.random.randint(115, 160)
        st.session_state.calories += round((u_weight * 0.055), 2)
        st.session_state.entropy_history.append(np.random.uniform(0.2, 0.6))
        st.session_state.report_ready = False # Reset report on new data
        st.rerun()

# Global Stats
max_hr = 220 - u_age
vo2_val = round(15 * (max_hr / st.session_state.heart_rate), 1)
stability_index = round(100 - (np.std(st.session_state.entropy_history) * 100), 2)

# --- 4. TABS INTERFACE ---
tab1, tab2, tab3, tab4 = st.tabs([
    "👣 GAIT & STEPS", 
    "🫀 CARDIAC LAB", 
    "🔥 METABOLIC DATA", 
    "🧠 AI CLINICAL REPORT"
])

# --- WINDOW 1: GAIT ---
with tab1:
    st.header("Kinetic Stride Analytics")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Total Steps", st.session_state.steps)
        st.metric("Gait Stability", f"{stability_index}%")
    with c2:
        fig_gait = px.line(y=st.session_state.entropy_history[-10:], title="Stochastic Stride Variability", template="plotly_dark")
        st.plotly_chart(fig_gait, use_container_width=True)

# --- WINDOW 2: HEART RATE ---
with tab2:
    st.header("Cardiac Telemetry")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pulse Rate", f"{st.session_state.heart_rate} BPM")
        st.progress(st.session_state.heart_rate / 200)
    with col2:
        fig_hr = go.Figure(go.Indicator(mode="gauge+number", value=st.session_state.heart_rate, gauge={'axis':{'range':[40,200]}, 'bar':{'color':"#ef4444"}}))
        st.plotly_chart(fig_hr, use_container_width=True)

# --- WINDOW 3: CALORIES ---
with tab3:
    st.header("Metabolic Flux")
    st.metric("Burned Calories", f"{int(st.session_state.calories)} kcal")
    st.bar_chart(np.random.randint(10, 50, 10))

# --- WINDOW 4: THE BIG AI REPORT WINDOW ---
with tab4:
    st.header("🛡️ Secure AI Diagnostic Portal")
    
    # ACTION BUTTONS
    btn_col1, btn_col2 = st.columns([1, 4])
    
    with btn_col1:
        if st.button("🔍 GENERATE AI REPORT"):
            with st.spinner("Analyzing Bio-Kinetic Patterns..."):
                time.sleep(2) # Fake "AI Processing" delay
                st.session_state.report_ready = True
    
    if st.session_state.report_ready:
        risk_status = "HEALTHY" if vo2_val > 32 else "MODERATE RISK"
        status_color = "#00ffbd" if risk_status == "HEALTHY" else "#fbbf24"
        
        # The Professional Report UI
        st.markdown(f"""
        <div style="background: #0d1117; padding: 30px; border-radius: 15px; border-left: 10px solid {status_color}; margin-top: 20px;">
            <h2 style="color: {status_color};">BIO-CLINICAL SUMMARY: {risk_status}</h2>
            <hr style="opacity: 0.1;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <p><b>Subject Age:</b> {u_age} | <b>Metabolic Age:</b> {u_age - 2 if st.session_state.steps > 8000 else u_age + 1}</p>
                    <p><b>VO2 Max Estimate:</b> {vo2_val} mL/kg/min</p>
                    <p><b>Gait Entropy Index:</b> {round(np.mean(st.session_state.entropy_history), 3)}</p>
                </div>
                <div>
                    <p><b>Stability Rating:</b> {stability_index}% (Optimal)</p>
                    <p><b>Active Calorie Burn:</b> {int(st.session_state.calories)} kcal</p>
                    <p><b>Cardiac Response:</b> Normal Sinus Rhythm (Simulated)</p>
                </div>
            </div>
            <div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; margin-top: 25px; border-left: 5px solid #3b82f6;">
                <b>🧠 AI CLINICIAN INSIGHT:</b><br>
                Based on the current step count of {st.session_state.steps} and a Heart Rate of {st.session_state.heart_rate} BPM, 
                the subject's VO2 Max is estimated at {vo2_val}. Stride regularity is within clinical parameters. 
                <b>Recommendation:</b> Maintain current activity level to optimize aerobic conditioning.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # DOWNLOAD SECTION
        st.markdown("---")
        report_text = f"Patient Report\nSteps: {st.session_state.steps}\nBPM: {st.session_state.heart_rate}\nVO2Max: {vo2_val}\nStatus: {risk_status}"
        
        st.download_button(
            label="📥 DOWNLOAD CLINICAL REPORT (.TXT)",
            data=report_text,
            file_name=f"Stride_AI_Report_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    else:
        st.info("System Ready. Please click 'Generate AI Report' to initiate physiological analysis.")
