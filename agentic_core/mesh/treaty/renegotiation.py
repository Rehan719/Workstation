import asyncio
from typing import Dict, Any, List, Optional
from agentic_core.mesh.ledger.treaty_ledger import TreatyLedger
from agentic_core.mesh.negotiation.treaty_negotiation import TreatyNegotiator
from agentic_core.ueg.logger import VSBUEGLogger

class AutonomousRenegotiator:
    """
    Performance-driven autonomous treaty updates.
    Ensures treaties evolve with the organism's needs.
    """
    def __init__(self, node_id: str, ledger: TreatyLedger, negotiator: TreatyNegotiator, ueg_logger: Optional[Any] = None):
        self.node_id = node_id
        self.ledger = ledger
        self.negotiator = negotiator
        self.ueg = ueg_logger or VSBUEGLogger()

    async def renegotiate_if_needed(self, treaty_id: str, performance_delta: float) -> bool:
        """
        Evaluate performance and trigger renegotiation if deviation exceeds tolerance.
        """
        if treaty_id not in self.ledger.treaties:
            return False

        treaty = self.ledger.treaties[treaty_id]

        if abs(performance_delta) < 0.05:
            return False

        await self.ueg.log_minimisation_event("renegotiation_started", {"treaty_id": treaty_id, "delta": performance_delta})

        new_intents = [{"id": "updated_intent", "profile": [0.9, 0.1]}]
        peer_intents = [{"id": "peer_intent", "profile": [0.1, 0.9]}]

        negotiation_result = await self.negotiator.negotiate(new_intents, peer_intents)

        treaty["terms"] = negotiation_result["terms"]
        treaty["status"] = "renegotiated"

        await self.ueg.log_minimisation_event("renegotiation_complete", {
            "treaty_id": treaty_id,
            "wasserstein": negotiation_result["wasserstein"]
        })
        return True
