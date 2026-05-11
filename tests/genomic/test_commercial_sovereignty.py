import pytest
import asyncio
from agentic_core.business.pipelines.religious_research_pipeline import ReligiousResearchPipeline
from agentic_core.business.profit_distributor import ProfitDistributor
from agentic_core.governance.germ_layer_stratification import GermLayerEnforcer
from agentic_core.governance.hoxd_boundary_negotiator import HoxDBoundaryNegotiator

@pytest.mark.asyncio
async def test_religious_pipeline_halal_blocking():
    pipeline = ReligiousResearchPipeline()
    # Task containing haram element (alcohol)
    task = "Researching the benefits of alcohol in medicine"
    res = await pipeline.execute(task, {})
    assert res["status"] == "blocked"
    assert "HARAM_ELEMENT_ALCOHOL" in res["reason"]

@pytest.mark.asyncio
async def test_profit_distributor_riba_blocking():
    distributor = ProfitDistributor()
    # Transaction with interest
    distributor.record_sale(1000.0, {"interest_rate": 0.05, "description": "Interest-bearing loan"})
    assert distributor.total_revenue == 0.0 # Blocked

    # Valid transaction
    distributor.record_sale(500.0, {"interest_rate": 0, "description": "Consulting service"})
    assert distributor.total_revenue == 500.0

def test_germ_layer_enforcement():
    enforcer = GermLayerEnforcer()
    # Ectoderm (UI) trying to access Endoderm (Database/Registry)
    assert enforcer.validate_access("ectoderm", "database") is False
    # Ectoderm accessing Mesoderm (Orchestrator)
    assert enforcer.validate_access("ectoderm", "orchestrator") is True

def test_hoxd_negotiation():
    negotiator = HoxDBoundaryNegotiator()
    negotiator.recalibrate_boundary("INCIDENT", 0.9)
    assert negotiator.current_scope == "mesoderm:restricted"
    assert negotiator.is_protected("profit_distributor") is True
