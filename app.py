import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="AI Stride Hub", layout="centered")

# --- Consolidated Styling ---
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
    }
    
    .metric-value { font-size: 1.8rem; font-weight: 800; margin: 0; }
    .metric-label { font-size: 0.8rem; opacity: 0.6; margin: 0; text-transform: uppercase; }
    
    .award-badge {
        background: rgba(139, 92, 246, 0.2);
        border: 2px solid #a78bfa;
        border-radius: 15px;
        width: 70px; height: 80px;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        margin: 10px auto;
    }
    .locked { opacity: 0.3; filter: grayscale(1); }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(74, 222, 128, 0.2); color: #4ade80;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data ---
days = ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"]
activity_data = [8.2, 10.3, 4.5, 7.2, 9.1, 11.0, 10.3] # In k-steps
current_steps = 10372

# --- Sidebar Navigation ---
menu = st.sidebar.radio("Navigation", ["Dashboard", "Step Analytics", "Gait & AI Insights", "Awards"])

if menu == "Dashboard":
    st.markdown("### Daily Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="glass-card">
                <p class="metric-label">💓 Heart Rate</p>
                <p class="metric-value">72 <span style="font-size:1rem; color:#f87171;">bpm</span></p>
                <span class="status-badge">Resting</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        # Calorie math: ~0.04 calories per step
        kcal = int(current_steps * 0.04)
        st.markdown(f"""
            <div class="glass-card">
                <p class="metric-label">🔥 Burned</p>
                <p class="metric-value">{kcal} <span style="font-size:1rem; color:#fbbf24;">kcal</span></p>
                <span class="status-badge">Active</span>
            </div>
        """, unsafe_allow_html=True)

    # Main Step Ring
    st.markdown(f"""
        <div style="border: 12px solid rgba(255,255,255,0.05); border-top: 12px solid #4ade80; border-radius: 50%; width: 200px; height: 200px; margin: 30px auto; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h1 style="margin:0;">{current_steps:,}</h1>
            <p style="margin:0; opacity:0.6;">Steps Today</p>
        </div>
    """, unsafe_allow_html=True)

elif menu == "Step Analytics":
    st.markdown("### Step Analytics")
    
    # Monthly comparison card
    st.markdown("""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between;">
                <div><p style="opacity:0.6; margin:0;">Target</p><h2 style="margin:0;">10.0k</h2></div>
                <div style="text-align:right;"><p style="color:#4ade80; margin:0;">Average</p><h2 style="color:#4ade80; margin:0;">8.6k</h2></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    fig = go.Figure(go.Scatter(x=days, y=activity_data, mode='lines+markers', 
                               line=dict(color='#4ade80', width=4, shape='spline'), 
                               fill='tozeroy', fillcolor='rgba(74, 222, 128, 0.1)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      xaxis=dict(showgrid=False, color="white"), yaxis=dict(visible=False), height=250)
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Gait & AI Insights":
    st.markdown("### 🤖 Stride Intelligence")
    st.markdown("""
        <div class="glass-card" style="border-left: 5px solid #8b5cf6;">
            <p style="margin:0; font-weight:600; color:#a78bfa;">AI ANALYSIS</p>
            <p style="margin:0; font-size:0.9rem; opacity:0.8;">Your symmetry is at 94%. Slight left-leaning detected during the last 2km.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Radar Chart for Gait
    categories = ['Symmetry', 'Balance', 'Impact', 'Tempo', 'Posture']
    fig_radar = go.Figure(go.Scatterpolar(r=[94, 88, 70, 91, 85], theta=categories, fill='toself', line_color='#8b5cf6'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"), 
                            paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=300)
    st.plotly_chart(fig_radar, use_container_width=True)

elif menu == "Awards":
    st.markdown("### Achievements")
    award_type = st.tabs(["Steps", "Streaks"])
    
    with award_type[0]:
        vals = ["10k", "50k", "100k", "250k", "500k", "1M"]
        unlocked = ["10k", "50k"]
        for row in range(0, 6, 3):
            cols = st.columns(3)
            for i in range(3):
                v = vals[row+i]
                status = "" if v in unlocked else "locked"
                cols[i].markdown(f'<div class="award-badge {status}"><b>{v[:-1]}</b><br><small>{v[-1]}</small></div><p style="text-align:center; font-size:0.7rem;">{v}</p>', unsafe_allow_html=True)
