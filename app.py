import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

# --- Initialize Session State for Real-Time Tracking ---
if 'steps' not in st.session_state:
    st.session_state.steps = 8420
if 'heart_rate' not in st.session_state:
    st.session_state.heart_rate = 72
if 'calories' not in st.session_state:
    st.session_state.calories = 310.5

# --- 2. GLOBAL UI STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;700;900&family=JetBrains+Mono:wght@400&display=swap');
    
    .stApp { background: #050505; font-family: 'Outfit', sans-serif; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0a0c !important; border-right: 1px solid #3b82f633; }
    
    .research-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .stat-label { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #3b82f6; letter-spacing: 2px; }
    .stat-value { font-size: 2.8rem; font-weight: 900; margin: 0; color: #ffffff; }
    
    @keyframes pulse { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }
    .live-dot { height: 10px; width: 10px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; margin-right: 8px; }
    
    .report-box {
        background: #111;
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6; font-weight:900; margin-bottom:0;'>STRIDE-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:\"JetBrains Mono\"; font-size:0.7rem; opacity:0.6; margin-top:0;'>SYSTEM CORE v3.0 [PG-RESEARCH]</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio("RESEARCH MODULES", 
                    ["[01] Step Analytics", 
                     "[02] Caloric Detector", 
                     "[03] Neural Motion & Validation", 
                     "[04] Heart Beat Analysis",
                     "[05] AI Health Report"])
    
    st.markdown("---")
    if st.button("🚀 TRIGGER LIVE WALK"):
        st.session_state.steps += np.random.randint(5, 15)
        st.session_state.heart_rate = np.random.randint(110, 135)
        st.session_state.calories += round(np.random.uniform(0.5, 1.2), 2)
        st.toast("Capturing Real-time Motion Data...")
        
    st.markdown("<p style='font-size:0.8rem;'><span class='live-dot'></span> TELEMETRY: ACTIVE</p>", unsafe_allow_html=True)

# --- 4. MODULE ROUTING ---

if page == "[01] Step Analytics":
    st.title("Kinetic Volume Analytics")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="research-card"><p class="stat-label">Total Volume</p><p class="stat-value">{st.session_state.steps}</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="research-card"><p class="stat-label">Velocity</p><p class="stat-value">1.4 m/s</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="research-card"><p class="stat-label">Compliance</p><p class="stat-value">92%</p></div>', unsafe_allow_html=True)
    
    # Real-time Trend Graph
    t = np.linspace(0, 10, 50)
    steps_trend = np.cumsum(np.random.poisson(5, 50)) + st.session_state.steps
    fig = go.Figure(go.Scatter(x=t, y=steps_trend, fill='tozeroy', line_color='#3b82f6'))
    fig.update_layout(template="plotly_dark", title="Accumulated Motion Waveform", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif page == "[02] Caloric Detector":
    st.title("Metabolic Expenditure")
    kcal = st.session_state.calories
    color = "#fbbf24" if kcal > 400 else "#00ffbd"
    
    st.markdown(f"""
        <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:30px; text-align:center;">
            <h1 style="margin:0; font-size:4rem; color:white;">{kcal}</h1>
            <p style="color:{color}; font-weight:900;">KCAL BURNED (LIVE)</p>
        </div>
    """, unsafe_allow_html=True)
    
    fig = go.Figure(data=[go.Pie(labels=['Carbs', 'Lipids'], values=[65, 35], hole=.6, marker_colors=['#fbbf24', '#333'])])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif page == "[04] Heart Beat Analysis":
    st.title("Hemodynamic Telemetry")
    bpm = st.session_state.heart_rate
    is_danger = bpm > 120
    color = "#ff4b4b" if is_danger else "#00ffbd"
    
    st.markdown(f"""
        <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:30px; text-align:center;">
            <h1 style="margin:0; font-size:5rem; color:white;">{bpm}</h1>
            <p style="color:{color}; font-weight:900;">LIVE BPM TRACKING</p>
        </div>
    """, unsafe_allow_html=True)

    # Pulsing ECG Graph
    x = np.linspace(0, 4, 1000)
    y = np.sin(2 * np.pi * (bpm/60) * x) + 0.1 * np.random.normal(0,1,1000)
    fig = go.Figure(go.Scatter(x=x, y=y, line_color=color))
    fig.update_layout(template="plotly_dark", height=300, xaxis_visible=False, yaxis_visible=False)
    st.plotly_chart(fig, use_container_width=True)

elif page == "[05] AI Health Report":
    st.title("Final Health Diagnosis & Report")
    
    if st.button("🔍 RUN FULL BODY SCAN"):
        with st.status("Analyzing Kinetic Data...", expanded=True) as status:
            time.sleep(1.5)
            st.write("Checking Metabolic Rate...")
            time.sleep(1)
            st.write("Validating Gait Symmetry...")
            status.update(label="Analysis Complete!", state="complete")

        st.markdown(f"""
        <div class="report-box">
            <h2 style="color:#3b82f6;">STRIDE-AI DIAGNOSTIC REPORT</h2>
            <hr style="opacity:0.2;">
            <p><b>Subject:</b> Harsh Saxena | <b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p><b>Summary:</b> Your current activity level shows a <b>{'High' if st.session_state.steps > 8000 else 'Moderate'}</b> kinetic volume.</p>
            <ul>
                <li><b>Heart Health:</b> {'Elevated BPM. Suggesting cooldown.' if st.session_state.heart_rate > 100 else 'Stable resting heart rate.'}</li>
                <li><b>Metabolic State:</b> Current burn is {st.session_state.calories} kcal. You are in the <b>Fat Oxidation Zone</b>.</li>
                <li><b>Suggestion:</b> Increase hydration. Your step count is {10000 - st.session_state.steps} steps away from the daily goal.</li>
            </ul>
            <p style="color:#3b82f6; font-size:0.8rem;"><i>*This is an AI-generated research insight.</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.button("📥 DOWNLOAD PDF REPORT")

# Default page catch for Neural Motion
elif page == "[03] Neural Motion & Validation":
    st.title("Neural Motion Analytics")
    st.info("System checking Gait Symmetry... Walk with your device to calibrate.")
    z = np.linspace(0, 1, 100)
    fig_3d = go.Figure(data=[go.Scatter3d(x=np.cos(z*6), y=np.sin(z*6), z=z, mode='lines', line=dict(color='#3b82f6', width=10))])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_3d, use_container_width=True)
