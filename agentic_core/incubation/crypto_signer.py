import logging
import hashlib
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class SigstoreSigner:
    """
    v60 Mastery: Sigstore Cryptographic Signing Simulator.
    Ensures all user approvals are cryptographically anchored.
    """
    def __init__(self):
        self.transparency_log = []

    def sign_approval(self, user_id: str, action: str, rationale: str) -> str:
        """Signs an approval and records it in the transparency log."""
        timestamp = datetime.now().isoformat()
        payload = {
            "user_id": user_id,
            "action": action,
            "rationale": rationale,
            "timestamp": timestamp
        }

        # SHA-384 data-dependent hashing (as mandated by Article H/Sigstore)
        signature = hashlib.sha384(json.dumps(payload, sort_keys=True).encode()).hexdigest()

        bundle = {
            "payload": payload,
            "signature": f"sigstore:{signature}"
        }

        self.transparency_log.append(bundle)
        logger.info(f"ACTION SIGNED: {action} by {user_id} [{signature[:8]}...]")

        return signature

    def verify_bundle(self, bundle: dict) -> bool:
        payload = bundle.get("payload")
        signature = bundle.get("signature", "").replace("sigstore:", "")
        expected = hashlib.sha384(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return signature == expected
