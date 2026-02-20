from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone

class BaseAgent(ABC):
    """
    Base class for all specialized agents in the Jules AI ecosystem.
    """
    def __init__(self, agent_id: str, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.instance_id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)

    @abstractmethod
    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a given task.
        """
        pass

    def log(self, message: str, level: str = "INFO"):
        print(f"[{datetime.now(timezone.utc).isoformat()}] [{self.agent_id}] [{level}] {message}")
