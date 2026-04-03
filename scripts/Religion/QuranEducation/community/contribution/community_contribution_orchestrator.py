import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List

class CommunityContributionOrchestrator:
    """
    BACKEND ORCHESTRATOR: COMMUNITY CONTRIBUTION WORKFLOW v8.3
    Handles ingestion, validation, and pipeline routing for community content.
    """
    def __init__(self, archive_manager, scholar_handler):
        self.archive = archive_manager
        self.scholar = scholar_handler
        self.output_dir = "outputs/Religion/QuranEducation/community"
        self.audit_log = f"{self.output_dir}/audit/community_contribution_log_v8.3.jsonl"
        os.makedirs(os.path.dirname(self.audit_log), exist_ok=True)

    def ingest_contribution(self, contribution_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingest a community contribution with validation and pipeline routing.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        contribution_id = f"CONT-{hashlib.sha256(f'{timestamp}|{contribution_data.get('contributor')}|{contribution_data.get('title')}'.encode()).hexdigest()[:8]}"

        # 1. Schema Validation (Mock)
        validation_status = self._validate_schema(contribution_data)

        # 2. Pipeline Routing
        pipelines = self._route_to_pipelines(contribution_data)

        # 3. Theological Consistency Check (Mock Trigger for Scholar)
        theological_check = "pending_scholar_review"

        result = {
            "id": contribution_id,
            "status": validation_status,
            "timestamp": timestamp,
            "pipelines": pipelines,
            "theological_check": theological_check,
            "data": contribution_data
        }

        # 4. Log to Audit Trail
        self._log_audit("INGESTION", result)

        return result

    def _validate_schema(self, data: Dict[str, Any]) -> str:
        # Check for required fields
        required = ["title", "contributor", "category", "content"]
        for field in required:
            if field not in data:
                return f"INVALID: Missing field {field}"
        return "VALIDATED"

    def _route_to_pipelines(self, data: Dict[str, Any]) -> List[str]:
        # Intelligent routing logic based on category
        category = data.get("category", "").lower()
        if category == "audio":
            return ["Scraping", "Knowledge", "Learning"]
        elif category == "text":
            return ["Ingestion", "Knowledge", "Forge"]
        elif category == "interactive":
            return ["Forge", "Learning", "Developer"]
        return ["Learning"]

    def _log_audit(self, action: str, details: Dict[str, Any]):
        event = {
            "version": "8.3.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "details": details
        }
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(event) + "\n")

    def approve_contribution(self, contribution_id: str, scholar_id: str) -> Dict[str, Any]:
        """
        Final approval workflow after scholar review.
        """
        approval_event = {
            "id": contribution_id,
            "scholar": scholar_id,
            "status": "APPROVED",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self._log_audit("APPROVAL", approval_event)
        return approval_event
