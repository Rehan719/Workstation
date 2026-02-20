from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
import uuid

class CRDTStore:
    """
    Local-first data layer using Conflict-free Replicated Data Types (CRDT).
    Implements a Last-Writer-Wins (LWW) Register pattern for project state synchronization.
    """
    def __init__(self):
        self.state: Dict[str, Dict[str, Any]] = {}  # project_id -> {value, timestamp}

    def update(self, project_id: str, data: Any):
        """
        Updates the local replica with a timestamp.
        """
        self.state[project_id] = {
            "value": data,
            "timestamp": datetime.now(timezone.utc).timestamp(),
            "node_id": str(uuid.uuid4())
        }

    def merge(self, remote_state: Dict[str, Dict[str, Any]]):
        """
        Merges a remote replica into the local state using LWW semantics.
        """
        for project_id, remote_entry in remote_state.items():
            if project_id not in self.state:
                self.state[project_id] = remote_entry
            else:
                local_entry = self.state[project_id]
                if remote_entry["timestamp"] > local_entry["timestamp"]:
                    self.state[project_id] = remote_entry
                elif remote_entry["timestamp"] == local_entry["timestamp"]:
                    # Tie-break with node_id
                    if remote_entry["node_id"] > local_entry["node_id"]:
                        self.state[project_id] = remote_entry

    def get(self, project_id: str) -> Optional[Any]:
        entry = self.state.get(project_id)
        return entry["value"] if entry else None
