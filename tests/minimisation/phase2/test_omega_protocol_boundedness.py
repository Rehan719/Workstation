import pytest
import torch
from agentic_core.minimisation.recirculation.omega_protocol import OmegaProtocol
from agentic_core.minimisation.pipeline import MinimisationPipeline
from agentic_core.ueg.logger import VSBUEGLogger
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_omega_protocol_boundedness_hold():
    # Setup mocks
    pipeline = MagicMock(spec=MinimisationPipeline)
    ueg = VSBUEGLogger("data/test_boundedness.log")

    # Protocol with 15% threshold
    protocol = OmegaProtocol(pipeline, ueg, entropy_threshold=0.15)

    # State with low entropy reduction (e.g., 5%)
    system_state = {"reduction_pct": 0.05, "total_entropy": 0.5}

    res = await protocol.execute_macro_cycle(system_state)

    # Should trigger 888_HOLD
    assert "888_HOLD" in res.macro_cycle_id
    assert res.entropy_reduction == 0.05

@pytest.mark.asyncio
async def test_omega_protocol_execution_flow():
    pipeline = MagicMock(spec=MinimisationPipeline)
    ueg = VSBUEGLogger("data/test_flow.log")
    protocol = OmegaProtocol(pipeline, ueg, entropy_threshold=0.10)

    # High reduction (20%)
    system_state = {"reduction_pct": 0.20, "total_entropy": 0.3}

    res = await protocol.execute_macro_cycle(system_state)

    assert "888_HOLD" not in res.macro_cycle_id
    assert res.entropy_reduction == 0.20
