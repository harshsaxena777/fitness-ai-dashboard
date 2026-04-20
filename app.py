import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

# --- 2. MIDNIGHT & STATE MANAGEMENT ---
current_date = datetime.now().strftime("%Y-%m-%d")

if 'last_reset_date' not in st.session_state:
    st.session_state.last_reset_date = current_date

# Auto-reset at midnight
if st.session_state.last_reset_date != current_date:
    st.session_state.steps = 0
    st.session_state.heart_rate = 72
    st.session_state.calories = 0.0
    st.session_state.last_reset_date = current_date

# Initialize values if not present
if 'steps' not in st.session_state:
    st.session_state.steps = 0
if 'heart_rate' not in st.session_state:
    st.session_state.heart_rate = 72
if 'calories' not in st.session_state:
    st.session_state.calories = 0.0

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
    
    .report-box {
        background: #111;
        border-left: 5px solid #3b82f6;
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
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
    
    # Live Action Controls
    st.markdown("### 🎛️ CONTROL PANEL")
    if st.button("🚀 TRIGGER LIVE WALK"):
        st.session_state.steps += np.random.randint(15, 30)
        st.session_state.heart_rate = np.random.randint(110, 138)
        st.session_state.calories += round(np.random.uniform(0.9, 1.8), 2)
        st.toast("Capturing motion vectors...")
        
    if st.button("🔄 SYSTEM REBOOT"):
        st.session_state.steps = 0
        st.session_state.heart_rate = 72
        st.session_state.calories = 0.0
        st.rerun()

    st.markdown("---")
    st.markdown(f"<p style='font-size:0.8rem;'><span class='live-dot'></span> TELEMETRY: ACTIVE</p>", unsafe_allow_html=True)
    st.caption(f"Last Reset: {st.session_state.last_reset_date}")

# --- 5. PAGE LOGIC ---

if page == "[01] Step Analytics":
    st.title("Kinetic Volume Analytics")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="research-card"><p class="stat-label">Total Volume</p><p class="stat-value">{st.session_state.steps}</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="research-card"><p class="stat-label">Velocity</p><p class="stat-value">1.4 m/s</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="research-card"><p class="stat-label">Compliance</p><p class="stat-value">92%</p></div>', unsafe_allow_html=True)
    
    t = np.linspace(0, 10, 50)
    steps_trend = np.cumsum(np.random.normal(5, 2, 50)) + st.session_state.steps
    fig = go.Figure(go.Scatter(x=t, y=steps_trend, fill='tozeroy', line_color='#3b82f6', mode='lines+markers'))
    fig.update_layout(template="plotly_dark", title="Spatial Motion Waveform", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif page == "[02] Caloric Detector":
    st.title("Metabolic Expenditure")
    kcal = st.session_state.calories
    status = "✅ OPTIMAL" if kcal < 500 else "⚡ HIGH INTENSITY"
    color = "#00ffbd" if kcal < 500 else "#fbbf24"
    
    st.markdown(f"""
        <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:40px; text-align:center;">
            <p style="color:{color}; font-weight:900; margin:0;">{status}</p>
            <h1 style="margin:0; font-size:5rem; color:white;">{kcal}</h1>
            <p>KCAL EXPENDED</p>
        </div>
    """, unsafe_allow_html=True)

elif page == "[04] Heart Beat Analysis":
    st.title("Hemodynamic Telemetry")
    bpm = st.session_state.heart_rate
    color = "#ff4b4b" if bpm > 110 else "#00ffbd"
    
    st.markdown(f"""
        <div style="background:{color}22; border: 2px solid {color}; border-radius:20px; padding:40px; text-align:center;">
            <h1 style="margin:0; font-size:6rem; color:white;">{bpm}</h1>
            <p style="color:{color}; font-weight:900;">LIVE BPM ANALYSIS</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Live Waveform
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (bpm/60) * x)
    fig = go.Figure(go.Scatter(x=x, y=y, line_color=color))
    fig.update_layout(template="plotly_dark", height=300, xaxis_visible=False, yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

elif page == "[05] AI Health Report":
    st.title("Smart Diagnostic Engine")
    
    if st.button("🔍 INITIATE BIO-SCAN"):
        with st.status("Accessing Neural Core...", expanded=True) as status:
            time.sleep(1)
            st.write("Aggregating daily kinetics...")
            time.sleep(1)
            st.write("Comparing against WHO health standards...")
            status.update(label="Scan Complete!", state="complete")

        st.markdown(f"""
        <div class="report-box">
            <h2 style="color:#3b82f6; margin-top:0;">STRIDE-AI CLINICAL SUMMARY</h2>
            <p style="font-family:monospace; opacity:0.6;">REF ID: SA-{''.join(np.random.choice(list('0123456789ABC'), 6))}</p>
            <hr style="opacity:0.1;">
            <p><b>Analysis for Harsh Saxena:</b></p>
            <ul>
                <li><b>Mobility:</b> You have covered <b>{st.session_state.steps} steps</b>. {'Target not met. Recommendation: Walk 20 mins more.' if st.session_state.steps < 5000 else 'Great mobility volume detected!'}</li>
                <li><b>Cardiac:</b> Last detected BPM was <b>{st.session_state.heart_rate}</b>. Status: <b>{'Stable' if st.session_state.heart_rate < 100 else 'Elevated (Post-Activity)'}</b>.</li>
                <li><b>Metabolic:</b> {st.session_state.calories} kcal burned. Fuel source: <b>Lipid Dominant</b>.</li>
            </ul>
            <p style="background:#3b82f622; padding:10px; border-radius:5px; border-left:3px solid #3b82f6;">
                <b>AI Suggestion:</b> Based on your gait symmetry and caloric burn, we suggest increasing hydration by 500ml today.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("📥 EXPORT MEDICAL PDF", data="[Simulated PDF Content]", file_name="Stride_Report.pdf")

else: # Neural Motion Page
    st.title("Neural Motion & Gait")
    st.info("Visualizing 3D Stride Morphology...")
    z = np.linspace(0, 1, 100)
    fig_3d = go.Figure(data=[go.Scatter3d(x=np.cos(z*10), y=np.sin(z*10), z=z, mode='lines', line=dict(color='#3b82f6', width=8))])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_3d, use_container_width=True)
