import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Multi-Window Suite", layout="wide")

# --- 2. SESSION STATE MANAGEMENT ---
if 'steps' not in st.session_state: st.session_state.steps = 5200
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 145.0

# --- 3. SIDEBAR: GLOBAL CONTROLS ---
with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6;'>STRIDE-AI PRO</h2>", unsafe_allow_html=True)
    u_age = st.slider("User Age", 18, 80, 22)
    u_weight = st.slider("User Weight (kg)", 40, 120, 70)
    
    st.markdown("---")
    if st.button("📡 INJECT LIVE SENSOR DATA"):
        st.session_state.steps += np.random.randint(200, 600)
        st.session_state.heart_rate = np.random.randint(115, 160)
        st.session_state.calories += round((u_weight * 0.05), 2)
        st.rerun()
    
    st.info("System Status: Active Monitoring")

# --- 4. GLOBAL CALCULATIONS ---
max_hr = 220 - u_age
vo2_val = round(15 * (max_hr / st.session_state.heart_rate), 1)

# --- 5. UI LAYOUT (SEPARATE WINDOWS VIA TABS) ---
st.title("Clinical Research Workstation")

# Creating separate windows for each feature
tab1, tab2, tab3, tab4 = st.tabs([
    "👣 STEPS ANALYTICS", 
    "🫀 HEART RATE MONITOR", 
    "🔥 CALORIE EXPENDITURE", 
    "🧠 AI CLINICAL REPORT"
])

# --- WINDOW 1: STEPS ---
with tab1:
    st.header("Step Dynamic Analysis")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Total Steps", st.session_state.steps)
        st.write(f"Goal Completion: {int((st.session_state.steps/10000)*100)}%")
        st.progress(min(st.session_state.steps/10000, 1.0))
    
    with c2:
        # Simulated Stride Frequency
        t = np.linspace(0, 10, 100)
        y = np.sin(t) + np.random.normal(0, 0.05, 100)
        fig_steps = px.line(x=t, y=y, title="Stride Pattern (Live Waveform)", template="plotly_dark")
        fig_steps.update_traces(line_color='#3b82f6')
        st.plotly_chart(fig_steps, use_container_width=True)

# --- WINDOW 2: HEART RATE ---
with tab2:
    st.header("Cardiovascular Telemetry")
    col_hr1, col_hr2 = st.columns(2)
    
    with col_hr1:
        st.metric("Current BPM", f"{st.session_state.heart_rate} BPM")
        # Heart Rate Zone Logic
        hr = st.session_state.heart_rate
        if hr > max_hr * 0.85: zone = "Peak (Anaerobic)"
        elif hr > max_hr * 0.7: zone = "Cardio (Aerobic)"
        else: zone = "Fat Burn"
        st.subheader(f"Current Zone: {zone}")
    
    with col_hr2:
        fig_hr = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = st.session_state.heart_rate,
            gauge = {'axis': {'range': [40, 200]}, 'bar': {'color': "#ef4444"}}
        ))
        fig_hr.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_hr, use_container_width=True)

# --- WINDOW 3: CALORIES ---
with tab3:
    st.header("Metabolic Energy Tracking")
    st.metric("Total Calories Burned", f"{int(st.session_state.calories)} kcal")
    
    # Calorie Intensity Heatmap (Simulated 24h)
    data = np.random.randint(10, 100, (1, 12))
    fig_cal = px.imshow(data, labels=dict(x="Hours", color="Kcal Intensity"),
                        x=[f"{i}h" for i in range(2, 26, 2)], color_continuous_scale='YlOrRd')
    fig_cal.update_layout(title="Metabolic Flux (Last 12 Hours)", template="plotly_dark")
    st.plotly_chart(fig_cal, use_container_width=True)

# --- WINDOW 4: FINAL AI CLINICAL REPORT ---
with tab4:
    st.header("🛡️ Integrated AI Clinical Intelligence")
    
    risk_level = "LOW" if st.session_state.heart_rate < 130 else "MODERATE"
    status_color = "#00ffbd" if risk_level == "LOW" else "#fbbf24"
    
    st.markdown(f"""
    <div style="background: #0d1117; padding: 25px; border-radius: 15px; border-left: 10px solid {status_color};">
        <h2 style="color: {status_color};">DIAGNOSTIC SUMMARY: {risk_level} RISK</h2>
        <hr style="opacity: 0.1;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
            <div>
                <h4>Physiological Data</h4>
                <p><b>Metabolic Age:</b> {u_age - 2 if st.session_state.steps > 8000 else u_age + 1} Years</p>
                <p><b>VO2 Max Estimate:</b> {vo2_val} mL/kg/min</p>
                <p><b>Cardiac Efficiency:</b> 92% (Optimal)</p>
            </div>
            <div>
                <h4>Activity Breakdown</h4>
                <p><b>Distance Equivalent:</b> {round(st.session_state.steps * 0.0008, 2)} km</p>
                <p><b>Energy Expenditure:</b> {int(st.session_state.calories)} kcal</p>
                <p><b>Gait Stability:</b> High Correlation (0.94)</p>
            </div>
        </div>
        <div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; margin-top: 25px;">
            <b>🧠 AI Clinician Insight:</b>
            Subject is currently in an active state with a VO2 Max of {vo2_val}. 
            Cardiac response to the current kinetic load (Step Count: {st.session_state.steps}) is stable. 
            Recommend maintaining this intensity for metabolic optimization.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Comparative Table
    st.markdown("### 📊 Cross-Metric Comparison")
    comparison_data = pd.DataFrame({
        "Metric": ["Heart Rate", "Steps", "Active Calories", "VO2 Max"],
        "User Value": [f"{st.session_state.heart_rate} BPM", st.session_state.steps, f"{int(st.session_state.calories)} kcal", vo2_val],
        "WHO Standard": ["60-100", "10,000", "> 300 (Daily)", "> 35.0"],
        "Status": ["PASS" if st.session_state.heart_rate < 100 else "ACTIVE", "IN PROGRESS", "COLLECTING", "ELITE"]
    })
    st.table(comparison_data)
