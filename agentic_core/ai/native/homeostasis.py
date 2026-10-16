"""
Homeostatic Cognition Controller — closes the §8 biomimetic homeostasis loop around §6 cognition.

The vision (§8) requires the living organism's homeostasis (immune ↔ nervous ↔ metabolic) + circadian
operation + a survival instinct to make the platform "dynamic, adaptive, responsive" — and (§6) the native
AI swarm/orchestration is the cognitive work that loop must govern. Previously the native orchestrator only
read the IMMUNE threat (throttling concurrency); circadian rhythm and metabolic ATP did not modulate
cognition, and cognitive work did not feed back into metabolic load.

What it reads and what it writes (W742 - stated as the code does it, not as the loop was first drawn):
  • READ   — `biobus.organism_context()` yields composite health, circadian cycle, the ATP ratio, immune
             threat and a homeostatic recommendation. Admission (max concurrent agents) is capped by that
             recommendation and by the immune floor. The ATP term is a SIMULATOR whose production exceeds its
             consumption on the current model, so its `< 0.3` floor cannot fire; each answer computes this as
             `organism.atp_can_fall`.
  • BUDGET — the work budget (molecular/work_budget.py, Owner ruling S18.1) is the energy figure that CAN run
             down. Behind WORKSTATION_WORK_BUDGET (off by default) its gate holds admission at 1 once the
             window's capacity is spent, or while its store cannot be read.
  • WRITE  — a RUN passes its demand as `metabolic_load`, which asks the ATP simulator to advance
             (organism_context → _update_atp). A projection (`snapshot`, `project`) reads without asking.
"""
from __future__ import annotations

from typing import Any, Dict

from agentic_core.molecular import work_budget as _work_budget

#  W742 (S18.1) - this controller is the one reader of the work budget's throttle, and registers itself where the
#  budget computes `gates_anything`, so that field is true only while a reader that acts on it is loaded.
_work_budget.register_consumer(
    "native homeostasis admission",
    "while the gate holds, the native tree and the org cascade run their nodes one at a time; single model "
    "calls, deliverables and every other AI door are not held, and no run is refused or deferred")


def _fire(signal_type: str, source: str, msg: str, intensity: float = 0.4) -> None:
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal(signal_type, source, msg[:80], intensity)
    except Exception:
        pass


# W506 (FU-265d) — the ATP threshold, named once. It was a bare 0.3 in two comparisons, so no surface
# could report it and no reader could see that the figure cannot reach it.
_ATP_CONSERVE_AT = 0.3


class HomeostaticController:
    """Admits native-AI cognitive work as a function of the living-organism state and the work budget, and
    feeds a run's cognitive demand back into the metabolic simulator. FAIL-CLOSED (W742): if the organism cannot
    be read, nothing was measured, so admission holds at 1 and the answer says why - never the requested
    capacity on absent evidence (W494 clause 1)."""

    def assess(self, demand_nodes: int = 1, requested_parallel: int = 4, *,
               read_only: bool = False) -> Dict[str, Any]:
        """Compute the homeostatic cognitive posture for a unit of work.

        `demand_nodes` scales the metabolic load (more agents = more energy expended — the WRITE side of
        the loop); `requested_parallel` is the caller's desired concurrency, which we cap by the organism's
        homeostatic headroom. Returns the admitted `max_parallel`, a `posture`, and the live organism state.

        W742 — `read_only=True` is a projection: the organism is read WITHOUT advancing the ATP simulator
        and no reflex signal is fired, so the projection changes no ATP or reflex state (a caller such as the
        composition preview may still change other state). `atp_mode` says which mode was asked for.
        """
        # WRITE side: cognitive demand → metabolic load (0.2 floor; grows with the agent count, capped 1.0).
        load = max(0.2, min(1.0, 0.2 + max(0, demand_nodes) * 0.08))
        _wb = _work_budget.gate()           # W742 (S18.1) — the throttle the ruling ships inert
        try:
            from agentic_core.organism.biobus import biobus
            ctx = (biobus.organism_context(metabolic_load=load, advance_atp=False) if read_only
                   else biobus.organism_context(metabolic_load=load))   # a RUN reads + feeds ATP via _update_atp
        except Exception as exc:
            #  W742 — FAIL-CLOSED. This branch granted the caller's request under the posture the live path
            #  keeps for peak focus, while nothing had been read. Where nothing was measured the decision HOLDS
            #  (W494 clause 1), and the answer says why.
            return {"max_parallel": 1, "posture": "protected",
                    "metabolic_load": round(load, 3), "atp_mode": "projection" if read_only else "run",
                    "organism": None, "work_budget": _wb,
                    "reason": (f"the organism could not be read ({exc.__class__.__name__}), so nothing was "
                               f"measured and admission holds at 1 rather than granting the "
                               f"{max(1, int(requested_parallel))} requested"),
                    "governed_by": "homeostatic controller (organism unavailable — fail-closed, held at 1)"}

        rec = ctx.get("recommended", {}) or {}
        immune_threat = (ctx.get("immune", {}) or {}).get("threat_level", "NOMINAL")
        cycle = (ctx.get("circadian", {}) or {}).get("cycle", "")
        # W506 (FU-265d) — the metabolic block WHOLE, so its qualifier can travel with its figure
        _met = ctx.get("metabolic", {}) or {}
        from agentic_core.organism.biobus import atp_depletion_state
        _dep = atp_depletion_state()
        _atp_raw = _met.get("atp_ratio")
        atp = float(_atp_raw) if _atp_raw is not None else 1.0   # W438: the biobus fallback carries None

        # Cap concurrency by the WHOLE-organism recommendation (composite health: immune·self-healing·
        # metabolic), then apply the survival-instinct immune floor (preserves prior protective behaviour).
        cap = min(int(requested_parallel), int(rec.get("max_parallel_agents", requested_parallel)))
        if immune_threat in ("HIGH", "CRITICAL"):
            cap = 1
        elif immune_threat == "ELEVATED":
            cap = min(cap, 2)
        if atp < _ATP_CONSERVE_AT:          # metabolic survival instinct: protect remaining energy
            cap = 1
        if _wb.get("holds"):                # W742 (S18.1) — the work budget is spent (or unreadable): serial
            cap = 1
        cap = max(1, cap)

        #  W638 (FU-596) — A CAP THE CALLER ASKED FOR IS NOT A DEFENCE. `cap == 1` alone made every sequential
        #  cascade (which requests 1) report the organism as defending itself while immune was NOMINAL and the
        #  throttle off. Protected means the ORGANISM forced the floor, or cut a larger request down to it.
        _forced_floor = ((immune_threat in ("HIGH", "CRITICAL")) or atp < _ATP_CONSERVE_AT
                         or bool(_wb.get("holds")))
        _cut_to_one = cap == 1 and int(requested_parallel) > 1
        if bool(rec.get("should_throttle")) or _forced_floor or _cut_to_one:
            posture = "protected"           # organism is defending itself — minimal cognitive load
        elif cycle != "ACTIVE_FOCUS" or cap < int(requested_parallel):
            posture = "reduced"             # off-peak circadian / partial headroom — measured load
        else:
            posture = "full"                # peak focus, healthy, energised — full cognitive power

        if posture != "full" and not read_only:     # W742 — a projection fires no signal
            _fire("reflex", "native.homeostasis",
                  f"cognition {posture}: cap={cap} atp={atp:.2f} {cycle} immune={immune_threat}", 0.5)

        return {
            "max_parallel": cap,
            "posture": posture,
            "metabolic_load": round(load, 3),
            #  W742 - the MODE this answer was computed in, not an outcome: a run ASKS the ATP simulator to
            #  advance (biobus throttles that to once a second, so a run inside that second advances nothing);
            #  a projection never asks
            "atp_mode": "projection" if read_only else "run",
            "organism": {
                "mode": ctx.get("mode"),
                "composite_health": ctx.get("composite_health"),
                "circadian": cycle,
                "is_peak_focus": cycle == "ACTIVE_FOCUS",
                "atp_ratio": round(atp, 3),
                # W506 (FU-265d) — the qualifier TRAVELS WITH THE FIGURE. biobus has carried
                # metabolic.measured=False and a basis since W494 and this reader dropped both, so every
                # surface downstream printed the number as a live vital. A figure whose qualifier is
                # available and omitted is the badge-in-the-DOM defect at the API layer.
                "atp_measured": bool(_met.get("measured")),
                "atp_basis": _met.get("basis"),
                "atp_can_fall": _dep["can_deplete"],
                # ...and the posture the ATP term selects is UNREACHABLE on the current model, said rather
                # than silently never chosen (the same dead branch P2.7(4) found in the heartbeat).
                "conserving_posture_reachable": _dep["can_deplete"],
                "conserving_posture_basis": (
                    None if _dep["can_deplete"] else
                    "the 'conserving' posture is selected below an ATP of "
                    f"{_ATP_CONSERVE_AT} and the figure cannot fall to it: " + _dep["basis"]),
                "immune_threat": immune_threat,
                "should_throttle": bool(rec.get("should_throttle")),
            },
            # W506 (FU-265d) — "real state" was doing the work of a claim. The immune, self-healing and
            # circadian terms ARE read from live state; the metabolic one is a simulator, and the sentence
            # covered all of them.
            "work_budget": _wb,
            "governed_by": ("homeostatic controller (§8 organism → §6 cognition). The immune, self-healing and "
                            "circadian terms are read from live state; the metabolic (ATP) term is simulated "
                            "and says so in organism.atp_basis"
                            + (f". The work budget holds admission at 1: {_wb.get('reason')}"
                               if _wb.get("holds") else "")),
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
        the ATP simulator is not advanced and no signal is fired (W742: snapshot reads with read_only=True);
        the actual run is governed by §8 homeostasis at execution time."""
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
        """Read-only current homeostatic posture — the ATP simulator is not advanced and no signal is fired
        (W742) — for surfacing live."""
        return self.assess(demand_nodes=0, requested_parallel=4, read_only=True)


homeostasis = HomeostaticController()
