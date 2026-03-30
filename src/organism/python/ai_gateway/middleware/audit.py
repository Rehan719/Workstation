import json
import hashlib
import time
from typing import Dict, Any, Optional
from src.organism.python.core.governance import SovereignAuditLog

class AIAuditMiddleware:
    """
    Extends SovereignAuditLog with AI-specific event logging for
    tribunal-admissible evidence chains.
    """
    def __init__(self, base_audit: SovereignAuditLog):
        self.base_audit = base_audit

    async def log_ai_action(
        self,
        action: str,
        payload: Dict[str, Any],
        provider: str,
        approval_token: Optional[str] = None
    ):
        """
        SHA-256 chain + human approval signature + timestamp + provider metadata.
        """
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

        entry = {
            "id": f"AI-{int(time.time()*1000)}",
            "type": "AI_ACTION",
            "action": action,
            "provider": provider,
            "payload_hash": payload_hash,
            "approval_token": approval_token,
            "metadata": {
                "lib": "SovereignAIGateway v1.0",
                "evidence_standard": "UK_EMPLOYMENT_TRIBUNAL_READY"
            }
        }

        # Log to the base hash-chained ledger
        self.base_audit.log_entry(entry)
        return entry
