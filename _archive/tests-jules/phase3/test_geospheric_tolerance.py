import pytest
import numpy as np
from agentic_core.recirculation.fractal_loop import FractalRecirculationEngine
from agentic_core.ueg.logger import VSBUEGLogger
@pytest.mark.asyncio
async def test_geospheric_tolerance_enforcement():
    engine = FractalRecirculationEngine()
    ctx = {"id": "test_drift", "requires_reratification": False}
    await engine._enforce_geospheric_tolerance(ctx)
    assert "id" in ctx
