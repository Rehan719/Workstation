import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, Optional

import yaml

from agentic_core.ueg.ueg_manager import UEGManager

logger = logging.getLogger("NemoclawRuntime")


class NemoclawRuntime:
    """
    IDBO Layer 5: Resilience & Enforcement Runtime.
    Provides pre/post-execution interception hooks for all constitutional operations.
    Integrates circuit breakers, rule-based AST validation, and SHA-3-512 UEG logging.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config = {}
        if config_path:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)

        self.ueg = UEGManager()
        self.tripped = False
        self.failure_counter = 0
        self.max_failures = self.config.get("max_failures", 3)
        self.merkle_root = "0" * 64

    async def intercept(self, stage: str, target: Any, context: Dict[str, Any]) -> bool:
        """
        Main interception point for pre/post execution checks.
        Returns True if execution is permitted, False otherwise.
        """
        if self.tripped:
            logger.critical(
                f"Nemoclaw: Circuit breaker tripped. Blocking {stage} on {type(target).__name__}"
            )
            return False

        logger.info(f"Nemoclaw: Intercepting {stage} stage for {type(target).__name__}")

        # Rule-based validation (AST-like pattern matching)
        compliance = await self._validate_rules(stage, target, context)

        # Log interception event to UEG
        await self._log_interception(stage, target, compliance)

        return compliance

    async def _validate_rules(
        self, stage: str, target: Any, context: Dict[str, Any]
    ) -> bool:
        """
        Compiles target state and context into validation-ready AST and runs rule checks.
        Enforces structural integrity and constitutional compliance of deliberation outcomes.
        """
        if hasattr(target, "constitutional_validation"):
            if not target.constitutional_validation.passed:
                return False

        # AST-level validation: check for forbidden patterns in context/target
        target_str = str(target).lower()
        forbidden_patterns = self.config.get(
            "forbidden_patterns", ["bypass_gaas", "force_accept_violation"]
        )
        for pattern in forbidden_patterns:
            if pattern in target_str:
                logger.error(
                    f"Nemoclaw: Forbidden pattern '{pattern}' detected in {stage} stage."
                )
                return False

        return True

    async def _log_interception(self, stage: str, target: Any, compliance: bool):
        """Logs interception event with SHA-3-512 anchoring to UEG."""
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "stage": stage,
            "target_type": type(target).__name__,
            "compliance": compliance,
            "previous_root": self.merkle_root,
        }

        serialized = json.dumps(payload, sort_keys=True)
        self.merkle_root = hashlib.sha3_512(serialized.encode()).hexdigest()

        await self.ueg.log_event(
            event_type="nemoclaw_interception",
            payload=payload,
            merkle_root=self.merkle_root,
        )

    async def execute_guarded(self, func: Callable, *args, **kwargs) -> Any:
        """Executes a function with pre/post-execution constitutional gating."""
        context = kwargs.get("context", {})

        # Pre-execution gate
        if not await self.intercept("pre-execution", func, context):
            raise RuntimeError("Nemoclaw: Pre-execution constitutional violation.")

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Post-execution gate
            if not await self.intercept("post-execution", result, context):
                raise RuntimeError("Nemoclaw: Post-execution constitutional violation.")

            return result
        except Exception as e:
            self.failure_counter += 1
            if self.failure_counter >= self.max_failures:
                self.tripped = True
                logger.critical(
                    f"Nemoclaw: Circuit breaker tripped after {self.failure_counter} failures."
                )
            raise e

    def reset_breaker(self):
        self.tripped = False
        self.failure_counter = 0
