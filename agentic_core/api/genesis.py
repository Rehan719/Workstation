"""
Genesis API — the unified Sovereign Journey orchestrator.

Materialises the Workstation IDBO vision as ONE progressive, intelligently-
autonomous workflow. It takes a user's raw problem and drives it through all
three phases — Conceptualisation → Design & Development → Enterprise
Commercialisation — composing the six-engine cognitive cascade, the MJM meta-
assessment, the design and business engines, and the v16-Omega constitutional
gate into a single end-to-end journey whose deliverable is the user's *own* VSB
(Virtual Sovereign Business) blueprint.

  GET  /api/v1/genesis/status    — orchestrator status + the engines it composes
  POST /api/v1/genesis/journey   — run the full Concept → Commercialisation cascade
"""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.auth.core import get_current_user, request_owner_id
from agentic_core.api.intelligence import _ai_cognitive_prime, _ai_mjm_lifecycle
from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
from agentic_core.vbs.quality import assure_delivery

router = APIRouter(prefix="/api/v1/genesis", tags=["genesis-journey"])


def _score_candidate(text: str, sections: List[str]) -> Dict[str, float]:
    """§4.5 — score a candidate solution on REAL MEASURED proxies (honest, never fabricated): section
    coverage, specificity (detail density), and structure. Returns 0–1 sub-scores + a weighted composite."""
    t = text or ""
    low = t.lower()
    coverage = round(sum(1 for s in sections if s.lower() in low) / max(1, len(sections)), 3)
    specificity = round(min(1.0, len(t.strip()) / 2800.0), 3)              # detail density (range to discriminate)
    structure = round(min(1.0, t.count("##") / max(1, len(sections))), 3)  # uses the requested structure
    score = round(0.30 * coverage + 0.50 * specificity + 0.20 * structure, 3)
    return {"coverage": coverage, "specificity": specificity, "structure": structure, "score": score}


# §4.5 (W419) — the five criteria the spec names for candidate selection, and their honest status.
# TWO are measurable today from one deterministic call (screen_compliance: regex rules + engines,
# ~0.15 ms warm, zero model calls). THREE are not measurable at selection time and are DECLARED
# rather than proxied — inventing a proxy for them is the exact failure §4.5 already committed.
_CAND_MEASURED = {
    "compliance": "screen_compliance frameworks sharia_halal · uk_legal · regulatory",
    "safety": "screen_compliance frameworks ehs · ethical · sharia_halal",
}
_CAND_UNMEASURED = {
    "effectiveness": "needs outcome data that does not exist at selection time",
    "efficiency": "no in-house instrument",
    "commercial viability": "no in-house instrument",
}
_VERDICT_SCORE = {"pass": 1.0, "review": 0.5, "fail": 0.0}
# Reused verbatim from agentic_core.vbs.quality._measure_bar so §10 and §4.5 cannot drift apart.
_SAFETY_FRAMEWORKS = ("ethical", "ehs", "sharia_halal")


def _screen_candidate(text: str) -> Dict[str, Any]:
    """§4.5 + §11 — run the deterministic compliance screen over ONE candidate and reduce it to the
    two criteria the spec names that are genuinely measurable here. Never raises: a screen fault
    leaves both criteria unmeasured and says so, rather than silently scoring the candidate 0 (which
    would disqualify a good candidate for an infrastructure hiccup)."""
    try:
        from agentic_core.api.compliance import screen_compliance
        s = screen_compliance(text or "")
    except Exception as exc:  # noqa: BLE001 — a screen fault must not decide a ranking
        return {"screen_error": str(exc), "compliance": None, "safety": None, "disqualified": False,
                "verdicts": {}}
    verdicts = {v.get("framework"): v.get("status") for v in (s.get("verdicts") or [])}
    comp = [_VERDICT_SCORE.get(v, 0.5) for f, v in verdicts.items() if f not in _SAFETY_FRAMEWORKS]
    safe = [_VERDICT_SCORE.get(verdicts[f], 0.5) for f in _SAFETY_FRAMEWORKS if f in verdicts]
    return {
        "verdicts": verdicts,
        "overall": s.get("overall"),
        "compliance": round(sum(comp) / len(comp), 3) if comp else None,
        "safety": round(sum(safe) / len(safe), 3) if safe else None,
        # VETO: a candidate the §11 screen fails cannot be selected, whatever its prose scores.
        "disqualified": s.get("overall") == "fail",
    }


def _verify_stage(text: str, sections: List[str]) -> Dict[str, Any]:
    """§5 — verify/validate a single journey stage on REAL MEASURED proxies (section coverage · specificity ·
    structure). Honest: a measured quality check, never fabricated. `verified` = composite score ≥ 0.5 AND at
    least two-thirds of the stage's expected sections present."""
    m = _score_candidate(text or "", sections)
    present = sum(1 for s in sections if s.lower() in (text or "").lower())
    m["sections_present"] = f"{present}/{len(sections)}"
    m["verified"] = bool(m["score"] >= 0.5 and present * 3 >= len(sections) * 2)
    return m

# Shares the same UEG audit log as the constitutional engine, so journeys are
# recorded in the one tamper-evident governance trail.
_UEG = UEGLogger()
_GOV = UnifiedConstitutionalInterceptorV16Omega("genesis-node", _UEG)


class JourneyRequest(BaseModel):
    problem: str
    domain: str = "enterprise"
    realm: str = "enterprise"   # canonical: agentic_core.taxonomy.REALMS (§17.1, W311)
    establish: bool = False     # §4→§5 — culminate the journey by ESTABLISHING the living VSB IDBO enterprise
    name: str = ""              # optional name for the established VSB
    entity_type: str = "waqf_ltd_hybrid"   # legal/economic form when establishing
    # §4 (W302) — the one continuous workflow ships the newborn's WHOLE living body at birth
    ship_output: bool = True


async def _q(prompt: str, agent: str) -> str:
    """Gateway query with graceful degradation (never raises)."""
    try:
        return await gateway.query(prompt, agent=agent, augment=False)   # W332 — journey copy persists/ships
    except Exception as e:
        return f"[{agent} unavailable: {e}]"


@router.get("/status")
async def genesis_status():
    return {
        "orchestrator": "Sovereign Journey (Genesis)",
        "phases": ["Conceptualisation", "Design & Development", "Enterprise Commercialisation"],
        "composes": [
            "CognitiveCascade(6: Inkashaf/Samajh/Soch/Aqal/Hoshiyari/Iman)",
            "MJM (Mushahida/Jaiza/Muaina)",
            "DDPIE (design)", "BDP (commercialisation)",
            "gaas.v5 constitutional gate", "VSB blueprint",
        ],
        "deliverable": "The user's own VSB IDBO — Concept → Commercialisation",
        "governance": _GOV.circuit_breaker.state(),
    }


@router.post("/journey")
async def genesis_journey(req: JourneyRequest, user: dict | None = Depends(get_current_user)):
    """Run the full intelligently-autonomous Concept → Commercialisation cascade."""

    # In-house-first AI with provenance: the synthesis stages record which OWNED resource
    # served them (this local _q shadows the module helper for the journey's stages).
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    async def _q(prompt: str, agent: str) -> str:  # noqa: F811 — local, provenance-aware
        try:
            # W332 — journey stages persist into the entity/plan and can ship: no cross-request recall
            res = await gateway.query_meta(prompt, agent=agent, augment=False)
            sb = res.get("served_by", "native")
            provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
            provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
            return res.get("output", "")
        except Exception as e:
            return f"[{agent} unavailable: {e}]"

    # ── Phase 1 — Conceptualisation (understand → analyse → optimal concept) ──
    try:
        cognitive = await _ai_cognitive_prime(req.problem, req.domain)
    except Exception as e:
        cognitive = f"[cognitive unavailable: {e}]"
    try:
        mjm = await _ai_mjm_lifecycle(req.problem, req.domain, cognitive)
    except Exception as e:
        mjm = f"[mjm unavailable: {e}]"
    concept = await _q(
        "You are the IDBO Conceptualisation engine. Using the analysis below, define the optimal "
        "solution concept that clears or mitigates the problem.\n\n"
        f"Problem: {req.problem}\nDomain: {req.domain}\n"
        f"Cognitive cascade: {cognitive[:800]}\nMJM assessment: {mjm[:500]}\n\n"
        "## Problem Understanding\n## Optimal Solution Concept\n## Why This Concept Wins",
        "genesis_concept",
    )

    # ── Stage 3 — Innovate & Research (§4.3): discover the best, latest and most effective approaches and
    #    innovative options across science · technology · business · operations · law · the domain. ──
    research = await _q(
        "You are the IDBO Innovate & Research engine. For the concept below, discover the BEST, LATEST and "
        "most effective approaches and innovative options — drawing across science, technology, business, "
        "operations, law/compliance, and the domain.\n\n"
        f"Concept: {concept[:700]}\nDomain: {req.domain}\n\n"
        "## Best & Latest Approaches (science · technology · business · operations · law)\n"
        "## Innovative Options\n## Recommended Direction",
        "genesis_research",
    )

    # ── Stage 5 — Model · Simulate · Optimise · Rank (§4.5): generate DISTINCT candidate solution
    #    approaches (informed by the research), MODEL each, score on OWNED evidence criteria (real measured
    #    proxies — coverage · specificity · structure; never fabricated), and select the BEST to carry forward. ──
    _cand_sections = ["Approach", "Key Steps", "Effectiveness", "Risks & Mitigations"]
    _cand_specs = [
        ("pragmatic",  "the fastest, lowest-risk, most pragmatic approach"),
        ("innovative", "the most innovative, best-in-class, highest-impact approach"),
        ("lean",       "the leanest, most cost-effective, resource-minimal approach"),
    ]
    candidates: List[Dict[str, Any]] = []
    for cid, framing in _cand_specs:
        ctext = await _q(
            f"You are the IDBO Solution Architect. Propose {framing} to realise this concept — be specific "
            f"and concrete, drawing on the research.\n\nConcept: {concept[:600]}\nResearch: {research[:600]}\n"
            f"Domain: {req.domain}\n\n"
            "## Approach\n## Key Steps\n## Effectiveness\n## Risks & Mitigations", f"genesis_candidate_{cid}")
        candidates.append({"id": cid, "framing": framing, "approach": ctext, **_score_candidate(ctext, _cand_sections)})

    # §4.5 (W305) — "modelled, SIMULATED": each candidate is forward-simulated through the owned
    # MODEL-FREE digital-twin pattern (system = the concept; scenario = the candidate's approach),
    # and a simulation-derived score joins the ranking with DECLARED weights (60% modelled-text
    # evidence · 40% simulated evidence) — text proxies no longer carry selection alone. Honest:
    # the sim score measures the simulation narrative's substance on the same real proxies
    # (coverage of the canonical twin sections) — never fabricated telemetry.
    _twin_sections = ["State Trajectory", "Emergent Behaviour", "Stress / Failure Points",
                      "Recommended Setpoints"]
    for c in candidates:
        sim = await _q(
            f"You are a digital-twin simulator. System under twin: {concept[:300]} (domain {req.domain}). "
            f"Forward-simulate this candidate approach as the operating scenario: {c['approach'][:500]}\n"
            "## State Trajectory (t0→tN)\n## Emergent Behaviour\n## Stress / Failure Points\n"
            "## Recommended Setpoints", f"genesis_twin_{c['id']}")
        _sim_m = _score_candidate(sim, _twin_sections)
        c["simulation"] = sim[:1200]
        c["simulation_score"] = _sim_m["score"]
        c["modelled_score"] = c["score"]
        # FORM score — coverage · specificity · structure, over both the candidate and its twin.
        # Renamed from "score" deliberately: it measures how the text is SHAPED, not whether the
        # solution is good, and calling it "score" is what let it stand in for evidence for so long.
        c["form_score"] = round(0.6 * c["modelled_score"] + 0.4 * _sim_m["score"], 3)
        # §4.5 (W419) — REAL criteria enter the ranking here. Until now the composite was form only,
        # and form SATURATES: specificity = min(1, len/2800), so any candidate past ~2800 characters
        # carrying the prompt's own headings scores exactly 1.000. All candidates then tied and the
        # stable sort handed the win to whichever _cand_specs named first — always "pragmatic".
        c.update({"screen": _screen_candidate(c["approach"])})

    _screened = [c for c in candidates if c["screen"].get("compliance") is not None]
    for c in candidates:
        s = c["screen"]
        if s.get("compliance") is None:          # screen unavailable — rank on form, and SAY so
            c["score"] = c["form_score"]
            c["score_basis"] = "form only — the §11 screen did not run for this candidate"
        else:
            c["score"] = round(0.40 * c["form_score"] + 0.35 * s["compliance"] + 0.25 * s["safety"], 3)
            c["score_basis"] = (f"0.40 form {c['form_score']} · 0.35 compliance {s['compliance']} "
                                f"· 0.25 safety {s['safety']}")

    # VETO before ranking: a candidate the §11 screen FAILS cannot win, whatever its prose scores.
    candidates.sort(key=lambda c: (not c["screen"].get("disqualified", False), c["score"]), reverse=True)
    for i, c in enumerate(candidates, 1):
        c["rank"] = i
    _eligible = [c for c in candidates if not c["screen"].get("disqualified", False)]
    _vetoed = [c["id"] for c in candidates if c["screen"].get("disqualified", False)]
    winner = (_eligible or candidates)[0]

    # Ties are DETECTED and DISCLOSED. Previously an exact tie was resolved silently by list
    # position and the payload reported the winner as "selected on evidence" regardless.
    _top = [c["id"] for c in _eligible if c["score"] == winner["score"]]
    _tied = len(_top) > 1

    stage_5 = {
        "method": "candidates modelled + FORWARD-SIMULATED through the owned digital-twin pattern, "
                  "then screened by the deterministic §11 compliance/safety screen. Declared "
                  "weights: 0.40 FORM (coverage · specificity · structure, over candidate + twin) "
                  "· 0.35 compliance · 0.25 safety. A candidate the screen FAILS is vetoed and "
                  "cannot be selected. Real measured proxies, never fabricated.",
        "candidates": candidates,
        "selected": winner["id"],
        "vetoed": _vetoed,
        "tie": {"detected": _tied, "tied_candidates": _top,
                "resolved_by": "list order — NOT evidence" if _tied else None},
        "criteria_measured": _CAND_MEASURED,
        "criteria_not_measured": _CAND_UNMEASURED,
        "honesty": ("Two of the five criteria §4.5 names are measured here (compliance, safety); "
                    "three are NOT measured at selection time and are named in "
                    "criteria_not_measured. FORM is a shape proxy, not solution quality — it "
                    "saturates at 1.000 for any candidate past ~2800 characters."),
        "selection_basis": (
            (f"TIE at {winner['score']} across {len(_top)} candidates ({', '.join(_top)}) — resolved "
             f"by list order, NOT by evidence. ") if _tied else "") + (
            f"selected {winner['id']} on {winner['score_basis']}"
            + (f"; vetoed for §11 failure: {', '.join(_vetoed)}" if _vetoed else "")),
    }

    # ── Phase 2 — Design & Development (the SELECTED best candidate → buildable solution) ──
    design = await _q(
        "You are the IDBO Design & Development engine. Turn the SELECTED best approach into a buildable design.\n\n"
        f"Concept: {concept[:600]}\nSelected approach ({winner['id']} — {winner['framing']}): {winner['approach'][:700]}\n"
        f"Domain: {req.domain}\n\n"
        "## Solution Architecture\n## Core Components\n## Technology & Delivery Plan\n## MVP Scope",
        "genesis_design",
    )

    # ── Stage 7 — Enhance via Operational Intelligence (§4.7): make the designed solution not just
    #    innovative but DELIVERABLE, COMPLIANT and OPERABLE — operations delivery + compliance
    #    (legal · regulatory · EHS · Sharia/halal · ethical) + operational excellence. ──
    operations = await _q(
        "You are the IDBO Operational Intelligence engine. Make the designed solution not just innovative but "
        "DELIVERABLE, COMPLIANT and OPERABLE.\n\n"
        f"Design: {design[:800]}\nDomain: {req.domain}\n\n"
        "## Operations Delivery (how it runs day-to-day)\n"
        "## Compliance (legal · regulatory · EHS · Sharia/halal · ethical)\n"
        "## Operational Excellence (quality · efficiency · continual improvement)",
        "genesis_operations",
    )

    # ── Phase 3 — Enterprise Commercialisation (+ the user's VSB blueprint) ──
    commercial = await _q(
        "You are the IDBO Commercialisation engine. Define how to take this to market and the living "
        "VSB (Virtual Sovereign Business) — a specialised IDBO — that will run it.\n\n"
        f"Concept: {concept[:500]}\nDesign: {design[:500]}\nOperational intelligence: {operations[:500]}\n"
        f"Domain: {req.domain}\n\n"
        "## Go-To-Market Strategy\n## Revenue Model\n"
        "## VSB Blueprint (AI CEO + C-Suite → CoE → BTO; living BMS/QMS/DCS/EMS)\n## First 90 Days",
        "genesis_commercial",
    )

    # ── Constitutional governance attestation (logged to the UEG) ──
    async def _attest() -> str:
        return "Sovereign Journey synthesised under v16-Omega constitutional supervision."
    gov = await _GOV.intercept({"intent": "genesis_journey", "domain": req.domain}, _attest)

    # ── §5 — verify/validate EACH stage (real measured proxies: coverage · specificity · structure), so the
    #    whole cascade is verified, tested and validated stage-by-stage, not only at the final QMS gate. ──
    stage_verifications = {
        "concept": _verify_stage(concept, ["Problem Understanding", "Optimal Solution Concept", "Why This Concept Wins"]),
        "research": _verify_stage(research, ["Best & Latest Approaches", "Innovative Options", "Recommended Direction"]),
        "design": _verify_stage(design, ["Solution Architecture", "Core Components", "Technology & Delivery Plan", "MVP Scope"]),
        "operations": _verify_stage(operations, ["Operations Delivery", "Compliance", "Operational Excellence"]),
        "commercialisation": _verify_stage(commercial, ["Go-To-Market Strategy", "Revenue Model", "VSB Blueprint", "First 90 Days"]),
    }
    stages_verified = sum(1 for v in stage_verifications.values() if v["verified"])

    # ── Continual operational delivery within the LIVING QMS: the journey's buildable + go-to-market
    # delivery is gated by the OWNED QMS, held to the §10 Solution-Quality Bar, recorded within the §8
    # biomimetic organism — the same capability the cascade + deliverables deliver through.
    # §10 (W307) — the journey attests ONLY the bar criteria its own real process earned this run
    # (each basis names the actual step); the gate records them per-criterion, never as a bare list.
    # §10 (W419) — every attestation below is DERIVED from this run and names its real output.
    # Two of these were previously constant sentences ("stage 5 forward-simulated each candidate
    # through the owned digital-twin pattern" / "best-of-candidates selection on combined
    # modelled+simulated evidence") that would have been written identically had the twin returned a
    # single empty line. An attestation that cannot be false is not evidence. The gate now records
    # these as ATTESTED rather than measured, and they must at minimum be true of THIS run.
    _sim_lengths = [len(c.get("simulation") or "") for c in candidates]
    _simulated_ok = [n for n in _sim_lengths if n >= 200]
    _bar_evidence = {
        "modelled": (f"stage 5 modelled {len(candidates)} candidates; form scores "
                     + " · ".join(f"{c['id']}={c['modelled_score']}" for c in candidates)),
        "ranked": stage_5["selection_basis"],
        "categorised": f"realm '{req.realm}' × domain '{req.domain}' categorisation",
    }
    # Attest "simulated" ONLY if the twin actually produced substantive output for every candidate.
    if len(_simulated_ok) == len(candidates) and candidates:
        _bar_evidence["simulated"] = (
            f"digital-twin forward-simulation returned {min(_sim_lengths)}-{max(_sim_lengths)} chars "
            f"per candidate; twin scores "
            + " · ".join(f"{c['id']}={c['simulation_score']}" for c in candidates))
    # Attest "optimised" ONLY when the selection actually discriminated — a tie means it did not.
    if not stage_5["tie"]["detected"] and len(candidates) > 1:
        _bar_evidence["optimised"] = (
            f"selected {winner['id']} at {winner['score']} over "
            + " · ".join(f"{c['id']}={c['score']}" for c in candidates if c["id"] != winner["id"])
            + f" ({winner['score_basis']})")
    if stages_verified == len(stage_verifications):
        _bar_evidence["tested"] = (f"all {stages_verified}/{len(stage_verifications)} stages verified: "
                                   + " · ".join(f"{k}={v['sections_present']}"
                                                for k, v in stage_verifications.items()))
        _bar_evidence["validated"] = ("every stage validated against its declared section structure: "
                                      + " · ".join(f"{k}={v['score']}"
                                                   for k, v in stage_verifications.items()))
    quality_assurance = await assure_delivery(
        f"{design}\n{commercial}",
        ["Solution Architecture", "Core Components", "Technology & Delivery Plan", "MVP Scope",
         "Go-To-Market Strategy", "Revenue Model", "VSB Blueprint", "First 90 Days"],
        label="genesis", evidence=_bar_evidence)

    # ── §4→§5 SEAM — optionally culminate the journey by ESTABLISHING the living VSB IDBO enterprise, so a
    #    plainly-described challenge flows in ONE continuous workflow all the way to a living enterprise that
    #    then operates/improves/evolves autonomously (led by the Chief). Additive + best-effort.
    established_vsb = None
    if req.establish:
        try:
            established_vsb = await genesis_establish(EstablishRequest(
                problem=req.problem, domain=req.domain, realm=req.realm, name=req.name,
                concept=concept, design=design, commercialisation=commercial,
                entity_type=req.entity_type, ship_output=req.ship_output,
                research=research, operations=operations,
                selected_candidate=(stage_5 or {}).get("candidates", [{}])[0]
                    if (stage_5 or {}).get("candidates") else {},
                stage_verifications=stage_verifications),
                user=user if isinstance(user, dict) else None)   # W302+W304 - the whole journey flows
        except Exception as e:
            established_vsb = {"error": f"establishment deferred: {e}"}

    return {
        "problem": req.problem,
        "domain": req.domain,
        "realm": req.realm,
        "phase_1_conceptualisation": {"cognitive_cascade": cognitive, "mjm_assessment": mjm, "concept": concept},
        "stage_3_innovate_research": research,     # §4.3 — best/latest approaches across science·tech·business·ops·law
        "stage_5_model_simulate_rank": stage_5,   # §4.5 — candidate solutions modelled + evidence-ranked → best selected
        "phase_2_design_development": design,
        "stage_7_operational_intelligence": operations,   # §4.7 — deliverable · compliant · operable
        "phase_3_commercialisation": commercial,
        "governance": {"status": gov.status, "checkpoint": gov.checkpoint_id, "node": gov.node},
        "stage_verifications": stage_verifications,       # §5 — each stage verified/tested/validated (measured)
        "stages_verified": f"{stages_verified}/{len(stage_verifications)}",
        "quality_assurance": quality_assurance,
        "ai_provenance": provenance,
        "engines_used": [
            "Inkashaf", "Samajh", "Soch", "Aqal", "Hoshiyari", "Iman",
            "MJM", "DDPIE", "BDP", "gaas.v5",
        ],
        "established_vsb": established_vsb,   # §4→§5 — the living VSB enterprise, when establish=True
        "deliverable": "The user's own VSB IDBO — Concept → Commercialisation"
                       + (" → established living enterprise" if established_vsb and not (isinstance(established_vsb, dict) and established_vsb.get("error")) else ""),
        "status": "complete",
    }


class EstablishRequest(BaseModel):
    problem: str
    domain: str = "enterprise"
    realm: str = "enterprise"
    name: str = ""
    concept: str = ""
    design: str = ""
    commercialisation: str = ""
    owner_id: str = "default"
    entity_type: str = "waqf_ltd_hybrid"   # legal/economic form: sole|ltd|plc|trust|waqf|multinational|nonprofit|charity|waqf_ltd_hybrid
    ship_output: bool = True   # §4 (W302) — auto-ship the §13 living body at birth
    # §4 (W304) — the FULL journey record survives establishment (defaults empty for the
    # standalone /establish path; honest stubs render when absent — never invented content).
    research: str = ""
    operations: str = ""
    selected_candidate: dict = {}
    stage_verifications: dict = {}


def _attach_delivery_swarm(entity: dict, vsb_id: str, name: str, problem: str,
                           domain: str, concept: str = "") -> None:
    """Give the VSB its OWN bespoke, reconfigurable native swarm cascade — its in-house delivery org
    (Chief → AI CEO → C-Suite → CoE → BTO) as a runnable, owned Resource-Fabric resource. Shared by
    the blocking /establish and the SSE /establish/stream. Best-effort (never blocks establishment)."""
    try:
        from agentic_core.api import resource_fabric as rf
        org_tiers = ["Chief (owner twin)", "AI CEO", "C-Suite", "Centre of Excellence", "Build-to-Order"]
        cascade = rf.register_swarm(
            name=f"{name} — delivery swarm",
            context=(f"VSB: {name}\nMission: {problem}\nDomain: {domain}\n"
                     f"Concept: {(concept or problem)[:600]}"),
            usage_area="delivery", vsb_id=vsb_id, org=org_tiers,
            owner_id=entity.get("owner_id"),   # §14 (W324) — the cascade belongs to the entity's owner
            stages=[
                {"role": "ai-ceo", "instruction": "Frame the objective and set the directive for the C-Suite."},
                {"role": "c-suite", "instruction": "Break the directive into specialist workstreams (finance, technical, market, legal/compliance)."},
                {"role": "centre-of-excellence", "instruction": "Produce the specialist deliverable for the highest-priority workstream."},
                {"role": "build-to-order", "instruction": "Integrate the workstreams into a Build-to-Order delivery plan."},
            ],
        )
        entity["native_swarm"] = {
            "cascade_id": cascade["id"], "name": cascade["name"], "org": org_tiers,
            "stages": [s["role"] for s in cascade["stages"]],
            "run": "/api/v1/resources/swarm/run", "posture": "in-house-first",
        }
    except Exception:
        pass


async def _derive_name(problem: str, domain: str, requested: str = "") -> str:
    """The VSB's name: the user's when given, else AI-derived — with the native engine's provenance
    marker / markdown headings / scaffold lines filtered so an auto-named VSB never inherits them.
    Shared by the blocking /establish and the SSE /establish/stream."""
    name = (requested or "").strip()
    if name:
        return name
    derived = await _q(
        "Propose ONE concise, brandable business name (2-4 words, no quotes, no preamble, no "
        f"markdown) for a venture that solves: {problem}\nDomain: {domain}\nReturn ONLY the name.",
        "genesis_vsb_name",
    )
    cand = ""
    for line in (derived or "").splitlines():
        s = line.strip().strip('"').strip("*").strip()
        low = s.lower()
        if (not s or s.startswith(("_[", "#", "-", ">")) or ":" in s
                or "native structured engine" in low or len(s.split()) > 6):
            continue
        cand = s[:60]
        break
    return cand or f"VSB — {problem[:40]}"


def _seed_plan_from_journey(vsb_id: str, name: str, req: "EstablishRequest", entity: dict) -> None:
    """§4×§5 (W315) — ONE plan-seeding core for BOTH establish paths. The SSE path (the UI's
    primary) previously birthed entities whose Chief-owned Business Plan opened with an EMPTY
    concept and no §4.7 operations objective, because this logic lived only inline in the
    blocking path. Best-effort: a plan fault never loses an establishment."""
    try:
        from agentic_core.api import business_plan as bp_mod
        import time as _time
        import uuid as _uuid
        plan = bp_mod._load(vsb_id)
        plan["owner"] = req.owner_id
        plan["executive_summary"] = (
            f"{name} is a living VSB IDBO established to solve: {req.problem[:200]}."
            + (f" Go-to-market & operating model: {req.commercialisation[:280]}" if req.commercialisation else "")
        ).strip()[:1200]
        plan["concept"] = (req.concept or f"Optimal solution concept for: {req.problem[:160]}").strip()[:1200]
        plan["vision"] = f"A self-running {req.entity_type} VSB IDBO that commercialises this solution beneficently."
        plan["mission"] = f"Deliver: {req.problem[:160]}"
        plan["strategy"] = ("Concept → Design → Commercialisation, governed by the Board "
                            "(Chief = owner's digital twin) → AI CEO → C-Suite → CoE → BTO.")
        plan.setdefault("objectives", [])
        if not plan["objectives"]:
            for _title in ("Validate the concept", "Deliver the design", "Launch to market"):
                plan["objectives"].append({
                    "id": f"obj-{_uuid.uuid4().hex[:8]}", "title": _title, "kpi": "", "timeline": "",
                    "owner_role": "AI CEO", "progress_pct": 0, "status": "planned", "reviews": [],
                    "created_at": _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime()),
                })
        # §4 (W304) — the journey's operational intelligence seeds a REAL plan objective (only
        # when genuinely provided — never an invented one, never a duplicate).
        if req.operations.strip() and not any(
                o.get("source") == "genesis_journey.operations" for o in plan["objectives"]):
            plan["objectives"].append({
                "id": f"obj-{_uuid.uuid4().hex[:8]}",
                "title": "Operationalise per the journey's §4.7 operational intelligence",
                "kpi": "operational readiness delivered", "timeline": "next review",
                "owner_role": "Business Transformation Office", "progress_pct": 0,
                "status": "planned", "reviews": [],
                "source": "genesis_journey.operations",
                "created_at": _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime()),
            })
        bp_mod._save(plan)
        entity["business_plan_scope"] = vsb_id
    except Exception:
        pass


@router.post("/establish")
async def genesis_establish(req: EstablishRequest, user: dict | None = Depends(get_current_user)):
    """
    Instantiate a living VSB IDBO entity from a Genesis journey blueprint — the
    headline deliverable: Workstation *generates* the user's own Enterprise IDBO.
    The entity is persisted into the shared VSB store, so it appears in /api/v1/vsb
    and its dashboard, with its DNA encoded into the epigenetic genome registry.
    """
    # §17.5 user isolation — with auth enabled, the established VSB's owner is ALWAYS the
    # authenticated user (server-side stamp). Single-user mode unchanged.
    req.owner_id = request_owner_id(user, req.owner_id)
    import uuid as _uuid
    import time as _time
    from agentic_core.api import vsb as vsb_mod

    vsb_id = f"vsb-{_uuid.uuid4().hex[:10]}"
    name = await _derive_name(req.problem, req.domain, req.name)

    async def _attest() -> str:
        return "VSB establishment attested under v16-Omega constitutional supervision."
    gov = await _GOV.intercept({"intent": "genesis_establish", "domain": req.domain}, _attest)

    genome_spec = {
        "vsb_id": vsb_id,
        "origin": "genesis_journey",
        "problem": req.problem,
        "domain": req.domain,
        "realm": req.realm,
        "concept": req.concept[:1000],
        "design": req.design[:1000],
        "commercialisation": req.commercialisation[:1000],
        "constitutional_alignment": gov.status == "allowed",
    }
    try:
        vsb_mod._genome_registry.store_epigenetic_pattern(pattern_id=vsb_id, data=genome_spec, layer=1)
    except Exception:
        pass

    entity = {
        "vsb_id": vsb_id,
        "name": name,
        "challenge": req.problem,
        "domain": req.domain,
        "realm": req.realm,
        "scope": "commercialise",
        "owner_id": req.owner_id,
        "status": "operational",
        "stage": "commercialise",
        "genome_spec": genome_spec,
        "epigenetic_traits": {"domain": req.domain, "origin": "genesis"},
        "generation": 0,
        "ceo_specification": (req.commercialisation or req.concept)[:2000],
        "swarm_config": {
            "CEO": f"AI CEO — {name}",
            "CFO": "Financial modelling and capital allocation",
            "CTO": "Technical architecture and system health",
            "CMO": "Go-to-market and demand generation",
            "CLO": "Legal and regulatory compliance",
            "CoE": ["Research", "Design", "Engineering", "Science", "Commercial", "Compliance"],
        },
        "genesis_blueprint": {
            "concept": req.concept,
            "design": req.design,
            "commercialisation": req.commercialisation,
        },
        # §4 (W304) — the FULL journey record survives establishment (untruncated; empty for
        # the standalone path — honest stubs render in the repo, never invented content).
        "genesis_journey": {
            "research": req.research,
            "operations": req.operations,
            "selected_candidate": req.selected_candidate,
            "stage_verifications": req.stage_verifications,
        },
        "governance": {"status": gov.status, "checkpoint": gov.checkpoint_id},
        "created_at": _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime()),
    }
    # Every generated VSB IDBO entity gets its own Board of Directors, chaired by a
    # Chief that is the digital twin of THIS VSB's owner (governs the AI CEO arms-length).
    try:
        from agentic_core.api import board as board_mod
        entity["board"] = board_mod.board_for_owner(req.owner_id, f"Commercialise: {req.problem[:120]}")
    except Exception:
        pass
    # Initialise the VSB's living economic metabolism in its selected legal/economic form.
    try:
        from agentic_core.economy.metabolism import EconomicMetabolism
        _metab = EconomicMetabolism(vsb_id, req.entity_type, req.owner_id)
        entity["economy"] = {
            "entity_type": req.entity_type,
            "entity_name": _metab.template["name"],
            "waterfall": _metab.waterfall,
            "capital_preserved": _metab.template["capital_preserved"],
            "currency": "WST (virtual)",
        }
    except Exception:
        pass
    # §4 — register the established VSB as a LIVING entity the organism autonomously tends (the heartbeat
    # will continually run its virtual economy cycles), so it "operates, improves and evolves forever".
    try:
        from agentic_core.economy.living_vsbs import register as _register_living
        _register_living(vsb_id, name, req.entity_type, req.domain, req.owner_id)
        entity["living"] = {"autonomous_operation": "registered — the organism tends this VSB on the circadian "
                            "heartbeat (paced virtual economy cycles)", "virtual": True}
    except Exception:
        pass
    # W315 — the ONE shared plan-seeding core (both establish paths call it)
    _seed_plan_from_journey(vsb_id, name, req, entity)
    _attach_delivery_swarm(entity, vsb_id, name, req.problem, req.domain, req.concept)
    vsb_mod._save_vsb(entity)

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "genesis.establish", f"VSB established: {vsb_id} — {name}", 0.9)
    except Exception:
        pass

    # §3×§8×§12 (W309) — BIRTH IS ALIVE: the newborn's first §11 screen + first governed economy
    # cycle run AT establishment (the same paths the heartbeat rotates), so the entity enters the
    # organism's living loops immediately instead of waiting inert for its first rotation. Runs
    # BEFORE the birth ship so the shipped body reflects the entity WITH its first vitals.
    birth_vitals: Dict[str, Any] = {}
    try:
        from agentic_core.organism.heartbeat import screen_living_vsb
        birth_vitals["first_screen"] = screen_living_vsb(vsb_id)
    except Exception as exc:
        birth_vitals["first_screen"] = {"error": str(exc)[:160]}
    try:
        from agentic_core.economy.living_vsbs import operate_vsb
        birth_vitals["first_cycle"] = operate_vsb(vsb_id)
    except Exception as exc:
        birth_vitals["first_cycle"] = {"error": str(exc)[:160]}

    # §4 (W302) — the ONE continuous workflow ships the newborn's WHOLE §13 living body at birth
    # (repo + website + webapp + mobile + board pack in one act via the existing ship machinery) —
    # previously the entity was born body-less until five manual clicks. Best-effort: a ship
    # failure NEVER blocks establishment; the outcome is recorded honestly either way.
    initial_ship = None
    if req.ship_output:
        try:
            from agentic_core.api.vsb import ship_vsb_repo
            _s = await ship_vsb_repo(vsb_id, user=user if isinstance(user, dict) else None)
            initial_ship = {"shipped": True, "coherent_whole": _s.get("coherent_whole"),
                            "surfaces": sorted((_s.get("surfaces") or {}).keys()),
                            "commit": (_s.get("version_control") or {}).get("commit")}
        except Exception as exc:
            initial_ship = {"shipped": False, "error": str(exc)[:160]}

    return {
        "vsb_id": vsb_id,
        "name": name,
        "status": "operational",
        "dashboard": f"/api/v1/vsb/{vsb_id}",
        "governance": entity["governance"],
        "initial_ship": initial_ship,   # §4 (W302) — the body shipped at birth (or honestly not)
        "birth_vitals": birth_vitals,   # §3×§8×§12 (W309) — first screen + first cycle at birth
        "deliverable": "Living Enterprise IDBO (VSB) generated, governed, and persisted",
    }


@router.post("/establish/stream")
async def genesis_establish_stream(req: EstablishRequest, user: dict | None = Depends(get_current_user)):
    """SSE-streamed establishment — users WATCH the VSB being born: naming → constitutional
    attestation → genome encoding → Board + Chief → living economy → living-entity registration →
    business plan → delivery swarm → operational. Every event reflects a REAL completed step (the
    same machinery as the blocking /establish; nothing is narrated that did not happen)."""
    from fastapi.responses import StreamingResponse
    import json as _json
    import uuid as _uuid
    import time as _time

    req.owner_id = request_owner_id(user, req.owner_id)   # §17.5 — server-side owner stamp

    def _event(stage: str, label: str, content: str, data: dict | None = None) -> str:
        payload: Dict[str, Any] = {"stage": stage, "label": label, "content": content}
        if data:
            payload["data"] = data
        return f"data: {_json.dumps(payload)}\n\n"

    async def _stream():
        from agentic_core.api import vsb as vsb_mod
        vsb_id = f"vsb-{_uuid.uuid4().hex[:10]}"
        yield _event("init", "Establishment Initiated",
                     f"Generating a living Enterprise IDBO for: {req.problem[:120]}", {"vsb_id": vsb_id})

        # 1 — naming (AI-derived when blank; scaffold lines filtered)
        name = await _derive_name(req.problem, req.domain, req.name)
        yield _event("named", "Named", f"The enterprise is named: {name}", {"name": name})

        # 2 — constitutional attestation (gaas.v5)
        async def _attest() -> str:
            return "VSB establishment attested under v16-Omega constitutional supervision."
        gov = await _GOV.intercept({"intent": "genesis_establish", "domain": req.domain}, _attest)
        yield _event("governance", "Constitutionally Attested",
                     f"gaas.v5 gate: {gov.status}", {"status": gov.status, "checkpoint": gov.checkpoint_id})

        # 3 — genome encoding (epigenetic registry)
        genome_spec = {
            "vsb_id": vsb_id, "origin": "genesis_journey", "problem": req.problem,
            "domain": req.domain, "realm": req.realm, "concept": req.concept[:1000],
            "design": req.design[:1000], "commercialisation": req.commercialisation[:1000],
            "constitutional_alignment": gov.status == "allowed",
        }
        try:
            vsb_mod._genome_registry.store_epigenetic_pattern(pattern_id=vsb_id, data=genome_spec, layer=1)
            yield _event("genome", "Genome Encoded", "DNA stored in the epigenetic registry (layer 1).")
        except Exception as e:
            yield _event("genome", "Genome Encoding Skipped", f"registry unavailable: {str(e)[:80]}")

        # 4 — the entity, then the §3.3 living-organisation facets (each event reflects what attached)
        entity = {
            "vsb_id": vsb_id, "name": name, "challenge": req.problem, "domain": req.domain,
            "realm": req.realm, "scope": "commercialise", "owner_id": req.owner_id,
            "status": "operational", "stage": "commercialise", "genome_spec": genome_spec,
            "epigenetic_traits": {"domain": req.domain, "origin": "genesis"}, "generation": 0,
            "ceo_specification": (req.commercialisation or req.concept)[:2000],
            "genesis_blueprint": {"concept": req.concept, "design": req.design,
                                  "commercialisation": req.commercialisation},
            # §4 (W304) — the full journey record survives on the SSE path too
            "genesis_journey": {"research": req.research, "operations": req.operations,
                                "selected_candidate": req.selected_candidate,
                                "stage_verifications": req.stage_verifications},
            "governance": {"status": gov.status, "checkpoint": gov.checkpoint_id},
            "created_at": _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime()),
        }
        vsb_mod.enrich_vsb_entity(entity, owner_id=req.owner_id, problem=req.problem,
                                  domain=req.domain, entity_type=req.entity_type)
        # §4×§5 (W315) — SSE path plan PARITY: the same seeding core as the blocking path, so the
        # Chief's living Business Plan opens with the journey's concept + the §4.7 ops objective.
        _seed_plan_from_journey(vsb_id, name, req, entity)
        if entity.get("board"):
            yield _event("board", "Board + Chief Seated",
                         "Board of Directors chaired by the owner's digital-twin Chief (arms-length).",
                         {"directors": len((entity["board"] or {}).get("directors", []) or [])})
        if entity.get("economy"):
            yield _event("economy", "Living Economy Initialised",
                         f"{entity['economy'].get('entity_name')} — virtual WST only (real rails gated).",
                         {"entity_type": entity["economy"].get("entity_type")})
        if entity.get("living"):
            yield _event("living", "Registered as a Living Entity",
                         "The organism tends this VSB on the circadian heartbeat (governed economy cycles).")
        if entity.get("business_plan_scope"):
            yield _event("plan", "Business Plan Seeded",
                         "A living business plan (Chief/Board-owned) opens with the founder's idea.")

        # 5 — the bespoke in-house delivery swarm
        _attach_delivery_swarm(entity, vsb_id, name, req.problem, req.domain, req.concept)
        if entity.get("native_swarm"):
            yield _event("swarm", "Delivery Swarm Registered",
                         "Chief → AI CEO → C-Suite → CoE → Build-to-Order, runnable on the owned fabric.",
                         {"cascade_id": entity["native_swarm"].get("cascade_id")})

        # 6 — persist + operational
        vsb_mod._save_vsb(entity)
        try:
            from agentic_core.organism.biobus import biobus
            biobus.fire_signal("motor", "genesis.establish", f"VSB established: {vsb_id} — {name}", 0.9)
        except Exception:
            pass
        # 6b — §3×§8×§12 (W309): BIRTH IS ALIVE — first §11 screen + first governed economy cycle
        # at establishment (watchable; runs before the ship so the body reflects the vitals)
        birth_vitals: Dict[str, Any] = {}
        try:
            from agentic_core.organism.heartbeat import screen_living_vsb
            birth_vitals["first_screen"] = screen_living_vsb(vsb_id)
            _fs = birth_vitals["first_screen"] or {}
            yield _event("vitals", "First Compliance Screen",
                         f"§11 verdict: {_fs.get('overall', '?')}", _fs)
        except Exception as exc:
            birth_vitals["first_screen"] = {"error": str(exc)[:160]}
        try:
            from agentic_core.economy.living_vsbs import operate_vsb
            birth_vitals["first_cycle"] = operate_vsb(vsb_id)
            _fc = birth_vitals["first_cycle"] or {}
            yield _event("vitals", "First Economy Cycle",
                         ("cycle ran" if _fc.get("cycle_ran") is not False else
                          f"held: {_fc.get('held') or _fc.get('governance') or 'governance'}"), _fc)
        except Exception as exc:
            birth_vitals["first_cycle"] = {"error": str(exc)[:160]}

        # 7 — §4 (W302): the newborn's WHOLE §13 living body ships at birth (watchable, honest)
        initial_ship = None
        if req.ship_output:
            try:
                from agentic_core.api.vsb import ship_vsb_repo
                _s = await ship_vsb_repo(vsb_id, user=user if isinstance(user, dict) else None)
                for _sname, _sinfo in sorted((_s.get("surfaces") or {}).items()):
                    yield _event("ship", f"Shipped: {_sname}",
                                 ("surface generated" if "error" not in _sinfo
                                  else f"surface failed: {_sinfo['error'][:80]}"),
                                 {"surface": _sname, **{k: v for k, v in _sinfo.items() if k != 'error'}})
                initial_ship = {"shipped": True, "coherent_whole": _s.get("coherent_whole"),
                                "commit": (_s.get("version_control") or {}).get("commit")}
            except Exception as exc:
                initial_ship = {"shipped": False, "error": str(exc)[:160]}
                yield _event("ship", "Ship Deferred", f"body not shipped: {str(exc)[:80]}")

        yield _event("complete", "Operational", f"{name} is alive.", {
            "vsb_id": vsb_id, "name": name, "status": "operational",
            "dashboard": f"/api/v1/vsb/{vsb_id}",
            "initial_ship": initial_ship,
            "birth_vitals": birth_vitals,
            # parity with the blocking path — the UI badge must reflect the REAL gate outcome
            "governance": entity["governance"],
            "deliverable": "Living Enterprise IDBO (VSB) generated, governed, and persisted",
        })

    return StreamingResponse(_stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
