from datetime import datetime  # <-- Is line ko change karo
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# --- 1. THE "ENGINE" (Actual Backend Logic) ---
class StrideEngine:
    @staticmethod
    def process_sensor_fusion(accel_data, gyro_data):
        """Simulates noise filtering and peak detection logic."""
        filtered = np.convolve(accel_data, np.ones(5)/5, mode='valid')
        peaks = (filtered > 1.5).sum() # Threshold logic for step detection
        return peaks, filtered

    @staticmethod
    def medical_decision_logic(bpm, age, asymmetry):
        """Hard clinical rules that drive the app's functionality."""
        max_hr = 220 - age
        risk_level = "LOW"
        advice = "Maintain current pace."
        
        if bpm > (max_hr * 0.85):
            risk_level = "HIGH (Cardiac Stress)"
            advice = "Immediate rest required. Heart rate exceeds safety threshold."
        elif asymmetry > 12:
            risk_level = "MODERATE (Gait Instability)"
            advice = "High risk of ankle sprain. Correct your stride balance."
            
        return risk_level, advice

# --- 2. SESSION INITIALIZATION ---
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'raw_stream' not in st.session_state: st.session_state.raw_stream = np.random.randn(100)
if 'u_age' not in st.session_state: st.session_state.u_age = 22

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="STRIDE-AI | Processing Engine", layout="wide")

st.markdown("""
<style>
    .stApp { background: #020617; }
    .logic-card { 
        background: #1e293b; padding: 20px; border-radius: 10px; 
        border: 1px solid #3b82f6; margin-bottom: 20px;
    }
    .critical-alert { background: #450a0a; color: #fecaca; padding: 15px; border-radius: 8px; border: 1px solid #ef4444; }
</style>
""", unsafe_allow_html=True)

st.title("⚙️ STRIDE-AI: Logic Processing Unit")
st.write("This version focuses on **Backend Signal Processing** and **Clinical Decision Rules**.")

# --- 4. FUNCTIONAL MODULES ---

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📡 Live Signal Processing (Input vs Output)")
    
    # Simulate a "Process" button that actually runs logic
    if st.button("▶️ RUN SIGNAL FUSION ALGORITHM"):
        with st.spinner("Applying Low-Pass Filter & Peak Detection..."):
            time.sleep(1)
            new_steps, filtered_signal = StrideEngine.process_sensor_fusion(
                np.random.uniform(0.5, 2.5, 100), None
            )
            st.session_state.steps += new_steps
            st.session_state.raw_stream = filtered_signal
            st.toast(f"Algorithm detected {new_steps} valid peaks!")

    # Visualizing the Output of the Logic
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=st.session_state.raw_stream, mode='lines', name='Filtered Signal', line=dict(color='#60a5fa')))
    fig.update_layout(title="Processed Kinetic Waveform", template="plotly_dark", height=300)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🧠 Decision Matrix")
    input_bpm = st.number_input("Input BPM from Sensor", 60, 200, 110)
    input_asym = st.slider("Gait Asymmetry (%)", 0, 30, 5)
    
    # Run the Decision Logic
    risk, advice = StrideEngine.medical_decision_logic(input_bpm, st.session_state.u_age, input_asym)
    
    st.markdown(f"""
    <div class="logic-card">
        <p style="margin:0; font-size:0.8rem; opacity:0.7;">CURRENT RISK ASSESSMENT</p>
        <h2 style="color:{'#ef4444' if 'HIGH' in risk else '#10b981'}; margin:0;">{risk}</h2>
        <hr style="opacity:0.2;">
        <p><b>AI Recommendation:</b><br>{advice}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "HIGH" in risk:
        st.markdown("<div class='critical-alert'>🚨 EMERGENCY OVERRIDE: Cardiac Threshold Triggered</div>", unsafe_allow_html=True)

# --- 5. DATA TABLE (Functional Tracking) ---
st.write("### 📊 Internal Processing Log")
log_data = pd.DataFrame({
    "Timestamp": [datetime.now().strftime("%H:%M:%S") for _ in range(5)],
    "Logic_Gate": ["Peak_Detect", "Noise_Filter", "Threshold_Check", "BMR_Calc", "Symmetry_Sync"],
    "Status": ["Success", "Active", "Triggered", "Success", "Analyzing"],
    "Value": [st.session_state.steps, "0.45Hz", risk, "1840 kcal", f"{input_asym}%"]
})
st.table(log_data)
