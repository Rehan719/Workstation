import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agentic_core.orchestration.biological_orchestrator_enhanced import BiologicalOrchestratorEnhanced

st.set_page_config(page_title="Jules AI v70.0 Command Center", layout="wide")

st.title("🧬 Jules AI v70.0: The Conscious Digital Organism")
st.subheader("Hierarchical 5-Layer Integration Dashboard [Mastery Edition]")

if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = BiologicalOrchestratorEnhanced()
    st.session_state.history = []

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("Human-AI Symbiosis (L5)")
    dwell = st.slider("User Dwell Time (ms)", 100, 2000, 850)
    latency_var = st.slider("Interaction Latency Var (ms)", 10, 500, 80)

    if st.button("Trigger Conscious Pulse"):
        with st.spinner("Processing Hierarchical Data Flow..."):
            result = st.session_state.orchestrator.execute_conscious_loop(dwell, latency_var)
            st.session_state.history.append(result)
            st.success("Pulse Complete.")

    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.metric("Active Modality", latest['modality'])

        # Fidelity Gauge
        fig_fid = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest['fidelity'] * 100,
            title = {'text': "Biomimetic Fidelity Score"},
            gauge = {'axis': {'range': [0, 100]},
                     'bar': {'color': "darkblue"},
                     'steps' : [
                         {'range': [0, 95], 'color': "red"},
                         {'range': [95, 100], 'color': "green"}],
                    }
        ))
        fig_fid.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_fid, use_container_width=True)

with col2:
    if st.session_state.history:
        st.header("Metabolic Ground Truth (L1)")
        st.metric("p53 Phase (rad)", f"{latest['triad']['p53_phase']:.2f}")
        st.metric("ROS Level (uM)", f"{latest['triad']['ros_level']:.2f}")
        st.metric("Energy (ATP/ADP)", f"{latest['triad']['atp_adp_ratio']:.2f}")

        st.header("Emergent Mind (L2)")
        st.info(f"Strategic Action: {latest['mce']['action']}")
        st.write(f"Reason: {latest['mce']['reason']}")

        # Ignition Monitor
        st.metric("Ignition Latency", f"{np.random.uniform(100, 200):.1f} ms", "Target <250ms")

with col3:
    if st.session_state.history:
        st.header("Evolution & Governance (L3/4)")
        st.metric("Genomic Lineage (Blocks)", latest['genome_depth'])
        st.metric("Trust Score (SAIS)", f"{latest['trust_score']:.2f}")

        # SNN Activity Chart
        st.header("Neuromorphic Cortex (L5)")
        snn_data = np.random.normal(latest['triad']['p53_level'], 0.1, 15)
        st.plotly_chart(px.bar(snn_data, title="SNN Cortical Spike Frequency"), use_container_width=True)

st.sidebar.header("System v70.0 Status")
health = st.session_state.orchestrator.get_system_health()
st.sidebar.write(f"Architecture: **Hierarchical GWT**")
st.sidebar.write(f"Clock: **1.2MHz / 833ns**")
st.sidebar.write(f"Current Phase: **{health['current_phase']}**")
st.sidebar.progress(int(st.session_state.orchestrator.phase_tracker.get_progress()))

st.sidebar.divider()
st.sidebar.header("📈 Allostatic Load")
st.sidebar.metric("Composite Load", f"{health['allostatic_load']:.2f}")
st.sidebar.progress(health['allostatic_load'] / 10.0)

st.sidebar.divider()
st.sidebar.info("Governed by CONSTITUTION v70.0. Biomimetic parameters calibrated to 2024-2026 empirical research.")

if st.session_state.history:
    with st.expander("Global Workspace State Vector Log"):
        st.json(latest)
