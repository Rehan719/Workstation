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
# W588 (FU-409) — renamed from UnifiedConstitutionalInterceptorV16Omega, which the WIRED constitutional
# engine in gaas/v5 also carried: two live classes under one name, and this module is the only live
# importer of this one, so it is named for what it is to this path.
from agentic_core.governance.uci_interceptor import RecirculationPreflight

# ARTICLE 1137: Landauer-bounded computation (TFEL)
try:
    from core.transcendent_subsystems.tfel import ThermodynamicFreeEnergyLedger
except ImportError:
    class ThermodynamicFreeEnergyLedger:
        """The ledger is UNAVAILABLE, and this says so rather than inventing a budget.

        W546 (FU-329) — the stub this replaces returned `{"budget_remaining": 1e9}` from
        meter_operation: a billion bits of headroom, reported by a class that meters nothing. It was
        THINNER THAN ITS PRODUCER (no export_cycle_ledger, no budget, no E_min), so any caller reaching
        it got a different shape as well as a fabricated figure — and because the real module imports
        fine on a machine whose path includes the repository root, this branch runs on deployments where
        it does not and is exercised by nothing here. A stub that fabricates on the path least likely to
        be tested is the worst place to put one.

        Every field is three-state and the shape matches the real ledger's, so a caller cannot tell them
        apart by accident — only by reading `available`.
        """

        def __init__(self, **kwargs):
            self.available = False
            self.basis = ("NOT AVAILABLE: core.transcendent_subsystems.tfel could not be imported in "
                          "this deployment, so no information cost is metered and no Landauer floor is "
                          "computed. Nothing here is a measurement")

        def meter_operation(self, name, bits, bits_basis: str = ""):
            #  the real ledger's key set, so a caller cannot tell the two apart by shape — only by
            #  reading `available` or the basis, which is the honest discriminator
            return {"op": name, "metered": False, "entropy_bits": None,
                    "bits_basis": bits_basis or "not recorded: this ledger meters nothing",
                    "landauer_floor_joules": None,
                    "energy_basis": self.basis, "budget_remaining": None,
                    "basis": self.basis, "timestamp": None}

        def export_cycle_ledger(self, cid):
            return {"cycle_id": cid, "total_entropy_bits": None, "metered_operations": 0,
                    "compliance": None, "compliance_basis": self.basis}

logger = logging.getLogger(__name__)


def _payload_bits(obj: Any) -> tuple:
    """The MEASURED size in bits of what a stage actually handled, and a basis saying what that is.

    W546 (FU-234) — six stages passed hardcoded bit counts to the thermodynamic ledger (1e4 for sense,
    5e4 for intend, 5e5 for analyse, 2e5 for act, 5e4 for learn, 1e5 for reflect), each recorded BEFORE
    the stage did any work. So the figure could not have described what the stage processed even in
    principle, and the ledger's joules were arithmetic over an invented input — on a path the heartbeat
    runs every beat.

    WHAT THIS MEASURES AND WHAT IT DOES NOT. It is the serialised size of the stage's payload: a real,
    reproducible quantity. It is NOT the number of bits the computation erased, which is what Landauer's
    bound is about, and nothing here measures that. The basis travels with the figure so the ledger's
    floor is never read as the energy a stage drew.
    """
    #  EVERY LOOKUP IS DEFENSIVE, and a full suite paid for that. The six call sites read ctx["state"]
    #  directly, where the literals they replaced touched nothing — and a stage can be driven with a
    #  context that has no state key at all (test_w530 does exactly that), so the measurement raised
    #  KeyError on a path the literal had always survived. An absent payload is the honest answer
    #  there, which the None branch below already gives.
    #  AN ABSENT PAYLOAD IS NOT A SMALL ONE. Serialising None gives the four bytes of "null", so a stage
    #  whose input never arrived would have metered 32 bits — a figure reporting that four bytes were
    #  handled when nothing was. The ledger's meter_operation treats a None bit count as NOT METERED,
    #  which is the honest answer, and this is how it gets one. The first draft of this helper hit the
    #  case for real: three of the six stages were pointed at key names this module does not use
    #  ("analysis", "action", "learning" rather than "strategy", "act", "learn"), and each quietly
    #  metered 32 bits of nothing instead of failing.
    if obj is None:
        return None, ("NOT METERED: this stage's input payload is absent, so there is nothing to size. "
                      "Serialising it would report the four bytes of a null literal as data handled")
    try:
        import json
        _n = len(json.dumps(obj, default=str).encode("utf-8"))
        _how = "JSON-serialised"
    except Exception:
        _n = len(str(obj).encode("utf-8"))
        _how = "string-rendered (the payload would not serialise)"
    return float(_n * 8), (
        f"MEASURED: {_n} byte(s) of {_how} payload = {_n * 8} bits. This is the SIZE OF THE DATA this "
        f"stage handled, not the number of bits it erased — Landauer's bound concerns erasure and nothing "
        f"here measures that, so treat the ledger's figure as a floor over a measured payload size")

class _RefusingRegulator:
    """Refuses every mutation, and says why. W530 (FU-333).

    This replaces an always-approving stand-in. It reports NO confidence key at all: a regulator that
    approved nothing has no confidence to report, and emitting one was how a fabricated 0.95 reached a
    stored marker. When a real mutation regulator exists it replaces this object; until then, every
    adaptation is refused and the refusal is recorded, which is the honest state rather than a failure.
    """

    BASIS = ("no mutation regulator is configured, so no adaptation is approved. This is a REFUSAL, not an "
             "error: a gate with no implementation must block, and the always-approving stand-in that was "
             "here until W530 meant a self-modifying avatar whose only safety gate could not say no")

    async def validate_mutation(self, adaptation_type, before, after):
        return {"approved": False, "basis": self.BASIS, "adaptation_type": adaptation_type}


class _RefusingFixpoint:
    """Fails the stability constraint, and says why. W530 (FU-333).

    The stand-in it replaces always returned True, so the constraint passed vacuously. There is no
    fixpoint checker on this platform; claiming stability without one is the defect W526 removed from a
    digest that was named after a proof.
    """

    BASIS = ("no fixpoint checker is implemented, so recursive stability is NOT established and the "
             "constraint fails closed rather than passing on a constant")

    def verify(self, adaptation_type, before, after):
        return False


def clearance_inputs(user_id: Any, mode: str, drafts: Dict[str, Any]) -> Dict[str, Any]:
    """The RECORDED inputs clearance gates 2 and 3 read (FU-471, option 3). Shared by the loop and the chat route.

    Gate 2: the signatures on this learner's active approvals for this mode, and the quorum that mode needs.
    Gate 3: the Owner's goals, and each draft held with its measured properties; the emitted draft is named.
    Nothing here is supplied when its record does not exist: a missing record reaches the gate as missing.
    """
    from agentic_core.avatars.core import balance_objectives as _bo
    from agentic_core.avatars.core import ratifications as _rat
    _sig = _rat.signatures_for(str(user_id or ""), mode)
    _goals = _bo.get()
    return {"signatures": _sig["signatures"], "quorum_required": _sig["quorum_required"],
            "signatures_basis": _sig["basis"], "objectives": _goals["objectives"],
            "objectives_basis": _goals["basis"], "candidates": _bo.candidates(drafts),
            "emitted_candidate": "emitted" if "emitted" in drafts else None}


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
        #  W553 (FU-358) — registered at construction, for the reason given in clearance_chain:
        #  a guardrail a caller has to remember to ask for is not on the path.
        from agentic_core.validation.constitutional_validators import register_all as _register
        self.enforcement_registry = _register(self.enforcement)
        self.uci = RecirculationPreflight(ueg_logger=self.ueg)
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

        # Epigenetic gates. W530 (FU-333) — these were a regulator that ALWAYS returned approved:True
        # with a confidence of 0.95 and a verifier that always returned True, both named Mock, in this
        # constructor, behind no flag. EpigeneticMemoryEngine already refuses correctly — its
        # `approved` default is False, so a regulator returning nothing blocks — and that fail-closed
        # default was being bypassed by handing it something that cannot say no. A gate with no
        # implementation must BLOCK, so what is injected now refuses and says why.
        self.epigenetic_memory = EpigeneticMemoryEngine(
            ueg_logger,
            regulator=_RefusingRegulator(),
            lob_fixpoint=_RefusingFixpoint(),
        )

        self.override_active = False

    async def execute_cycle(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        The metabolic heart of the organism.
        Enforces latency assertions and 7-layer UCI interception.
        """
        if self.override_active:
            # W533 — this branch returned two keys while the others return seven, and it is the branch that
            # runs when the platform has been deliberately halted: the one least likely to be exercised
            # before it is needed. A caller indexing stages_measured here used to raise, and one using .get
            # would read a halted cycle as nought stages measured without being told it was halted at all.
            return {"status": "HALTED", "reason": "Constitutional override active",
                    "cycle_id": None, "output": None, "withheld_reason": None,
                    "stages": [], "stages_measured": 0,
                    "stages_basis": ("no stage ran: a constitutional override is active, so this is a "
                                     "HALTED cycle and not an unmeasured one")}

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
                # W533 — a cycle that measured all six stages and emitted NOTHING is not the same cycle as
                # one that delivered, so the record distinguishes them here too.
                "emission_withheld": bool(isinstance(ctx["state"].get("act"), dict)
                                          and ctx["state"]["act"].get("withheld")),
            })

            # W533 — a withheld emission must not report SUCCESS. Before this, a refusal could not reach
            # here at all (it raised), so there was no status for "the loop ran correctly and the gate said
            # no" -- the only vocabulary was success or crash.
            _act = ctx["state"]["act"] if isinstance(ctx["state"].get("act"), dict) else {}
            _withheld = bool(_act.get("withheld"))
            return {
                "status": "WITHHELD" if _withheld else "SUCCESS",
                "cycle_id": ctx["cycle_id"],
                "reason": _act.get("withheld_reason") if _withheld else None,
                "withheld_reason": _act.get("withheld_reason") if _withheld else None,
                "stages_basis": f"{len(stage_records)} stage(s) each measured on its own clock",
                "stages": stage_records,
                "stages_measured": len(stage_records),
                "output": ctx["state"]["act"]
            }

        except Exception as e:
            logger.error(f"Avatar metabolic cycle failure: {e}")
            await self.ueg.log_event("AVATAR_METABOLIC_FAILURE", {
                "id": ctx["cycle_id"],
                "error": str(e)
            })
            raise e

    def _numeric_state(self) -> Dict[str, float]:
        """The avatar's numeric state, flattened, for a drift baseline. Only recorded numbers; nothing derived."""
        out: Dict[str, float] = {}
        for dom, vals in (getattr(self.state, "skill_profile", None) or {}).items():
            for k, v in (vals or {}).items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    out[f"skill.{dom}.{k}"] = float(v)
        _e = getattr(self.state, "energy_budget_j", None)
        if isinstance(_e, (int, float)) and not isinstance(_e, bool):
            out["energy_budget_j"] = float(_e)
        return out

    async def _stage_sense(self, ctx: Dict):
        """Observe environment via VSB + tool interception."""
        _bits, _bits_basis = _payload_bits(ctx.get("input"))
        self.tfel.meter_operation("metabolic_sense", bits=_bits, bits_basis=_bits_basis)
        return await self.cognitive_orchestrator.process_engine("hoshiyari", ctx["input"], ctx)

    async def _stage_intend(self, ctx: Dict):
        """Form instructional intent via Niyyah ratification."""
        _bits, _bits_basis = _payload_bits((ctx.get("state") or {}).get("observation"))
        self.tfel.meter_operation("metabolic_intend", bits=_bits, bits_basis=_bits_basis)
        async def ratify():
            return await self.cognitive_orchestrator.process_engine("niyyah", ctx["state"]["observation"], ctx)
        return await self.uci.intercept({"intent": "ratify", "context": ctx}, ratify)

    async def _stage_analyze(self, ctx: Dict):
        """Mushāwara Deliberation: Selecting optimal strategy."""
        _bits, _bits_basis = _payload_bits((ctx.get("state") or {}).get("intent"))
        self.tfel.meter_operation("metabolic_analyze", bits=_bits, bits_basis=_bits_basis)
        mode_config = self.mode_manager.get_current_config()
        # Enforces ≥3 engine consensus for high-impact emissions
        return await self.cognitive_orchestrator.consult(
            {"task": "Strategy Synthesis", "context": ctx},
            list(mode_config.cognitive_weights.keys())
        )

    async def _stage_act(self, ctx: Dict):
        """Emission refinery + Tool effector."""
        _bits, _bits_basis = _payload_bits((ctx.get("state") or {}).get("strategy"))
        self.tfel.meter_operation("metabolic_act", bits=_bits, bits_basis=_bits_basis)

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
            # W547 (FU-233) — THE READER, FIXED WITH ITS WRITER. This attached the refinery's confidence
            # to EVERY EMISSION the loop produced, and that figure was 1.05 on every run: 0.90 plus 0.05
            # per refinement pass, over a loop that always ran three passes because the enforcement it
            # consults refuses while no validator is registered. It is None now, and a None beside a key
            # named for a confidence is an absence a reader would fill in — so the basis travels with it,
            # and the enforcement's real verdict travels too, which is the fact the figure was standing in
            # for all along.
            "vrpr_confidence": vrpr_res.confidence_score,
            "vrpr_confidence_basis": vrpr_res.confidence_basis,
            "vrpr_verification_passed": vrpr_res.verification_passed,
            "vrpr_verification_basis": vrpr_res.verification_basis,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # P3.28 — TAFAKKUR'S BASELINE IS A RECORDED STATE, never invented. The avatar's numeric state (its
        # learner skill profile and its energy budget) is snapshotted at the end of each cycle and the next
        # cycle's gate 4 measures drift FROM it. The first cycle has no baseline, and gate 4 says so.
        _current = self._numeric_state()
        ctx["baseline"] = getattr(self, "_drift_baseline", None)
        ctx["current"] = _current
        # FU-471 (Owner ruling 2026-10-06, option 3) — gates 2 and 3 get RECORDED inputs, never invented ones:
        # the learner's standing approvals for this mode (a request is not a signature), and the Owner's goals
        # over the drafts this loop actually holds, each measured from its text.
        ctx.update(clearance_inputs(ctx.get("user_id"), self.mode_manager.current_mode.value,
                                    {"draft": draft_text, "refined": vrpr_res.content,
                                     "emitted": personalized_text}))
        # 5-gate constitutional clearance mandatory per emission
        clearance_res = await self.clearance.validate_emission(emission, ctx)
        self._drift_baseline = _current
        if not clearance_res.passed:
            # W533 — this raised, so a gate DOING ITS JOB killed the organism's metabolic cycle: the three
            # stages after this one went unmeasured, and the refusal was filed as a metabolic FAILURE, which
            # files a governance decision as a malfunction. A refusal is an outcome. The emission is withheld
            # with the gate's reason, nothing is rendered, no tool runs, and the cycle carries on and is
            # measured. The content is moved off `text` rather than left on it, so no reader can mistake a
            # withheld draft for something that cleared.
            emission["withheld"] = True
            emission["withheld_reason"] = clearance_res.reason
            emission["withheld_draft"] = emission.pop("text", None)
            emission["text"] = None
            emission["gates"] = getattr(clearance_res, "gates", None)
            emission["withheld_basis"] = (
                "the constitutional clearance chain did not clear this emission, so it is withheld rather "
                "than delivered. This is the gate working, not a stage failing: the cycle continues and "
                "reports status WITHHELD, which is never SUCCESS")
            await self.ueg.log_event("AVATAR_EMISSION_WITHHELD", {
                "id": emission["id"],
                "cycle_id": ctx["cycle_id"],
                "reason": clearance_res.reason,
                "gates": getattr(clearance_res, "gates", None),
            })
            return emission

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
        _bits, _bits_basis = _payload_bits((ctx.get("state") or {}).get("act"))
        self.tfel.meter_operation("metabolic_learn", bits=_bits, bits_basis=_bits_basis)

        # W530 — A MISSING OUTCOME IS NOT A WIN. This read `.get("success", True)`, so a cycle whose
        # caller recorded no outcome was written into the user's skill profile as a success. Measured:
        # update_skill runs Bayesian Knowledge Tracing over a strict bool, so True inflates p_known and
        # False deflates it — there is no "not recorded" value to pass. A BKT update needs an
        # OBSERVATION, so with none we do not update at all and say so. This one accumulated: every
        # unmeasured cycle distorted a stored profile that later decisions read.
        recorded = ctx["user_context"].get("success")
        if isinstance(recorded, bool):
            await self.skill_profiler.update_skill(ctx["user_id"], ctx["domain"], recorded)
            skill_note = f"skill profile updated from a recorded outcome (success={recorded})"
        else:
            skill_note = ("skill profile NOT updated: this cycle recorded no outcome, and a Bayesian "
                          "update needs an observation. Counting an unmeasured cycle as either a success "
                          "or a failure would move a stored profile on no evidence")

        # W530 — NO PLACEHOLDER ADAPTATION IS PROPOSED. The `after` state it passed was a LITERAL
        # STRING where refined weights belong (the replaced wording is in the commit message, not here,
        # because a guard forbids it in source). The engine computes marker_id from sha256 of `after`,
        # so over that constant it was THE SAME MARKER
        # ID on every cycle for every user: a content hash that looked like content-addressing and bound
        # every marker to one placeholder. Nothing here computes refined weights, so nothing is proposed,
        # and the stage says that rather than submitting a mutation in name only.
        return {
            "skill": skill_note,
            "adaptation_proposed": False,
            "adaptation_basis": ("no adaptation was proposed: this stage has no mechanism that computes "
                                 "refined cognitive weights, and proposing a mutation whose new state is a "
                                 "placeholder is a mutation proposal in name only. Its marker id would be "
                                 "a hash of that placeholder, identical for every user and every cycle"),
            "regulator": _RefusingRegulator.BASIS,
        }

    async def _stage_reflect(self, ctx: Dict):
        """Post-instructional meta-audit."""
        _bits, _bits_basis = _payload_bits((ctx.get("state") or {}).get("learn"))
        self.tfel.meter_operation("metabolic_reflect", bits=_bits, bits_basis=_bits_basis)
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
