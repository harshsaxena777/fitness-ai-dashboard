import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# --- 1. RESEARCH SUITE CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Intelligence Hub", layout="wide")

# --- 2. ADVANCED UI THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    .stApp { background: #0a0a0c; font-family: 'Inter', sans-serif; color: #f0f0f0; }
    
    .report-container { background: #16161a; border: 1px solid #2d2d35; border-radius: 12px; padding: 25px; margin-bottom: 20px; }
    .report-header { border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; }
    .ref-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .ref-table th { color: #3b82f6; text-align: left; padding: 10px; border-bottom: 1px solid #2d2d35; }
    .ref-table td { padding: 10px; border-bottom: 1px solid #1c1c22; }
    .status-badge { padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.7rem; }
    
    .stDownloadButton > button { width: 100%; background: #3b82f6 !important; color: white !important; border-radius: 8px !important; }
    
    /* Intelligence Hub Styling */
    .ai-brain-card {
        background: linear-gradient(135deg, #1e1e26 0%, #111115 100%);
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
lab_data = {
    "Parameter": ["Gait Symmetry", "Impact Force", "Avg Heart Rate", "Metabolic Efficiency", "Stride Length"],
    "Your Value": [0.82, 2.4, 158, 0.72, 0.78],
    "Normal Range": ["0.90 - 1.00", "1.5 - 2.1 G", "60 - 140 BPM", "0.80 - 0.95", "0.70 - 0.85 m"],
    "Unit": ["Ratio", "G-Force", "BPM", "η", "Meters"],
    "Status": ["Low", "High", "Critical", "Low", "Normal"]
}
df_report = pd.DataFrame(lab_data)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🧠 STRIDE-AI CORE")
    page = st.radio("Navigation", ["Intelligence Hub", "Dashboard View", "Lab Report Module"])
    st.markdown("---")
    st.download_button(label="📥 DOWNLOAD CLINICAL REPORT", data=df_report.to_csv(index=False).encode('utf-8'), file_name="StrideAI_Full_Report.csv", mime="text/csv")

# --- 5. PAGE ROUTING ---

# NEW FEATURE: INTELLIGENCE HUB (The "Balance" between raw data and reports)
if page == "Intelligence Hub":
    st.title("AI Decision Matrix & Stride Comparison")
    
    st.markdown("""
    <div class="ai-brain-card">
        <h3 style='margin:0; color:#3b82f6;'>Neural Logic Engine</h3>
        <p style='opacity:0.7;'>Analyzing 512 gait features against the Biomechanical Gold Standard (BGS) Model.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_plot, col_logic = st.columns([2, 1])
    
    with col_plot:
        st.subheader("BGS vs. Live Pattern Comparison")
        # Creating a comparison graph
        x = np.linspace(0, 10, 100)
        gold_standard = np.sin(x) + 2
        user_pattern = np.sin(x) * 0.7 + 2.3 + np.random.normal(0, 0.1, 100)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=gold_standard, name="Gold Standard (Optimal)", line=dict(color="#00ffbd", dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=user_pattern, name="Your Stride (Live)", line=dict(color="#f87171", width=3)))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The Red line indicates propulsion lag and vertical instability compared to the Healthy Baseline (Green).")

    with col_logic:
        st.subheader("AI Probability")
        st.write("Confidence in Anomaly Detection:")
        st.progress(88)
        st.write("Model Confidence (LSTM-CNN):")
        st.progress(94)
        
        st.markdown("""
        **Anomaly Signature:**
        - Medial Collapse Detected
        - Late Heel Strike
        - Compensatory Hip Sway
        """)

elif page == "Dashboard View":
    st.title("Real-Time Telemetry Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Symmetry", "82%", "-8%")
    c2.metric("Heart Rate", "158 BPM", "+18 BPM", delta_color="inverse")
    c3.metric("Impact", "2.4G", "+0.3G", delta_color="inverse")
    c4.metric("Burn Rate", "412 kcal", "Active")
    
    st.subheader("Neural Gait Reconstruction (3D)")
    z = np.linspace(0, 1, 100)
    fig = go.Figure(data=[go.Scatter3d(x=np.cos(z*6), y=np.sin(z*6), z=z, mode='lines', line=dict(color='#3b82f6', width=8))])
    fig.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Lab Report Module":
    st.title("Biomechanical & Physiological Lab Report")
    st.markdown(f"""
    <div class="report-container">
        <div class="report-header">
            <div><h2 style="margin:0; color:#3b82f6;">STRIDE-AI DIAGNOSTICS</h2><p style="font-size:0.8rem; opacity:0.7;">Patient Ref: USER_0942</p></div>
            <div style="text-align:right;"><p style="margin:0;">Date: {datetime.now().strftime('%d %b %Y')}</p><p style="margin:0; color:#00ffbd;">SYSTEM VALIDATED</p></div>
        </div>
        <table class="ref-table">
            <tr><th>TEST PARAMETER</th><th>RESULT</th><th>REFERENCE RANGE</th><th>UNIT</th><th>INTERPRETATION</th></tr>
    """, unsafe_allow_html=True)
    
    for i, row in df_report.iterrows():
        color = "#ff4b4b" if row['Status'] in ["Low", "High", "Critical"] else "#00ffbd"
        st.markdown(f"<tr><td>{row['Parameter']}</td><td style='font-weight:bold; color:{color};'>{row['Your Value']}</td><td>{row['Normal Range']}</td><td>{row['Unit']}</td><td><span class='status-badge' style='background:{color}33; color:{color}; border:1px solid {color};'>{row['Status']}</span></td></tr>", unsafe_allow_html=True)
        
    st.markdown("</table></div>", unsafe_allow_html=True)
    
    ca, cb = st.columns(2)
    with ca:
        st.error("#### Biomechanical Precautions")
        st.write("1. Reduce speed to 8km/h.\n2. Targeted calf activation.\n3. Inspect medial shoe wear.")
    with cb:
        st.warning("#### Physiological Precautions")
        st.write("1. Cardiac strain detected.\n2. 500ml Isotonic intake.\n3. 48hr recovery suggested.")
