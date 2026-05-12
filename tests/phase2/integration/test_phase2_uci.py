import pytest
import asyncio
from core.transcendent_subsystems.csl import CausalSovereigntyLayer, CausalGraph
from core.transcendent_subsystems.tfel import ThermodynamicFreeEnergyLedger
from core.governance.nemoclaw_engine import NemoclawEngine
from core.governance.unified_constitutional_interceptor_supreme import UnifiedConstitutionalInterceptorSupreme

@pytest.mark.asyncio
async def test_phase2_supreme_uci():
    # 1. Setup
    ueg = None
    uci = UnifiedConstitutionalInterceptorSupreme("TEST_NODE", ueg)

    # 2. Register a Causal Graph for tests
    graph_data = CausalGraph(
        nodes=["withdrawal", "fund_stability", "market_context"],
        edges=[("withdrawal", "fund_stability"), ("market_context", "fund_stability")],
        confounders={}
    )
    uci.csl.register_graph("capital", graph_data)

    # 3. Action closure
    async def mock_action():
        return "SUCCESSFUL_EXECUTION"

    # 4. Context for consequential action
    context = {
        "intent": "rebalance_portfolio",
        "domain": "capital",
        "is_consequential": True,
        "treatment": "withdrawal",
        "outcome": "fund_stability",
        "observed_vars": ["market_context"],
        "bit_complexity": 5000
    }

    # 5. Intercept
    result = await uci.intercept(context, mock_action)

    # 6. Assertions
    assert result["status"] == "success"
    assert "csl_proof" in context
    assert "tfel_receipt" in context
    assert "legal_coverage" in context
    assert context["legal_coverage"] == 1.0

    print(f"\n✅ Phase 2 Supreme UCI Interception Verified. Legal Coverage: {context['legal_coverage']}")
