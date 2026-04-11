import logging
import hashlib
import json
import hmac
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class AuthResult(BaseModel):
    status: str
    user_id: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)
    reason: Optional[str] = None
    session_id: Optional[str] = None

class ZeroTrustSecurityManager:
    """
    Enforces zero-trust principles across all MJM operations.
    1. Never trust, always verify.
    2. Least privilege access.
    3. Assume breach.
    """

    def __init__(self, secret_key: str = "sovereign-secret"):
        self.secret_key = secret_key
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.audit_log: List[Dict[str, Any]] = []

    async def authenticate_request(self, payload: Dict[str, Any], signature: str) -> AuthResult:
        """Verifies request signature and generates a session."""
        expected_sig = hmac.new(self.secret_key.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_sig, signature):
            logger.warning("ZeroTrust: Authentication failed - signature mismatch")
            return AuthResult(status="rejected", reason="signature_invalid")

        user_id = payload.get("user_id", "anonymous")
        session_id = hashlib.sha256(f"{user_id}:{datetime.now(timezone.utc).timestamp()}".encode()).hexdigest()[:16]

        self.sessions[session_id] = {
            "user_id": user_id,
            "permissions": ["execute_workflow", "read_intelligence"],
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=1)
        }

        self._log_event("authentication", {"user_id": user_id, "session_id": session_id, "status": "success"})
        return AuthResult(status="authenticated", user_id=user_id, session_id=session_id, permissions=self.sessions[session_id]["permissions"])

    async def authorize_operation(self, session_id: str, required_permission: str) -> bool:
        """Verifies if the session has the required permission."""
        session = self.sessions.get(session_id)
        if not session:
            return False

        if datetime.now(timezone.utc) > session["expires_at"]:
            del self.sessions[session_id]
            return False

        if required_permission in session["permissions"]:
            self._log_event("authorization", {"session_id": session_id, "permission": required_permission, "status": "allowed"})
            return True

        self._log_event("authorization", {"session_id": session_id, "permission": required_permission, "status": "denied"})
        return False

    def _log_event(self, event_type: str, data: Dict[str, Any]):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "data": data
        }
        self.audit_log.append(entry)
        logger.info(f"ZeroTrust Audit: {event_type} - {data}")
