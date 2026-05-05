from .water_cycle import PIDController
from datetime import datetime

class DataCarbonCycle:
    def __init__(self, storage_system, ueg, validator):
        self.pid = PIDController(setpoint=50.0, kp=1.0, ki=0.1, kd=0.2)
        self.storage = storage_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {"active_data": 0.0, "archived_data": 0.0}

    async def photosynthesize(self, data_inflow: float) -> float:
        # data inflow/ingestion
        self.reservoirs["active_data"] += data_inflow
        if hasattr(self.ueg, "log"):
            await self.ueg.log("carbon_photosynthesis", data_inflow=data_inflow)
        return data_inflow

    async def regulate_homeostasis(self, current_load: float) -> float:
        error = self.pid.setpoint - current_load
        correction = self.pid.compute(error)
        if hasattr(self.storage, "adjust_metabolism"):
            self.storage.adjust_metabolism(correction)
        return correction

    async def get_state(self):
        return {"reservoirs": self.reservoirs, "setpoint": self.pid.setpoint}
