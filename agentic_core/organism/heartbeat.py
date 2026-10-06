"""
Organism Heartbeat — the continuous-autonomy scheduler.

Makes Workstation IDBO run itself continuously: a circadian-modulated background
rhythm that pulses the central nervous system, checks homeostasis, ticks the
Vision→Realisation→Transformation engine, and (paced + constitutionally gated)
drives self-evolution — every beat logged to the gaas.v5 UEG for audit.

Integrations (existing systems, wired together):
  • Circadian biomimetic cycle  — beat intensity & cadence modulate by time-of-day
  • Central nervous system      — each beat fires a reflex pulse (biobus)
  • UEG (constitutional audit)   — every beat is hash-chain logged
  • Constitutional awareness     — expensive/autonomous AI actions are arms-length,
                                   opt-in and paced (never runaway), KPI-aware

Efficiency + safety: the beat itself is CHEAP (no AI) — pulse, homeostasis read,
transformation introspection, UEG log. EXPENSIVE cognition (full AI evolution
cycles) is OPT-IN (off by default) and paced, so the rhythm runs continuously
without runaway token cost.
"""
from __future__ import annotations

import asyncio
import datetime
import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger("organism.heartbeat")


def screen_one_deliverable() -> Dict[str, Any]:
    """§11 — screen ONE living deliverable per beat, least-recently-screened first. P3.2 clause (4).

    FOUR STATES, and the last two are the ones a naive version collapses:
      screened, clean    → `last_screened` set, verdict recorded
      screened, flagged  → the verdict is RECORDED AND SHOWN; a flag a reader cannot see is not a screen
      never screened     → `last_screened` absent, and the card SAYS "not screened yet" rather than blank
      could not screen   → `last_screened` absent WITH a reason. This is NOT "never screened": a broken
                           screen must not look like a young deliverable.

    The rotation mirrors the VSB one deliberately — one per beat by least-recently-screened — so the cost
    per beat is bounded and a fleet is covered over time rather than all at once.
    """
    from agentic_core.api.deliverables import _load as _dlv_load, _save as _dlv_save
    from agentic_core.api.compliance import screen_compliance

    try:
        rows = _dlv_load() or []
    except Exception as e:                   # noqa: BLE001 — reported, never read as "none to screen"
        #  `deliverables` is None, NOT 0: the store could not be opened, so the count is UNKNOWN. Reporting
        #  0 here would assert "no deliverable exists" about a store nobody could read.
        return {"screened": None, "id": None, "verdict": None, "deliverables": None,
                "could_not_run": f"the deliverable store could not be read ({e.__class__.__name__})",
                "basis": ("NOT a statement that there are no deliverables: the store itself could not be "
                          "read, and an empty answer here would be indistinguishable from an empty store")}
    if not rows:
        return {"screened": None, "id": None, "verdict": None, "deliverables": 0,
                "could_not_run": None,
                "basis": "no deliverable exists yet, so there was nothing to screen on this beat"}

    #  least-recently-screened first; a deliverable never screened sorts to the front because "" < any date
    target = sorted(rows, key=lambda d: str(d.get("last_screened") or ""))[0]
    _text = " ".join(str(target.get(k) or "") for k in ("title", "brief", "kind", "content"))[:4000]
    if not _text.strip():
        target["last_screened_error"] = ("this deliverable carries no screenable text, so no verdict was "
                                         "produced - which is NOT a clean screen")
        _dlv_save(rows)
        return {"screened": None, "id": target.get("id"), "verdict": None, "deliverables": len(rows),
                "could_not_run": "the deliverable carries no screenable text",
                "basis": ("recorded on the deliverable so a reader is not shown a blank where a verdict "
                          "would go, and not shown a PASS that nothing earned")}

    verdict = screen_compliance(_text)
    #  `_now()` does NOT exist in this module — caught before applying. heartbeat.py's own idiom,
    #  used at seven other sites, is time.strftime over time.gmtime.
    target["last_screened"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    target["last_screened_verdict"] = verdict.get("overall")
    target["last_screened_basis"] = (
        f"screened on the circadian compliance beat; verdict {verdict.get('overall')!r}. One deliverable is "
        f"screened per beat, least-recently-screened first, so a fleet is covered over time - a deliverable "
        f"with no `last_screened` has NOT been reached yet and is not thereby clean.")
    target.pop("last_screened_error", None)
    _dlv_save(rows)
    return {"screened": target.get("id"), "id": target.get("id"), "verdict": verdict.get("overall"),
            "deliverables": len(rows), "could_not_run": None,
            "basis": target["last_screened_basis"]}


def screen_living_vsb(vsb_id: str) -> Optional[Dict[str, Any]]:
    """§11 — screen ONE living VSB over its current plan + registration text; persist per-VSB
    history (capped); a REGRESSION (prior non-fail → fail) registers with the immune system and
    marks the shipped repo stale (§13 drift honesty, W309). Reusable: the heartbeat's rotation
    (W288) and the ESTABLISHMENT first-screen (W309 — birth is alive) share this one path."""
    from agentic_core.config import StoreUnavailable, atomic_write_json, data_path, read_json_strict
    from agentic_core.economy.living_vsbs import list_living
    living = (list_living() or {}).get("living_vsbs") or []
    target = next((v for v in living if v.get("vsb_id") == vsb_id), None)
    if not target:
        return None
    store_path = data_path("vsb_compliance_history.json")
    try:
        hist: Dict[str, Any] = read_json_strict(store_path, dict, expect=dict)   # W472 (FU-049/FU-053)
    except StoreUnavailable as e:
        # the screen would run, but its verdict has nowhere honest to go: the history is not replaced
        return {"vsb_id": vsb_id, "overall": None, "regression": False, "history_unavailable": str(e),
                "note": "the compliance history could not be read whole — the screen was not recorded"}
    # the CURRENT living text: registration identity + the scoped plan's objectives
    parts = [str(target.get("name") or ""), str(target.get("mission") or ""),
             str(target.get("domain") or "")]
    try:
        from agentic_core.api.business_plan import _load as _bp_load
        _plan = _bp_load(vsb_id) or {}
        for o in _plan.get("objectives", [])[:10]:
            parts.append(f"{o.get('title')} {o.get('kpi')}")
        # §11 (W322) — the verdict with economy TEETH screens the entity's SUBSTANCE, not just
        # header fields: a haram-substance entity previously passed because its name and
        # objective titles read clean. The challenge, concept and plan narrative join the text.
        parts.append(str(_plan.get("concept") or "")[:1200])
        parts.append(str(_plan.get("executive_summary") or "")[:800])
    except Exception:
        pass
    try:
        from agentic_core.api.vsb import _load_vsb, _blueprint
        _ent = _load_vsb(vsb_id)
        if _ent:
            parts.append(str(_ent.get("challenge") or "")[:800])
            _bp = _blueprint(_ent)
            parts.append(_bp.get("concept", "")[:1200])
            parts.append(_bp.get("commercialisation", "")[:800])
    except Exception:
        pass
    from agentic_core.api.compliance import screen_compliance
    screen = screen_compliance(" ".join(p for p in parts if p))
    rec = hist.get(vsb_id) or {}
    prior = rec.get("overall")
    regression = bool(prior and prior != "fail" and screen["overall"] == "fail")
    entries = (rec.get("history") or [])[-19:]
    entries.append({"overall": screen["overall"],
                    "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    # W506 (P2.7(6)) - the latest screen's VERDICTS are persisted, with the coverage statement that
    # qualifies them. `screen_compliance` returns all three and this writer kept only `overall`, so the
    # roster's `verdicts` field could never be filled and every row showed an empty list for an entity
    # that had been screened. Latest only and capped, so the store does not grow with every beat.
    _verdicts = [v for v in (screen.get("verdicts") or []) if isinstance(v, dict)][:12]
    hist[vsb_id] = {"overall": screen["overall"], "last_at": entries[-1]["at"],
                    "regression": regression, "verdicts": _verdicts,
                    "coverage_gaps": screen.get("coverage_gaps"),
                    "assessed_by": screen.get("assessed_by"),
                    "history": entries}
    atomic_write_json(store_path, hist)
    if regression:
        try:
            from agentic_core.organism.immune import immune
            immune.record(f"compliance:vsb:{vsb_id}", "compliance_regression")
            from agentic_core.organism.biobus import biobus
            biobus.fire_signal("reflex", "organism.compliance.regression",
                               f"{vsb_id} regressed to FAIL", 0.9)
        except Exception:
            pass
        try:   # §13 (W309) — a FAIL regression is drift: the shipped body no longer tells the truth
            from agentic_core.api.vsb import mark_repo_stale
            mark_repo_stale(vsb_id, "compliance regression to FAIL")
        except Exception:
            pass
    return {"vsb_id": vsb_id, "overall": screen["overall"], "regression": regression}


def circadian_phase(hour: Optional[int] = None) -> str:
    """Time-of-day circadian phase (matches the organism's circadian system)."""
    h = datetime.datetime.now().hour if hour is None else hour
    if 6 <= h < 9 or 17 <= h < 20:
        return "ACTIVE_REST"
    if 9 <= h < 17:
        return "ACTIVE_FOCUS"
    if 20 <= h < 23:
        return "MAINTENANCE_FOCUS"
    return "MAINTENANCE_REST"


_INTENSITY = {"ACTIVE_FOCUS": 1.0, "ACTIVE_REST": 0.7,
              "MAINTENANCE_FOCUS": 0.5, "MAINTENANCE_REST": 0.3}


class OrganismHeartbeat:
    """A singleton circadian rhythm that keeps the organism self-running."""

    def __init__(self):
        self.running = False
        self.beats = 0
        self.last_beat: Optional[str] = None
        self.last_phase: Optional[str] = None
        self.last_realisation: Optional[float] = None
        self.last_recovery: Optional[str] = None   # last autonomous metabolic self-recovery (ATP before->after)
        self.last_self_healing: Optional[float] = None   # last self-healing circuit health read on the beat
        self.last_heal: Optional[str] = None        # last proactive self-heal (circuits probed for recovery)
        self.last_genome: Optional[Dict[str, Any]] = None   # last genome-population vital sign on the beat
        #  §17.3 (P3.3, W585) — the last cadence refresh the beat performed, or None for "the beat has
        #  not refreshed a layer", which is not the same as "no layer was ever due"
        self.last_cadence: Optional[Dict[str, Any]] = None
        #  P3.4 (W587) — what the Owner's twin did on the beat, or why it withheld. None means the twin
        #  step has not run, which is not the same as a twin that ran and withheld.
        self.last_twin_directive: Optional[Dict[str, Any]] = None
        self.last_evolution: Optional[Dict[str, Any]] = None   # last autonomous evolution (proposals → governance)
        self.last_vsb_operated: Optional[str] = None   # §4 — last living VSB autonomously operated on the beat
        # W503 (FU-045, FU-063) — the visits that were NOT cycles. Declared and published, because a
        # trace the beat keeps and /status never reports is a fact rendered nowhere (FU-264's shape).
        self.last_vsb_failed: Optional[Dict[str, Any]] = None        # the visit raised
        self.last_vsb_not_operated: Optional[Dict[str, Any]] = None  # the visit was held or refused
        self.last_transfer_reconcile: Optional[Dict[str, Any]] = None   # W466 — last stranded-transfer pass
        self.last_intake_reconcile: Optional[Dict[str, Any]] = None     # W467 — last stranded-consume pass
        self.last_vsb_evolved: Optional[Dict[str, Any]] = None   # §8×§3 (W309) — last child VSB evolved on the tick
        # W506 (P2.7(2)) - a reaction that happened BETWEEN beats. `reflex_arcs_registered` was 0
        # for the platform's whole life, so these were structurally always empty.
        self.last_reflex = None                 # {arc, at, trigger, result} of the last arc that fired
        self.reflex_reactions = 0               # how many times an arc has driven a check off-beat
        # §8 (W506, P2.7(3)) - the last immune defence THIS organism engaged, and the beat it was
        # engaged on. Both None on a platform that has never been under threat, which is different
        # from one that could not defend itself - and until this round it was always the latter.
        self.last_immune_defence: Optional[Dict[str, Any]] = None
        self._last_defence_beat: Optional[int] = None
        self.interval_seconds = 60            # base cadence (modulated by circadian)
        self.auto_evolve = False              # opt-in: autonomous AI evolution cycles
        self.auto_economy = False             # opt-in: autonomous economy cycles
        self.auto_ship = False                # opt-in (§13, W319): re-ship STALE repos on the beat
        self.auto_align = False               # opt-in: route vision gaps to tiers each beat (cheap, plan-only)
        self.auto_compliance = False          # opt-in (§11, W288): re-screen living VSBs on the beat
        # W420 — surfaced so the UI can tell the user whether their choice will actually survive a
        # restart, instead of showing a toggle that silently forgets.
        self.autonomy_persisted: bool = True
        self.autonomy_restored_at: Optional[str] = None
        self.last_compliance: Optional[Dict[str, Any]] = None   # last continuous-compliance reading
        self._evolve_every = 30               # beats between evolution attempts (when enabled)
        self._beats_since_evolve = 0
        # W532 (P3.16) — the recirculation loop, paced and OFF by default. Six stages with their engine
        # calls is expensive, so this follows section 4's idiom for expensive work rather than section 1's
        # for cheap work. Off by default means no existing deployment changes behaviour.
        self.auto_metabolic = False
        #  FU-461 — WHERE A FAILED BEAT STEP IS RECORDED. Twenty-two handlers in this file had a bare
        #  `pass`, about fifteen of them immediately after an `actions.append(...)`: the step raised,
        #  nothing was appended, and the beat reported a shorter actions list with no sign anything had
        #  gone wrong. W589 fixed ONE of them (the cadence step, line ~340) and wrote the reason in place:
        #  a swallowed exception made a step that CANNOT RUN indistinguishable from a step with nothing to
        #  do, because both appended no action and left no trace.
        #  ONE DICT, not a record field per step: most steps have no `self.last_*` to write to, and
        #  inventing fifteen of them would be fifteen fields nobody reads.
        self.last_step_failures: Dict[str, str] = {}
        self._beats_since_metabolic = 0
        self._metabolic_every = 10
        self.last_metabolic: Optional[Dict[str, Any]] = None
        self._log: List[Dict[str, Any]] = []
        self._task: Optional["asyncio.Task"] = None
        self._ueg = None
        self._load_autonomy()   # W420 — restore the Owner's autonomy choices; defaults stand if none

    def _ueg_logger(self):
        if self._ueg is None:
            try:
                from agentic_core.gaas.v5 import UEGLogger
                self._ueg = UEGLogger()
            except Exception:
                self._ueg = False
        return self._ueg or None

    async def beat(self) -> Dict[str, Any]:
        """One heartbeat — cheap, constitutionally logged, circadian-aware."""
        self.beats += 1
        phase = circadian_phase()
        intensity = _INTENSITY.get(phase, 0.5)
        self.last_phase = phase
        self.last_beat = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        actions: List[str] = []
        #  FU-461 — CLEARED HERE, not accumulated. A failure recorded on an earlier beat would otherwise be
        #  reported as a failure of this one for the rest of the process's life, which is the stale-record
        #  defect W589's cadence comment warns about two lines above its own fix. Assigned rather than
        #  mutated so the attribute exists before any step can record into it.
        self.last_step_failures = {}

        # 1. Pulse the central nervous system (the heartbeat itself)
        try:
            from agentic_core.organism.biobus import biobus
            biobus.fire_signal("reflex", "organism.heartbeat", f"beat {self.beats} [{phase}]", intensity)
            actions.append("pulse")
        except Exception:
            pass

        # 2. Homeostasis check + AUTONOMOUS self-regulation (cheap, no AI) — the §8 survival instinct on the
        #    beat: the organism reads its own state and, when energy is depleted, actively RESTS to restore it
        #    (self-healing without manual trigger — §3 "runs, maintains, defends, heals itself").
        # W506 (P2.7(2)) — the check itself lives in `respond_to_health`, which a REGISTERED reflex arc
        # also drives between beats. One function, two callers: a second copy of the threshold here
        # would drift from the arc's copy the first time either changed.
        _h = self.respond_to_health()
        health = _h.get("health")     # read ONCE and carried to the beat record below
        if _h.get("read"):
            actions.append("homeostasis")
        if self.respond_to_energy().get("recovered"):
            actions.append("self_recovery")

        # 2c. Self-healing reflex (immune → self-healing on the beat): read the circuit-breaker health and,
        #     when circuits are OPEN past their recovery window, the organism ACTIVELY probes them for
        #     recovery (proactive self-healing, not just passive timeout) — §3 "defends and heals itself".
        # W506 (P2.7(2)) — same extraction: a registered arc drives this between beats.
        if self.respond_to_circuits().get("probed"):
            actions.append("self_heal")

        # §8 (W506, P2.7(3)) — the organism ENGAGES its own immune defence at ≥HIGH. The CCA route that
        # does this was built and had no caller, so a HIGH threat waited for an admin to press a button.
        if self.respond_to_threat().get("engaged"):
            actions.append("immune_defence")

        # 2d. Genome vital sign — read the organism's genome-population genetics (count, mean fitness,
        #     generational depth) as part of its self-monitoring, so the genome subsystem joins the living
        #     loop rather than sitting in isolated CRUD. Cheap (file summary), no AI.
        try:
            from agentic_core.api.organism_status import _genome_state
            gs = _genome_state()
            #  W584 (FU-405) — THE BASIS TRAVELS WITH THE NUMBER. This copied three fields, and after
            #  the aggregate was corrected it would have published `mean_fitness: None` with no reason at
            #  all - leaving a reader of the beat unable to tell "nothing in this platform evaluates
            #  fitness" from "the store could not be read". Fixing a writer without its reader moves the
            #  lie down a layer (W475's class), so the vital sign now carries what the figure is worth.
            self.last_genome = {"total": gs.get("total_genomes"), "mean_fitness": gs.get("mean_fitness"),
                                "mean_fitness_basis": gs.get("mean_fitness_basis"),
                                "mean_declared_fitness": gs.get("mean_declared_fitness"),
                                "fitness_composition": gs.get("fitness_composition"),
                                "max_generation": gs.get("max_generation")}
            if gs.get("total_genomes"):
                actions.append("genome_scan")
        except Exception:
            pass

        # 2d-bis. §17.3 CADENCE — the Strategic and Action-Plan layers refresh themselves (P3.3, W585).
        #     Measured before this existed: the cadence was PROMPT TEXT only, so nothing refreshed
        #     quarterly, weekly, on a market signal or on a KPI. The due-check is a pure comparison and
        #     the default composition is derived from the plan's own stored state, so this stays within
        #     the "cheap + deterministic + virtual" rule the steps around it keep. Nothing is appended to
        #     `actions` when nothing was due — an action list that always carries an entry says nothing
        #     about whether anything happened.
        #     W589 — ONE HANDLER PER LAYER. The try used to wrap the whole loop with the action appended
        #     after it, so a second layer that raised discarded the FIRST layer's refresh - which had
        #     already been written to the plan with its history entry. The beat then reported nothing while
        #     the plan said otherwise, which is worse than a silent failure: two records of the same beat
        #     disagreeing. Now a layer that refreshed is recorded as refreshed whatever the other does.
        try:
            from agentic_core.organism import cadence as _cad
            _refreshed, _cad_failed = [], []
            #  W593 (FU-431, M1 R3.6) — ONE VSB PER BEAT JOINS THE APEX. W585 refreshed "workstation" only,
            #  so no VSB's Strategic or Action-Plan layer was ever refreshed while §17.3 and the surface
            #  spoke of the layers generally. `refresh` has always taken a SCOPE and `_plan_path` resolves
            #  each entity's own plan; the beat just never passed anything else. Round-robin by the BEAT
            #  COUNTER rather than by the roster's `last_operated` timestamp, which the §4 economy step uses
            #  because a cycle POSTS and must not double-post: a refresh is idempotent on its own due-check
            #  (`refresh` returns refreshed=False when nothing is due), so a repeated turn costs nothing and
            #  a missed one is picked up next pass - no new persisted field, no extra write per beat.
            _scopes = ["workstation"]
            _roster_note = "the apex only"
            try:
                from agentic_core.economy.living_vsbs import _load as _load_roster
                _entries = [v for v in (_load_roster() or {}).values()
                            if isinstance(v, dict) and isinstance(v.get("vsb_id"), str)]
                if _entries:
                    _pick = _entries[self.beats % len(_entries)]
                    _scopes.append(str(_pick["vsb_id"]))
                    _roster_note = (f"the apex plus 1 of {len(_entries)} living entit(ies), chosen by "
                                    f"beat {self.beats} % {len(_entries)} - every entity is visited "
                                    f"REGULARLY, not exactly every {len(_entries)} beats, because a roster "
                                    f"that changes size shifts the rotation")
            except Exception as _roster_err:              # noqa: BLE001 — an unreadable roster is SAID
                _roster_note = (f"the apex only: the living roster could not be read "
                                f"({_roster_err.__class__.__name__}), so no entity took its turn this beat "
                                f"- which is not the same as there being none")
            for _scope in _scopes:
                for _layer in _cad.LAYERS:
                    try:
                        _res = _cad.refresh(_scope, _layer)
                    except Exception as _layer_err:      # noqa: BLE001 — recorded, not swallowed
                        _cad_failed.append({"scope": _scope, "layer": _layer,
                                            "could_not_run": f"{_layer_err.__class__.__name__}: "
                                                             f"{_layer_err}"})
                        continue
                    if _res.get("refreshed"):
                        _refreshed.append({"scope": _scope, "layer": _layer,
                                           "trigger": _res["entry"]["trigger"],
                                           "reason": _res["entry"]["reason"], "at": _res["entry"]["at"],
                                           "served_by": _res["entry"]["served_by"]})
            #  W593 (FU-430) — WRITTEN ON EVERY BEAT THAT COMPLETED THE STEP. This was
            #  `if _refreshed or _cad_failed`, so a beat with nothing due left an EARLIER beat's record in
            #  place — and the /organism/cadence surface added in the same round presented it as "what the
            #  most recent heartbeat managed". From beat 3 onwards that sentence was false for every
            #  quiet beat. MILESTONE M1 found it (R3.4) in the round that wrote it. The beat NUMBER travels
            #  with the record so the surface can name the beat instead of implying the latest, and
            #  `nothing_was_due` separates a quiet cadence from a broken one.
            self.last_cadence = {
                "beat": self.beats,
                "refreshed": _refreshed,
                "could_not_run": _cad_failed or None,
                "nothing_was_due": not _refreshed and not _cad_failed,
                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "scopes": _scopes,
                "scope_basis": _roster_note,
                "basis": (f"{len(_refreshed)} layer(s) refreshed on beat {self.beats} across "
                          f"{len(_scopes)} scope(s) ({_roster_note}) and {len(_cad_failed)} could not run. "
                          f"A layer that could not run is still DUE - this is not 'nothing was due'"
                          if (_refreshed or _cad_failed) else
                          f"beat {self.beats} completed the cadence step over {len(_scopes)} scope(s) "
                          f"({_roster_note}) and NO layer was due. This is a quiet cadence, not a broken "
                          f"one, and not a record left over from an earlier beat"),
            }
            if _refreshed:
                actions.append("cadence_refresh")
        except Exception as _cad_err:
            #  a plan that cannot be read whole must not stop the beat, and it must not be refreshed
            #  either: cadence.refresh reads strictly, so an unreadable plan raises here rather than
            #  being overwritten with an invented one (the FU-395 class).
            #  W589 — BUT IT IS RECORDED. This was `pass`, and a swallowed exception made a cadence that
            #  CANNOT RUN indistinguishable from a cadence with nothing due: both appended no action and
            #  left no trace. Since the whole point of §17.3 is that the layers refresh THEMSELVES, a
            #  cadence that has silently stopped firing is the failure that matters most, and it was the
            #  one this handler hid. `actions` is still not appended to - claiming an action for a failure
            #  would be the opposite defect - so the three states are told apart by this record instead.
            self.last_cadence = {
                "refreshed": [],
                "could_not_run": f"{_cad_err.__class__.__name__}: {_cad_err}",
                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "basis": ("the cadence step raised, so NO layer was refreshed on this beat. This is not "
                          "'nothing was due': the due-check never completed, and a layer that is due is "
                          "still due. The beat continues because an unreadable plan must not stop it, and "
                          "the plan is deliberately NOT written - cadence.refresh reads strictly so that a "
                          "plan it cannot read is left alone rather than overwritten with an invented one"),
            }

        # 2e. §4 — autonomously OPERATE one living VSB enterprise (round-robin, paced): run one virtual economy
        #     cycle for the least-recently-operated established VSB, so each "continually, autonomously operates"
        #     forever. Cheap + deterministic + virtual; the registry is only populated once VSBs are established.
        #     W288 HONESTY FIX: this now actually honours the auto_economy flag — it was settable and
        #     reported in status() but never consulted, so cycles ran regardless of the Owner's setting.
        if self.auto_economy:
            try:
                from agentic_core.economy.living_vsbs import operate_one
                op = operate_one()
                # W503 (FU-063) — THE FOUR OUTCOMES, read from the one field the producer now sets
                # instead of re-derived here. The ladder this replaces counted a FAIL-screen hold and a
                # governance hold as an entity OPERATED (`last_vsb_operated` set, action "operate_vsb"),
                # and W503's own FU-045 branch filed `{error, cycle_ran: True}` — a cycle that POSTED and
                # whose roster bookkeeping then raised — as a failed visit. `outcome` distinguishes all
                # four, and only `ran` sets `last_vsb_operated`, because only `ran` operated anything.
                _outcome = (op or {}).get("outcome")
                if op and op.get("held") == "roster_unavailable":
                    # W472 — nothing was tended, and the beat says so under this exact name, which
                    # /status publishes. Kept ahead of the generic refused branch on purpose.
                    actions.append("roster_unavailable")
                elif op and _outcome == "ran":
                    self.last_vsb_operated = op.get("vsb_id")
                    actions.append("operate_vsb")
                    if op.get("bookkeeping_raised"):
                        # the cycle stands; the roster's record of the visit did not
                        actions.append("operate_vsb_bookkeeping_raised")
                        logger.warning("heartbeat: %s's cycle posted but the roster bookkeeping raised: %s",
                                       op.get("vsb_id"), str(op.get("error"))[:200])
                elif op and _outcome in ("held", "refused"):
                    # a visit happened and nothing was operated. `last_vsb_operated` stays as it was.
                    actions.append(f"vsb_{_outcome}")
                    self.last_vsb_not_operated = {
                        "vsb_id": op.get("vsb_id"), "outcome": _outcome,
                        "reason": str(op.get("held") or (op.get("governance") or {}).get("status")
                                      or "unrecorded"),
                        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                elif op and (_outcome == "raised" or op.get("error")):
                    # W503 (FU-045) — A FAILED VISIT LEAVES A TRACE. There was no branch here at all: the
                    # error result was discarded, so a visit that failed left nothing in the beat, nothing
                    # in the chain and nothing in the log. `last_vsb_operated` is deliberately NOT set.
                    actions.append("operate_vsb_failed")
                    self.last_vsb_failed = {"vsb_id": op.get("vsb_id"), "error": str(op.get("error"))[:200],
                                            "cycle_ran": bool(op.get("cycle_ran")), "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                    try:
                        from agentic_core.gaas.v5 import UEGLogger
                        UEGLogger().log({"type": "organism.vsb_visit_failed", "vsb_id": op.get("vsb_id"),
                                         "error": str(op.get("error"))[:200],
                                         "cycle_ran": bool(op.get("cycle_ran")),
                                         "disclaimer": "Virtual/simulated WST — no real funds moved."})
                    except Exception:
                        pass
                    logger.warning("heartbeat: VSB visit failed for %s: %s",
                                    op.get("vsb_id"), str(op.get("error"))[:200])
                elif op:
                    # W503 (FU-045, FU-063) — A RESULT THIS READER CANNOT CLASSIFY. Every return path in
                    # the tree stamps `outcome` today, so this is not reachable; it exists because the
                    # alternative is the exact defect FU-045 was registered for. The four branches above
                    # match on `outcome` (and on `error`), and a result carrying neither would match
                    # NOTHING and leave the visit with no trace anywhere — a silent fall-through inside
                    # the code written to remove silent fall-throughs. It is reported as unclassified,
                    # which is louder than the other outcomes on purpose: reaching it means a producer
                    # and this reader disagree about what a visit result looks like.
                    actions.append("operate_vsb_unclassified")
                    self.last_vsb_not_operated = {
                        "vsb_id": op.get("vsb_id"), "outcome": "unclassified",
                        "reason": ("the visit returned a result naming no outcome, so the beat cannot say "
                                   "what happened; nothing is claimed about this entity"),
                        "keys": sorted(str(k) for k in op)[:12],
                        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                    logger.error("heartbeat: a VSB visit returned an unclassifiable result for %s (keys: %s)",
                                 op.get("vsb_id"), sorted(str(k) for k in op)[:12])
            except Exception:
                pass
            # W466 (register FU-023) — every fifth beat, complete transfers whose sender was debited and whose receiver
            # was never credited (a replay that cannot debit; see transfers.reconcile_receiver_legs). Runs only with
            # autonomous economy on — the same opt-in as the cycles above — and says what it did in status().
            if self.beats % 5 == 0:
                try:
                    from agentic_core.economy.transfers import reconcile_receiver_legs
                    rep = reconcile_receiver_legs()
                    self.last_transfer_reconcile = {
                        "beat": self.beats, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        **{k: rep.get(k) for k in ("open_legs", "reconciled", "closed_only", "skipped_settling",
                                                   "failed", "close_failed", "ledgers_unreadable", "skipped")}}
                    if rep.get("reconciled"):
                        actions.append("transfer_reconcile")
                except Exception as err:
                    self.last_transfer_reconcile = {"beat": self.beats,
                                                    "error": f"{type(err).__name__}: {str(err)[:160]}"}
                    logger.warning("stranded-transfer reconciliation failed on beat %s: %s", self.beats, err)
                # W467 (refutation) — and recognised events a cycle consumed but never posted (the process stopped)
                try:
                    from agentic_core.economy.revenue import reconcile_stranded_consumes
                    irep = reconcile_stranded_consumes()
                    self.last_intake_reconcile = {"beat": self.beats, **irep}
                    if irep.get("given_back"):
                        actions.append("intake_reconcile")
                except Exception as err:
                    self.last_intake_reconcile = {"beat": self.beats, "error": f"{type(err).__name__}: {str(err)[:160]}"}
                    logger.warning("stranded-intake reconciliation failed on beat %s: %s", self.beats, err)

        # 2f. §11 (W288) — CONTINUOUS compliance: re-screen ONE living VSB per beat (round-robin,
        #     least-recently-screened), so an entity screened at establishment is re-evaluated as its
        #     plan and record evolve — "continuously monitored and evaluated live", not event-only.
        #     A REGRESSION (previously pass/review → now fail) registers with the immune system and
        #     fires a reflex signal (§12 survival tie-in). Cheap + deterministic; per-VSB history kept.
        if self.auto_compliance:
            try:
                self.last_compliance = self._compliance_beat()
                if self.last_compliance:
                    actions.append("compliance_rescreen")
            except Exception as _cr_err:
                #  FU-461 — RECORDED, not swallowed. This handler is the one P3.2 clause (4)'s deliverable
                #  screen runs inside: a bare `pass` here made "the compliance step had nothing due" and
                #  "the compliance step could not run" the same observable, because both append no action
                #  and leave no trace. NOT appended to `actions` — W589's rule, kept: an action is something
                #  the beat DID, and claiming one for a failure would be the opposite defect.
                self._step_failed("compliance_rescreen", _cr_err)

        # 2g. §P3.16 (W532) — THE RECIRCULATION LOOP, DRIVEN FROM THE BEAT. Paced and opt-in, because six
        #     stages with their engine calls is expensive. The SUBJECT IS THE ORGANISM: execute_cycle wants a
        #     user_context and there is no avatar population store to round-robin over, so rather than
        #     fabricate a user the platform cycles itself — which is what this loop is, its own docstring
        #     calling it the organism's metabolic loop. The per-user case is the avatar path, a different
        #     clause. What it records is the point: the per-stage latencies W527 measures, and any breach BY
        #     NAME, so a breach is a fact in the beat rather than a line in a log.
        self._beats_since_metabolic += 1
        if self.auto_metabolic and self._beats_since_metabolic >= self._metabolic_every:
            self._beats_since_metabolic = 0
            try:
                from agentic_core.avatars.core.recirculation_orchestrator import (
                    AvatarRecirculationOrchestrator)
                from agentic_core.avatars.core.avatar_engine import AvatarState
                # W533 — the orchestrator requires a VSBUEGLogger-shaped logger: it calls the async
                # log_event and log_minimisation_event. The heartbeat's own _ueg_logger() returns
                # gaas.v5.UEGLogger, whose interface is a SYNCHRONOUS .log(dict), so handing it over
                # made every stage fail on an await of a non-coroutine. Two logger interfaces exist
                # in this repository and the dependency decides which one is correct here.
                from agentic_core.ueg.logger import VSBUEGLogger as _VSBUEG
                _orch = AvatarRecirculationOrchestrator(
                    _VSBUEG(),
                    AvatarState(avatar_id="platform", user_id="platform"))
                _ctx = await _orch.execute_cycle({
                    "user_id": "platform",
                    "domain": "organism_self_regulation",
                    "subject_basis": ("the ORGANISM, not a user: no avatar population is recorded for the "
                                      "beat to round-robin over, and inventing a user to cycle would be a "
                                      "subject nobody asked for"),
                })
                _stages = (_ctx or {}).get("stages") or []
                _breached = [g["stage"] for g in _stages if g.get("breached")]
                # W533 — THE CYCLE RAN AND EMITTED NOTHING, and that had the same record as a delivered
                # cycle. Clearance gate 1 withholds the emission because the engines supply no
                # constitutional verdict, so six measured stages and an empty mouth is the NORMAL state of
                # this platform today. A beat reporting that as a clean cycle would be the same defect this
                # programme keeps removing, one layer up: the run is honest about its latencies and silent
                # about its outcome. Three states now, not two.
                _status = (_ctx or {}).get("status")
                _withheld = _status == "WITHHELD"
                self.last_metabolic = {
                    "at": self.last_beat,
                    "stages_measured": len(_stages),
                    "stages": _stages,
                    "breached_stages": _breached,
                    "breach_count": len(_breached),
                    "subject": "platform",
                    "cycle_status": _status,
                    "emitted": (False if _withheld else None if _status is None else True),
                    "withheld_reason": (_ctx or {}).get("withheld_reason"),
                    "basis": (f"{len(_stages)} stage(s) measured individually; "
                              f"{len(_breached)} breached an untuned default budget"
                              + ("; the emission was WITHHELD by the clearance chain, so the cycle ran but "
                                 "delivered nothing — measured is not the same as delivered"
                                 if _withheld else "")
                              if _stages else
                              "the cycle returned no stage record, so NOTHING was measured — this is not a "
                              "clean run, it is an unmeasured one"),
                }
                actions.append("metabolic_cycle_withheld" if _withheld else "metabolic_cycle")
            except Exception as exc:                  # noqa: BLE001 — recorded, never silently skipped
                self.last_metabolic = {
                    "at": self.last_beat,
                    "stages_measured": 0,
                    "failed": f"{exc.__class__.__name__}: {exc}",
                    "basis": ("the metabolic cycle FAILED, so no latency was measured. A failure is not a "
                              "clean beat and is recorded as one here"),
                }
                actions.append("metabolic_cycle_failed")

        # 3. Transformation tick — vision-realisation introspection (no AI)
        try:
            from agentic_core.api.transformation import _realise
            self.last_realisation = _realise().get("overall_realisation")
            actions.append("transformation_tick")
        except Exception:
            pass

        # 3b. Autonomous alignment (opt-in) — route vision gaps to the living tiers, AND let the Owner's
        #     twin direct unprompted (P3.4 clause 2, W587).
        #
        #     MEASURED BEFORE THIS CHANGE: this step was `await align(AlignRequest(execute=False))` and
        #     nothing else. `align` is the vision-gap router, not a board directive, and execute=False made
        #     even that plan-only — so the beat produced no directive at all, which is what the clause
        #     ("auto_align → board_directive with execute") is written against.
        #
        #     The twin's own step REFUSES when the Chief is a ROLE — no instruction and no decision of the
        #     Owner's exists, so acting would be the platform directing itself under their name — and it is
        #     idempotent on the Owner's RECORD rather than on the clock, because this beat visits every
        #     sixty seconds and a directive per visit would grow the living plan unasked. Both outcomes are
        #     recorded; neither is silent.
        if self.auto_align:
            try:
                from agentic_core.api.cognition import align, AlignRequest
                await align(AlignRequest(execute=False))
                actions.append("alignment")
            except Exception:
                pass
            try:
                from agentic_core.api.board import twin_directive_unprompted
                _tw = await twin_directive_unprompted("workstation")
                self.last_twin_directive = {
                    "issued": bool(_tw.get("issued")),
                    "reason": _tw.get("reason"),
                    "directive_id": _tw.get("directive_id"),
                    "owner_inputs": _tw.get("owner_inputs"),
                    "basis": _tw.get("basis"),
                    "founder_model_basis": _tw.get("founder_model_basis"),
                    "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }
                #  the action list records what HAPPENED, not that the step ran: a refusal and an issued
                #  directive are different facts and a single marker for both would say neither
                actions.append("twin_directive" if _tw.get("issued") else
                               f"twin_directive_withheld:{_tw.get('reason')}")
            except Exception:
                pass

        # 4. Paced, opt-in self-evolution (EXPENSIVE — arms-length gated). AUTONOMOUS evolution ALWAYS routes
        #    its proposals through the Change Control Agency (submit_to_change_control=True): with no human in
        #    the loop, unsupervised self-improvement must be governed arms-length — never silent self-mutation.
        self._beats_since_evolve += 1
        # §8 (W310) — the reconfiguration engine's defensive levers are EXPRESSED, not just stored:
        # `organism.metabolic_throttle` (an immune/owner-set defence) genuinely suppresses the
        # expensive evolution work while metabolic ATP is low. Honest: the skip is a recorded action.
        _throttled = False
        _cfg_org: Dict[str, Any] = {}
        try:
            from agentic_core.organism.reconfiguration import _load_config
            from agentic_core.organism.biobus import biobus as _bb
            _cfg_org = (_load_config() or {}).get("organism") or {}
            if _cfg_org.get("metabolic_throttle"):
                _ctx = _bb.organism_context()
                # §8 (W341) — atp_ratio lives under the 'metabolic' key: the old top-level read
                # always defaulted to 1.0, so the W310 defensive lever could NEVER fire.
                if float(((_ctx.get("metabolic") or {}).get("atp_ratio")) or 1.0) < 0.2:
                    _throttled = True
                    actions.append("metabolic_throttle")
        except Exception:
            pass
        # §8 (W310/W346) — the `organism.evolution_auto_apply` lever gets its REAL consumer: when
        # the Owner enables it, CCA-APPROVED evolution proposals are applied on the beat (mutations
        # still gated by the CCA decision — this only automates the post-approval application).
        # W346 — runs on EVERY beat, not inside the paced evolve tick's maintenance-phase gate:
        # applying an ALREADY-APPROVED change is cheap and must not wait hours for a circadian
        # window (the e2e test caught approved mutations stranded until the next maintenance phase).
        # ORDER MATTERS: apply runs BEFORE the paced evolve tick — a re-evolve replaces the
        # proposal set with a new submitted CCA, which would orphan the approved one.
        try:
            if _cfg_org.get("evolution_auto_apply"):
                from agentic_core.api.vsb import apply_approved_evolution
                from agentic_core.economy.living_vsbs import list_living as _ll
                for _v in ((_ll() or {}).get("living_vsbs") or [])[:10]:
                    _ap = apply_approved_evolution(_v.get("vsb_id"))
                    # W493 (refutation) - `applied` is True whenever the apply RAN to completion, which
                    # includes consuming an approval with no applicable mutation. Recording
                    # "evolution_applied" for that beat is the round's own defect: an action named for
                    # something that did not happen. The two outcomes are now named separately.
                    if _ap.get("generation_advanced") or int(_ap.get("mutations_applied") or 0) > 0:
                        actions.append("evolution_applied")
                    elif _ap.get("applied"):
                        actions.append("evolution_approval_consumed_no_mutation_applicable")
        except Exception:
            pass


        if (self.auto_evolve and not _throttled and phase in ("MAINTENANCE_FOCUS", "MAINTENANCE_REST")
                and self._beats_since_evolve >= self._evolve_every):
            self._beats_since_evolve = 0
            try:
                from agentic_core.api.sovereign_evolution import run_cycle, CycleRequest
                cyc = await run_cycle(CycleRequest(focus="autonomous heartbeat maintenance",
                                                   submit_to_change_control=True))
                subs = (cyc or {}).get("change_control_submissions") if isinstance(cyc, dict) else None
                self.last_evolution = {"submitted_to_governance": len(subs) if subs else 0}
                actions.append("evolution_cycle")
            except Exception:
                pass
            # §8×§3 (W309) — the organism tends its CHILDREN too: on the same paced evolve tick,
            # evolve the least-recently-evolved living VSB (round-robin; system context — the
            # entity's own evolution machinery, proposals recorded on its record, repo refreshed).
            try:
                from agentic_core.api.vsb import evolve_vsb, EvolveRequest, _load_vsb, _gate_block_reason
                from agentic_core.economy.living_vsbs import list_living
                _live = (list_living() or {}).get("living_vsbs") or []
                # W452 (P1.4) — a Mode 3 gate holds the organism's hand too: a gated entity is skipped
                # WITH a recorded action (never a silent except-pass), and the next one is tended.
                _held = [v.get("vsb_id") for v in _live
                         if _gate_block_reason(_load_vsb(v.get("vsb_id")) or {})]
                for _h in _held:
                    actions.append(f"evolve_vsb_held_by_review_gate:{_h}")
                _live = [v for v in _live if v.get("vsb_id") not in _held]
                if _live:
                    # W493 (FU-165) - this picked the least-recently-EVOLVED entity, but `last_evolved`
                    # now means "last APPLIED" and this loop runs evolution CYCLES. Sorting by the applied
                    # stamp would let an entity that files every beat keep sorting first forever, starving
                    # the round-robin; it sorts by the cycle stamp, falling back for older records.
                    def _last_cycle(v: dict) -> str:
                        _rec = _load_vsb(v.get("vsb_id")) or {}
                        return str(_rec.get("last_evolution_cycle") or _rec.get("last_evolved") or "")
                    _t = sorted(_live, key=_last_cycle)[0]
                    _ev = await evolve_vsb(_t.get("vsb_id"),
                                           EvolveRequest(trigger="autonomous heartbeat"), user=None)
                    # W493 (refutation, via the pre-flight's `keys` lead) - this published
                    # `generation` alone for a cycle that only FILED proposals. The number is real but
                    # it did not move, so a caller reading the status saw "last VSB evolved - generation
                    # 3" for a beat where nothing was applied. It records what the cycle DID: the cycle
                    # count, the outcome, and that no generation advanced - an autonomous cycle never
                    # applies, because the apply is a separate step gated on the Owner's approval.
                    _evd = _ev if isinstance(_ev, dict) else {}
                    self.last_vsb_evolved = {"vsb_id": _t.get("vsb_id"),
                                             "generation": _evd.get("generation"),
                                             "generation_advanced": False,
                                             "evolution_cycles_run": _evd.get("evolution_cycles_run"),
                                             "outcome": _evd.get("outcome"),
                                             "basis": "a cycle ran and filed proposals; the genome "
                                                      "mutates only after the Owner approves the "
                                                      "change record, so no generation advanced here"}
                    actions.append("evolve_vsb")
                    # §12 (W330) — the entity's OWN self_investment funds its evolution
                    try:
                        from agentic_core.economy.living_vsbs import spend_self_investment
                        spend_self_investment(_t.get("vsb_id"), "autonomous evolution cycle")
                    except Exception:
                        pass
            except Exception:
                pass
        # §13 (W319) — the STALE flag gets its autonomous consumer: when the Owner enables
        # auto_ship, the heartbeat re-ships ONE stale repo per beat (oldest stale first) so the
        # shipped body tracks the life; the re-ship itself is UEG-logged by ship_vsb_repo, and the
        # re-ship-on-drift closure is recorded as a distinct UEG event here.
        if self.auto_ship:
            try:
                from agentic_core.api.vsb import _REPO_STORE, ship_vsb_repo
                import json as _json
                _stale = []
                for _p in _REPO_STORE.glob("*.ship.json"):
                    try:
                        _s = _json.loads(_p.read_text(encoding="utf-8"))
                        if _s.get("stale"):
                            _stale.append((_s.get("stale_since") or "", _s.get("vsb_id")))
                    except Exception:
                        continue
                # W452 (P1.4) — a stale repo behind a Mode 3 gate is NOT re-shipped; the hold is recorded
                from agentic_core.api.vsb import _load_vsb as _hb_load, _gate_block_reason as _hb_gate
                _held_ship = [v for _, v in _stale if _hb_gate(_hb_load(v) or {})]
                for _h in _held_ship:
                    actions.append(f"reship_held_by_review_gate:{_h}")
                _stale = [x for x in _stale if x[1] not in _held_ship]
                if _stale:
                    _vid = sorted(_stale)[0][1]
                    _res = await ship_vsb_repo(_vid, user=None)
                    self.last_reshipped = {"vsb_id": _vid,
                                           "coherent_whole": (_res or {}).get("coherent_whole")}
                    actions.append("reshipped_stale_repo")
                    # §12 (W330) — the re-ship is development work the entity funds itself
                    try:
                        from agentic_core.economy.living_vsbs import spend_self_investment
                        spend_self_investment(_vid, "autonomous repo re-ship")
                    except Exception:
                        pass
                    try:
                        self._ueg_logger().log({"type": "vsb.repo.reshipped_on_drift",
                                                "vsb_id": _vid, "beat": self.beats})
                    except Exception:
                        pass
            except Exception:
                pass

        # 5. Constitutional audit — hash-chain the beat into the UEG
        ueg = self._ueg_logger()
        if ueg:
            try:
                ueg.log({"type": "heartbeat", "beat": self.beats, "phase": phase,
                         "realisation": self.last_realisation, "health": health,
                         "self_healing": self.last_self_healing, "actions": actions})
            except Exception:
                pass

        record = {"beat": self.beats, "phase": phase, "intensity": intensity,
                  "realisation": self.last_realisation, "health": health,
                  "self_recovery": self.last_recovery if "self_recovery" in actions else None,
                  "actions": actions, "at": self.last_beat,
                  #  FU-461 — the steps that were ATTEMPTED AND FAILED on THIS beat, by name. ADDED beside
                  #  `actions` rather than folded into it: `actions` keeps meaning what the beat did, so no
                  #  existing reader's understanding of it changes. A shorter `actions` list on its own
                  #  cannot distinguish a step with nothing due from a step that could not run, which is the
                  #  whole reason this field exists.
                  "steps_failed": dict(getattr(self, "last_step_failures", {}) or {}),
                  "steps_failed_basis": (
                      "steps attempted on this beat that raised, by name, cleared at the start of every "
                      "beat so a failure never outlives the beat that had it. They are deliberately NOT in "
                      "`actions`: an action is something the beat performed. Twenty-two handlers in this "
                      "file swallowed their exception; FU-461 tracks the eleven still to convert, so an "
                      "EMPTY steps_failed means no CONVERTED step failed - not that nothing failed."),
                  }
        self._log.append(record)
        self._log = self._log[-100:]
        return record

    async def run(self) -> None:
        self.running = True
        logger.info("Organism heartbeat started (continuous circadian autonomy).")
        while self.running:
            try:
                await self.beat()
            except Exception as exc:
                logger.debug("heartbeat error: %s", exc)
            # Circadian-modulated cadence — rest phases beat slower (efficiency).
            phase = self.last_phase or circadian_phase()
            factor = 1.0 / _INTENSITY.get(phase, 0.5)
            await asyncio.sleep(self.interval_seconds * factor)

    # ── §3 reflex arcs — W506 (P2.7(2)) ───────────────────────────────────────────
    #
    # Each responder is ONE check, driven from two places: `beat()` on the rhythm, and a reflex arc
    # registered on the nervous system when a burst of signals accumulates between beats. The arc is the
    # wake-up, never a second copy of the threshold - `register_reflex` accumulates signals of a TYPE, which
    # cannot express "health below 0.5", so the callback re-reads the real state and the real threshold
    # decides. Every responder returns WHAT IT DID, so a caller never has to infer it.

    def respond_to_health(self) -> Dict[str, Any]:
        """Read the immune health and alert when it is below the homeostasis threshold."""
        out: Dict[str, Any] = {"read": False, "health": None, "alerted": False}
        try:
            from agentic_core.organism.immune import immune
            health = immune.status().get("health")
            out["read"], out["health"] = True, health
            if health is not None and health < 0.5:
                from agentic_core.organism.biobus import biobus
                biobus.fire_signal("reflex", "organism.heartbeat.alert", f"health {health}", 0.9)
                out["alerted"] = True
        except Exception as exc:
            out["error"] = f"{exc.__class__.__name__}: {exc}"
        return out

    def respond_to_energy(self) -> Dict[str, Any]:
        """Rest and recover when the energy ratio is depleted (§8 survival instinct on the beat)."""
        out: Dict[str, Any] = {"read": False, "atp": None, "recovered": False}
        try:
            from agentic_core.organism.biobus import atp_depletion_state, biobus
            atp = (biobus.organism_context().get("metabolic", {}) or {}).get("atp_ratio", 1.0)
            out["read"], out["atp"] = True, atp
            # §8 (W506, P2.7(4)) - this threshold is UNREACHABLE on the current model, and said so rather
            # than silently never firing. Measured from the arithmetic: consumption is at most 0.1 per tick
            # and production at least 0.4 at the lowest efficiency this code passes, so the ratio only rises
            # to its ceiling. P2.7(4)'s label arm requires the survival copy be removed "until the branch can
            # fire"; DERIVING it means the branch starts working by itself if the constants ever change,
            # instead of being deleted and forgotten.
            _dep = atp_depletion_state()
            out["threshold"] = self.ENERGY_THRESHOLD
            out["can_deplete"] = _dep["can_deplete"]
            if not _dep["can_deplete"]:
                out["why_not"] = ("the energy figure cannot fall to the threshold on this model, so no "
                                  "recovery can be triggered by it: " + _dep["basis"])
                return out
            if atp < self.ENERGY_THRESHOLD:     # energy depleted → autonomously rest & recover
                from agentic_core.ai.native.homeostasis import homeostasis
                rec = homeostasis.recover(cycles=3)
                if rec.get("recovered"):
                    self.last_recovery = f"{rec['atp_before']:.0%}->{rec['atp_after']:.0%}"
                    out["recovered"] = True
        except Exception as exc:
            out["error"] = f"{exc.__class__.__name__}: {exc}"
        return out

    def respond_to_circuits(self) -> Dict[str, Any]:
        """Probe circuits that are OPEN past their recovery window (proactive self-healing)."""
        out: Dict[str, Any] = {"read": False, "open_circuits": None, "probed": 0}
        try:
            from agentic_core.organism.self_healing import self_healer
            sh = self_healer.status()
            self.last_self_healing = sh.get("overall_health")
            out["read"], out["open_circuits"] = True, sh.get("open_circuits", 0)
            if sh.get("open_circuits", 0) > 0:
                heal = self_healer.attempt_heal()
                if heal.get("count"):
                    self.last_heal = ",".join(heal["probed"])[:80]
                    out["probed"] = heal["count"]
                    from agentic_core.organism.biobus import biobus
                    biobus.fire_signal("reflex", "organism.heartbeat.self_heal",
                                       f"probed {heal['count']} circuit(s): {self.last_heal}", 0.8)
        except Exception as exc:
            out["error"] = f"{exc.__class__.__name__}: {exc}"
        return out

    # The arcs, declared ONCE. `responder` names a method above; `threshold` is how many signals of
    # `trigger` inside the nervous system's 60s window wake the check. The thresholds are deliberately
    # above the resting rate: one beat fires a single "reflex" pulse, so an arc at 8 cannot be tripped by
    # the rhythm alone - it takes a real burst (errors, regressions, heal probes) to reach it.
    #
    # ONLY THE CHEAP, ACTING CHECKS GET AN ARC. W506 first registered all four and that was wrong twice
    # over, which measuring the suite showed (it ran about twice as slow, because an arc fires inside
    # `nervous.fire` on any caller's stack):
    #   · `respond_to_energy` reads the whole organism context, which touches the config file and advances
    #     the ATP simulator - and its threshold is UNREACHABLE on the current model (P2.7(4)), so the arc
    #     would do that work to react to nothing. An arc whose responder can never act is the dead-branch
    #     class one layer up.
    #   · `respond_to_threat` SUBMITS A GOVERNED CHANGE RECORD and moves a live config lever. A burst of
    #     ordinary error signals would have done that from inside an arbitrary caller, and P2.7(3) asks
    #     only that the HEARTBEAT engage the defence - which it does, on the beat, where a governed change
    #     belongs. The arc was scope I added beyond the criterion and it carried a real hazard.
    # Both still run on the beat. What is left here reads in-memory state and acts on it.
    REFLEX_ARCS = (
        {"name": "organism.reflex.health", "trigger": "reflex", "threshold": 8,
         "responder": "respond_to_health"},
        {"name": "organism.reflex.circuits", "trigger": "reflex", "threshold": 8,
         "responder": "respond_to_circuits"},
    )

    # §8 (W506, P2.7(3)) — the threat scale, ORDERED. A string comparison would put "HIGH" above
    # "CRITICAL" alphabetically and so skip the worst case, silently.
    THREAT_ORDER = ("NOMINAL", "ELEVATED", "HIGH", "CRITICAL")
    DEFEND_AT = "HIGH"
    # §8 (W506, P2.7(4)) - named, because a threshold buried in a comparison cannot be reported and a
    # reader could not see that it is unreachable on the current energy model.
    ENERGY_THRESHOLD = 0.3
    _DEFENCE_COOLDOWN_BEATS = 30     # engage_immune_defence writes a record and moves a live lever

    def respond_to_threat(self) -> Dict[str, Any]:
        """Engage the immune defence when the threat reaches DEFEND_AT. W506 (P2.7(3)).

        The CCA's `immune_reconfigure` route was fully built and had NO caller anywhere, so the organism
        never defended itself: a HIGH threat sat until an admin pressed a button. This calls the ungated
        core, which is the same body the route calls - the reflex is governed and recorded exactly as an
        admin-submitted change is, and the change it creates is revertible through `revert_immune_defence`.
        """
        out: Dict[str, Any] = {"read": False, "threat": None, "engaged": False, "why_not": None}
        try:
            from agentic_core.api.change_control import _immune_threat
            threat = (_immune_threat() or "NOMINAL").upper()
            out["read"], out["threat"] = True, threat
            order = self.THREAT_ORDER
            if threat not in order:
                out["why_not"] = f"the threat level {threat!r} is not on the scale {order}"
                return out
            if order.index(threat) < order.index(self.DEFEND_AT):
                out["why_not"] = f"{threat} is below {self.DEFEND_AT}"
                return out
            # `or` here was a falsy-ZERO defect: a defence engaged on beat 0 stored 0, and
            # `0 or -10**9` is the sentinel, so the cooldown never applied and a sustained threat
            # submitted a change on every beat. The guard caught it; a probe that had already beaten
            # once could not, because beats was then non-zero.
            last = self._last_defence_beat
            since = None if last is None else self.beats - last
            if since is not None and since < self._DEFENCE_COOLDOWN_BEATS:
                out["why_not"] = (f"a defence was engaged {since} beat(s) ago and the cooldown is "
                                  f"{self._DEFENCE_COOLDOWN_BEATS} — a sustained threat must not submit a "
                                  f"change every beat")
                return out
            from agentic_core.api.change_control import engage_immune_defence
            res = engage_immune_defence(threat, requested_by="organism.heartbeat",
                                        requested_by_verified=False)
            self._last_defence_beat = self.beats
            self.last_immune_defence = {
                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "threat": threat, "cca_id": res.get("cca_id"), "status": res.get("status"),
                "reconfiguration": res.get("reconfiguration"),
                # carried so a reader can undo it without first fetching the record — the reversal being
                # available is the difference between a defence and a one-way switch
                "reversible": res.get("reversible"), "revert_with": res.get("revert_with"),
            }
            out["engaged"], out["result"] = True, self.last_immune_defence
        except Exception as exc:
            out["error"] = f"{exc.__class__.__name__}: {exc}"
        return out

    def register_reflexes(self) -> Dict[str, Any]:
        """Register this organism's reflex arcs on the nervous system. Idempotent by name.

        W506 (P2.7(2)) - `register_reflex` had been implemented and never called, so
        `reflex_arcs_registered` was 0 and the heartbeat's three threshold checks ran only on the beat:
        a burst at the start of an interval waited out the whole interval. Idempotent because `start()`
        may be called more than once, and an arc registered twice responds twice to one burst.
        """
        from agentic_core.organism.nervous import nervous
        registered, already = [], []
        existing = {a.get("name") for a in getattr(nervous, "_reflex_arcs", [])}
        for arc in self.REFLEX_ARCS:
            if arc["name"] in existing:
                already.append(arc["name"])
                continue
            responder = getattr(self, arc["responder"])

            def _fire(signal, _responder=responder, _name=arc["name"]) -> None:
                # The reaction is recorded on THIS instance, which is the one `/status` reads - a
                # between-beat response that left no trace would be indistinguishable from none.
                result = _responder()
                self.last_reflex = {"arc": _name, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                    "trigger": getattr(signal, "source", None), "result": result}
                self.reflex_reactions += 1

            nervous.register_reflex(arc["name"], arc["trigger"], arc["threshold"], _fire)
            registered.append(arc["name"])
        return {"registered": registered, "already_registered": already,
                "arcs_on_the_bus": len(getattr(nervous, "_reflex_arcs", []))}

    def start(self) -> None:
        if self._task and not self._task.done():
            return
        self.running = True
        try:            # W506 (P2.7(2)) - the arcs go on the bus before the rhythm does, so a burst in the
            self.register_reflexes()   # first interval is already answered. Idempotent, so a restart is safe.
        except Exception as exc:
            logger.debug("reflex registration deferred: %s", exc)
        try:
            self._task = asyncio.create_task(self.run())
        except RuntimeError:
            pass  # no running event loop yet (import-time); will be started at app startup

    def stop(self) -> None:
        self.running = False

    def _step_failed(self, step: str, err: BaseException) -> None:
        """Record a beat step that was ATTEMPTED AND FAILED. It NEVER appends to `actions`.

        W589's rule, kept: claiming an action for a failure would be the opposite defect. `actions` stays
        the list of what the beat DID; this dict is what it TRIED AND COULD NOT DO. A reader comparing the
        two can tell a quiet beat from a broken one, which a shorter actions list alone cannot express.
        """
        self.last_step_failures[step] = f"{err.__class__.__name__}: {err}"

    def _compliance_beat(self) -> Optional[Dict[str, Any]]:
        """§11 (W288) — re-screen the least-recently-screened LIVING VSB (round-robin).
        Returns a compact reading or None with no living VSBs."""
        from agentic_core.config import data_path
        from agentic_core.economy.living_vsbs import list_living
        living = (list_living() or {}).get("living_vsbs") or []
        if not living:
            return None
        # W506 (FU-075) - a partial read makes entries look ABSENT, so their last_at reads "" and they
        # sort first. That is fail-safe for this rotation (a lost history is re-screened soonest) and the
        # behaviour is unchanged; the incompleteness is logged so it is attributable rather than invisible.
        from agentic_core.config import read_json_reported
        hist, _hist_why = read_json_reported(data_path("vsb_compliance_history.json"), {})
        hist = hist or {}
        if _hist_why:
            logger.error("the VSB compliance history could not be read whole, so this rotation may be "
                         "choosing on incomplete timestamps: %s", _hist_why)
        target = sorted(living, key=lambda v: ((hist.get(v.get("vsb_id"), {}) or {}).get("last_at") or ""))[0]
        _vsb_res = screen_living_vsb(target.get("vsb_id"))
        #  P3.2 clause (4) — THE BEAT EXTENDS TO LIVING DELIVERABLES, one per beat, least-recently-screened
        #  first: the same rotation as the VSB one above, so the per-beat cost stays bounded and a fleet is
        #  covered over time rather than all at once. Its own failure is RECORDED and never swallowed.
        try:
            _dlv_res = screen_one_deliverable()
        except Exception as _dlv_err:        # noqa: BLE001 — recorded, never swallowed (FU-461's class)
            _dlv_res = {"screened": None,
                        "could_not_run": f"{_dlv_err.__class__.__name__}: {_dlv_err}"}
        if isinstance(_vsb_res, dict):
            #  `vsb_screened` and `vsb_basis` on BOTH returns, so a reader asking which VSB this beat
            #  screened does not get undefined on the normal path and a value on the fallback one.
            return {**_vsb_res, "vsb_screened": target.get("vsb_id"),
                    "vsb_basis": "a living VSB was screened on this beat",
                    "deliverable_screen": _dlv_res}
        #  THE DELIVERABLE SCREEN IS NOT DISCARDED WHEN THE VSB HALF HAS NOTHING TO SAY.
        #  `screen_living_vsb` is declared Optional and returns None when its target has left the roster
        #  between the read above and the lookup inside it. Returning _vsb_res unchanged there would mean a
        #  deliverable was screened, its verdict written to the record, and the beat reported NOTHING about
        #  it - screened, persisted, and read by nobody, which is the reach class this plan keeps finding.
        #  The `if not living: return None` path above is deliberately left alone: deliverables belong to
        #  entities (§13), and making the beat append `compliance_rescreen` on a beat that screened nothing
        #  would change what that action MEANS to the readers at :470 who treat it as "a VSB was screened".
        return {"vsb_screened": None,
                "vsb_basis": "no living VSB could be screened this beat (its target left the roster between "
                             "the roster read and the screen), so the VSB half of this reading is absent "
                             "rather than clean",
                "deliverable_screen": _dlv_res}

    # §3 · §4.10 · §12 (W420) — the autonomy settings are DURABLE. Until now configure() wrote to
    # instance attributes only, so every one of these reverted to False on restart. A user who
    # switched on the behaviour the product is named for ("once established it runs, maintains,
    # defends, improves and grows itself") silently lost it the next time the process came up, and
    # nothing said so. Persisted here and reloaded in _load_autonomy() at construction.
    _AUTONOMY_KEYS = ("auto_evolve", "auto_economy", "auto_align", "auto_compliance", "auto_ship")

    def _evolution_auto_apply(self) -> Dict[str, Any]:
        """Current state of the CCA-governed post-approval auto-apply lever, with its path."""
        try:
            from agentic_core.organism.reconfiguration import _load_config
            on = bool(((_load_config() or {}).get("organism") or {}).get("evolution_auto_apply"))
        except Exception as exc:  # noqa: BLE001 — a config read must not break status
            return {"enabled": None, "readable": False, "error": str(exc),
                    "governed_by": "Change Control Agency"}
        return {
            "enabled": on,
            "readable": True,
            "governed_by": "Change Control Agency",
            "consumer": "organism.heartbeat applies CCA-APPROVED evolution proposals each beat",
            "how_to_change": "submit a change request to the CCA at /change-control",
            "why_not_a_toggle": "the arms-length approval it sits behind is the point",
            "effect_when_off": "approved evolution proposals are never applied; they wait",
        }

    def _autonomy_store(self):
        from agentic_core.config import data_path
        return data_path("organism_autonomy.json")

    def _load_autonomy(self) -> None:
        """Restore persisted autonomy settings. Never raises: a missing or corrupt store leaves the
        safe defaults (all False) in place rather than failing the organism's construction."""
        import json as _json
        try:
            p = self._autonomy_store()
            if not p.exists():
                return
            saved = _json.loads(p.read_text(encoding="utf-8"))
            for k in self._AUTONOMY_KEYS:
                if isinstance(saved.get(k), bool):
                    setattr(self, k, saved[k])
            if isinstance(saved.get("interval_seconds"), int):
                self.interval_seconds = max(5, saved["interval_seconds"])
            self.autonomy_restored_at = saved.get("saved_at")
        except Exception as exc:  # noqa: BLE001 — autonomy state must never block startup
            logger.warning("autonomy settings could not be restored (%s); defaults stand", exc)

    def _save_autonomy(self) -> None:
        from agentic_core.config import atomic_write_json
        payload = {k: getattr(self, k) for k in self._AUTONOMY_KEYS}
        payload["interval_seconds"] = self.interval_seconds
        payload["saved_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            atomic_write_json(self._autonomy_store(), payload)
        except Exception as exc:  # noqa: BLE001 — a failed save must not silently look like success
            logger.error("autonomy settings NOT persisted (%s) — they will revert on restart", exc)
            self.autonomy_persisted = False
            return
        self.autonomy_persisted = True

    def configure(self, interval_seconds: Optional[int] = None,
                  auto_evolve: Optional[bool] = None, auto_economy: Optional[bool] = None,
                  auto_align: Optional[bool] = None,
                  auto_compliance: Optional[bool] = None,
                  auto_ship: Optional[bool] = None) -> None:
        if interval_seconds is not None:
            self.interval_seconds = max(5, int(interval_seconds))
        if auto_evolve is not None:
            self.auto_evolve = bool(auto_evolve)
        if auto_economy is not None:
            self.auto_economy = bool(auto_economy)
        if auto_align is not None:
            self.auto_align = bool(auto_align)
        if auto_compliance is not None:
            self.auto_compliance = bool(auto_compliance)
        if auto_ship is not None:
            self.auto_ship = bool(auto_ship)
        self._save_autonomy()

    def _reflex_arc_count(self):
        """How many arcs are actually ON the bus, or None when the bus cannot be read. W506 (P2.7(2)).

        Read from the nervous system rather than from `REFLEX_ARCS`, because the declaration says what this
        organism INTENDS to register and only the bus says what is registered - a registration that failed
        must not be reported as one that succeeded.
        """
        try:
            from agentic_core.organism.nervous import nervous
            return len(getattr(nervous, "_reflex_arcs", []))
        except Exception:
            return None

    def status(self) -> Dict[str, Any]:
        return {
            "running": self.running,
            "beats": self.beats,
            "circadian_phase": self.last_phase or circadian_phase(),
            "phase_intensity": _INTENSITY.get(self.last_phase or circadian_phase(), 0.5),
            "last_beat": self.last_beat,
            "last_realisation": self.last_realisation,
            "last_self_healing": self.last_self_healing,
            "last_recovery": self.last_recovery,
            "last_heal": self.last_heal,
            "last_genome": self.last_genome,
            "last_cadence": self.last_cadence,
            "last_twin_directive": self.last_twin_directive,
            "last_evolution": self.last_evolution,
            "last_vsb_operated": self.last_vsb_operated,
            # W503 — `last_vsb_operated` only ever names an entity a cycle RAN for; these say what
            # happened on the visits that did not run one, which used to leave no record at all.
            "last_vsb_failed": self.last_vsb_failed,
            "last_vsb_not_operated": self.last_vsb_not_operated,
            "last_transfer_reconcile": self.last_transfer_reconcile,
            "last_intake_reconcile": self.last_intake_reconcile,
            "last_vsb_evolved": self.last_vsb_evolved,
            "last_reshipped": getattr(self, "last_reshipped", None),
            "auto_ship": self.auto_ship,
            "interval_seconds": self.interval_seconds,
            "auto_evolve": self.auto_evolve,
            "auto_economy": self.auto_economy,
            "auto_align": self.auto_align,
            "auto_compliance": self.auto_compliance,          # §11 (W288) — continuous re-screening
            # W420 — the UI must be able to say whether these survive a restart. `False` here means a
            # save FAILED and the choice will be lost; the surface says so rather than implying it stuck.
            "autonomy_persisted": self.autonomy_persisted,
            "autonomy_restored_at": self.autonomy_restored_at,
            # §8 (W424) — `evolution_auto_apply` has a REAL consumer on this beat (it applies
            # CCA-approved evolution proposals) and had no UI anywhere, so a user could not
            # see whether approved work would ever land. Reported READ-ONLY on purpose: it is
            # a governed lever set through Change Control, not a free toggle, and surfacing a
            # switch here would route around the arms-length approval it exists behind.
            "evolution_auto_apply": self._evolution_auto_apply(),
            "last_compliance": self.last_compliance,
            # W506 (P2.7(2)) - the REFLEX ARCS, said rather than implied. `reflex_arcs_registered`
            # was 0 for the platform's whole life because register_reflex had no caller, so the
            # three threshold checks below ran only on the beat. `reflex_reactions` counts the times
            # an arc drove one BETWEEN beats; 0 with arcs registered means no burst has occurred,
            # which is different from no arcs being on the bus, so both are reported.
            "reflex_arcs_registered": self._reflex_arc_count(),
            "reflex_arcs": [a["name"] for a in self.REFLEX_ARCS],
            "reflex_reactions": self.reflex_reactions,
            "last_reflex": self.last_reflex,
            # §8 (W506, P2.7(3)) - the defence the organism engaged ITSELF, with the way back. Before
            # this round nothing called the reconfigurator, so this was structurally always absent.
            "last_immune_defence": self.last_immune_defence,
            "defends_at": self.DEFEND_AT,
            "recent": self._log[-10:],
            "integrations": ["circadian", "central_nervous_system", "immune", "self_healing",
                             "metabolic_atp", "genome", "UEG_audit", "constitutional_arms_length"],
            # W545 (FU-344) — THE METABOLIC CYCLE'S OUTCOME, which this surface did not carry.
            # Section 2g has recorded `cycle_status`, `emitted` and `withheld_reason` since W533, and
            # NOTHING SERVED ANY OF IT: not this status dict, not a route, not a page. So the platform's
            # NORMAL state — a full six-stage cycle that measures every latency and then deliberately
            # delivers nothing, because the clearance chain withholds the emission for want of a
            # constitutional verdict — was visible only inside the heartbeat object. An operator reading
            # this surface saw a running beat with no breaches and would reasonably infer the avatar was
            # emitting. A withheld outcome that renders as a healthy beat is a delivery claim made by
            # omission, which is the defect class this programme keeps removing one layer up.
            # None here means the cycle has not run on this process (the lever is off by default), which
            # is different from a cycle that ran and withheld — and the consumer can tell them apart
            # because a cycle that ran carries `cycle_status`.
            "last_metabolic": self.last_metabolic,
            "metabolic_basis": (
                "the metabolic cycle has not run on this process, so there is no outcome to report — the "
                "loop is paced and OFF by default, and this is not a withheld emission"
                if self.last_metabolic is None else
                (self.last_metabolic.get("basis")
                 or "the cycle ran but recorded no basis for its outcome")),
            "note": "Continuous circadian autonomy — cheap pulse every beat; expensive cognition opt-in + paced.",
        }


# Singleton
heartbeat = OrganismHeartbeat()
