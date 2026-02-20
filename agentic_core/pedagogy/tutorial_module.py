from typing import Any, Dict, List

class TutorialModule:
    """
    Provides interactive tutorials that walk users through common workflows.
    """
    def __init__(self):
        self.active_tutorials = {}

    async def start_tutorial(self, user_id: str, tutorial_id: str) -> Dict[str, Any]:
        """Starts a guided tutorial."""
        tutorial_data = {
            "vqe_setup": ["Step 1: Define Hamiltonian", "Step 2: Choose Ansatz", "Step 3: Run Optimizer"],
            "collaborative_lab": ["Step 1: Create Workspace", "Step 2: Invite Alice", "Step 3: Merge Changes"]
        }

        steps = tutorial_data.get(tutorial_id, ["Welcome Step"])
        self.active_tutorials[user_id] = {"id": tutorial_id, "steps": steps, "current": 0}
        return {"step": steps[0], "total": len(steps)}

    async def advance_step(self, user_id: str) -> Dict[str, Any]:
        """Advances to the next step in the active tutorial."""
        session = self.active_tutorials.get(user_id)
        if not session:
            return {"error": "No active tutorial"}

        session["current"] += 1
        if session["current"] >= len(session["steps"]):
            return {"status": "completed"}

        return {"step": session["steps"][session["current"]], "progress": session["current"]}
