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
    passed: bool
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
    engine: Literal["inkashaf", "aqal", "samajh", "hoshiyari", "soch", "iman", "mjm"]
    query: str
    domain: str = "general"
    context: Dict[str, Any] = {}
    constitutional_constraints: List[ConstitutionalRule] = []
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConsultationResponse(BaseModel):
    engine: str
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    constitutional_validation: ValidationResult
    citations: List[Citation] = []
    fallback_path: Optional[str] = None
    reasoning_trace: Optional[str] = None
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
