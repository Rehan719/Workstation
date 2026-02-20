from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

class WorkspaceManager:
    """
    Article W: The Adaptive Collaborative Workspace.
    Manages real-time multi-user collaborative workspaces with shared state.
    """
    def __init__(self):
        self.workspaces = {}
        self.active_sessions = {}

    async def create_workspace(self, user_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        workspace_id = str(uuid.uuid4())
        workspace = {
            'id': workspace_id,
            'owner': user_id,
            'members': {user_id: 'owner'},
            'state': {},
            'history': [],
            'created_at': datetime.utcnow().isoformat()
        }
        self.workspaces[workspace_id] = workspace
        return workspace

    async def join_workspace(self, workspace_id: str, user_id: str) -> Dict[str, Any]:
        if workspace_id not in self.workspaces:
            raise ValueError("Workspace not found")

        workspace = self.workspaces[workspace_id]
        if user_id not in workspace['members']:
            workspace['members'][user_id] = 'viewer'

        return workspace

    async def update_state(self, workspace_id: str, user_id: str, changes: Dict[str, Any]):
        workspace = self.workspaces.get(workspace_id)
        if not workspace: return

        # In a real system, use Y.js/CRDT logic here
        workspace['state'].update(changes)
        workspace['history'].append({
            'user': user_id,
            'changes': changes,
            'timestamp': datetime.utcnow().isoformat()
        })
