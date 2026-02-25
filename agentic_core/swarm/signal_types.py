from enum import Enum, auto
import time
from typing import Dict, Any, Optional
import uuid

class SignalType(Enum):
    RECRUITMENT = auto() # Request for assistance
    TRAIL = auto()       # Pheromone-like marking of success
    ALARM = auto()       # Threat detection broadcast
    AGGREGATION = auto() # Cluster formation request
    DISPERSAL = auto()   # Resource scarcity/overpopulation
    HEARTBEAT = auto()   # Liveliness check
    TASK_UPDATE = auto() # Status of assigned task

class SwarmSignal:
    def __init__(self,
                 sender_id: str,
                 signal_type: SignalType,
                 payload: Dict[str, Any],
                 priority: int = 0,
                 target_id: Optional[str] = None):
        self.signal_id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.signal_type = signal_type
        self.payload = payload
        self.priority = priority # 0: Low, 1: High
        self.target_id = target_id
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "sender_id": self.sender_id,
            "signal_type": self.signal_type.name,
            "payload": self.payload,
            "priority": self.priority,
            "target_id": self.target_id,
            "timestamp": self.timestamp
        }
