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

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.api.intelligence import _ai_cognitive_prime, _ai_mjm_lifecycle
from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger

router = APIRouter(prefix="/api/v1/genesis", tags=["genesis-journey"])

# Shares the same UEG audit log as the constitutional engine, so journeys are
# recorded in the one tamper-evident governance trail.
_UEG = UEGLogger("meta/gaas_v5_ueg.json")
_GOV = UnifiedConstitutionalInterceptorV16Omega("genesis-node", _UEG)


class JourneyRequest(BaseModel):
    problem: str
    domain: str = "enterprise"
    realm: str = "enterprise"   # enterprise | learning | developing | scholarship


async def _q(prompt: str, agent: str) -> str:
    """Gateway query with graceful degradation (never raises)."""
    try:
        return await gateway.query(prompt, agent=agent)
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
async def genesis_journey(req: JourneyRequest):
    """Run the full intelligently-autonomous Concept → Commercialisation cascade."""

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

    # ── Phase 2 — Design & Development (concept → buildable solution) ──
    design = await _q(
        "You are the IDBO Design & Development engine. Turn the concept into a buildable design.\n\n"
        f"Concept: {concept[:900]}\nDomain: {req.domain}\n\n"
        "## Solution Architecture\n## Core Components\n## Technology & Delivery Plan\n## MVP Scope",
        "genesis_design",
    )

    # ── Phase 3 — Enterprise Commercialisation (+ the user's VSB blueprint) ──
    commercial = await _q(
        "You are the IDBO Commercialisation engine. Define how to take this to market and the living "
        "VSB (Virtual Sovereign Business) — a specialised IDBO — that will run it.\n\n"
        f"Concept: {concept[:600]}\nDesign: {design[:600]}\nDomain: {req.domain}\n\n"
        "## Go-To-Market Strategy\n## Revenue Model\n"
        "## VSB Blueprint (AI CEO + C-Suite → CoE → BTO; living BMS/QMS/DCS/EMS)\n## First 90 Days",
        "genesis_commercial",
    )

    # ── Constitutional governance attestation (logged to the UEG) ──
    async def _attest() -> str:
        return "Sovereign Journey synthesised under v16-Omega constitutional supervision."
    gov = await _GOV.intercept({"intent": "genesis_journey", "domain": req.domain}, _attest)

    return {
        "problem": req.problem,
        "domain": req.domain,
        "realm": req.realm,
        "phase_1_conceptualisation": {"cognitive_cascade": cognitive, "mjm_assessment": mjm, "concept": concept},
        "phase_2_design_development": design,
        "phase_3_commercialisation": commercial,
        "governance": {"status": gov.status, "checkpoint": gov.checkpoint_id, "node": gov.node},
        "engines_used": [
            "Inkashaf", "Samajh", "Soch", "Aqal", "Hoshiyari", "Iman",
            "MJM", "DDPIE", "BDP", "gaas.v5",
        ],
        "deliverable": "The user's own VSB IDBO — Concept → Commercialisation",
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


@router.post("/establish")
async def genesis_establish(req: EstablishRequest):
    """
    Instantiate a living VSB IDBO entity from a Genesis journey blueprint — the
    headline deliverable: Workstation *generates* the user's own Enterprise IDBO.
    The entity is persisted into the shared VSB store, so it appears in /api/v1/vsb
    and its dashboard, with its DNA encoded into the epigenetic genome registry.
    """
    import uuid as _uuid
    import time as _time
    from agentic_core.api import vsb as vsb_mod

    vsb_id = f"vsb-{_uuid.uuid4().hex[:10]}"

    name = req.name.strip()
    if not name:
        derived = await _q(
            "Propose ONE concise, brandable business name (max 5 words, no quotes, no preamble) "
            f"for a venture that solves: {req.problem}\nDomain: {req.domain}\nReturn only the name.",
            "genesis_vsb_name",
        )
        name = (derived.strip().splitlines()[0].strip()[:60] if derived else "") or f"VSB — {req.problem[:40]}"

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
    vsb_mod._save_vsb(entity)

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "genesis.establish", f"VSB established: {vsb_id} — {name}", 0.9)
    except Exception:
        pass

    return {
        "vsb_id": vsb_id,
        "name": name,
        "status": "operational",
        "dashboard": f"/api/v1/vsb/{vsb_id}",
        "governance": entity["governance"],
        "deliverable": "Living Enterprise IDBO (VSB) generated, governed, and persisted",
    }
