import logging
import asyncio
from typing import Dict, Any, List
from .goal_decomposer import GoalDecomposer
from .feature_extractor import FeatureExtractor
from .ml_ensemble import MLEnsemble
from .gate_calibrator import GateCalibrator
from .autonomy_manager import AutonomyManager
from .approval_manager import ApprovalManager
from .escalation_manager import EscalationManager
from .crypto_signer import CryptoSigner

logger = logging.getLogger(__name__)

class AdaptiveIncubationEngine:
    """
    ARTICLE CO: Dynamically Adaptive Incubation Mechanism.
    Orchestrates user-driven incubation with hybrid governance and ML-calibrated gates.
    """
    def __init__(self):
        self.decomposer = GoalDecomposer()
        self.extractor = FeatureExtractor()
        self.ensemble = MLEnsemble()
        self.calibrator = GateCalibrator()
        self.autonomy = AutonomyManager()
        self.approval = ApprovalManager()
        self.escalation = EscalationManager()
        self.signer = CryptoSigner()
        self.active_projects = {}

    async def incubate_project(self, user_goal: Dict[str, Any]):
        """CO-I: Goal-Driven Autonomy."""
        logger.info(f"CO: Incubating project for goal: {user_goal['title']}")

        # 1. Decompose goal into workflows
        workflows = self.decomposer.decompose(user_goal)

        for workflow in workflows:
            # CO-II: Fully Delegated Autonomy for operational execution
            if self.autonomy.is_delegated(workflow):
                await self._execute_autonomously(workflow)
            else:
                # CO-VI: Conditional Approval Gates
                approval = await self.approval.request_approval(workflow)
                if approval['status'] == 'approved':
                    await self._execute_with_oversight(workflow, approval['signature'])
                else:
                    logger.warning(f"Workflow {workflow['id']} rejected by user.")

    async def _execute_autonomously(self, workflow: Dict[str, Any]):
        logger.info(f"CO-II: Executing {workflow['id']} autonomously.")
        # Simulated execution
        await asyncio.sleep(0.1)

    async def _execute_with_oversight(self, workflow: Dict[str, Any], signature: str):
        logger.info(f"CO-VIII: Executing {workflow['id']} with cryptographic oversight.")
        # CO-VIII: Cryptographic Signing validation
        if self.signer.verify_signature(workflow, signature):
            await asyncio.sleep(0.1)
        else:
            logger.error(f"CO-VIII: Invalid signature for workflow {workflow['id']}")

    def calibrate_gates(self, content: str, user_signals: Dict[str, Any]):
        """CO-V: ML Ensemble Calibration."""
        # CO-III: Content Complexity Metrics
        content_metrics = self.extractor.extract_content_features(content)

        # CO-IV: User Behavior Signals
        behavior_metrics = self.extractor.extract_behavior_features(user_signals)

        # CO-V: Ensemble adjustment
        thresholds = self.ensemble.calibrate_thresholds(content_metrics, behavior_metrics)
        self.calibrator.apply_thresholds(thresholds)
        return thresholds
