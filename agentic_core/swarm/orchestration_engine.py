import logging
from typing import List, Dict, Any, Optional
import uuid
from .signal_types import SwarmSignal, SignalType
from .signaling_protocol import SignalingProtocol

logger = logging.getLogger(__name__)

class SwarmTask:
    def __init__(self, goal: str, parent_id: Optional[str] = None):
        self.task_id = str(uuid.uuid4())
        self.goal = goal
        self.parent_id = parent_id
        self.assigned_to: Optional[str] = None
        self.status = "PENDING" # PENDING, ASSIGNED, COMPLETED, FAILED
        self.results: Any = None

class OrchestrationEngine:
    """
    DM: Collective Intelligence Orchestration Engine.
    Handles Task Decomposition and Assignment.
    """
    def __init__(self, agent_id: str, signaling: SignalingProtocol):
        self.agent_id = agent_id
        self.signaling = signaling
        self.tasks: Dict[str, SwarmTask] = {}
        self.swarm_nodes: List[str] = [] # List of active agent IDs

    def decompose_goal(self, high_level_goal: str) -> List[SwarmTask]:
        """Decomposes a goal into a DAG of sub-tasks"""
        logger.info(f"ORCHESTRATOR: Decomposing goal: {high_level_goal}")
        # Simplified decomposition logic
        sub_goals = [
            f"Research: {high_level_goal}",
            f"Analyze: {high_level_goal}",
            f"Synthesize: {high_level_goal}"
        ]
        new_tasks = [SwarmTask(sg) for sg in sub_goals]
        for t in new_tasks:
            self.tasks[t.task_id] = t
        return new_tasks

    def assign_tasks(self):
        """Assigns pending tasks to available swarm members"""
        pending_tasks = [t for t in self.tasks.values() if t.status == "PENDING"]
        if not pending_tasks:
            return

        logger.info(f"ORCHESTRATOR: Assigning {len(pending_tasks)} pending tasks.")

        for task in pending_tasks:
            # For simulation, we broadcast a recruitment signal
            recruitment = SwarmSignal(
                sender_id=self.agent_id,
                signal_type=SignalType.RECRUITMENT,
                payload={"task_id": task.task_id, "goal": task.goal},
                priority=0
            )
            self.signaling.send_signal(recruitment)
            task.status = "ASSIGNED"

    def update_task_status(self, task_id: str, status: str, results: Any = None):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = status
            task.results = results
            logger.info(f"ORCHESTRATOR: Task {task_id} updated to {status}")
