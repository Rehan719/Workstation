# MJM Intelligence Engine v1.0

The Mushahida-Jaiza-Muaina (MJM) Intelligence Engine is a standalone Signature Product within the Workstation ecosystem. It operationalizes the Urdu Intelligence Lifecycle framework into an automated, verifiable, AI-augmented workflow for generating litigation-ready intelligence dossiers.

## 🏗️ Core Methodology

- **Mushahida (Observation):** Fact-finding layer for evidence acquisition and chronological documentation.
- **Jaiza (Evaluation):** Analysis layer for pattern recognition, risk-benefit assessment, and regulatory alignment.
- **Muaina (Inspection):** Proposal layer for developing implementation roadmaps and litigation-ready packages.

## 🚀 Quick Start

### Installation
```bash
cd products/mjm-intelligence-engine
pip install -e .
```

### Usage (CLI)
```python
from core.workflow_orchestrator import MJMWorkflowOrchestrator

orchestrator = MJMWorkflowOrchestrator()
# 1. Start Observation
m_id = orchestrator.run_mushahida(["query 1", "query 2"], "user_id")
# 2. Run Analysis
j_id = orchestrator.run_jaiza(m_id, "user_id")
# 3. Generate Proposal
mu_id = orchestrator.run_muaina(j_id, "selected_option", "user_id")
```

## 🌐 UI Stack
- **Frontend:** React 18 + TypeScript + Tailwind CSS
- **Localization:** Support for Urdu (مشاہدہ/جائزہ/معائنہ) and English.

## 🔐 Governance & Verification
Every output element has traceable provenance to source evidence via SHA-256 hashing and immutable checkpointing.
