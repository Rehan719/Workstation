import asyncio
from typing import Dict, Any, List, Optional
from agentic_core.mesh.negotiation.treaty_negotiation import TreatyNegotiator
from agentic_core.mesh.negotiation.jurisdiction_routing import JurisdictionRouter
from agentic_core.ueg.logger import VSBUEGLogger

class StreamNegotiator:
    """
    Asynchronous stream-based negotiation for high-throughput treaty exchange.
    Optimises for minimal connection overhead (Biomimetic Efficiency) with Legal Precision.
    """
    def __init__(self, node_id: str, negotiator: TreatyNegotiator, router: JurisdictionRouter, ueg_logger: Optional[Any] = None):
        self.node_id = node_id
        self.negotiator = negotiator
        self.router = router
        self.ueg = ueg_logger or VSBUEGLogger()
        self.active_streams: Dict[str, asyncio.Queue] = {}

    async def open_negotiation_stream(self, peer_id: str):
        self.active_streams[peer_id] = asyncio.Queue()
        await self.ueg.log_minimisation_event("negotiation_stream_opened", {"peer": peer_id})

    async def send_intent(self, peer_id: str, intent: Dict[str, Any]):
        if peer_id not in self.active_streams:
            await self.open_negotiation_stream(peer_id)

        # Legal check before sending
        if not self.router.validate_treaty_legal_bounds([intent]):
            await self.ueg.log_minimisation_event("intent_blocked_legal", {"peer": peer_id, "intent_id": intent.get("id")})
            return

        await self.active_streams[peer_id].put(intent)
        await self.ueg.log_minimisation_event("intent_stream_sent", {"peer": peer_id, "intent_id": intent.get("id")})

    async def process_incoming_negotiations(self, peer_id: str):
        """Consume intents and trigger negotiation cycles with legal filtering."""
        queue = self.active_streams.get(peer_id)
        if not queue: return

        intents_to_negotiate = []
        while not queue.empty():
            peer_intent = await queue.get()
            if self.router.validate_treaty_legal_bounds([peer_intent]):
                intents_to_negotiate.append(peer_intent)
            else:
                await self.ueg.log_minimisation_event("incoming_intent_blocked_legal", {"peer": peer_id, "intent_id": peer_intent.get("id")})

        if intents_to_negotiate:
            my_intents = [{"id": "local_1", "profile": [0.8, 0.2]}]
            result = await self.negotiator.negotiate(my_intents, intents_to_negotiate)
            await self.ueg.log_minimisation_event("stream_negotiation_cycle_complete", {
                "peer": peer_id,
                "wasserstein": result["wasserstein"],
                "terms_count": len(result["terms"])
            })
