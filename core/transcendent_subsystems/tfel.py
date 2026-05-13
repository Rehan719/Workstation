import math, time
from dataclasses import dataclass
from datetime import datetime, timezone
@dataclass
class ThermodynamicBudget:
    max_entropy_bits: float; current_entropy_bits: float = 0.0
    @property
    def remaining(self) -> float: return self.max_entropy_bits - self.current_entropy_bits
class ThermodynamicFreeEnergyLedger:
    def __init__(self, budget_bits=1e12, temperature=300.0, ueg_logger=None):
        self.E_min = 1.380649e-23 * temperature * math.log(2); self.budget = ThermodynamicBudget(budget_bits); self.ueg, self.hw = ueg_logger, 1.0
    def meter_operation(self, name, bits):
        if bits > self.budget.remaining: raise PermissionError(f"TFEL: {name} exceeds budget")
        self.budget.current_entropy_bits += bits
        return {"op": name, "entropy_bits": bits, "energy_joules": bits * self.E_min * self.hw, "budget_remaining": self.budget.remaining, "timestamp": time.time()}
    def export_cycle_ledger(self, cid):
        res = {"cycle_id": cid, "total_entropy_bits": self.budget.current_entropy_bits, "compliance": True, "timestamp": datetime.now(timezone.utc).isoformat()}
        self.budget.current_entropy_bits = 0.0
        return res
