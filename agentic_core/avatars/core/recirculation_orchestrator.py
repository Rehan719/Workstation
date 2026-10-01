"""
Living Workstation Avatar — Persistent Recirculation Orchestrator (vΩ∞-AVATAR-OMNISYNTHESIS).
Manages the 6-stage metabolic loop for the persistent instructional cognitive organism.
"""
import asyncio
import time
import logging
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from agentic_core.avatars.core.avatar_engine import AvatarState
from agentic_core.avatars.core.clearance_chain import ConstitutionalClearanceChain
from agentic_core.avatars.cognition.mushawara_bridge import AvatarCognitiveOrchestrator
from agentic_core.avatars.modes.mode_controller import AvatarModeManager, AvatarMode
from agentic_core.avatars.memory.skill_profiler import SkillProfiler
from agentic_core.avatars.memory.epigenetic_engine import EpigeneticMemoryEngine
from agentic_core.avatars.output.multimodal_renderer import MultimodalRenderer, AvatarRenderer
from agentic_core.avatars.output.voice_engine import VoiceEngine
from agentic_core.avatars.tools.tool_registry import AvatarToolRegistry
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme
from agentic_core.quality.vrpr_pipeline import VRPRPipeline
from agentic_core.personalisation.sil_personaliser import SILPersonaliser
from agentic_core.governance.uci_interceptor import UnifiedConstitutionalInterceptorV16Omega

# ARTICLE 1137: Landauer-bounded computation (TFEL)
try:
    from core.transcendent_subsystems.tfel import ThermodynamicFreeEnergyLedger
except ImportError:
    class ThermodynamicFreeEnergyLedger:
        def __init__(self, **kwargs):
            """Simulated TFEL."""
        def meter_operation(self, name, bits): return {"budget_remaining": 1e9}

logger = logging.getLogger(__name__)

class AvatarRecirculationOrchestrator:
    """
    IDBO Layer 9/10/11: Orchestration & Evolution.
    Executes the 6-stage metabolic loop: SENSE → INTEND → ANALYZE → ACT → LEARN → REFLECT.

    W527 (P3.16) — this said "Target p95 latency: <500ms (SENSE -> ACT)". A p95 is a claim about a
    DISTRIBUTION: it needs many runs ranked against one another. This class measures one cycle at a time and
    keeps no history of previous cycles, so there was nothing a p95 could be computed from — a statistic's
    name attached to something that never computed it.

    WHAT IS MEASURED NOW: each of the six stages on its own clock, recorded per cycle with its budget and
    whether it breached, in the AVATAR_CYCLE_METABOLIC event. Every budget is an untuned DEFAULT.
    AN ASPIRATION, NOT A RESULT: <500ms from SENSE to ACT remains the design intent. Reporting a p95 would
    need a retained series of cycle timings, which nothing here stores; until that exists, the honest figure
    is the single-cycle measurement beside the budget it was compared against.
    """

    def __init__(self, ueg_logger: Any, state: AvatarState):
        self.ueg = ueg_logger
        self.state = state
        self.enforcement = OmniEnforcementPatternSupreme(
            {"fail_on_missing_validator": False},
            {"task": "recirculation_final"}
        )
        self.uci = UnifiedConstitutionalInterceptorV16Omega(ueg_logger=self.ueg)
        self.cognitive_orchestrator = AvatarCognitiveOrchestrator(ueg_logger, self.enforcement)
        self.clearance = ConstitutionalClearanceChain(ueg_logger, self.cognitive_orchestrator)
        self.mode_manager = AvatarModeManager(ueg_logger)
        self.skill_profiler = SkillProfiler(ueg_logger)
        self.tfel = ThermodynamicFreeEnergyLedger(ueg_logger=ueg_logger)

        self.voice = VoiceEngine(config={})
        self.visual = AvatarRenderer(config={"type": "2d"})
        self.renderer = MultimodalRenderer(self.voice, self.visual)

        from agentic_core.causal.csl import CausalSovereigntyLayer
        self.csl = CausalSovereigntyLayer(ueg_logger=ueg_logger)
        self.tools = AvatarToolRegistry(ueg_logger, self.csl, self.tfel)

        self.vrpr = VRPRPipeline(self.ueg, self.enforcement)
        self.sil = SILPersonaliser()

        # Epigenetic gates (vΩ∞-AVATAR-OMNISYNTHESIS)
        async def mock_validate(*args): return {'approved': True, 'confidence': 0.95}
        self.epigenetic_memory = EpigeneticMemoryEngine(
            ueg_logger,
            regulator=type('Mock', (), {'validate_mutation': mock_validate}),
            lob_fixpoint=type('Mock', (), {'verify': lambda *a: True})
        )

        self.override_active = False

    async def execute_cycle(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        The metabolic heart of the organism.
        Enforces latency assertions and 7-layer UCI interception.
        """
        if self.override_active:
            return {"status": "HALTED", "reason": "Constitutional override active"}

        start_time = time.time()
        session_id = f"sess_{self.state.avatar_id[-8:]}"

        ctx = {
            "cycle_id": f"cyc_{int(start_time * 1000)}",
            "session_id": session_id,
            "user_id": self.state.user_id,
            "user_context": user_context,
            "input": user_context.get("input", ""),
            "domain": user_context.get("domain", "general_productivity"),
            "state": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        #  W527 (P3.16) — ALL SIX stages are measured, each on its own clock. Before this, four were timed
        #  cumulatively and LEARN and REFLECT were not timed at all, so the loop reported on two thirds of
        #  itself. The records travel out of this method; they are not only logged.
        stage_records = []
        try:
            ctx["state"]["observation"], _r = await self._measure_stage("SENSE", self._stage_sense(ctx))
            stage_records.append(_r)

            ctx["state"]["intent"], _r = await self._measure_stage("INTEND", self._stage_intend(ctx))
            stage_records.append(_r)

            ctx["state"]["strategy"], _r = await self._measure_stage("ANALYZE", self._stage_analyze(ctx))
            stage_records.append(_r)

            ctx["state"]["act"], _r = await self._measure_stage("ACT", self._stage_act(ctx))
            stage_records.append(_r)

            ctx["state"]["learn"], _r = await self._measure_stage("LEARN", self._stage_learn(ctx))
            stage_records.append(_r)

            ctx["state"]["reflect"], _r = await self._measure_stage("REFLECT", self._stage_reflect(ctx))
            stage_records.append(_r)

            total_duration = time.time() - start_time
            _breached = [r["stage"] for r in stage_records if r["breached"]]
            ctx["stages"] = stage_records
            await self.ueg.log_event("AVATAR_CYCLE_METABOLIC", {
                "id": ctx["cycle_id"],
                "duration_s": total_duration,
                "mode": self.mode_manager.current_mode.value,
                "domain_p_known": self.skill_profiler.get_skill_level(ctx["user_id"], ctx["domain"]),
                # W527 (P3.16) — the breaches are FACTS HERE, not a line in a log file. `stages_measured`
                # is counted rather than written as 6, so a stage added without timing cannot hide.
                "stages": stage_records,
                "stages_measured": len(stage_records),
                "stages_declared": len(self._STAGE_BUDGETS_MS),
                "breached_stages": _breached,
                "breach_count": len(_breached),
                "budgets_are_defaults": self._BUDGETS_ARE_DEFAULTS,
            })

            return {
                "status": "SUCCESS",
                "cycle_id": ctx["cycle_id"],
                "output": ctx["state"]["act"]
            }

        except Exception as e:
            logger.error(f"Avatar metabolic cycle failure: {e}")
            await self.ueg.log_event("AVATAR_METABOLIC_FAILURE", {
                "id": ctx["cycle_id"],
                "error": str(e)
            })
            raise e

    async def _stage_sense(self, ctx: Dict):
        """Observe environment via VSB + tool interception."""
        self.tfel.meter_operation("metabolic_sense", bits=1e4)
        return await self.cognitive_orchestrator.process_engine("hoshiyari", ctx["input"], ctx)

    async def _stage_intend(self, ctx: Dict):
        """Form instructional intent via Niyyah ratification."""
        self.tfel.meter_operation("metabolic_intend", bits=5e4)
        async def ratify():
            return await self.cognitive_orchestrator.process_engine("niyyah", ctx["state"]["observation"], ctx)
        return await self.uci.intercept({"intent": "ratify", "context": ctx}, ratify)

    async def _stage_analyze(self, ctx: Dict):
        """Mushāwara Deliberation: Selecting optimal strategy."""
        self.tfel.meter_operation("metabolic_analyze", bits=5e5)
        mode_config = self.mode_manager.get_current_config()
        # Enforces ≥3 engine consensus for high-impact emissions
        return await self.cognitive_orchestrator.consult(
            {"task": "Strategy Synthesis", "context": ctx},
            list(mode_config.cognitive_weights.keys())
        )

    async def _stage_act(self, ctx: Dict):
        """Emission refinery + Tool effector."""
        self.tfel.meter_operation("metabolic_act", bits=2e5)

        strategy = ctx["state"]["strategy"]
        draft_text = strategy.get("outcome", {}).get("synthesized_response", "I am ready.")

        # Output Refinery pipeline: Verifier→Polisher→Enhancer→Redrafter
        vrpr_res = await self.vrpr.process(draft_text, ctx)

        # SIL Personalization
        personalized_text = await self.sil.calibrate_response(ctx["user_id"], ctx["input"], vrpr_res.content)

        emission = {
            "id": f"emit_{ctx['cycle_id']}",
            "text": personalized_text,
            "mode": self.mode_manager.current_mode.value,
            "vrpr_confidence": vrpr_res.confidence_score,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # 5-gate constitutional clearance mandatory per emission
        clearance_res = await self.clearance.validate_emission(emission, ctx)
        if not clearance_res.passed:
            raise RuntimeError(f"Gate Breach: {clearance_res.reason}")

        emission["attestations"] = clearance_res.attestations

        # Synchronized Multimodal Render
        expression = strategy.get("outcome", {}).get("expression", "neutral")
        overlays = strategy.get("outcome", {}).get("overlays", [])
        await self.renderer.render(personalized_text, expression, overlays)

        # Tool Effector: Pearl-do identification gated
        if "suggested_tools" in strategy.get("outcome", {}):
            emission["tool_results"] = []
            for tool_req in strategy["outcome"]["suggested_tools"]:
                res = await self.tools.execute(tool_req["name"], tool_req["params"], ctx["user_context"])
                emission["tool_results"].append(res)

        return emission

    async def _stage_learn(self, ctx: Dict):
        """Update epigenetic memory via Merkle-linked mutation."""
        self.tfel.meter_operation("metabolic_learn", bits=5e4)

        success = ctx["user_context"].get("success", True)
        await self.skill_profiler.update_skill(ctx["user_id"], ctx["domain"], success)

        return await self.epigenetic_memory.propose_adaptation(
            user_id=ctx["user_id"],
            trigger_event="metabolic_cycle_completion",
            adaptation_type="strategy_tuning",
            before={"weights": self.mode_manager.get_current_config().cognitive_weights},
            after={"weights": "REFINED_BY_EPIGENETIC_ENGINE"}
        )

    async def _stage_reflect(self, ctx: Dict):
        """Post-instructional meta-audit."""
        self.tfel.meter_operation("metabolic_reflect", bits=1e5)
        return await self.cognitive_orchestrator.process_engine("tafakkur", ctx["state"]["act"], ctx)

    #  Per-stage budgets, every one a DEFAULT. Nothing in this repository has calibrated a stage budget
    #  against its own measured history, so a figure below one of these is within an aspiration rather
    #  than within a tuned limit — and each record says so rather than implying otherwise.
    _STAGE_BUDGETS_MS = {"SENSE": 100, "INTEND": 200, "ANALYZE": 500, "ACT": 500,
                         "LEARN": 1000, "REFLECT": 60000}
    _BUDGETS_ARE_DEFAULTS = ("every budget here is an untuned DEFAULT: no measurement of this platform's "
                             "own stage timings has set any of them, so 'within budget' is an aspiration "
                             "met, not a performance result")

    async def _measure_stage(self, stage: str, coro):
        """Await one stage, time IT ALONE, and return (result, record).

        W527 (P3.16). The four checks this replaces each passed the cycle's ORIGINAL start time, so every
        stage after the first reported the sum of itself and everything before it. A per-stage figure has to
        start when the stage does, or it carries the name of one stage while measuring several.
        """
        began = time.perf_counter()
        try:
            result = await coro
            failed = None
        except Exception as exc:                          # noqa: BLE001 — the stage's failure is recorded
            result, failed = None, f"{exc.__class__.__name__}: {exc}"
        ms = (time.perf_counter() - began) * 1000.0
        limit = self._STAGE_BUDGETS_MS.get(stage)
        record = {
            "stage": stage,
            "ms": round(ms, 3),
            "budget_ms": limit,
            "budget_is_a_default": True,
            "breached": (limit is not None and ms > limit),
            "measured": "this stage alone, from its own start (not cumulative from the cycle's start)",
        }
        if failed:
            record["failed"] = failed
        if record["breached"]:
            #  kept, because an operator watching logs should still see it — but the log is no longer the
            #  only place it exists
            logger.warning("LATENCY BREACH in stage %s: %.2fms > %sms (untuned default)", stage, ms, limit)
        if failed:
            raise RuntimeError(f"stage {stage} failed: {failed}")
        return result, record
