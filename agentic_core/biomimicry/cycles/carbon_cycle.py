from .base_cycle import CycleController
class CarbonCycle(CycleController):
    def __init__(self, ueg):
        super().__init__('carbon', 1.0, ueg)
