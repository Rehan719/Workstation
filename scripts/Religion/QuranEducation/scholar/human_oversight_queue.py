import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

class HumanOversightQueue:
    """
    Manages scholar review workflows for critical AI decisions.
    Industrialized v8.8 Backend: Acts as "Scholar Laboratory".
    Integrates v8.6 Human-in-the-Loop requirements.
    """
    def __init__(self, queue_file: str = "knowledge/Religion/QuranEducation/scholar/oversight_queue.json", facility_orchestrator=None):
        self.queue_file = queue_file
        self.facility_orchestrator = facility_orchestrator
        os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        self.load_queue()

    def load_queue(self):
        if os.path.exists(self.queue_file):
            with open(self.queue_file, "r") as f:
                self.queue = json.load(f)
        else:
            self.queue = []

    def save_queue(self):
        with open(self.queue_file, "w") as f:
            json.dump(self.queue, f, indent=2)

    def add_to_queue(self, source_engine: str, content_id: str, issue: str, metadata: Dict[str, Any]) -> str:
        """Adds a critical AI decision to the human review queue."""
        if self.facility_orchestrator:
            return self.facility_orchestrator.run_in_facility(
                "laboratories",
                "add_to_oversight_queue",
                self._add_logic,
                source_engine, content_id, issue, metadata
            )
        else:
            return self._add_logic(source_engine, content_id, issue, metadata)

    def _add_logic(self, source_engine, content_id, issue, metadata):
        item_id = str(uuid.uuid4())
        item = {
            "item_id": item_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_engine": source_engine,
            "content_id": content_id,
            "issue_description": issue,
            "metadata": metadata,
            "status": "PENDING"
        }
        self.queue.append(item)
        self.save_queue()
        return item_id

    def resolve_item(self, item_id: str, scholar_id: str, decision: str, notes: str) -> bool:
        """Resolves a queue item with scholar decision."""
        if self.facility_orchestrator:
            return self.facility_orchestrator.run_in_facility(
                "laboratories",
                "resolve_oversight_item",
                self._resolve_logic,
                item_id, scholar_id, decision, notes
            )
        else:
            return self._resolve_logic(item_id, scholar_id, decision, notes)

    def _resolve_logic(self, item_id: str, scholar_id: str, decision: str, notes: str) -> bool:
        for item in self.queue:
            if item["item_id"] == item_id:
                item["status"] = "RESOLVED"
                item["scholar_id"] = scholar_id
                item["decision"] = decision
                item["decision_notes"] = notes
                item["resolved_at"] = datetime.now(timezone.utc).isoformat()
                self.save_queue()
                self._log_to_audit(item)
                return True
        return False

    def _log_to_audit(self, item: Dict[str, Any]):
        audit_log = "outputs/Religion/QuranEducation/audit/sovereign_audit_log_v8.8.jsonl"
        audit_event = {
            "version": "8.8.0",
            "phase": 12,
            "pipeline": "Introspection",
            "action": "HUMAN_OVERSIGHT_DECISION",
            "details": item
        }
        with open(audit_log, "a") as f:
            f.write(json.dumps(audit_event) + "\n")

if __name__ == "__main__":
    queue = HumanOversightQueue()
    print("📋 Adding sample theological flag to HITL queue...")
    item_id = queue.add_to_queue(
        "TheologicalConsistencyChecker",
        "lesson_01",
        "Potential ambiguity in Tafsir of Surah Al-Fatiha verse 4.",
        {"consistency_score": 0.92, "xai_trace": "counterfactual_flagged"}
    )
    print(f"✅ Item Added: {item_id}")

    print("🎓 Resolving item with Scholar Approval...")
    queue.resolve_item(item_id, "scholar_786", "APPROVE", "Contextual interpretation is verified as sahih.")
    print("✅ Item Resolved and Logged to Audit.")
