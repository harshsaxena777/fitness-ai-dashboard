import streamlit as st
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="FitnessPro AI", layout="centered")

# --- SHARED DATA (Defined globally to avoid NameErrors) ---
days = ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"]
activity_data = [2.9, 8.9, 2.5, 0.4, 1.2, 10.4, 1.4]

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .main {
        background: linear-gradient(180deg, #6366f1 0%, #312e81 100%);
        font-family: 'Inter', sans-serif;
        color: white;
    }
    
    .circle-container {
        border: 8px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        width: 280px;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: auto;
        box-shadow: 0 0 50px rgba(255, 255, 255, 0.1);
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
    }

    .boost-btn {
        background: white;
        color: #4f46e5;
        border-radius: 30px;
        padding: 12px 24px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        display: block;
        text-decoration: none;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
    }

    .stat-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid white;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin: 5px;
    }
    
    .stat-active { background-color: #fbbf24; border-color: #fbbf24; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Home Dashboard", "User Profile"])

if menu == "Home Dashboard":
    # --- SCREEN 1: DASHBOARD ---
    st.markdown("<p style='text-align:right;'>🔥 1</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="circle-container">
            <p style="margin:0; font-size:1rem;">👟 Wed, 10th</p>
            <h1 style="margin:0; font-size:4rem; font-weight:bold;">10,372</h1>
            <p style="margin:0; color:#cbd5e1;">Goal achieved</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<a class='boost-btn'>⚡ Activate 2X Boost</a>", unsafe_allow_html=True)

    # Streak Calendar Row
    cols = st.columns(7)
    for i, col in enumerate(cols):
        # Using the global 'days' list
        active = "stat-active" if days[i] in ["Sat", "Wed"] else ""
        col.markdown(f"<div style='text-align:center; font-size:0.8rem;'>{days[i]}<br><div class='stat-circle {active}'>{'✓' if active else ''}</div></div>", unsafe_allow_html=True)

    st.markdown("### Activity Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=activity_data, 
                             mode='lines+markers', line=dict(color='white', width=3),
                             fill='tozeroy', fillcolor='rgba(255,255,255,0.1)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      xaxis=dict(showgrid=False, color="white"), yaxis=dict(showgrid=False, showticklabels=False),
                      margin=dict(l=0, r=0, t=0, b=0), height=200)
    st.plotly_chart(fig, use_container_width=True)

else:
    # --- SCREEN 2: PROFILE ---
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.image("https://ui-avatars.com/api/?name=Harsh+Saxena&background=000&color=fff&size=128", width=120)
    st.markdown(f"""
        <h2 style='margin-bottom:0;'>Harsh Saxena</h2>
        <p style='color:#cbd5e1;'>@harshsaxena26647167798 📋</p>
        <p style='font-style:italic;'>Welcome to Final Year Project</p>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.metric("Following", "0")
    c2.metric("Followers", "0")
    st.markdown("</div>", unsafe_allow_html=True)