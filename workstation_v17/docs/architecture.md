# 12-Layer IDBO Architecture Mapping

The JULES v17.0 organism maps its 12 biomimetic layers to the following implementation files:

1.  **Identity (Immutable Genome)**: `core/identity.py` (PQC-backed DIDs, TPM attestation).
2.  **Hardware (Physiological Substrate)**: `core/hardware_abstraction.py` (HAL for RTX/DGX, STDP hooks).
3.  **Expression (Sequence-to-Function)**: `core/nemotron_integration.py` (HTN planning, intent translation).
4.  **Regulation (Epigenetic State)**: `core/gaas_validator_v4.py` (Constitutional GaaS intercepts).
5.  **Resilience (Immune System)**: `core/biomimetic_self_healing.py` (AEHO 4-tier repair).
6.  **Propagation (NANITE Mesh)**: `core/federation_libp2p.py` (libp2p P2P discovery).
7.  **Module Library (Genetic Code)**: `core/vsb_ueg_logger.py` (Content-addressed Merkle-DAG store).
8.  **Recombination (Fusion/Mutation)**: `core/cross_domain_transfer.py` (Neural pathway fusion).
9.  **Orchestration (Dynamic CNS)**: `agents/c_suite_v17.py` (LangGraph agent assembly).
10. **Evolution (Natural Selection)**: `core/fractal_recirculation.py` (Nematron NAS competitive loops).
11. **Civilisation (Federation)**: `core/federation_libp2p.py` (Treaty framework, MultiSigCouncil).
12. **UX (Consciousness)**: `realms/realm_implementations.py` (Audience realms).
