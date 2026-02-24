import streamlit as st
import time
import pandas as pd
import plotly.express as px
from agentic_core import EnterpriseOrganism

st.set_page_config(page_title="Jules AI v66.0 Enterprise Organism", layout="wide")

st.title("🧬 Jules AI v66.0: The Enterprise Organism")
st.markdown("### Biological Orchestration & Professional Competency Command Center")

if 'organism' not in st.session_state:
    st.session_state.organism = EnterpriseOrganism()
    st.session_state.history = []

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Environmental Input")
    signal_type = st.selectbox("Signal Type", ["GrowthFactor", "Cytokine", "NutrientLevel", "Risk"])
    intensity = st.slider("Intensity", 0.0, 1.0, 0.5)

    if st.button("Trigger Environmental Signal"):
        with st.spinner("Processing through signaling cascades..."):
            result = st.session_state.organism.process_environment(signal_type, intensity, {"source": "Dashboard"})
            st.session_state.history.append(result)
            st.success("Signal Transduced.")

with col2:
    if st.session_state.history:
        latest = st.session_state.history[-1]

        st.header("Genomic Expression Profile")
        exp_df = pd.DataFrame(latest['expression'].items(), columns=['Module', 'Expression Level'])
        fig_exp = px.bar(exp_df, x='Module', y='Expression Level', color='Expression Level', range_y=[0, 1])
        st.plotly_chart(fig_exp, use_container_width=True)

        st.header("Metabolic Flux Allocation")
        flux_df = pd.DataFrame(latest['flux'].items(), columns=['Pathway', 'Flux Units'])
        fig_flux = px.pie(flux_df, values='Flux Units', names='Pathway', hole=.3)
        st.plotly_chart(fig_flux, use_container_width=True)
    else:
        st.info("No active signals. Awaiting environmental stimuli.")

st.sidebar.header("System Status")
st.sidebar.write("Version: v66.0.0")
st.sidebar.write("Clock Speed: 1.2MHz")
st.sidebar.progress(85, text="Organism Integrity")

if st.session_state.history:
    st.header("Conserved Patterns Discovered")
    if latest['patterns']:
        st.write(latest['patterns'])
    else:
        st.write("Synthesizing patterns from history...")
