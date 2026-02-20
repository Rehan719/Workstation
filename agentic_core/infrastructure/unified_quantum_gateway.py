from typing import Any, Dict, Optional
from ..security.sigstore_handler import SigstoreHandler

class UnifiedQuantumGateway:
    """
    Unified entry point for quantum backend access.
    Enforces Sigstore signature verification for all hybrid workloads (Article V).
    """
    def __init__(self):
        self.sigstore = SigstoreHandler()

    async def submit_job(self, circuit: Any, container_info: Dict[str, Any]) -> str:
        """Submit a quantum job with mandatory signature verification."""
        image_path = container_info.get('image_path')
        signature = container_info.get('signature')

        # Enforce policy
        policy_check = await self.sigstore.enforce_policy(image_path, signature)
        if not policy_check['allowed']:
            raise PermissionError(f"Job submission rejected: {policy_check['reason']}")

        # Proceed with submission (Mocked)
        job_id = f"job-{hash(str(circuit))}"
        return job_id
