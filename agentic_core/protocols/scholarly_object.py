import uuid
import hashlib
import json
from datetime import datetime, timezone
from typing import List, Tuple, Union, Optional, Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

class ContributionEntry(json.JSONEncoder):
    def __init__(self, agent_id: str, action: str, timestamp: datetime, reason: Optional[str] = None):
        self.agent_id = agent_id
        self.action = action  # "create", "modify", "approve", "refine"
        self.timestamp = timestamp
        self.reason = reason

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "action": self.action,
            "timestamp": self.timestamp.isoformat(),
            "reason": self.reason
        }

class ScholarlyObject:
    """
    v47.0: Represents an atomic unit of intellectual value with an immutable provenance ledger
    and blockchain anchoring (Article AT).
    """
    def __init__(self, obj_type: str, content: Union[str, bytes], created_by: str,
                 derived_from: Optional[List[str]] = None):
        self.id = str(uuid.uuid4())
        self.type = obj_type
        self.content = content
        self.created_by = created_by
        self.created_at = datetime.now(timezone.utc)
        self.modified_by: List[Tuple[str, datetime]] = []
        self.derived_from = derived_from or []
        self.ledger = [ContributionEntry(created_by, "create", self.created_at).to_dict()]
        self.signature: Optional[str] = None
        self.blockchain_receipt: Optional[Dict[str, Any]] = None

    def anchor(self, receipt: Dict[str, Any]):
        """
        v47.0: Attaches a blockchain anchor receipt (IPFS CID, TX Hash).
        """
        self.blockchain_receipt = receipt
        self.ledger.append(ContributionEntry("blockchain", "anchored", datetime.now(timezone.utc)).to_dict())

    def modify(self, new_content: Union[str, bytes], agent_id: str, reason: str = ""):
        self.content = new_content
        now = datetime.now(timezone.utc)
        self.modified_by.append((agent_id, now))
        self.ledger.append(ContributionEntry(agent_id, "modify", now, reason).to_dict())
        self.signature = None  # Invalidate signature
        self.blockchain_receipt = None # Anchoring needs to be redone for new content

    def get_signing_data(self) -> bytes:
        obj_dict = {
            "id": self.id,
            "type": self.type,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "ledger": self.ledger,
            "content_hash": hashlib.sha256(self.content if isinstance(self.content, bytes) else self.content.encode()).hexdigest()
        }
        return json.dumps(obj_dict, sort_keys=True).encode()

    def sign(self, private_key: rsa.RSAPrivateKey):
        """
        Signs the object using the provided RSA private key.
        """
        data = self.get_signing_data()
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.signature = signature.hex()

    def verify(self, public_key: rsa.RSAPublicKey) -> bool:
        """
        Verifies the object's signature using the provided RSA public key.
        """
        if not self.signature:
            return False

        data = self.get_signing_data()
        try:
            public_key.verify(
                bytes.fromhex(self.signature),
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
