from typing import Any, Dict, List, Optional
import asyncio
import yaml
import os
from .base_agent import BaseAgent
from .protocols.samp import SAMPMessage
from .quantum_ai.hierarchy_manager import CapabilityHierarchyManager
from .interface.hybrid_granularity_controller import HybridGranularityController
from .tools.context_aware_integrator import ContextAwareToolIntegrator

class Orchestrator(BaseAgent):
    """
    C-IV Orchestrator Agent: Strategic planning, goal decomposition, and hybrid toolchain activation.
    Integrates Hierarchy Management (Article R), Hybrid Granularity (Article S), and Context-Aware Tools (Article T).
    """
    def __init__(self, agent_id: str = "orchestrator.v31", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.workers: Dict[str, BaseAgent] = {}

        # v31.0 Enhanced Engines
        self.hierarchy_manager = CapabilityHierarchyManager()
        self.granularity_controller = HybridGranularityController()
        self.tool_integrator = ContextAwareToolIntegrator()

    def register_worker(self, worker: BaseAgent):
        self.workers[worker.agent_id] = worker
        self.log(f"Registered worker: {worker.agent_id}")

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Decomposes a high-level goal into subtasks and coordinates execution with v31.0 enhancements.
        """
        self.log(f"Starting C-IV orchestration for task: {task.get('goal', 'No goal specified')}")

        # v31.0 Article S: Process Granularity Signals
        if context and 'interaction' in context:
            await self.granularity_controller.process_interaction(context.get('user_id', 'default'), context['interaction'])

        # v31.0 Article R: Check Hierarchy Prerequisites
        target_tier = task.get('tier', 'tier1')
        await self.hierarchy_manager.ensure_tier_prerequisites(target_tier)

        # 1. Plan (Goal Decomposition)
        plan = await self._plan(task)
        self.log(f"Generated execution plan with {len(plan)} subtasks")

        # 2. Execute subtasks with Context-Aware Tooling (Article T)
        results = {}
        for subtask in plan:
            # Activate toolchain if needed
            enhanced_task = await self.tool_integrator.process_task(subtask)
            subtask.update(enhanced_task)

            worker_id = subtask.get("assigned_agent") or subtask.get("agent")
            if worker_id in self.workers:
                self.log(f"Delegating subtask '{subtask['id']}' to {worker_id} (Tools: {subtask.get('tools_used', [])})")
                results[subtask["id"]] = await self.workers[worker_id].execute(subtask, context)
            else:
                self.log(f"No worker registered for agent type: {worker_id}", level="ERROR")

        # 3. Aggregate results
        final_output = self._aggregate(results)

        # Sign final artifact if requested (Article T)
        if task.get('produces_artifact'):
            final_output = await self.tool_integrator.process_task({**task, 'artifact_data': final_output})

        return final_output

    async def _plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Dynamic planning: selects a workflow based on task type or uses LLM reasoning.
        """
        task_type = task.get("type", "scientific_publication")

        if task_type == "agent_direct":
            return [task]
        workflow_path = f"config/workflows/{task_type}.yaml"

        if os.path.exists(workflow_path):
            self.log(f"Loading workflow from {workflow_path}")
            with open(workflow_path, 'r') as f:
                workflow = yaml.safe_load(f)
                return workflow.get("steps", [])

        # Fallback to simple static planning
        goal = task.get("goal", "").lower()
        if "paper" in goal or "manuscript" in goal:
            return [
                {"id": "lit_review", "assigned_agent": "research.literature.v3", "query": goal},
                {"id": "drafting", "assigned_agent": "writing.manuscript.architect.v4", "content": "${lit_review}"}
            ]
        return []

    def _aggregate(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregates results from workers.
        """
        return {
            "status": "completed",
            "components": results
        }

if __name__ == "__main__":
    # Entry point for the orchestrator service
    orchestrator = Orchestrator()
    print("🚀 Jules AI C-IV Orchestrator Service is running...")

    async def main_loop():
        while True:
            # In a real system, this would listen to a message queue (RabbitMQ/Redis)
            await asyncio.sleep(60)

    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Stopping Orchestrator...")
