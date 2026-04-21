import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Clinical Station", layout="wide")

# --- 2. SESSION DATA ENGINE ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 120.0
if 'logs' not in st.session_state: st.session_state.logs = []

def add_log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{ts}] RX_SIGNAL: {msg}")

# --- 3. GLOBAL CALCULATIONS (FIXED ERROR) ---
# Inhe page logic se pehle rakhna zaroori hai
with st.sidebar:
    st.title("🛡️ STRIDE-AI CORE")
    st.markdown("---")
    u_age = st.slider("User Age", 15, 80, 22)
    u_weight = st.slider("Weight (kg)", 40, 120, 70)
    
    # VO2 Max calculation (Accessible by ALL pages)
    vo2_val = round(15 * ((220 - u_age) / st.session_state.heart_rate), 1)
    
    st.markdown("### 🎛️ CONTROLS")
    if st.button("🚀 TRIGGER LIVE DATA"):
        st.session_state.steps += np.random.randint(150, 400)
        st.session_state.heart_rate = np.random.randint(115, 155)
        st.session_state.calories += round((u_weight * 0.06), 2)
        add_log(f"Packet received. New Step Count: {st.session_state.steps}")
        st.rerun()

    page = st.radio("HUB NAVIGATION", ["Executive Dashboard", "Neural Kinetics", "AI Clinical Report"])

# --- 4. STYLING ---
st.markdown("""
<style>
    .stApp { background: #020408; color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    .metric-card { background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; text-align: center; border-top: 3px solid #3b82f6; }
    .terminal-box { background: #000; color: #00ff41; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.75rem; height: 100px; overflow-y: auto; border: 1px solid #333; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 5. TOP NEURAL LOG ---
st.markdown("### 🧬 SYSTEM NEURAL LOG")
logs_display = "".join([f"<div>{l}</div>" for l in st.session_state.logs[-3:]])
st.markdown(f'<div class="terminal-box">{logs_display}</div>', unsafe_allow_html=True)

# --- 6. PAGE: EXECUTIVE DASHBOARD ---
if page == "Executive Dashboard":
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><small>TOTAL STEPS</small><h2>{st.session_state.steps}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><small>CURRENT BPM</small><h2>{st.session_state.heart_rate}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><small>VO2 MAX (est)</small><h2>{vo2_val}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><small>KCAL BURN</small><h2>{int(st.session_state.calories)}</h2></div>', unsafe_allow_html=True)

    # Multi-Axis Motion Graph
    st.markdown("### 📊 Tri-Axial Kinetic Telemetry")
    t = np.linspace(0, 10, 100)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=np.sin(t)+np.random.normal(0,0.1,100), name='X (Stance)', line_color='#3b82f6'))
    fig.add_trace(go.Scatter(x=t, y=np.cos(t)+np.random.normal(0,0.1,100), name='Y (Swing)', line_color='#00ffbd'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- 7. PAGE: NEURAL KINETICS (New Advance Feature) ---
elif page == "Neural Kinetics":
    st.title("🧠 Neural Stride Entropy")
    st.write("Analyzing spatiotemporal variability in walking patterns.")
    
    # 3D Spiral visualizing Gait Stability
    z = np.linspace(0, 10, 200)
    x = np.cos(z) * (st.session_state.steps / 2000)
    y = np.sin(z) * (st.session_state.heart_rate / 50)
    fig_3d = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='#3b82f6', width=6))])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_3d, use_container_width=True)

# --- 8. PAGE: AI CLINICAL REPORT (FIXED & ENHANCED) ---
elif page == "AI Clinical Report":
    st.title("📋 Advanced Bio-Diagnostic Hub")
    
    # Advanced logic for risk
    risk_score = (st.session_state.heart_rate / (220-u_age)) * 100
    risk_level = "CRITICAL" if risk_score > 85 else "OPTIMAL" if risk_score < 70 else "MODERATE"
    risk_color = "#ff4b4b" if risk_level == "CRITICAL" else "#00ffbd" if risk_level == "OPTIMAL" else "#fbbf24"
    
    st.markdown(f"""
    <div style="background: #0d1117; padding: 30px; border-radius: 15px; border: 1px solid {risk_color};">
        <h2 style="color: {risk_color}; margin: 0;">BIO-DIAGNOSTIC STATUS: {risk_level}</h2>
        <hr style="opacity: 0.1; margin: 20px 0;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div>
                <p><b>Metabolic Age:</b> {u_age - 3 if st.session_state.steps > 7000 else u_age + 2} yrs</p>
                <p><b>Cardiac Load:</b> {int(risk_score)}% of max capacity</p>
            </div>
            <div>
                <p><b>VO2 Max Insight:</b> {vo2_val} mL/kg/min</p>
                <p><b>Gait Stability:</b> 94.2% (High Correlation)</p>
            </div>
        </div>
        <div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 10px; margin-top: 25px; border-left: 5px solid #3b82f6;">
            <b>AI Clinical Assessment:</b> Based on current telemetry, user is in <b>Aerobic Zone 2</b>. 
            The VO2 Max of {vo2_val} suggests high efficiency in oxygen utilization. 
            Recommended action: Maintain intensity for 15 more minutes to optimize lipid metabolism.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Comparison Table
    st.markdown("### 📊 Cross-Reference Benchmarks")
    df_bench = pd.DataFrame({
        "Metric": ["Steps", "BPM", "Metabolic Age", "VO2 Max"],
        "Current": [st.session_state.steps, st.session_state.heart_rate, u_age - 3 if st.session_state.steps > 7000 else u_age + 2, vo2_val],
        "WHO Goal": ["10,000", "60-100", f"< {u_age}", "> 40.0"]
    })
    st.table(df_bench)
