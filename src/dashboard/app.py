import sys
from pathlib import Path
# Add repository root to Python path
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import asyncio
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

# Article 284: Unified Product Interface Mandate
st.set_page_config(page_title="Jules AI v100.0 Apotheosis Dashboard", layout="wide")

st.title("🧬 Jules AI v100.0: Apotheosis of Synergy")
st.markdown("### Integrated Digital Reactor Ecosystem (Science, Religion, Law, Employment, Education)")

if 'organism' not in st.session_state:
    st.session_state.organism = ConsciousOrganismV99_0()
    st.session_state.history = []

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("Human-AI Symbiosis")
    intent = st.text_input("User Intent", "Research Quantum Biology")
    domain = st.selectbox("Domain Reactor", ["Science", "Religion", "Law", "Employment", "Education"])

    if st.button("Execute Transcendent Cycle"):
        with st.spinner(f"Orchestrating {domain} Reactor..."):
            async def run():
                if not getattr(st.session_state.organism, 'is_running', False):
                    await st.session_state.organism.start()
                return await st.session_state.organism.handle_intent(intent, {"domain": domain.lower()})

            result = asyncio.run(run())
            st.session_state.history.append(result)
            st.success("Cycle Complete.")

    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.metric("Action Taken", latest.get('action', 'N/A'))
        if hasattr(st.session_state.organism, 'granularity'):
            st.write(f"Granularity Mode: {st.session_state.organism.granularity.current_mode}")

with col2:
    st.header("Metabolic & Cognitive Status")
    st.write("Survival Instinct Hierarchy (SIH): **ACTIVE**")

    # Simple vital metrics visualization
    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.write("Fidelity Target: ≥99.2%")
        if 'result' in latest:
             st.json(latest['result'])
    else:
        st.info("Trigger a cycle to view real-time metrics.")

with col3:
    st.header("Quantum & Evolution")
    if st.session_state.history:
        latest = st.session_state.history[-1]
        if 'result' in latest and isinstance(latest['result'], dict) and 'backend' in latest['result']:
            st.metric("Quantum Backend", latest['result']['backend'])

        st.write("Recursive Prompt Evolution: **ENABLED**")
        if latest.get('new_prompt'):
            st.text_area("Mutated Prompt", latest['new_prompt'], height=150)

st.divider()
st.sidebar.header("System v99.0 Status")
if hasattr(st.session_state.organism, 'agent_id'):
    st.sidebar.write(f"Agent ID: `{st.session_state.organism.agent_id}`")
st.sidebar.write("Governance: `CONSTITUTION v100.0` (288 Articles)")
st.sidebar.write("Era: `TRANSCENDENT`")

if st.session_state.history:
    with st.expander("Transcendent Event Log"):
        st.json(st.session_state.history)
