import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI PRO | Clinical Suite", layout="wide")

# --- 2. SESSION STATE & DATA LOGGING ---
if 'steps' not in st.session_state: st.session_state.steps = 1250
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 45.0
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

# --- 3. SIDEBAR: ADVANCED CONTROLS ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6; font-weight:900;'>STRIDE-AI PRO</h1>", unsafe_allow_html=True)
    st.caption("v8.0 | Clinical Research Mode")
    st.markdown("---")
    
    # User Profile
    u_weight = st.number_input("Weight (kg)", 40, 150, 70)
    
    # Navigation
    page = st.selectbox("MODULE SELECTOR", 
                        ["Analytics Dashboard", "Gait Symmetry", "Health Projections", "Export Center"])
    
    st.markdown("---")
    if st.button("🚀 INJECT LIVE TELEMETRY"):
        st.session_state.steps += np.random.randint(50, 150)
        st.session_state.heart_rate = np.random.randint(110, 145)
        st.session_state.calories += round((u_weight * 0.05), 2)
        st.rerun()

# --- 4. THEME STYLING ---
st.markdown("""
<style>
    .stApp { background: #050505; color: #e0e0e0; }
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 15px; padding: 20px; text-align: center;
    }
    .stat-val { font-size: 2.2rem; font-weight: 800; color: #ffffff; }
    .stat-lab { font-size: 0.7rem; color: #3b82f6; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# --- 5. PAGE: DASHBOARD ---
if page == "Analytics Dashboard":
    # Top Row Metrics
    elapsed = str(timedelta(seconds=int(time.time() - st.session_state.start_time)))
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-card"><p class="stat-lab">STEPS</p><p class="stat-val">{st.session_state.steps}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><p class="stat-lab">PULSE</p><p class="stat-val">{st.session_state.heart_rate}</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card"><p class="stat-lab">METABOLIC</p><p class="stat-val">{st.session_state.calories} kcal</p></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><p class="stat-lab">UPTIME</p><p class="stat-val">{elapsed}</p></div>', unsafe_allow_html=True)

    # Iframe Clock Integration
    st.components.v1.iframe("https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=en&size=medium&timezone=Asia%2FKolkata", height=110)

    # Live Stride Frequency Wave
    st.markdown("### 📡 Real-time Stride Frequency (Hz)")
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.random.uniform(0.8, 1.2, 100)
    fig = px.line(x=x, y=y, template="plotly_dark")
    fig.update_traces(line_color='#3b82f6', fill='tozeroy')
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# --- 6. PAGE: GAIT SYMMETRY (Radar Chart) ---
elif page == "Gait Symmetry":
    st.title("⚖️ Gait Symmetry Analysis")
    st.write("Assessment of bilateral walking mechanics.")
    
    # Radar Chart Data
    categories = ['Stability', 'Rhythm', 'Velocity', 'Symmetry', 'Endurance']
    values = [85, 70, 92, 88, 65] # These can be dynamic based on steps
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=values, theta=categories, fill='toself', line_color='#00ffbd'
    ))
    fig_radar.update_layout(polar=dict(bgcolor="black", radialaxis=dict(visible=True, range=[0, 100])),
                           template="plotly_dark", paper_bgcolor='black')
    st.plotly_chart(fig_radar, use_container_width=True)
    st.info("AI Analysis: Your 'Endurance' score is lower than average. Consider interval training.")

# --- 7. PAGE: HEALTH PROJECTIONS (Predictive Graph) ---
elif page == "Health Projections":
    st.title("📈 Predictive Health Modeling")
    st.write("AI-driven forecast for the next 7 days based on current intensity.")
    
    days = [(datetime.now() + timedelta(days=i)).strftime('%d %b') for i in range(1, 8)]
    # Predictive logic (Current steps + daily increment)
    future_steps = [st.session_state.steps + (i * 1200) for i in range(1, 8)]
    
    fig_proj = px.bar(x=days, y=future_steps, labels={'x':'Date', 'y':'Predicted Steps'}, 
                      title="Step Forecast (LSTM Model)", color=future_steps, color_continuous_scale='Blues')
    st.plotly_chart(fig_proj, use_container_width=True)

# --- 8. PAGE: EXPORT CENTER (CSV Export) ---
elif page == "Export Center":
    st.title("📤 Research Data Export")
    st.write("Generate and download your activity log for clinical submission.")
    
    data_log = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Steps": [st.session_state.steps],
        "BPM": [st.session_state.heart_rate],
        "Calories": [st.session_state.calories]
    }
    df = pd.DataFrame(data_log)
    st.table(df)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 DOWNLOAD RESEARCH CSV", data=csv, file_name="StrideAI_Log.csv", mime="text/csv")
