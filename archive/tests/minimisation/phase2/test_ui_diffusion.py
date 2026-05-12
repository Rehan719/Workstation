import pytest
import torch
from agentic_core.ux.adapters.diffusion_ui_adapter import DiffusionUIAdapter
from agentic_core.biomimicry.minimisation.core.diffusion_engine import DiffusionEngine

@pytest.mark.asyncio
async def test_ui_diffusion_mask_enforcement():
    # Setup diffusion that tries to zero out everything
    drift = lambda t, y: -100.0 * y
    diffusion = lambda t, y: torch.zeros_like(y)
    engine = DiffusionEngine(drift, diffusion)

    adapter = DiffusionUIAdapter(engine, base_complexity=1.0)

    # Task context requiring low precision
    task = {"required_precision": 0.1}
    user = {"attention_span": 1.0}

    ui_config = await adapter.render_minimised_interface(user, task)

    # Transparency of disclosures must be exactly 1.0 (Art. 1111)
    assert ui_config["legal_disclosures"]["opacity"] == 1.0
    assert ui_config["legal_disclosures"]["visible"] == True

    # Complexity should be reduced but not below 0.2
    assert ui_config["complexity"] >= 0.2
