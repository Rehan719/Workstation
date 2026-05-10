"""
EternalImmutabilityGuard – Locks core constitutional invariants permanently.
"""
from typing import Dict, Any, List, Optional
import yaml
import os
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger

class EternalImmutabilityGuard:
    def __init__(self, ueg_logger: Any, genome_path: str = "config/immutable_genome.yaml"):
        self.ueg = ueg_logger
        self.immutable_articles: List[int] = []
        if os.path.exists(genome_path):
            with open(genome_path, "r") as f:
                data = yaml.safe_load(f)
                self.immutable_articles = data.get("immutable_articles", [])

    async def validate_amendment(self, proposed_changes: List[int]) -> bool:
        """
        Rejects any amendment that attempts to touch eternally locked articles.
        """
        for article in proposed_changes:
            if article in self.immutable_articles:
                await self.ueg.log_event(
                    "ETERNAL_IMMUTABILITY_VIOLATION",
                    {"article": article, "action": "AMENDMENT_REJECTED"}
                )
                return False # Hard rejection
        return True
