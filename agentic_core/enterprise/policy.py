import logging
import os
import datetime
from typing import Dict, Any, List, Optional
from agentic_core.governance.qms import QualityManagementSystem
from agentic_core.governance.dcs import DocumentControlSystem
from agentic_core.governance.bms import BusinessManagementSystem
from agentic_core.governance.ems import EvolutionManagementSystem
from .webscrape_coe import WebScrapeCoE
from .agentic_governance_coe import AgenticGovernanceCoE

logger = logging.getLogger(__name__)

class PolicyCoE:
    """
    ARTICLE 341, 531 & 596: Centre for Policy & Governance.
    Ensures constitutional fidelity and ethical alignment.
    Unifies QMS, DCS, BMS, and EMS.
    Includes Semi-Automated Grand Synthesis Approval Workflow.
    """
    def __init__(self):
        self.dcs_path = "docs/dcs"
        os.makedirs(self.dcs_path, exist_ok=True)
        self.qms = QualityManagementSystem()
        self.dcs = DocumentControlSystem()
        self.bms = BusinessManagementSystem()
        self.ems = EvolutionManagementSystem()
        self.webscrape_coe = WebScrapeCoE()
        self.agentic_gov_coe = AgenticGovernanceCoE()
        self.proposed_blueprints: List[Dict[str, Any]] = []

    def store_in_dcs(self, document_name: str, content: str):
        """ARTICLE 359: Stores documentation in the Document Control System (DCS)."""
        logger.info(f"Policy: Storing {document_name} in DCS.")
        self.dcs.check_in(document_name, document_name, content, "PolicyCoE", "Direct Storage")

    def submit_assimilation_blueprint(self, blueprint: Dict[str, Any]):
        """ARTICLE 596: UVIAP triggers this to propose a new synthesis."""
        blueprint["submitted_at"] = datetime.datetime.now().isoformat()
        blueprint["status"] = "PENDING_APPROVAL"
        self.proposed_blueprints.append(blueprint)
        logger.info(f"Policy: New Assimilation Blueprint proposed: {blueprint.get('id', 'unknown')}")

    def approve_blueprint(self, blueprint_id: str) -> bool:
        """Mandatory Entity Approval Step (Article 596)."""
        for bp in self.proposed_blueprints:
            if bp.get("id") == blueprint_id:
                bp["status"] = "APPROVED"
                bp["approved_at"] = datetime.datetime.now().isoformat()
                logger.info(f"Policy: Blueprint {blueprint_id} APPROVED by Entity.")
                # Trigger GSE rerun (simulated)
                self.ems.log_evolution_event("GSE_RERUN_TRIGGERED", {"blueprint_id": blueprint_id})
                return True
        return False

    def interpret_mandate(self, article_num: int) -> str:
        interpretations = {
            336: "Dual-purpose means profit is the engine, and ethics is the driver.",
            342: "C-Suite agents are direct extensions of the AI CEO's will."
        }
        return interpretations.get(article_num, "General mandate: Follow Survival Instinct Hierarchy.")

    def review_policy_alignment(self, proposal: Dict[str, Any]) -> bool:
        logger.info("Policy: Reviewing proposal for purpose alignment.")
        return proposal.get("purpose_alignment_score", 0.0) >= 0.90
