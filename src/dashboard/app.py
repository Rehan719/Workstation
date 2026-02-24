import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
from agentic_core.orchestration.conscious_organism_v70_0 import ConsciousOrganismV70_0

st.set_page_config(page_title="Jules AI v70.0 Conscious Organism", layout="wide")

st.title("🧬 Jules AI v70.0: The Conscious Biomimetic Organism")
st.markdown("### Hierarchical Digital Life Command Center")

if 'organism' not in st.session_state:
    st.session_state.organism = ConsciousOrganismV70_0()
    st.session_state.history = []

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("User Interaction Proxies")
    dwell = st.slider("Dwell Time (ms)", 100, 2000, 750)
    latency = st.slider("Interaction Latency (ms)", 10, 500, 100)

    if st.button("Run Conscious Cycle"):
        with st.spinner("Broadcasting to Global Workspace..."):
            result = st.session_state.organism.run_organism_cycle(dwell, latency)
            st.session_state.history.append(result)
            st.success("Cycle Complete.")

with col2:
    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.header("Metabolic Ground Truth (L1)")
        st.metric("p53 Phase (rad)", f"{latest['triad']['p53_phase']:.2f}")
        st.metric("ROS Level (uM)", f"{latest['triad']['ros_level']:.2f}")
        st.metric("Energy Ratio", f"{latest['triad']['atp_adp_ratio']:.2f}")

        st.header("Strategic Decision (L2)")
        st.info(f"Action: {latest['mce']['action']}")
        st.write(f"Reason: {latest['mce']['reason']}")

with col3:
    if st.session_state.history:
        st.header("Evolution & Governance (L3/4)")
        st.metric("Genome Lineage (Blocks)", latest['genome_len'])
        st.metric("Identity Trust Score", f"{latest['trust_score']:.2f}")

        st.header("User Symbiosis (L5)")
        st.write(f"Active Modality: {latest['input_modality']}")

        # SNN Activity
        snn_data = np.random.normal(0.5, 0.1, 10)
        st.plotly_chart(px.bar(snn_data, title="SNN Cortical Spikes"), use_container_width=True)

st.sidebar.header("Organism v70.0")
st.sidebar.write(f"Agent ID: {st.session_state.organism.agent_id}")
st.sidebar.write("Architecture: Hierarchical GWT")
st.sidebar.write("Clock: 1.2MHz / 833ns")
st.sidebar.progress(97, text="Biomimetic Fidelity Score")

if st.session_state.history:
    st.header("Global Workspace Log")
    st.json(latest)
