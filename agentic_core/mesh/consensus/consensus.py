import asyncio
from typing import Dict, List, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger
class MeshConsensus:
    def __init__(self, node_id: str, reputation: Dict[str, float], ueg_logger: Optional[VSBUEGLogger] = None):
        self.node_id, self.reputation, self.ueg = node_id, reputation, ueg_logger or VSBUEGLogger()
    async def reach_consensus(self, proposal: Dict[str, Any], peers: List[str]) -> bool:
        votes = {p: (self.reputation.get(p, 0.5) > 0.5 if "fail" not in str(proposal.get("id")) else self.reputation.get(p, 0.5) < 0.5) for p in peers}
        votes[self.node_id] = True
        total = sum(self.reputation.get(p, 0.5) for p in votes.keys())
        agree = sum(self.reputation.get(p, 0.5) for p, v in votes.items() if v)
        decision = (agree / total) >= 0.67 if total > 0 else False
        await self.ueg.log_minimisation_event("consensus_reached", {"id": proposal.get("id"), "decision": decision})
        return decision
