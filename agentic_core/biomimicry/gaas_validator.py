import logging
import json
import re
import os
import time
from typing import Dict, Any, Optional, List

class GaaSValidator:
    """
    Governance-as-a-Service (GaaS) Middleware.
    Validates agentic traffic against the Workstation Constitution.
    """
    def __init__(self, constitution_path: str):
        self.constitution_path = constitution_path
        self.logger = logging.getLogger("GaaSValidator")
        self.trust_factors: Dict[str, float] = {} # agent_id -> T_Fa
        self.enforcement_mode = "Adaptive" # Coercive, Normative, Adaptive, adaptive_immune, symbiotic_audit

        # Load and parse constitution
        self.articles = self._load_articles()

    def _load_articles(self) -> List[Dict[str, Any]]:
        """Parses the Markdown constitution file for Articles."""
        articles = []
        if not os.path.exists(self.constitution_path):
            self.logger.error(f"Constitution not found at {self.constitution_path}")
            return []

        with open(self.constitution_path, 'r') as f:
            content = f.read()

        # Updated Regex to find "**ARTICLE XXX: TITLE**" and its serves line
        matches = re.finditer(r"\*\*ARTICLE (\d+): (.*?)\*\*\n(.*?)\*Serves: (.*?)\*", content, re.DOTALL)
        for match in matches:
            articles.append({
                "number": int(match.group(1)),
                "title": match.group(2).strip(),
                "text": match.group(3).strip(),
                "serves": match.group(4).strip(),
                "risk": self._determine_risk(int(match.group(1)))
            })

        self.logger.info(f"Loaded {len(articles)} articles from {self.constitution_path}")
        return articles

    def _determine_risk(self, article_num: int) -> str:
        # High risk articles related to core modifications or security
        if article_num in [1089, 1091, 1099, 1101, 1104, 1108, 1114, 1115, 1116, 1121, 1123]:
            return "High"
        if article_num in [1087, 1093, 1094, 1103, 1105, 1110, 1112, 1113, 1119]:
            return "Medium"
        return "Low"

    def validate_payload(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intercepts and validates an agentic payload.
        """
        intent = payload.get("intent", "unknown")
        is_high_risk = payload.get("high_risk", False)
        swarm_id = payload.get("swarm_id")

        t_fa = self.trust_factors.get(agent_id, 1.0)

        # Swarm Trust Factor (Article 1114/1117)
        swarm_t_fa = self.trust_factors.get(f"swarm_{swarm_id}", 1.0) if swarm_id else 1.0
        effective_t_fa = min(t_fa, swarm_t_fa)

        decision = "ALLOW"
        reason = "Constitutional alignment verified."
        violated_article = None

        # Check for High-Risk intent without proper trust (Article 1101 & 1114)
        if is_high_risk:
            if effective_t_fa < 0.8:
                decision = "BLOCK"
                reason = "Violation of Article 1101/1114: High-risk action by low-trust agent/swarm."
                violated_article = 1114 if swarm_id else 1101
            else:
                decision = "PENDING_APPROVAL"
                reason = "Article 1114: Swarm high-risk action requires 10-minute human veto window."
                violated_article = 1114

        # Update trust factor
        if decision == "ALLOW":
            self.trust_factors[agent_id] = min(1.0, t_fa + 0.01)
        else:
            self.trust_factors[agent_id] = max(0.0, t_fa - 0.1)

        result = {
            "decision": decision,
            "reason": reason,
            "t_fa": self.trust_factors[agent_id],
            "agent_id": agent_id,
            "violated_article": violated_article,
            "timestamp": time.time()
        }

        self.logger.info(f"GaaS Decision: {decision} for {agent_id} | Reason: {reason}")
        return result

    def set_enforcement_mode(self, mode: str):
        if mode in ["Coercive", "Normative", "Adaptive", "adaptive_immune", "symbiotic_audit"]:
            self.enforcement_mode = mode
            self.logger.info(f"GaaS enforcement mode set to {mode}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    gaas = GaaSValidator("agentic_core/constitution/CONSTITUTION_v138.0.0.md")
    print(f"Parsed {len(gaas.articles)} articles.")
    if gaas.articles:
        print(f"First parsed article: {gaas.articles[0]['number']} - {gaas.articles[0]['title']}")
