import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Research Station", layout="wide")

# --- 2. SESSION DATA ENGINE ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 120.0
if 'logs' not in st.session_state: st.session_state.logs = []

def add_log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{ts}] SIGNAL_REC: {msg}")

# --- 3. STYLING (The "Pro" Look) ---
st.markdown("""
<style>
    .stApp { background: #040508; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    .metric-card {
        background: #0d1117; border: 1px solid #30363d;
        padding: 20px; border-radius: 12px; text-align: center;
    }
    .terminal-box {
        background: #000; color: #00ff41; padding: 15px;
        border-radius: 8px; font-family: 'Courier New', monospace;
        font-size: 0.8rem; height: 120px; overflow-y: auto; border: 1px solid #333;
    }
    .risk-high { color: #ff4b4b; font-weight: bold; }
    .risk-low { color: #00ffbd; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: DATA INJECTION ---
with st.sidebar:
    st.title("🛡️ STRIDE-AI CORE")
    st.markdown("---")
    u_age = st.slider("User Age", 15, 80, 22)
    u_weight = st.slider("Weight (kg)", 40, 120, 70)
    
    st.markdown("### 🎛️ CONTROLS")
    if st.button("🚀 TRIGGER LIVE DATA"):
        st.session_state.steps += np.random.randint(100, 300)
        st.session_state.heart_rate = np.random.randint(110, 150)
        st.session_state.calories += round((u_weight * 0.05), 2)
        add_log(f"Received {st.session_state.steps} step-packets...")
        st.rerun()

    page = st.radio("HUB", ["Executive Dashboard", "Gait Dynamics", "AI Clinical Report"])

# --- 5. TOP LOG WINDOW ---
st.markdown("### 🧬 SYSTEM NEURAL LOG")
logs_display = "".join([f"<div>{l}</div>" for l in st.session_state.logs[-4:]])
st.markdown(f'<div class="terminal-box">{logs_display}</div>', unsafe_allow_html=True)

# --- 6. PAGE: EXECUTIVE DASHBOARD ---
if page == "Executive Dashboard":
    # 4 Main Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card">👣 <br>STEPS<br><h2>{st.session_state.steps}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card">🫀 <br>BPM<br><h2>{st.session_state.heart_rate}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card">🔥 <br>KCAL<br><h2>{int(st.session_state.calories)}</h2></div>', unsafe_allow_html=True)
    
    # Complex Calculation: VO2 Max Estimate
    vo2 = round(15 * ((220 - u_age) / st.session_state.heart_rate), 1)
    with c4: st.markdown(f'<div class="metric-card">💨 <br>VO2 MAX<br><h2>{vo2}</h2></div>', unsafe_allow_html=True)

    # Signal Graph (Triaxial Mimic)
    st.markdown("### 📡 Real-time Triaxial Signal Extraction")
    t = np.linspace(0, 10, 100)
    fig_sig = go.Figure()
    fig_sig.add_trace(go.Scatter(x=t, y=np.sin(t) + np.random.normal(0, 0.1, 100), name="X-Axis (Stability)", line_color="#3b82f6"))
    fig_sig.add_trace(go.Scatter(x=t, y=np.cos(t) + np.random.normal(0, 0.1, 100), name="Y-Axis (Momentum)", line_color="#00ffbd"))
    fig_sig.update_layout(template="plotly_dark", height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sig, use_container_width=True)

# --- 7. PAGE: GAIT DYNAMICS ---
elif page == "Gait Dynamics":
    st.title("⚖️ Gait Phase Segmentation")
    
    # Sunburst Chart for Walking Cycle
    fig_sun = go.Figure(go.Sunburst(
        labels=["Gait", "Stance (60%)", "Swing (40%)", "Heel Strike", "Mid-Stance", "Toe-Off", "Initial Swing", "Terminal Swing"],
        parents=["", "Gait", "Gait", "Stance (60%)", "Stance (60%)", "Stance (60%)", "Swing (40%)", "Swing (40%)"],
        values=[100, 60, 40, 20, 20, 20, 20, 20],
        marker=dict(colorscale='Blues')
    ))
    fig_sun.update_layout(margin=dict(t=0, l=0, r=0, b=0), paper_bgcolor='black', height=500)
    st.plotly_chart(fig_sun, use_container_width=True)
    
    st.info("Analysis: Stance-to-Swing ratio is within clinical norms (1.5:1). Gait symmetry: 94%.")

# --- 8. PAGE: AI CLINICAL REPORT ---
elif page == "AI Clinical Report":
    st.title("🧠 Clinical Intelligence Hub")
    
    # Risk Assessment Logic
    risk_level = "LOW" if st.session_state.heart_rate < 120 else "MODERATE"
    risk_class = "risk-low" if risk_level == "LOW" else "risk-high"
    
    st.markdown(f"""
    <div style="background: #111; padding: 25px; border-radius: 15px; border: 1px solid #333;">
        <h3>BIO-METRIC ANALYSIS REPORT</h3>
        <hr style="opacity: 0.1;">
        <p><b>Subject Age:</b> {u_age} | <b>Weight:</b> {u_weight} kg</p>
        <p><b>Calculated Risk Score:</b> <span class="{risk_class}">{risk_level}</span></p>
        <p><b>Metabolic Age Estimate:</b> {u_age - 2 if st.session_state.steps > 8000 else u_age + 1} years</p>
        <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;">
            <b>AI Recommendation:</b> Based on current VO2 Max of {vo2}, user is in 'Aerobic Zone 2'. 
            Continue intensity for optimal fat-oxidation. 
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Historical Benchmark Table
    st.markdown("### 📊 Clinical Benchmarks")
    bench_data = pd.DataFrame({
        "Parameter": ["Steps", "BPM", "Efficiency", "Phase Balance"],
        "User": [st.session_state.steps, st.session_state.heart_rate, "88%", "Stable"],
        "Target": ["10,000", "60-100", " >85%", "Symmetrical"]
    })
    st.table(bench_data)
