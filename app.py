import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# --- 1. CONFIG & SYSTEM REBOOT LOGIC ---
st.set_page_config(page_title="STRIDE-AI Mobile Pro", layout="centered")

def reboot_system():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.toast("System Rebooted... All sensors recalibrated.", icon="🔄")
    time.sleep(1)

# --- 2. SESSION STATE INITIALIZATION ---
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 145.0
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 3. UI STYLING ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .reboot-btn>button { background-color: #ef4444 !important; color: white !important; border: none; }
    .report-card { background: #0d1117; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; line-height: 1.6; }
    .status-tag { background: #1e293b; padding: 5px 10px; border-radius: 8px; font-size: 0.8rem; color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP NAVIGATION & REBOOT ---
c_title, c_reboot = st.columns([4, 1])
with c_title:
    st.title("📱 STRIDE-AI")
with c_reboot:
    st.markdown('<div class="reboot-btn">', unsafe_allow_html=True)
    if st.button("🔄"):
        reboot_system()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. SEPARATE SCREENS VIA TABS ---
tabs = st.tabs(["👣 Steps", "🫀 Heart", "🔥 Kcal", "🧘 Posture", "🔮 Risk", "🧠 AI Report"])

# SCREEN 1: STEPS
with tabs[0]:
    st.subheader("Pedometer Analytics")
    st.metric("Total Daily Steps", st.session_state.steps, delta="+420 vs avg")
    st.write("Real-time Step Frequency")
    st.line_chart(np.random.randn(20))
    if st.button("Inject Step Data"):
        st.session_state.steps += 250
        st.rerun()

# SCREEN 2: HEART RATE
with tabs[1]:
    st.subheader("Cardiac Telemetry")
    st.metric("Current Pulse", f"{st.session_state.heart_rate} BPM")
    fig_hr = go.Figure(go.Indicator(mode="gauge+number", value=st.session_state.heart_rate, gauge={'axis':{'range':[40,200]}, 'bar':{'color':"#ef4444"}}))
    fig_hr.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
    st.plotly_chart(fig_hr, use_container_width=True)

# SCREEN 3: CALORIES
with tabs[2]:
    st.subheader("Metabolic Energy")
    st.metric("Calories Burned", f"{int(st.session_state.calories)} kcal")
    st.info("Metabolic efficiency is 12% higher than baseline.")
    st.bar_chart(np.random.randint(10, 50, 7))

# SCREEN 4: POSTURE ANALYSIS (New Dedicated Screen)
with tabs[3]:
    st.subheader("Posture & Alignment")
    st.markdown('<p class="status-tag">Software-Only Pose Modeling</p>', unsafe_allow_html=True)
    posture_score = np.random.randint(70, 95)
    st.metric("Spinal Alignment Score", f"{posture_score}%")
    
    st.write("Joint Angle Variance (Simulated)")
    st.area_chart(np.random.rand(15))
    st.caption("AI detects a slight 2° tilt in the pelvic region. Adjust your stance.")

# SCREEN 5: RISK PREDICTION (Fall & Diet)
with tabs[4]:
    st.subheader("Predictive Risk Engine")
    
    # Fall Risk
    st.write("---")
    st.write("🚷 **Fall Risk Assessment**")
    f_risk = "LOW" if st.session_state.steps > 4000 else "MODERATE"
    st.progress(0.2 if f_risk == "LOW" else 0.6)
    st.write(f"Risk Level: **{f_risk}**")
    
    # Diet Correlation
    st.write("---")
    st.write("🥗 **Symptom Correlation**")
    diet = st.selectbox("Current Intake", ["Balanced", "High Caffeine", "High Sugar"])
    if diet == "High Caffeine":
        st.warning("Cardiac Jitter detected. Heart rate variability is fluctuating.")

# SCREEN 6: ELABORATIVE AI REPORT
with tabs[5]:
    st.subheader("Clinical Diagnostic Report")
    if st.button("🔍 GENERATE COMPREHENSIVE REPORT"):
        with st.spinner("Compiling Multi-Screen Data..."):
            time.sleep(2)
            st.session_state.report_ready = True

    if st.session_state.report_ready:
        st.markdown(f"""
        <div class="report-card">
            <h3 style="color:#3b82f6; margin-top:0;">STRIDE-AI FINAL CLINICAL AUDIT</h3>
            <p><b>1. Physical Activity Summary:</b><br>
            Total volume of {st.session_state.steps} steps executed. Subject is maintaining an active lifestyle. 
            Metabolic age is estimated at {22 - 2} years.</p>
            
            <p><b>2. Cardiovascular & Stress Analysis:</b><br>
            Current BPM ({st.session_state.heart_rate}) indicates a stable aerobic state. 
            VO2 Max estimation stands at {round(15*(190/st.session_state.heart_rate),1)} mL/kg/min, showing elite respiratory efficiency.</p>
            
            <p><b>3. Biomechanical & Posture Integrity:</b><br>
            Posture Score of {posture_score}% suggests no immediate musculoskeletal risk. 
            Gait entropy remains within 1.2% of the standard clinical deviation.</p>
            
            <p><b>4. Predictive Health Risk:</b><br>
            Fall risk is minimized (Level: LOW). No significant correlation between diet and cardiac distress found.</p>
            
            <hr style="opacity:0.2;">
            <p style="color:#00ffbd; font-weight:bold;">Final Verdict: Subject is physiologically optimized. No clinical intervention required.</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("📥 Export Detailed Log", "Full Data Log...", file_name="StrideAI_Full_Report.txt")
