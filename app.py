import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI PRO | Analytics Suite", layout="wide")

# --- 2. DATASET INTEGRATION (External Dataset Simulation) ---
# Yahan hum ek external CSV load kar rahe hain (Global Health Benchmarks)
@st.cache_data
def load_global_data():
    data = {
        'Region': ['Asia', 'Europe', 'Americas', 'Africa', 'Global Avg'],
        'Avg_Steps': [6500, 8200, 7800, 9100, 7500],
        'Avg_BPM': [72, 70, 74, 68, 71]
    }
    return pd.DataFrame(data)

global_df = load_global_data()

# --- 3. STATE MANAGEMENT ---
if 'steps' not in st.session_state: st.session_state.steps = 4200
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 78
if 'calories' not in st.session_state: st.session_state.calories = 150.0

# --- 4. SIDEBAR & CONTROLS ---
with st.sidebar:
    st.title("🛡️ STRIDE-AI PRO")
    st.markdown("---")
    page = st.selectbox("CHOOSE MODULE", ["Executive Dashboard", "Global Benchmarking", "Neural Bio-Scan"])
    
    st.write("### 🎛️ Sensor Input")
    if st.button("🚀 Push Live Telemetry"):
        st.session_state.steps += 150
        st.session_state.heart_rate = np.random.randint(110, 140)
        st.session_state.calories += 12.5
        st.rerun()

# --- 5. PAGE 1: EXECUTIVE DASHBOARD ---
if page == "Executive Dashboard":
    st.header("Executive Kinetic Overview")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # COMPLEX METRIC: Gauge Chart for Heart Rate
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = st.session_state.heart_rate,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Live BPM Telemetry", 'font': {'size': 24}},
            delta = {'reference': 70, 'increasing': {'color': "red"}},
            gauge = {
                'axis': {'range': [None, 200]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 100], 'color': "rgba(0, 255, 0, 0.1)"},
                    {'range': [100, 150], 'color': "rgba(255, 255, 0, 0.1)"},
                    {'range': [150, 200], 'color': "rgba(255, 0, 0, 0.1)"}
                ],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Arial"})
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.metric("Metabolic Age", "22.4 yrs", "-1.2 vs last week")
        st.metric("Caloric Efficiency", f"{st.session_state.calories/200:.2f}%")
    
    with col3:
        # IFRAME INTEGRATION: External Resource
        st.markdown("### 📽️ Bio-Mechanics Feed")
        # Embedding a medical/fitness visualization or live clock
        st.components.v1.iframe("https://www.youtube.com/embed/S_8SizG91U4", height=200)

# --- 6. PAGE 2: GLOBAL BENCHMARKING (External Dataset Use) ---
elif page == "Global Benchmarking":
    st.header("Global Kinetic Positioning")
    st.write("Comparing your data against international health standards.")
    
    # User vs Global Data
    user_val = st.session_state.steps
    global_avg = global_df[global_df['Region'] == 'Global Avg']['Avg_Steps'].values[0]
    
    fig_bar = px.bar(global_df, x='Region', y='Avg_Steps', title="Regional Step Average vs You",
                     color='Avg_Steps', color_continuous_scale='Blues')
    # Adding a line for current user steps
    fig_bar.add_hline(y=user_val, line_dash="dot", line_color="red", 
                      annotation_text=f"Your Current Position: {user_val}")
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown(f"""
    <div style="background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 15px; border: 1px solid #3b82f6;">
        <h4>AI Insight:</h4>
        <p>You are currently <b>{int((user_val/global_avg)*100)}%</b> of the Global Daily Average. 
        To reach the European standard of 8,200 steps, you need to increase activity by <b>{max(0, 8200-user_val)}</b> steps today.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 7. PAGE 3: NEURAL BIO-SCAN ---
else:
    st.title("Neural Core Analysis")
    st.write("Analyzing Gait Entropy and Biometric Symmetry...")
    
    # Complex 3D Visualization
    t = np.linspace(0, 20, 200)
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=np.cos(t) * (st.session_state.steps/1000), 
        y=np.sin(t) * (st.session_state.heart_rate/50), 
        z=t,
        mode='lines+markers',
        line=dict(color='#3b82f6', width=5),
        marker=dict(size=2, color=t, colorscale='Viridis')
    )])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=700)
    st.plotly_chart(fig_3d, use_container_width=True)
