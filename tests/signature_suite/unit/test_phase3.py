import pytest
import asyncio
from agentic_core.governance.amendment.self_amendment import SelfAmendmentEngine
from agentic_core.governance.multisig.ai_council import AICouncilSimulator
from agentic_core.legal.evolution.rule_evolution import LegalRuleEvolver
from agentic_core.mega_project.synthesizer import MegaProjectSynthesizer
from agentic_core.legal.precision_engine import UKLegalPrecisionEngine

class MockLegalEngine(UKLegalPrecisionEngine):
    def agent_covers_statute(self, agent, statutes): return True
    def validate(self, intent, context): return type('obj', (object,), {'is_compliant': True, 'coverage_score': 1.0})()
    def validate_assignment(self, assignment, tasks, agents): return 1.0

@pytest.mark.asyncio
async def test_self_amendment():
    engine = SelfAmendmentEngine()
    proposal = await engine.propose_amendment(1104, "Text", "Rationale")
    assert proposal["status"] == "proposed"

@pytest.mark.asyncio
async def test_council_voting():
    members = [{"id": "CLO", "expertise": 1.0, "reputation": 0.9}]
    council = AICouncilSimulator(members=members)
    proposal = {"id": "P1", "sb_kl_divergence": 0.1}
    vote = await council.vote_on_amendment(proposal)
    assert vote["approved"] is True

@pytest.mark.asyncio
async def test_legal_rule_evolution():
    mock_engine = MockLegalEngine()
    evolver = LegalRuleEvolver(legal_engine=mock_engine)
    new_rules = await evolver.evolve_for_new_statute("New Precedent 2024", {"coverage_impact": 0.1})
    assert new_rules["status"] == "evolved"

@pytest.mark.asyncio
async def test_mega_project_synthesis():
    synth = MegaProjectSynthesizer()
    deliverables = synth.generate_deliverables("Biofoundry_X", {"data": "verified"})
    assert "business_plan" in deliverables
