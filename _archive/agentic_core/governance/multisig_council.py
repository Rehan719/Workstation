from typing import List, Dict, Any
from datetime import datetime

class MultiSigCouncil:
    """
    MultiSigCouncil quorum record for high-risk changes.
    Records proposals and votes cast through approve(). There is NO vote intake in this build —
    no route, CLI or UI collects a vote from RepoOwner, ConsciousEntity or ChiefEthicsOfficer —
    so request_approval never returns an approval on its own.
    """
    QUORUM = 2

    def __init__(self, ueg):
        self.ueg = ueg
        self.members = ["RepoOwner", "ConsciousEntity", "ChiefEthicsOfficer"]
        self.proposals = {} # In Firestore in real life

    async def request_approval(self, proposal: Dict[str, Any]) -> bool:
        proposal_id = proposal.get("id", "prop_" + str(datetime.utcnow().timestamp()))
        # W415 — this recorded {"approvals": [], "status": "PENDING"} and then immediately called
        # auto_evaluate_simulated(), which cast the quorum itself — approve(pid, "RepoOwner") and
        # approve(pid, "ChiefEthicsOfficer") — flipping the record to
        # {"approvals": ["RepoOwner", "ChiefEthicsOfficer"], "status": "APPROVED"} and returning
        # True. The caller (agentic_core/genetic_immune/regulator.py:15, which routes every
        # proposal with risk_score > 0.7 here) and the stored artifact both read as a high-risk
        # change approved by a named two-of-three human quorum including the repo owner and the
        # Chief Ethics Officer. No human was asked, and nothing in the record distinguished it
        # from a genuinely voted one. Nothing in this build can collect those votes, so the
        # honest answer to "did the quorum approve this?" is no — not yet — and a high-risk
        # proposal is now withheld rather than self-certified.
        self.proposals[proposal_id] = {
            "proposal": proposal,
            "approvals": [],
            "status": "PENDING_HUMAN_QUORUM",
            "quorum_required": self.QUORUM,
            "vote_intake": "NOT_IMPLEMENTED",
            "note": ("No route, CLI or UI in this build collects a council vote. This proposal is "
                     "recorded as pending and is NOT approved; approve() must be called with a "
                     "real member decision before the quorum is met."),
        }

        if self.ueg:
            await self.ueg.log("PENDING_APPROVAL", proposal_id=proposal_id, members=self.members)

        return await self.auto_evaluate_simulated(proposal_id)

    async def approve(self, proposal_id: str, member: str) -> bool:
        if proposal_id in self.proposals and member in self.members:
            if member not in self.proposals[proposal_id]["approvals"]:
                self.proposals[proposal_id]["approvals"].append(member)

            if len(self.proposals[proposal_id]["approvals"]) >= self.QUORUM:
                self.proposals[proposal_id]["status"] = "APPROVED"
                return True
        return False

    async def auto_evaluate_simulated(self, proposal_id: str) -> bool:
        # W415 — this body was:
        #     await self.approve(proposal_id, "RepoOwner")
        #     await self.approve(proposal_id, "ChiefEthicsOfficer")
        #     return self.proposals[proposal_id]["status"] == "APPROVED"
        # i.e. the council voted for itself in two named people's names. The method is kept
        # (request_approval calls it) but it no longer casts anyone's vote: it reports the real
        # tally. Only approvals recorded through approve() by a genuine member decision count,
        # and there is no vote intake in this build, so this returns False.
        record = self.proposals.get(proposal_id)
        if not record:
            return False
        return len(record["approvals"]) >= self.QUORUM and record["status"] == "APPROVED"
