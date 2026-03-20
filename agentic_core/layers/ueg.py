import json
import time
from typing import Dict, Any, List, Optional
import hashlib

class UnifiedEventGraphUEG:
    """
    CENTRALIZED NERVOUS SYSTEM - Unified Event Graph (UEG).
    Provides immutable logging with cryptographic anchoring (Merkle Proofs).
    """
    def __init__(self, level: str = "FULL"):
        self.levels = ["FULL", "SELECTIVE", "DISABLED"]
        self.current_level = level if level in self.levels else "FULL"
        self.events: List[Dict[str, Any]] = []
        self.merkle_root: str = hashlib.sha256(b"genesis").hexdigest()

    def set_level(self, level: str) -> bool:
        """Dynamic configuration of logging level (GaaS)."""
        if level in self.levels:
            self.current_level = level
            print(f"UEG: Logging level updated to {self.current_level}.")
            return True
        return False

    def log_event(self, layer: str, component: str, event_type: str, payload: Dict[str, Any], tags: List[str] = []) -> bool:
        """Appends a new event to the Unified Event Graph."""
        if self.current_level == "DISABLED":
            return True

        if self.current_level == "SELECTIVE" and "audit-required" not in tags:
            return True

        event = {
            "layer": layer,
            "component": component,
            "event_type": event_type,
            "payload": payload,
            "tags": tags,
            "timestamp": time.time(),
            "event_id": hashlib.sha256(f"{layer}{component}{time.time()}".encode()).hexdigest()
        }

        self.events.append(event)
        self._update_merkle_root(event["event_id"])

        # In Phase 1, we also print to console for visibility
        print(f"UEG [{layer}]: {event_type} - {component}")
        return True

    def _update_merkle_root(self, event_id: str):
        """Cryptographic anchoring simulation."""
        self.merkle_root = hashlib.sha256((self.merkle_root + event_id).encode()).hexdigest()

    def get_events(self, event_type: Optional[str] = None, layer: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries the event graph."""
        filtered = self.events
        if event_type:
            filtered = [e for e in filtered if e["event_type"] == event_type]
        if layer:
            filtered = [e for e in filtered if e["layer"] == layer]
        return filtered

ueg = UnifiedEventGraphUEG()
