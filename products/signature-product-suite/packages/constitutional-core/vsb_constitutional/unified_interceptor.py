import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, List
from datetime import datetime, timezone
from .gaas_validator_v3 import GaaSValidatorV3
from .ueg_logger import UEGLogger

@dataclass
class InterceptionContext:
    framework: str
    action_type: str
    payload: Dict[str, Any]
    agent_id: str
    tool_name: Optional[str] = None
    execution_time_ms: float = 0.0

@dataclass
class InterceptionResult:
    status: str
    output: Any = None
    reason: Optional[str] = None
    checkpoint_id: Optional[str] = None
    warning: Optional[str] = None

class UnifiedConstitutionalInterceptor:
    """
    ARTICLE 11.1: Unified Constitutional Interceptor (UCI).
    Single middleware intercepting all agent-framework communication across
    AutoGen, LangGraph, CrewAI, and Mammouth.
    """
    def __init__(self, gaas_validator: GaaSValidatorV3, ueg_logger: UEGLogger):
        self.gaas = gaas_validator
        self.ueg = ueg_logger
        self.logger = logging.getLogger("UCI")

    async def intercept(self, context: InterceptionContext, execute_action: Callable[[], Any]) -> InterceptionResult:
        """
        Intercepts an agent action, enforcing constitutional rules before and after.
        """
        # 1. Pre-execution gate
        pre_result = await self.gaas.policy_gate.validate_action(context.action_type, context.payload)
        if not pre_result["allowed"]:
            self.ueg.log_policy_halt(self.gaas.domain, context.action_type, pre_result["reason"])
            if self.gaas.circuit_breaker.should_halt():
                # Trip on critical violation
                self.gaas.circuit_breaker.record_event(success=False, is_violation=True)
                raise Exception(f"Constitutional Violation: {pre_result['reason']}")
            return InterceptionResult(status="blocked", reason=pre_result["reason"])

        # 2. Execute the actual action
        start_time = time.time()
        try:
            output = await execute_action()
            execution_time = (time.time() - start_time) * 1000
            context.execution_time_ms = execution_time
            self.gaas.circuit_breaker.record_event(success=True)
        except Exception as e:
            self.ueg.log_constitutional_event({
                "type": "execution_failure",
                "agent_id": context.agent_id,
                "error": str(e)
            })
            self.gaas.circuit_breaker.record_event(success=False)
            raise

        # 3. Post-execution validation
        post_result = self.gaas.validate_payload(output)
        if not post_result["compliant"]:
            self.ueg.log_constitutional_event({
                "type": "post_validation_failure",
                "agent_id": context.agent_id,
                "violations": post_result["violations"]
            })
            return InterceptionResult(status="partial", output=output, warning="Output violates constitutional rules")

        # 4. Mandatory checkpoint
        checkpoint_id = f"CHK-{int(time.time() * 1000)}"
        self.ueg.log_constitutional_event({
            "type": "checkpoint",
            "checkpoint_id": checkpoint_id,
            "agent_id": context.agent_id,
            "action": context.action_type
        })

        return InterceptionResult(status="allowed", output=output, checkpoint_id=checkpoint_id)
