import logging
from collections import deque
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SensoryMemory:
    """
    CH-VII: Sensory Memory Buffers.
    Short-term storage for iconic and echoic memory.
    """
    def __init__(self, max_size: int = 100):
        self.iconic_memory = deque(maxlen=max_size) # Vision
        self.echoic_memory = deque(maxlen=max_size) # Audition
        self.haptic_memory = deque(maxlen=max_size) # Touch

    def buffer_sensory_event(self, event: Dict[str, Any]):
        """Retains recent experiences for temporal integration."""
        modality = event.get("modality")
        if modality == "vision":
            self.iconic_memory.append(event)
        elif modality == "audition":
            self.echoic_memory.append(event)
        elif modality == "touch":
            self.haptic_memory.append(event)

        logger.info(f"MEMORY: Buffered {modality} event.")

    def get_recent_history(self, modality: str) -> list:
        if modality == "vision": return list(self.iconic_memory)
        if modality == "audition": return list(self.echoic_memory)
        return []
