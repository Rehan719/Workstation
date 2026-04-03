import json
from datetime import datetime
import uuid
import os

class SourceValidationDAO:
    def __init__(self, ledger_manager):
        self.ledger_manager = ledger_manager
        self.proposals_path = "knowledge/Religion/QuranEducation/dao/source_proposals.json"
        self.ensure_proposals_exist()

    def ensure_proposals_exist(self):
        if not os.path.exists(self.proposals_path):
            with open(self.proposals_path, 'w') as f:
                json.dump({"proposals": []}, f, indent=2)

    def submit_source_proposal(self, user_id, source_url, description):
        proposal = {
            "id": f"prop-{uuid.uuid4().hex[:8]}",
            "proposer": user_id,
            "source_url": source_url,
            "description": description,
            "status": "pending",
            "timestamp": str(datetime.now()),
            "votes": {
                "approve": 0,
                "reject": 0
            },
            "voting_deadline": str(datetime.now()) # In a real system, this would be set to a future date
        }
        with open(self.proposals_path, 'r') as f:
            data = json.load(f)
        data["proposals"].append(proposal)
        with open(self.proposals_path, 'w') as f:
            json.dump(data, f, indent=2)
        return proposal

    def cast_vote(self, user_id, proposal_id, vote_type):
        # Weighted voting based on QEP-SOURCE-TOKEN balance
        token_balance = self.ledger_manager.get_balance(user_id, "QEP-SOURCE-TOKEN")
        if token_balance <= 0:
            return {"success": False, "reason": "Insufficient QEP-SOURCE-TOKEN balance"}

        with open(self.proposals_path, 'r') as f:
            data = json.load(f)

        for proposal in data["proposals"]:
            if proposal["id"] == proposal_id:
                if proposal["status"] != "pending":
                    return {"success": False, "reason": "Voting closed for this proposal"}

                # Simple weight multiplication for simulation
                weight = token_balance * 10
                proposal["votes"][vote_type] += weight

                # Check for consensus threshold
                if proposal["votes"]["approve"] > 100: # Mock threshold
                    proposal["status"] = "approved"
                    self.ledger_manager.update_reputation(proposal["proposer"], 10)
                elif proposal["votes"]["reject"] > 100:
                    proposal["status"] = "rejected"
                    self.ledger_manager.update_reputation(proposal["proposer"], -5)

                with open(self.proposals_path, 'w') as f:
                    json.dump(data, f, indent=2)
                return {"success": True, "status": proposal["status"]}

        return {"success": False, "reason": "Proposal not found"}
