from typing import Any, Dict, List, Optional
import os
import json
import uuid
from .base_agent import BaseAgent

class ProjectManager(BaseAgent):
    """
    Article: Establishing Governance, Provenance, and Operational Excellence.
    ASC Lifecycle Manager: Design, Deployment, Operation and Evolution.
    """
    def __init__(self, agent_id: str = "project_manager.v10", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.base_path = "content/projects"

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        action = task.get("action", "create")
        project_id = task.get("project_id", str(uuid.uuid4()))

        self.log(f"Project Manager executing action: {action} for project: {project_id}")

        if action == "create":
            return await self._create_project(project_id, task.get("brief", {}))
        elif action == "archive":
            return await self._archive_project(project_id)

        return {"status": "unknown_action", "project_id": project_id}

    async def _create_project(self, project_id: str, brief: Dict[str, Any]) -> Dict[str, Any]:
        path = os.path.join(self.base_path, project_id)
        os.makedirs(path, exist_ok=True)
        os.makedirs(os.path.join(path, "specs"), exist_ok=True)
        os.makedirs(os.path.join(path, "drafts"), exist_ok=True)
        os.makedirs(os.path.join(path, "approved"), exist_ok=True)
        os.makedirs(os.path.join(path, "provenance"), exist_ok=True)

        with open(os.path.join(path, "brief.md"), "w") as f:
            f.write(f"# Project Brief: {project_id}\n\n{json.dumps(brief)}")

        return {"status": "created", "project_id": project_id, "path": path}

    async def _archive_project(self, project_id: str) -> Dict[str, Any]:
        self.log(f"Archiving project {project_id}")
        return {"status": "archived", "project_id": project_id}
