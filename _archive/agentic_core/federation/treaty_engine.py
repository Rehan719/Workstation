import logging
import json
import time
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TreatyEngine:
    """
    ARTICLE 1012/1013: Treaty Framework v132.0.
    Handles negotiation, ratification, and enforcement of inter-republic treaties.
    """
    def __init__(self, owner_did: str):
        self.owner_did = owner_did
        self.active_treaties: Dict[str, Dict[str, Any]] = {}

    def propose_treaty(self, target_did: str, scope: List[str], duration_days: int = 30) -> Dict[str, Any]:
        """Creates a machine-readable JSON-LD treaty proposal."""
        treaty_id = f"treaty_{int(time.time())}_{target_did[-4:]}"

        proposal = {
            "@context": "https://workstation.ai/contexts/treaty",
            "id": treaty_id,
            "type": "SovereignTreaty",
            "parties": [self.owner_did, target_did],
            "scope": scope, # e.g. ["reactor_sharing", "research_collaboration"]
            "terms": {
                "start_date": time.time(),
                "end_date": time.time() + (duration_days * 86400),
                "secession_notice": "24h"
            },
            "status": "PROPOSED",
            "signatures": {}
        }

        logger.info(f"TreatyEngine: Proposed treaty {treaty_id} to {target_did} with scope {scope}")
        return proposal

    def ratify_treaty(self, proposal: Dict[str, Any], signature: str) -> bool:
        """Ratifies a treaty proposal with a cryptographic signature."""
        proposal["signatures"][self.owner_did] = signature
        proposal["status"] = "RATIFIED"

        self.active_treaties[proposal["id"]] = proposal
        logger.info(f"TreatyEngine: Treaty {proposal['id']} ratified and active.")
        return True

    def revoke_treaty(self, treaty_id: str):
        """
        ARTICLE 1013: Right of Secession.
        Unilaterally revokes a treaty with immediate effect.
        """
        if treaty_id in self.active_treaties:
            del self.active_treaties[treaty_id]
            logger.warning(f"TreatyEngine: Treaty {treaty_id} revoked via Right of Secession.")
        else:
            logger.error(f"TreatyEngine: Cannot revoke unknown treaty {treaty_id}")

    def list_active_treaties(self) -> List[Dict[str, Any]]:
        return list(self.active_treaties.values())
