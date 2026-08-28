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


def screen_living_vsb(vsb_id: str) -> Optional[Dict[str, Any]]:
    """§11 — screen ONE living VSB over its current plan + registration text; persist per-VSB
    history (capped); a REGRESSION (prior non-fail → fail) registers with the immune system and
    marks the shipped repo stale (§13 drift honesty, W309). Reusable: the heartbeat's rotation
    (W288) and the ESTABLISHMENT first-screen (W309 — birth is alive) share this one path."""
    from agentic_core.config import atomic_write_json, data_path, load_json_tolerant
    from agentic_core.economy.living_vsbs import list_living
    living = (list_living() or {}).get("living_vsbs") or []
    target = next((v for v in living if v.get("vsb_id") == vsb_id), None)
    if not target:
        return None
    store_path = data_path("vsb_compliance_history.json")
    hist: Dict[str, Any] = load_json_tolerant(store_path, {}) or {}
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
    hist[vsb_id] = {"overall": screen["overall"], "last_at": entries[-1]["at"],
                    "regression": regression, "history": entries}
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
        self.last_evolution: Optional[Dict[str, Any]] = None   # last autonomous evolution (proposals → governance)
        self.last_vsb_operated: Optional[str] = None   # §4 — last living VSB autonomously operated on the beat
        self.last_vsb_evolved: Optional[Dict[str, Any]] = None   # §8×§3 (W309) — last child VSB evolved on the tick
        self.interval_seconds = 60            # base cadence (modulated by circadian)
        self.auto_evolve = False              # opt-in: autonomous AI evolution cycles
        self.auto_economy = False             # opt-in: autonomous economy cycles
        self.auto_ship = False                # opt-in (§13, W319): re-ship STALE repos on the beat
        self.auto_align = False               # opt-in: route vision gaps to tiers each beat (cheap, plan-only)
        self.auto_compliance = False          # opt-in (§11, W288): re-screen living VSBs on the beat
        self.last_compliance: Optional[Dict[str, Any]] = None   # last continuous-compliance reading
        self._evolve_every = 30               # beats between evolution attempts (when enabled)
        self._beats_since_evolve = 0
        self._log: List[Dict[str, Any]] = []
        self._task: Optional["asyncio.Task"] = None
        self._ueg = None

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
        health = None
        try:
            from agentic_core.organism.immune import immune
            health = immune.status().get("health")
            if health is not None and health < 0.5:
                from agentic_core.organism.biobus import biobus
                biobus.fire_signal("reflex", "organism.heartbeat.alert", f"health {health}", 0.9)
            actions.append("homeostasis")
        except Exception:
            pass
        try:
            from agentic_core.organism.biobus import biobus
            atp = (biobus.organism_context().get("metabolic", {}) or {}).get("atp_ratio", 1.0)
            if atp < 0.3:                       # energy depleted → autonomously rest & recover
                from agentic_core.ai.native.homeostasis import homeostasis
                rec = homeostasis.recover(cycles=3)
                if rec.get("recovered"):
                    self.last_recovery = f"{rec['atp_before']:.0%}->{rec['atp_after']:.0%}"
                    actions.append("self_recovery")
        except Exception:
            pass

        # 2c. Self-healing reflex (immune → self-healing on the beat): read the circuit-breaker health and,
        #     when circuits are OPEN past their recovery window, the organism ACTIVELY probes them for
        #     recovery (proactive self-healing, not just passive timeout) — §3 "defends and heals itself".
        try:
            from agentic_core.organism.self_healing import self_healer
            sh = self_healer.status()
            self.last_self_healing = sh.get("overall_health")
            if sh.get("open_circuits", 0) > 0:
                heal = self_healer.attempt_heal()
                if heal.get("count"):
                    self.last_heal = ",".join(heal["probed"])[:80]
                    actions.append("self_heal")
                    from agentic_core.organism.biobus import biobus
                    biobus.fire_signal("reflex", "organism.heartbeat.self_heal",
                                       f"probed {heal['count']} circuit(s): {self.last_heal}", 0.8)
        except Exception:
            pass

        # 2d. Genome vital sign — read the organism's genome-population genetics (count, mean fitness,
        #     generational depth) as part of its self-monitoring, so the genome subsystem joins the living
        #     loop rather than sitting in isolated CRUD. Cheap (file summary), no AI.
        try:
            from agentic_core.api.organism_status import _genome_state
            gs = _genome_state()
            self.last_genome = {"total": gs.get("total_genomes"), "mean_fitness": gs.get("mean_fitness"),
                                "max_generation": gs.get("max_generation")}
            if gs.get("total_genomes"):
                actions.append("genome_scan")
        except Exception:
            pass

        # 2e. §4 — autonomously OPERATE one living VSB enterprise (round-robin, paced): run one virtual economy
        #     cycle for the least-recently-operated established VSB, so each "continually, autonomously operates"
        #     forever. Cheap + deterministic + virtual; the registry is only populated once VSBs are established.
        #     W288 HONESTY FIX: this now actually honours the auto_economy flag — it was settable and
        #     reported in status() but never consulted, so cycles ran regardless of the Owner's setting.
        if self.auto_economy:
            try:
                from agentic_core.economy.living_vsbs import operate_one
                op = operate_one()
                if op and not op.get("error"):
                    self.last_vsb_operated = op.get("vsb_id")
                    actions.append("operate_vsb")
            except Exception:
                pass

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
            except Exception:
                pass

        # 3. Transformation tick — vision-realisation introspection (no AI)
        try:
            from agentic_core.api.transformation import _realise
            self.last_realisation = _realise().get("overall_realisation")
            actions.append("transformation_tick")
        except Exception:
            pass

        # 3b. Autonomous alignment (opt-in, cheap plan-only) — route vision gaps to the living tiers
        if self.auto_align:
            try:
                from agentic_core.api.cognition import align, AlignRequest
                await align(AlignRequest(execute=False))
                actions.append("alignment")
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
                from agentic_core.api.vsb import evolve_vsb, EvolveRequest, _load_vsb
                from agentic_core.economy.living_vsbs import list_living
                _live = (list_living() or {}).get("living_vsbs") or []
                if _live:
                    _t = sorted(_live, key=lambda v: ((_load_vsb(v.get("vsb_id")) or {})
                                                      .get("last_evolved") or ""))[0]
                    _ev = await evolve_vsb(_t.get("vsb_id"),
                                           EvolveRequest(trigger="autonomous heartbeat"), user=None)
                    self.last_vsb_evolved = {"vsb_id": _t.get("vsb_id"),
                                             "generation": (_ev or {}).get("generation")
                                             if isinstance(_ev, dict) else None}
                    actions.append("evolve_vsb")
                    # §12 (W330) — the entity's OWN self_investment funds its evolution
                    try:
                        from agentic_core.economy.living_vsbs import spend_self_investment
                        spend_self_investment(_t.get("vsb_id"), "autonomous evolution cycle")
                    except Exception:
                        pass
            except Exception:
                pass
            # §8 (W310) — the `organism.evolution_auto_apply` lever gets its REAL consumer: when the
            # Owner enables it, CCA-APPROVED evolution proposals are applied on the beat (mutations
            # still gated by the CCA decision — this only automates the post-approval application).
            try:
                if _cfg_org.get("evolution_auto_apply"):
                    from agentic_core.api.vsb import apply_approved_evolution
                    from agentic_core.economy.living_vsbs import list_living as _ll
                    for _v in ((_ll() or {}).get("living_vsbs") or [])[:10]:
                        _ap = apply_approved_evolution(_v.get("vsb_id"))
                        if _ap.get("applied"):
                            actions.append("evolution_applied")
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
                  "actions": actions, "at": self.last_beat}
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

    def start(self) -> None:
        if self._task and not self._task.done():
            return
        self.running = True
        try:
            self._task = asyncio.create_task(self.run())
        except RuntimeError:
            pass  # no running event loop yet (import-time); will be started at app startup

    def stop(self) -> None:
        self.running = False

    def _compliance_beat(self) -> Optional[Dict[str, Any]]:
        """§11 (W288) — re-screen the least-recently-screened LIVING VSB (round-robin).
        Returns a compact reading or None with no living VSBs."""
        from agentic_core.config import data_path, load_json_tolerant
        from agentic_core.economy.living_vsbs import list_living
        living = (list_living() or {}).get("living_vsbs") or []
        if not living:
            return None
        hist: Dict[str, Any] = load_json_tolerant(data_path("vsb_compliance_history.json"), {}) or {}
        target = sorted(living, key=lambda v: ((hist.get(v.get("vsb_id"), {}) or {}).get("last_at") or ""))[0]
        return screen_living_vsb(target.get("vsb_id"))

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
            "last_evolution": self.last_evolution,
            "last_vsb_operated": self.last_vsb_operated,
            "last_vsb_evolved": self.last_vsb_evolved,
            "last_reshipped": getattr(self, "last_reshipped", None),
            "auto_ship": self.auto_ship,
            "interval_seconds": self.interval_seconds,
            "auto_evolve": self.auto_evolve,
            "auto_economy": self.auto_economy,
            "auto_align": self.auto_align,
            "auto_compliance": self.auto_compliance,          # §11 (W288) — continuous re-screening
            "last_compliance": self.last_compliance,
            "recent": self._log[-10:],
            "integrations": ["circadian", "central_nervous_system", "immune", "self_healing",
                             "metabolic_atp", "genome", "UEG_audit", "constitutional_arms_length"],
            "note": "Continuous circadian autonomy — cheap pulse every beat; expensive cognition opt-in + paced.",
        }


# Singleton
heartbeat = OrganismHeartbeat()
