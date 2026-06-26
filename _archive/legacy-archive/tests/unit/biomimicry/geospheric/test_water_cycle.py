import pytest
import sys
from unittest.mock import MagicMock

# Mock problematic dependencies
sys.modules['shap'] = MagicMock()
sys.modules['qiskit'] = MagicMock()
sys.modules['pennylane'] = MagicMock()
sys.modules['camel_tools'] = MagicMock()
sys.modules['oqs'] = MagicMock()
sys.modules['web3'] = MagicMock()
sys.modules['firebase_admin'] = MagicMock()

from agentic_core.biomimicry.cycles.water_cycle import HydrologicResourceManager

@pytest.mark.asyncio
async def test_water_cycle_evaporation():
    manager = HydrologicResourceManager()
    heat_load = 100.0
    temp = 350.15
    recovered = await manager.evaporate(heat_load, temp)

    assert recovered > 0
    assert manager.reservoirs["atmosphere"] > 0.001
    assert manager.reservoirs["ocean"] < 1.0

def test_water_cycle_homeostasis():
    manager = HydrologicResourceManager(target_temp=350.0)
    score = manager.get_homeostasis_score(350.0)
    assert score == 1.0

    score_low = manager.get_homeostasis_score(300.0)
    assert score_low < 1.0
