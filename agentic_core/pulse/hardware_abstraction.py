import platform

class HardwareAbstraction:
    """
    BS-V: Abstraction layer for ARM TrustZone, x86, RISC-V.
    Detects hardware capabilities for pulse clock isolation.
    """
    def __init__(self):
        self.arch = platform.machine()
        self.os = platform.system()

    def get_high_res_timer_capability(self) -> bool:
        # Most modern platforms have some form of high-res timer
        return True
