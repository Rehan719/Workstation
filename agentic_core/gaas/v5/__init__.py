"""
GaaS v5 — the v16-"Omega" constitutional interception stack.

Public surface:
    UnifiedConstitutionalInterceptorV16Omega  — the per-node middleware
    SelfTuningCircuitBreaker                  — RL error-rate breaker (Article 5.2)
    ConstitutionalPolicyGate                  — deterministic pre/post gate (Article 11.1)
    UEGLogger                                 — SHA3-512 hash-chained event log
    InterceptionResult                        — structured outcome of an interception
"""
from .ueg import UEGLogger
from .policy_gate import ConstitutionalPolicyGate
from .circuit_breaker_rl import SelfTuningCircuitBreaker
from .uci_v16_omega import UnifiedConstitutionalInterceptorV16Omega, InterceptionResult

__all__ = [
    "UEGLogger",
    "ConstitutionalPolicyGate",
    "SelfTuningCircuitBreaker",
    "UnifiedConstitutionalInterceptorV16Omega",
    "InterceptionResult",
]
