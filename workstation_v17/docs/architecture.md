# JULES v17.0 Architecture: Sovereign Digital Organism

## 🧠 12-Layer IDBO implementation
The organism follows the Integrated Digital Biological Organism (IDBO) architecture, mapped to the `workstation_v17` codebase:

1.  **Identity (Cellular Genotype)**: Managed in `core/vsb_ueg_logger.py` via SHA-3-512 Merkle-DAG hashes and bitemporal state in `core/sovereign_state_kernel.py`.
2.  **Hardware (Physiological Substrate)**: Classical surrogates in `core/classical_oam_qkd_surrogate.py` for quantum-derived security.
3.  **Expression (Nervous System)**: `core/nemotron_integration.py` providing intent-to-action translation via LatentMoE.
4.  **Regulation (Epigenetics)**: `core/gaas_validator_v4.py` and `core/nemoclaw_runtime.py` enforcing policy-as-code.
5.  **Resilience (Immune System)**: `core/biomimetic_self_healing.py` implementing AEHO repair layers.
6.  **Propagation (Reproduction)**: Mesh-ready interfaces (libp2p stubs) for multi-node federation.
7.  **Module Library (Genetic Code)**: Content-addressed registration of realms in `realms/`.
8.  **Recombination (Mutation/Fusion)**: `core/self_rewriter.py` for autonomous code evolution.
9.  **Orchestration (CNS)**: `core/jules_omega_organism_v17.py` CEO orchestrator.
10. **Evolution (Natural Selection)**: `core/fractal_recirculation.py` managing nested competitive loops.
11. **Civilisation (Ecosystem)**: Domain Realms (Legal, Bio, etc.) interacting via the Virtual Systems Bridge (VSB).
12. **UX (Consciousness)**: The 10-word value proposition anchor and CLI/Council interfaces.

## 🔁 Fractal Recirculation
- **Micro (<100ms)**: Per-agent safety heartbeats.
- **Meso (<15min)**: Workflow and unit-economic optimization.
- **Macro (<60s)**: Strategic evolution and recursive learning.
