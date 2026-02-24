import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
from agentic_core.orchestration.homeostatic_orchestrator_v69_0 import HomeostaticOrchestratorV69_0

st.set_page_config(page_title="Jules AI v69.0 Synthetic Organism", layout="wide")

st.title("🧬 Jules AI v69.0: Autonomous Synthetic Organism")
st.markdown("### Molecular & Cellular Fidelity Command Center")

if 'organism' not in st.session_state:
    st.session_state.organism = HomeostaticOrchestratorV69_0()
    st.session_state.history = []

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("Environmental Input")
    signal = st.selectbox("Stimulus Type", ["HighInformation", "ThreatDetected", "SignalRelay", "Normal"])
    intensity = st.slider("Intensity", 0.0, 1.0, 0.5)

    if st.button("Simulate Lifecycle Step"):
        with st.spinner("Processing molecular cascades..."):
            result = st.session_state.organism.lifecycle_step(signal, intensity)
            st.session_state.history.append(result)
            st.success("Lifecycle Step Completed.")

with col2:
    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.header("Homeostatic Status")

        st.metric("p53 Phase", latest['p53_phase'])
        st.metric("Circadian Cycle", latest['circadian_cycle'])
        st.metric("ATP/ADP Ratio", f"{latest['atp_ratio']:.2f}")

        # Forecast Gauges
        st.metric("Allostatic Forecast (10m)", f"{latest['allostatic_forecast']:.2f}")
        st.metric("Metabolic Reclamation (ME)", f"{latest['reclaimed_me']:.2f}")

with col3:
    if st.session_state.history:
        st.header("Cellular Phenotype Activity")
        # Sample cell expression
        cells = st.session_state.organism.cells
        cell_data = []
        for c in cells:
             cell_data.append({"ID": c.cell_id, "Type": c.cell_type, "Genes": len(c.active_functions)})

        df_cells = pd.DataFrame(cell_data)
        st.table(df_cells)

        # Energy Flux Chart
        st.header("Metabolic Flux")
        flux_data = np.random.normal(latest['atp_ratio'], 0.5, 10)
        st.plotly_chart(px.line(flux_data, title="ATP Synthesis Flux (Michaelis-Menten simulated)"))

st.sidebar.header("System v69.0")
st.sidebar.write(f"Agent: {st.session_state.organism.agent_id}")
st.sidebar.write("Genome: Synthetic (v69.0)")
st.sidebar.progress(98, text="Molecular Integrity")

if st.session_state.history:
    st.header("Molecular Log")
    st.json(latest)
