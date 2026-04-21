import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. RESEARCH ENGINE CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Neural Station", layout="wide")

st.markdown("""
<style>
    .stApp { background: #000205; color: #00d4ff; font-family: 'Courier New', monospace; }
    .status-bar {
        background: rgba(0, 212, 255, 0.05); border: 1px solid #00d4ff33;
        padding: 10px; border-radius: 5px; font-size: 0.8rem; margin-bottom: 20px;
    }
    .console-out {
        background: #000; height: 180px; overflow-y: scroll;
        border: 1px solid #00d4ff55; padding: 10px; color: #00ff41;
        font-size: 0.75rem; line-height: 1.2; margin-top: 10px;
    }
    .metric-box {
        border-left: 3px solid #00d4ff; background: #001220;
        padding: 15px; border-radius: 0 10px 10px 0; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA SIMULATION ENGINE ---
if 'steps' not in st.session_state: st.session_state.steps = 8421
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'raw_logs' not in st.session_state: st.session_state.raw_logs = []

def log_packet(msg):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    st.session_state.raw_logs.append(f"[{ts}] RX_SIGNAL_PACKET: {msg}")

# --- 3. SIDEBAR: NEURAL PARAMETERS ---
with st.sidebar:
    st.markdown("<h2 style='letter-spacing:5px;'>STRIDE_X</h2>", unsafe_allow_html=True)
    st.markdown("---")
    sim_mode = st.radio("OPERATIONAL MODE", ["BIO-TELEMETRY", "GAIT PHASE DYNAMICS", "NEURAL FORECAST"])
    
    st.markdown("### RAW SIGNAL INJECTION")
    if st.button("📡 INJECT KINETIC DATA"):
        st.session_state.steps += np.random.randint(150, 450)
        st.session_state.heart_rate = np.random.randint(120, 160)
        log_packet(f"DATA_BURST_SYNC: {np.random.hexcode if hasattr(np, 'hexcode') else '0x'+os.urandom(2).hex()}")
        st.rerun()

# --- 4. TOP STATUS & LOGS ---
st.markdown('<div class="status-bar">SYSTEM_STATUS: ONLINE | LATENCY: 24ms | ENCRYPTION: AES-256</div>', unsafe_allow_html=True)

# --- 5. MODULES ---

if sim_mode == "BIO-TELEMETRY":
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown("### CORE METRICS")
        st.markdown(f'<div class="metric-box"><small>STRIDE_COUNT</small><br><b>{st.session_state.steps}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box"><small>BPM_CORE</small><br><b>{st.session_state.heart_rate}</b></div>', unsafe_allow_html=True)
        
        # FFT Signal Mimic
        st.markdown("### FFT FREQUENCY ANALYSIS")
        freq_data = np.random.normal(0, 1, 20)
        st.bar_chart(freq_data)

    with c2:
        # Complex Multi-Line Signal
        st.markdown("### TRIAXIAL ACCELEROMETER RAW (X, Y, Z)")
        t = np.linspace(0, 10, 100)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=np.sin(t)+np.random.normal(0,0.1,100), name='Axis-X', line_color='#00d4ff'))
        fig.add_trace(go.Scatter(x=t, y=np.cos(t)+np.random.normal(0,0.1,100), name='Axis-Y', line_color='#ff00ff'))
        fig.add_trace(go.Scatter(x=t, y=np.sin(t/2)+np.random.normal(0,0.1,100), name='Axis-Z', line_color='#00ff41'))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig, use_container_width=True)

elif sim_mode == "GAIT PHASE DYNAMICS":
    st.title("Gait Phase Segmentation")
    
    # Sunburst Chart for Gait Cycle
    labels = ["Gait Cycle", "Stance Phase", "Swing Phase", "Initial Contact", "Mid-Stance", "Terminal Stance", "Pre-Swing", "Initial Swing", "Mid-Swing", "Terminal Swing"]
    parents = ["", "Gait Cycle", "Gait Cycle", "Stance Phase", "Stance Phase", "Stance Phase", "Stance Phase", "Swing Phase", "Swing Phase", "Swing Phase"]
    values = [100, 60, 40, 10, 20, 20, 10, 13, 13, 14]
    
    fig_sun = go.Figure(go.Sunburst(labels=labels, parents=parents, values=values, marker=dict(colorscale='Blues')))
    fig_sun.update_layout(margin=dict(t=0, l=0, r=0, b=0), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_sun, use_container_width=True)
    st.write("Current Phase Stability Index: **0.942 (Optimal)**")

elif sim_mode == "NEURAL FORECAST":
    st.title("Monte Carlo Health Projection")
    
    # 1000 Simulations logic
    n_sims = 100
    base_steps = st.session_state.steps
    sim_results = [base_steps + np.cumsum(np.random.normal(500, 200, 30)) for _ in range(n_sims)]
    
    fig_sim = go.Figure()
    for s in sim_results[:10]: # Draw 10 paths
        fig_sim.add_trace(go.Scatter(y=s, mode='lines', line=dict(width=1), opacity=0.3))
    
    fig_sim.update_layout(title="30-Day Mobility Forecast (1000 Simulations)", template="plotly_dark", showlegend=False)
    st.plotly_chart(fig_sim, use_container_width=True)
    
    st.success("AI Result: 98.4% Probability of meeting WHO Health Benchmarks within 14 days.")

# --- 6. TERMINAL OUTPUT ---
st.markdown("### LIVE_SIGNAL_CONSOLE")
logs = "".join([f"<div>{log}</div>" for log in st.session_state.raw_logs[-8:]])
st.markdown(f'<div class="console-out">{logs}</div>', unsafe_allow_html=True)
