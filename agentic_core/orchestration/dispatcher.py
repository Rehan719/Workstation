import logging
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class FrameworkType(Enum):
    AUTOGEN = "autogen"
    CREWAI = "crewai"
    LANGGRAPH = "langgraph"
    LOCAL_REACTOR = "local_reactor"

class TaskDispatcher:
    """
    v0.9 Orchestrator Layer (L3).
    Dynamically selects the optimal agentic framework per subtask.
    Features a simple heuristic-based decision model.
    """
    def __init__(self):
        self.performance_registry = {} # TaskType -> PerformanceScore
        self.framework_capabilities = {
            FrameworkType.AUTOGEN: ["conversational", "debate", "multi-agent-synthesis"],
            FrameworkType.CREWAI: ["sequential-workflow", "role-based-research", "task-delegation"],
            FrameworkType.LANGGRAPH: ["cyclic-graph", "stateful-orchestration", "code-generation"],
            FrameworkType.LOCAL_REACTOR: ["single-turn", "fast-lookup", "domain-ontology"]
        }

    async def dispatch(self, task_description: str, task_type: str) -> Dict[str, Any]:
        """Dispatches a task to the most suitable framework."""
        framework = self._select_framework(task_type)
        logger.info(f"Orchestrator L3: Dispatching '{task_type}' task to {framework.value}")

        # v0.9: Unified dispatcher logic
        if framework == FrameworkType.AUTOGEN:
             return await self._run_autogen(task_description)
        elif framework == FrameworkType.CREWAI:
             return await self._run_crewai(task_description)
        elif framework == FrameworkType.LANGGRAPH:
             return await self._run_langgraph(task_description)
        else:
             return await self._run_local_reactor(task_description)

    def _select_framework(self, task_type: str) -> FrameworkType:
        # v0.9 Selection Heuristic
        task_type = task_type.lower()
        if any(kw in task_type for kw in ["debate", "talk", "discuss", "synthesis"]):
            return FrameworkType.AUTOGEN
        if any(kw in task_type for kw in ["research", "sequential", "team"]):
            return FrameworkType.CREWAI
        if any(kw in task_type for kw in ["code", "iterative", "stateful"]):
            return FrameworkType.LANGGRAPH
        return FrameworkType.LOCAL_REACTOR

    async def _run_autogen(self, description: str):
        # Simulated AutoGen execution
        return {"status": "SUCCESS", "framework": "AutoGen", "output": f"Multi-agent conversational synthesis complete for: {description}"}

    async def _run_crewai(self, description: str):
        # Simulated CrewAI execution
        return {"status": "SUCCESS", "framework": "CrewAI", "output": f"Role-based research team finished task: {description}"}

    async def _run_langgraph(self, description: str):
        # Simulated LangGraph execution
        return {"status": "SUCCESS", "framework": "LangGraph", "output": f"Stateful graph iteration complete for: {description}"}

    async def _run_local_reactor(self, description: str):
        return {"status": "SUCCESS", "framework": "LocalReactor", "output": f"Domain-specific reactor processed: {description}"}

orchestrator_dispatcher = TaskDispatcher()
