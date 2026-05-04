import sys
import unittest.mock

# Create a class for torch.Tensor
class MockTensor:
    """Mock Tensor class for environments without torch."""
    def __repr__(self):
        return "MockTensor"

mock_torch = unittest.mock.MagicMock()
mock_torch.Tensor = MockTensor
sys.modules['torch'] = mock_torch

sys.modules['shap'] = unittest.mock.MagicMock()
sys.modules['qiskit'] = unittest.mock.MagicMock()
sys.modules['web3'] = unittest.mock.MagicMock()
sys.modules['ot'] = unittest.mock.MagicMock()

import logging
from agentic_core.simulations.digital_twin_controller import DigitalTwinController
import asyncio

logging.basicConfig(level=logging.INFO)

async def main():
    c = DigitalTwinController()
    result = await c.step()
    import json
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
