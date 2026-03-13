import logging
import time
from typing import Dict, Any, List, Optional
from enum import IntEnum

logger = logging.getLogger(__name__)

class GovernanceTier(IntEnum):
    T1_MINIMAL = 1
    T2_SANDBOX = 2
    T3_PAUSE = 3
    T4_ISOLATION = 4

class AgencyRiskIndex:
    """
    ARTICLE 601: ARI scores agents based on Autonomy, Adaptability, and Continuity.
    Determines governance tier and containment strategy.
    """
    def __init__(self):
        self.scores: Dict[str, Dict[str, int]] = {}

    def calculate_ari(self, agent_id: str, autonomy: int, adaptability: int, continuity: int) -> int:
        """Scores 0-3 on each dimension, maps to T1-T4."""
        total = autonomy + adaptability + continuity
        self.scores[agent_id] = {
            "autonomy": autonomy,
            "adaptability": adaptability,
            "continuity": continuity,
            "total": total
        }

        if total <= 2: return GovernanceTier.T1_MINIMAL
        if total <= 5: return GovernanceTier.T2_SANDBOX
        if total <= 7: return GovernanceTier.T3_PAUSE
        return GovernanceTier.T4_ISOLATION

class AgenticTelemetrySchema:
    """
    ARTICLE 601: ATS captures semantic cognitive and action events.
    """
    @staticmethod
    def create_event(agent_id: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "agent_id": agent_id,
            "event_type": event_type, # e.g., plan.start, tool.invoke, human.escalate
            "payload": payload,
            "timestamp": time.time(),
            "schema_version": "1.0.0"
        }

class RuntimeConstitutionalFramework:
    """
    ARTICLE 601: Unified Runtime Governance.
    Enforces MI9 (ARI, ATS, FSM, Drift, Containment) and arifOS Floors.
    """
    def __init__(self):
        self.ari = AgencyRiskIndex()
        self.conformance_engines: Dict[str, Any] = {} # AgentID -> FSM
        self.baseline_behavior: Dict[str, List[float]] = {}
        self.active_containments: Dict[str, GovernanceTier] = {}

    def verify_action(self, agent_id: str, event: Dict[str, Any]) -> bool:
        """Enforces FSM conformance and drift detection."""
        # ARTICLE 601: FSM Conformance (e.g., must have approval for sensitive actions)
        if agent_id in self.conformance_engines:
            fsm = self.conformance_engines[agent_id]
            current_state = fsm.get("state", "IDLE")
            event_type = event.get("event_type")

            # temporal policy: action.sensitive requires prior approve.action
            if event_type == "action.sensitive" and current_state != "APPROVED":
                logger.error(f"FSM_VIOLATION: {agent_id} attempted sensitive action in state {current_state}")
                return False

            # Update state
            if event_type == "approve.action":
                fsm["state"] = "APPROVED"
            elif event_type == "action.complete":
                fsm["state"] = "IDLE"

        # ARTICLE 601: Behavioral Drift Detection
        if agent_id in self.baseline_behavior:
            baseline = self.baseline_behavior[agent_id]
            current_latency = event.get("payload", {}).get("latency", 0.0)
            if current_latency > max(baseline) * 2.5: # Simple drift heuristic
                logger.warning(f"DRIFT_DETECTED: {agent_id} latency {current_latency} exceeds baseline")
                # In a real system, we'd trigger graduated containment here

        return True

    def apply_containment(self, agent_id: str, tier: GovernanceTier):
        """ARTICLE 601: Graduated Containment Strategy."""
        logger.warning(f"RUNTIME_GOVERNANCE: Applying {tier.name} to {agent_id}")
        self.active_containments[agent_id] = tier

    def check_arifos_floors(self, event: Dict[str, Any]) -> bool:
        """ARTICLE 601/610: Immutable arifOS Constitutional Floors."""
        # Floor 1: Non-violation of Dual-Purpose Foundation
        pas = event.get("payload", {}).get("pas", 1.0)
        if pas < 0.90:
            logger.error(f"FLOOR_VIOLATION: Purpose Alignment Score {pas} below floor for {event['agent_id']}")
            return False

        # Floor 2: Entropy constraint ΔS ≤ 0 (Peace verification)
        entropy_delta = event.get("payload", {}).get("entropy_delta", -0.1)
        if entropy_delta > 0:
            logger.error(f"FLOOR_VIOLATION: Entropy increase ΔS={entropy_delta} detected")
            return False

        # Floor 3: 888_HOLD human approval gating
        if event.get("event_type") == "action.irreversible":
            if not event.get("payload", {}).get("human_approved"):
                logger.error(f"RUNTIME_GOVERNANCE: 888_HOLD Violation for {event['agent_id']}")
                return False
        return True
