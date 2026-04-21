import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

# --- 2. STATE MANAGEMENT & DATA INTEGRATION ---
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 0.0

# External Benchmark Data (Comparison Logic)
GLOBAL_STEP_AVG = 7500 

# --- 3. GLOBAL UI STYLING ---
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
    .report-box { background: #111; border-left: 5px solid #3b82f6; padding: 25px; border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.2); }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6; font-weight:900;'>STRIDE-AI</h1>", unsafe_allow_html=True)
    page = st.radio("RESEARCH MODULES", 
                    ["[01] Dashboard", "[02] Neural Motion", "[03] AI Health Report"])
    
    st.markdown("---")
    st.markdown("### 🎛️ SENSOR EMULATION")
    if st.button("🚀 TRIGGER MOTION"):
        st.session_state.steps += np.random.randint(25, 60)
        st.session_state.heart_rate = np.random.randint(110, 140)
        st.session_state.calories += round(np.random.uniform(1.5, 3.5), 2)
        st.rerun()
    
    if st.button("🔄 SYSTEM REBOOT"):
        st.session_state.steps = 0
        st.session_state.heart_rate = 72
        st.session_state.calories = 0.0
        st.rerun()

# --- 5. PAGE: DASHBOARD ---
if page == "[01] Dashboard":
    st.title("Kinetic Executive Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="research-card"><p class="stat-label">TOTAL STEPS</p><p class="stat-value">{st.session_state.steps}</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="research-card"><p class="stat-label">LIVE BPM</p><p class="stat-value">{st.session_state.heart_rate}</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="research-card"><p class="stat-label">KCAL BURN</p><p class="stat-value">{st.session_state.calories}</p></div>', unsafe_allow_html=True)

    # EXTERNAL INTEGRATION: IFRAME (Live Analytics Clock or Motion Visualization)
    st.markdown("### 🌐 External Telemetry Feed")
    # Embedding a clean, professional analog clock/data visualizer
    st.components.v1.iframe("https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=en&size=medium&timezone=Asia%2FKolkata", height=120)

    # Comparison Graph with External Benchmark
    st.markdown("### 📊 Global Benchmarking")
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Global Avg', x=['Steps'], y=[GLOBAL_STEP_AVG], marker_color='rgba(255,255,255,0.1)'))
    fig.add_trace(go.Bar(name='Current User', x=['Steps'], y=[st.session_state.steps], marker_color='#3b82f6'))
    fig.update_layout(template="plotly_dark", barmode='overlay', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig, use_container_width=True)

# --- 6. PAGE: AI HEALTH REPORT (DYNAMIC & COMPLEX) ---
elif page == "[03] AI Health Report":
    st.title("🛡️ AI Smart Diagnostic Engine")
    
    if st.button("🔍 INITIATE DEEP BIO-SCAN"):
        with st.status("Analyzing Live Metrics...", expanded=True) as status:
            time.sleep(1)
            st.write("Fetching Global Health Benchmarks...")
            time.sleep(1)
            st.write("Cross-referencing Cardiac Zones...")
            status.update(label="Scan Complete!", state="complete")

        steps = st.session_state.steps
        bpm = st.session_state.heart_rate
        
        # Complex Logic
        step_diff = GLOBAL_STEP_AVG - steps
        status_color = "#00ffbd" if steps > GLOBAL_STEP_AVG else "#fbbf24"
        
        st.markdown(f"""
        <div class="report-box" style="border-left-color: {status_color};">
            <h2 style="color: {status_color}; margin: 0;">CLINICAL SUMMARY</h2>
            <hr style="opacity: 0.1; margin: 15px 0;">
            <p><b>Global Comparison:</b> You are at <b>{int((steps/GLOBAL_STEP_AVG)*100)}%</b> of the international daily average.</p>
            <p><b>Diagnostic:</b> {'Optimal kinetic volume reached.' if steps > GLOBAL_STEP_AVG else f'Sedentary trend detected. Shortfall of {step_diff} steps.'}</p>
            <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;">
                <b>AI Prescription:</b> Based on {bpm} BPM, your cardiovascular strain is <b>{'High' if bpm > 120 else 'Normal'}</b>. 
                {'Immediate recovery suggested.' if bpm > 120 else 'Keep maintaining current pace for fat-oxidation.'}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 7. PAGE: NEURAL MOTION ---
else:
    st.title("Neural Motion Analytics")
    z = np.linspace(0, 1, 100)
    fig_3d = go.Figure(data=[go.Scatter3d(x=np.cos(z*10), y=np.sin(z*10), z=z, mode='lines', line=dict(color='#3b82f6', width=8))])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_3d, use_container_width=True)
