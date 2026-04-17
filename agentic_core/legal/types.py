from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class TribunalTask:
    """UK Employment Tribunal Task definition."""
    id: str
    statute: str  # e.g., "EqualityAct2010", "ERA1996", "ACASCode"
    claim_type: str  # e.g., "unfair_dismissal", "discrimination"
    priority: float
    required_precedents: List[str] = field(default_factory=list)
    jurisdiction: str = "England_Wales"  # "England_Wales", "Scotland", "NI"

@dataclass
class LegalAgent:
    """Agent with legal competencies and jurisdiction."""
    id: str
    competencies: List[str]  # statutes agent is trained on
    available_capacity: float
    jurisdiction: str
    experience_level: float = 0.5  # [0, 1]

@dataclass
class LegalCompliance:
    """Result of a legal compliance validation."""
    is_compliant: bool
    coverage_score: float
    violations: List[str]
    matched_precedents: List[str]
    audit_hash: str
