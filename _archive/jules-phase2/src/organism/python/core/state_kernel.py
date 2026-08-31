import asyncio
import logging
import json
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

logger = logging.getLogger(__name__)

class StateChange(BaseModel):
    key: str
    old_value: Any
    new_value: Any
    timestamp: float = Field(default_factory=lambda: datetime.utcnow().timestamp())
    session_id: Optional[str] = None

class SovereignState:
    """
    Unified state manager merging local and global context with session isolation.
    """
    def __init__(self, storage_dir: str = "data/organism/state"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self._lock = asyncio.Lock()
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._global_context: Dict[str, Any] = {}

    async def merge_context(self, local: Dict[str, Any], global_ctx: Dict[str, Any]) -> Dict[str, Any]:
        """Merges local workstation state with global AI CEO context."""
        async with self._lock:
            merged = {**global_ctx, **local}
            self._global_context.update(global_ctx)
            return merged

    async def persist_session(self, session_id: str, state: Dict[str, Any]):
        """Persists session-isolated state to disk."""
        async with self._lock:
            self._sessions[session_id] = state
            file_path = os.path.join(self.storage_dir, f"{session_id}.json")
            try:
                with open(file_path, "w") as f:
                    json.dump(state, f, indent=2)
                logger.info(f"SovereignState: Persisted session {session_id}")
            except Exception as e:
                logger.error(f"SovereignState: Persistence failure for {session_id}: {e}")

    async def restore_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Restores session state from disk or memory."""
        if session_id in self._sessions:
            return self._sessions[session_id]

        file_path = os.path.join(self.storage_dir, f"{session_id}.json")
        if os.path.exists(file_path):
            try:
                async with self._lock:
                    with open(file_path, "r") as f:
                        state = json.load(f)
                        self._sessions[session_id] = state
                        return state
            except Exception as e:
                logger.error(f"SovereignState: Restore failure for {session_id}: {e}")
        return None

    async def set_value(self, session_id: str, key: str, value: Any):
        """Updates a state value and triggers a change event."""
        async with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = {}

            old_value = self._sessions[session_id].get(key)
            self._sessions[session_id][key] = value

            change = StateChange(
                key=key,
                old_value=old_value,
                new_value=value,
                session_id=session_id
            )
            return change
