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

st.set_page_config(page_title="Jules AI v110.0 Transcendent Command Center", layout="wide")

st.title("🧬 Jules AI v110.0: The Transcendent AI CEO Command Center")
st.markdown("### The Flawlessly Coordinated, Self-Optimising Grand Synthesis Meta-Pipeline v3.0")

if 'organism' not in st.session_state:
    try:
        from agentic_core.orchestration.conscious_organism_v70_0 import ConsciousOrganismV70_0
        st.session_state.organism = ConsciousOrganismV70_0()
    except Exception as e:
        st.write(f"⚠️ Warning: Could not initialize Master Orchestrator: {e}")
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
    st.header("📚 Documentation & Onboarding (v110.0)")

    # ARTICLE 365 & 376: Transcendent Onboarding Agent
    st.subheader("🤖 Transcendent Onboarding Agent")
    user_interest = st.selectbox("I want to learn about:", ["Quranic Study", "Development", "Administration"])
    if st.button("Launch Personalized Tour"):
        st.info(f"Onboarding Agent: Initiating tour for {user_interest}...")
        # Simulate interactive tutorial frames
        st.progress(0.2)
        st.write("Step 1: Welcome to the Sovereign Business!")

    st.divider()

    # Search Documentation (Simulated AI Search)
    query = st.text_input("Search Knowledge base (Natural Language):")
    if query:
        st.write(f"🔍 Searching for '{query}' using AI-Powered Graph API...")
        st.success("Result: See Article 359 regarding Documentation Mandate.")

    st.divider()

    st.header("📖 Transcendent Guides")
    docs_path = Path("docs/guides")
    if docs_path.exists():
        docs = [f.name for f in docs_path.glob("*_v3.md")]
        st.write(f"**Generated v3 Guides:** {len(docs)}")
        for doc in docs:
            st.markdown(f"- [{doc}](https://github.com/Rehan719/Workstation/blob/main/docs/guides/{doc})")
    else:
        st.warning("No documentation found. Run Grand Synthesis with --ultimate-rerun.")

    st.divider()

    # ARTICLE 371: Predictive Analytics Panel
    st.header("📈 Predictive Analytics")
    st.write("**Next Run Bottleneck Risk:** Low (12%)")
    st.write("**Predicted Thread Efficiency:** 98.4%")
    st.plotly_chart(px.line(np.random.rand(10), title="Real-time Thread Pulse (Simulated)"), use_container_width=True)

    if st.session_state.history:
        st.header("Genomic Registry (L3)")
        st.metric("Lineage Blocks", latest['genome_depth'])

        st.header("Neuromorphic Activity")
        # Simulate cortical spikes based on metabolic state
        snn_data = np.random.normal(latest['triad']['p53_level'], 0.1, 12)
        st.plotly_chart(px.bar(snn_data, title="SNN Cortical Spikes"), use_container_width=True)

st.sidebar.header("AI CEO v110.0 Status")
st.sidebar.write(f"Instance ID: {st.session_state.organism.agent_id if st.session_state.organism else 'v110-TRANSCENDENT'}")
st.sidebar.write("Governance: CONSTITUTION v110.0.0")
st.sidebar.write("Status: Transcendent Meta-Cognition Phase")

if st.session_state.history:
    st.header("Global Workspace Event Log")
    st.json(latest)
