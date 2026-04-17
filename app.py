import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(page_title="AI Stride - Advanced Health Hub", layout="centered")

# --- Enhanced Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(165deg, #1e1b4b 0%, #0f172a 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: white;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    
    .metric-value { font-size: 1.8rem; font-weight: 800; margin: 0; }
    .metric-label { font-size: 0.8rem; opacity: 0.6; margin: 0; text-transform: uppercase; }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-good { background: rgba(74, 222, 128, 0.2); color: #4ade80; }
    .status-alert { background: rgba(248, 113, 113, 0.2); color: #f87171; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("AI Stride")
menu = st.sidebar.selectbox("Go to", ["Live Dashboard", "Step Analytics", "Gait & AI Insights", "Awards"])

# --- Mock Data Engine ---
days = ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"]
steps = [8200, 10372, 4500, 7200, 9100, 11000, 10372]
bpm_history = np.random.randint(65, 85, size=24) # 24 hours of heart rate

if menu == "Live Dashboard":
    st.markdown("### Daily Overview")
    
    # --- Top Row: Dynamic Metrics ---
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f"""
            <div class="glass-card">
                <p class="metric-label">💓 Heart Rate</p>
                <p class="metric-value">74 <small style="font-size:1rem;">BPM</small></p>
                <span class="status-badge status-good">Normal</span>
            </div>
        """, unsafe_allow_html=True)
        
    with m2:
        # Simple calorie math: Steps * 0.04 (avg burn)
        calories = int(10372 * 0.04)
        st.markdown(f"""
            <div class="glass-card">
                <p class="metric-label">🔥 Calories</p>
                <p class="metric-value">{calories} <small style="font-size:1rem;">kcal</small></p>
                <span class="status-badge status-good">85% of goal</span>
            </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
            <div class="glass-card">
                <p class="metric-label">⚡ Intensity</p>
                <p class="metric-value">High</p>
                <span class="status-badge status-good">Active</span>
            </div>
        """, unsafe_allow_html=True)

    # --- Heart Rate Graph ---
    st.markdown("#### Heart Rate Trend (Last 24h)")
    fig_bpm = go.Figure()
    fig_bpm.add_trace(go.Scatter(y=bpm_history, mode='lines', line=dict(color='#f87171', width=3), fill='tozeroy', fillcolor='rgba(248, 113, 113, 0.1)'))
    fig_bpm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), 
                          xaxis=dict(visible=False), yaxis=dict(showgrid=False, color="gray"))
    st.plotly_chart(fig_bpm, use_container_width=True)

    # --- Step Ring (Visual Core) ---
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <div style="border: 15px solid rgba(255,255,255,0.05); border-top: 15px solid #4ade80; border-radius: 50%; width: 220px; height: 220px; margin: auto; display: flex; flex-direction: column; justify-content: center;">
                <h1 style="margin:0; font-size:3rem;">10,372</h1>
                <p style="margin:0; opacity:0.6;">Steps Today</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif menu == "Gait & AI Insights":
    st.markdown("### 🤖 Stride AI Intelligence")
    st.info("The LSTM model is analyzing your movement patterns in real-time.")

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
            <div class="glass-card">
                <p class="metric-label">Stride Symmetry</p>
                <p class="metric-value">98.2%</p>
                <p style="font-size:0.7rem; opacity:0.5;">Near perfect balance detected.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        st.markdown("""
            <div class="glass-card">
                <p class="metric-label">Impact Force</p>
                <p class="metric-value">Low</p>
                <p style="font-size:0.7rem; opacity:0.5;">Optimal for joint health.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Radar Chart for Gait Analysis ---
    categories = ['Balance', 'Power', 'Consistency', 'Posture', 'Flexibility']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[98, 85, 90, 70, 80], theta=categories, fill='toself', line_color='#8b5cf6'))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=350
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("""
        <div class="glass-card" style="border-left: 5px solid #8b5cf6;">
            <p style="margin:0; font-weight:600;">AI Insight</p>
            <p style="margin:0; font-size:0.9rem; opacity:0.8;">Your left stride is slightly shorter during inclines. Focus on core engagement to maintain symmetry.</p>
        </div>
    """, unsafe_allow_html=True)
