from typing import Any, Dict, List, Optional
import asyncio
import yaml
import os
from .base_agent import BaseAgent
from .protocols.samp import SAMPMessage

class Orchestrator(BaseAgent):
    """
    L3 Orchestrator Agent: Goal decomposition, resource allocation, and agent coordination.
    Integrates PC-Agent hierarchical model and AutoGen conversational concepts.
    """
    def __init__(self, agent_id: str = "orchestrator.v10", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)
        self.workers: Dict[str, BaseAgent] = {}

    def register_worker(self, worker: BaseAgent):
        self.workers[worker.agent_id] = worker
        self.log(f"Registered worker: {worker.agent_id}")

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Decomposes a high-level goal into subtasks and coordinates execution.
        """
        self.log(f"Starting orchestration for task: {task.get('goal', 'No goal specified')}")

        # 1. Plan (Goal Decomposition)
        plan = await self._plan(task)
        self.log(f"Generated execution plan with {len(plan)} subtasks")

        # 2. Execute subtasks
        results = {}
        for subtask in plan:
            worker_id = subtask.get("assigned_agent") or subtask.get("agent")
            if worker_id in self.workers:
                self.log(f"Delegating subtask '{subtask['id']}' to {worker_id}")
                results[subtask["id"]] = await self.workers[worker_id].execute(subtask, context)
            else:
                self.log(f"No worker registered for agent type: {worker_id}", level="ERROR")

        # 3. Aggregate results
        final_output = self._aggregate(results)
        return final_output

    async def _plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Dynamic planning: selects a workflow based on task type or uses LLM reasoning.
        """
        task_type = task.get("type", "scientific_publication")
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
