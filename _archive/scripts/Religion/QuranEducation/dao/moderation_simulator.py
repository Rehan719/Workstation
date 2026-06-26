import json
from datetime import datetime
import uuid
import os

class ModerationDAO:
    def __init__(self, ledger_manager):
        self.ledger_manager = ledger_manager
        self.moderation_path = "knowledge/Religion/QuranEducation/dao/moderation_proposals.json"
        self.ensure_moderation_exists()

    def ensure_moderation_exists(self):
        if not os.path.exists(self.moderation_path):
            with open(self.moderation_path, 'w') as f:
                json.dump({"proposals": []}, f, indent=2)

    def submit_moderation_proposal(self, user_id, content_id, moderation_action, reason):
        proposal = {
            "id": f"mod-{uuid.uuid4().hex[:8]}",
            "moderator": user_id,
            "content_id": content_id,
            "moderation_action": moderation_action,
            "reason": reason,
            "status": "pending",
            "timestamp": str(datetime.now()),
            "votes": {
                "approve": 0,
                "reject": 0
            },
            "voting_deadline": str(datetime.now()) # Mock deadline
        }
        with open(self.moderation_path, 'r') as f:
            data = json.load(f)
        data["proposals"].append(proposal)
        with open(self.moderation_path, 'w') as f:
            json.dump(data, f, indent=2)
        return proposal

    def cast_vote(self, user_id, proposal_id, vote_type):
        # Weighted voting based on QEP-MOD-TOKEN balance
        token_balance = self.ledger_manager.get_balance(user_id, "QEP-MOD-TOKEN")
        if token_balance <= 0:
            return {"success": False, "reason": "Insufficient QEP-MOD-TOKEN balance"}

        with open(self.moderation_path, 'r') as f:
            data = json.load(f)

        for proposal in data["proposals"]:
            if proposal["id"] == proposal_id:
                if proposal["status"] != "pending":
                    return {"success": False, "reason": "Voting closed for this proposal"}

                # Reputation-weighted voting (Simulation)
                reputation = self.ledger_manager.get_reputation(user_id)
                weight = token_balance + (reputation / 10)
                proposal["votes"][vote_type] += weight

                # Check for consensus threshold
                if proposal["votes"]["approve"] > 50: # Mock threshold
                    proposal["status"] = "approved"
                    self.ledger_manager.update_reputation(user_id, 2)
                    self.ledger_manager.issue_token(user_id, "QEP-MOD-TOKEN", 1) # Reward for good moderation
                elif proposal["votes"]["reject"] > 50:
                    proposal["status"] = "rejected"
                    self.ledger_manager.update_reputation(user_id, -1) # Penalty for poor moderation

                with open(self.moderation_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return {"success": True, "status": proposal["status"]}

        return {"success": False, "reason": "Proposal not found"}
