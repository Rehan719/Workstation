import pytest
import torch
from agentic_core.orchestration.adapters.legal_aware_ot_router import LegalAwareOptimalTaskRouter
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
from agentic_core.legal.types import TribunalTask, LegalAgent
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_legal_hard_constraint_enforcement():
    ot_core = OptimalTransportRouter(epsilon=0.01)
    legal_engine = UKLegalPrecisionEngineImpl("configs/legal_precision.yaml")
    ueg_logger = VSBUEGLogger("data/test_ueg_hard.log")
    router = LegalAwareOptimalTaskRouter(ot_core, legal_engine, ueg_logger)

    # Task requires EqualityAct2010
    tasks = [TribunalTask(id="T_SENSITIVE", statute="EqualityAct2010", claim_type="discrimination", priority=1.0, jurisdiction="UK")]

    # Agent NOT qualified
    agents = [LegalAgent(id="A_UNQUALIFIED", competencies=["General"], available_capacity=1.0, jurisdiction="UK")]

    assignment = await router.assign_tribunal_tasks(tasks, agents)

    # Assignment should be empty because no qualified agent exists (Hard Constraint)
    assert "T_SENSITIVE" not in assignment
    assert len(assignment) == 0

@pytest.mark.asyncio
async def test_jurisdiction_hard_constraint():
    ot_core = OptimalTransportRouter(epsilon=0.01)
    legal_engine = UKLegalPrecisionEngineImpl("configs/legal_precision.yaml")
    ueg_logger = VSBUEGLogger("data/test_ueg_jur.log")
    router = LegalAwareOptimalTaskRouter(ot_core, legal_engine, ueg_logger)

    tasks = [TribunalTask(id="T1", statute="ERA1996", claim_type="unfair_dismissal", priority=1.0, jurisdiction="Scotland")]

    # Qualified but wrong jurisdiction
    agents = [LegalAgent(id="A1", competencies=["ERA1996"], available_capacity=1.0, jurisdiction="England_Wales")]

    assignment = await router.assign_tribunal_tasks(tasks, agents)
    assert "T1" not in assignment
