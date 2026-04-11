from typing import List, Dict, Any
from ..core.models import ProposalPackage

class GitHubWorkflowAdapter:
    """
    Adapter for generating GitHub-native async collaboration workflows.
    Produces scripts and templates for user execution.
    """

    def __init__(self, repo_url: str = "https://github.com/Rehan719/Workstation"):
        self.repo_url = repo_url

    def generate_workflow_bundle(self, proposal: ProposalPackage, contributor: str) -> Dict[str, Any]:
        """
        Generates a bundle of git commands and PR templates for a proposal.
        """
        timestamp = int(proposal.analysis_ref.split(".")[0]) if "." in proposal.analysis_ref else "now"
        branch_name = f"mjm/proposal-{timestamp}"

        return {
            "branch": branch_name,
            "git_commands": [
                f"git checkout -b {branch_name}",
                f"cp outputs/mjm/{proposal.analysis_ref}.json products/mjm-intelligence-engine/docs/proposals/",
                f"git add .",
                f"git commit -m 'feat: MJM proposal - {proposal.title}'",
                f"gh pr create --title 'MJM: {proposal.title}' --body 'Provenance: {proposal.analysis_ref}'"
            ],
            "templates": {
                "pull_request": f"## MJM Intelligence Proposal: {proposal.title}\n\n### Summary\n{proposal.description}\n\n### Provenance\n- Checkpoint: {proposal.analysis_ref}\n- Contributor: {contributor}",
                "review_checklist": "- [ ] Verify Evidence Provenance\n- [ ] Check Regulatory Alignment\n- [ ] Assess Implementation Feasibility"
            }
        }
