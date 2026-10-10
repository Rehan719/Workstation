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

from typing import Optional

from fastapi import APIRouter, HTTPException
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
            #  W593 — SHAPE-COMPLETE, and `active` is gone: it is the orphan of the vocabulary W438
            #  replaced, read by nothing, while `operational` - which the anatomy page indexes with no
            #  default - was absent. This return means NO ENTITY HAS EVER BEEN ESTABLISHED, which is a
            #  real zero, unlike the exception return below.
            return {"total": 0, "operational": 0, "operating": 0, "legacy_operating": 0,
                    "operational_basis": ("no VSB entity store exists yet, so no entity has been "
                                          "established - this is a true zero, not an unreadable store"),
                    "by_status": {}, "domains": [], "domains_total": 0}
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
        #  W593 (FU-425, M1 R2.3) — THE PREDICATE NAMES THE VOCABULARY THE WRITER USES. This read
        #  `s in ("operational", "active")`, and the comment above records the FIRST round of exactly this
        #  defect (W438: counting "active" when the writer persisted "operational"). W496 then made the
        #  status DERIVED, and `_derived_status` returns "operating" - so the predicate matched nothing the
        #  writer emits and the figure was structurally zero AGAIN, silently lowering the readiness computed
        #  from it. The current term is imported from the writer's own module rather than retyped, so the
        #  next vocabulary change cannot orphan this counter a third time.
        from agentic_core.api.vsb import OPERATING_STATUS as _OPERATING
        _LEGACY_OPERATING = ("operational", "active")   # written by pre-W496 establish paths, still on disk
        _now = sum(n for s, n in by_status.items() if s == _OPERATING)
        _legacy = sum(n for s, n in by_status.items() if s in _LEGACY_OPERATING)
        _not_counted = ", ".join(sorted(s for s in by_status
                                         if s != _OPERATING and s not in _LEGACY_OPERATING))
        domains = sorted({v.get("domain", "") for v in entities if v.get("domain")})
        return {"total": len(entities),
                #  the key keeps its MEANING - how many are operating - and gains a correct value. It is
                #  not renamed, because the page reads it; the computation is what was wrong.
                "operational": _now + _legacy,
                "operating": _now,
                "legacy_operating": _legacy,
                "operational_basis": (
                    f"counts status == {_OPERATING!r}, which is what _derived_status returns today "
                    f"({_now} entit(ies)), plus {_legacy} written by pre-W496 paths that still carry "
                    f"{list(_LEGACY_OPERATING)} on disk. Statuses NOT counted as operating: "
                    #  W593 — the empty case is reachable. `... or "none"` bound to the whole
                    #  concatenation, which is never falsy, so with every status operating the sentence
                    #  ended on its colon and stopped.
                    + (_not_counted or "none")),
                "by_status": by_status,
                "domains": domains[:10], "domains_total": len(domains)}
    except Exception as _e:
        #  W593 — SHAPE-COMPLETE. FU-425 added three keys to the success return and left this fallback
        #  carrying the old shape, so a reader indexing them on an unreadable store got a KeyError. Same
        #  class as FU-415, reproduced two files away in the round that registered it.
        return {"total": 0, "operational": 0, "operating": 0, "legacy_operating": 0,
                "operational_basis": (f"the entity store could not be read "
                                      f"({_e.__class__.__name__}), so NO status was counted - which is "
                                      f"not a count of zero operating entities"),
                "by_status": {}, "domains": [], "domains_total": 0}


def _cca_state() -> dict:
    """Get CCA queue summary."""
    try:
        cca_store = data_path("change_control")
        if not cca_store.exists():
            return {"pending": 0, "approved": 0, "awaiting_board_ratification": 0, "implemented": 0}
        from agentic_core.api.change_control import awaiting_board_ratification
        pending = approved = awaiting = implemented = 0
        for p in cca_store.glob("*.json"):
            try:
                c = json.loads(p.read_text(encoding="utf-8"))
                s = c.get("status", "")
                if s in ("submitted", "under_review"):
                    pending += 1
                elif awaiting_board_ratification(c):
                    awaiting += 1          # W464 (FU-012) — not approved until the Board ratifies it
                elif s == "approved":
                    approved += 1
                elif s == "implemented":
                    implemented += 1
            except Exception:
                pass
        return {"pending": pending, "approved": approved, "awaiting_board_ratification": awaiting,
                "implemented": implemented}
    except Exception:
        return {"pending": 0, "approved": 0, "awaiting_board_ratification": 0, "implemented": 0}


def _genome_state() -> dict:
    """Summarise the genome registry: count, generational depth, the population's dominant trait, and what
    the stored fitness values actually are.

    FU-404 (W584) — this docstring used to call the summary "the organism's genetic health (computed from
    the stored genomes, no fabrication)" and the summary used to carry a `mean_fitness` number. Both were
    wrong together: nothing in this platform evaluates fitness, so every stored value is a model's
    self-declared guess, the unencoded 0.5 default, or a mean inherited from a crossover that evaluated
    nothing — and 11 of the 15 genomes in the live store carried the default. The records keep that
    three-state provenance honestly and this aggregate threw it away. `mean_fitness` is therefore None
    with a basis; `mean_declared_fitness` and `fitness_composition` carry what is true instead.
    """
    import json as _json
    try:
        genome_store = data_path("genomes")
        if not genome_store.exists():
            return {"total_genomes": 0, "encoded_genomes": 0, "mean_fitness": None,
                    "max_generation": 0, "dominant_trait": None, "dominant_trait_tied": [],
                    "dominant_trait_basis": "no genomes stored yet",
                    "mean_fitness_basis": "no genome store exists yet",
                    "mean_declared_fitness": None, "fitness_composition": {},
                    "encoded_basis": "no genome store exists yet"}
        files = list(genome_store.glob("*.json"))
        if not files:
            return {"total_genomes": 0, "encoded_genomes": 0, "mean_fitness": None,
                    "max_generation": 0, "dominant_trait": None, "dominant_trait_tied": [],
                    "dominant_trait_basis": "no genomes stored yet",
                    "mean_fitness_basis": "no genomes stored yet",
                    "mean_declared_fitness": None, "fitness_composition": {},
                    "encoded_basis": "no genomes stored yet"}
        fitnesses: list[float] = []
        declared: list[float] = []
        prov_counts: dict[str, int] = {}
        max_gen = 0
        # §8 (W495, FU-129, S8.2) - the page labelled this count "encoded genomes" while it was simply
        # the number of JSON files in genomes/. Every stored genome has encoded:false, because the
        # deterministic floor cannot declare traits and each record says so ("not encoded - this vector
        # is NOT an analysis of the entity"). A count says what population it covers, so the encoded
        # ones are counted separately and the label can be true either way.
        encoded_n = 0
        trait_sums: dict[str, float] = {}
        trait_counts: dict[str, int] = {}
        for p in files:
            try:
                g = _json.loads(p.read_text())
            except Exception:
                continue
            if g.get("encoded") is True:
                encoded_n += 1
            f = g.get("fitness_score")
            # FU-404 (W584) — the number is kept WITH what it is worth. The records carry a three-state
            # provenance and the mean used to throw it away; a mean over self-declared numbers and
            # filler is not the same figure as a mean over evaluated ones, and nothing here evaluates.
            _prov = str(g.get("fitness_provenance") or "").strip() or "unknown (pre-W438 genome)"
            _kind = ("declared" if _prov.startswith("ai-declared")
                     else "default" if _prov.startswith("default")
                     else "inherited" if _prov.startswith("inherited")
                     else "unknown")
            prov_counts[_kind] = prov_counts.get(_kind, 0) + 1
            if isinstance(f, (int, float)):
                fitnesses.append(float(f))
                if _kind == "declared":
                    declared.append(float(f))
            max_gen = max(max_gen, int(g.get("generation", 0) or 0))
            for axis, val in (g.get("traits") or {}).items():
                if isinstance(val, (int, float)):
                    trait_sums[axis] = trait_sums.get(axis, 0.0) + float(val)
                    trait_counts[axis] = trait_counts.get(axis, 0) + 1
        # FU-404 (W584) — THERE IS NO EVALUATED FITNESS TO AVERAGE, so this reports none. genome.py says
        # it plainly where the number is written ("the fitness is the MODEL'S self-declared number even
        # when parsed; nothing in this system measures it") and OrganismAnatomy.tsx says it to the reader
        # ("no fitness here is ever evaluated"). This function averaged all three provenances into one
        # figure and its docstring called the result the organism's genetic health, computed "no
        # fabrication" — while 11 of the 15 stored genomes carried the 0.5 default. A mean over filler is
        # not a health figure, and a mean that blends filler with a model's own guess is not one either.
        # What IS true is kept rather than deleted: the self-declared mean is reported as its own field,
        # labelled unverified, and the composition is counted so a reader can see what the population is.
        mean_fitness = None
        mean_declared_fitness = round(sum(declared) / len(declared), 3) if declared else None
        fitness_composition = dict(sorted(prov_counts.items()))
        _n_decl, _n_def = prov_counts.get("declared", 0), prov_counts.get("default", 0)
        _n_inh, _n_unk = prov_counts.get("inherited", 0), prov_counts.get("unknown", 0)
        mean_fitness_basis = (
            f"NOT MEASURED: nothing in this platform evaluates fitness, so there is no evaluated value "
            f"to average and no mean is reported. Of {len(files)} stored genome(s): {_n_decl} carry a "
            f"model's self-declared number (unverified), {_n_def} carry the unencoded default (nobody "
            f"declared anything), {_n_inh} inherited a mean from a crossover that evaluated nothing, and "
            f"{_n_unk} predate provenance tracking. mean_declared_fitness is the mean of the "
            f"{_n_decl} SELF-DECLARED value(s) only and is a report of what models claimed, never a "
            f"measurement of genetic health."
            if files else "no genomes stored yet")
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
                "mean_fitness_basis": mean_fitness_basis,
                "mean_declared_fitness": mean_declared_fitness,
                "fitness_composition": fitness_composition,
                "encoded_genomes": encoded_n,
                "encoded_basis": (
                    f"{encoded_n} of {len(files)} stored genome(s) carry encoded:true. An unencoded "
                    f"genome's traits were not declared by any model - the deterministic floor cannot "
                    f"encode, so its vector is not an analysis of the entity."
                    if encoded_n < len(files) else
                    f"all {len(files)} stored genome(s) are encoded"),
                "max_generation": max_gen, "dominant_trait": dominant,
                "dominant_trait_tied": tied if len(tied) > 1 else [],
                "dominant_trait_basis": ("no numeric traits stored" if not trait_sums else
                                         f"{len(tied)} trait axes tie at the top - none dominates"
                                         if len(tied) > 1 else f"highest mean of {len(means)} axes")}
    except Exception:
        # W495 - shape-complete: every return of this function carries the same keys
        return {"total_genomes": 0, "encoded_genomes": 0, "mean_fitness": None, "max_generation": 0,
                "dominant_trait": None, "dominant_trait_tied": [],
                "dominant_trait_basis": "unavailable (read error)",
                "mean_fitness_basis": "unavailable - the genome store could not be read",
                "mean_declared_fitness": None, "fitness_composition": {},
                "encoded_basis": "unavailable - the genome store could not be read"}


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
        # W494 (refutation) — the round taught OrganismDashboard.tsx to render mode_basis and to hang
        # composite_health_basis on the figure's tooltip, and this payload is built as an explicit dict
        # with no **ctx spread, so neither field ever left the process: the paragraph the round added
        # could not render at all. Clause (3) is that the measured share TRAVELS.
        "composite_health_basis": ctx.get("composite_health_basis"),
        "composite_health_measured_weight": ctx.get("composite_health_measured_weight"),
        "mode": ctx["mode"],
        "mode_basis": ctx.get("mode_basis"),
        "mode_decided_on": ctx.get("mode_decided_on"),
        "mode_decidable": ctx.get("mode_decidable"),
        "mode_decidable_basis": ctx.get("mode_decidable_basis"),
        "measured_weight_below_half": ctx.get("measured_weight_below_half"),
        "measured_weight_basis": ctx.get("measured_weight_basis"),
        "health_summary": ctx["health_summary"],
        **({"context_error": ctx["error"]} if ctx.get("error") else {}),

        # ── Biomimetic systems ────────────────────────────────────────────────
        "systems": {
            "immune": {
                "health": imm["health"],
                "threat_level": imm["threat_level"],
                "errors_in_window": imm["errors_in_window"],
                #  W637 (FU-592/599) — the review flags and what the health figure counted travel with it:
                #  this block is a fixed key set, so a field not copied here reaches no page.
                "review_flags_in_window": imm.get("review_flags_in_window"),
                "events_in_window": imm.get("events_in_window"),
                "health_basis": imm.get("health_basis"),
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
            "effective": True,
            "effect": "a config-change request is filed with Change Control (below)",
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
                    "effective": True,
                    "effect": "rest cycles were run against the ATP simulator",
                })
        except Exception:
            pass

    # Immune recovery — fire recovery signals
    if ctx["immune"]["threat_level"] in ("HIGH", "CRITICAL"):
        # §8 (W495, FU-129, S8.6) - "elevated_monitoring" is appended here and read NOWHERE: a
        # repo-wide grep finds only this append site. Nothing monitors anything more closely because of
        # it, so it is an OBSERVATION, not an adjustment, and the response counts the two kinds apart.
        adjustments.append({
            "system": "immune",
            "action": "elevated_monitoring",
            "reason": f"Threat level {ctx['immune']['threat_level']}",
            "effective": False,
            "effect": ("recorded only - nothing in this codebase reads 'elevated_monitoring', so no "
                       "monitoring changed"),
        })

    # Circadian regulation — adjust priority
    if not ctx["circadian"]["is_peak_focus"]:
        # §8 (W495, FU-129, S8.6) - same: nothing reads "defer_non_urgent", so nothing is deferred.
        adjustments.append({
            "system": "scheduler",
            "action": "defer_non_urgent",
            "reason": f"Outside peak focus window ({ctx['circadian']['cycle']})",
            "effective": False,
            "effect": ("recorded only - nothing in this codebase reads 'defer_non_urgent', so no work "
                       "was deferred or re-prioritised"),
        })

    biobus.fire_signal(
        "reflex", "organism.homeostasis",
        f"Homeostasis cycle: {len(adjustments)} adjustments, mode={ctx['mode']}",
        0.7
    )

    # AI recommendation if degraded
    recommendation = None
    # W495 - initialised here, not reached out of locals(): the response declares them unconditionally
    recommendation_served_by = None
    recommendation_is_external = False
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
            # W495 (FU-129, S8.6) - this used gateway.query, which discards served_by, so the text was
            # printed into the result box with nothing saying whether a model wrote it or the
            # deterministic floor composed it. query_meta carries the provenance the page needs.
            _meta = await gateway.query_meta(prompt, agent="homeostasis", augment=False, user_text=(req.reason or None))
            recommendation = _meta.get("output") if isinstance(_meta, dict) else str(_meta)
            recommendation_served_by = (_meta or {}).get("served_by") if isinstance(_meta, dict) else None
            recommendation_is_external = bool((_meta or {}).get("is_external")) if isinstance(_meta, dict) else False
        except Exception:
            recommendation = "AI recommendation unavailable — check gateway health."

    return {
        "homeostasis_triggered": True,
        "reason": req.reason,
        "organism_mode": ctx["mode"],
        "composite_health": ctx["composite_health"],
        # W495 (FU-129, S8.6) - the page read len(adjustments_made) and printed "N adjustment(s)
        # made". Two of the four actions are recorded and read by nothing, so the counts are separate
        # and the label can be true.
        "adjustments_made": adjustments,
        "adjustments_effective": [a for a in adjustments if a.get("effective")],
        "adjustments_effective_count": sum(1 for a in adjustments if a.get("effective")),
        "observations_only_count": sum(1 for a in adjustments if a.get("effective") is False),
        "adjustments_basis": (
            f"{sum(1 for a in adjustments if a.get('effective'))} of {len(adjustments)} entr(y/ies) "
            f"changed something; the rest are observations this codebase records and does not act on"),
        "ai_recommendation": recommendation,
        "ai_recommendation_served_by": recommendation_served_by,
        "ai_recommendation_is_external": recommendation_is_external,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
@router.get("/selection/{vsb_id}")
async def organism_selection(vsb_id: str):
    """Can selection act on this entity? It REFUSES while any of §8's four measures is unmeasured.

    P3.27 clause (3). The answer is deliberately not a score: it is ASSESSABLE or NOT_ASSESSABLE, and a
    refusal NAMES the measures that are missing. One of the four — founder-alignment — has no mechanism
    anywhere in this platform, so selection refuses today for a reason a reader can check, and will keep
    refusing until a founder actually says something rather than having a proxy stand in for them.
    """
    from agentic_core.organism import selection as _sel
    r = _sel.assess(vsb_id)
    return {
        **r,
        "measures_required": list(_sel.MEASURES),
        "method": ("each measure is read from its own source and carries its own `measured` flag; nothing "
                   "is defaulted, a recorded zero is a measurement and an absence is not. No verdict, "
                   "score or ranking is produced here"),
    }


@router.get("/selection/{vsb_id}/floor")
async def organism_selection_floor(vsb_id: str):
    """Is this entity under a hard floor? A flag is a REVIEW, never a retirement.

    P3.27 clause (4). A floor creates no optimisation pressure toward a proxy because it reads no number
    to improve: there is a line and an entity is either under it or not. A floor that cannot be assessed
    says so and never counts as passed, so the result carries its own COVERAGE — this platform records no
    per-entity obligations, so the §8-obligations floor is reported unassessable rather than cleared.
    """
    from agentic_core.organism import selection as _sel
    r = _sel.negative_selection(vsb_id)
    return {
        **r,
        "method": ("each floor is a LINE, not a score, and nothing is ranked against it. A breach FLAGS "
                   "the entity for review; nothing here removes anything and a removal is governed "
                   "through Change Control"),
    }
@router.get("/cadence")
async def organism_cadence(scope: str = "workstation"):
    """The §17.3 cadence: when each layer last refreshed, whether it is due, and the whole history.

    P3.3 clause (2). Every entry carries its trigger, its reason, its provenance and the content it
    DISPLACED — a refresh that overwrote the plan without a history entry would fail the clause, and an
    entry that recorded only the new text would still lose the old one.
    """
    from agentic_core.config import StoreUnavailable
    from agentic_core.organism import cadence as _cad
    try:
        st = _cad.state(scope)
        hist = _cad.history(scope)
    except StoreUnavailable as e:
        raise HTTPException(status_code=503, detail=(
            f"{e} - the plan was NOT read and no cadence state is reported. A refresh is never written "
            f"over a plan that could not be read whole."))
    #  W589 — WHAT THE LAST BEAT ACTUALLY MANAGED, which the state above cannot say. The beat used to
    #  swallow a cadence failure with `except Exception: pass`, so a cadence that had STOPPED FIRING looked
    #  exactly like a cadence with nothing due. It now records the reason - and a record nothing surfaces is
    #  only readable by a test, so it is reported here. The two answer different questions: `layers` is read
    #  from the plan and says whether a layer is due NOW; `last_beat` says what the most recent heartbeat
    #  did, including a failure that wrote nothing. Due in the first and failing in the second is the silent
    #  state this exists to end.
    from agentic_core.organism.heartbeat import heartbeat as _hb
    _lastc = getattr(_hb, "last_cadence", None)
    #  W593 (FU-430) — THE RECORD NAMES ITS OWN BEAT, and the reader can see whether that is the latest.
    #  This block used to assert "what the most recent heartbeat managed" as a property of the data, with
    #  nothing a reader could check it against — and between W589 and W593 it was FALSE on every beat where
    #  nothing was due, because the producer only wrote the record when something happened. The producer is
    #  fixed; this makes the claim verifiable rather than trusting it.
    _rec_beat = (_lastc or {}).get("beat")
    _now_beat = getattr(_hb, "beats", None)
    _is_latest = (_rec_beat is not None and _now_beat is not None and _rec_beat == _now_beat)
    _last_beat = {
        "ran": bool(_lastc),
        "beat": _rec_beat,
        "heartbeat_beats": _now_beat,
        "is_the_latest_beat": _is_latest if _lastc else None,
        "nothing_was_due": (_lastc or {}).get("nothing_was_due"),
        "refreshed": (_lastc or {}).get("refreshed") or [],
        #  W593 (FU-431) — WHICH ENTITIES THE BEAT VISITED. `refreshed` names layers; before this the
        #  §17.3 cadence only ever ran for "workstation" while the surface spoke of the layers generally,
        #  so a reader had no way to tell the apex-only beat from one that reaches the roster.
        "scopes": (_lastc or {}).get("scopes") or [],
        "scope_basis": (_lastc or {}).get("scope_basis"),
        "could_not_run": (_lastc or {}).get("could_not_run"),
        "at": (_lastc or {}).get("at"),
        "beat_basis": ("`beat` is the beat this record was written on and `heartbeat_beats` is the count "
                       "now; when they differ the record is NOT the latest beat and this says so rather "
                       "than calling it the most recent. Between W589 and W593 the record was only written "
                       "when a layer refreshed or failed, so on a quiet beat it was an earlier beat's "
                       "record presented as the current one (MILESTONE M1, R3.4)"),
        "basis": ((_lastc or {}).get("basis") or
                  ("NO BEAT HAS RUN A CADENCE STEP IN THIS PROCESS YET, so this is not a report that the "
                   "cadence is healthy and not a report that it failed - nothing has been attempted. The "
                   "layer states above are read from the plan and are unaffected by that")),
    }
    return {
        **st,
        "history": hist,
        "history_count": len(hist),
        "last_beat": _last_beat,
        "method": ("each layer is due on elapsed time (quarterly for strategic, weekly for the action "
                   "plan) or on its own signal (a market signal, a KPI trigger), whichever comes first. "
                   "The due check is a pure function of the last refresh, the time and the signals, so a "
                   "trigger can be FORCED rather than waited for. A layer never refreshed says so rather "
                   "than reporting an age of zero"),
        "last_beat_basis": ("`layers` is the plan's own record of when each layer last refreshed; "
                            "`last_beat` is what the most recent heartbeat managed. A layer that is DUE "
                            "while last_beat.could_not_run is set means the cadence is not firing, which "
                            "an absent action alone could never distinguish from nothing being due"),
    }


@router.post("/cadence/refresh")
async def organism_cadence_refresh(layer: str, scope: str = "workstation",
                                   signal: Optional[str] = None, force: bool = False):
    """Refresh one §17.3 layer now. A SIGNAL fires it regardless of the clock; `force` is recorded as such.

    Nothing here invents a market signal or a KPI breach: both are supplied by whoever observed one. A
    refresh that is neither due nor forced writes NOTHING and says why, so a caller polling this route
    cannot accidentally rewrite the plan on every call.
    """
    from agentic_core.config import StoreUnavailable
    from agentic_core.organism import cadence as _cad
    if layer not in _cad.LAYERS:
        raise HTTPException(status_code=422, detail=(
            f"unknown cadence layer {layer!r}; §17.3 has {list(_cad.LAYERS)}"))
    try:
        return _cad.refresh(scope, layer, signal=signal, force=force)
    except StoreUnavailable as e:
        raise HTTPException(status_code=503, detail=(
            f"{e} - the plan was NOT read and nothing was written. A tolerant read here would hand this "
            f"route a fresh empty plan and the write would replace the real one."))
