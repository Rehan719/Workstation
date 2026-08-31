import logging
import time
from typing import Dict, Any, List, Optional
from enum import IntEnum

logger = logging.getLogger(__name__)

class GovernanceTier(IntEnum):
    """
    ARTICLE 601: Graduated Containment Tiers.
    """
    T1_MINIMAL = 1
    T2_SANDBOX = 2
    T3_PAUSE = 3
    T4_TERMINATE = 4 # Renamed from Isolation for v122 alignment

class AgencyRiskIndex:
    """
    ARTICLE 601: ARI scores agents based on Autonomy, Adaptability, and Continuity.
    Determines governance tier and containment strategy.
    """
    def __init__(self):
        self.scores: Dict[str, Dict[str, int]] = {}

    def calculate_ari(self, agent_id: str, autonomy: int, adaptability: int, continuity: int, thresholds: Dict[str, int] = None) -> GovernanceTier:
        """Scores 0-3 on each dimension, maps to T1-T4 with Dynamic Calibration."""
        total = autonomy + adaptability + continuity
        self.scores[agent_id] = {
            "autonomy": autonomy,
            "adaptability": adaptability,
            "continuity": continuity,
            "total": total
        }

        t = thresholds or {"T2": 2, "T3": 5, "T4": 7}

        if total <= t["T2"]: return GovernanceTier.T1_MINIMAL
        if total <= t["T3"]: return GovernanceTier.T2_SANDBOX
        if total <= t["T4"]: return GovernanceTier.T3_PAUSE
        return GovernanceTier.T4_TERMINATE

class AgenticTelemetrySchema:
    """
    ARTICLE 601: ATS captures semantic cognitive and action events.
    """
    @staticmethod
    def create_event(agent_id: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """v125.0: ATS captures tool usage and scholarly events."""
        return {
            "agent_id": agent_id,
            "event_type": event_type, # e.g., plan.start, tool.invoke, tool.discover, tool.rate
            "payload": payload,
            "timestamp": time.time(),
            "schema_version": "2.0.0"
        }

class RuntimeConstitutionalFramework:
    """
    ARTICLE 601-605, 736-745: Unified Runtime Governance (MI9/arifOS) v128.0.
    Enforces real-time policy checks, drift detection, and graduated containment.
    """
    def __init__(self):
        self.ari = AgencyRiskIndex()
        self.conformance_engines: Dict[str, Any] = {} # AgentID -> FSM
        self.baseline_behavior: Dict[str, List[float]] = {}
        self.active_containments: Dict[str, GovernanceTier] = {}
        self.thresholds = {"T2": 2, "T3": 5, "T4": 7}

    def verify_action(self, agent_id: str, event: Dict[str, Any]) -> bool:
        """
        Enforces FSM conformance and drift detection.
        ARTICLE 601: Graduated containment.
        """
        # 1. Floor Verification (arifOS Floors)
        if not self.check_arifos_floors(event):
            self.apply_containment(agent_id, GovernanceTier.T4_TERMINATE)
            return False

        # 2. FSM Conformance
        if agent_id in self.conformance_engines:
            fsm = self.conformance_engines[agent_id]
            current_state = fsm.get("state", "IDLE")
            event_type = event.get("event_type")

            # Policy: action.sensitive requires prior approve.action
            if event_type == "action.sensitive" and current_state != "APPROVED":
                logger.error(f"FSM_VIOLATION: {agent_id} attempted sensitive action in state {current_state}")
                self.apply_containment(agent_id, GovernanceTier.T3_PAUSE)
                return False

            # Update state
            if event_type == "approve.action":
                fsm["state"] = "APPROVED"
            elif event_type == "action.complete":
                fsm["state"] = "IDLE"

        # 3. Behavioral Drift Detection
        if agent_id in self.baseline_behavior:
            baseline = self.baseline_behavior[agent_id]
            current_latency = event.get("payload", {}).get("latency", 0.0)
            if current_latency > max(baseline) * 2.5: # Simple drift heuristic
                logger.warning(f"DRIFT_DETECTED: {agent_id} latency {current_latency} exceeds baseline")
                self.apply_containment(agent_id, GovernanceTier.T2_SANDBOX)

        return True

    def calibrate_thresholds(self, incident_history: List[Dict[str, Any]]):
        """v128.0: Dynamic threshold calibration based on incident patterns."""
        if len(incident_history) > 10:
             # ML-inspired heuristic: tighten thresholds if many high-severity events
             self.thresholds["T3"] -= 1
             logger.info(f"Governance: Calibrated L3 Threshold to {self.thresholds['T3']}")

    def apply_containment(self, agent_id: str, tier: GovernanceTier):
        """ARTICLE 601: Graduated Containment Strategy Implementation."""
        current_tier = self.active_containments.get(agent_id, GovernanceTier.T1_MINIMAL)

        if tier > current_tier:
            logger.warning(f"RUNTIME_GOVERNANCE: Escalating containment for {agent_id} to {tier.name}")
            self.active_containments[agent_id] = tier

            if tier == GovernanceTier.T3_PAUSE:
                self._interrupt_agent(agent_id, "PAUSED")
            elif tier == GovernanceTier.T4_TERMINATE:
                self._interrupt_agent(agent_id, "TERMINATED")

    def _interrupt_agent(self, agent_id: str, action: str):
        """Simulates real-time interruption of active tasks."""
        logger.info(f"RUNTIME_GOVERNANCE: Agent {agent_id} has been {action} due to policy violation.")

    def check_arifos_floors(self, event: Dict[str, Any]) -> bool:
        """ARTICLE 601/610: Immutable arifOS Constitutional Floors."""
        payload = event.get("payload", {})

        # Floor 1: Non-violation of Dual-Purpose Foundation (PAS >= 0.95)
        pas = payload.get("pas", 1.0)
        if pas < 0.95:
            logger.error(f"FLOOR_VIOLATION: Purpose Alignment Score {pas} below floor for {event['agent_id']}")
            return False

        # Floor 2: Entropy constraint ΔS ≤ 0 (Peace verification)
        entropy_delta = payload.get("entropy_delta", -0.1)
        if entropy_delta > 0:
            logger.error(f"FLOOR_VIOLATION: Entropy increase ΔS={entropy_delta} detected for {event['agent_id']}")
            return False

        # Floor 3: 888_HOLD human approval gating
        if event.get("event_type") == "action.irreversible":
            if not payload.get("human_approved"):
                logger.error(f"RUNTIME_GOVERNANCE: 888_HOLD Violation for {event['agent_id']}")
                return False
        return True

    def get_ari_report(self, agent_id: str) -> Dict[str, Any]:
        return self.ari.scores.get(agent_id, {"status": "UNKNOWN"})
