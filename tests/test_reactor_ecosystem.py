import pytest
import asyncio
from agentic_core.reactor.science import ScienceReactor
from agentic_core.reactor.law import LawReactor
from agentic_core.reactor.employment import EmploymentReactor
from agentic_core.reactor.religion import ReligionReactor
from agentic_core.reactor.sovereign_business import SovereignBusinessIncubator
from agentic_core.quantum.interface import UnifiedQuantumInterface
from agentic_core.business.commander import AICommander
from agentic_core.business.dispatcher import AIDispatcher

@pytest.mark.asyncio
async def test_science_reactor_incubation():
    reactor = ScienceReactor()
    res = await reactor.incubate("Quantum Biology", {})
    assert res["status"] == "INCUBATION_COMPLETE"
    assert "hypotheses" in res

@pytest.mark.asyncio
async def test_law_reactor_compliance():
    reactor = LawReactor()
    res = await reactor.incubate("Service Agreement", {})
    assert "compliance_report" in res
    assert res["risk_score"] < 0.5

@pytest.mark.asyncio
async def test_employment_launch_kit():
    reactor = EmploymentReactor()
    res = await reactor.incubate("Software Engineer", {})
    assert res["status"] == "READY_FOR_LAUNCH"
    bundle = res["launch_kit"]
    assert bundle["metadata"]["type"] == "CareerLaunchKit"
    assert len(bundle["items"]) == 3

@pytest.mark.asyncio
async def test_religion_reactor_scholarship():
    reactor = ReligionReactor()
    res = await reactor.incubate("Surah Al-Fatiha", {})
    assert res["status"] == "SCHOLARLY_READY"
    assert "scholarly_tafsir" in res

@pytest.mark.asyncio
async def test_quantum_interface_free_tier():
    qi = UnifiedQuantumInterface()
    res = await qi.run_circuit({"name": "Test"}, tier="free")
    assert res["backend"] == "internal_tensor_sim"
    assert "advantage_projection" in res
    assert res["advantage_projection"]["advantage_status"] == "SIGNIFICANT"

@pytest.mark.asyncio
async def test_ai_ceo_marketing():
    commander = AICommander("SOVEREIGN_V99")
    res = await commander.launch_campaign("science", "Researchers")
    assert res["status"] == "PUBLISHED"

def test_ai_dispatcher_onboarding():
    commander = AICommander("SOVEREIGN_V99")
    dispatcher = AIDispatcher(commander)
    dispatcher.onboard_client("user_001", "law", "pro")
    dispatcher.meter_usage("user_001", "law", "contract_generation")

@pytest.mark.asyncio
async def test_live_deployment_pipeline():
    sbi = SovereignBusinessIncubator()
    # Incubate with auto_deploy=True
    res = await sbi.incubate("Organic Coffee Chain", {"auto_deploy": True})
    assert res["status"] == "LIVE"
    assert "live_entity" in res
    assert "frontend_url" in res["live_entity"]

@pytest.mark.asyncio
async def test_reactor_live_api_integration():
    reactor = ScienceReactor()
    res = await reactor.incubate("Genomic Evolution", {})
    # Verify live API search results are present
    assert res["sources_count"] > 0
    assert "arXiv" in res["scientific_paper"]["content"] or "Live Research" in res["literature_review"]["content"]

@pytest.mark.asyncio
async def test_ai_ceo_oversight():
    from agentic_core.ai_ceo.oversight_manager import HumanOversightManager
    hom = HumanOversightManager()

    # Test Auto-approval
    id1 = hom.request_approval("LOW_RISK_MARKETING", {"msg": "hello"})
    assert id1.startswith("rev_")
    assert any(a["id"] == id1 and a["status"] == "AUTO_APPROVED" for a in hom.audit_log)

    # Test Pending/Reject
    id2 = hom.request_approval("HIGH_STAKES_PRICING", {"price": 999.0})
    assert any(a["id"] == id2 and a["status"] == "PENDING" for a in hom.pending_actions)
    hom.reject_action(id2, "Too expensive")
    assert any(a["id"] == id2 and a["status"] == "REJECTED" for a in hom.audit_log)
