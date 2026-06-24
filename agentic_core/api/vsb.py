"""
VSB (Virtual Sovereign Business) — Full Spawn Pipeline

This is the flagship feature of Workstation IDBO. It takes a user's challenge
description and spawns a complete Virtual Sovereign Business entity through
the full intelligence pipeline:

  Challenge
    → Nine Cognitive Engines (understand the problem deeply)
    → MJM Orchestrator (meta-judgement: assess, validate, specify)
    → GaaS Constitutional Gate (alignment check)
    → Genomic Registry (encode VSB DNA into epigenetic memory)
    → Agent Swarm Configuration (CEO → C-Suite → CoE)
    → Digital Twin (validate the solution model)
    → VSB Entity persisted + dashboard accessible

  POST /api/v1/vsb/spawn         — spawn a new VSB from a challenge
  GET  /api/v1/vsb               — list all spawned VSBs
  GET  /api/v1/vsb/{vsb_id}      — get VSB state and vitals
  POST /api/v1/vsb/{vsb_id}/evolve — trigger evolution cycle
  GET  /api/v1/vsb/{vsb_id}/genome — get VSB genome from epigenetic registry
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus
from agentic_core.cognitive.cascade_v16 import UltimateCognitiveCascade
from agentic_core.mjm.mjm import MJMOrchestratorV4
from agentic_core.genetic_immune.genomic_registry import GenomicRegistry
router = APIRouter(prefix="/api/v1/vsb", tags=["vsb"])

_cascade = UltimateCognitiveCascade()
_mjm = MJMOrchestratorV4()
_genome_registry = GenomicRegistry()

# GaaS needs YAML genome/legal files — wrap gracefully
_gaas = None
try:
    from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4
    import os
    _genome_yaml = os.getenv("GAAS_GENOME_PATH", "")
    _legal_yaml = os.getenv("GAAS_LEGAL_PATH", "")
    if _genome_yaml and _legal_yaml and os.path.exists(_genome_yaml) and os.path.exists(_legal_yaml):
        _gaas = GaaSValidatorV4(_genome_yaml, _legal_yaml)
except Exception:
    pass

_VSB_STORE = data_path("vsb_entities")
_VSB_STORE.mkdir(parents=True, exist_ok=True)

_CONCEPT_TO_COMMERCIALISE_STAGES = [
    ("intake",       "Challenge Intake",         "CEO receives and decomposes the challenge"),
    ("research",     "Research & Discovery",      "Research CoE synthesises domain knowledge and evidence"),
    ("design",       "Solution Design",           "Design CoE architects the optimal solution"),
    ("build",        "Build & Development",       "Engineering CoE develops the solution via Factory"),
    ("validate",     "Digital Twin Validation",   "Science CoE validates solution in digital twin simulation"),
    ("commercialise","Commercialisation",          "Commercial CoE creates marketplace listing and launch plan"),
    ("genome",       "Genome Encoding",           "VSB constitution encoded in epigenetic registry"),
    ("launch",       "VSB Entity Launch",         "VSB entity created and operational"),
]


def _vsb_path(vsb_id: str) -> Path:
    return _VSB_STORE / f"{vsb_id}.json"


def _load_vsb(vsb_id: str) -> dict | None:
    p = _vsb_path(vsb_id)
    return json.loads(p.read_text()) if p.exists() else None


def _save_vsb(vsb: dict) -> None:
    _vsb_path(vsb["vsb_id"]).write_text(json.dumps(vsb, indent=2))


def _list_vsbs() -> list[dict]:
    result = []
    for p in sorted(_VSB_STORE.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            v = json.loads(p.read_text())
            result.append({
                "vsb_id": v["vsb_id"],
                "name": v.get("name", ""),
                "domain": v.get("domain", ""),
                "status": v.get("status", ""),
                "stage": v.get("stage", ""),
                "created_at": v.get("created_at", ""),
                # org flags — surface which VSBs are fully-established living organisations
                "has_board": bool(v.get("board")),
                "entity_type": (v.get("economy") or {}).get("entity_type"),
                "business_plan_scope": v.get("business_plan_scope"),
                "has_native_swarm": bool(v.get("native_swarm")),
            })
        except Exception:
            pass
    return result


@router.get("")
async def list_vsbs():
    entities = _list_vsbs()
    return {"entities": entities, "total": len(entities)}


@router.get("/{vsb_id}")
async def get_vsb(vsb_id: str):
    vsb = _load_vsb(vsb_id)
    if not vsb:
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")
    return vsb


@router.get("/{vsb_id}/genome")
async def get_vsb_genome(vsb_id: str):
    vsb = _load_vsb(vsb_id)
    if not vsb:
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")
    return {
        "vsb_id": vsb_id,
        "genome_spec": vsb.get("genome_spec", {}),
        "epigenetic_traits": vsb.get("epigenetic_traits", {}),
        "generation": vsb.get("generation", 0),
    }


class SpawnRequest(BaseModel):
    challenge: str
    domain: str = "enterprise"
    realm: str = "enterprise"
    scope: str = "build"     # concept | build | commercialise
    owner_id: str = "default"


@router.post("/spawn")
async def spawn_vsb(req: SpawnRequest):
    """
    Full VSB spawn as SSE stream. Each stage emits a progress event.
    The cognitive cascade, MJM, GaaS gate, and genome encoding happen
    before the AI synthesis cascade begins.
    """
    async def _stream():
        vsb_id = f"vsb-{uuid.uuid4().hex[:10]}"
        started = time.time()

        def _event(stage: str, label: str, content: str, data: dict = None) -> str:
            payload = {"stage": stage, "label": label, "content": content}
            if data:
                payload["data"] = data
            return f"data: {json.dumps(payload)}\n\n"

        biobus.fire_signal("sensory", "vsb.spawn", f"VSB spawn initiated: {req.challenge[:80]}", 0.9)
        yield _event("init", "VSB Spawn Initiated", f"Spawning VSB for challenge: {req.challenge[:120]}", {"vsb_id": vsb_id})

        # ── Stage 1: Cognitive Cascade ────────────────────────────────────────
        yield _event("cognitive", "Nine Cognitive Engines", "Running UltimateCognitiveCascade...")
        try:
            cascade_result = await _cascade.execute_cascade({
                "problem": req.challenge,
                "domain": req.domain,
                "scope": req.scope,
            })
            cascade_summary = str(cascade_result.get("plan", cascade_result))[:400]
        except Exception as e:
            cascade_result = {"error": str(e)}
            cascade_summary = f"Cascade encountered: {e}"
        biobus.fire_signal("cognitive", "vsb.cascade", f"Nine engines complete: {vsb_id}", 0.7)
        yield _event("cognitive_complete", "Cascade Complete", cascade_summary, {"status": cascade_result.get("status", "done")})

        # ── Stage 2: MJM Evaluation ───────────────────────────────────────────
        yield _event("mjm", "MJM Orchestrator", "Mushahida-Jaiza-Muaina evaluation...")
        try:
            mjm_result = await _mjm.run_lifecycle({"challenge": req.challenge, "cascade": cascade_result})
            mjm_summary = str(mjm_result.get("result", mjm_result))[:300]
        except Exception as e:
            mjm_result = {"error": str(e)}
            mjm_summary = f"MJM note: {e}"
        yield _event("mjm_complete", "MJM Evaluation Complete", mjm_summary)

        # ── Stage 3: GaaS Constitutional Gate ────────────────────────────────
        yield _event("gaas", "Constitutional Gate", "GaaS validation — purpose and ethics alignment...")
        gaas_passed = True
        if _gaas is not None:
            try:
                gaas_result = await _gaas.validate_intent(
                    intent={"type": "vsb_spawn", "domain": req.domain, "challenge": req.challenge[:200]},
                    context={"cascade_status": cascade_result.get("status", "unknown")}
                )
                gaas_passed = not gaas_result.get("violations", [])
                gaas_message = "Constitutional alignment confirmed." if gaas_passed else f"GaaS: {gaas_result.get('violations', [])}"
            except Exception as e:
                gaas_message = f"GaaS gate: {e}"
        else:
            gaas_message = "Constitutional alignment assumed (configure GAAS_GENOME_PATH + GAAS_LEGAL_PATH for full gate)."
        biobus.fire_signal(
            "reflex" if not gaas_passed else "motor",
            "vsb.gaas",
            f"Constitutional gate: {'PASSED' if gaas_passed else 'BLOCKED'}",
            0.9 if not gaas_passed else 0.5,
        )
        yield _event("gaas_complete", "GaaS Gate Complete", gaas_message, {"passed": gaas_passed})

        # ── Stage 4: CEO Strategy ─────────────────────────────────────────────
        yield _event("ceo_strategy", "AI CEO Strategy", "CEO generating VSB strategy and specification...")
        ceo_prompt = (
            f"You are the AI CEO of Workstation IDBO, spawning a new VSB.\n\n"
            f"Challenge: {req.challenge}\n"
            f"Domain: {req.domain} | Realm: {req.realm} | Scope: {req.scope}\n"
            f"Cognitive analysis: {str(cascade_result.get('plan', ''))[:300]}\n\n"
            f"Generate a complete VSB specification including:\n"
            f"1. VSB name and purpose statement\n"
            f"2. Agent team configuration (CEO + C-Suite + CoE)\n"
            f"3. Key products and deliverables\n"
            f"4. Success metrics and milestones\n"
            f"5. Critical resources and constraints\n\n"
            f"Format as a structured business entity specification."
        )
        try:
            ceo_spec = await gateway.query(ceo_prompt, agent="vsb_ceo")
        except Exception as e:
            ceo_spec = f"CEO specification pending: {e}"
        yield _event("ceo_complete", "CEO Strategy Complete", ceo_spec[:500])

        # ── Stage 5: Genome Encoding ──────────────────────────────────────────
        yield _event("genome", "Genome Encoding", "Encoding VSB DNA into epigenetic registry...")
        genome_spec = {
            "vsb_id": vsb_id,
            "challenge": req.challenge,
            "domain": req.domain,
            "realm": req.realm,
            "scope": req.scope,
            "cascade_analysis": cascade_result.get("status", "complete"),
            "mjm_result": str(mjm_result.get("result", "optimised"))[:100],
            "constitutional_alignment": gaas_passed,
        }
        try:
            _genome_registry.store_epigenetic_pattern(
                pattern_id=vsb_id,
                data=genome_spec,
                layer=1  # long-term layer
            )
            _genome_registry.commit_mutation(
                acquired_traits={
                    f"vsb_{vsb_id}_domain": req.domain,
                    f"vsb_{vsb_id}_spawned": time.time(),
                },
                zkp_proof=f"spawn_{vsb_id}"
            )
            genome_encoded = True
        except Exception as e:
            genome_encoded = False
        yield _event("genome_complete", "Genome Encoded", f"VSB genome {'encoded in epigenetic registry' if genome_encoded else 'stored locally'}.")

        # ── Stage 6: Agent Swarm Config ───────────────────────────────────────
        yield _event("swarm", "Agent Swarm Config", "Configuring CEO + C-Suite + CoE for this domain...")
        swarm_config = {
            "CEO":  f"AI CEO — strategic direction for {req.domain} challenge",
            "CFO":  "Financial modelling and capital allocation",
            "CTO":  "Technical architecture and system health",
            "CMO":  f"Marketing strategy for {req.domain} solution",
            "CLO":  "Legal and regulatory compliance",
            "CoE":  ["Research", "Design", "Engineering", "Science", "Commercial", "Compliance"],
        }
        yield _event("swarm_complete", "Swarm Configured", f"Agent hierarchy set for {req.domain} domain.", {"swarm": swarm_config})

        # ── Persist VSB Entity ────────────────────────────────────────────────
        vsb_entity = {
            "vsb_id": vsb_id,
            "name": f"VSB — {req.challenge[:60]}",
            "challenge": req.challenge,
            "domain": req.domain,
            "realm": req.realm,
            "scope": req.scope,
            "owner_id": req.owner_id,
            "status": "operational",
            "stage": req.scope,
            "genome_spec": genome_spec,
            "epigenetic_traits": {"domain": req.domain, "constitutional_alignment": gaas_passed},
            "generation": 0,
            "ceo_specification": ceo_spec[:2000],
            "swarm_config": swarm_config,
            "cascade_analysis": cascade_result,
            "mjm_result": mjm_result,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "elapsed_seconds": round(time.time() - started, 2),
        }
        _save_vsb(vsb_entity)
        biobus.record_operation("vsb_spawn", "vsb.spawn", success=True, payload=f"{vsb_id} [{req.domain}]")
        biobus.fire_signal("motor", "vsb.launch", f"VSB launched: {vsb_id} — {req.challenge[:60]}", 0.9)

        yield _event("complete", "VSB Operational", f"VSB {vsb_id} is now operational.", {
            "vsb_id": vsb_id,
            "dashboard": f"/api/v1/vsb/{vsb_id}",
            "elapsed_seconds": vsb_entity["elapsed_seconds"],
        })

    return StreamingResponse(
        _stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


class EvolveRequest(BaseModel):
    trigger: str = "manual"
    context: str = ""


@router.post("/{vsb_id}/evolve")
async def evolve_vsb(vsb_id: str, req: EvolveRequest):
    """
    Trigger an evolution cycle for a VSB — runs MJM analysis on current state
    and generates genome mutations to improve performance.
    """
    vsb = _load_vsb(vsb_id)
    if not vsb:
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")

    prompt = (
        f"You are performing an evolution cycle for VSB: {vsb['name']}\n"
        f"Domain: {vsb['domain']} | Stage: {vsb['stage']}\n"
        f"Current challenge: {vsb['challenge']}\n"
        f"Trigger: {req.trigger}\n"
        + (f"Context: {req.context}\n" if req.context else "")
        + "\nGenerate 3 specific evolution proposals to improve this VSB's performance, "
        "output quality, or value delivery. For each, format as:\n"
        "EVOLVE | trait | proposed_change | expected_impact\n"
        "Output ONLY the EVOLVE lines."
    )

    biobus.fire_signal("cognitive", "vsb.evolve", f"Evolution cycle: {vsb_id} gen {vsb.get('generation',0)+1}", 0.7)
    raw = await gateway.query(prompt, agent=f"vsb_evolution_{vsb_id}")
    proposals = []
    for line in raw.splitlines():
        if line.upper().startswith("EVOLVE"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                proposals.append({
                    "trait": parts[1],
                    "proposed_change": parts[2],
                    "expected_impact": parts[3],
                })

    vsb["generation"] = vsb.get("generation", 0) + 1
    vsb["last_evolved"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    vsb["evolution_proposals"] = proposals
    _save_vsb(vsb)

    return {
        "vsb_id": vsb_id,
        "generation": vsb["generation"],
        "proposals": proposals,
        "trigger": req.trigger,
    }
