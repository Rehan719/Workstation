import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EnvironmentManager:
    """Manages application lifecycle environments: Dev, Staging, Prod."""
    def __init__(self):
        self.apps = {}

    def set_environment(self, app_id: str, env: str):
        if env not in ["dev", "staging", "prod"]:
            return False

        logger.info(f"EnvMgr: Moving {app_id} to {env}")
        self.apps[app_id] = env
        return True

    def get_status(self, app_id: str) -> str:
        return self.apps.get(app_id, "unknown")
