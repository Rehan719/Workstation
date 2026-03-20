# v154.0 Architecture Mapping: The Grand Synthesis

## Executive Summary
This document provides the canonical mapping between legacy Workstation modules and the new **Unified Seven-Layer Architecture** established in v154.0.

## Layer 1: Genomic Foundation (The Soul)
- **Legacy Components**: `agentic_core/constitution/`, `agentic_core/evolution/ueg_merkle_dag.py`.
- **v154.0 Path**: `agentic_core/layers/l1_genomic/`.
- **Primary Source**: `genome/constitution.work` (Merkle-DAG root).

## Layer 2: Edge Runtime & Hardware Abstraction (The Body)
- **Legacy Components**: `agentic_core/config/parameters.py`.
- **v154.0 Path**: `agentic_core/layers/l2_runtime/`.
- **Integration**: Pluggable `llama.cpp` and `ONNX Runtime` interfaces.

## Layer 3: Biomimetic Integration Layer (Autonomic Systems)
- **Legacy Components**: `agentic_core/homeostasis/`, `agentic_core/immune/`, `agentic_core/swarm/`.
- **v154.0 Path**: `agentic_core/layers/l3_biomimetic/`.

## Layer 4: Agent & Model Library (Genetic Memory)
- **Legacy Components**: `agentic_core/registry/`, `agentic_core/models/`.
- **v154.0 Path**: `agentic_core/layers/l4_library/`.

## Layer 5: Recombination Engine (The Workshop)
- **Legacy Components**: `agentic_core/evolution/recombination/`.
- **v154.0 Path**: `agentic_core/layers/l5_recombination/`.
- **Algorithms**: TIES-Merging, DARE, Adapter Grafting.

## Layer 6: Evolution & Orchestration (The Hive Mind)
- **Legacy Components**: `agentic_core/orchestration/clownfish.py`, `agentic_core/api/v280/csuite_enhanced.py`.
- **v154.0 Path**: `agentic_core/layers/l6_evolution/`.

## Layer 7: User Experience (The Universe)
- **Legacy Components**: `apps/web/src/pages/`, `apps/mobile/`.
- **v154.0 Path**: `agentic_core/layers/l7_ux/` (Logic) + `apps/web/src/pages/developers/Forge.tsx`.
- **First Light**: Developer Realm (The Forge).

---
*Authorized by the VSB AI CEO & Repo Owner.*
