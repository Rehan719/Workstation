from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConstitutionalRule(BaseModel):
    rule_id: str
    description: str
    enforcement_level: Literal["advisory", "mandatory", "strict"]


class ValidationResult(BaseModel):
    """Three-state, because a validation nothing performed must be able to say so.

    P3.12/FU-310 — `passed` was a bare bool, so every engine passed `passed=True` over a constitutional check
    that never ran: a verdict that cannot come out otherwise. None means NOT ASSESSED, which is neither a pass
    nor a failure, and `basis` says which of the three this is and why.
    """
    passed: Optional[bool] = None
    basis: Optional[str] = None
    violations: List[str] = []
    merkle_root: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Citation(BaseModel):
    source: str
    fragment: str
    confidence: float
    metadata: Dict[str, Any] = {}


class ConsultationRequest(BaseModel):
    consultation_id: Optional[str] = None
    # P3.12/FU-310 — the registry's EngineType declares NINE engines and this Literal listed SEVEN, so the
    # contract and the registry disagreed about what exists. Derived from the registry, plus "mjm" which is a
    # lifecycle rather than a cognitive engine and is not in EngineType. The three meta engines (tawazun,
    # niyyah, tafakkur) are PLANNED under P3.13 and are accepted by the contract while their modules refuse.
    engine: str = Field(description="an EngineType value, or 'mjm'")
    query: str
    domain: str = "general"
    context: Dict[str, Any] = {}
    constitutional_constraints: List[ConstitutionalRule] = []
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConsultationResponse(BaseModel):
    """P3.12/FU-310 — three defects removed, and each one forced an engine to lie.

    `confidence` was a REQUIRED float with no three-state option, so an engine that cannot judge its own
    confidence had to invent a number — all eight constructors did (0.88 in the engines, 0.96 in MJM). It is
    now optional with a `confidence_basis`: None means nothing computed it, and that is the honest answer for
    an engine that has not been built yet.

    And there was NO provenance field, so once an engine calls a model the response could not say what served
    it. Every other output surface in this repository carries `served_by` / `is_external`; without these the
    cognitive layer would be the one place that discipline stops.
    """
    engine: str
    answer: str
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    confidence_basis: Optional[str] = None
    served_by: Optional[str] = None
    is_external: bool = False
    constitutional_validation: ValidationResult
    citations: List[Citation] = []
    fallback_path: Optional[str] = None
    reasoning_trace: Optional[str] = None
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
