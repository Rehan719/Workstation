import pytest
import asyncio
from src.orchestrator.orchestrator import Orchestrator
from src.scholarship.grant_generator import GrantProposalGenerator
from src.scholarship.policy_generator import PolicyBriefGenerator
from src.orchestrator.collaboration import CollaborativeIntelligenceProtocol

@pytest.mark.asyncio
async def test_v53_scholarship_extension():
    orchestrator = Orchestrator()
    grant_gen = GrantProposalGenerator(orchestrator.ueg)
    policy_gen = PolicyBriefGenerator(orchestrator.ueg)

    proposal = await grant_gen.generate_proposal("PSC Cure", ["Alice", "Bob"])
    assert "v99.0.0" in proposal["title"]
    assert len(proposal["specific_aims"]) == 2

    brief = await policy_gen.generate_brief("AI Safety", "Regulators")
    assert brief["integrity_level"] == "Formally Verified"
    assert "v99.0.0" in brief["executive_summary"]

@pytest.mark.asyncio
async def test_v53_collaboration_protocol():
    orchestrator = Orchestrator()
    collab = CollaborativeIntelligenceProtocol(orchestrator.ueg)

    proposal = {"action": "accept_hypothesis_1"}
    votes = {"agent_alpha": True, "agent_beta": True, "agent_gamma": True, "user_admin": True}

    decision = await collab.process_collaborative_decision("test_user", proposal, votes)
    assert decision["consensus"]["status"] == "COMMITTED"
    assert "attribution" in decision

@pytest.mark.asyncio
async def test_v53_adversarial_testing():
    orchestrator = Orchestrator()
    hypothesis_data = {
        "metrics": {"variance": 0.1},
        "reasoning": "Strong evidence exists."
    }

    # Layer 5 upgraded to Adversary (which is an AdversarialHypothesisTestingEngine)
    report = await orchestrator.verifier.l5.probe_hypothesis("hypo_1", hypothesis_data)
    assert "robustness_score" in report
    assert "attack_reports" in report
