from typing import List, Dict, Any
from datetime import datetime
import asyncio
import sys

class MultiSigCouncil:
    """
    Simulated MultiSigCouncil for high-risk changes.
    Logs to UEG and requires quorum from simulated members.
    """
    def __init__(self, ueg):
        self.ueg = ueg
        self.members = ["RepoOwner", "ConsciousEntity", "ChiefEthicsOfficer"]
        self.proposals = {}

    async def request_approval(self, proposal: Dict[str, Any]) -> bool:
        proposal_id = proposal.get("id", "prop_" + str(datetime.utcnow().timestamp()))
        self.proposals[proposal_id] = {
            "proposal": proposal,
            "approvals": [],
            "status": "PENDING"
        }

        if self.ueg:
            await self.ueg.log_event("PENDING_APPROVAL", {"proposal_id": proposal_id, "members": self.members})

        # Refinement: Wait for user input if in interactive mode, else auto-evaluate for CI
        if sys.stdin.isatty():
             print(f"\n[MultiSigCouncil] High-risk proposal {proposal_id} pending.")
             print(f"Details: {proposal}")
             user_choice = input("Approve this proposal? (y/n): ")
             if user_choice.lower() == 'y':
                 await self.approve(proposal_id, "RepoOwner")
                 await self.approve(proposal_id, "ConsciousEntity")
        else:
             # Auto-evaluate simulated for CI/Headless
             return await self.auto_evaluate_simulated(proposal_id)

        return self.proposals[proposal_id]["status"] == "APPROVED"

    async def approve(self, proposal_id: str, member: str) -> bool:
        if proposal_id in self.proposals and member in self.members:
            if member not in self.proposals[proposal_id]["approvals"]:
                self.proposals[proposal_id]["approvals"].append(member)

            if len(self.proposals[proposal_id]["approvals"]) >= 2:
                self.proposals[proposal_id]["status"] = "APPROVED"
                return True
        return False

    async def auto_evaluate_simulated(self, proposal_id: str) -> bool:
        # For vΩ∞-MASTER implementation, we simulate two approvals
        await self.approve(proposal_id, "RepoOwner")
        await self.approve(proposal_id, "ChiefEthicsOfficer")
        return self.proposals[proposal_id]["status"] == "APPROVED"
