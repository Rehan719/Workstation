import pytest
from agentic_core.recirculation.fractal_loop import FractalRecirculationEngine
@pytest.mark.asyncio
async def test_loop():
    engine = FractalRecirculationEngine()
    res = await engine.run_cycle({"user_id": "test", "tier": "advanced", "action": "test"})
    assert res["status"] == "SUCCESS"
