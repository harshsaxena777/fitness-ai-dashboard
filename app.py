import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# --- M.Tech Research Configuration ---
st.set_page_config(page_title="STRIDE-X | Biomechanical Twin", layout="wide")

# --- High-End CSS: Cyber-Research Aesthetic ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&family=Outfit:wght@300;700;900&display=swap');
    
    .stApp {
        background: #050505;
        font-family: 'Outfit', sans-serif;
        color: #e0e0e0;
    }
    
    /* Terminal Effect */
    .terminal-log {
        background: rgba(0, 20, 0, 0.9);
        border: 1px solid #00ff41;
        color: #00ff41;
        font-family: 'JetBrains Mono', monospace;
        padding: 15px;
        font-size: 0.75rem;
        border-radius: 5px;
        height: 150px;
        overflow-y: hidden;
        box-shadow: inset 0 0 10px #00ff4133;
    }

    /* Research Card */
    .research-card {
        background: linear-gradient(145deg, #111, #1a1a1a);
        border-left: 4px solid #3b82f6;
        padding: 20px;
        border-radius: 0 15px 15px 0;
        margin-bottom: 20px;
    }

    /* Data Glitch Highlight */
    .glitch-text {
        color: #3b82f6;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* Floating Metrics */
    .floater {
        border: 1px solid rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        background: rgba(255,255,255,0.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown("<h1 style='margin:0;'>STRIDE <span style='color:#3b82f6;'>X-1</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='opacity:0.5; margin:0;'>NEURAL BIOMECHANICS & KINETIC TELEMETRY</p>", unsafe_allow_html=True)
with c2:
    st.markdown("<br><div style='text-align:right;'><span style='background:#f8717133; color:#f87171; padding:5px 15px; border-radius:20px; font-size:0.8rem;'>LIVE TELEMETRY: CONNECTED</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- Layout: 3 Column Research View ---
left_col, mid_col, right_col = st.columns([1, 2, 1])

with left_col:
    st.markdown("#### [01] BIOMETRIC VECTORS")
    
    # Heart Rate with "Waveform" feel
    st.markdown("""
        <div class="research-card">
            <small>HEART RATE VARIABILITY (HRV)</small>
            <h2 style="color:#f87171; margin:0;">74.2 <span style="font-size:0.8rem;">ms</span></h2>
            <div style="height:2px; background:rgba(248,113,113,0.3); width:80%;"></div>
        </div>
    """, unsafe_allow_html=True)

    # Calories - High precision
    st.markdown("""
        <div class="research-card" style="border-left-color: #fbbf24;">
            <small>METABOLIC EXPENDITURE</small>
            <h2 style="color:#fbbf24; margin:0;">412.08 <span style="font-size:0.8rem;">kcal</span></h2>
            <p style="font-size:0.7rem; opacity:0.6;">Efficiency Index: 0.94 η</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Step Analytics with Stride Length
    st.markdown("""
        <div class="research-card" style="border-left-color: #4ade80;">
            <small>STRIDE MORPHOLOGY</small>
            <h2 style="color:#4ade80; margin:0;">0.78 <span style="font-size:0.8rem;">m/step</span></h2>
            <p style="font-size:0.7rem; opacity:0.6;">Anomalies Detected: 0.02%</p>
        </div>
    """, unsafe_allow_html=True)

with mid_col:
    st.markdown("#### [02] 3D KINETIC DIGITAL TWIN")
    
    # 3D Mesh / Scatter visualization of gait cycle
    t = np.linspace(0, 2*np.pi, 100)
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=np.cos(t), y=np.sin(t), z=t,
        mode='lines',
        line=dict(color='#3b82f6', width=10)
    )])
    fig_3d.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Live Spectral Analysis (FFT)
    st.markdown("#### GAIT FREQUENCY SPECTRUM (PSD)")
    freq = np.linspace(0, 5, 100)
    amp = np.exp(-freq) * np.random.normal(1, 0.05, 100)
    fig_fft = go.Figure(go.Scatter(x=freq, y=amp, fill='tozeroy', line_color='#3b82f6'))
    fig_fft.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=150, margin=dict(l=0,r=0,t=0,b=0),
                          xaxis=dict(title="Frequency (Hz)", color="gray"), yaxis=dict(visible=False))
    st.plotly_chart(fig_fft, use_container_width=True)

with right_col:
    st.markdown("#### [03] NEURAL LOGS")
    
    # Real-time Terminal Log
    log_entries = [
        f"[{datetime.now().strftime('%H:%M:%S')}] PACKET_RECIEVED: HEX_0x442",
        f"[{datetime.now().strftime('%H:%M:%S')}] LSTM_INFERENCE: SYMMETRY_OK",
        f"[{datetime.now().strftime('%H:%M:%S')}] CNN_FILTER: NOISE_REDUCED_12dB",
        f"[{datetime.now().strftime('%H:%M:%S')}] IMU_AXIS: X:0.02, Y:0.88, Z:0.12",
        f"[{datetime.now().strftime('%H:%M:%S')}] ANALYTICS: CALORIC_MODEL_STABLE"
    ]
    st.markdown(f"""
        <div class="terminal-log">
            { "<br>".join(log_entries) }
            <br> > SYSTEM_IDLE_LISTENING...
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # AI Confidence Gauge
    st.markdown("#### INFERENCE CONFIDENCE")
    st.markdown("""
        <div class="floater">
            <h1 style="color:#3b82f6; margin:0;">99.4%</h1>
            <small>MODEL RELIABILITY INDEX</small>
        </div>
    """, unsafe_allow_html=True)

# --- Footer System Status ---
st.markdown("---")
cols = st.columns(6)
status_labels = ["GPS: LOCK", "IMU: ACTIVE", "BTLE: 4.2", "MEM: 12GB", "LAT: 12ms", "VER: 2.04-STABLE"]
for i, status in enumerate(status_labels):
    cols[i].markdown(f"<small style='opacity:0.4;'>{status}</small>", unsafe_allow_html=True)
