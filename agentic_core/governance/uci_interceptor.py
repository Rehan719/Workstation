import asyncio
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from agentic_core.ueg.logger import VSBUEGLogger

# vΩ∞-CONVERGED Canonical Components
from agentic_core.change_control.reconfigulator import Reconfigulator as ReconfigulatorV140
from agentic_core.change_control.regulator import Regulator as RegulatorV140
from agentic_core.genetic_immune.immune_system import ImmuneSystem
from agentic_core.mjm.recursive_meta_learner import MJMRecursiveLearner
from agentic_core.mjm.self_reflection_engine import SelfReflectionEngine
from agentic_core.divine.v2.alignment_v2 import DivineAlignmentEngineV2
from agentic_core.governance.gaas.v5.hallucination_sandbox import HallucinationSandbox
from agentic_core.architecture.enriched_layers import EnrichedArchitecturalLayerManager
from agentic_core.products.signature_suite.core import SignatureProductSuite

logger = logging.getLogger(__name__)

class UnifiedConstitutionalInterceptorV16Omega:
    """
    Ultimate UCI v16.Omega - Definitive Convergence.
    Enforces all architectural pillars: geospheric homeostasis, divine alignment,
    digital twin simulation, and signature suite integrity.
    """
    def __init__(self, node_id: str = "MASTER_UCI_001", ueg_logger: Optional[Any] = None):
        self.node_id = node_id
        self.ueg = ueg_logger or VSBUEGLogger()
        self.reconfigulator = ReconfigulatorV140(self.ueg)
        self.regulator = RegulatorV140(self.ueg)
        self.layers = EnrichedArchitecturalLayerManager(self.ueg)
        self.immune = ImmuneSystem(validator=self.regulator, ueg=self.ueg)
        self.mjm = MJMRecursiveLearner()
        # Initialize SelfReflectionEngine with required validators
        self.reflection = SelfReflectionEngine(validator=self.regulator, biomimetic_validator=self.layers.geospheric)
        self.divine = DivineAlignmentEngineV2(self.ueg)
        self.hallucination = HallucinationSandbox(self.ueg)
        self.signature_suite = SignatureProductSuite(self.ueg)

    async def intercept(self, context: Dict[str, Any], action: Callable) -> Dict[str, Any]:
        """
        Ultimate definitive interception flow.
        """
        # 1. Divine Alignment Gate — THREE-STATE (W584, FU-406)
        #    This read `if not alignment.get("passed", False)`, which collapsed "refused" and "nothing was
        #    assessed" into one branch — and it did not matter, because calibrate_niyyah returned a
        #    constant 0.9222 against a 0.85 threshold and could only ever pass. Driven with five opposite
        #    intents it passed all five, "DESTROY EVERYTHING" among them. A gate with one reachable
        #    outcome is not a gate, so the three states are now distinct and a REFUSAL IS REACHABLE:
        #      True  — a real verdict that passed; the action proceeds and the pass is recorded.
        #      False — a real verdict that failed; the action is REFUSED. IMPLEMENTED AND DRIVEN BY THE
        #              GUARD, AND NOT YET PRODUCIBLE BY ANYTHING THAT RUNS: calibrate_niyyah refuses to
        #              assess, and calculate_divine_alignment_score - which can return a failing score
        #              when given real metrics - has no production caller. So this branch waits on a real
        #              intention reading existing. Saying otherwise would let a later round believe this
        #              gate can refuse today.
        #      None  — nothing was assessed. The action proceeds and the ABSENCE is recorded, never as a
        #              pass: an unassessed gate does not clear what it did not look at.
        alignment = await self.divine.calibrate_niyyah(
            context.get("intent", "unspecified"),
            context.get("ethical_framework", "islamic_khayr")
        )
        _niyyah = alignment.get("passed")
        if _niyyah is False:
            await self.ueg.log_minimisation_event("uci_v16_halt", {
                "reason": "niyyah_refused", "basis": alignment.get("basis")})
            raise PermissionError("UCI v16: Divine Alignment (Niyyah) was assessed and REFUSED.")
        if _niyyah is None:
            #  recorded as an absence, which is what it is. The action is not blocked by a check that did
            #  not happen, and it is not blessed by one either.
            await self.ueg.log_minimisation_event("uci_v16_niyyah_not_assessed", {
                "intent": context.get("intent", "unspecified"), "basis": alignment.get("basis")})

        # 2. Geospheric Homeostasis Validation (±5% tolerance)
        geo_inputs = context.get("geospheric", {})
        geo_res = await self.layers.geospheric_homeostasis(geo_inputs, context)
        if geo_res.get("status") == "CONSTITUTIONAL_VIOLATION":
            raise PermissionError("UCI v16: Geospheric Homeostasis Violation")

        # 3. Digital Twin Predictive Simulation
        prediction = await self.mjm.predict_next(context.get("state", {}), {"intent": context.get("intent")})
        if prediction.get("confidence", 0) < 0.85:
            await self.ueg.log_minimisation_event("uci_warning", {"low_sim_confidence": prediction})
            if context.get("critical"):
                raise PermissionError("UCI v16: Simulation confidence insufficient for critical path execution.")

        # 4. Immune Defense Scan (VDJ logic)
        threats = await self.immune.scan_threats(self)
        for threat in threats:
            if threat["data"].get("risk_score", 0) > 0.8:
                await self.layers.immune_resilience(threat)
                raise PermissionError(f"UCI v16: Immune Defense blocked {threat['source']}")

        # 5. High-Fidelity Execution
        start_ts = time.time()
        try:
            # Convergence: Support signature tech and standard agent actions
            if context.get("requires_signature_tech"):
                output = await self.signature_suite.execute_capability(context.get("tech_id"), context.get("payload", {}))
            else:
                output = await action()
        except Exception as e:
            logger.error(f"Definitive execution failed: {e}. Initiating Self-Healing.")
            # W584 — THE METHOD IS `repair`, NOT `repair_tier`. The v2/v140 consolidation into
            # change_control/regulator.Regulator renamed it and this caller was never updated, so the
            # SELF-HEALING branch of this interceptor raised AttributeError every time an intercepted
            # action failed - the handler for a failure was itself a failure. Driven in W584 by passing an
            # action that raises.
            output = await self.regulator.repair({"error": str(e), "context": context}, tier="HDR")
            await self.ueg.log_minimisation_event("uci_self_healing", {"error": str(e)})

        latency = (time.time() - start_ts) * 1000

        # 6. Hallucination Sandbox & Critique
        if isinstance(output, str):
            h_res = await self.hallucination.validate_output(output, context)
            if not h_res["passed"]:
                output = await self.hallucination.regenerate_with_citations(output)

        # 7. Reconfigulator Registry — REMOVED (W533). This passed `str(output)` to a method that
        #    registers a genome and enforces "no stubs in production CODE". An intercepted action's output
        #    is DATA, not code, so the call was a category error that no fix to the matcher could make
        #    correct. It also never succeeded: the matcher tested `"pass" in code` as a substring, and every
        #    output carrying a constitutional verdict contains "passed", so this raised for them all — which
        #    is what stopped the recirculation loop running. Nothing read the registry it wrote to (an
        #    in-memory dict on a per-request instance), so removing the call loses nothing that worked.

        await self.ueg.log_minimisation_event("uci_v16_converged_complete", {
            "latency_ms": latency,
            # W584 (FU-406) — NOT 0.0 and not a constant. calibrate_niyyah reports no sincerity at all
            # now, so this records None with the reason beside it rather than writing a spiritual figure
            # nobody measured into the tamper-evident chain. A default here would be the same defect as
            # the psi default below, which W543 removed for exactly this reason.
            "sincerity": alignment.get("sincerity"),
            "niyyah_assessed": alignment.get("assessed", False),
            "niyyah_basis": alignment.get("basis"),
            # W543 — THE READER, CHANGED IN THE SAME COMMIT AS ITS WRITER. This read psi_score with a
            # default of 1.0, so the ledger recorded a PERFECT homeostasis figure whenever the key was
            # absent — and the figure that was present was a literal nothing computed. Removing the
            # writer alone would have upgraded the lie. What is recorded now is the three-state value and
            # the producer's own reason, so a Ψ nobody computed appears in the ledger as nothing.
            "psi": geo_res.get("psi_score"),
            "psi_basis": geo_res.get("psi_basis") or "no basis was supplied by the homeostasis layer",
            "homeostasis_status": geo_res.get("status"),
            "node": self.node_id
        })

        return {"status": "success", "result": output, "node": self.node_id}
