import asyncio
import hashlib
from typing import Dict, Any

class ApprovalManager:
    """CO-VI: Manages conditional approval gates with transparent rationale."""

    async def request_approval(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        # In a real system, this would wait for user input on the dashboard
        # For simulation, we'll auto-approve with a mock signature
        rationale = f"Workflow '{workflow['type']}' requires oversight due to high semantic density."

        # Simulated user approval delay
        await asyncio.sleep(0.01)

        signature = hashlib.sha256(f"user_approved:{workflow['id']}".encode()).hexdigest()

        return {
            "status": "approved",
            "rationale": rationale,
            "signature": signature
        }
