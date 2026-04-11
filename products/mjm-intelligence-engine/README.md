# MJM Intelligence Engine v1.0

The Mushahida-Jaiza-Muaina (MJM) Intelligence Engine is a standalone Signature Product within the Workstation ecosystem. It operationalizes the Urdu Intelligence Lifecycle framework into an automated, verifiable, AI-augmented workflow for generating litigation-ready intelligence dossiers.

## 🏗️ Core Methodology

- **Mushahida (Observation):** Fact-finding layer for evidence acquisition (DuckDuckGo Search + BeautifulSoup) and chronological documentation.
- **Jaiza (Evaluation):** Analysis layer for pattern recognition and risk-benefit assessment (LLM-driven via Ollama with heuristic fallback).
- **Muaina (Inspection):** Proposal layer for developing implementation roadmaps (Gantt charts) and litigation-ready packages (UK Employment Tribunal).

## 🚀 Quick Start

### Installation
```bash
cd products/mjm-intelligence-engine
pip install -r requirements.txt
pip install -e .
```

### Usage (Python API)
```python
from core.orchestration.workflow_orchestrator import MJMWorkflowOrchestrator

orchestrator = MJMWorkflowOrchestrator()
# Execute end-to-end pipeline
bundle = await orchestrator.execute_pipeline({
    "domain_id": "patient_safety",
    "queries": ["query 1"],
    "contributor": "user_id"
})
```

## 🌐 UI Stack
- **Frontend:** React 18 + TypeScript + Tailwind CSS
- **Localization:** Support for Urdu (مشاہدہ/جائزہ/معائنہ) and English.

## 🔐 Governance & Verification
Every output element has traceable provenance to source evidence via SHA-256 hashing and immutable checkpointing. Cross-layer traceability ensures that every proposal links back to specific evidence nodes.

## 🏛️ Litigation Ready
The Muaina module generates drafts for UK Employment Tribunal submissions, including ET1 guidance, witness statements, and formal email templates aligned with the Equality Act 2010.
