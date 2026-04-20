import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

# --- 2. MIDNIGHT RESET & STATE MANAGEMENT ---
current_date = datetime.now().strftime("%Y-%m-%d")

if 'last_reset_date' not in st.session_state:
    st.session_state.last_reset_date = current_date

# Auto-reset if date changed (Midnight)
if st.session_state.last_reset_date != current_date:
    st.session_state.steps = 0
    st.session_state.heart_rate = 72
    st.session_state.calories = 0.0
    st.session_state.last_reset_date = current_date

# Initialize session variables
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 0.0

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
    
    @keyframes pulse { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }
    .live-dot { height: 10px; width: 10px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; margin-right: 8px; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6; font-weight:900; margin-bottom:0;'>STRIDE-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:\"JetBrains Mono\"; font-size:0.7rem; opacity:0.6; margin-top:0;'>SYSTEM CORE v3.0 [PG-RESEARCH]</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio("RESEARCH MODULES", 
                    ["[01] Step Analytics", 
                     "[02] Caloric Detector", 
                     "[03] Neural Motion", 
                     "[04] Heart Beat Analysis",
                     "[05] AI Health Report"])
    
    st.markdown("---")
    st.markdown("### 🎛️ CONTROL PANEL")
    
    # Live Simulation Button
    if st.button("🚀 TRIGGER LIVE WALK"):
        st.session_state.steps += np.random.randint(20, 50)
        st.session_state.heart_rate = np.random.randint(115, 145)
        st.session_state.calories += round(np.random.uniform(1.5, 3.0), 2)
        st.toast("Capturing real-time telemetry...")
        
    # Manual Reset Button
    if st.button("🔄 SYSTEM REBOOT (0)"):
        st.session_state.steps = 0
        st.session_state.heart_rate = 72
        st.session_state.calories = 0.0
        st.rerun()

    st.markdown("---")
    st.markdown(f"<p style='font-size:0.8rem;'><span class='live-dot'></span> TELEMETRY: ACTIVE</p>", unsafe_allow_html=True)

# --- 5. PAGE MODULES ---

if page == "[01] Step Analytics":
    st.title("Kinetic Volume Analytics")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="research-card"><p class="stat-label">Total Steps</p><p class="stat-value">{st.session_state.steps}</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="research-card"><p class="stat-label">Velocity</p><p class="stat-value">1.4 m/s</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="research-card"><p class="stat-label">Compliance</p><p class="stat-value">92%</p></div>', unsafe_allow_html=True)
    
    # Real-time Movement Graph
    t = np.linspace(0, 10, 50)
    y = np.cumsum(np.random.poisson(5, 50)) + st.session_state.steps
    fig = go.Figure(go.Scatter(x=t, y=y, fill='tozeroy', line_color='#3b82f6', mode='lines'))
    fig.update_layout(template="plotly_dark", title="Spatial Motion Accumulation", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif page == "[02] Caloric Detector":
    st.title("Metabolic Expenditure")
    kcal = st.session_state.calories
    color = "#00ffbd" if kcal < 500 else "#fbbf24"
    
    st.markdown(f"""
        <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:40px; text-align:center;">
            <p style="color:{color}; font-weight:900; margin:0;">METABOLIC STATUS</p>
            <h1 style="margin:0; font-size:5rem; color:white;">{kcal}</h1>
            <p>TOTAL KCAL BURNED</p>
        </div>
    """, unsafe_allow_html=True)

elif page == "[04] Heart Beat Analysis":
    st.title("Hemodynamic Telemetry")
    bpm = st.session_state.heart_rate
    color = "#ff4b4b" if bpm > 120 else "#00ffbd"
    
    st.markdown(f"""
        <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:40px; text-align:center;">
            <h1 style="margin:0; font-size:6rem; color:white;">{bpm}</h1>
            <p style="color:{color}; font-weight:900;">LIVE PULSE (BPM)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Waveform Animation
    x = np.linspace(0, 4, 1000)
    y = np.sin(np.pi * (bpm/60) * x)
    fig = go.Figure(go.Scatter(x=x, y=y, line_color=color))
    fig.update_layout(template="plotly_dark", height=300, xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif page == "[05] AI Health Report":
    st.title("🛡️ AI Smart Diagnostic Engine")
    
    if st.button("🔍 INITIATE DEEP BIO-SCAN"):
        with st.status("Analyzing Live Metrics...", expanded=True) as status:
            time.sleep(1)
            st.write("Aggregating Stride Data...")
            time.sleep(1)
            st.write("Calculating Metabolic Age...")
            status.update(label="Scan Complete!", state="complete")

        # --- DYNAMIC REPORT LOGIC ---
        steps = st.session_state.steps
        bpm = st.session_state.heart_rate
        
        # 1. Activity Category
        if steps < 1000:
            cat, col, adv = "SEDENTARY", "#ff4b4b", "Risk of stiffness. Please initiate movement."
        elif 1000 <= steps < 8000:
            cat, col, adv = "MODERATELY ACTIVE", "#fbbf24", "Steady state. Good metabolic flow."
        else:
            cat, col, adv = "ATHLETIC", "#00ffbd", "Exceptional volume. Focus on muscle recovery."

        # 2. Cardiac State
        hr_stat = "⚠️ HIGH STRAIN" if bpm > 125 else "✅ STABLE"
        hr_adv = "Reduce pace. Focus on deep breathing." if bpm > 125 else "Heart health within endurance limits."

        # --- THE DYNAMIC REPORT BOX ---
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid {col}; border-radius: 20px; padding: 30px; margin-top: 20px;">
            <h2 style="color: {col}; margin: 0;">CLINICAL SUMMARY</h2>
            <hr style="opacity: 0.1; margin: 20px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <p style="color: #3b82f6; font-family: 'JetBrains Mono'; font-size: 0.8rem; margin: 0;">ACTIVITY STATUS</p>
                    <h3 style="margin: 5px 0;">{cat} ({steps} Steps)</h3>
                    <p style="font-size: 0.9rem; opacity: 0.8;">{adv}</p>
                </div>
                <div>
                    <p style="color: #3b82f6; font-family: 'JetBrains Mono'; font-size: 0.8rem; margin: 0;">CARDIAC TELEMETRY</p>
                    <h3 style="margin: 5px 0;">{hr_stat} ({bpm} BPM)</h3>
                    <p style="font-size: 0.9rem; opacity: 0.8;">{hr_adv}</p>
                </div>
            </div>
            <div style="margin-top: 30px; padding: 20px; background: rgba(59, 130, 246, 0.1); border-radius: 10px;">
                <p style="margin: 0; font-size: 0.85rem;">
                    <b>AI Prescription:</b> Based on daily analysis, your current <b>{st.session_state.calories} kcal</b> burn 
                    is {'optimal' if steps > 5000 else 'below threshold'}. Recommendation: 
                    {'Increase hydration immediately.' if bpm > 115 else 'Maintain current pace.'}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.info("Tip: Use Ctrl+P to save this dynamic report for your project documentation.")

else: # Neural Motion
    st.title("Neural Motion Analytics")
    st.info("Visualizing 3D Gait Morphology...")
    z = np.linspace(0, 1, 100)
    fig_3d = go.Figure(data=[go.Scatter3d(x=np.cos(z*10), y=np.sin(z*10), z=z, mode='lines', line=dict(color='#3b82f6', width=8))])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_3d, use_container_width=True)
