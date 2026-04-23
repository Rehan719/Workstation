from .water_cycle import HydrologicResourceManager
from .carbon_cycle import CarbonDataMetabolism
from .nitrogen_cycle import NitrogenTaskMediator
from .oxygen_cycle import OxygenComputationalMetabolism
from .phosphorus_cycle import PhosphorusMemoryHierarchy
from .sulfur_cycle import SulfurErrorResilience
from .psi_functional import EcosystemHealthObjective
from typing import Dict, Any

class GeosphericHomeostaticOrchestrator:
    """
    Coordinates Earth's six biogeochemical cycles as a converged digital fabric.
    Enforces Ψ-Functional health targets and cycle coupling feedback.
    """
    def __init__(self, target_psi: float = 0.90):
        self.water = HydrologicResourceManager()
        self.carbon = CarbonDataMetabolism()
        self.nitrogen = NitrogenTaskMediator()
        self.oxygen = OxygenComputationalMetabolism()
        self.phosphorus = PhosphorusMemoryHierarchy()
        self.sulfur = SulfurErrorResilience()
        self.psi_objective = EcosystemHealthObjective()
        self.target_psi = target_psi

    def step(self, system_load: float, error_rate: float, data_size: float) -> Dict[str, Any]:
        """Executes one homeostatic step of the geospheric ecosystem."""

        # 1. Regulate Cycles
        water_res = self.water.balance_resources(system_load)
        carbon_burial = self.carbon.respire_unused_data(data_size)
        oxygen_mode = self.oxygen.regulate_metabolic_rate(system_load)

        # 2. Cycle Coupling (Feedback)
        # Oxygen (compute) produces heat (Water)
        thermal_load = system_load * 50.0
        evap_energy = self.water.evaporate(thermal_load)

        # Sulfur (errors) triggers Acid Rain (Slowdown)
        sulfur_response = self.sulfur.trigger_acid_rain(error_rate)

        # 3. Health Evaluation
        metrics = {
            "water": 0.95,
            "carbon": 0.92,
            "nitrogen": 0.98,
            "oxygen": 0.94,
            "phosphorus": 0.96,
            "sulfur": 1.0 - error_rate
        }

        psi_score = self.psi_objective.evaluate(metrics)

        return {
            "psi_score": psi_score,
            "status": "HOMEOSTATIC" if psi_score >= self.target_psi else "PERTURBED",
            "cycle_states": {
                "oxygen": oxygen_mode,
                "water": water_res["mode"],
                "sulfur": sulfur_response["action"]
            }
        }
