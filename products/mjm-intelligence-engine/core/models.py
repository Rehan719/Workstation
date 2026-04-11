import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class MJMPhase(str, Enum):
    MUSHAHIDA = "mushahida"
    JAIZA = "jaiza"
    MUAINA = "muaina"

class EvidenceSource(BaseModel):
    type: str
    uri: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class EvidenceItem(BaseModel):
    id: str
    content: str
    source: EvidenceSource
    metadata: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    tags: List[str] = Field(default_factory=list)
    sha256: str
    provenance_id: Optional[str] = None

    @classmethod
    def create(cls, content: str, source: EvidenceSource, metadata: Dict[str, Any] = None, tags: List[str] = None):
        sha256 = hashlib.sha256(content.encode()).hexdigest()
        item_id = f"EVD-{sha256[:8]}-{int(datetime.now(timezone.utc).timestamp())}"
        return cls(
            id=item_id,
            content=content,
            source=source,
            metadata=metadata or {},
            tags=tags or [],
            sha256=sha256
        )

class EvidenceGraph(BaseModel):
    items: List[EvidenceItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sha256: Optional[str] = None

    def calculate_hash(self):
        content = "".join([i.sha256 for i in sorted(self.items, key=lambda x: x.id)])
        self.sha256 = hashlib.sha256(content.encode()).hexdigest()
        return self.sha256

    def get_timeline(self) -> List[EvidenceItem]:
        return sorted(self.items, key=lambda x: x.source.timestamp)

class AnalysisDossier(BaseModel):
    evidence_graph_ref: str # SHA-256 of the source graph
    patterns: List[Dict[str, Any]] = Field(default_factory=list)
    risks: List[Dict[str, Any]] = Field(default_factory=list)
    strategic_options: List[Dict[str, Any]] = Field(default_factory=list)
    regulatory_compliance: Dict[str, Any] = Field(default_factory=dict)
    confidence_intervals: Dict[str, Any] = Field(default_factory=dict)
    sha256: Optional[str] = None

    def calculate_hash(self):
        content = json.dumps(self.model_dump(exclude={"sha256"}), sort_keys=True)
        self.sha256 = hashlib.sha256(content.encode()).hexdigest()
        return self.sha256

class ProposalPackage(BaseModel):
    analysis_ref: str # SHA-256 of the source dossier
    title: str
    description: str
    roadmap: List[Dict[str, Any]] = Field(default_factory=list)
    success_metrics: Dict[str, Any] = Field(default_factory=dict)
    verification_protocol: Dict[str, Any] = Field(default_factory=dict)
    litigation_bundle: Optional[Dict[str, Any]] = None
    sha256: Optional[str] = None

    def calculate_hash(self):
        content = json.dumps(self.model_dump(exclude={"sha256"}), sort_keys=True)
        self.sha256 = hashlib.sha256(content.encode()).hexdigest()
        return self.sha256

class MJMOutputBundle(BaseModel):
    evidence_graph: EvidenceGraph
    analysis_dossier: AnalysisDossier
    proposal_package: ProposalPackage
    provenance_json_ld: str

class WorkflowState(BaseModel):
    checkpoint_id: str
    phase: MJMPhase
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    contributor: str
    sha256: Optional[str] = None

    def calculate_hash(self):
        content = json.dumps(self.model_dump(exclude={"sha256"}), sort_keys=True, default=str)
        self.sha256 = hashlib.sha256(content.encode()).hexdigest()
        return self.sha256
