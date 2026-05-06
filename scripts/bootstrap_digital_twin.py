import sys
import unittest.mock
from unittest.mock import MagicMock

# 1. Setup Mock Torch correctly for SciPy compatibility
class MockTorchTensor:
    pass

mock_torch = MagicMock()
mock_torch.Tensor = MockTorchTensor
sys.modules['torch'] = mock_torch

# Other mocks
sys.modules['shap'] = MagicMock()
sys.modules['qiskit'] = MagicMock()
sys.modules['web3'] = MagicMock()
sys.modules['ot'] = MagicMock()

import asyncio
import logging
from agentic_core.simulations.digital_twin_controller import DigitalTwinController
from agentic_core.biomimicry.geospheric.digital_twin_orchestrator import DigitalTwinOrchestrator
from agentic_core.mjm.self_reflection_engine import SelfReflectionEngine
from agentic_core.mjm.recursive_meta_learner import MJMRecursiveLearner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting Digital Twin Bootstrap Validation...")

    # Setup Dependencies
    mock_ueg = unittest.mock.AsyncMock()
    mock_ueg.log_event = unittest.mock.AsyncMock()
    mock_ueg.get_last_entries = unittest.mock.AsyncMock(return_value=[])

    validator = MagicMock()
    validator.validate_thermal_operation = unittest.mock.AsyncMock()

    # Instantiate Orchestrator and Engines
    mock_inner_mjm = MagicMock()
    mock_inner_mjm.jaiza = unittest.mock.AsyncMock(return_value={})
    mjm_model = MJMRecursiveLearner(orchestrator=mock_inner_mjm, learner=MagicMock())
    orchestrator = DigitalTwinOrchestrator(
        validator=validator,
        mjm_model=mjm_model,
        ueg=mock_ueg
    )

    reflection_engine = SelfReflectionEngine(
        validator=validator,
        biomimetic_validator=MagicMock()
    )

    # Initialize Controller
    c = DigitalTwinController(
        orchestrator=orchestrator,
        reflection_engine=reflection_engine
    )

    # Execute Twin Step
    result = await c.step()

    # Output Results
    import json
    def serializer(obj):
        if isinstance(obj, (set, MagicMock, unittest.mock.AsyncMock)):
            return str(obj)
        return str(obj)

    print(json.dumps(result, indent=2, default=serializer))
    logger.info("Digital Twin Bootstrap Completed Successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bootstrap Failed: {e}", exc_info=True)
        sys.exit(1)
