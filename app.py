import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd  # <--- Yeh missing tha, ab fix ho gaya
import time
from datetime import datetime

# --- MOBILE OPTIMIZED CONFIG ---
st.set_page_config(
    page_title="STRIDE-AI Mobile", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE MANAGEMENT ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 145.0
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- STYLING FOR MOBILE ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #3b82f6;
        font-weight: bold;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
    }
    .report-box {
        background: #0d1117; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 8px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

st.title("📱 STRIDE-AI Mobile")

# --- DATA INJECTION ---
if st.button("📡 SYNC LIVE DATA"):
    with st.spinner("Fetching Sensor Data..."):
        time.sleep(1)
        st.session_state.steps += np.random.randint(200, 600)
        st.session_state.heart_rate = np.random.randint(110, 160)
        st.session_state.calories += 15.5
        st.session_state.report_ready = False
        st.rerun()

# --- TABS INTERFACE ---
tab1, tab2, tab3 = st.tabs(["📊 Stats", "🫀 Heart", "🧠 AI Report"])

with tab1:
    c1, c2 = st.columns(2)
    c1.metric("Steps", st.session_state.steps)
    c2.metric("Kcal", int(st.session_state.calories))
    
    st.write("### Stride Activity")
    # Fixed pandas data frame
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['Movement'])
    st.line_chart(chart_data)

with tab2:
    st.metric("Pulse", f"{st.session_state.heart_rate} BPM")
    fig_hr = go.Figure(go.Indicator(
        mode = "gauge+number", 
        value = st.session_state.heart_rate,
        gauge = {'axis': {'range': [40, 200]}, 'bar': {'color': "#ef4444"}}
    ))
    fig_hr.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_hr, use_container_width=True)

with tab3:
    st.write("### Clinical Intelligence")
    if st.button("🔍 GENERATE MOBILE REPORT"):
        with st.spinner("AI Analysis in progress..."):
            time.sleep(2)
            st.session_state.report_ready = True
    
    if st.session_state.report_ready:
        vo2_est = round(15 * (190/st.session_state.heart_rate), 1)
        st.markdown(f"""
        <div class="report-box">
            <h3 style="color:#3b82f6; margin-top:0;">Diagnostic Summary</h3>
            <p><b>VO2 Max Estimate:</b> {vo2_est} mL/kg/min</p>
            <p><b>Gait Stability:</b> 94% (Stable)</p>
            <p><b>Clinical Risk:</b> Low</p>
            <hr style="opacity:0.2;">
            <p style="font-size:0.9rem; color:#aaa;">
            <b>AI Advice:</b> Your heart rate recovery is optimal. Keep maintaining a consistent stride frequency.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple Download for Mobile
        st.download_button("📥 Save Report", "Steps: " + str(st.session_state.steps) + "\nBPM: " + str(st.session_state.heart_rate), file_name="Health_Report.txt")
