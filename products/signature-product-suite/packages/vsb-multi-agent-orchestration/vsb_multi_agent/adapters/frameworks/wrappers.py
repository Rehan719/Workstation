from typing import Dict, Any, List

class ConstitutionalWrapper:
    """Base class for framework-specific constitutional wrappers."""
    def __init__(self, gaas):
        self.gaas = gaas

class AutoGenConstitutionalWrapper(ConstitutionalWrapper):
    """Wraps AutoGen GroupChat with constitutional moderation."""
    async def moderate_message(self, message: str, sender: str) -> bool:
        gate_result = await self.gaas.policy_gate.validate_action("agent_message", {"content": message, "sender": sender})
        if not gate_result["allowed"]:
            self.gaas.ueg.log_policy_halt(self.gaas.domain, "agent_message", gate_result["reason"])
            return False
        return True

class LangGraphConstitutionalWrapper(ConstitutionalWrapper):
    """Wraps LangGraph nodes with constitutional checkpointers."""
    async def checkpoint_node(self, node_id: str, state: Dict[str, Any]) -> bool:
        # Before node execution, validate state
        if self.gaas.circuit_breaker.should_halt():
            return False
        return True

class CrewAIConstitutionalWrapper(ConstitutionalWrapper):
    """Wraps CrewAI tasks with constitutional policy gates."""
    async def validate_task_execution(self, task_id: str, context: Dict[str, Any]) -> bool:
        gate_result = await self.gaas.policy_gate.validate_action("task_execution", {"task_id": task_id, "context": context})
        return gate_result["allowed"]
