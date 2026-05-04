from .base_cycle import CycleController
class OxygenCycle(CycleController):
    def __init__(self, ueg):
        super().__init__('oxygen', 1.0, ueg)
