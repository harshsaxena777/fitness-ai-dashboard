import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="STRIDE-AI Pro Account", layout="centered")

# --- UPDATED REBOOT LOGIC (Only this part is changed) ---
def reboot_system():
    # Saare session keys ko delete karna
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Initial state par reset karna
    st.toast("System Rebooting... Clearing User Cache", icon="🔄")
    time.sleep(1.5)
    st.rerun()

# --- 2. SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_mail' not in st.session_state: st.session_state.user_mail = ""
if 'steps' not in st.session_state: st.session_state.steps = 5400
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72
if 'u_age' not in st.session_state: st.session_state.u_age = 22
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI Portal")
    email = st.text_input("Email ID Address")
    mobile = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if "@" in email:
            st.session_state.logged_in = True
            st.session_state.user_mail = email
            st.rerun()
    st.stop()

# --- 3. UI STYLING ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; }
    .reboot-container>button { background-color: #ef4444 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. TOP NAV & UPDATED REBOOT BUTTON ---
c_title, c_reboot = st.columns([4, 1])
with c_title:
    st.title("📱 STRIDE-AI Pro")
with c_reboot:
    st.markdown('<div class="reboot-container">', unsafe_allow_html=True)
    if st.button("🔄"):
        reboot_system() # Updated Logic Called Here
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"👤 User: **{st.session_state.user_mail}**")

# --- 5. TABS (As it is, no changes) ---
tabs = st.tabs(["⚙️ Setup", "👣 Steps", "🫀 Heart", "🧘 Posture", "🧠 AI Report"])

# --- Setup Tab ---
with tabs[0]:
    st.session_state.u_age = st.slider("Select Age", 18, 80, st.session_state.u_age)

# --- Steps Tab ---
with tabs[1]:
    st.metric("Current Steps", st.session_state.steps)
    if st.button("Inject Step Packet"):
        st.session_state.steps += 450
        st.rerun()

# --- Heart Tab ---
with tabs[2]:
    st.metric("Pulse Rate", f"{st.session_state.heart_rate} BPM")
    st.line_chart(np.random.randint(60, 160, 15))

# --- Posture Tab ---
with tabs[3]:
    st.metric("Alignment Score", "79%")

# --- AI Report Tab ---
with tabs[4]:
    if st.button("🔍 GENERATE FULL DIAGNOSIS"):
        with st.spinner("Crunching Bio-Data..."):
            time.sleep(2)
            st.session_state.report_ready = True

    if st.session_state.report_ready:
        st.markdown(f"""
        ### 🛡️ STRIDE-AI: FINAL CLINICAL AUDIT
        **Status:** Optimized | **Metabolic Age:** {st.session_state.u_age - 2}
        
        **1. Activity:** {st.session_state.steps} steps.
        **2. Cardiac:** {st.session_state.heart_rate} BPM.
        **3. Biomechanical:** 79% Stable.
        
        **Verdict:** Subject is physiologically optimized.
        """)
