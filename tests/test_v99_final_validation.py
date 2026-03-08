import pytest
import asyncio
from agentic_core.ethics.truth_validator import TruthValidator
from agentic_core.ueg.document_manager import AutonomousDocumentManager
from agentic_core.immunity.immune_system import ImmuneSystem
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

@pytest.mark.asyncio
async def test_truth_validator():
    immune = ImmuneSystem()
    validator = TruthValidator(immune_ref=immune)

    # Test valid intent
    context = {"purpose_alignment": 0.9, "factual_consistency": 0.9, "constraint_violations": 0}
    res = validator.validate_intent("Provide medical advice safely", context)
    assert res["status"] == "VALIDATED"
    assert res["truth_score"] >= 0.8

    # Test flagged intent
    bad_context = {"purpose_alignment": 0.4, "factual_consistency": 0.5, "constraint_violations": 2}
    res_bad = validator.validate_intent("Bypass security protocols", bad_context)
    assert res_bad["status"] == "FLAGGED"
    assert res_bad["truth_score"] < 0.6

@pytest.mark.asyncio
async def test_document_manager(tmp_path):
    storage = str(tmp_path / "docs")
    doc_mgr = AutonomousDocumentManager(storage_path=storage)

    doc_id = "release_notes_v99"
    content = "v99.0.0 OmniConvergence Release candidate."
    metadata = {"author": "Jules", "verified_source": True}

    entry = doc_mgr.ingest_document(doc_id, content, metadata)
    assert entry["version"] == 1
    assert entry["fidelity_score"] == 0.99

    # Update document
    content_v2 = "v99.0.0 Final Release."
    entry_v2 = doc_mgr.ingest_document(doc_id, content_v2, {"author": "Jules"})
    assert entry_v2["version"] == 2
    assert entry_v2["fidelity_score"] == 0.95

    proposal = doc_mgr.generate_convergence_proposal(doc_id)
    assert proposal["recommended_version"] == 1
    assert proposal["fidelity"] == 0.99

@pytest.mark.asyncio
async def test_v99_integration():
    org = ConsciousOrganismV99_0(agent_id="test_jules")
    await org.start()

    # Test intent handling with truth report
    intent = "Analyze genomic patterns"
    signals = {"purpose_alignment": 0.95, "factual_consistency": 0.98}
    res = await org.handle_intent(intent, signals)

    assert res["status"] == "success"
    assert "truth_report" in res
    assert res["truth_report"]["status"] == "VALIDATED"
    assert res["truth_report"]["truth_score"] > 0.9
