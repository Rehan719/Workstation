import logging
import numpy as np

logger = logging.getLogger(__name__)

class Chaperone:
    """
    DT: Heat Shock Response.
    Assists in protein (code) folding and prevents aggregation.
    """
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.occupied = 0

    def assist_folding(self, client_id: str) -> bool:
        if self.occupied < self.capacity:
            self.occupied += 1
            logger.debug(f"HSP: {self.name} assisting folding of {client_id}")
            return True
        else:
            logger.warning(f"HSP: {self.name} at full capacity!")
            return False

    def release(self):
        if self.occupied > 0:
            self.occupied -= 1

class HeatShockResponse:
    """
    DT: System-wide stress response.
    """
    def __init__(self):
        self.hsp70 = Chaperone("HSP70", 100)
        self.hsf1_active = False

    def detect_stress(self, misfolded_count: int):
        if misfolded_count > 10:
            self.hsf1_active = True
            logger.info("HSP: HSF1 Activated. Upregulating chaperone production.")
            self.hsp70.capacity += 50
        else:
            self.hsf1_active = False

    def handle_misfolding(self, clients: List[str]) -> List[str]:
        failed = []
        for client in clients:
            if not self.hsp70.assist_folding(client):
                failed.append(client)
        return failed
