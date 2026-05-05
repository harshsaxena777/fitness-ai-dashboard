# --- 1. THE REBOOT LOGIC (START FROM ZERO) ---
def reboot_system():
    # Poora session data delete karna
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # User ko feedback dena aur zero-reset confirm karna
    st.toast("System Resetting... All metrics set to zero.", icon="🔄")
    time.sleep(1)
    # Refresh hoke app initial defaults par chali jayegi

# --- 2. SESSION STATE INITIALIZATION ---
# Jab reboot call hoga, toh ye values default (Zero) par set ho jayengi
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'steps' not in st.session_state: 
    st.session_state.steps = 0  # <--- Reboot ke baad zero se shuru hoga
if 'heart_rate' not in st.session_state: 
    st.session_state.heart_rate = 0 # <--- Pulse bhi zero/baseline
if 'report_ready' not in st.session_state: 
    st.session_state.report_ready = False
if 'u_age' not in st.session_state:
    st.session_state.u_age = 22 # Default age reset
