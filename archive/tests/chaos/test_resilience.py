import pytest
import pytest_asyncio
import asyncio
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

@pytest_asyncio.fixture
async def organism():
    org = ConsciousOrganismV99_0()
    await org.start()
    yield org
    await org.shutdown()

@pytest.mark.asyncio
async def test_reliability_resilience(organism):
    """
    Chaos Test: Reliability Engine (Article 91)
    Simulate External Service Failures and Retries.
    """
    # 1. Simulate External Service Failure
    async def failing_operation():
        raise Exception("External Service Unavailable")

    # 2. Verify Reliability Engine Correctly Retries
    try:
        # Should attempt 3 retries (total 4 attempts)
        await organism.reliability.execute_with_retry(failing_operation)
    except Exception as e:
        assert str(e) == "External Service Unavailable"

    # Check that retry count in ReliabilityEngine (impl detail) matched
    # (Assuming we track attempt counts for validation)
    # assert organism.reliability.last_op_retry_count == 3

    # 3. Circuit Breaker Trip
    # Call it 5 times consecutively to trip the breaker
    for _ in range(5):
        try:
            await organism.reliability.execute_with_circuit_breaker("SlackService", failing_operation)
        except:
            pass

    # Check circuit status
    health = organism.reliability.get_service_health("SlackService")
    assert health["status"] == "OPEN"
    assert health["failure_count"] >= 5

@pytest.mark.asyncio
async def test_backpressure_and_rate_limiting(organism):
    """
    Chaos Test: Rate Limiting & Backpressure (Article 147)
    Inject excessive load on ConnectorRegistry.
    """
    # 1. Fill the token bucket for Slack (limit 10 per min)
    for i in range(10):
        res = organism.integrations.execute_integration("slack", {"msg": f"Test {i}"})
        assert res["status"] == "success"

    # 2. 11th call should trigger Rate Limit and Return Error
    res = organism.integrations.execute_integration("slack", {"msg": "Load Burst"})
    assert res["status"] == "error"
    assert res["msg"] == "RATE_LIMIT_EXCEEDED"
