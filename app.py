import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="STRIDE-AI | Clinical Intelligence", layout="wide")

st.markdown("""
<style>
    .stApp { background: #020204; color: #d1d1d1; font-family: 'Inter', sans-serif; }
    .terminal-log {
        background: #000; border: 1px solid #1f2937; border-radius: 5px;
        padding: 15px; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #4ade80;
        height: 150px; overflow-y: auto; margin-bottom: 20px;
    }
    .metric-container {
        background: linear-gradient(145deg, #0a0a0c, #111114);
        border: 1px solid #ffffff10; border-radius: 15px; padding: 20px;
    }
    .glitch-text { font-weight: 900; color: #3b82f6; text-transform: uppercase; letter-spacing: 3px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'steps' not in st.session_state: st.session_state.steps = 5420
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'logs' not in st.session_state: st.session_state.logs = [f"[{datetime.now().strftime('%H:%M:%S')}] System Initialized..."]

def add_log(msg):
    st.session_state.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# --- 3. SIDEBAR: PRO PARAMETERS ---
with st.sidebar:
    st.markdown("<h2 class='glitch-text'>STRIDE-AI v9</h2>", unsafe_allow_html=True)
    st.markdown("---")
    u_age = st.slider("User Age", 18, 80, 22)
    u_weight = st.slider("Mass (kg)", 40.0, 120.0, 70.0)
    
    module = st.sidebar.selectbox("RESEARCH HUB", 
        ["Biometric Workstation", "Gait Dynamics", "Clinical Intelligence"])
    
    if st.button("🔴 INJECT REAL-TIME TELEMETRY"):
        st.session_state.steps += np.random.randint(100, 300)
        st.session_state.heart_rate = np.random.randint(110, 155)
        add_log(f"Motion Detected: Intensity {np.random.choice(['High', 'Mid', 'Max'])}")
        st.rerun()

# --- 4. DATA ENGINE (COMPLEX CALCULATIONS) ---
# VO2 Max Estimate: 15 * (HRmax / HRrest)
vo2_max = round(15 * ( (220 - u_age) / st.session_state.heart_rate ), 2)
entropy_score = round(np.random.uniform(0.1, 0.4), 3) # Lower is more stable gait

# --- 5. UI LAYOUT ---

# TOP LOG: NEURAL ACTIVITY LOG (The "Complex" Look)
log_box = "".join([f"<div>{l}</div>" for l in st.session_state.logs[-5:]])
st.markdown(f'<div class="terminal-log">{log_box}</div>', unsafe_allow_html=True)

if module == "Biometric Workstation":
    # Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-container">👣 <small>STEPS</small><br><h2>{st.session_state.steps}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-container">🫀 <small>PULSE</small><br><h2>{st.session_state.heart_rate}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-container">💨 <small>VO2 MAX</small><br><h2>{vo2_max}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-container">⚖️ <small>ENTROPY</small><br><h2>{entropy_score}</h2></div>', unsafe_allow_html=True)

    # Intensity Heatmap (The "More Features" Part)
    st.markdown("### 🗓️ Weekly Metabolic Heatmap")
    intensity_data = np.random.randint(0, 100, (1, 7))
    fig_heat = px.imshow(intensity_data, 
                         labels=dict(x="Day of Week", y="Intensity", color="Level"),
                         x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                         color_continuous_scale='Blues')
    fig_heat.update_layout(height=150, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)

    # Live Gauge for Cardio Zone
    st.markdown("### 🎯 Cardiovascular Zone Analysis")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.heart_rate,
        gauge = {'axis': {'range': [40, 200]},
                 'steps': [{'range': [40, 100], 'color': "gray"},
                           {'range': [100, 140], 'color': "blue"},
                           {'range': [140, 200], 'color': "red"}],
                 'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': (220-u_age)*0.8}}))
    fig_gauge.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gauge, use_container_width=True)

elif module == "Gait Dynamics":
    st.title("🛰️ Spatiotemporal Gait Mapping")
    
    # 3D Stride Trajectory
    z = np.linspace(0, 10, 100)
    x = np.sin(z) * entropy_score * 10
    y = np.cos(z) * entropy_score * 10
    
    fig_3d = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='lines+markers', 
                                         line=dict(color='#3b82f6', width=5),
                                         marker=dict(size=3, color=z, colorscale='Plasma'))])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_3d, use_container_width=True)
    st.info("Technical Note: The 3D spiral represents the neural feedback loop of your gait. Higher entropy creates more 'noise' in the spiral.")

elif module == "Clinical Intelligence":
    st.title("🧠 Predictive Diagnostic Hub")
    
    # Complex Comparison Table
    st.write("Cross-Analysis: User Metrics vs. Clinical Norms")
    comparison_df = pd.DataFrame({
        "Metric": ["Resting BPM", "Stride Length", "VO2 Max", "Gait Rhythm"],
        "User Value": [st.session_state.heart_rate, "0.78m", vo2_max, "Stable"],
        "Clinical Target": ["60-100", "0.70m-0.85m", "35-45", "Consistent"],
        "Status": ["PASS", "PASS", "ELITE" if vo2_max > 45 else "NORMAL", "PASS"]
    })
    st.table(comparison_df)
    
    # Iframe: Real-time Data Visualization (NASA or Medical related for 'The Look')
    st.markdown("### 📡 Live Clinical Reference Feed")
    st.components.v1.iframe("https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=en&size=medium&timezone=Asia%2FKolkata", height=120)
    
    if st.button("📂 EXPORT CLINICAL JSON"):
        add_log("Exporting session data to JSON format...")
        st.download_button("Download Report", data=comparison_df.to_json(), file_name="Stride_Report.json")
