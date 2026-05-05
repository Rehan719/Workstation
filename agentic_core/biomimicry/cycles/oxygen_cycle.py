from .water_cycle import PIDController

class MetabolicScheduler:
    def __init__(self, cpu_system, ueg, validator):
        self.pid = PIDController(setpoint=60.0, kp=1.5, ki=0.2, kd=0.3)
        self.cpu_system = cpu_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {"cpu_respiration": 0.0}

    async def respire(self, scaling_factor: float):
        self.reservoirs["cpu_respiration"] = scaling_factor
        if hasattr(self.ueg, "log"):
            await self.ueg.log("oxygen_respiration", scaling=scaling_factor)
        return scaling_factor

    async def regulate_homeostasis(self, cpu_utilization: float) -> float:
        error = self.pid.setpoint - cpu_utilization
        correction = self.pid.compute(error)
        return correction

    async def get_state(self):
        return {"reservoirs": self.reservoirs, "setpoint": self.pid.setpoint}
