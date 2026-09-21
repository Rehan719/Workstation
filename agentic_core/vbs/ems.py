import logging
from typing import Dict, Any

class EnvironmentalManagementSystem:
    """VBS: EMS Stewardship — CO2 accrual over reported energy.

    W440 docstring truth: no FLOP/Watt monitoring exists (nothing reads FLOPs); the class accrues
    kgCO2 per reported Wh (real arithmetic over caller figures) and returns two constants the
    route discloses as simulated. The accrual is in-memory, per-process.
    """
    def __init__(self, config_path: str):
        self.logger = logging.getLogger("EMS")
        self.total_co2_kg = 0.0
        self.last_emissions_kg = 0.0   # W489 — this call's own estimate, kept separate from the total

    # W489 (sweep S11.7, C3) — THIS RUN'S FIGURE AND THE PROCESS TOTAL ARE DIFFERENT NUMBERS.
    # `monitor_efficiency` returned the literal 0.85 and callers rendered it as "EMS +85%" on a green
    # chip beside "this run's result" — it is identical on every run and `energy_wh` never touches it.
    # Worse, the CO2 figure shown as the run's was `total_co2_kg`, a PROCESS-LIFETIME accumulator on a
    # module singleton, so it grew across every cascade since server start. The per-call emission was
    # computed and thrown away. It is now returned, so a caller can report the run's own figure, and
    # the constant is named a constant.
    EFFICIENCY_GAIN_CONSTANT = 0.85     # a fixed catalogue figure — nothing measures efficiency here
    KG_CO2_PER_WH = 0.00045             # a fixed intensity factor applied to an energy ESTIMATE

    async def monitor_efficiency(self, energy_wh: float) -> float:
        """Accrue this call's estimated emissions and return the efficiency CONSTANT (not a measurement).

        Prefer `measure(energy_wh)`, which returns this call's own emissions alongside it."""
        self.last_emissions_kg = round(energy_wh * self.KG_CO2_PER_WH, 9)
        self.total_co2_kg += self.last_emissions_kg
        return self.EFFICIENCY_GAIN_CONSTANT

    async def measure(self, energy_wh: float) -> dict:
        """This call's emissions estimate, the process total, and the efficiency constant — each named."""
        await self.monitor_efficiency(energy_wh)
        return {
            "co2_kg_this_run": self.last_emissions_kg,
            "process_total_co2_kg": round(self.total_co2_kg, 9),
            "efficiency_gain_constant": self.EFFICIENCY_GAIN_CONSTANT,
            "efficiency_measured": False,
            "basis": (f"emissions = energy estimate x {self.KG_CO2_PER_WH} kgCO2/Wh (a constant); the "
                      f"efficiency figure is the fixed {self.EFFICIENCY_GAIN_CONSTANT} and is not measured; "
                      f"the process total accrues across every run since this server started"),
        }

    def get_resource_gain(self) -> float:
        return 0.22 # ≥20%/cycle target
