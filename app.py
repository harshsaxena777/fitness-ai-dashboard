import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# --- PG RESEARCH SUITE: CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

# --- GLOBAL CSS: RESEARCH LAB AESTHETIC ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;700;900&family=JetBrains+Mono:wght@400&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 50%, #101014 0%, #050505 100%);
        font-family: 'Outfit', sans-serif;
        color: #e0e0e0;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0c !important;
        border-right: 1px solid rgba(0, 242, 255, 0.2);
    }

    /* Research Card Styling */
    .research-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .stat-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #00f2ff;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .stat-value {
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(90deg, #fff, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    @keyframes pulse {
        0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; }
    }
    .live-dot {
        height: 10px; width: 10px; background-color: #ff4b4b; border-radius: 50%;
        display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #ff4b4b;
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#00f2ff; font-weight:900;'>STRIDE-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:"JetBrains Mono"; font-size:0.7rem; opacity:0.6;'>SYSTEM CORE v3.0</p>", unsafe_allow_html=True)
    page = st.radio("RESEARCH MODULES", ["Kinetics", "Metabolics", "Neural Motion", "Hemodynamics"])
    st.markdown("---")
    st.markdown("<p style='font-size:0.8rem;'><span class='live-dot'></span> TELEMETRY: ACTIVE</p>", unsafe_allow_html=True)

# --- LOGIC: MULTI-PAGE ROUTING ---
if page == "Kinetics":
    st.title("Step Analytics & Kinetic Load")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="research-card"><p class="stat-label">Total Volume</p><p class="stat-value">10,372</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="research-card"><p class="stat-label">Velocity</p><p class="stat-value">1.4 <small style="-webkit-text-fill-color: white;">m/s</small></p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="research-card"><p class="stat-label">Compliance</p><p class="stat-value">92<small style="-webkit-text-fill-color: white;">%</small></p></div>', unsafe_allow_html=True)
    
    t = np.linspace(0, 24, 100)
    y = np.abs(np.sin(t/4) * 500 + np.random.normal(0, 50, 100))
    fig = go.Figure(go.Scatter(x=t, y=y, fill='tozeroy', line_color='#00f2ff'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Metabolics":
    st.title("Metabolic Expenditure Analysis")
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown('<div class="research-card"><p class="stat-label">Session Burn</p><p class="stat-value" style="background: linear-gradient(90deg, #fff, #ffcc00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">412.08</p><p>kcal</p></div>', unsafe_allow_html=True)
    with col_r:
        fig = go.Figure(data=[go.Pie(labels=['Carbs', 'Lipids'], values=[70, 30], hole=.6, marker_colors=['#ffcc00', '#555'])])
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

elif page == "Neural Motion":
    st.title("LSTM Stride Morphology (3D)")
    z = np.linspace(0, 1, 100)
    fig = go.Figure(data=[go.Scatter3d(x=np.cos(z*6), y=np.sin(z*6), z=z, mode='lines', line=dict(color='#7000ff', width=10))])
    fig.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Hemodynamics":
    st.title("Cardiovascular Telemetry")
    m1, m2 = st.columns([1, 2])
    with m1:
        st.markdown('<div class="research-card"><p class="stat-label">BPM</p><p class="stat-value" style="background: linear-gradient(90deg, #fff, #ff4b4b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">74</p></div>', unsafe_allow_html=True)
    with m2:
        x = np.linspace(0, 2, 500)
        y = np.sin(20*x) * np.exp(-x) 
        fig = go.Figure(go.Scatter(x=x, y=y, line_color='#ff4b4b'))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
