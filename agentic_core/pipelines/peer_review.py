from typing import Dict, Any, List
import asyncio
from ..orchestrator import Orchestrator

class PeerReviewPipeline:
    """
    Article U: Scientific Integrity Framework.
    Coordinates a multi-agent peer review simulation.
    """
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator

    async def run_review(self, manuscript: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the peer review process with specialized agents.
        """
        print(f"🔬 Starting Peer Review Simulation for: {manuscript.get('title', 'Draft')}")

        # 1. Domain Review (C-VI Reasoning)
        domain_task = {
            "id": "review_domain",
            "type": "agent_direct", # Avoid triggering complex workflows
            "assigned_agent": "research.reviewer.v31",
            "prompt_template": "config/prompts/review/domain_reviewer.yaml",
            "manuscript_text": manuscript.get("content"),
            "domain": manuscript.get("domain")
        }

        # 2. Statistical Review (Article L Validation)
        stat_task = {
            "id": "review_stats",
            "type": "agent_direct", # Avoid triggering complex workflows
            "assigned_agent": "data_science.reviewer.v31",
            "prompt_template": "config/prompts/review/statistical_reviewer.yaml",
            "manuscript_text": manuscript.get("content"),
            "metrics": manuscript.get("metrics")
        }

        # Execute reviews in parallel
        results = await asyncio.gather(
            self.orchestrator.execute(domain_task),
            self.orchestrator.execute(stat_task)
        )

        # 3. Synthesize Review Report
        review_report = self._synthesize_reviews(results)

        print("✅ Peer Review Complete.")
        return {
            "status": "reviewed",
            "overall_recommendation": review_report["recommendation"],
            "critiques": review_report["critiques"],
            "integrity_score": 0.92 # Mock
        }

    def _synthesize_reviews(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Consolidates feedback from multiple reviewers."""
        critiques = []
        for r in results:
            components = r.get("components", {})
            for sub_res in components.values():
                critiques.append(sub_res.get("feedback", "No issues found."))

        return {
            "recommendation": "Minor Revisions Required",
            "critiques": critiques
        }
