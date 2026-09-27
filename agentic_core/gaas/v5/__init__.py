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

# §10 (W494, FU-130) — THE SCOPE OF AN INTENT GATE.
# Five call sites hand intercept() nothing but an intent label, a domain and a CONSTANT attestation
# sentence, then report the verdict as governance over the whole delivery. policy_gate.validate only
# substring-checks the intent against a prohibited list, and validate_output regexes that constant
# sentence — so "allowed" cannot reflect anything any tier actually wrote, and it can never come out
# any other way for a well-formed request. genesis.py's streaming establish path already said this
# ("screened the establish intent and domain — not the enterprise's content"); the wording lives here
# now so every emitter says the same thing and none can quietly stop saying it.
INTENT_GATE_SCOPE = ("intent + domain only — this gate screened the request's intent label against the "
                     "prohibited list and its own constant attestation sentence. The delivery's content "
                     "was NOT screened, so this verdict is not a judgement on what was produced.")


def intent_gate_result(status: str, checkpoint: str | None = None, node: str | None = None,
                       **extra: object) -> dict:
    """The shape every intent-gate emitter returns: a verdict that says what it covers."""
    out: dict = {"status": status, "scope": INTENT_GATE_SCOPE, "screened": "intent + domain",
                 "content_screened": False}
    if checkpoint is not None:
        out["checkpoint"] = checkpoint
    if node is not None:
        out["node"] = node
    out.update(extra)
    return out


__all__ = [
    "INTENT_GATE_SCOPE",
    "intent_gate_result",
    "UEGLogger",
    "ConstitutionalPolicyGate",
    "SelfTuningCircuitBreaker",
    "UnifiedConstitutionalInterceptorV16Omega",
    "InterceptionResult",
]
