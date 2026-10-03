"""
Unified Constitutional Interceptor — v16 "Omega" — GaaS v5.

ARTICLE 11.1. The single middleware through which every agent-framework call
(AutoGen, LangGraph, CrewAI, Mammouth, NeMo, Nematron, …) is routed. The Omega
revision is node-scoped, self-logging to the UEG, and fronted by a self-tuning
RL circuit breaker.

Lifecycle of every intercepted call:
    0. Breaker check       — refuse fast if the node's breaker is open
    1. Pre-execution gate  — deny / escalate prohibited intents
    2. Execute             — run the wrapped action (sync or async)
    3. Post-execution gate — validate the produced output
    4. Checkpoint          — write a tamper-evident record to the UEG
"""
from __future__ import annotations

import inspect
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from .ueg import UEGLogger
from .policy_gate import ConstitutionalPolicyGate
from . import horizon_guardrails as _guardrails
from .circuit_breaker_rl import SelfTuningCircuitBreaker

logger = logging.getLogger("gaas.v5.uci")


@dataclass
class InterceptionResult:
    """Structured outcome of an interception."""

    status: str                       # allowed | blocked | partial | halted
    output: Any = None
    reason: Optional[str] = None
    checkpoint_id: Optional[str] = None
    warning: Optional[str] = None
    latency_ms: float = 0.0
    node: Optional[str] = None
    ueg_logged: Optional[bool] = None   # W472 (FU-054) — whether this decision reached the constitutional ledger
    article: Optional[str] = None       # W505 (FU-007) — WHICH constitutional article refused
    violations: Optional[list] = None   # W505 (FU-006) — the post gate's ACTUAL findings. They were
    #                                     chained to the ledger and dropped from the result, so a caller
    #                                     could only report the fixed `warning` sentence.
    escalation: bool = False            # W505 (FU-007) — True when the refusal is an outstanding human
    #                                     approval (article 7.3), not a breach. `status` stays "blocked"
    #                                     either way, so a reader that halts on it keeps halting.
    guardrails: Optional[dict] = None   # W551 (P2.12) — the three Horizon guardrails' own report:
    #                                     every gate's verdict, what it did NOT look at, and the
    #                                     distress route field shown as unfilled. ADDED, never
    #                                     substituted: `status` and `escalation` keep their meanings,
    #                                     because three readers halt on the first and the second
    #                                     decides whether the breaker counts a refusal as a breach.

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


class UnifiedConstitutionalInterceptorV16Omega:
    """Per-node constitutional middleware (the v16-Omega UCI)."""

    def __init__(
        self,
        node_id: str,
        ueg_logger: Optional[UEGLogger] = None,
        policy_gate: Optional[ConstitutionalPolicyGate] = None,
        circuit_breaker: Optional[SelfTuningCircuitBreaker] = None,
    ):
        self.node_id = node_id
        self.ueg = ueg_logger or UEGLogger()
        self.policy_gate = policy_gate or ConstitutionalPolicyGate(domain=node_id)
        self.circuit_breaker = circuit_breaker or SelfTuningCircuitBreaker(self.ueg, domain=node_id)
        self.logger = logging.getLogger(f"gaas.v5.uci[{node_id}]")

    @staticmethod
    async def _run(action: Callable) -> Any:
        """Execute an action that may be sync, async, or return an awaitable."""
        result = action()
        if inspect.isawaitable(result):
            return await result
        return result

    def _ueg(self, write: Callable[[], Any]) -> bool:
        """W472 (register FU-054) — the interceptor's OWN ledger writes never raise out of a decision: a chain that
        cannot be read whole, or a store lock that timed out, used to turn an allowed action into an exception (the
        Board re-ran its action, the governed cycle reported an ungated bypass, a posted transfer answered 500).
        The decision stands; whether it reached the ledger is said (ueg_logged)."""
        try:
            write()
            return True
        except Exception as exc:
            logger.warning("UCI %s: the constitutional ledger did not take the record (%s: %s)",
                           self.node_id, exc.__class__.__name__, str(exc)[:120])
            return False

    async def intercept(self, context: Dict[str, Any], action: Callable) -> InterceptionResult:
        action_type = str(context.get("intent") or context.get("action_type") or "generic")

        # 0. Breaker open → refuse fast
        if self.circuit_breaker.should_halt():
            logged = self._ueg(lambda: self.ueg.log_policy_halt(self.node_id, action_type, "circuit breaker open"))
            return InterceptionResult(status="halted", reason=self.circuit_breaker.trip_reason,
                                      node=self.node_id, ueg_logged=logged)

        # 0b. W551 (P2.12) — THE THREE HORIZON GUARDRAILS, IN THE SEQUENCE. The item's words are
        #     "attached to the gaas.v5 interceptor, not beside it": a guardrail a caller has to remember
        #     to ask for is a guardrail that is not on the path. They screen the REQUEST here and the
        #     OUTPUT at step 3, and an escalation is recorded as an ESCALATION rather than a breach, so a
        #     screen doing its job does not trip the breaker and halt the node (the W505 distinction).
        _g_in = _guardrails.screen_all(context.get("text") or context.get("prompt")
                                       or context.get("query") or action_type)
        if _g_in["escalate"]:
            logged = self._ueg(lambda: self.ueg.log_policy_halt(
                self.node_id, action_type, f"horizon guardrail: {', '.join(_g_in['escalated_by'])}"))
            self.circuit_breaker.record_event(success=False, is_violation=False, severe=False,
                                              escalation=True)
            return InterceptionResult(
                status="blocked", node=self.node_id, ueg_logged=logged, escalation=True,
                reason=("a Horizon guardrail escalated this request: "
                        + "; ".join(_g_in["gates"][g]["action"] for g in _g_in["escalated_by"])),
                guardrails=_g_in)

        # 1. Pre-execution gate
        pre = self.policy_gate.validate(action_type, context)
        if not pre["allowed"]:
            logged = self._ueg(lambda: self.ueg.log_policy_halt(self.node_id, action_type, pre["reason"]))
            # W505 (FU-007) — WHICH ARTICLE refused decides what this is. An action waiting for a human
            # approval it declared it needs is an escalation working, not a constitutional violation; it used
            # to be recorded as one, and the breaker then halted every later action on this node until
            # somebody reset it by hand. A prohibited INTENT (11.1) is a real breach and still trips first.
            _escalation = str(pre.get("article") or "") == "7.3"
            self.circuit_breaker.record_event(success=False, is_violation=not _escalation,
                                              severe=not _escalation, escalation=_escalation)
            # The STATUS stays "blocked". Three readers already depend on its four values - the economy
            # cycle halts on ("blocked", "halted"), and letting an escalation past that check would move
            # money while an approval was still outstanding. The distinction is ADDED, not substituted.
            return InterceptionResult(status="blocked", reason=pre["reason"], node=self.node_id,
                                      ueg_logged=logged, article=pre.get("article"),
                                      escalation=_escalation)

        # 2. Execute
        start = time.time()
        try:
            output = await self._run(action)
            latency = (time.time() - start) * 1000.0
            self.circuit_breaker.record_event(success=True)
        except Exception as exc:
            self.circuit_breaker.record_event(success=False)
            self._ueg(lambda: self.ueg.log_constitutional_event({
                "type": "execution_failure", "node": self.node_id,
                "action": action_type, "error": str(exc)}))
            raise                                     # the action's OWN error, never the ledger's

        # 2b. W551 (P2.12) — THE SAME THREE GATES OVER THE OUTPUT. A request can pass every screen and
        #     the answer still carry a ruling, a proof claim or counsel to someone in distress: the
        #     subject of the screen is the TEXT, and the output is text the platform wrote itself, which
        #     is the half that matters most. An escalation here withholds the emission.
        _g_out = _guardrails.screen_all(output if isinstance(output, str) else str(output))
        if _g_out["escalate"]:
            logged = self._ueg(lambda: self.ueg.log_constitutional_event({
                "type": "horizon_guardrail_withheld", "node": self.node_id, "action": action_type,
                "gates": _g_out["escalated_by"]}))
            self.circuit_breaker.record_event(success=False, is_violation=False, severe=False,
                                              escalation=True)
            return InterceptionResult(
                status="blocked", node=self.node_id, ueg_logged=logged, escalation=True,
                latency_ms=latency,
                reason=("a Horizon guardrail withheld this output: "
                        + "; ".join(_g_out["gates"][g]["action"] for g in _g_out["escalated_by"])),
                guardrails=_g_out)

        # 3. Post-execution gate
        post = self.policy_gate.validate_output(output)
        if not post["compliant"]:
            logged = self._ueg(lambda: self.ueg.log_constitutional_event({
                "type": "post_validation_failure", "node": self.node_id,
                "violations": post["violations"]}))
            return InterceptionResult(status="partial", output=output,
                                      warning="Output violates constitutional rules",
                                      violations=list(post.get("violations") or []),
                                      latency_ms=latency, node=self.node_id, ueg_logged=logged)

        # 4. Checkpoint
        checkpoint_id = f"CHK-{int(time.time() * 1000)}"
        logged = self._ueg(lambda: self.ueg.log_constitutional_event({
            "type": "checkpoint", "checkpoint_id": checkpoint_id, "node": self.node_id,
            "action": action_type, "latency_ms": round(latency, 2)}))

        # W551 (P2.12) — THE LIMITS TRAVEL WITH THE ALLOWED RESULT TOO, and this is the half a first
        # draft of this change missed. If the guardrail report appeared only on an escalation, its
        # ABSENCE on a success would read as a clearance — and these screens certify nothing: each is an
        # English phrase screen and a non-match means its own patterns found nothing, not that the
        # subject was absent. The bar's words are "each gate's stated limit is on the surface", and a
        # limit shown only when it fired is a limit shown exactly when nobody needs it. The output
        # screen's report is carried, because it is the later of the two and ran over what will be sent.
        return InterceptionResult(status="allowed", output=output, checkpoint_id=checkpoint_id,
                                  latency_ms=latency, node=self.node_id, ueg_logged=logged,
                                  guardrails=_g_out)
