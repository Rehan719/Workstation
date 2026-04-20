import asyncio
from typing import List, Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class AICouncilSimulator:
    """
    AI-simulated MultiSigCouncil with weighted voting based on expertise and reputation.
    """
    def __init__(self, members: List[Dict[str, Any]], ueg_logger: Optional[Any] = None):
        self.members = members # e.g. [{"id": "CLO", "expertise": 1.0, "reputation": 0.9}]
        self.ueg = ueg_logger or VSBUEGLogger()

    async def vote_on_amendment(self, proposal: Dict[str, Any], timeout_sec: float = 10.0) -> Dict[str, Any]:
        votes = []
        for member in self.members:
            # Simulate voting logic: higher KL divergence (risk) might lead to Rejection
            risk = proposal.get("sb_kl_divergence", 0.0)
            if risk > 5.0 and member["id"] == "CLO":
                vote = False # Legal Officer rejects high-risk amendment
            else:
                vote = True
            votes.append({"member": member["id"], "vote": vote, "weight": member["expertise"] * member["reputation"]})

        total_weight = sum(v["weight"] for v in votes)
        approve_weight = sum(v["weight"] for v in votes if v["vote"])

        decision = (approve_weight / total_weight) >= 0.67 if total_weight > 0 else False

        result = {
            "amendment_id": proposal.get("id"),
            "approved": decision,
            "approve_weight_pct": (approve_weight / total_weight) * 100 if total_weight > 0 else 0,
            "votes": votes
        }

        await self.ueg.log_minimisation_event("council_vote_complete", result)
        return result
