import pytest
import asyncio
from decimal import Decimal
from datetime import datetime, UTC
from unittest.mock import AsyncMock, MagicMock

from agentic_core.governance.precedent_registry import PrecedentRegistry
from agentic_core.governance.ai_constitutional_judge import ConstitutionalJudge
from agentic_core.resilience.bug_bounty_pipeline import BugBountyPipeline
from agentic_core.resilience.disaster_recovery import DisasterRecovery
from products.capital_fund.treasury.defi_yield_aggregator import TreasuryYieldManager
from products.capital_fund.adapters.qan_bridge import QANBridgeSimulator
from agentic_core.governance.eternal_immutability import EternalImmutabilityGuard

@pytest.fixture
def mock_ueg():
    ueg = MagicMock()
    ueg.log_event = AsyncMock(return_value="evt_999")
    return ueg

@pytest.fixture
def mock_mjm():
    mjm = MagicMock()
    return mjm

@pytest.mark.asyncio
async def test_precedent_registry(mock_ueg):
    registry = PrecedentRegistry()
    registry.ueg = mock_ueg

    precedent = {
        "precedent_id": "TEST_001",
        "title": "Test Case",
        "ruling": "Confirmed"
    }

    hash_val = await registry.add_precedent(precedent)
    assert len(hash_val) == 128 # sha3-512
    mock_ueg.log_event.assert_called_with("PRECEDENT_ANCHORED", pytest.any)

@pytest.mark.asyncio
async def test_ai_judge_adjudication(mock_ueg, mock_mjm):
    judge = ConstitutionalJudge(mock_ueg, mock_mjm)
    dispute = {"id": "DISP_001", "type": "TREATY_BREACH"}

    ruling = await judge.adjudicate(dispute)
    assert ruling["status"] == "PENDING_RATIFICATION"
    assert "ruling_id" in ruling
    mock_ueg.log_event.assert_called_with("AI_JUDGE_RULING_PROPOSED", pytest.any)

@pytest.mark.asyncio
async def test_bug_bounty_critical_patch(mock_ueg):
    reconfigulator = AsyncMock()
    reconfigulator.propose_enhancement.return_value = "patch_sha3"

    pipeline = BugBountyPipeline(mock_ueg, reconfigulator)
    report = {"title": "Critical Overflow", "severity": "CRITICAL"}

    report_id = await pipeline.triage_and_patch(report)
    assert report_id.startswith("BUG_")
    reconfigulator.propose_enhancement.assert_called()
    mock_ueg.log_event.assert_any_call("AUTONOMOUS_PATCH_GENERATED", pytest.any)

@pytest.mark.asyncio
async def test_disaster_recovery_quorum(mock_ueg):
    mesh = AsyncMock()
    mesh.discover_peers.return_value = [{"peer_id": "node_b"}, {"peer_id": "node_c"}, {"peer_id": "node_d"}]

    dr = DisasterRecovery("node_a", mock_ueg, mesh)

    # 1. State Replication
    await dr.replicate_state("state_abc")
    assert mock_ueg.log_event.call_count >= 1

    # 2. Recovery Quorum
    consensus_hash = await dr.initiate_recovery()
    assert consensus_hash == "sha3_last_good_state"
    mock_ueg.log_event.assert_any_call("RECOVERY_QUORUM_REACHED", pytest.any)

@pytest.mark.asyncio
async def test_defi_yield_allocation(mock_ueg):
    engine = AsyncMock()
    yield_mgr = TreasuryYieldManager(mock_ueg, engine)

    await yield_mgr.auto_deploy_yield(Decimal("1000000"), Decimal("50000"))

    engine.execute_defi_deposit.assert_called()
    mock_ueg.log_event.assert_any_call("TREASURY_YIELD_DEPLOYED", pytest.any)

@pytest.mark.asyncio
async def test_pq_cross_chain_simulator(mock_ueg):
    bridge = QANBridgeSimulator(mock_ueg)
    receipt = await bridge.settle_cross_node(Decimal("1000"), "node_b", "node_a")

    assert receipt["status"] == "FINALIZED"
    assert receipt["pqc_algorithm"] == "ML-DSA-87"
    assert await bridge.get_pq_balance("node_b") == Decimal("1000")
    mock_ueg.log_event.assert_called()

@pytest.mark.asyncio
async def test_eternal_immutability_guard(mock_ueg):
    # Mock immutable_genome.yaml creation
    import os
    genome_path = "tests/phase9/test_immutable.yaml"
    os.makedirs("tests/phase9", exist_ok=True)
    with open(genome_path, "w") as f:
        f.write("immutable_articles: [1128, 1135]\n")

    guard = EternalImmutabilityGuard(mock_ueg, genome_path)

    # Valid amendment
    assert await guard.validate_amendment([1150, 1160]) is True

    # Invalid amendment (Article 1135 is owner veto)
    assert await guard.validate_amendment([1135]) is False
    mock_ueg.log_event.assert_called_with("ETERNAL_IMMUTABILITY_VIOLATION", pytest.any)
