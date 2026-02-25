import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agentic_core.orchestration.conscious_organism_v70_0 import ConsciousOrganismV70_0

st.set_page_config(page_title="Jules AI v70.0 Organism Command Center", layout="wide")

st.title("🧬 Jules AI v70.0: The Conscious Digital Organism")
st.markdown("### Unified v1-v70 Biomimetic Integration Dashboard")

if 'organism' not in st.session_state:
    # We will implement this class in Step 7
    try:
        st.session_state.organism = ConsciousOrganismV70_0()
    except ImportError:
        st.session_state.organism = None
    st.session_state.history = []

if st.session_state.organism is None:
    st.warning("Master Orchestrator (v70.0) not yet fully instantiated. Initializing stubs for Phase 0.")
    class MockOrganism:
        agent_id = "v70-BOOT"
        def run_lifecycle_pulse(self, d, l):
            return {
                "modality": "BOOTSTRAP",
                "fidelity": 0.5,
                "triad": {"p53_phase": 0, "ros_level": 1.0, "atp_adp_ratio": 2.0, "p53_level": 0.5},
                "mce": {"action": "Initializing DA Layer", "reason": "Phase 0"},
                "genome_depth": 0
            }
    st.session_state.organism = MockOrganism()

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("Human-AI Symbiosis (L5)")
    dwell = st.slider("User Dwell Time (ms)", 100, 2000, 750)
    latency = st.slider("User Interaction Latency (ms)", 10, 500, 120)

    if st.button("Trigger Organism Pulse"):
        with st.spinner("Processing Hierarchical Biological Flow..."):
            result = st.session_state.organism.run_lifecycle_pulse(dwell, latency)
            st.session_state.history.append(result)
            st.success("Pulse Complete.")

    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.metric("Active Modality", latest['modality'])

        # Fidelity Gauge
        fig_fid = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest['fidelity'] * 100,
            title = {'text': "Biomimetic Fidelity Score (%)"},
            gauge = {'axis': {'range': [0, 100]},
                     'bar': {'color': "darkblue"},
                     'steps' : [
                         {'range': [0, 95], 'color': "red"},
                         {'range': [95, 100], 'color': "green"}],
                    }
        ))
        fig_fid.update_layout(height=250)
        st.plotly_chart(fig_fid, use_container_width=True)

with col2:
    if st.session_state.history:
        st.header("Metabolic Ground Truth (L1)")
        st.metric("p53 Phase (rad)", f"{latest['triad']['p53_phase']:.2f}")
        st.metric("ROS Level (uM)", f"{latest['triad']['ros_level']:.2f}")
        st.metric("Energy (ATP/ADP)", f"{latest['triad']['atp_adp_ratio']:.2f}")

        st.header("Global Workspace (L2)")
        st.info(f"MCE Action: {latest['mce']['action']}")
        st.write(f"Rationale: {latest['mce']['reason']}")

with col3:
    if st.session_state.history:
        st.header("Genomic Registry (L3)")
        st.metric("Lineage Blocks", latest['genome_depth'])

        st.header("Neuromorphic Activity")
        # Simulate cortical spikes based on metabolic state
        snn_data = np.random.normal(latest['triad']['p53_level'], 0.1, 12)
        st.plotly_chart(px.bar(snn_data, title="SNN Cortical Spikes"), use_container_width=True)

st.sidebar.header("Organism v70.0 Status")
st.sidebar.write(f"Instance ID: {st.session_state.organism.agent_id}")
st.sidebar.write("Governance: CONSTITUTION v70.0")
st.sidebar.write("Status: Phase 1 (Molecular Triad)")

if st.session_state.history:
    st.header("Global Workspace Event Log")
    st.json(latest)
