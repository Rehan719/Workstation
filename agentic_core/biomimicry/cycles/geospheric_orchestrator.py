import os
import yaml
import numpy as np
from typing import Dict, Any, Optional
from .water_cycle import HydrologicResourceManager
from .carbon_cycle import CarbonDataMetabolism
from .nitrogen_cycle import NitrogenTaskMediator
from .oxygen_cycle import MetabolicScheduler
from .phosphorus_cycle import PhosphorusMemoryHierarchy
from .sulfur_cycle import SulfurErrorResilience
from .psi_functional import EcosystemHealthObjective
from agentic_core.crypto.entropy_pool import EntropyPool

class GeosphericHomeostaticOrchestrator:
    def __init__(self, target_psi: float = 0.90, entropy_pool: Optional[EntropyPool] = None):
        self.entropy_pool = entropy_pool or EntropyPool()
        self.water = HydrologicResourceManager(entropy_pool=self.entropy_pool)
        self.carbon = CarbonDataMetabolism()
        self.nitrogen = NitrogenTaskMediator()
        self.oxygen = MetabolicScheduler()
        self.phosphorus = PhosphorusMemoryHierarchy()
        self.sulfur = SulfurErrorResilience()
        self.psi_objective = EcosystemHealthObjective()
        self.target_psi = target_psi
        self.coupling_weights = self._load_coupling_config()

    def _load_coupling_config(self) -> Dict[str, float]:
        config_path = "config/geospheric/coupling_weights.yaml"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    data = yaml.safe_load(f)
                    return data.get("coupling", {})
            except Exception:
                return {}
        return {}

    def step(self, inputs: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        temp = inputs.get("current_temp", 348.15)
        w_out = self.water.evaporate(inputs.get("heat_load", 0.0), temp)
        c_out = self.carbon.photosynthesize(inputs.get("raw_data_size", 0.0))
        self.nitrogen.fix_input(inputs.get("input_count", 0))
        o_out = self.oxygen.respire(inputs.get("process_load", 0.0), inputs.get("metabolic_state", "active"))
        m_out = self.phosphorus.uptake(inputs.get("data_to_memory", 0.0))
        self.sulfur.emit_odor(inputs.get("error_severity", 0.0))

        rain = self.sulfur.trigger_acid_rain()
        if rain["mode"] == "acid_rain":
             throttle = self.coupling_weights.get("sulfur_to_oxygen", 0.15)
             self.oxygen.o2_level *= (1 - throttle)

        self.water.evaporate(o_out["heat_generated"], temp)

        cycle_scores = {
            "water": self.water.get_homeostasis_score(temp),
            "carbon": self.carbon.get_homeostasis_score(),
            "nitrogen": self.nitrogen.get_homeostasis_score(),
            "oxygen": self.oxygen.get_homeostasis_score(temp),
            "phosphorus": self.phosphorus.get_homeostasis_score(),
            "sulfur": self.sulfur.get_homeostasis_score()
        }

        psi = self.psi_objective.evaluate(
            cycle_scores, context.get("system_metrics", {}),
            context.get("legal_compliance", 1.0), context.get("closed_loop_waste", 0.0),
            context.get("biomimetic_fidelity", 1.0), context.get("genetic_integrity", 1.0)
        )

        stability_index = np.mean(list(cycle_scores.values())) - 1.0

        return {
            "psi_score": psi,
            "stability_index": float(stability_index),
            "status": "HOMEOSTATIC" if (psi >= self.target_psi and stability_index < 0) else "PERTURBED",
            "cycle_scores": cycle_scores
        }
