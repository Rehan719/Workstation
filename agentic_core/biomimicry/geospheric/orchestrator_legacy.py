import os
import yaml
import numpy as np
from typing import Dict, Any, Optional
from agentic_core.biomimicry.cycles.water_cycle import WaterCycle as HydrologicResourceManager
from agentic_core.biomimicry.cycles.carbon_cycle import CarbonCycle as CarbonDataMetabolism
from agentic_core.biomimicry.cycles.nitrogen_cycle import NitrogenCycle as NitrogenTaskMediator
from agentic_core.biomimicry.cycles.oxygen_cycle import OxygenCycle as MetabolicScheduler
from agentic_core.biomimicry.cycles.phosphorus_cycle import PhosphorusCycle as PhosphorusMemoryHierarchy
from agentic_core.biomimicry.cycles.sulfur_cycle import SulfurCycle as SulfurErrorResilience
from agentic_core.biomimicry.cycles.psi_functional import EcosystemHealthObjective
from agentic_core.crypto.entropy_pool import EntropyPool
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.divine.v2.alignment_v2 import DivineAlignmentEngineV2

class GeosphericHomeostaticOrchestrator:
    def __init__(self, target_psi: float = 0.90, entropy_pool: Optional[EntropyPool] = None, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.entropy_pool = entropy_pool or EntropyPool()
        self.niyyah = DivineAlignmentEngineV2(self.ueg)

        self.water = HydrologicResourceManager(entropy_pool=self.entropy_pool, ueg_logger=self.ueg, niyyah_engine=self.niyyah)
        self.carbon = CarbonDataMetabolism(ueg_logger=self.ueg, niyyah_engine=self.niyyah)
        self.nitrogen = NitrogenTaskMediator(ueg_logger=self.ueg, niyyah_engine=self.niyyah)
        self.oxygen = MetabolicScheduler(ueg_logger=self.ueg, niyyah_engine=self.niyyah)
        self.phosphorus = PhosphorusMemoryHierarchy(ueg_logger=self.ueg, niyyah_engine=self.niyyah)
        self.sulfur = SulfurErrorResilience(ueg_logger=self.ueg, niyyah_engine=self.niyyah)

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
        return {
            "sulfur_to_oxygen": 0.15,
            "oxygen_to_water": 0.20,
            "carbon_to_nitrogen": 0.10
        }

    async def step(self, inputs: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        temp = inputs.get("current_temp", 348.15)

        # 1. Divine Alignment (Niyyah) check for the whole step
        divine_res = await self.niyyah.calibrate_niyyah(context.get("intent", "geospheric_homeostasis"))
        divine_score = divine_res["alignment_score"]

        # 2. Cycle Executions
        w_out = await self.water.evaporate(inputs.get("heat_load", 0.0), temp)
        c_out = await self.carbon.photosynthesize(inputs.get("raw_data_size", 0.0))
        await self.nitrogen.fix_nitrogen(inputs.get("input_count", 0))
        o_out = await self.oxygen.respire(inputs.get("process_load", 0.0), inputs.get("metabolic_state", "active"))
        m_out = await self.phosphorus.uptake(inputs.get("data_to_memory", 0.0))
        await self.sulfur.emit_odor(inputs.get("error_severity", 0.0))

        # 3. Apply coupling feedback
        rain = await self.sulfur.trigger_acid_rain(inputs.get("error_frequency", 0.0))
        if rain["mode"] == "acid_rain":
             throttle = self.coupling_weights.get("sulfur_to_oxygen", 0.15)
             self.oxygen.o2_level *= (1 - throttle)

        # Heat from oxygen -> water evaporation
        heat_from_o2 = o_out["heat_generated"] * self.coupling_weights.get("oxygen_to_water", 0.20)
        await self.water.evaporate(heat_from_o2, temp)

        # 4. Evaluate ecosystem health
        cycle_scores = {
            "water": self.water.get_homeostasis_score(temp),
            "carbon": self.carbon.get_homeostasis_score(),
            "nitrogen": self.nitrogen.get_homeostasis_score(),
            "oxygen": self.oxygen.get_homeostasis_score(temp),
            "phosphorus": self.phosphorus.get_homeostasis_score(),
            "sulfur": self.sulfur.get_homeostasis_score()
        }

        # Ψ-Functional Objective
        psi = self.psi_objective.evaluate(
            cycle_scores, context.get("system_metrics", {}),
            legal_compliance=context.get("legal_compliance", 1.0),
            closed_loop_waste=context.get("closed_loop_waste", 0.0),
            biomimetic_fidelity=context.get("biomimetic_fidelity", 1.0),
            genetic_integrity=context.get("genetic_integrity", 1.0)
        )

        # Hard constraint on Divine Alignment
        if divine_score < 0.80:
            psi = float('-inf')

        stability_index = np.mean(list(cycle_scores.values())) - 1.0

        status = "HOMEOSTATIC" if (psi >= self.target_psi and stability_index < 0) else "PERTURBED"
        if psi == float('-inf'):
            status = "CONSTITUTIONAL_VIOLATION"

        res = {
            "psi_score": psi,
            "stability_index": float(stability_index),
            "divine_score": divine_score,
            "status": status,
            "cycle_scores": cycle_scores
        }

        await self.ueg.log_minimisation_event("geospheric_orchestrator_step", res)
        return res
