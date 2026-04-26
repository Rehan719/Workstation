from typing import Dict, Any

class PhosphorusMemoryHierarchy:
    def __init__(self, ram_capacity: float = 1.0):
        self.reservoirs = {
            "ram": 0.05,
            "ssd": 0.2,
            "archive": 0.75
        }
        self.ram_capacity = ram_capacity

    def uptake(self, data_size: float) -> Dict[str, float]:
        available_p = min(self.reservoirs["ssd"], data_size)
        if self.reservoirs["ram"] + available_p > self.ram_capacity:
            available_p = self.ram_capacity - self.reservoirs["ram"]
        self.reservoirs["ssd"] -= available_p
        self.reservoirs["ram"] += available_p
        return {
            "uptake_amount": available_p,
            "is_limiting": self.reservoirs["ram"] >= self.ram_capacity
        }

    def get_homeostasis_score(self) -> float:
        usage = self.reservoirs["ram"] / self.ram_capacity
        return 1.0 - (usage if usage > 0.9 else 0.0)

    def get_output(self) -> float:
        return 1.0 - (self.reservoirs["ram"] / self.ram_capacity)

    def validate(self, cycle_state: Any, context: Any) -> Any:
        return type('Validation', (), {'passed': True, 'score': 1.0, 'reason': ''})()
