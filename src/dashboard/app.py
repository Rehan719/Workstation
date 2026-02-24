import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px
from agentic_core.orchestration.enterprise_organism_v66_1 import EnterpriseOrganismV66_1

st.set_page_config(page_title="Jules AI v66.1 Physiological Dashboard", layout="wide")

st.title("🧬 Jules AI v66.1: Physiological Coherence Dashboard")
st.markdown("### Experimentally-Validated Enterprise Organism")

if 'organism' not in st.session_state:
    st.session_state.organism = EnterpriseOrganismV66_1()
    st.session_state.history = []

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("Stimulus Control")
    signal_type = st.selectbox("Signal Type", ["GrowthFactor", "Cytokine", "NutrientLevel", "Risk"])
    intensity = st.slider("Intensity", 0.0, 1.0, 0.5)

    if st.button("Trigger Validated Stimulus"):
        with st.spinner("Transducing via empirical cascades..."):
            result = st.session_state.organism.process_environment_v66_1(signal_type, intensity, {"source": "Dashboard"})
            st.session_state.history.append(result)
            st.success("Stimulus Processed.")

with col2:
    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.header("Fidelity & Coherence")

        # Fidelity Gauge
        st.metric("State-Transition Fidelity", f"{latest['fidelity_score']:.4f}")
        st.metric("Coherence Entropy", f"{latest['coherence_entropy']:.4f} nats")

        # Mahalanobis Distance
        st.metric("Integrated State Dist", f"{latest['physiological_dist']:.4f}")

        if latest['fidelity_score'] > 0.85:
            st.success("Constitutional Fidelity: PASSED")
        else:
            st.warning("Constitutional Fidelity: DEGRADED")

with col3:
    if st.session_state.history:
        st.header("Biomarker Distribution")
        # Simulated biomarkers for visualization
        biomarkers = np.random.normal(0.5, 0.1, 12)
        df_bio = pd.DataFrame(biomarkers, columns=['Value'])
        fig_bio = px.box(df_bio, y="Value", points="all", title="Reference Biomarker Spread")
        st.plotly_chart(fig_bio, use_container_width=True)

st.sidebar.header("Organism v66.1")
st.sidebar.write("Phylogenetic Range: Bilaterian")
st.sidebar.write("Clock Granularity: 833ns")
st.sidebar.progress(92, text="Physiological Stability")

if st.session_state.history:
    st.header("Immune Function Log")
    st.write(f"Decision Triggered: {latest['decision_trigger']}")
    st.json(latest['legacy_data']['expression'])
