import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime
import io

# --- 1. RESEARCH SUITE CONFIG ---
st.set_page_config(page_title="STRIDE-AI | Neural Clinical Lab", layout="wide")

# --- 2. ADVANCED UI THEME (High-Contrast Lab Aesthetic) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    .stApp { background: #050505; font-family: 'Inter', sans-serif; color: #f0f0f0; }
    
    .report-container { background: #0d0d11; border: 1px solid #1f1f27; border-radius: 12px; padding: 30px; margin-bottom: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .report-header { border-bottom: 3px solid #3b82f6; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; }
    
    .ref-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    .ref-table th { color: #3b82f6; text-align: left; padding: 12px; border-bottom: 2px solid #1f1f27; font-family: 'JetBrains Mono'; }
    .ref-table td { padding: 12px; border-bottom: 1px solid #141418; }
    
    .status-badge { padding: 5px 12px; border-radius: 4px; font-weight: 800; font-size: 0.7rem; text-transform: uppercase; }
    .stDownloadButton > button { width: 100%; background: linear-gradient(90deg, #3b82f6, #2563eb) !important; color: white !important; border: none !important; padding: 15px !important; font-weight: 700 !important; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# --- 3. THE "HEAVY" DATA ENGINE (New Data Features) ---
# We are adding Z-Scores, Sample Variance, and Confidence Intervals
lab_data = {
    "Parameter ID": ["GAIT_SYM_01", "IMP_FRC_02", "HR_TELE_03", "MET_EFF_04", "STR_LEN_05", "CAD_FREQ_06"],
    "Bio-Metric Parameter": ["Gait Symmetry Index", "Peak Impact Force", "Mean Heart Rate", "Metabolic Efficiency (η)", "Mean Stride Length", "Step Cadence"],
    "Result": [0.82, 2.4, 158, 0.72, 0.78, 172],
    "Z-Score": [-1.4, +2.1, +2.8, -1.1, -0.2, +0.5], # Deviation from mean
    "Reference Range": ["0.90 - 1.00", "1.5 - 2.1 G", "60 - 140 BPM", "0.80 - 0.95", "0.70 - 0.85 m", "160 - 180 spm"],
    "Confidence (CI)": ["98.2%", "94.5%", "99.1%", "89.4%", "97.0%", "95.5%"],
    "Status": ["ABNORMAL", "HIGH", "CRITICAL", "LOW", "NORMAL", "NORMAL"]
}
df_heavy = pd.DataFrame(lab_data)

# Function to generate the 'Heavy' Report
def convert_df_to_heavy_csv(df):
    output = io.StringIO()
    output.write("STRIDE-AI CLINICAL BIOMECHANICS REPORT\n")
    output.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("Sensor Frequency: 100Hz | Algorithm: LSTM-CNN Hybrid v3.0\n")
    output.write("-" * 50 + "\n")
    df.to_csv(output, index=False)
    return output.getvalue().encode('utf-8')

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🦾 SYSTEM CALIBRATION")
    st.caption("Environment: Bareilly Research Wing")
    page = st.radio("Switch View", ["Intelligence Hub", "Clinical Lab Report"])
    st.markdown("---")
    
    # Actionable Download
    heavy_report = convert_df_to_heavy_csv(df_heavy)
    st.download_button(
        label="📄 DOWNLOAD FULL KINETIC DOSSIER",
        data=heavy_report,
        file_name=f"STRIDE_AI_DOSSIER_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
    )
    st.caption("Report includes Z-Scores and Neural Confidence Intervals.")

# --- 5. PAGE ROUTING ---

if page == "Intelligence Hub":
    st.title("Neural Decision Matrix")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader("Gait Signal Decomposition")
        x = np.linspace(0, 10, 100)
        # Showing the "Signal Noise" vs "Filtered Stride"
        noise = np.random.normal(0, 0.2, 100)
        signal = np.sin(x) + 2
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=signal + noise, name="Raw Sensor Data", line=dict(color="rgba(255,255,255,0.2)")))
        fig.add_trace(go.Scatter(x=x, y=signal, name="Neural Filtered Stride", line=dict(color="#3b82f6", width=4)))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### Model Architecture")
        st.code("""
Layer (type)         Output Shape
================================
Conv1D (CNN)        (None, 64, 32)
LSTM (Recurrent)    (None, 32)
Dense (Softmax)     (None, 6)
================================
Precision: 0.984 | Recall: 0.97
        """)
        st.info("The model is currently identifying a 'Pronation Cluster' with 94% probability.")

elif page == "Clinical Lab Report":
    st.title("Biomechanical Clinical Dossier")
    
    st.markdown(f"""
    <div class="report-container">
        <div class="report-header">
            <div>
                <h1 style="margin:0; color:#3b82f6; letter-spacing:-1px;">STRIDE-AI LABS</h1>
                <p style="font-family:'JetBrains Mono'; font-size:0.8rem; opacity:0.6;">BIOMECHANICAL INFRASTRUCTURE v3.0</p>
            </div>
            <div style="text-align:right;">
                <p style="margin:0; font-weight:800;">REF NO: SA-2026-942</p>
                <p style="margin:0; color:#3b82f6;">{datetime.now().strftime('%d %B %Y')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Heavy Report Table
    st.markdown("""
    <table class="ref-table">
        <tr>
            <th>ID</th>
            <th>TEST PARAMETER</th>
            <th>RESULT</th>
            <th>Z-SCORE</th>
            <th>REF. RANGE</th>
            <th>STATUS</th>
        </tr>
    """, unsafe_allow_html=True)
    
    for _, row in df_heavy.iterrows():
        color = "#ff4b4b" if row['Status'] in ["ABNORMAL", "HIGH", "CRITICAL"] else "#00ffbd"
        st.markdown(f"""
        <tr>
            <td style="font-family:'JetBrains Mono'; font-size:0.7rem; opacity:0.5;">{row['Parameter ID']}</td>
            <td style="font-weight:600;">{row['Bio-Metric Parameter']}</td>
            <td style="color:{color}; font-weight:800;">{row['Result']}</td>
            <td style="font-family:'JetBrains Mono';">{row['Z-Score']}</td>
            <td>{row['Reference Range']}</td>
            <td><span class="status-badge" style="background:{color}22; color:{color}; border:1px solid {color}44;">{row['Status']}</span></td>
        </tr>
        """, unsafe_allow_html=True)
        
    st.markdown("</table></div>", unsafe_allow_html=True)
    
    # Detailed AI Interpretation Section
    st.subheader("Neural Diagnostic Interpretations")
    
    with st.expander("🔍 View Deep Feature Analysis"):
        st.write("""
        - **KINETIC ASYMMETRY:** Detected -1.4 Z-Score in Symmetry Index. This suggests a significant neurological or muscular imbalance during the propulsion phase.
        - **HEMODYNAMIC STRAIN:** Heart rate is 2.8 Standard Deviations above resting mean. 
        - **METABOLIC DRIFT:** Low efficiency (0.72) indicates early onset of anaerobic fatigue.
        """)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.error("#### Prescriptive Interventions")
        st.markdown("""
        - **Correction:** Implement unilateral strength training for the Left Gastrocnemius.
        - **Load:** Decrease weekly kinetic volume by 15% until Symmetry > 0.90.
        """)
    with c2:
        st.warning("#### Critical Alerts")
        st.markdown("""
        - **Zone 5 Alert:** Heart rate is in the 98th percentile for this age group.
        - **Impact Alert:** Peak G-force exceeds structural safety of current footwear.
        """)
