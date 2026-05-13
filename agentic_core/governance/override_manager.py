import logging, json
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import ed25519

class OverrideManager:
    """
    CRYPTOGRAPHIC MIGRATION PATH (Constitutional Document):
    - Current: Ed25519 signature verification for Owner Veto
    - Target: Dilithium-5 (FIPS 204) post-quantum signatures
    - Trigger for migration: When python-oqs or equivalent is available
                             in the sovereign dependency tree, OR
                             when QBER monitoring detects quantum threat
                             elevation (>5% baseline deviation).
    - Backward compatibility: Ed25519 signatures remain valid indefinitely
      per Löb-stable fixpoint contract; Dilithium-5 will be added as
      additional verification path, not replacement.
    - UEG Log: Every override logs both signature type and migration status.
    """
    def __init__(self, ueg_logger=None):
        self.ueg, self.priv = ueg_logger, ed25519.Ed25519PrivateKey.generate()
        self.pub, self.did = self.priv.public_key(), "did:workstation:owner"

    async def request_override(self, action_id, violation):
        payload = {"message": "CONSTITUTIONAL_OVERRIDE", "action_id": action_id, "violation": violation, "timestamp": datetime.now(timezone.utc).isoformat(), "owner_did": self.did}
        if self.ueg: await self.ueg.log_minimisation_event("override_requested", payload)
        return payload

    def sign_override(self, payload): return self.priv.sign(json.dumps(payload, sort_keys=True).encode())

    async def apply_override(self, action_id, sig, payload):
        if payload.get("action_id") != action_id: return False
        try:
            self.pub.verify(sig, json.dumps(payload, sort_keys=True).encode())
            if self.ueg: await self.ueg.log_minimisation_event("override_applied", {"action_id": action_id, "sig_type": "ed25519", "migration": "pending_dilithium5"})
            return True
        except: return False
