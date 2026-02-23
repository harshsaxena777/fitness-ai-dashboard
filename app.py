import streamlit as st
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="FitnessPro AI", layout="centered")

# --- SHARED DATA ---
days = ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"]
activity_data = [2.9, 8.9, 2.5, 407, 1.2, 10.4, 14]

# --- ALL-IN-ONE PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(165deg, #5c5be5 0%, #3a3897 40%, #1e1b4b 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: white;
    }

    /* Glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 28px;
        padding: 24px;
        margin-bottom: 20px;
    }

    /* Dashboard Ring */
    .progress-ring {
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 70%);
        border: 12px solid rgba(255, 255, 255, 0.05);
        border-top: 12px solid #ffffff;
        border-radius: 50%;
        width: 240px; height: 240px;
        margin: 20px auto;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        box-shadow: 0 0 40px rgba(255, 255, 255, 0.1);
    }

    /* Awards & Streaks styling */
    .award-badge {
        background: rgba(139, 92, 246, 0.3);
        border: 2px solid #a78bfa;
        border-radius: 15px;
        width: 80px; height: 90px;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        margin: 10px auto;
    }
    .streak-medal {
        background: rgba(251, 191, 36, 0.15);
        border: 2px solid #fbbf24;
        border-radius: 50%;
        width: 70px; height: 70px;
        display: flex; justify-content: center; align-items: center;
        margin: 10px auto;
        font-size: 1.5rem;
    }
    .locked { opacity: 0.35; filter: grayscale(1); }

    /* Interactive Elements */
    .stat-circle {
        width: 32px; height: 32px; border-radius: 50%;
        border: 2px solid rgba(255,255,255,0.2); display: inline-flex;
        justify-content: center; align-items: center; margin: 5px;
    }
    .stat-active { background: #fbbf24; border-color: #fbbf24; color: #1e1b4b; box-shadow: 0 0 15px #fbbf24; }
    
    .btn-boost {
        background: #ffffff; color: #5c5be5 !important;
        font-weight: 800; padding: 14px 35px; border-radius: 50px;
        text-align: center; display: block; width: fit-content; margin: 25px auto;
        text-decoration: none; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Dashboard", "Highlights", "Awards", "Step Analytics"])

if menu == "Dashboard":
    st.markdown("<div style='display:flex; justify-content:space-between; align-items:center;'><span>👤</span> <span style='background:rgba(255,255,255,0.15); padding:6px 18px; border-radius:20px; font-weight:bold;'>🔥 1</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="progress-ring">
            <p style="margin:0; opacity:0.7; font-size:0.9rem;">👟 Wed, 10th</p>
            <h1 style="margin:0; font-size:3.8rem; font-weight:800;">10,372</h1>
            <p style="margin:0; color:#fbbf24; font-weight:bold;">Goal achieved</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<a class='btn-boost'>⚡ Activate 2X Boost</a>", unsafe_allow_html=True)

    cols = st.columns(7)
    for i, col in enumerate(cols):
        is_active = "stat-active" if days[i] in ["Sat", "Wed"] else ""
        col.markdown(f"<div style='text-align:center;'><span style='font-size:0.65rem; opacity:0.6;'>{days[i]}</span><br><div class='stat-circle {is_active}'>{'✓' if is_active else ''}</div></div>", unsafe_allow_html=True)

    fig = go.Figure(go.Scatter(x=days, y=activity_data, mode='lines+markers', line=dict(color='white', width=4), fill='tozeroy', fillcolor='rgba(255,255,255,0.1)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(visible=False), height=180, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

elif menu == "Highlights":
    st.markdown("### Highlights")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<p style='font-weight:bold;'>Streak Calendar</p>", unsafe_allow_html=True)
    cols = st.columns(7)
    for i, col in enumerate(cols):
        is_active = "stat-active" if days[i] in ["Sat", "Wed"] else ""
        col.markdown(f"<div style='text-align:center; font-size:0.7rem;'>{days[i]}<br><div class='stat-circle {is_active}'>{'✓' if is_active else ''}</div></div>", unsafe_allow_html=True)
    
    fig = go.Figure(go.Scatter(x=days, y=[2.9, 8.9, 2.5, 0.4, 1.2, 10.4, 1.4], mode='lines+markers', line=dict(color='white', width=2), fill='tozeroy'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(visible=False), height=100, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<p style='font-weight:bold;'>Achievements ></p>", unsafe_allow_html=True)
    cols = st.columns(3)
    ach = ["100k", "150k", "200k"]
    for i, col in enumerate(cols):
        locked = "locked" if i > 0 else ""
        col.markdown(f'<div class="award-badge {locked}"><b>{ach[i][:-1]}</b><br><small>k</small></div><p style="text-align:center; font-size:0.7rem;">{ach[i]} steps</p>', unsafe_allow_html=True)

elif menu == "Awards":
    st.markdown("### Awards")
    # Exact reproduction of your 2nd and 3rd image sections
    award_type = st.radio("Type", ["Steps", "Streaks"], horizontal=True, label_visibility="collapsed")
    
    if award_type == "Steps":
        st.markdown("#### Steps")
        vals = ["10k", "50k", "75k", "100k", "150k", "200k", "250k", "300k", "350k", "400k", "450k", "500k"]
        unlocked = ["10k", "50k", "75k", "100k"]
        for row in range(0, 12, 3):
            cols = st.columns(3)
            for i in range(3):
                v = vals[row+i]
                status = "" if v in unlocked else "locked"
                cols[i].markdown(f'<div class="award-badge {status}"><b>{v[:-1]}</b><br><small>k</small></div><p style="text-align:center; font-size:0.7rem;">{v} steps</p>', unsafe_allow_html=True)
    else:
        st.markdown("#### Streaks")
        streaks = ["3-Day", "7-Day", "14-Day", "21-Day", "30-Day", "60-Day", "100-Day", "150-Day", "300-Day"]
        for row in range(0, 9, 3):
            cols = st.columns(3)
            for i in range(3):
                cols[i].markdown(f'<div class="streak-medal locked">🔥</div><p style="text-align:center; font-size:0.7rem;">{streaks[row+i]} Streak</p>', unsafe_allow_html=True)

elif menu == "Step Analytics":
    st.markdown("### Steps")
    # High-interactivity brush up
    st.markdown("""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between;">
                <div><p style="opacity:0.6; font-size:0.8rem; margin:0;">Last Month</p><h2 style="margin:0;">28.75k</h2></div>
                <div style="text-align:right;"><p style="color:#4ade80; font-size:0.8rem; margin:0;">This Month</p><h2 style="color:#4ade80; margin:0;">38.67k</h2></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    fig = go.Figure(go.Scatter(x=[1, 8, 15, 22, 29], y=[5, 12, 28, 32, 38], mode='lines+markers', line=dict(color='#4ade80', width=5, shape='spline'), fill='tozeroy', fillcolor='rgba(74, 222, 128, 0.1)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, color="white"), yaxis=dict(visible=False), height=250, margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center;">
            <div><p style="opacity:0.7; margin:0;">Total steps</p><h3 style="margin:0; color:#4ade80;">26,410 steps</h3></div>
            <div style="background:rgba(74, 222, 128, 0.2); padding:10px; border-radius:15px; color:#4ade80;">▲ 81%</div>
        </div>
    """, unsafe_allow_html=True)
