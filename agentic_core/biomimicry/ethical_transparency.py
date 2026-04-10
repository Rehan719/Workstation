import time
import logging
from typing import Dict, Any, List

class EthicalChannel:
    """
    Transparency and Constitutional Audit Trail.
    Renders GaaS decisions into human-readable natural language.
    """
    def __init__(self, gaas_validator, ueg_callback=None):
        self.logger = logging.getLogger("EthicalChannel")
        self.gaas = gaas_validator
        self.ueg_callback = ueg_callback

    def explain_decision(self, decision_event: Dict[str, Any]) -> str:
        """
        Translates a technical GaaS decision into a plain-English explanation.
        """
        decision = decision_event.get("decision", "UNKNOWN")
        reason = decision_event.get("reason", "No reason provided.")
        article_num = decision_event.get("violated_article")

        explanation = f"GaaS Decision: {decision}. "

        if decision == "BLOCK":
            explanation += f"This action was prevented because it failed to align with the Workstation Constitution."
            if article_num:
                # Mock lookup in parsed articles
                article = next((a for a in self.gaas.articles if a["number"] == article_num), None)
                if article:
                    explanation += f" Specifically, it violated Article {article_num} ({article['title']})."
        elif decision == "PENDING_APPROVAL":
            explanation += "This action is high-priority and requires human oversight before it can proceed."
        else:
            explanation += "Everything looks good! This action aligns with our constitutional values."

        self._emit_event("ETHICAL_EXPLANATION", {
            "agent_id": decision_event.get("agent_id"),
            "explanation": explanation
        })

        return explanation

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "EthicalChannel",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    from agentic_core.biomimicry.gaas_validator import GaaSValidator
    gaas = GaaSValidator("agentic_core/constitution/CONSTITUTION_v138.0.0.md")
    ethical = EthicalChannel(gaas)

    # Test block explanation
    mock_event = {"decision": "BLOCK", "reason": "Low trust", "violated_article": 1114, "agent_id": "test_agent"}
    print(ethical.explain_decision(mock_event))
