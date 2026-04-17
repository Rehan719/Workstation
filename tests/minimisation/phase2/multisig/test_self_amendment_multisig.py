import pytest
import torch
import time
from agentic_core.minimisation.recirculation.self_amendment import SelfAmendmentGenerator
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_self_amendment_multisig_workflow():
    sb_engine = SchrödingerBridgeEngine()
    ueg = VSBUEGLogger("data/test_multisig.log")
    generator = SelfAmendmentGenerator(sb_engine, ueg)

    # 1. Generate Proposal
    target_objectives = torch.ones(10) / 10.0
    proposal = await generator.generate_amendment_proposal(
        current_constitution={},
        target_objectives=target_objectives,
        context={"optimization_target": "latency_reduction"}
    )

    # 2. Verify MultiSig Configuration
    assert proposal["status"] == "AWAITING_MULTISIG"
    assert proposal["multisig_config"]["required_quorum"] == 3
    assert proposal["multisig_config"]["veto_window_seconds"] == 600

    # 3. Simulate Vote (Quorum check)
    votes = ["CEO", "CLO", "CTO"] # Quorum met
    is_quorum_met = len(votes) >= proposal["multisig_config"]["required_quorum"]
    assert is_quorum_met == True

    # 4. Simulate Veto Window Check
    time_passed = 5 # 5 seconds passed
    is_veto_expired = time_passed >= proposal["multisig_config"]["veto_window_seconds"]
    assert is_veto_expired == False # Still in veto window (Art. 1101)

    # 5. Verify Mathematical Justification
    assert "kl_divergence" in proposal["mathematical_justification"]
    assert proposal["mathematical_justification"]["convergence"] == True
