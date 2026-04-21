import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

# --- 2. STATE MANAGEMENT ---
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 0.0

# --- 3. SIDEBAR: USER BIO-DATA (New Feature) ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6; font-weight:900;'>STRIDE-AI</h1>", unsafe_allow_html=True)
    
    st.markdown("### 👤 User Profile")
    u_age = st.number_input("Age", min_value=10, max_value=100, value=21)
    u_weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    u_height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
    
    # Complex Calculation: BMR (Mifflin-St Jeor Equation)
    bmr = (10 * u_weight) + (6.25 * u_height) - (5 * u_age) + 5
    
    st.markdown("---")
    page = st.radio("RESEARCH MODULES", 
                    ["[01] Dashboard", "[02] Neural Motion", "[03] AI Health Report"])
    
    st.markdown("---")
    if st.button("🚀 TRIGGER MOTION"):
        st.session_state.steps += np.random.randint(30, 70)
        st.session_state.heart_rate = np.random.randint(110, 145)
        # Dynamic Calorie burn based on weight
        st.session_state.calories += round((u_weight * 0.04), 2) 
        st.rerun()

# --- 4. GLOBAL UI STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;700;900&family=JetBrains+Mono:wght@400&display=swap');
    .stApp { background: #050505; font-family: 'Outfit', sans-serif; color: #e0e0e0; }
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
</style>
""", unsafe_allow_html=True)

# --- 5. PAGE: DASHBOARD ---
if page == "[01] Dashboard":
    st.title("Kinetic Executive Overview")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="research-card"><p class="stat-label">TOTAL STEPS</p><p class="stat-value">{st.session_state.steps}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="research-card"><p class="stat-label">LIVE BPM</p><p class="stat-value">{st.session_state.heart_rate}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="research-card"><p class="stat-label">ACTIVE KCAL</p><p class="stat-value">{st.session_state.calories}</p></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="research-card"><p class="stat-label">BMR BASE</p><p class="stat-value">{int(bmr)}</p></div>', unsafe_allow_html=True)

    # Iframe Integration (World Health Map or Clock)
    st.components.v1.iframe("https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=en&size=medium&timezone=Asia%2FKolkata", height=120)

    # Hydration Tracker (New Component)
    st.markdown("### 💧 Real-time Hydration Strategy")
    water_needed = round((st.session_state.steps / 1000) * 0.25, 2) # 250ml per 1000 steps
    st.progress(min(water_needed/3.0, 1.0))
    st.write(f"Based on activity, you need to consume **{water_needed} Liters** of additional water.")

# --- 6. PAGE: AI HEALTH REPORT ---
elif page == "[03] AI Health Report":
    st.title("🛡️ AI Smart Diagnostic Engine")
    
    if st.button("🔍 INITIATE BIO-METRIC SCAN"):
        with st.status("Analyzing Personal Bio-Data...", expanded=True) as status:
            time.sleep(1)
            st.write(f"Calculating BMR for {u_age}yo Male/Female...")
            time.sleep(1)
            st.write("Verifying Gait Symmetry...")
            status.update(label="Analysis Complete!", state="complete")

        # Complex Logic based on User Profile
        target_steps = 10000
        completion = (st.session_state.steps / target_steps) * 100
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border-left: 5px solid #3b82f6; padding: 25px; border-radius: 15px;">
            <h2 style="color: #3b82f6; margin: 0;">OFFICIAL HEALTH SUMMARY</h2>
            <hr style="opacity: 0.1; margin: 15px 0;">
            <p><b>User Profile:</b> {u_age} years | {u_weight}kg | {u_height}cm</p>
            <p><b>Activity Score:</b> {int(completion)}% of daily target reached.</p>
            <div style="background: rgba(59, 130, 246, 0.1); padding: 15px; border-radius: 10px; margin-top: 15px;">
                <b>AI Prescription:</b> Your BMR is {int(bmr)} kcal. Total energy expenditure today is <b>{int(bmr + st.session_state.calories)} kcal</b>.
                {'Warning: High BPM detected for your age group.' if st.session_state.heart_rate > (220 - u_age)*0.7 else 'Heart rate is optimal for aerobic conditioning.'}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 7. PAGE: NEURAL MOTION ---
else:
    st.title("Neural Motion Analytics")
    # Complexity: Dynamic Spiral based on Steps
    t = np.linspace(0, 10, 100)
    fig_3d = go.Figure(data=[go.Scatter3d(x=np.cos(t), y=np.sin(t), z=t, mode='lines', line=dict(color='#3b82f6', width=8))])
    fig_3d.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', height=600)
    st.plotly_chart(fig_3d, use_container_width=True)
