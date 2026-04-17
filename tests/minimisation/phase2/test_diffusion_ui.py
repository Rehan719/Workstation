import pytest
import torch
from agentic_core.ux.adapters.diffusion_ui_adapter import DiffusionUIAdapter
from agentic_core.biomimicry.minimisation.core.diffusion_engine import DiffusionEngine

@pytest.mark.asyncio
async def test_diffusion_ui_complexity_adaptation():
    # Linear drift towards target
    drift = lambda t, y: 0.5 * (torch.tensor([0.5, 0.5, 0.5]) - y)
    diffusion = lambda t, y: torch.ones_like(y) * 0.01

    engine = DiffusionEngine(drift, diffusion)
    adapter = DiffusionUIAdapter(engine, base_complexity=1.0)

    user_context = {"attention_span": 0.5}
    task_context = {"required_precision": 0.2}

    ui_config = await adapter.render_minimised_interface(user_context, task_context)

    assert "complexity" in ui_config
    assert ui_config["legal_disclosures"]["visible"] == True
    assert ui_config["legal_disclosures"]["opacity"] == 1.0

    # Should be less than base complexity
    assert ui_config["complexity"] < 1.0
    assert ui_config["complexity"] >= 0.2 # Min limit

@pytest.mark.asyncio
async def test_diffusion_ui_min_limit():
    drift = lambda t, y: -10.0 * torch.ones_like(y)
    diffusion = lambda t, y: torch.zeros_like(y)
    engine = DiffusionEngine(drift, diffusion)
    adapter = DiffusionUIAdapter(engine, base_complexity=1.0)

    # Force complexity very low
    ui_config = await adapter.render_minimised_interface({"attention_span": 1.0}, {"required_precision": 0.0})
    assert ui_config["complexity"] == 0.2
    assert adapter._legal_disclosure_visible(ui_config, {})
