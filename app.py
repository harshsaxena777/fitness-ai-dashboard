import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import time

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="STRIDE-AI Pro", layout="wide")

# --- 2. THE REBOOT LOGIC (START FROM ZERO) ---
def reboot_system():
    # Poori session tijori ko khali kar dena
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # User ko feedback dena
    st.toast("System Cleared. Starting from Zero...", icon="🔄")
    time.sleep(1)
    # App refresh hoke login par chali jayegi

# --- 3. SESSION STATE INITIALIZATION ---
# Agar reboot hua hai, toh ye values wapas default par aayengi
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'u_age' not in st.session_state: st.session_state.u_age = 22
if 'steps' not in st.session_state: st.session_state.steps = 0  # <--- Reset to Zero
if 'heart_rate' not in st.session_state: st.session_state.heart_rate = 72 # Baseline BPM
if 'report_ready' not in st.session_state: st.session_state.report_ready = False

# --- 4. LOGIN INTERFACE ---
if not st.session_state.logged_in:
    st.title("🔐 STRIDE-AI: Clinical Access")
    with st.container():
        user = st.text_input("User Email ID", placeholder="admin@stride.ai")
        pwd = st.text_input("Security Pin", type="password")
        if st.button("Initialize Dashboard"):
            if "@" in user:
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 5. TOP NAV & REBOOT BUTTON ---
header_col, reboot_col = st.columns([5, 1])
with header_col:
    st.title("🏥 STRIDE-AI: Professional Diagnostic Suite")
with reboot_col:
    # REBOOT BUTTON: Ispe click karte hi 'reboot_system' function trigger hoga
    if st.button("🔄 Reboot System", help="Clear all data and restart"):
        reboot_system()
        st.rerun()

st.divider()

# --- 6. FUNCTIONAL TABS ---
tabs = st.tabs(["👣 Activity", "🫀 Cardiac", "🧘 Posture", "🧠 AI Report"])

# --- TAB 1: ACTIVITY (WITH MIXED INTERVAL SYNC) ---
with tabs[0]:
    st.subheader("Kinetic Analytics")
    st.metric("Live Step Count", st.session_state.steps)
    
    if st.button("Sync Sensor Data"):
        # Randomized increments (10, 20, or 30)
        random_increment = np.random.choice([10, 20, 30])
        st.session_state.steps += random_increment
        st.toast(f"Data Synced! +{random_increment} steps.")
        time.sleep(0.3)
        st.rerun()
    
    # Graph for visual feel
    st.bar_chart(np.random.randint(0, 100, 24))

# --- TAB 2: CARDIAC ---
with tabs[1]:
    st.metric("Current BPM", f"{st.session_state.heart_rate}")
    if st.button("⚡ Live Sync Pulse"):
        st.session_state.heart_rate = np.random.randint(70, 150)
        st.rerun()

# --- TAB 4: AI REPORT (ELABORATIVE & CLEAN) ---
with tabs[3]:
    st.subheader("📋 Clinical Audit")
    if st.button("🔍 GENERATE DIAGNOSIS"):
        st.session_state.report_ready = True
            
    if st.session_state.report_ready:
        st.markdown(f"""
        ### 🛡️ STRIDE-AI FINAL CLINICAL AUDIT
        ---
        - **Total Steps Recorded:** {st.session_state.steps}
        - **Average Cardiac Load:** {st.session_state.heart_rate} BPM
        - **Posture Integrity:** 79% (Stable)
        
        **Final Verdict:** 
        Subject is in monitoring phase. All sensors are active and reporting baseline values.
        """)

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
