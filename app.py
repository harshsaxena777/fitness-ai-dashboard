import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
from datetime import datetime
from fpdf import FPDF
import base64

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="STRIDE-AI | Research Suite", layout="wide")

# --- 2. STATE MANAGEMENT & MIDNIGHT RESET ---
current_date = datetime.now().strftime("%Y-%m-%d")
if 'last_reset_date' not in st.session_state:
    st.session_state.last_reset_date = current_date

if st.session_state.last_reset_date != current_date:
    st.session_state.steps = 0
    st.session_state.heart_rate = 72
    st.session_state.calories = 0.0
    st.session_state.last_reset_date = current_date

if 'steps' not in st.session_state: st.session_state.steps = 0
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'calories' not in st.session_state: st.session_state.calories = 0.0

# --- 3. PDF GENERATION LOGIC ---
def create_pdf_report(steps, bpm, calories):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_fill_color(59, 130, 246)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, "STRIDE-AI CLINICAL REPORT", 0, 1, 'C')
    
    # Patient Info
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.ln(25)
    pdf.cell(0, 10, f"Subject: Harsh Saxena", 0, 1)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d %B, %Y | %I:%M %p')}", 0, 1)
    pdf.cell(0, 10, "System ID: STRIDE-IND-2026", 0, 1)
    pdf.line(10, 85, 200, 85)
    
    # Vital Stats Section
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "1. ACTIVITY TELEMETRY", 0, 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"- Total Stride Volume: {steps} Steps", 0, 1)
    pdf.cell(0, 10, f"- Measured Heart Rate: {bpm} BPM", 0, 1)
    pdf.cell(0, 10, f"- Metabolic Expenditure: {calories} Kcal", 0, 1)
    
    # AI Predictions & Precautions
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "2. AI DIAGNOSTIC INSIGHTS", 0, 1)
    pdf.set_font("Arial", '', 11)
    
    if bpm > 110:
        diagnosis = "Condition: Elevated Cardiac Activity. Heart rate suggests Zone 4/5 training level."
        precaution = "Precaution: Immediate reduction in intensity. Focus on nasal breathing to lower BPM."
    else:
        diagnosis = "Condition: Normal Aerobic Stability. Cardiovascular system is in recovery/low-intensity mode."
        precaution = "Precaution: Optimal state. No immediate intervention required."
        
    pdf.multi_cell(0, 10, diagnosis)
    pdf.multi_cell(0, 10, precaution)
    
    # Summary
    pdf.ln(10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, "Note: This is an AI-generated report for research purposes using LSTM-CNN gait analysis models. Please consult a doctor for clinical validation.", 1, 'C', True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. UI STYLING (SAME AS BEFORE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;700;900&display=swap');
    .stApp { background: #050505; font-family: 'Outfit', sans-serif; color: #e0e0e0; }
    .report-box { background: #111; border-left: 5px solid #3b82f6; padding: 25px; border-radius: 15px; margin-top: 20px; border: 1px solid rgba(59, 130, 246, 0.2); }
    .stat-value { font-size: 2.8rem; font-weight: 900; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color:#3b82f6; font-weight:900;'>STRIDE-AI</h1>", unsafe_allow_html=True)
    page = st.radio("RESEARCH MODULES", ["[01] Step Analytics", "[02] Caloric Detector", "[04] Heart Beat Analysis", "[05] AI Health Report"])
    
    st.markdown("---")
    if st.button("🚀 TRIGGER LIVE WALK"):
        st.session_state.steps += np.random.randint(15, 40)
        st.session_state.heart_rate = np.random.randint(105, 140)
        st.session_state.calories += round(np.random.uniform(1.2, 2.5), 2)
        st.rerun()

    if st.button("🔄 SYSTEM REBOOT"):
        st.session_state.steps = 0
        st.session_state.heart_rate = 72
        st.session_state.calories = 0.0
        st.rerun()

# --- 6. PAGE: AI HEALTH REPORT ---
if page == "[05] AI Health Report":
    st.title("Smart Diagnostic Engine")
    
    st.markdown(f"""
    <div class="report-box">
        <h3>REAL-TIME DATA CAPTURED:</h3>
        <p>Steps: <b>{st.session_state.steps}</b> | BPM: <b>{st.session_state.heart_rate}</b> | Calories: <b>{st.session_state.calories}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 GENERATE CLINICAL MEDICAL REPORT"):
        with st.spinner("Analyzing Bio-Metrics..."):
            time.sleep(2)
            report_data = create_pdf_report(st.session_state.steps, st.session_state.heart_rate, st.session_state.calories)
            
            st.success("Report Generated Successfully!")
            st.download_button(
                label="📥 DOWNLOAD OFFICIAL PDF REPORT",
                data=report_data,
                file_name=f"StrideAI_Report_{datetime.now().strftime('%H%M')}.pdf",
                mime="application/pdf"
            )

# --- OTHER PAGES (Placeholder for Step/Heart/Calorie graphs - use previous code for those) ---
elif page == "[01] Step Analytics":
    st.title("Step Analytics")
    st.markdown(f'<div class="stat-value">{st.session_state.steps}</div>', unsafe_allow_html=True)
    # Add your plotly code here...
