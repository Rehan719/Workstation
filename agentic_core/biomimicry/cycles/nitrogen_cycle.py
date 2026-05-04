from .base_cycle import CycleController
class NitrogenCycle(CycleController):
    def __init__(self, ueg):
        super().__init__('nitrogen', 1.0, ueg)
