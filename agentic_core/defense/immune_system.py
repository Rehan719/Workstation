import hashlib
from typing import List, Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class ImmuneDefense:
    """
    Lymphatic-Immune Defence.
    Uses VDJ recombination to generate unique antibody-like detectors for rogue agents.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.antibody_repertoire: List[str] = []

    async def vdj_recombine(self, segments: List[str]) -> str:
        """Combinatorially generate a unique threat detector."""
        raw = "".join(segments)
        antibody = hashlib.sha3_256(raw.encode()).hexdigest()
        self.antibody_repertoire.append(antibody)
        await self.ueg.log_minimisation_event("immune_antibody_generated", {"repertoire_size": len(self.antibody_repertoire)})
        return antibody

    async def scan_agent_activity(self, agent_id: str, activity_blob: Dict[str, Any]) -> bool:
        """Scan activity for patterns matching the antibody repertoire."""
        blob_hash = hashlib.sha3_256(str(activity_blob).encode()).hexdigest()
        is_threat = any(blob_hash.startswith(ab[:8]) for ab in self.antibody_repertoire)

        if is_threat:
            await self.ueg.log_minimisation_event("immune_threat_detected", {"agent": agent_id})

        return is_threat
