import uuid
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Tuple, Union, Optional, Dict, Any

class ContributionEntry:
    def __init__(self, agent_id: str, action: str, timestamp: str = None, reason: Optional[str] = None):
        self.agent_id = agent_id
        self.action = action  # "create", "modify", "approve", "refine", "sign"
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        self.reason = reason

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "action": self.action,
            "timestamp": self.timestamp,
            "reason": self.reason
        }

class ScholarlyObject:
    """
    ARTICLE 98: Universal Provenance & FAIR Intelligence.
    Wraps digital artifacts with an immutable audit trail.
    """
    def __init__(self, obj_type: str, content: Union[str, bytes], created_by: str,
                 derived_from: Optional[List[str]] = None):
        self.id = str(uuid.uuid4())
        self.type = obj_type
        self.content = content
        self.created_by = created_by
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.modified_by: List[Dict[str, str]] = []
        self.derived_from = derived_from or []
        self.ledger = [ContributionEntry(created_by, "create").to_dict()]
        self.signature: Optional[str] = None

    def add_contribution(self, agent_id: str, action: str, reason: str = ""):
        entry = ContributionEntry(agent_id, action, reason=reason)
        self.ledger.append(entry.to_dict())
        if action == "modify":
            self.modified_by.append({"agent_id": agent_id, "timestamp": entry.timestamp})

    def sign(self, signer_id: str):
        """Simulates cryptographic signing (e.g. OpenTimestamps/Sigstore)."""
        data_to_sign = self._get_signing_data()
        self.signature = hashlib.sha256(json.dumps(data_to_sign, sort_keys=True).encode()).hexdigest()
        self.add_contribution(signer_id, "sign", reason=f"Hash: {self.signature}")

    def _get_signing_data(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "derived_from": self.derived_from,
            "ledger": self.ledger,
            "content_hash": hashlib.sha256(self.content if isinstance(self.content, bytes) else self.content.encode()).hexdigest()
        }

    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "type": self.type,
            "content": self.content.decode('utf-8') if isinstance(self.content, bytes) else self.content,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "ledger": self.ledger,
            "signature": self.signature
        }, indent=2)
