import pytest
import asyncio
from decimal import Decimal
from unittest.mock import patch, AsyncMock, MagicMock
from products.capital_fund.adapters.external_market import ExternalMarketAdapter
from products.capital_fund.adapters.crypto_gateway import CryptoGateway
from products.capital_fund.orchestration.semi_autonomous import SemiAutonomousExecutor
from agentic_core.constitutional.evolution_manager import ConstitutionalEvolutionManager
from agentic_core.statistics.live_rigor_monitor import LiveRigorMonitor

@pytest.mark.asyncio
async def test_phase3_global_civilisation_lifecycle():
    """
    End-to-end integration test for Phase 3: Global Investment Civilisation.
    """
    uid = "sovereign_123"

    with patch("products.capital_fund.core.vault.GaaSValidator") as mock_gaas, \
         patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg, \
         patch("products.capital_fund.core.vault.db") as mock_db, \
         patch("agentic_core.mjm.hd_omni_learner.MJMv4OmniLearner"), \
         patch("agentic_core.consultation.mushawara.consultation_orchestrator.ConsultationOrchestrator"):

        # Setup mocks
        mock_gaas.return_value.validate_action = AsyncMock(return_value={"passed": True, "hash": "phase3"})
        mock_ueg.return_value.log_event = AsyncMock(return_value="event_p3")
        mock_db.run_transaction.return_value = 10000.0

        # 1. Initialize Global Components
        market_adapter = ExternalMarketAdapter(mock_gaas.return_value, mock_ueg.return_value)
        market_adapter.external_markets_enabled = True

        crypto_gateway = CryptoGateway(uid, mock_gaas.return_value, mock_ueg.return_value)
        # Override vault ueg in gateway
        crypto_gateway.vault.ueg = mock_ueg.return_value
        crypto_gateway.vault.audit.ueg_logger = mock_ueg.return_value

        rigor_monitor = LiveRigorMonitor(mock_ueg.return_value)

        # 2. Execute External Trade (GLOBAL MARKETS)
        trade = await market_adapter.execute_trade(uid, "BTC", "BUY", Decimal("0.5"), "key_p3")
        assert trade["status"] == "EXECUTED"
        assert trade["total_value"] == 32500.0 # 0.5 * 65000

        # 3. Verify Crypto Deposit (ON-CHAIN)
        deposit = await crypto_gateway.verify_onchain_deposit("0x123", "ETH", Decimal("1.5"))
        assert deposit["status"] == "COMPLETED"

        # 4. Statistical Validation (RIGOR)
        stats_res = await rigor_monitor.validate_metric("ROI", 0.12, 0.08)
        assert "ci_95" in stats_res

        # 5. Constitutional Evolution (ADAPTATION)
        evo_manager = ConstitutionalEvolutionManager(mock_ueg.return_value, mock_gaas.return_value, AsyncMock())
        amend_id = await evo_manager.propose_amendment("1130", "Limit -> 25%", "Better diversification", uid)
        assert amend_id.startswith("amend_1130")

        # Verify integration via UEG calls
        assert mock_ueg.return_value.log_event.called
