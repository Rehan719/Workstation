"""
Avatar Tool Registry (vΩ∞-LIVING-AVATAR-FINAL).
Constitutional Effector Gate with Pearl-do Causal Proofs.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import hashlib
import json
from datetime import datetime, timezone
import logging

from agentic_core.tools.registry import ToolRegistry as CoreToolRegistry
from src.organism.python.organs.openclaw_adapter import OpenClawAdapter
from src.organism.python.neural.event_bus import AsyncEventBus

logger = logging.getLogger(__name__)

@dataclass
class ToolResult:
    tool_name: str
    success: bool
    output: Any
    entropy_cost: float
    constitutional_attestation: str
    causal_proof: Optional[str]

class AvatarToolRegistry:
    """
    IDBO Layer 4: Regulation / UCI Tool Effector.
    Enforces the following invariants for all external modifications:
    1. Tier-based access control.
    2. Causal Identifiability ( Pearl-do calculus).
    3. Thermodynamic Free Energy accounting.
    4. Cryptographic Merkle-linkage in UEG.
    """
    ALLOWED_TOOLS = {
        "file_search": {"tiers": ["free", "standard", "advanced"], "consequential": False},
        "web_search": {"tiers": ["standard", "advanced"], "consequential": False},
        "document_generation": {"tiers": ["standard", "advanced"], "consequential": True},
        "code_execution": {"tiers": ["advanced"], "consequential": True},
        "task_runner": {"tiers": ["standard", "advanced"], "consequential": True},
        "calendar": {"tiers": ["free", "standard", "advanced"], "consequential": False}
    }

    def __init__(self, ueg_logger: Any, csl_layer: Any, tfel_ledger: Any):
        self.ueg = ueg_logger
        self.csl = csl_layer
        self.tfel = tfel_ledger

        # Integration with core workstation limbs
        self.core_registry = CoreToolRegistry()
        self._register_default_tools()
        self.bus = AsyncEventBus() # For local dispatch
        self.limbs = OpenClawAdapter(self.core_registry, self.bus)

    def _register_default_tools(self):
        """Pre-registers standard tools for the avatar effector."""
        for tool in self.ALLOWED_TOOLS:
            self.core_registry.register_tool(
                name=tool,
                category="avatar_effector",
                capabilities=["metabolic_action"],
                config={}
            )

    async def execute(self, tool_name: str, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """
        Execute tool with 5-phase validation flow.
        """
        user_tier = context.get("tier", "free")
        user_id = context.get("user_id", "anonymous")

        # Phase 1: Structural (Tier & Presence)
        if tool_name not in self.ALLOWED_TOOLS:
            raise ValueError(f"CRITICAL: Tool '{tool_name}' unregistered.")

        tool_def = self.ALLOWED_TOOLS[tool_name]
        if user_tier not in tool_def["tiers"]:
            raise PermissionError(f"Tier Violation: {tool_name} requires {tool_def['tiers'][0]}+")

        # Phase 2: Governance (Causal Sovereignty)
        causal_proof = None
        if tool_def["consequential"]:
            causal_proof = await self.csl.generate_identifiability_proof(
                action={"tool": tool_name, "params": params},
                context=context
            )
            if not causal_proof:
                await self.ueg.log_event("CAUSAL_SOVEREIGNTY_BREACH", {"tool": tool_name})
                raise RuntimeError("Pearl-do verification failed: Unidentifiable causal path.")

        # Phase 3: Physical (Thermodynamic Metering)
        # Metering bits for the effector operation
        metering = self.tfel.meter_operation(f"effector_{tool_name}", bits=2e5)
        entropy_cost = 500.0 # Standard bit cost

        # Phase 4: Execution (Sovereign Dispatch through OpenClaw)
        logger.info(f"Avatar Effector: {tool_name} requested by {user_id}")
        try:
            action_id = f"act_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}"
            execution_event = await self.limbs.execute_action(action_id, tool_name, params)

            success = execution_event.result.status == "SUCCESS"
            output = execution_event.result.output if success else execution_event.result.error

        except Exception as e:
            output = str(e)
            success = False
            logger.error(f"Execution failure: {tool_name} -> {e}")

        # Phase 5: Recursive (UEG Merkle Linkage)
        attestation_payload = {
            "t": tool_name,
            "p": hashlib.sha256(json.dumps(params, sort_keys=True).encode()).hexdigest(),
            "ts": datetime.now(timezone.utc).isoformat(),
            "s": "SUCCESS" if success else "FAILED",
            "csl": causal_proof
        }
        attestation = hashlib.sha3_512(json.dumps(attestation_payload, sort_keys=True).encode()).hexdigest()

        await self.ueg.log_event("TOOL_METABOLIC_ACTION", {
            "tool": tool_name,
            "success": success,
            "attestation": attestation,
            "entropy": entropy_cost,
            "causal_proof": causal_proof
        })

        return ToolResult(
            tool_name=tool_name,
            success=success,
            output=output,
            entropy_cost=0.5,
            constitutional_attestation=attestation,
            causal_proof=causal_proof
        )

import time
