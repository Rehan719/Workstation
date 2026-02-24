import logging
from typing import Set

logger = logging.getLogger(__name__)

class ThreatMemory:
    """
    BY-II: Persistent threat pattern database.
    Ensures rapid recognition of known threats (<50ms).
    """
    def __init__(self):
        self.memory: Set[int] = set()

    def remember_threat(self, threat_hash: int):
        self.memory.add(threat_hash)
        logger.info(f"IMMUNE MEMORY: Logged new threat pattern {threat_hash}")

    def is_known_threat(self, threat_hash: int) -> bool:
        return threat_hash in self.memory
