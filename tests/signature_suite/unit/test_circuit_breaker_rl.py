import pytest
import asyncio
from agentic_core.gaas.v5.circuit_breaker_rl import SelfTuningCircuitBreaker

@pytest.mark.asyncio
async def test_circuit_breaker_tuning():
    cb = SelfTuningCircuitBreaker()
    # Simulate errors to trip
    for _ in range(5):
        tripped = await cb.check_health(False)
    assert tripped is True

    # Simulate many successes to relax threshold
    for _ in range(20):
        await cb.check_health(True)
    assert cb.error_threshold > 5
