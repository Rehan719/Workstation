from typing import Dict, Any, List
import datetime

class PRDaemon:
    """
    L4 Meta-Cognitive Maintenance: Automatically suggests PRs based on evolutionary analysis.
    Mimics the interaction with GitHub API to proposal improvements.
    """
    def __init__(self):
        self.proposals_log = []

    async def propose_improvement(self, winning_gene: Dict[str, Any], rationale: str) -> Dict[str, Any]:
        """
        Creates a simulated Pull Request for a prompt or config update.
        """
        pr_id = f"PR-{int(datetime.datetime.now().timestamp())}"
        proposal = {
            "pr_id": pr_id,
            "title": f"Meta: Improve Prompt Performance (Ref: {winning_gene.get('gene_id', 'unknown')})",
            "body": f"Proposed change: {winning_gene.get('content')}\nRationale: {rationale}",
            "status": "open",
            "created_at": datetime.datetime.now().isoformat()
        }

        self.proposals_log.append(proposal)
        print(f"🚀 Autonomous PR Created: {proposal['title']}")

        return proposal

    def get_active_proposals(self) -> List[Dict[str, Any]]:
        return [p for p in self.proposals_log if p["status"] == "open"]
