import json
import os
import hashlib
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class LegalEvent:
    id: str
    date: str
    description: str
    source_document: str
    source_page: Optional[int] = None
    related_parties: List[str] = field(default_factory=list)
    legal_tags: List[str] = field(default_factory=list) # e.g. ["EqA_2010_S15", "ERA_1996_S103A"]
    confidence: float = 0.8
    audit_hash: Optional[str] = None # Link to SovereignAuditLog entry

class EvidenceGraph:
    """
    Structured storage for extracted legal facts.
    Maintains link to original documents and AI audit trail.
    """
    def __init__(self, storage_path: str = "data/organism/evidence_graph.json"):
        self.storage_path = storage_path
        self.events: Dict[str, LegalEvent] = {}
        self._load()

    def add_event(self, event: LegalEvent):
        self.events[event.id] = event
        self._save()

    def get_event(self, event_id: str) -> Optional[LegalEvent]:
        return self.events.get(event_id)

    def query_by_tag(self, tag: str) -> List[LegalEvent]:
        return [e for e in self.events.values() if tag in e.legal_tags]

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.events[k] = LegalEvent(**v)
            except Exception:
                self.events = {}

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({k: asdict(v) for k, v in self.events.items()}, f, indent=2)

    def get_chronology(self) -> List[LegalEvent]:
        """Returns events sorted by date."""
        return sorted(self.events.values(), key=lambda x: x.date)
