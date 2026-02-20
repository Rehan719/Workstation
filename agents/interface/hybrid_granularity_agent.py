from typing import Any, Dict, Optional
from agentic_core.base_agent import BaseAgent
from agentic_core.interface.hybrid_granularity_controller import HybridGranularityController

class HybridGranularityAgent(BaseAgent):
    """
    Agent responsible for managing UI information density based on user behavior (Article S).
    """
    def __init__(self, agent_id: str = "agent.granularity.v31", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.controller = HybridGranularityController()

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        user_id = context.get("user_id", "default_user") if context else "default_user"
        action = task.get("action")

        if action == "process_interaction":
            interaction = task.get("interaction", {})
            result = await self.controller.process_interaction(user_id, interaction)
            return {"status": "success", "suggested_action": result}

        elif action == "explicit_change":
            mode = task.get("mode")
            await self.controller.handle_explicit_change(user_id, mode)
            return {"status": "success", "new_mode": mode}

        return {"status": "error", "message": "No valid action provided"}
