import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
from agentic_core.orchestration.swarm_organism_v67_0 import SwarmOrganismV67_0

st.set_page_config(page_title="Jules AI v67.0 Swarm Dashboard", layout="wide")

st.title("🐝 Jules AI v67.0: Swarm Intelligence Command Center")
st.markdown("### Evolutionary Enhancement & Collective Orchestration")

if 'organism' not in st.session_state:
    st.session_state.organism = SwarmOrganismV67_0()
    st.session_state.history = []
    st.session_state.swarm_nodes = ["organism-001", "organism-002", "organism-003"]

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Swarm Controls")
    goal = st.text_input("High-Level Research Goal", "Analyze quantum neural-immune crosstalk")
    if st.button("Initiate Swarm Workflow"):
        with st.spinner("Decomposing goal into collective tasks..."):
            tasks = st.session_state.organism.execute_swarm_task(goal)
            st.session_state.history.append({"type": "SWARM_START", "goal": goal, "tasks": tasks})
            st.success(f"Dispatched {len(tasks)} tasks to swarm.")

    st.divider()
    st.header("Individual Physiological Health")
    # v66.1 metrics
    intensity = st.slider("Local Stimulus Intensity", 0.0, 1.0, 0.5)
    if st.button("Process Local Signal"):
        res = st.session_state.organism.process_environment_v66_1("GrowthFactor", intensity, {"source": "Dashboard"})
        st.session_state.history.append({"type": "LOCAL_SIGNAL", "result": res})

with col2:
    tab1, tab2, tab3 = st.tabs(["Swarm Topology", "Orchestration DAG", "Fidelity & Coherence"])

    with tab1:
        st.header("Active Swarm Nodes")
        swarm_df = pd.DataFrame({
            "Agent ID": st.session_state.swarm_nodes,
            "Role": ["Leader", "Worker", "Worker"],
            "Load": [3.4, 5.2, 4.1],
            "Status": ["ACTIVE", "ACTIVE", "IDLE"]
        })
        st.table(swarm_df)

        # Simulated Network Latency
        lat_data = pd.DataFrame({
            "Instance": ["001->002", "001->003", "002->003"],
            "Latency (ms)": [14.2, 16.5, 12.8]
        })
        st.plotly_chart(px.bar(lat_data, x="Instance", y="Latency (ms)", title="Inter-Organism Latency (DL Target <12ms Local)"))

    with tab2:
        if st.session_state.history and st.session_state.history[-1]["type"] == "SWARM_START":
            st.header("Task Decomposition Graph")
            tasks = st.session_state.history[-1]["tasks"]
            for t in tasks:
                st.info(f"Task: {t.goal} | Status: {t.status}")
        else:
            st.write("No active swarm workflows.")

    with tab3:
        st.header("Physiological Fidelity (v66.1)")
        # Show latest local signal results if available
        local_signals = [h for h in st.session_state.history if h["type"] == "LOCAL_SIGNAL"]
        if local_signals:
            latest_res = local_signals[-1]["result"]
            st.metric("State-Transition Fidelity", f"{latest_res['fidelity_score']:.4f}")
            st.metric("Integrated State Dist", f"{latest_res['physiological_dist']:.4f}")
        else:
            st.write("Awaiting local physiological telemetry.")

st.sidebar.header("Swarm v67.0 Status")
st.sidebar.write(f"Instance ID: {st.session_state.organism.agent_id}")
st.sidebar.write("Governance: CONSTITUTION v67.0")
st.sidebar.progress(95, text="Swarm Synergy")
st.sidebar.metric("Swarm Allostatic Load", f"{st.session_state.organism.meta_governor.swarm_allostatic_load:.2f}")
