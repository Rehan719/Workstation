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
        self.interval_seconds = 60            # base cadence (modulated by circadian)
        self.auto_evolve = False              # opt-in: autonomous AI evolution cycles
        self.auto_economy = False             # opt-in: autonomous economy cycles
        self.auto_align = False               # opt-in: route vision gaps to tiers each beat (cheap, plan-only)
        self._evolve_every = 30               # beats between evolution attempts (when enabled)
        self._beats_since_evolve = 0
        self._log: List[Dict[str, Any]] = []
        self._task: Optional["asyncio.Task"] = None
        self._ueg = None

    def _ueg_logger(self):
        if self._ueg is None:
            try:
                from agentic_core.gaas.v5 import UEGLogger
                self._ueg = UEGLogger("meta/gaas_v5_ueg.json")
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
        try:
            from agentic_core.economy.living_vsbs import operate_one
            op = operate_one()
            if op and not op.get("error"):
                self.last_vsb_operated = op.get("vsb_id")
                actions.append("operate_vsb")
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
        if (self.auto_evolve and phase in ("MAINTENANCE_FOCUS", "MAINTENANCE_REST")
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

    def configure(self, interval_seconds: Optional[int] = None,
                  auto_evolve: Optional[bool] = None, auto_economy: Optional[bool] = None,
                  auto_align: Optional[bool] = None) -> None:
        if interval_seconds is not None:
            self.interval_seconds = max(5, int(interval_seconds))
        if auto_evolve is not None:
            self.auto_evolve = bool(auto_evolve)
        if auto_economy is not None:
            self.auto_economy = bool(auto_economy)
        if auto_align is not None:
            self.auto_align = bool(auto_align)

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
            "interval_seconds": self.interval_seconds,
            "auto_evolve": self.auto_evolve,
            "auto_economy": self.auto_economy,
            "auto_align": self.auto_align,
            "recent": self._log[-10:],
            "integrations": ["circadian", "central_nervous_system", "immune", "self_healing",
                             "metabolic_atp", "genome", "UEG_audit", "constitutional_arms_length"],
            "note": "Continuous circadian autonomy — cheap pulse every beat; expensive cognition opt-in + paced.",
        }


# Singleton
heartbeat = OrganismHeartbeat()
