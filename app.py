import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

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
    
    @keyframes heart-pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
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
                     "[04] Heart Beat Analysis"])
    
    st.markdown("---")
    st.markdown("<p style='font-size:0.8rem;'><span class='live-dot'></span> TELEMETRY: ACTIVE</p>", unsafe_allow_html=True)
    st.caption("AI Model: LSTM-CNN Hybrid")

# --- 4. MODULE ROUTING ---

# --- PAGE 1: KINETICS ---
if page == "[01] Step Analytics":
    st.title("Kinetic Volume Analytics")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="research-card"><p class="stat-label">Total Volume</p><p class="stat-value">10,372</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="research-card"><p class="stat-label">Velocity</p><p class="stat-value">1.4 m/s</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="research-card"><p class="stat-label">Compliance</p><p class="stat-value">92%</p></div>', unsafe_allow_html=True)
    
    t = np.linspace(0, 24, 100)
    steps = np.abs(np.sin(t/4) * 500 + np.random.normal(0, 50, 100))
    fig = go.Figure(go.Scatter(x=t, y=steps, fill='tozeroy', line_color='#3b82f6'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: METABOLICS ---
elif page == "[02] Caloric Detector":
    st.title("Metabolic Expenditure & AI Validation")
    
    kcal_burned = 412.08
    is_high_intensity = kcal_burned > 400
    color, status = ("#fbbf24", "⚡ GLYCOGEN DEPLETION RISK") if is_high_intensity else ("#00ffbd", "✅ OPTIMAL BURN")

    c_box, c_diag = st.columns([1, 2])
    with c_box:
        st.markdown(f"""
            <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:30px; text-align:center;">
                <p style="color:{color}; font-weight:900; margin:0;">{status}</p>
                <h1 style="margin:0; font-size:3rem; color:white;">{kcal_burned}</h1>
                <small>KCAL DETECTED</small>
            </div>
        """, unsafe_allow_html=True)
    with c_diag:
        if is_high_intensity:
            st.warning("**AI Analysis:** High metabolic intensity detected. Substrate shift to glucose utilization.")
            st.markdown("- **Precaution:** Consume electrolytes and fast carbohydrates.")
            st.markdown("- **Precaution:** Monitor for lactate threshold fatigue.")
        else:
            st.success("**AI Analysis:** Metabolic rate stable. Fat-oxidation optimized.")

    fig = go.Figure(data=[go.Pie(labels=['Carbs', 'Lipids'], values=[70, 30], hole=.6, marker_colors=['#fbbf24', '#333'])])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 3: NEURAL MOTION ---
elif page == "[03] Neural Motion & Validation":
    st.title("Neural Motion Analytics & AI Prescription")
    
    symmetry = 0.82 
    is_anomaly = symmetry < 0.85
    color, status = ("#f87171", "⚠️ ANOMALY DETECTED") if is_anomaly else ("#00ffbd", "✅ MOTION VALIDATED")

    c_box, c_diag = st.columns([1, 2])
    with c_box:
        st.markdown(f"""
            <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:30px; text-align:center;">
                <p style="color:{color}; font-weight:900; margin:0;">{status}</p>
                <h1 style="margin:0; font-size:3.5rem; color:white;">{int(symmetry*100)}%</h1>
                <small>GAIT SCORE</small>
            </div>
        """, unsafe_allow_html=True)
    with c_diag:
        if is_anomaly:
            st.error(f"**Diagnostic:** Propulsion deficit of {int((1-symmetry)*100)}% in unilateral gait phase.")
            st.markdown("- **Precaution:** Reduce treadmill incline immediately.")
            st.markdown("- **Precaution:** Check for medial shoe-sole compression.")
        else:
            st.success("**Diagnostic:** Stride morphology is within optimal parameters.")

    z = np.linspace(0, 1, 100)
    fig_3d = go.Figure(data=[go.Scatter3d(x=np.cos(z*6), y=np.sin(z*6), z=z, mode='lines', line=dict(color=color, width=10))])
    fig_3d.update_layout(scene=dict(bgcolor="black", xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), paper_bgcolor='black', height=500, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig_3d, use_container_width=True)

# --- PAGE 4: HEART ANALYSIS ---
elif page == "[04] Heart Beat Analysis":
    st.title("Hemodynamic Telemetry & Cardiac Safety")
    
    current_bpm = 158
    is_danger = current_bpm > 150
    color, status = ("#ff4b4b", "🚨 ANAEROBIC THRESHOLD") if is_danger else ("#00ffbd", "✅ AEROBIC STABILITY")
    pulse_anim = "animation: heart-pulse 0.6s infinite;" if is_danger else ""

    c_box, c_diag = st.columns([1, 2])
    with c_box:
        st.markdown(f"""
            <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:30px; text-align:center; {pulse_anim}">
                <p style="color:{color}; font-weight:900; margin:0;">{status}</p>
                <h1 style="margin:0; font-size:4rem; color:white;">{current_bpm}</h1>
                <small>LIVE BPM</small>
            </div>
        """, unsafe_allow_html=True)
    with c_diag:
        if is_danger:
            st.error("**Cardiac Warning:** Cardiovascular strain high. Zone 5 training detected.")
            st.markdown("- **Precaution:** Immediate recovery: Reduce to walking pace.")
            st.markdown("- **Precaution:** Focus on deep nasal breathing.")
        else:
            st.success("**Cardiac AI:** Heart rate within endurance aerobic range.")

    x = np.linspace(0, 2, 500)
    y = np.sin(20*x) * np.exp(-x) 
    fig = go.Figure(go.Scatter(x=x, y=y, line_color='#ff4b4b'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250)
    st.plotly_chart(fig, use_container_width=True)
