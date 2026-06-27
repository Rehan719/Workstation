import pytest
import asyncio
from agentic_core.architecture.enriched_layers import EnrichedArchitecturalLayerManager
from agentic_core.ueg.logger import VSBUEGLogger

from unittest.mock import MagicMock, AsyncMock
from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType

@pytest.mark.asyncio
async def test_14_layer_mapping():
    ueg = VSBUEGLogger()

    # Mock and register engines
    mock_engine = MagicMock()
    mock_engine.process = AsyncMock(return_value=MagicMock(confidence=0.95, constitutional_trace=[]))
    for et in [EngineType.INKASHAF, EngineType.AQAL, EngineType.SAMAJH]:
        CognitiveEngineRegistry.register(et, mock_engine)

    manager = EnrichedArchitecturalLayerManager(ueg)

    # Verify all 14 layers are present
    assert len(manager.layers_14) == 14

    # Test L0 (Legacy Shim)
    res_l0 = await manager.execute_sovereign(0, {"data": "test_data"})
    assert res_l0["status"] == "SUCCESS"
    assert res_l0["result"] is True

    # Test L9 (Mushawara Integration)
    res_l9 = await manager.execute_sovereign(9, {"task": "test_task"})
    assert res_l9["status"] == "SUCCESS"
    assert "consensus" in res_l9

    # Test L13 (Reflection Integration)
    res_l13 = await manager.execute_sovereign(13, {"data": "audit_logs"})
    assert res_l13["status"] == "SUCCESS"
    assert res_l13["drift"] == 0.003

    # Test Generic Adapter (L7)
    res_l7 = await manager.execute_sovereign(7, {"id": "req_123"})
    assert res_l7["status"] == "SUCCESS"
    assert res_l7["layer"] == 7

@pytest.mark.asyncio
async def test_legacy_backward_compatibility():
    ueg = VSBUEGLogger()
    manager = EnrichedArchitecturalLayerManager(ueg)

    # Test direct legacy calls
    res = await manager.mycelial_propagation("data")
    assert res is True

    tasks = await manager.ant_colony_orchestration([{"id": 1, "relevance": 0.5}])
    assert len(tasks) == 1
