import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class EpistemicState(BaseModel):
    domain_id: str
    known_facts: List[str] = Field(default_factory=list)
    uncertainty_areas: List[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EpistemicStateTracker:
    """
    Tracks what the MJM engine knows, doesn't know, and how confident it is.
    """

    def __init__(self):
        self.states: Dict[str, EpistemicState] = {}

    def update_state(self, domain_id: str, new_knowledge: List[str], uncertainties: List[str]):
        """Updates the epistemic state for a specific domain."""
        if domain_id not in self.states:
            self.states[domain_id] = EpistemicState(domain_id=domain_id)

        state = self.states[domain_id]
        state.known_facts = list(set(state.known_facts + new_knowledge))
        state.uncertainty_areas = list(set(state.uncertainty_areas + uncertainties))
        state.last_updated = datetime.now(timezone.utc)

        logger.info(f"EpistemicTracker: Updated {domain_id}. Facts: {len(state.known_facts)}, Uncertainties: {len(state.uncertainty_areas)}")

    def get_summary(self, domain_id: str) -> Dict[str, Any]:
        """Returns a summary of the epistemic state for a domain."""
        state = self.states.get(domain_id, EpistemicState(domain_id=domain_id))
        return {
            "total_facts": len(state.known_facts),
            "total_uncertainties": len(state.uncertainty_areas),
            "last_synapse": state.last_updated.isoformat(),
            "recommended_research": state.uncertainty_areas[:3]
        }
