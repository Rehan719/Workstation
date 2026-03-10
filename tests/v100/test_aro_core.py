import asyncio
import pytest
import json
import yaml
from agentic_core.optimizer.engine import AdaptiveResourceOptimizer

@pytest.fixture
def aro():
    return AdaptiveResourceOptimizer()

@pytest.mark.asyncio
async def test_aro_ral_processing_json(aro):
    ral_spec = json.dumps({
        "id": "req_123",
        "domain": "science",
        "requirements": {
            "8 CPU cores": 4,
            "16GB RAM": 32,
            "api_quotas": 100
        }
    })

    result = await aro.process_ral_request("user_001", "pro", ral_spec)

    assert result["status"] == "SUCCESS"
    assert "pool_id" in result
    assert result["verification"]["translated_requirements"]["compute"] == 4

    # Verify inventory reduction
    inventory = aro.fabric.get_inventory_status()
    assert inventory["compute"]["available"] == 96

@pytest.mark.asyncio
async def test_aro_ral_processing_yaml(aro):
    ral_spec = """
    id: req_456
    domain: law
    requirements:
      compute: 2
      gpu: 1
    """

    result = await aro.process_ral_request("user_002", "enterprise", ral_spec)

    assert result["status"] == "SUCCESS"
    assert result["pool_id"] is not None

    inventory = aro.fabric.get_inventory_status()
    assert inventory["gpu"]["available"] == 7

@pytest.mark.asyncio
async def test_scheduler_circuit_breaker(aro):
    # Simulate low API quota in monitor
    aro.monitor.history.append({"api_quota_remaining": 0.05})
    # The monitor.get_current_usage currently returns static 0.85 in one place and history in another.
    # Let's check scheduler.py: it uses monitor.get_current_usage()

    # Override monitor behavior for test
    aro.monitor.get_current_usage = lambda: {"api_quota_remaining": 0.05}

    ral_spec = json.dumps({
        "id": "req_fail",
        "domain": "general",
        "requirements": {"compute": 1}
    })

    # First call should trigger circuit breaker
    result = await aro.process_ral_request("user_003", "free", ral_spec)
    assert result["status"] == "QUEUED" # It triggers 80% threshold -> returns QUEUED

    # Second call should be REJECTED because circuit is now open
    result2 = await aro.process_ral_request("user_004", "free", ral_spec)
    assert result2["status"] == "REJECTED"
    assert result2["reason"] == "CIRCUIT_BREAKER_ACTIVE"
