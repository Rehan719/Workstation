import pytest
import torch
import numpy as np
from agentic_core.orchestration.adapters.ot_router import LegalAwareOptimalTaskRouter
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
from agentic_core.legal.types import TribunalTask, LegalAgent
from agentic_core.ueg.logger import VSBUEGLogger
import os

@pytest.fixture
def ot_router():
    ot_core = OptimalTransportRouter(epsilon=0.01)
    legal_engine = UKLegalPrecisionEngineImpl("configs/legal_precision.yaml")
    ueg_logger = VSBUEGLogger("data/test_ueg.log")
    return LegalAwareOptimalTaskRouter(ot_core, legal_engine, ueg_logger)

@pytest.mark.asyncio
async def test_ot_tribunal_assignment_legal_coverage(ot_router):
    # Tasks with specific requirements
    tasks = [
        TribunalTask(id="T1", statute="EqualityAct2010", claim_type="discrimination", priority=0.8, jurisdiction="England_Wales"),
        TribunalTask(id="T2", statute="ERA1996", claim_type="unfair_dismissal", priority=0.9, jurisdiction="Scotland")
    ]

    # Agents with matching and non-matching competencies
    agents = [
        LegalAgent(id="A1", competencies=["EqualityAct2010"], available_capacity=1.0, jurisdiction="England_Wales", experience_level=0.8),
        LegalAgent(id="A2", competencies=["ERA1996"], available_capacity=1.0, jurisdiction="Scotland", experience_level=0.9),
        LegalAgent(id="A3", competencies=["Generic"], available_capacity=1.0, jurisdiction="England_Wales", experience_level=0.5)
    ]

    assignment = await ot_router.assign_tribunal_tasks(tasks, agents)

    # Assert 100% legal coverage
    assert assignment["T1"] == "A1" # Only A1 can do T1
    assert assignment["T2"] == "A2" # Only A2 can do T2
    assert "T3" not in assignment # No tasks should be unassigned if possible

def test_ot_router_build_default_cost_matrix(ot_router):
    tasks = [TribunalTask(id="T1", statute="EA", claim_type="disc", priority=0.8)]
    agents = [LegalAgent(id="A1", competencies=["EA"], available_capacity=1.0, jurisdiction="UK", experience_level=0.5)]
    C = ot_router._build_default_cost_matrix(tasks, agents)
    assert C.shape == (1, 1)
    assert C[0, 0] == pytest.approx(0.3)

@pytest.mark.asyncio
async def test_ot_router_empty(ot_router):
    assert await ot_router.assign_tribunal_tasks([], []) == {}

@pytest.mark.asyncio
async def test_ot_router_no_valid_agents(ot_router):
    tasks = [TribunalTask(id="T1", statute="EA", claim_type="disc", priority=0.8, jurisdiction="Scotland")]
    agents = [LegalAgent(id="A1", competencies=["Other"], available_capacity=1.0, jurisdiction="England_Wales")]
    # Should skip T1 as no agent qualified
    res = await ot_router.assign_tribunal_tasks(tasks, agents)
    assert res == {}
