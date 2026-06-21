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

    async def intercept(self, context: Dict[str, Any], action: Callable) -> InterceptionResult:
        action_type = str(context.get("intent") or context.get("action_type") or "generic")

        # 0. Breaker open → refuse fast
        if self.circuit_breaker.should_halt():
            self.ueg.log_policy_halt(self.node_id, action_type, "circuit breaker open")
            return InterceptionResult(status="halted", reason=self.circuit_breaker.trip_reason,
                                      node=self.node_id)

        # 1. Pre-execution gate
        pre = self.policy_gate.validate(action_type, context)
        if not pre["allowed"]:
            self.ueg.log_policy_halt(self.node_id, action_type, pre["reason"])
            self.circuit_breaker.record_event(success=False, is_violation=True)
            return InterceptionResult(status="blocked", reason=pre["reason"], node=self.node_id)

        # 2. Execute
        start = time.time()
        try:
            output = await self._run(action)
            latency = (time.time() - start) * 1000.0
            self.circuit_breaker.record_event(success=True)
        except Exception as exc:
            self.circuit_breaker.record_event(success=False)
            self.ueg.log_constitutional_event({
                "type": "execution_failure", "node": self.node_id,
                "action": action_type, "error": str(exc)})
            raise

        # 3. Post-execution gate
        post = self.policy_gate.validate_output(output)
        if not post["compliant"]:
            self.ueg.log_constitutional_event({
                "type": "post_validation_failure", "node": self.node_id,
                "violations": post["violations"]})
            return InterceptionResult(status="partial", output=output,
                                      warning="Output violates constitutional rules",
                                      latency_ms=latency, node=self.node_id)

        # 4. Checkpoint
        checkpoint_id = f"CHK-{int(time.time() * 1000)}"
        self.ueg.log_constitutional_event({
            "type": "checkpoint", "checkpoint_id": checkpoint_id, "node": self.node_id,
            "action": action_type, "latency_ms": round(latency, 2)})

        return InterceptionResult(status="allowed", output=output, checkpoint_id=checkpoint_id,
                                  latency_ms=latency, node=self.node_id)
