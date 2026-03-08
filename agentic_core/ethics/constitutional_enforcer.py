import logging
import json
import os
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ConstitutionalEnforcer:
    """
    L-C-VIII: Constitutional Runtime Enforcement.
    Actively monitors system behavior against the 77 articles of v99.0.0.
    """
    def __init__(self, constitution_path: str = "agentic_core/constitution/CONSTITUTION_v99.0.0.md"):
        self.constitution_path = constitution_path
        self.audit_log = []
        self.violations = []
        # In a real system, we would parse the markdown to get all articles
        self.active_articles = self._load_article_manifest()

    def _load_article_manifest(self) -> List[str]:
        # Represents the 77 articles for monitoring
        manifest_path = "agentic_core/constitution/manifest.json"
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                return list(json.load(f).get("articles", {}).keys())
        return [f"Article {i}" for i in range(1, 78)]

    def verify_action(self, action_type: str, metadata: Dict[str, Any]) -> bool:
        """Verifies if an action complies with constitutional mandates."""
        is_compliant = True
        reason = "Compliant"

        # Example check: Survival hierarchy (Immune > Nervous)
        if action_type == "subsystem_override":
            source = metadata.get("source")
            target = metadata.get("target")
            hierarchy = ["immune", "nervous", "digestive", "aging"]
            if source in hierarchy and target in hierarchy:
                if hierarchy.index(source) >= hierarchy.index(target):
                    is_compliant = False
                    reason = f"Violation of Survival Hierarchy: {source} cannot override {target}"

        # Example check: Tier 1 Parameter immutability
        if action_type == "parameter_update" and metadata.get("tier") == 1:
            is_compliant = False
            reason = "Violation of Article CP-I: Tier 1 parameters are immutable at runtime."

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_type,
            "compliant": is_compliant,
            "reason": reason,
            "metadata": metadata
        }
        self.audit_log.append(log_entry)

        if not is_compliant:
            self.violations.append(log_entry)
            logger.error(f"CONSTITUTIONAL VIOLATION: {reason}")

        return is_compliant

    def get_compliance_report(self) -> Dict[str, Any]:
        total = len(self.audit_log)
        violations = len(self.violations)
        return {
            "compliance_rate": (total - violations) / total if total > 0 else 1.0,
            "total_actions_audited": total,
            "violation_count": violations,
            "recent_violations": self.violations[-5:]
        }
