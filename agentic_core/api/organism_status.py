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
        return {
            "total_projects": total,
            "by_stage": stage_counts,
            "running": running,
            "commercialisation_rate": completion_rate,
            "pipeline_health": "FLOURISHING" if completion_rate > 0.3 else "GROWING" if total > 0 else "DORMANT",
        }
    except Exception:
        return {"total_projects": 0, "by_stage": {}, "running": 0, "commercialisation_rate": 0.0, "pipeline_health": "UNKNOWN"}


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
        active = sum(1 for v in entities if v.get("status") == "active")
        domains = list({v.get("domain", "") for v in entities if v.get("domain")})
        return {"total": len(entities), "active": active, "domains": domains[:10]}
    except Exception:
        return {"total": 0, "active": 0, "domains": []}


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
                "dominant_trait_basis": ("no genomes stored" if not trait_sums else
                                         f"{len(tied)} trait axes tie at the top - none dominates"
                                         if len(tied) > 1 else f"highest mean of {len(means)} axes")}
    except Exception:
        return {"total_genomes": 0, "mean_fitness": None, "max_generation": 0, "dominant_trait": None}


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

        # ── Composite health ──────────────────────────────────────────────────
        "composite_health": ctx["composite_health"],
        "mode": ctx["mode"],
        "health_summary": ctx["health_summary"],

        # ── Biomimetic systems ────────────────────────────────────────────────
        "systems": {
            "immune": {
                "health": imm["health"],
                "threat_level": imm["threat_level"],
                "errors_in_window": imm["errors_in_window"],
                "active_responses": imm["active_responses"],
                "hot_endpoint": imm.get("hot_endpoint"),
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


@router.get("/health-summary")
async def health_summary():
    """Compact health check for operational decision-making."""
    ctx = biobus.organism_context()
    return {
        "composite_health": ctx["composite_health"],
        "mode": ctx["mode"],
        "should_throttle": ctx["recommended"]["should_throttle"],
        "max_parallel_agents": ctx["recommended"]["max_parallel_agents"],
        "circadian_cycle": ctx["circadian"]["cycle"],
        "is_peak_focus": ctx["circadian"]["is_peak_focus"],
        "summary": ctx["health_summary"],
    }


@router.get("/systems")
async def individual_systems():
    """Individual system statuses without aggregation."""
    return {
        "immune": immune.status(),
        "nervous": nervous.status(),
        "self_healing": self_healer.status(),
    }


@router.get("/signals")
async def signal_feed(n: int = 100):
    """Recent nervous system signal feed — the organism's activity log."""
    signals = nervous.recent_signals(min(n, 200))
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

    # Calculate how far along the org is
    stages_reached = []
    if lifecycle["total_projects"] > 0:
        stages_reached.append("concept")
    if lifecycle["by_stage"].get("prototype", 0) > 0:
        stages_reached.append("prototype")
    if lifecycle["by_stage"].get("commercialise", 0) > 0:
        stages_reached.append("commercialise")
    if vsb["total"] > 0:
        stages_reached.append("vsb_spawn")
    if vsb["active"] > 0:
        stages_reached.append("vsb_active")

    return {
        "lifecycle_stages_reached": stages_reached,
        "farthest_stage": stages_reached[-1] if stages_reached else "none",
        "projects": lifecycle,
        "vsb_entities": vsb,
        "organism_mode": ctx["mode"],
        "commercialisation_readiness": min(
            1.0,
            (lifecycle["commercialisation_rate"] * 0.5) +
            (vsb["active"] / max(vsb["total"], 1) * 0.5)
        ) if vsb["total"] > 0 else lifecycle["commercialisation_rate"],
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

    # Metabolic adjustment — slow down if ATP depleted
    if ctx["metabolic"]["atp_ratio"] < 0.3:
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
