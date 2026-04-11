import logging
import hashlib
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RuntimeAttestationManager:
    """
    Ensures MJM engine code and state haven't been tampered with at runtime.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir
        self.baseline_hashes: Dict[str, str] = {}

    def capture_baseline(self, file_paths: List[str]):
        """Records initial hashes of critical modules."""
        for path in file_paths:
            full_path = os.path.join(self.root_dir, path)
            if os.path.exists(full_path):
                self.baseline_hashes[path] = self._compute_hash(full_path)
        logger.info(f"RuntimeAttestation: Baseline captured for {len(self.baseline_hashes)} files")

    async def verify_code_integrity(self) -> Dict[str, Any]:
        """Compares current file hashes against baseline."""
        violations = []
        for path, baseline in self.baseline_hashes.items():
            full_path = os.path.join(self.root_dir, path)
            if not os.path.exists(full_path):
                violations.append({"path": path, "reason": "file_missing"})
                continue

            current_hash = self._compute_hash(full_path)
            if current_hash != baseline:
                violations.append({"path": path, "reason": "hash_mismatch"})

        status = "verified" if not violations else "compromised"
        if status == "compromised":
            logger.error(f"RuntimeAttestation: Integrity violation detected! {violations}")

        return {
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "violations": violations
        }

    def _compute_hash(self, filepath: str) -> str:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
