import sys
import os
import asyncio
import logging
import unittest.mock
from unittest.mock import MagicMock

# 1. Setup Mock Torch correctly for environments without it
class MockTorchTensor:
    pass

mock_torch = MagicMock()
mock_torch.Tensor = MockTorchTensor
sys.modules['torch'] = mock_torch

# Other mocks for heavyweight dependencies
sys.modules['shap'] = MagicMock()
sys.modules['qiskit'] = MagicMock()
sys.modules['web3'] = MagicMock()
sys.modules['ot'] = MagicMock()

# Ensure we can import from the root
sys.path.append(os.getcwd())

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
    mjm_model = MJMRecursiveLearner()

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

    # Execute Twin Step: SENSE -> SIMULATE -> REFLECT -> EVOLVE
    logger.info("Executing bootstrap step...")
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
        # Check for fix_genome_symlink before running
        if not os.path.exists("agentic_core/genome/chromosome.py"):
            print("ERROR: Genome path not found. Please run 'python scripts/fix_genome_symlink.py' first.")
            sys.exit(1)

        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bootstrap Failed: {e}", exc_info=True)
        sys.exit(1)
