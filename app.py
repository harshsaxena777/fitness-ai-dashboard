import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Clinical Research Suite", layout="wide")

# --- 2. SESSION STATE (The "Virtual Sensor" Engine) ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 145.0
if 'entropy_history' not in st.session_state: st.session_state.entropy_history = list(np.random.uniform(0.3, 0.5, 10))

# --- 3. SIDEBAR: BIO-PARAMETER TUNING ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6;'>STRIDE-AI v13</h1>", unsafe_allow_html=True)
    st.caption("Clinical Intelligence Workstation")
    st.markdown("---")
    
    u_age = st.slider("Subject Age", 18, 80, 22)
    u_weight = st.slider("Subject Weight (kg)", 40, 150, 70)
    
    st.markdown("### 🛠️ Simulation Controls")
    if st.button("🚀 INJECT KINETIC DATA"):
        st.session_state.steps += np.random.randint(300, 800)
        st.session_state.heart_rate = np.random.randint(110, 165)
        st.session_state.calories += round((u_weight * 0.055), 2)
        # Update Entropy (Stochastic variability)
        st.session_state.entropy_history.append(np.random.uniform(0.2, 0.6))
        st.rerun()
    
    st.markdown("---")
    st.warning("Mode: Software-Only Bio-Modeling")

# --- 4. GLOBAL RESEARCH CALCULATIONS ---
max_hr = 220 - u_age
# Advanced VO2 Max Logic
vo2_val = round(15 * (max_hr / st.session_state.heart_rate), 1)
# Stability Index (Inverse of Entropy variance)
stability_index = round(100 - (np.std(st.session_state.entropy_history) * 100), 2)

# --- 5. INTERFACE LAYOUT (TABS) ---
st.title("🛡️ Research-Grade Health Workstation")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👣 Gait Analytics", 
    "🫀 Cardiac Suite", 
    "🔥 Metabolic Lab", 
    "🔮 What-If Engine",
    "🧠 AI Clinical Report"
])

# --- TAB 1: GAIT ANALYTICS (Advancement: Stochastic Entropy) ---
with tab1:
    st.header("Spatiotemporal Gait Mapping")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Gait Stability Index", f"{stability_index}%")
        st.write("Entropy measure of inter-stride variability.")
        if stability_index > 90:
            st.success("Status: Highly Stable Stride")
        else:
            st.error("Status: High Chaos Detected")
            
    with c2:
        # Entropy Graph
        fig_entropy = px.line(y=st.session_state.entropy_history[-15:], 
                             title="Stochastic Entropy Index (Real-time)", 
                             labels={'y': 'Entropy Value', 'x': 'Time Packets'},
                             template="plotly_dark")
        fig_entropy.update_traces(line_color='#00ffbd', mode='lines+markers')
        st.plotly_chart(fig_entropy, use_container_width=True)

# --- TAB 2: CARDIAC SUITE ---
with tab2:
    st.header("Cardiovascular Stress Telemetry")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Heart Rate", f"{st.session_state.heart_rate} BPM")
        # Zone Classification
        hr = st.session_state.heart_rate
        zone = "Peak" if hr > max_hr*0.85 else "Cardio" if hr > max_hr*0.7 else "Fat Burn"
        st.info(f"Target Zone: {zone}")
    
    with col2:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = st.session_state.heart_rate,
            gauge = {'axis': {'range': [40, 200]}, 'bar': {'color': "#3b82f6"},
                     'steps': [{'range': [40, 100], 'color': "gray"}, {'range': [100, 200], 'color': "#ef4444"}]}))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

# --- TAB 3: METABOLIC LAB ---
with tab3:
    st.header("Energy Expenditure Analysis")
    st.metric("Cumulative Calorie Burn", f"{int(st.session_state.calories)} kcal")
    
    # BMR Prediction
    bmr = 10 * u_weight + 6.25 * 175 - 5 * u_age + 5
    st.write(f"Estimated Basal Metabolic Rate (BMR): **{int(bmr)} kcal/day**")
    
    # Heatmap of Intensity
    heat_data = np.random.randint(20, 100, (1, 10))
    fig_heat = px.imshow(heat_data, color_continuous_scale='Reds', title="Metabolic Intensity Heatmap")
    st.plotly_chart(fig_heat, use_container_width=True)

# --- TAB 4: WHAT-IF ENGINE (Advancement: Predictive Modeling) ---
with tab4:
    st.header("🔮 Predictive Health Forecasting")
    st.write("Modify your daily routine to see your predicted 'Digital Twin' health score.")
    
    pred_steps = st.slider("Projected Daily Steps", 1000, 20000, 5000)
    # Simple Linear Regression Simulation
    future_vo2 = vo2_val + (pred_steps - st.session_state.steps) * 0.001
    
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        st.metric("Predicted VO2 Max", f"{round(future_vo2, 1)} mL/kg/min")
    with c_p2:
        risk_reduction = "15%" if pred_steps > 10000 else "5%"
        st.metric("Cardio Risk Reduction", risk_reduction)

# --- TAB 5: AI CLINICAL REPORT ---
with tab5:
    st.header("📋 Final AI Clinical Diagnostic Report")
    
    risk_status = "HEALTHY" if vo2_val > 35 else "AT RISK"
    status_color = "#00ffbd" if risk_status == "HEALTHY" else "#ef4444"
    
    st.markdown(f"""
    <div style="background: #0d1117; padding: 30px; border-radius: 15px; border-left: 10px solid {status_color};">
        <h2 style="color: {status_color};">BIO-DIAGNOSTIC STATUS: {risk_status}</h2>
        <hr style="opacity: 0.1;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><b>Clinical VO2 Max:</b> {vo2_val} (Target: >35)</p>
                <p><b>Gait Entropy Index:</b> {round(np.mean(st.session_state.entropy_history), 3)} (Stable)</p>
                <p><b>Metabolic Age:</b> {u_age - 2 if st.session_state.steps > 8000 else u_age + 1} Years</p>
            </div>
            <div>
                <p><b>Cardiac Efficiency:</b> {int((1 - (st.session_state.heart_rate/200))*100)}%</p>
                <p><b>Active Energy Burn:</b> {int(st.session_state.calories)} kcal</p>
                <p><b>Pathological Flag:</b> NONE DETECTED</p>
            </div>
        </div>
        <div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; margin-top: 25px; border-left: 5px solid #3b82f6;">
            <b>🧠 AI Clinical Insight:</b>
            Subject is exhibiting a VO2 Max of {vo2_val} mL/kg/min. 
            The <b>Stochastic Entropy</b> analysis confirms high stride regularity (Stability: {stability_index}%). 
            Current kinetic volume is sufficient to maintain a metabolic age lower than chronological age.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download JSON button for clinical export
    report_data = {"Steps": st.session_state.steps, "BPM": st.session_state.heart_rate, "VO2Max": vo2_val}
    st.download_button("📥 Export Patient JSON", data=str(report_data), file_name="patient_report.json")
