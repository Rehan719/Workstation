import pytest
import asyncio
from decimal import Decimal
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from agents.legal.ai_ceo_legal_entity import AICEOLegalEntity
from agentic_core.federation.autonomous_mesh import AutonomousMesh
from products.capital_fund.mesh.treaty_schema import BilateralTreaty
from products.capital_fund.governance.dao_executive_bridge import DAOExecutiveBridge
from products.capital_fund.governance.safe_automator import GnosisSafeAutomator
from agentic_core.verification.tlc_runner import TLCRuntimeChecker
from agentic_core.governance.self_evolving_constitution import SelfEvolvingConstitution
from products.capital_fund.sub_funds.genome_manager import SubFundGenomeManager
from products.capital_fund.core.vault import CapitalVault

@pytest.fixture
def mock_ueg():
    ueg = MagicMock()
    ueg.log_event = AsyncMock(return_value="evt_123")
    ueg.query_events = AsyncMock(return_value=[{"vote": "yes"}] * 3)
    return ueg

@pytest.fixture
def mock_validator():
    val = MagicMock()
    val.validate_action = AsyncMock(return_value={"passed": True, "hash": "sha3_abc"})
    return val

@pytest.fixture
def mock_signer():
    signer = MagicMock()
    signer.sign = AsyncMock(return_value=b"pqc_signature")
    return signer

@pytest.mark.asyncio
async def test_vault_deposit(mock_ueg, mock_validator):
    vault = CapitalVault("did:owner", mock_validator, mock_ueg)
    did_manager = MagicMock()
    did_manager.verify_signed_intent.return_value = True
    vault.did_manager = did_manager

    evt = await vault.deposit(Decimal("1000"), "USDC", {}, {"context": "test"})
    assert evt == "evt_123"
    mock_ueg.log_event.assert_called()

@pytest.mark.asyncio
async def test_mesh_discovery(mock_validator):
    mesh = AutonomousMesh(mock_validator)
    peers = await mesh.discover_peers()
    assert len(peers) > 0

    treaty = await mesh.negotiate_treaty(peers[0], {"liquidity_cap": 10.0})
    assert treaty.status == "SIGNED"
    assert treaty.node_b == peers[0]["id"]

@pytest.mark.asyncio
async def test_dao_bridge(mock_ueg):
    safe_automator = MagicMock()
    bridge = DAOExecutiveBridge(MagicMock(), safe_automator)
    bridge.ueg = mock_ueg

    tx_hash = await bridge.execute_proposal("prop_456", {"reason": "rebalance"})
    assert tx_hash.startswith("0x_executed")
    mock_ueg.log_event.assert_called()

@pytest.mark.asyncio
async def test_self_evolving_constitution(mock_ueg):
    tlc = TLCRuntimeChecker()
    mjm = MagicMock()
    mjm.generate_amendment = AsyncMock(return_value={"id": "amend_789", "tla_spec": "MODULE Amendment..."})

    engine = SelfEvolvingConstitution(tlc, mjm)
    engine.ueg = mock_ueg

    success = await engine.monitor_and_propose(0.80, {})
    assert success is True
    mock_ueg.log_event.assert_called()

@pytest.mark.asyncio
async def test_subfund_genome(mock_ueg):
    manager = SubFundGenomeManager()
    manager.ueg = mock_ueg

    genome_hash = await manager.create_genome({"risk": "low", "target": "8%"})
    assert len(genome_hash) == 128 # sha3-512
    mock_ueg.log_event.assert_called()

@pytest.mark.asyncio
async def test_legal_entity_registration(mock_ueg):
    entity = AICEOLegalEntity(mock_ueg)
    # Mock config file for factory
    import os
    if not os.path.exists("config/sovereign_config.yaml"):
        os.makedirs("config", exist_ok=True)
        with open("config/sovereign_config.yaml", "w") as f:
            f.write("phase8: {}\n")

    receipt = await entity.register_as_legal_entity("Wyoming", "wyoming_dao", {})
    assert receipt.status == "BUNDLED_FOR_FILING"
    assert receipt.bundle.jurisdiction == "Wyoming"
    mock_ueg.log_event.assert_called()
