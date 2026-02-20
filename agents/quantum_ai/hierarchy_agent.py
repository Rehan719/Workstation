from typing import Any, Dict, Optional
from agentic_core.base_agent import BaseAgent
from agentic_core.quantum_ai.hierarchy_manager import CapabilityHierarchyManager

class HierarchyAgent(BaseAgent):
    """
    Agent responsible for enforcing the three-tier capability hierarchy (Article R).
    """
    def __init__(self, agent_id: str = "agent.hierarchy.v31", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.manager = CapabilityHierarchyManager()

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        action = task.get("action", "check_stability")
        tier = task.get("tier", "tier1")

        self.log(f"HierarchyAgent performing: {action} on {tier}")

        if action == "check_stability":
            is_stable = await self.manager.check_tier_stability(tier)
            return {"status": "success", "tier": tier, "stable": is_stable}

        elif action == "verify_prerequisites":
            try:
                await self.manager.ensure_tier_prerequisites(tier)
                return {"status": "success", "message": f"Prerequisites for {tier} are satisfied."}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        return {"status": "error", "message": f"Unknown action: {action}"}
