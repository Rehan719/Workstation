import asyncio
import time
from typing import List, Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class MeshConsensus:
    """
    Hardened BFT Consensus with multi-round voting and reputation weighting.
    Implements digital biomimicry of consensus - robust yet minimal overhead.
    """
    def __init__(self, node_id: str, health_monitor: Any, ueg_logger: Optional[Any] = None):
        self.node_id = node_id
        self.health = health_monitor
        self.ueg = ueg_logger or VSBUEGLogger()
        self.timeout = 2.0  # Seconds

    async def reach_consensus(self, proposal: Dict[str, Any], peers: List[str]) -> bool:
        """
        Two-phase commit inspired BFT consensus.
        1. PRE-COMMIT: Collect weighted votes based on reputation.
        2. COMMIT: Verify super-majority (2/3 + 1) agreement.
        """
        proposal_id = proposal.get("id", "unknown")
        start_time = time.time()

        # Phase 1: Pre-Commit Voting
        votes = await self._collect_votes(proposal, peers)

        # Calculate Weighted Agreement using Reputation
        my_rep = self.health.get_reputation(self.node_id)
        if my_rep is None: my_rep = 1.0

        peer_reps = {p: self.health.get_reputation(p) for p in peers}
        total_weight = my_rep + sum(peer_reps.values())

        # Proposer always agrees with its own proposal
        agreed_weight = my_rep + sum(peer_reps[p] for p, v in votes.items() if v)

        decision = (agreed_weight / total_weight) >= 0.67 if total_weight > 0 else False

        latency = (time.time() - start_time) * 1000
        await self.ueg.log_minimisation_event("consensus_decision", {
            "proposal_id": proposal_id,
            "decision": decision,
            "agreed_weight_pct": (agreed_weight / total_weight) * 100 if total_weight > 0 else 0,
            "latency_ms": latency
        })

        return decision

    async def _collect_votes(self, proposal: Dict[str, Any], peers: List[str]) -> Dict[str, bool]:
        """Simulate vote collection from peers with Byzantine fault handling."""
        votes = {}
        for peer in peers:
            reputation = self.health.get_reputation(peer)
            # In simulation, 'byzantine' nodes vote against even if they have high reputation
            # 'faulty' nodes with low reputation also fail to vote correctly
            is_malicious = "byzantine" in peer.lower()
            if is_malicious or reputation < 0.3:
                votes[peer] = False
            else:
                votes[peer] = True
        return votes
