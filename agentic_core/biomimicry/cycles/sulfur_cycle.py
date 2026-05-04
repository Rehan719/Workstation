from .base_cycle import CycleController
class SulfurCycle(CycleController):
    def __init__(self, ueg):
        super().__init__('sulfur', 1.0, ueg)
