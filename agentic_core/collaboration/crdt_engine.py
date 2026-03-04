import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class CRDTState:
    """
    ARTICLE 92: DUAL-MODE LOCAL-FIRST ARCHITECTURE.
    Enhanced CRDT implementation with per-field LWW and custom resolution hooks.
    """
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.data: Dict[str, Any] = {}
        self.lamport_clock = 0
        self.conflict_resolver_hook = None

    def set_conflict_resolver(self, hook: callable):
        """Sets a custom application-level conflict resolver."""
        self.conflict_resolver_hook = hook

    def update(self, key: str, value: Any):
        self.lamport_clock += 1
        self.data[key] = {
            "value": value,
            "clock": self.lamport_clock,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "origin": "local"
        }

    def merge(self, remote_state: Dict[str, Any]):
        """
        Per-field Last-Writer-Wins (LWW) merge logic.
        Incorporates custom resolution hooks for ambiguous concurrent edits.
        """
        for key, remote_val in remote_state.items():
            local_val = self.data.get(key)

            # Scenario 1: Field is new locally
            if not local_val:
                self.data[key] = remote_val
                continue

            # Scenario 2: Clear precedence via Lamport clock
            if remote_val["clock"] > local_val["clock"]:
                self.data[key] = remote_val
            elif remote_val["clock"] < local_val["clock"]:
                continue # Local version is newer
            else:
                # Scenario 3: Clock collision (Concurrent Edit)
                # Tie-break with timestamp
                if remote_val["timestamp"] > local_val["timestamp"]:
                    self.data[key] = remote_val
                elif remote_val["timestamp"] == local_val["timestamp"]:
                    # Scenario 4: Absolute Ambiguity
                    if self.conflict_resolver_hook:
                        resolved_val = self.conflict_resolver_hook(key, local_val, remote_val)
                        self.data[key] = resolved_val
                    else:
                        # Default heuristic: keep local (no-op)
                        logger.debug(f"CRDT merge collision for {key}. Keeping local version.")

class CollaborationManager:
    """Manages real-time multi-user collaboration sessions."""
    def __init__(self):
        self.sessions: Dict[str, CRDTState] = {}

    def get_or_create_session(self, project_id: str) -> CRDTState:
        if project_id not in self.sessions:
            self.sessions[project_id] = CRDTState(project_id)
        return self.sessions[project_id]

    async def sync_project(self, project_id: str, remote_payload: Dict[str, Any]):
        session = self.get_or_create_session(project_id)
        session.merge(remote_payload)
        return session.data
