from .base_cycle import CycleController
class WaterCycle(CycleController):
    def __init__(self, ueg):
        super().__init__('water', 1.0, ueg)
