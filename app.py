import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time

# --- MOBILE OPTIMIZED CONFIG ---
st.set_page_config(
    page_title="STRIDE-AI Mobile", 
    layout="centered", # Mobile ke liye centered best hai
    initial_sidebar_state="collapsed" # Mobile par sidebar hide rakho
)

# --- SESSION STATE ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- STYLING FOR MOBILE ---
st.markdown("""
<style>
    /* Mobile Touch optimization */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3em;
        background-color: #3b82f6;
    }
    /* Metric styling for small screens */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📱 STRIDE-AI Mobile")

# --- DATA INJECTION (Big Button for Finger Touch) ---
if st.button("📡 SYNC SENSOR DATA"):
    with st.spinner("Syncing..."):
        time.sleep(1)
        st.session_state.steps += np.random.randint(200, 500)
        st.session_state.heart_rate = np.random.randint(110, 155)
        st.session_state.report_ready = False
        st.rerun()

# --- TABS (Mobile Swipe Friendly) ---
tab1, tab2, tab3 = st.tabs(["📊 Stats", "🫀 Heart", "🧠 AI Report"])

with tab1:
    # Mobile par 2 columns theek rehte hain
    c1, c2 = st.columns(2)
    c1.metric("Steps", st.session_state.steps)
    c2.metric("Stability", "94%")
    
    # Simple Chart for Mobile
    st.write("Stride Pattern")
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['x'])
    st.line_chart(chart_data)

with tab2:
    st.metric("Pulse", f"{st.session_state.heart_rate} BPM")
    # Gauge chart mobile par chota rakhenge
    fig_hr = go.Figure(go.Indicator(
        mode = "gauge+number", value = st.session_state.heart_rate,
        gauge = {'axis': {'range': [40, 200]}, 'bar': {'color': "#ef4444"}}
    ))
    fig_hr.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_hr, use_container_width=True)

with tab3:
    if st.button("🔍 GENERATE MOBILE REPORT"):
        st.session_state.report_ready = True
    
    if st.session_state.report_ready:
        st.success("Report Generated Successfully")
        st.markdown(f"""
        <div style="background: #111; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6;">
            <h4>Diagnostic Summary</h4>
            <p><b>Status:</b> Healthy</p>
            <p><b>VO2 Max:</b> {round(15 * (198/st.session_state.heart_rate), 1)}</p>
            <hr>
            <small>AI Advice: Your gait is stable. Keep moving!</small>
        </div>
        """, unsafe_allow_html=True)
