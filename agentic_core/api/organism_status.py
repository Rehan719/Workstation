"""
Master Organism Status API — unified view of all IDBO biomimetic systems.

This is the single authoritative surface for the organism's complete health
and operational state. Integrates:
  - Immune system (error monitoring, threat level)
  - Nervous system (signal routing, arousal state)
  - Self-healing (circuit breaker status)
  - Metabolic (ATP ratio, energy efficiency)
  - Circadian (work cycle, timing regulation)
  - Genome (entity trait encoding)
  - Reconfiguration (runtime config)
  - Change Control (pending and recent decisions)
  - Project lifecycle position (concept→commercialise)

  GET  /api/v1/organism/status         — full unified organism state
  GET  /api/v1/organism/health-summary — compact health for operational decisions
  POST /api/v1/organism/homeostasis    — trigger auto-regulatory adjustment
  GET  /api/v1/organism/lifecycle      — concept→commercialise pipeline state
  GET  /api/v1/organism/systems        — individual system statuses
  GET  /api/v1/organism/signals        — recent nervous system signal feed
"""
from __future__ import annotations

import datetime
import json
import time
from pathlib import Path
from agentic_core.config import data_path

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus
from agentic_core.organism.immune import immune
from agentic_core.organism.nervous import nervous
from agentic_core.organism.self_healing import self_healer

router = APIRouter(prefix="/api/v1/organism", tags=["idbo-organism"])


# ── Helpers ───────────────────────────────────────────────────────────────────

def _lifecycle_state() -> dict:
    """Aggregate project lifecycle across all projects."""
    try:
        from agentic_core.projects.api import _all_projects
        projects = _all_projects()
        stage_counts = {"concept": 0, "prototype": 0, "commercialise": 0}
        running = 0
        for p in projects:
            s = getattr(p, "stage", getattr(p, "status", "concept"))
            if s in stage_counts:
                stage_counts[s] += 1
            if getattr(p, "status", "") == "running":
                running += 1
        total = len(projects)
        commercialised = stage_counts.get("commercialise", 0)
        completion_rate = round(commercialised / total, 3) if total else 0.0
        # W438 — "GROWING" used to be earned by mere existence (4 idle projects, nothing running,
        # nothing ever advanced -> GROWING). Growth now requires recent activity, and the rule ships
        # with the verdict.
        import time as _time
        recent_cutoff = _time.time() - 30 * 86400
        def _ts(p):
            # W438 refuter catch: the Project model stores created_at/updated_at as EPOCH FLOATS;
            # the first version parsed only ISO strings, so recently_touched was structurally zero
            # and GROWING was unreachable while its basis claimed a measurement
            for attr in ("updated_at", "created_at"):
                v = getattr(p, attr, None)
                if v:
                    try:
                        return float(v)
                    except (TypeError, ValueError):
                        pass
                    try:
                        return _time.mktime(_time.strptime(str(v)[:19], "%Y-%m-%dT%H:%M:%S"))
                    except ValueError:
                        pass
            return 0.0
        recently_touched = sum(1 for p in projects if _ts(p) > recent_cutoff)
        health = ("FLOURISHING" if completion_rate > 0.3 else
                  "GROWING" if recently_touched > 0 else
                  "STATIC" if total > 0 else "DORMANT")
        return {
            "total_projects": total,
            "by_stage": stage_counts,
            "running": running,
            "commercialisation_rate": completion_rate,
            "pipeline_health": health,
            "pipeline_health_basis": (f"FLOURISHING: >30% commercialised · GROWING: any project "
                                      f"touched in 30 days ({recently_touched} were) · STATIC: "
                                      f"projects exist but idle · DORMANT: none"),
        }
    except Exception:
        return {"total_projects": 0, "by_stage": {}, "running": 0, "commercialisation_rate": 0.0,
                "pipeline_health": "UNKNOWN", "pipeline_health_basis": "lifecycle state unreadable"}


def _vsb_state() -> dict:
    """Aggregate VSB entity state."""
    try:
        vsb_store = data_path("vsb_entities")
        if not vsb_store.exists():
            return {"total": 0, "active": 0, "domains": []}
        entities = []
        for p in vsb_store.glob("*.json"):
            try:
                v = json.loads(p.read_text())
                entities.append(v)
            except Exception:
                pass
        # W438 — the only status the VSB writer persists is "operational"; this counted "active",
        # so the figure was structurally ZERO forever and silently HALVED commercialisation_readiness
        # for any org with VSBs (spawning VSBs lowered reported readiness)
        by_status: dict[str, int] = {}
        for v in entities:
            s = str(v.get("status") or "unknown")
            by_status[s] = by_status.get(s, 0) + 1
        operational = sum(n for s, n in by_status.items() if s in ("operational", "active"))
        domains = sorted({v.get("domain", "") for v in entities if v.get("domain")})
        return {"total": len(entities), "operational": operational, "by_status": by_status,
                "domains": domains[:10], "domains_total": len(domains)}
    except Exception:
        return {"total": 0, "operational": 0, "by_status": {}, "domains": [], "domains_total": 0}


def _cca_state() -> dict:
    """Get CCA queue summary."""
    try:
        cca_store = data_path("change_control")
        if not cca_store.exists():
            return {"pending": 0, "approved": 0, "implemented": 0}
        pending = approved = implemented = 0
        for p in cca_store.glob("*.json"):
            try:
                c = json.loads(p.read_text())
                s = c.get("status", "")
                if s in ("submitted", "under_review"):
                    pending += 1
                elif s == "approved":
                    approved += 1
                elif s == "implemented":
                    implemented += 1
            except Exception:
                pass
        return {"pending": pending, "approved": approved, "implemented": implemented}
    except Exception:
        return {"pending": 0, "approved": 0, "implemented": 0}


def _genome_state() -> dict:
    """Summarise the genome registry as real population genetics: count, mean fitness, generational depth,
    and the population's dominant trait — the organism's genetic health (computed from the stored genomes,
    no fabrication)."""
    import json as _json
    try:
        genome_store = data_path("genomes")
        if not genome_store.exists():
            return {"total_genomes": 0, "mean_fitness": None, "max_generation": 0, "dominant_trait": None}
        files = list(genome_store.glob("*.json"))
        if not files:
            return {"total_genomes": 0, "mean_fitness": None, "max_generation": 0, "dominant_trait": None}
        fitnesses: list[float] = []
        max_gen = 0
        trait_sums: dict[str, float] = {}
        trait_counts: dict[str, int] = {}
        for p in files:
            try:
                g = _json.loads(p.read_text())
            except Exception:
                continue
            f = g.get("fitness_score")
            if isinstance(f, (int, float)):
                fitnesses.append(float(f))
            max_gen = max(max_gen, int(g.get("generation", 0) or 0))
            for axis, val in (g.get("traits") or {}).items():
                if isinstance(val, (int, float)):
                    trait_sums[axis] = trait_sums.get(axis, 0.0) + float(val)
                    trait_counts[axis] = trait_counts.get(axis, 0) + 1
        mean_fitness = round(sum(fitnesses) / len(fitnesses), 3) if fitnesses else None
        # §4.5 class (W433) — this took the first maximal key in dict order (the guard forbids that
        # expression appearing anywhere in this file, comments included, which is why it is described
        # rather than reproduced), and the trait axes insert in a fixed order, so a tie always crowned the same
        # axis. This surface's own docstring calls it "the single authoritative surface for the
        # organism's complete health", and this field claims the population's DOMINANT trait, so an
        # arbitrary pick is a claim about genetics that nothing measured.
        dominant, tied = None, []
        if trait_sums:
            means = {a: trait_sums[a] / trait_counts[a] for a in trait_sums}
            _top = max(means.values())
            tied = sorted(a for a, v in means.items() if v == _top)
            # With every axis equal there is no dominant trait at all — a flat population is a real
            # finding, not an occasion to name the alphabetically-first axis.
            dominant = tied[0] if len(tied) == 1 else None
        return {"total_genomes": len(files), "mean_fitness": mean_fitness,
                "max_generation": max_gen, "dominant_trait": dominant,
                "dominant_trait_tied": tied if len(tied) > 1 else [],
                "dominant_trait_basis": ("no numeric traits stored" if not trait_sums else
                                         f"{len(tied)} trait axes tie at the top - none dominates"
                                         if len(tied) > 1 else f"highest mean of {len(means)} axes")}
    except Exception:
        return {"total_genomes": 0, "mean_fitness": None, "max_generation": 0, "dominant_trait": None,
                "dominant_trait_tied": [], "dominant_trait_basis": "unavailable (read error)"}


# ── Main status endpoint ──────────────────────────────────────────────────────

@router.get("/status")
async def organism_status():
    """
    Full unified IDBO organism status — all systems, all metrics.
    The definitive health surface for the living digital organisation.
    """
    ctx = biobus.organism_context()
    ns = nervous.status()
    imm = immune.status()
    sh = self_healer.status()
    lifecycle = _lifecycle_state()
    vsb = _vsb_state()
    cca = _cca_state()
    genome = _genome_state()

    # Reconfiguration engine config
    try:
        from agentic_core.organism.reconfiguration import _load_config
        reconfig = _load_config()
        features = reconfig.get("features", {})
        domains_config = reconfig.get("domains", {})
    except Exception:
        features = {}
        domains_config = {}

    return {
        "organism": "Workstation IDBO",
        "version": "1.0.0",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),

        # ── Composite health — with the W438 disclosure passthrough: the W422 measured-only
        # score and per-term breakdown existed ONLY inside biobus; no HTTP surface carried them ──
        "composite_health": ctx["composite_health"],
        "composite_health_measured_only": ctx.get("composite_health_measured_only"),
        "composite_health_terms": ctx.get("composite_health_terms"),
        "mode": ctx["mode"],
        "health_summary": ctx["health_summary"],
        **({"context_error": ctx["error"]} if ctx.get("error") else {}),

        # ── Biomimetic systems ────────────────────────────────────────────────
        "systems": {
            "immune": {
                "health": imm["health"],
                "threat_level": imm["threat_level"],
                "errors_in_window": imm["errors_in_window"],
                "response_playbook": imm["response_playbook"],
                # W438 — the projection used to drop the W433 companion fields, so at THIS surface
                # a null was ambiguous (no errors vs tie) and one stray error read as genuinely hot
                "hot_endpoint": imm.get("hot_endpoint"),
                "hot_endpoint_errors": imm.get("hot_endpoint_errors"),
                "hot_endpoint_tied": imm.get("hot_endpoint_tied"),
            },
            "nervous": {
                "arousal_state": ns["arousal_state"],
                "signal_rate_per_second": ns["signal_rate_per_second"],
                "signals_last_60s": ns["signals_last_60s"],
                "by_type": ns.get("by_type_last_60s", {}),
                "total_signals": ns.get("total_signals", {}),
                "reflex_arcs": ns["reflex_arcs_registered"],
            },
            "self_healing": {
                "overall_health": sh["overall_health"],
                "open_circuits": sh["open_circuits"],
                "recent_events": sh["healing_log"][:3],
            },
            "metabolic": ctx["metabolic"],
            "circadian": ctx["circadian"],
            "genome": genome,
            "reconfiguration": {
                "features_active": sum(1 for v in features.values() if v is True),
                "domains_enabled": sum(1 for d in domains_config.values() if d.get("enabled")),
                "rpm_limit": ctx["runtime_config"]["rpm_limit"],
                "preferred_provider": ctx["runtime_config"]["preferred_provider"],
            },
        },

        # ── Operational state ─────────────────────────────────────────────────
        "operations": {
            "lifecycle": lifecycle,
            "vsb": vsb,
            "change_control": cca,
        },

        # ── Recommended behaviour ─────────────────────────────────────────────
        "recommended": ctx["recommended"],
    }


def _health_basis(ctx: dict) -> str:
    """Derive the basis from the terms' ACTUAL measured flags — never a constant assertion."""
    terms = ctx.get("composite_health_terms")
    if not terms:
        return ctx.get("composite_health_basis") or "basis unavailable (organism context degraded)"
    measured_w = sum(t.get("weight", 0) for t in terms.values() if t.get("measured"))
    unmeasured = [f"{k} ({t.get('basis', 'not a measurement')})"
                  for k, t in terms.items() if not t.get("measured")]
    return (f"{round(measured_w * 100)}% measured"
            + (f"; not measured: {'; '.join(unmeasured)}" if unmeasured else ""))


@router.get("/health-summary")
async def health_summary():
    """Compact health check for operational decision-making — carrying the W422 disclosure.

    W438 — composite_health is 20% SIMULATED (ATP on a constant load); biobus computed the
    measured-only companion score and per-term breakdown, but NO HTTP surface passed them through,
    so this route pitched the undisclosed blend "for operational decision-making". It also 500'd
    (KeyError) on biobus's degraded fallback — at exactly the moment the organism was least
    healthy."""
    ctx = biobus.organism_context()
    rec = ctx.get("recommended") or {}
    circ = ctx.get("circadian") or {}
    return {
        "composite_health": ctx["composite_health"],
        "composite_health_measured_only": ctx.get("composite_health_measured_only"),
        "composite_health_terms": ctx.get("composite_health_terms"),
        # W438 refuter catch: this basis was a CONSTANT asserted even when the terms said the
        # self-healing half was defaulted (fresh process) or the whole score was a fallback constant
        "health_basis": _health_basis(ctx),
        "mode": ctx["mode"],
        "should_throttle": rec.get("should_throttle", False),
        "max_parallel_agents": rec.get("max_parallel_agents", 2),
        "circadian_cycle": circ.get("cycle", "UNKNOWN"),
        "is_peak_focus": circ.get("is_peak_focus", False),
        "summary": ctx["health_summary"],
        **({"context_error": ctx["error"]} if ctx.get("error") else {}),
    }


@router.get("/systems")
async def individual_systems():
    """Individual system statuses without aggregation — with the honest scope stated: these are
    in-memory, per-process readings that zero on every restart (and under multi-worker serving
    reflect only the worker that answered)."""
    return {
        "immune": immune.status(),
        "nervous": nervous.status(),
        "self_healing": self_healer.status(),
        "scope": "in-memory, this server process since start",
    }


@router.get("/signals")
async def signal_feed(n: int = 100):
    """Recent nervous system signal feed — the organism's activity log."""
    signals = nervous.recent_signals(max(1, min(n, 200)))
    ns = nervous.status()
    return {
        "arousal_state": ns["arousal_state"],
        "signal_rate_per_second": ns["signal_rate_per_second"],
        "signals": signals,
        "count": len(signals),
    }


@router.get("/lifecycle")
async def lifecycle_status():
    """Concept→commercialise pipeline state across all projects and VSBs."""
    lifecycle = _lifecycle_state()
    vsb = _vsb_state()
    ctx = biobus.organism_context()

    # W438 — the old "farthest_stage" was a fixed append order presented as a pipeline position:
    # it minted a 9th lifecycle vocabulary (folding VSB existence into the project pipeline), so an
    # org whose projects had ALL sat at concept forever reported farthest_stage "vsb_spawn". The
    # project pipeline is now cumulative over its own 3-stage order, VSB state is separate booleans,
    # and the readiness formula ships with the verdict.
    order = ["concept", "prototype", "commercialise"]
    occupied = [s for s in order if lifecycle["by_stage"].get(s, 0) > 0]
    farthest = occupied[-1] if occupied else "none"
    stages_reached = order[: order.index(farthest) + 1] if farthest != "none" else []

    operational = vsb.get("operational", 0)
    readiness = (min(1.0, (lifecycle["commercialisation_rate"] * 0.5) +
                 (operational / max(vsb["total"], 1) * 0.5))
                 if vsb["total"] > 0 else lifecycle["commercialisation_rate"])
    return {
        "lifecycle_stages_reached": stages_reached,
        "farthest_stage": farthest,
        "stages_note": ("project stages are cumulative over concept-prototype-commercialise; NOTE "
                        "the known vocabulary issue (ledger item 2, Owner decision pending): project "
                        "stage advances only when set, and VSB records hold their own status"),
        "vsb_spawned": vsb["total"] > 0,
        "vsb_operational": operational > 0,
        "projects": lifecycle,
        "vsb_entities": vsb,
        "organism_mode": ctx["mode"],
        "commercialisation_readiness": readiness,
        "commercialisation_readiness_basis": (
            f"0.5 x project commercialisation_rate ({lifecycle['commercialisation_rate']}) + "
            f"0.5 x VSB operational share ({operational}/{max(vsb['total'], 1)})"
            if vsb["total"] > 0 else
            f"project commercialisation_rate alone ({lifecycle['commercialisation_rate']}) - no VSBs"),
    }


# ── Homeostasis ───────────────────────────────────────────────────────────────

class HomeostasisRequest(BaseModel):
    reason: str = "scheduled"


@router.post("/homeostasis")
async def trigger_homeostasis(req: HomeostasisRequest):
    """
    Trigger a homeostatic regulation cycle.

    The organism assesses its current state and automatically adjusts:
    - Rate limits (if under stress, reduce RPM)
    - Feature flags (if immune critical, disable non-essential features)
    - AI recommends config changes via CCA submission
    """
    ctx = biobus.organism_context()
    adjustments = []

    # Metabolic adjustment — slow down if ATP depleted (the biobus fallback carries None — W438)
    _atp = ctx.get("metabolic", {}).get("atp_ratio")
    if _atp is not None and _atp < 0.3:
        adjustments.append({
            "system": "gateway",
            "action": "reduce_rpm",
            "reason": f"Low ATP ratio ({ctx['metabolic']['atp_ratio']:.0%})",
        })
        # Auto-submit a CCA for config change
        try:
            from agentic_core.api.change_control import submit_change, SubmitChangeRequest
            await submit_change(SubmitChangeRequest(
                title="Auto-homeostasis: Reduce gateway RPM",
                change_type="config_minor",
                description=f"Reducing gateway RPM due to low ATP ratio ({ctx['metabolic']['atp_ratio']:.0%}). "
                            f"Organism mode: {ctx['mode']}.",
                rationale=f"Homeostatic regulation triggered: {req.reason}",
                affected_systems=["gateway", "ai_providers"],
                submitted_by="biobus.homeostasis",
                rollback_plan="Restore original RPM when ATP ratio recovers above 0.5.",
            ))
        except Exception:
            pass
        # §8 SURVIVAL INSTINCT — don't just throttle: actively REST to restore metabolic energy.
        try:
            from agentic_core.ai.native.homeostasis import homeostasis
            rec = homeostasis.recover(cycles=4)
            if rec.get("recovered"):
                adjustments.append({
                    "system": "metabolic",
                    "action": "rest_recovery",
                    "reason": f"Rest cycles restored ATP {rec['atp_before']:.0%} -> {rec['atp_after']:.0%}",
                })
        except Exception:
            pass

    # Immune recovery — fire recovery signals
    if ctx["immune"]["threat_level"] in ("HIGH", "CRITICAL"):
        adjustments.append({
            "system": "immune",
            "action": "elevated_monitoring",
            "reason": f"Threat level {ctx['immune']['threat_level']}",
        })

    # Circadian regulation — adjust priority
    if not ctx["circadian"]["is_peak_focus"]:
        adjustments.append({
            "system": "scheduler",
            "action": "defer_non_urgent",
            "reason": f"Outside peak focus window ({ctx['circadian']['cycle']})",
        })

    biobus.fire_signal(
        "reflex", "organism.homeostasis",
        f"Homeostasis cycle: {len(adjustments)} adjustments, mode={ctx['mode']}",
        0.7
    )

    # AI recommendation if degraded
    recommendation = None
    if ctx["mode"] in ("DEGRADED", "EMERGENCY"):
        prompt = (
            f"The IDBO organism is in {ctx['mode']} mode.\n"
            f"Immune health: {ctx['immune']['health']:.0%}, "
            f"threat: {ctx['immune']['threat_level']}\n"
            f"Open circuits: {ctx['self_healing']['open_circuits']}\n"
            f"Arousal: {ctx['nervous']['arousal_state']}\n\n"
            f"Recommend 3 immediate homeostatic actions to restore organism health. "
            f"Be specific — name which system, what action, and expected recovery time."
        )
        try:
            recommendation = await gateway.query(prompt, agent="homeostasis")
        except Exception:
            recommendation = "AI recommendation unavailable — check gateway health."

    return {
        "homeostasis_triggered": True,
        "reason": req.reason,
        "organism_mode": ctx["mode"],
        "composite_health": ctx["composite_health"],
        "adjustments_made": adjustments,
        "ai_recommendation": recommendation,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
