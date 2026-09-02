"""
Homeostatic Cognition Controller — closes the §8 biomimetic homeostasis loop around §6 cognition.

The vision (§8) requires the living organism's homeostasis (immune ↔ nervous ↔ metabolic) + circadian
operation + a survival instinct to make the platform "dynamic, adaptive, responsive" — and (§6) the native
AI swarm/orchestration is the cognitive work that loop must govern. Previously the native orchestrator only
read the IMMUNE threat (throttling concurrency); circadian rhythm and metabolic ATP did not modulate
cognition, and cognitive work did not feed back into metabolic load.

This controller closes both directions, using the real organism state (never fabricated):
  • READ  — `biobus.organism_context()` yields composite health (immune·self-healing·metabolic), circadian
            cycle, ATP ratio, immune threat, and a homeostatic recommendation. The native fabric admits
            cognitive work (max concurrent agents) as a function of ALL of these, not immune alone.
  • WRITE — the cognitive demand is passed as `metabolic_load`, so heavier swarm work EXPENDS more ATP
            (organism_context → _update_atp → ATPSimulator.update), depleting energy that then recovers on
            the circadian cycle. The loop is closed: cognition consumes energy; low energy throttles
            cognition; rest restores it.
"""
from __future__ import annotations

from typing import Any, Dict


def _fire(signal_type: str, source: str, msg: str, intensity: float = 0.4) -> None:
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal(signal_type, source, msg[:80], intensity)
    except Exception:
        pass


class HomeostaticController:
    """Admits native-AI cognitive work as a function of the whole living-organism state, and feeds the
    cognitive demand back into the metabolic loop. In-house, real organism state — best-effort and
    fail-open (if the organism is unavailable, cognition proceeds at the requested capacity)."""

    def assess(self, demand_nodes: int = 1, requested_parallel: int = 4) -> Dict[str, Any]:
        """Compute the homeostatic cognitive posture for a unit of work.

        `demand_nodes` scales the metabolic load (more agents = more energy expended — the WRITE side of
        the loop); `requested_parallel` is the caller's desired concurrency, which we cap by the organism's
        homeostatic headroom. Returns the admitted `max_parallel`, a `posture`, and the live organism state.
        """
        # WRITE side: cognitive demand → metabolic load (0.2 floor; grows with the agent count, capped 1.0).
        load = max(0.2, min(1.0, 0.2 + max(0, demand_nodes) * 0.08))
        try:
            from agentic_core.organism.biobus import biobus
            ctx = biobus.organism_context(metabolic_load=load)   # READ + feeds ATP via _update_atp(load)
        except Exception:
            return {"max_parallel": max(1, int(requested_parallel)), "posture": "full",
                    "metabolic_load": round(load, 3), "organism": None,
                    "governed_by": "homeostatic controller (organism unavailable — fail-open)"}

        rec = ctx.get("recommended", {}) or {}
        immune_threat = (ctx.get("immune", {}) or {}).get("threat_level", "NOMINAL")
        cycle = (ctx.get("circadian", {}) or {}).get("cycle", "")
        _atp_raw = (ctx.get("metabolic", {}) or {}).get("atp_ratio")
        atp = float(_atp_raw) if _atp_raw is not None else 1.0   # W438: the biobus fallback carries None

        # Cap concurrency by the WHOLE-organism recommendation (composite health: immune·self-healing·
        # metabolic), then apply the survival-instinct immune floor (preserves prior protective behaviour).
        cap = min(int(requested_parallel), int(rec.get("max_parallel_agents", requested_parallel)))
        if immune_threat in ("HIGH", "CRITICAL"):
            cap = 1
        elif immune_threat == "ELEVATED":
            cap = min(cap, 2)
        if atp < 0.3:                       # metabolic survival instinct: protect remaining energy
            cap = 1
        cap = max(1, cap)

        if bool(rec.get("should_throttle")) or cap == 1 or atp < 0.3:
            posture = "protected"           # organism is defending itself — minimal cognitive load
        elif cycle != "ACTIVE_FOCUS" or cap < int(requested_parallel):
            posture = "reduced"             # off-peak circadian / partial headroom — measured load
        else:
            posture = "full"                # peak focus, healthy, energised — full cognitive power

        if posture != "full":
            _fire("reflex", "native.homeostasis",
                  f"cognition {posture}: cap={cap} atp={atp:.2f} {cycle} immune={immune_threat}", 0.5)

        return {
            "max_parallel": cap,
            "posture": posture,
            "metabolic_load": round(load, 3),
            "organism": {
                "mode": ctx.get("mode"),
                "composite_health": ctx.get("composite_health"),
                "circadian": cycle,
                "is_peak_focus": cycle == "ACTIVE_FOCUS",
                "atp_ratio": round(atp, 3),
                "immune_threat": immune_threat,
                "should_throttle": bool(rec.get("should_throttle")),
            },
            "governed_by": "homeostatic controller (§8 organism → §6 cognition; real state)",
        }

    def recover(self, cycles: int = 4) -> Dict[str, Any]:
        """§8 SURVIVAL INSTINCT — actively RESTORE metabolic energy (rest), not merely throttle. Runs rest
        cycles on the OWNED ATP simulator (zero cognitive load → net energy production, improved on the
        circadian cycle) and fires a restoration signal. Real metabolic state; best-effort and fail-soft."""
        try:
            from agentic_core.organism.biobus import _get_atp, _circadian_cycle
            atp = _get_atp()
            if not atp:
                return {"recovered": False, "reason": "metabolic simulator unavailable"}
            before = round(min(1.0, atp.ratio / 15.0), 3)
            eff = 1.0 if _circadian_cycle() == "ACTIVE_FOCUS" else 0.85   # rest is most efficient at peak
            for _ in range(max(1, int(cycles))):
                atp.update(dt=1.0, metabolic_load=0.0, circadian_efficiency=eff)
            after = round(min(1.0, atp.ratio / 15.0), 3)
            _fire("reflex", "native.homeostasis",
                  f"metabolic recovery (rest): ATP {before:.2f}->{after:.2f}", 0.5)
            return {"recovered": bool(after > before), "atp_before": before, "atp_after": after,
                    "cycles": int(cycles), "method": "ATP rest cycles (owned metabolic simulator)"}
        except Exception as e:
            return {"recovered": False, "reason": str(e)[:80]}

    def project(self, demand_nodes: int) -> Dict[str, Any]:
        """Read-only §7 PRE-COMMIT projection: the CURRENT living-organism posture + admitted concurrency,
        and whether a cognitive demand of `demand_nodes` fits within it RIGHT NOW. Models, does not run —
        no extra ATP is expended (a simulation shouldn't consume energy); the actual run is governed by §8
        homeostasis at execution time."""
        snap = self.snapshot()
        cap = int(snap.get("max_parallel", 4))
        return {
            "projected_posture": snap.get("posture"),
            "admitted_max_parallel": cap,
            "demand_nodes": int(max(0, demand_nodes)),
            "fits_current_capacity": int(max(0, demand_nodes)) <= cap,
            "organism": snap.get("organism"),
            "note": "current §8 living-organism capacity — the run will be homeostatically governed at execution time",
        }

    def snapshot(self) -> Dict[str, Any]:
        """Read-only current homeostatic posture (no extra metabolic load) — for surfacing live."""
        return self.assess(demand_nodes=0, requested_parallel=4)


homeostasis = HomeostaticController()
