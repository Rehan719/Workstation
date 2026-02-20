import hashlib
import hmac
from typing import Any, Dict, List, Optional
import os

class SecureTaskMemory:
    """
    Article: Ensuring Robustness, Security, and Reliability in Autonomous Operations.
    Prevents 'plan injection' attacks via strict isolation and integrity guarantees.
    """
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key
        self.memory: Dict[str, Dict[str, Any]] = {}

    def store_plan(self, project_id: str, plan: List[Dict[str, Any]]):
        """
        Stores a plan with a cryptographic signature.
        """
        plan_data = str(plan).encode()
        signature = hmac.new(self.secret_key, plan_data, hashlib.sha256).hexdigest()
        self.memory[project_id] = {
            "plan": plan,
            "signature": signature
        }

    def verify_and_retrieve_plan(self, project_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieves a plan only if the signature is valid.
        """
        entry = self.memory.get(project_id)
        if not entry:
            return None

        plan = entry["plan"]
        stored_signature = entry["signature"]

        plan_data = str(plan).encode()
        actual_signature = hmac.new(self.secret_key, plan_data, hashlib.sha256).hexdigest()

        if hmac.compare_digest(stored_signature, actual_signature):
            return plan
        else:
            raise SecurityError(f"Plan integrity violation detected for project {project_id}!")

class SecurityError(Exception):
    pass
