# MJM Intelligence Engine API Reference

## Core Engines

### `MushahidaEngine`
Located in `core/mushahida/engine.py`.
- `acquire_evidence(queries: List[str], domain: str) -> EvidenceGraph`: Initiates fact-finding.
- `validate_provenance(item: EvidenceItem) -> Dict[str, Any]`: Verifies SHA-256 integrity.

### `JaizaEngine`
Located in `core/jaiza/engine.py`.
- `analyze(graph: EvidenceGraph) -> AnalysisDossier`: Performs AI-driven pattern recognition.
- `assess_risk_benefit(patterns, criteria) -> List[Dict]`: Multi-criteria decision analysis.

### `MuainaEngine`
Located in `core/muaina/engine.py`.
- `develop_proposal(dossier, option_id) -> ProposalPackage`: Builds actionable plans.
- `export_litigation_ready(package) -> Dict`: Formats for UK Employment Tribunal.

## Workflow

### `MJMWorkflowOrchestrator`
Located in `core/workflow_orchestrator.py`.
Manages the state machine and checkpointing for the intelligence lifecycle.
- `run_mushahida(queries, contributor)`
- `run_jaiza(checkpoint_id, contributor)`
- `run_muaina(checkpoint_id, option_id, contributor)`
