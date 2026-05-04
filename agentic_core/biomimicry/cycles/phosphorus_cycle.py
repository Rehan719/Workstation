from .base_cycle import CycleController
class PhosphorusCycle(CycleController):
    def __init__(self, ueg):
        super().__init__('phosphorus', 1.0, ueg)
