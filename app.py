import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# --- 1. RESEARCH SUITE CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Clinical Lab", layout="wide")

# --- 2. CLINICAL UI THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    .stApp { background: #0a0a0c; font-family: 'Inter', sans-serif; color: #f0f0f0; }
    
    /* Lab Report Styling */
    .report-container {
        background: #16161a;
        border: 1px solid #2d2d35;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .report-header {
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
    }

    /* Reference Range Table styling */
    .ref-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .ref-table th { color: #3b82f6; text-align: left; padding: 10px; border-bottom: 1px solid #2d2d35; }
    .ref-table td { padding: 10px; border-bottom: 1px solid #1c1c22; }
    .status-badge { padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.7rem; }
    
    /* Action Buttons */
    .stDownloadButton > button {
        width: 100%;
        background: #3b82f6 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA PREPARATION (The Lab Logic) ---
# Simulating the data fetched from your AI models
lab_data = {
    "Parameter": ["Gait Symmetry", "Impact Force", "Avg Heart Rate", "Metabolic Efficiency", "Stride Length"],
    "Your Value": [0.82, 2.4, 158, 0.72, 0.78],
    "Normal Range": ["0.90 - 1.00", "1.5 - 2.1 G", "60 - 140 BPM", "0.80 - 0.95", "0.70 - 0.85 m"],
    "Unit": ["Ratio", "G-Force", "BPM", "η", "Meters"],
    "Status": ["Low", "High", "Critical", "Low", "Normal"]
}
df_report = pd.DataFrame(lab_data)

# --- 4. SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.markdown("### 🔬 CLINICAL ENGINE")
    page = st.radio("Navigation", ["Dashboard View", "Lab Report Module"])
    st.markdown("---")
    
    # Actionable Report Download
    report_csv = df_report.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD FULL LAB REPORT",
        data=report_csv,
        file_name=f"StrideAI_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

# --- 5. PAGE ROUTING ---

if page == "Dashboard View":
    st.title("Real-Time Telemetry Dashboard")
    # Quick View Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Symmetry", "82%", "-8%")
    c2.metric("Heart Rate", "158 BPM", "+18 BPM", delta_color="inverse")
    c3.metric("Impact", "2.4G", "+0.3G", delta_color="inverse")
    c4.metric("Burn Rate", "412 kcal", "Active")
    
    # 3D Visualization Placeholder
    st.subheader("Neural Gait Reconstruction")
    z = np.linspace(0, 1, 100)
    fig = go.Figure(data=[go.Scatter3d(x=np.cos(z*6), y=np.sin(z*6), z=z, mode='lines', line=dict(color='#3b82f6', width=8))])
    fig.update_layout(scene=dict(bgcolor="black"), paper_bgcolor='black', margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Lab Report Module":
    st.title("Biomechanical & Physiological Lab Report")
    
    # Report Header
    st.markdown(f"""
    <div class="report-container">
        <div class="report-header">
            <div>
                <h2 style="margin:0; color:#3b82f6;">STRIDE-AI DIAGNOSTICS</h2>
                <p style="font-size:0.8rem; opacity:0.7;">Patient Ref: USER_0942 | Bareilly Analytics Lab</p>
            </div>
            <div style="text-align:right;">
                <p style="margin:0;">Date: {datetime.now().strftime('%d %b %Y')}</p>
                <p style="margin:0; color:#00ffbd;">SYSTEM VALIDATED</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # The "Medical Table"
    st.markdown("""
    <table class="ref-table">
        <tr>
            <th>TEST PARAMETER</th>
            <th>RESULT</th>
            <th>REFERENCE RANGE</th>
            <th>UNIT</th>
            <th>INTERPRETATION</th>
        </tr>
    """, unsafe_allow_html=True)
    
    for i, row in df_report.iterrows():
        color = "#ff4b4b" if row['Status'] in ["Low", "High", "Critical"] else "#00ffbd"
        st.markdown(f"""
        <tr>
            <td>{row['Parameter']}</td>
            <td style="font-weight:bold; color:{color};">{row['Your Value']}</td>
            <td>{row['Normal Range']}</td>
            <td>{row['Unit']}</td>
            <td><span class="status-badge" style="background:{color}33; color:{color}; border:1px solid {color};">{row['Status']}</span></td>
        </tr>
        """, unsafe_allow_html=True)
        
    st.markdown("</table></div>", unsafe_allow_html=True)
    
    # AI Clinical Precautions Section
    st.subheader("📋 AI Clinical Prescriptions")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.error("#### Biomechanical Precautions")
        st.write("""
        1. **Asymmetry Correction:** Left-side propulsion deficit observed. Reduce running speed to 8km/h to regain form.
        2. **Impact Management:** High vertical oscillation (2.4G) detected. Increase cadence by 5% to land softer.
        3. **Footwear:** Inspect lateral side of right shoe for foam collapse.
        """)
        
    with col_b:
        st.warning("#### Physiological Precautions")
        st.write("""
        1. **Cardiac Strain:** You are operating at 88% of Max HR. Heart rate recovery (HRR) monitoring suggested.
        2. **Hydration:** High burn rate (412kcal) in short duration. Isotonic intake (500ml) recommended.
        3. **Rest:** Allow 48 hours recovery before next high-impact session.
        """)

    # Interactive Action Buttons
    st.markdown("---")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        st.button("Print Clinical PDF")
    with btn_col2:
        st.button("Share with Physiotherapist")
    with btn_col3:
        st.success("Report Sync Complete")
