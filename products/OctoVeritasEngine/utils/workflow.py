import os
import json
import time
from typing import Dict, Any, Optional

class WorkflowCollaborator:
    """
    Implements multi-stakeholder workflows with optimistic lock/merge.
    """
    def __init__(self, workspace_dir: str = "outputs/workspace"):
        self.workspace_dir = workspace_dir
        os.makedirs(self.workspace_dir, exist_ok=True)

    def start_edit(self, recipe_id: str, user_id: str) -> bool:
        lock_path = os.path.join(self.workspace_dir, f"{recipe_id}.lock")
        if os.path.exists(lock_path):
            with open(lock_path, "r") as f:
                lock_data = json.load(f)

            # If lock is older than 5 mins, force override
            if time.time() - lock_data["timestamp"] > 300:
                print(f"Lock for {recipe_id} expired. Force override by {user_id}.")
            elif lock_data["user"] != user_id:
                return False

        with open(lock_path, "w") as f:
            json.dump({"user": user_id, "timestamp": time.time()}, f)
        return True

    def save_recipe(self, recipe_id: str, user_id: str, content: Dict[str, Any]) -> bool:
        lock_path = os.path.join(self.workspace_dir, f"{recipe_id}.lock")
        if not os.path.exists(lock_path):
            return False

        with open(lock_path, "r") as f:
            lock_data = json.load(f)

        if lock_data["user"] != user_id:
            return False

        recipe_path = os.path.join(self.workspace_dir, f"{recipe_id}.json")
        with open(recipe_path, "w") as f:
            json.dump(content, f)

        # Release lock
        os.remove(lock_path)
        return True

    def get_recipe(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        path = os.path.join(self.workspace_dir, f"{recipe_id}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return None
