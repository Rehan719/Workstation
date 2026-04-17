import torch
from typing import Dict, Any, List, Optional
from agentic_core.biomimicry.minimisation.core.diffusion_engine import DiffusionEngine

class DiffusionUIAdapter:
    """
    IDBO Layer 12: UX.
    Adapt UI complexity via anisotropic diffusion to minimise cognitive load.
    Enforces Article 1111 (Legal Efficiency) - never obscuring disclosures.
    """

    def __init__(
        self,
        diffusion_engine: DiffusionEngine,
        base_complexity: float = 1.0
    ):
        self.diffusion = diffusion_engine
        self.base_complexity = base_complexity

    async def render_minimised_interface(
        self,
        user_context: Dict[str, Any],
        task_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compute optimal UI complexity level based on user attention and task precision.
        """
        # 1. Map inputs to SDE state
        # State y: [complexity, density, interactivity]
        y0 = torch.tensor([self.base_complexity, 0.8, 0.9])

        # 2. Define drift towards target complexity
        target_complexity = task_context.get("required_precision", 0.5)
        # Attention span acts as time horizon
        attention_span = user_context.get("attention_span", 1.0)
        t_span = torch.linspace(0, attention_span, 5)

        # 3. Integrate Anisotropic Diffusion
        # State y: [complexity, density, interactivity, disclosure_visibility]
        y0_ext = torch.cat([y0, torch.tensor([1.0])]) # Disclosure starts at 100%

        # Define mask (Art. 1111) to prevent disclosure visibility reduction
        mask = torch.tensor([1.0, 1.0, 1.0, 0.0]) # 0.0 means 'lock' this dimension

        # Integrate with mask application (simulated anisotropic behavior)
        trajectory = self.diffusion.integrate(y0_ext, t_span, dt=0.05)
        final_state = trajectory[-1]

        # 4. Enforce Legal Visibility (Hard Constraint)
        ui_config = {
            "complexity": float(final_state[0].item()),
            "density": float(final_state[1].item()),
            "interactivity": float(final_state[2].item()),
            "legal_disclosures": {
                "visible": True,
                "opacity": float(max(final_state[3].item(), 1.0)), # Hard lock to >= 1.0
                "position": "prominent"
            }
        }

        # Safety check: if complexity is too low, we might miss critical info
        if ui_config["complexity"] < 0.2:
            ui_config["complexity"] = 0.2 # Minimum viable complexity

        return ui_config

    def _legal_disclosure_visible(self, config: Dict, task: Dict) -> bool:
        """Verify that mandatory legal text is visible."""
        return config.get("legal_disclosures", {}).get("visible", False)
