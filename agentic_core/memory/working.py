import redis
import json
from typing import Any, Dict, Optional

class WorkingMemory:
    """
    Working Memory: Redis-based ephemeral context and project state.
    """
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set_context(self, project_id: str, context: Dict[str, Any], ttl: int = 3600):
        self.client.setex(f"context:{project_id}", ttl, json.dumps(context))

    def get_context(self, project_id: str) -> Optional[Dict[str, Any]]:
        data = self.client.get(f"context:{project_id}")
        return json.loads(data) if data else None

    def update_context(self, project_id: str, updates: Dict[str, Any]):
        current = self.get_context(project_id) or {}
        current.update(updates)
        self.set_context(project_id, current)
