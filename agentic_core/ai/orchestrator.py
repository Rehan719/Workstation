from typing import List, Dict, Any
from agentic_core.ai.gateway import gateway

class CrewManager:
    """v148.0 Multi-Agent Orchestration Manager."""
    def __init__(self):
        self.agents = {
            "CEO": "Executive oversight and decision management.",
            "CFO": "Financial optimization and resource allocation.",
            "CTO": "Technical infrastructure and evolution trajectory."
        }

    async def delegate_task(self, agent_role: str, task: str) -> Dict[str, Any]:
        """Delegates a specific task to a C-Suite agent."""
        if agent_role not in self.agents:
            # W511 — the SAME SHAPE as the answer below. A caller doing `result["response"]` on this branch
            # raised KeyError, and it is the branch that runs when the role is wrong — the one most likely to
            # be hit. `error` is ADDED to the shape, not substituted for it.
            return {"agent": agent_role, "response": None, "status": "refused",
                    "error": f"Agent {agent_role} not found."}

        prompt = f"Agent: {agent_role}\nRole: {self.agents[agent_role]}\nTask: {task}"
        # P2.2 (W511) — the recall decision STATED. An agent-role prompt carries its own role and task;
        # there is no user context to recall, and a call that does not say leaves the next reader to look
        # up a default that has already changed once (W489).
        response = await gateway.query(prompt, augment=False, user_text=(task or None))   # W651 (FU-675)

        return {
            "agent": agent_role,
            "response": response,
            "status": "completed",
            "error": None,
        }

orchestrator = CrewManager()
