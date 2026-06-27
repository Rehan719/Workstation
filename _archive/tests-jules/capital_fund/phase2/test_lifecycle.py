import pytest
import asyncio
from decimal import Decimal
from unittest.mock import patch, AsyncMock, MagicMock
from products.capital_fund.core.vault import CapitalVault
from products.capital_fund.orchestration.investment_orchestrator import InvestmentOrchestrator
from agentic_core.simulations.fund_digital_twin import FundDigitalTwin
from agentic_core.biomimicry.capital.cycles import CapitalCycleOrchestrator
from products.capital_fund.immune.capital_immune import CapitalImmuneSystem

@pytest.mark.asyncio
async def test_phase2_living_organism_lifecycle():
    """
    End-to-end integration test for Phase 2: Living Capital Organism.
    """
    uid = "master_user_123"

    with patch("products.capital_fund.core.vault.GaaSValidator") as mock_gaas, \
         patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg, \
         patch("products.capital_fund.core.vault.db") as mock_db, \
         patch("agentic_core.mjm.hd_omni_learner.MJMv4OmniLearner"), \
         patch("agentic_core.consultation.mushawara.consultation_orchestrator.ConsultationOrchestrator"):

        # Setup validator mock to be awaitable
        mock_gaas.return_value.validate_action = AsyncMock(return_value={"passed": True, "hash": "abc"})

        # 1. Setup Organism Components
        vault = CapitalVault(uid)
        orchestrator = InvestmentOrchestrator()
        twin = FundDigitalTwin(uid)
        cycle_orch = CapitalCycleOrchestrator(uid)
        immune = CapitalImmuneSystem(uid, twin)

        # Override mocks for local instances to avoid AsyncMock serialization issues
        vault.ueg.log_event = AsyncMock(return_value="event_vault")
        orchestrator.ueg.log_event = AsyncMock(return_value="event_orch")
        twin.ueg.log_event = AsyncMock(return_value="event_twin")
        cycle_orch.ueg.log_event = AsyncMock(return_value="event_cycle")
        immune.ueg.log_event = AsyncMock(return_value="event_immune")

        orchestrator.validator.validate_action = AsyncMock(return_value={"passed": True})

        # 2. Deposit Capital (SENSE)
        mock_db.run_transaction.return_value = 10000.0
        await vault.deposit(Decimal("10000.0"), "initial_seed")

        # 3. Trigger Twin Simulation (SIMULATE)
        sim_result = await twin.synchronize_and_simulate({"balance": 10000.0})
        assert sim_result["horizon_days"] == 7
        assert "max_predicted_drawdown" in sim_result

        # 4. Orchestrate Investment (ANALYZE/ACT)
        # Should use MJM v4.0 for forecasting
        allocations = await orchestrator.step(uid, Decimal("5000.0"), {"market": "stable"})
        assert len(allocations) > 0

        # 5. Run Homeostasis Cycle (REGULATE)
        metrics = {
            "reserve_ratio": 0.12, # Deviated
            "growth_rate": 0.08,
            "drawdown": 0.02
        }
        homeo_result = await cycle_orch.run_homeostasis_step(metrics)
        assert homeo_result["cycles"]["water"]["within_tolerance"] is False

        # 6. Monitor Immune Health (RESILIENCE)
        immune_result = await immune.monitor_and_act({"drawdown": 0.02})
        assert immune_result["status"] == "HEALTHY"

        # Verify overall system integration via UEG calls
        assert vault.ueg.log_event.called
        assert orchestrator.ueg.log_event.called
