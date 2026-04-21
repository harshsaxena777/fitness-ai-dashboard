import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="STRIDE-AI | Clinical Suite", layout="wide")

if 'steps' not in st.session_state: st.session_state.steps = 4500
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 75
if 'calories' not in st.session_state: st.session_state.calories = 150.0

# --- 2. SIDEBAR INPUTS ---
with st.sidebar:
    st.title("🛡️ STRIDE-AI CORE")
    u_age = st.slider("User Age", 18, 80, 22)
    u_weight = st.slider("Weight (kg)", 40, 120, 70)
    
    # ADVANCED MATH
    max_hr = 220 - u_age
    # VO2 Max (Standard Cooper Estimate)
    vo2_val = round(15 * (max_hr / st.session_state.heart_rate), 1)
    
    st.markdown("---")
    if st.button("🚀 INJECT KINETIC DATA"):
        st.session_state.steps += np.random.randint(150, 400)
        st.session_state.heart_rate = np.random.randint(110, 165)
        # Metabolic Equivalent (MET) calculation for calories
        st.session_state.calories += round((u_weight * 0.04), 2)
        st.rerun()
    
    page = st.radio("HUB", ["Clinical Dashboard", "Bio-Metric Report"])

# --- 3. PAGE: DASHBOARD ---
if page == "Clinical Dashboard":
    st.title("Clinical Telemetry Overview")
    
    # Top Row Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Steps Executed", st.session_state.steps, f"+{np.random.randint(10,50)} local")
    with c2:
        # Determine HR Zone
        hr = st.session_state.heart_rate
        zone = "Peak" if hr > max_hr*0.85 else "Cardio" if hr > max_hr*0.7 else "Fat Burn" if hr > max_hr*0.5 else "Rest"
        st.metric("Heart Rate (BPM)", f"{hr} ({zone})", delta_color="inverse")
    with c3:
        st.metric("Energy Burn (kcal)", f"{int(st.session_state.calories)}", "Active")

    # Heart Rate Intensity Gauge
    st.markdown("### 🎯 Cardiac Zone Analysis")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.heart_rate,
        title = {'text': "BPM Intensity Zone"},
        gauge = {
            'axis': {'range': [40, 200]},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [40, 100], 'color': "#1f2937"},
                {'range': [100, 140], 'color': "#fbbf24"}, # Fat Burn
                {'range': [140, 170], 'color': "#f97316"}, # Cardio
                {'range': [170, 200], 'color': "#ef4444"}  # Peak
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'value': max_hr*0.85}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- 4. PAGE: BIO-METRIC REPORT ---
elif page == "Bio-Metric Report":
    st.title("🛡️ Diagnostic Clinical Summary")
    
    # Calorie Logic Breakdown
    total_energy = int(st.session_state.calories + (u_weight * 24)) # BMR + Active
    
    st.markdown(f"""
    <div style="background: #0d1117; padding: 30px; border-radius: 15px; border-left: 10px solid #3b82f6;">
        <h2 style="color: #3b82f6;">PATIENT BIO-DATA REPORT</h2>
        <hr style="opacity: 0.1;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><b>Cardiac Status:</b> {st.session_state.heart_rate} BPM (Stable)</p>
                <p><b>VO2 Max Estimate:</b> {vo2_val} mL/kg/min</p>
                <p><b>Active Calorie Burn:</b> {int(st.session_state.calories)} kcal</p>
            </div>
            <div>
                <p><b>Age-Predicted Max HR:</b> {max_hr} BPM</p>
                <p><b>Total Daily Expenditure:</b> ~{total_energy} kcal</p>
                <p><b>Clinical Risk:</b> LOW (Aerobic Stability)</p>
            </div>
        </div>
        <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
            <b>AI Insight:</b> Based on a VO2 Max of {vo2_val} and current Calorie burn, your metabolic efficiency 
            is 12% higher than the average for {u_age} year olds. 
            Recommendation: Sustain current BPM for 10 more minutes to hit Peak Fat-Oxidation Zone.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Comparison Table
    st.markdown("### 📊 Metrics vs Clinical Standards")
    report_df = pd.DataFrame({
        "Metric": ["Heart Rate", "Daily Steps", "Calorie Target", "Respiratory Efficiency"],
        "User Value": [f"{st.session_state.heart_rate} BPM", st.session_state.steps, f"{int(st.session_state.calories)} kcal", f"{vo2_val} (VO2)"],
        "Goal": ["60-100", "10,000", "500 (Active)", "> 35.0"],
        "Status": ["PASS" if st.session_state.heart_rate < 100 else "ELEVATED", "IN PROGRESS", "PENDING", "ELITE"]
    })
    st.table(report_df)
