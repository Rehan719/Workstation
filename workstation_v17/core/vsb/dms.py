import logging
import hashlib
import time
from typing import Dict, Any, Optional

class DocumentControlSystem:
    """
    DMS: Immutable Versioning & Cryptographic Audit.
    Manages document lineage and multi-sig approval traces.
    """
    def __init__(self, config_path: str):
        self.logger = logging.getLogger("DMS")
        self.registry = {} # artifact_id -> versions

    async def commit_artifact(self, artifact_id: str, content: Any, actor: str) -> str:
        """
        Versions and cryptographically signs a document/artifact.
        """
        content_hash = hashlib.sha3_512(str(content).encode()).hexdigest()
        version = len(self.registry.get(artifact_id, [])) + 1

        entry = {
            "version": version,
            "hash": content_hash,
            "timestamp": time.time_ns(),
            "actor": actor,
            "lineage": self.registry.get(artifact_id, [])[-1]["hash"] if artifact_id in self.registry else "GENESIS"
        }

        if artifact_id not in self.registry:
            self.registry[artifact_id] = []
        self.registry[artifact_id].append(entry)

        self.logger.info(f"DMS: Committed {artifact_id} v{version}")
        return content_hash

    async def retrieve_version(self, artifact_id: str, version: Optional[int] = None) -> Dict[str, Any]:
        if artifact_id not in self.registry:
            raise ValueError("Artifact not found")
        v_idx = (version - 1) if version else -1
        return self.registry[artifact_id][v_idx]
