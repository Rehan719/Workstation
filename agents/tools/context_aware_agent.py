from typing import Any, Dict, Optional
from agentic_core.base_agent import BaseAgent
from agentic_core.tools.context_aware_integrator import ContextAwareToolIntegrator

class ContextAwareAgent(BaseAgent):
    """
    Agent responsible for selective toolchain activation (Article T).
    """
    def __init__(self, agent_id: str = "agent.tools.v31", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.integrator = ContextAwareToolIntegrator()

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.log(f"ContextAwareAgent processing task: {task.get('id', 'unknown')}")
        result = await self.integrator.process_task(task)
        return result
