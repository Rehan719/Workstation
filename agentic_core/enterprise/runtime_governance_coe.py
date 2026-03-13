import logging
from typing import Dict, Any, List
from agentic_core.governance.runtime_framework import RuntimeConstitutionalFramework, GovernanceTier

logger = logging.getLogger(__name__)

class RuntimeGovernanceCoE:
    """
    ARTICLE 616: Oversees ATS, ARI, and Conformance Engines.
    """
    def __init__(self):
        self.runtime_gov = RuntimeConstitutionalFramework()

    def audit_agent(self, agent_id: str) -> Dict[str, Any]:
        logger.info(f"RUNTIME_COE: Auditing {agent_id}")
        return {
            "agent_id": agent_id,
            "status": "HEALTHY",
            "active_containment": self.runtime_gov.active_containments.get(agent_id, GovernanceTier.T1_MINIMAL).name,
            "ari_score": self.runtime_gov.ari.scores.get(agent_id, {})
        }

    def trigger_containment(self, agent_id: str, tier: GovernanceTier):
        """ARTICLE 601: Direct authority to trigger containment."""
        self.runtime_gov.apply_containment(agent_id, tier)
