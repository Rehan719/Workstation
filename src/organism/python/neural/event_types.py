from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

@dataclass
class BiomimeticEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    source: str = "unknown"  # "nematron" | "nemoclaw" | "openclaw" | "human" | "system"
    priority: int = 3  # 1=critical, 5=low

@dataclass
class StrategicIntent:
    goal: str
    action_type: str
    parameters: Dict[str, Any]
    reasoning: str

@dataclass
class IntentGenerated(BiomimeticEvent):
    intent: StrategicIntent = field(default_factory=lambda: StrategicIntent("", "", {}, ""))
    confidence: float = 0.0

@dataclass
class ValidationResult:
    is_valid: bool
    reason: str
    attestation: Optional[str] = None
    policy_version: str = "1.0.0"

@dataclass
class GovernanceValidated(BiomimeticEvent):
    action_id: str = ""
    validation_result: ValidationResult = field(default_factory=lambda: ValidationResult(False, ""))
    policy_version: str = "1.0.0"

@dataclass
class ExecutionResult:
    status: str  # "SUCCESS" | "FAILED" | "PENDING"
    output: Any
    error: Optional[str] = None

@dataclass
class ResourceUsage:
    cpu_ms: float
    memory_mb: float
    api_calls: int

@dataclass
class ActionExecuted(BiomimeticEvent):
    action_id: str = ""
    result: ExecutionResult = field(default_factory=lambda: ExecutionResult("PENDING", None))
    resource_delta: Optional[ResourceUsage] = None

@dataclass
class HomeostasisEvent(BiomimeticEvent):
    metric: str = ""
    value: float = 0.0
    status: str = "STABLE"  # "STABLE" | "STRESS" | "RECOVERY"

@dataclass
class AIActionInitiated(BiomimeticEvent):
    action: str = ""
    provider: str = ""
    payload_hash: str = ""

@dataclass
class AIInferenceComplete(BiomimeticEvent):
    action_id: str = ""
    provider: str = ""
    tokens_used: int = 0
    latency_ms: float = 0.0
    status: str = "SUCCESS" # "SUCCESS" | "FAILED" | "RATE_LIMITED"
