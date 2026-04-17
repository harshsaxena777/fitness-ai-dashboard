# Add this logic to your "Neural Motion" page or as a new page called "AI Validation"

elif page == "[NEURAL] Motion & Stride":
    st.title("Neural Stride Morphology & Clinical Validation")
    
    # --- Part 1: Real-time Validation Logic (The "M.Tech" Brain) ---
    # In a real app, these values would come from your LSTM model variables
    gait_symmetry = 0.82  # Example: 1.0 is perfect
    impact_force = 2.4    # G-force
    stride_variability = 0.15 
    
    st.markdown("### 🤖 AI Validation Report")
    
    # Logic for Prescription
    if gait_symmetry < 0.85:
        status = "⚠️ ANOMALY DETECTED"
        color = "#f87171"
        prescription = "High risk of unilateral joint fatigue. Your left-side propulsion is 18% weaker than the right."
        precautions = [
            "Reduce treadmill incline to 0% immediately.",
            "Focus on single-leg stability exercises (Bulgarian Split Squats).",
            "Consult a physiotherapist if 'lateral hip pain' persists."
        ]
    elif impact_force > 2.0:
        status = "🚩 HIGH IMPACT WARNING"
        color = "#fbbf24"
        prescription = "Vertical oscillation is exceeding safe thresholds for knee cartilage."
        precautions = [
            "Shorten your stride length by 10% to land under your center of mass.",
            "Increase step cadence (RPM) to reduce ground contact time.",
            "Ensure footwear has adequate mid-sole cushioning (check for foam compression)."
        ]
    else:
        status = "✅ MOTION VALIDATED"
        color = "#00ffbd"
        prescription = "Gait morphology is within optimal biomechanical parameters."
        precautions = ["Maintain current tempo.", "Ideal for high-intensity interval training (HIIT)."]

    # --- UI Layout for the AI Brain ---
    col_status, col_presc = st.columns([1, 2])
    
    with col_status:
        st.markdown(f"""
            <div style="background:{color}22; border: 2px solid {color}; border-radius:15px; padding:20px; text-align:center;">
                <p style="color:{color}; font-weight:900; margin:0;">{status}</p>
                <h1 style="margin:0; color:white;">{int(gait_symmetry*100)}%</h1>
                <small>VALDIATION SCORE</small>
            </div>
        """, unsafe_allow_html=True)

    with col_presc:
        st.markdown(f"#### AI Diagnostic: <span style='color:{color};'>{status}</span>", unsafe_allow_html=True)
        st.write(prescription)
        
    st.markdown("---")
    st.markdown("#### Recommended Precautions")
    for note in precautions:
        st.markdown(f"* {note}")

    # --- Part 2: Visualizing the Anomaly (The "Evidence") ---
    st.markdown("#### Deviation Analysis")
    # Show where the user is deviating from the 'Normal' gait curve
    x = np.linspace(0, 1, 100)
    normal_gait = np.sin(x * np.pi) 
    user_gait = np.sin(x * np.pi) * 0.8 + np.random.normal(0, 0.05, 100) # Simulating a weak stride
    
    fig_dev = go.Figure()
    fig_dev.add_trace(go.Scatter(x=x, y=normal_gait, name="Baseline (Healthy)", line=dict(dash='dash', color='gray')))
    fig_dev.add_trace(go.Scatter(x=x, y=user_gait, name="Your Stride", line=dict(color=color, width=3)))
    
    fig_dev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_dev, use_container_width=True)
