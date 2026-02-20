from typing import Any, Dict, Optional
import hashlib
import json
from datetime import datetime

class SigstoreHandler:
    """
    Article V: The Cryptographic Trust Layer.
    Integration with Sigstore for supply chain security.
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.rekor_log = [] # Mock transparency log

    async def sign_container(self, image_path: str, user_identity: str) -> Dict[str, Any]:
        """Sign a container image using Sigstore's key-less model (Mocked)."""
        timestamp = datetime.utcnow().isoformat()
        signature_data = f"{image_path}:{user_identity}:{timestamp}"
        signature = hashlib.sha256(signature_data.encode()).hexdigest()

        entry = {
            'image': image_path,
            'identity': user_identity,
            'signature': signature,
            'timestamp': timestamp,
            'rekor_id': hashlib.md5(signature.encode()).hexdigest()
        }
        self.rekor_log.append(entry)

        return entry

    async def verify_signature(self, image_path: str, signature_entry: Dict[str, Any]) -> bool:
        """Verify a container signature against Rekor."""
        # Check if entry exists in log
        for entry in self.rekor_log:
            if entry['image'] == image_path and entry['signature'] == signature_entry.get('signature'):
                return True
        return False

    async def enforce_policy(self, image_path: str, signature_entry: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Enforce image policy before allowing execution."""
        if not signature_entry:
            return {'allowed': False, 'reason': 'All containers must be signed and verified'}

        verified = await self.verify_signature(image_path, signature_entry)
        if verified:
            return {'allowed': True}
        else:
            return {'allowed': False, 'reason': 'Invalid or missing signature in transparency log'}
