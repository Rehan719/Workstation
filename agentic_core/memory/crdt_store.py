from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
import uuid

class CRDTStore:
    """
    Local-first data layer using Conflict-free Replicated Data Types (CRDT).
    Implements a multi-value LWW-Element-Set for robust project synchronization.
    """
    def __init__(self):
        self.state: Dict[str, Dict[str, Any]] = {}  # project_id -> {fields: {name: {value, timestamp}}, node_id}
        self.node_id = str(uuid.uuid4())

    def update_project(self, project_id: str, field_name: str, value: Any):
        """
        Updates a specific field in a project with local-first LWW semantics.
        """
        if project_id not in self.state:
            self.state[project_id] = {"fields": {}, "node_id": self.node_id}

        self.state[project_id]["fields"][field_name] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).timestamp()
        }

    def merge(self, remote_state: Dict[str, Dict[str, Any]]):
        """
        Merges a remote replica into the local state using field-level LWW semantics.
        """
        for project_id, remote_project in remote_state.items():
            if project_id not in self.state:
                self.state[project_id] = remote_project
            else:
                local_fields = self.state[project_id]["fields"]
                remote_fields = remote_project["fields"]

                for field_name, remote_data in remote_fields.items():
                    if field_name not in local_fields:
                        local_fields[field_name] = remote_data
                    else:
                        local_data = local_fields[field_name]
                        if remote_data["timestamp"] > local_data["timestamp"]:
                            local_fields[field_name] = remote_data

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the current state of all fields for a project.
        """
        project = self.state.get(project_id)
        if not project:
            return None

        return {name: data["value"] for name, data in project["fields"].items()}

    def get(self, project_id: str) -> Optional[Any]:
        # Legacy support
        return self.get_project(project_id)
