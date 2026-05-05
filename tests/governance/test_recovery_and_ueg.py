import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from agentic_core.biomimicry.geospheric.digital_twin_orchestrator import DigitalTwinOrchestrator
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_twin_state_recovery():
    # Mock UEG with a valid snapshot
    mock_ueg = MagicMock(spec=VSBUEGLogger)
    snapshot_data = {
        "constitutional_compliance": 1.0,
        "water_cycle": {"temp_setpoint": 75.0, "reservoirs": {}, "integral": 0.0},
        "carbon_cycle": {"reservoirs": {}, "setpoint": 50.0},
        "subscription_state": {},
        "simulation_confidence": 0.9,
        "timestamp": "2026-01-01T00:00:00Z"
    }

    mock_ueg.get_last_entries.return_value = [
        {"payload": {"event_type": "TWIN_STATE_SNAPSHOT", "data": snapshot_data}}
    ]

    orchestrator = DigitalTwinOrchestrator(ueg=mock_ueg)
    recovered = await orchestrator.recover_state()

    assert recovered is not None
    assert recovered.water_cycle["temp_setpoint"] == 75.0
    assert recovered.timestamp == "2026-01-01T00:00:00Z"

@pytest.mark.asyncio
async def test_ueg_batching():
    log_path = "data/test_ueg_batch.log"
    if os.path.exists(log_path): os.remove(log_path)

    logger = VSBUEGLogger(log_path=log_path)
    logger.batch_interval = 0.1 # Fast flush for test

    await logger.log_event("TEST_EVENT", {"val": 1})

    # Should not be in file yet
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            assert f.read() == ""

    await asyncio.sleep(0.2)

    # Should be flushed now
    assert os.path.exists(log_path)
    with open(log_path, "r") as f:
        content = f.read()
        assert "TEST_EVENT" in content

import os
