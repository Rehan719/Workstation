"""
Living Deliverables — the platform's outputs as first-class, reconfigurable, re-runnable artefacts.

A deliverable (report · presentation · website · app spec · service spec · brief) is produced on
Workstation's OWN native fabric (in-house-first, with served_by provenance), persisted, and kept
LIVING: it can be re-generated and reconfigured (different brief / sections) at any time, keeping a
version history. Deliverables can be grounded in a live VSB entity and are filed under that VSB.

  GET  /api/v1/deliverables/types              — the deliverable catalogue (type → default sections)
  POST /api/v1/deliverables/produce            — produce a new living deliverable on the native fabric
  GET  /api/v1/deliverables                     — list (optionally ?vsb_id=)
  GET  /api/v1/deliverables/{id}                — one deliverable + its version history
  POST /api/v1/deliverables/{id}/regenerate     — re-run / reconfigure (appends a new version)
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/deliverables", tags=["living-deliverables"])

_STORE = data_path("deliverables.json")

# Each living-deliverable type maps to a sensible default section structure (reconfigurable).
_TYPES: Dict[str, List[str]] = {
    "report": ["Executive Summary", "Background", "Analysis", "Findings", "Recommendations", "Next Steps"],
    "presentation": ["Title & Hook", "Problem", "Solution", "Market", "Business Model", "Traction", "The Ask"],
    "website": ["Hero", "Value Proposition", "Features", "How It Works", "Pricing", "Call To Action"],
    "app": ["Overview", "Core Features", "User Flows", "Solution Architecture", "MVP Scope", "Roadmap"],
    "service": ["Service Overview", "Offering", "Delivery Model", "Pricing", "SLA & Quality", "Next Steps"],
    "brief": ["Objective", "Context", "Key Factors", "Approach", "Next Steps"],
}


def _load() -> List[Dict[str, Any]]:
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save(rows: List[Dict[str, Any]]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(rows[-300:], indent=2), encoding="utf-8")


def _grounding(vsb_id: Optional[str]) -> str:
    if not vsb_id:
        return ""
    try:
        from agentic_core.api.vsb import _load_vsb
        v = _load_vsb(vsb_id)
        if not v:
            return ""
        return (f"\nGround this deliverable in the live VSB: {v.get('name')} "
                f"(domain: {v.get('domain')}; mission: {v.get('challenge', '')}).")
    except Exception:
        return ""


async def _generate(d_type: str, title: str, brief: str, domain: str,
                    vsb_id: Optional[str], sections: List[str]) -> Dict[str, Any]:
    secs = sections or _TYPES.get(d_type, _TYPES["report"])
    prompt = (
        f"Produce a {d_type} titled '{title or brief[:60]}'.\n"
        f"Brief: {brief}\nDomain: {domain}{_grounding(vsb_id)}\n\n"
        + "\n".join(f"## {s}" for s in secs)
    )
    meta = await gateway.query_meta(prompt, agent=f"deliverable:{d_type}", timeout=30.0)
    return {
        "content": meta.get("output", ""),
        "sections": secs,
        "ai_provenance": {
            "posture": "in-house-first",
            "served_by": meta.get("served_by", "native"),
            "is_external": bool(meta.get("is_external")),
        },
    }


class ProduceRequest(BaseModel):
    type: str = "report"
    title: str = ""
    brief: str
    domain: str = "enterprise"
    vsb_id: Optional[str] = None
    sections: List[str] = []          # optional override (reconfigure the structure)


class RegenerateRequest(BaseModel):
    brief: Optional[str] = None       # reconfigure the brief …
    sections: Optional[List[str]] = None  # … and/or the section structure


@router.get("/types")
async def deliverable_types():
    return {"types": [{"id": k, "sections": v} for k, v in _TYPES.items()],
            "posture": "in-house-first"}


@router.get("/output-formats")
async def output_formats():
    """Output formats a deliverable can be rendered into — drawn from Workstation's OWN omnimedia
    factory (`agentic_core.omnimedia`). Markdown export (`/export`) is live now; the richer formats
    (pptx/pdf/docx/xlsx/html/mp4/mp3/png/svg) are produced by the omnimedia generators. Honest: only
    `md` is wired end-to-end today — the rest are the catalogue the omnimedia module exposes."""
    try:
        from agentic_core.omnimedia.factory import OutputFormat
        omnimedia = [f.value for f in OutputFormat]
    except Exception:
        omnimedia = []
    return {
        "live": ["md"],
        "omnimedia_formats": omnimedia,
        "source": "agentic_core.omnimedia (the platform's own multimedia output factory)",
    }


@router.post("/produce")
async def produce(req: ProduceRequest):
    """Produce a new LIVING deliverable on the native fabric (in-house provenance)."""
    if req.type not in _TYPES and not req.sections:
        raise HTTPException(status_code=400,
                            detail=f"Unknown type '{req.type}'. Known: {list(_TYPES)} (or pass sections).")
    _t0 = time.time()
    gen = await _generate(req.type, req.title, req.brief, req.domain, req.vsb_id, req.sections)
    _dur = int((time.time() - _t0) * 1000)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    deliverable = {
        "id": f"deliv-{uuid.uuid4().hex[:8]}",
        "type": req.type,
        "title": req.title or req.brief[:60],
        "brief": req.brief,
        "domain": req.domain,
        "vsb_id": req.vsb_id,
        "sections": gen["sections"],
        "content": gen["content"],
        "ai_provenance": gen["ai_provenance"],
        "versions": [{"brief": req.brief, "content": gen["content"],
                      "ai_provenance": gen["ai_provenance"], "created_at": now}],
        "reusable": True, "rerunnable": True, "living": True,
        "created_at": now, "updated_at": now,
    }
    rows = _load()
    rows.append(deliverable)
    _save(rows)
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "deliverables.produce", f"{req.type}: {deliverable['title']}", 0.6)
    except Exception:
        pass
    try:
        from agentic_core.api.operational_excellence import record_outcome
        record_outcome("deliverable", f"deliverable:{req.type}",
                       served_by=gen["ai_provenance"]["served_by"],
                       is_external=gen["ai_provenance"]["is_external"],
                       duration_ms=_dur, success=bool(gen["content"]),
                       ref=deliverable["id"], vsb_id=req.vsb_id)
    except Exception:
        pass
    return deliverable


@router.get("")
async def list_deliverables(vsb_id: Optional[str] = None):
    rows = _load()
    if vsb_id:
        rows = [d for d in rows if d.get("vsb_id") == vsb_id]
    summaries = [{"id": d["id"], "type": d["type"], "title": d["title"], "vsb_id": d.get("vsb_id"),
                  "versions": len(d.get("versions", [])), "served_by": d.get("ai_provenance", {}).get("served_by"),
                  "updated_at": d.get("updated_at")} for d in rows]
    return {"deliverables": summaries[::-1], "total": len(summaries)}


@router.get("/{deliverable_id}")
async def get_deliverable(deliverable_id: str):
    for d in _load():
        if d["id"] == deliverable_id:
            return d
    raise HTTPException(status_code=404, detail=f"Deliverable {deliverable_id} not found.")


def _to_markdown(d: Dict[str, Any]) -> str:
    prov = d.get("ai_provenance", {})
    served = prov.get("served_by", "native")
    in_house = "in-house" if not prov.get("is_external") else f"via {served}"
    return (
        f"# {d.get('title', 'Deliverable')}\n\n"
        f"_{d.get('type', 'deliverable')} · produced on Workstation's own AI fabric ({in_house} · {served})_\n\n"
        f"> **Brief:** {d.get('brief', '')}\n\n"
        f"{d.get('content', '')}\n\n"
        "---\n"
        f"_Living deliverable `{d.get('id')}` — version {len(d.get('versions', []) or [1])}, "
        f"updated {d.get('updated_at', '')}. Re-generate or reconfigure it any time in Workstation IDBO._\n"
    )


@router.get("/{deliverable_id}/export")
async def export_deliverable(deliverable_id: str):
    """Export a living deliverable as a downloadable Markdown document so the user can take it
    out and use it — the platform's output, in the user's hands."""
    for d in _load():
        if d["id"] == deliverable_id:
            slug = "".join(c if c.isalnum() else "-" for c in d.get("title", "deliverable")).strip("-")[:60] or "deliverable"
            return Response(
                content=_to_markdown(d),
                media_type="text/markdown",
                headers={"Content-Disposition": f'attachment; filename="{slug}.md"'},
            )
    raise HTTPException(status_code=404, detail=f"Deliverable {deliverable_id} not found.")


@router.post("/{deliverable_id}/regenerate")
async def regenerate(deliverable_id: str, req: RegenerateRequest):
    """Re-run / reconfigure a living deliverable — appends a new version (history preserved)."""
    rows = _load()
    for d in rows:
        if d["id"] == deliverable_id:
            brief = req.brief or d["brief"]
            sections = req.sections if req.sections is not None else d.get("sections", [])
            gen = await _generate(d["type"], d["title"], brief, d.get("domain", "enterprise"),
                                  d.get("vsb_id"), sections)
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            d["brief"] = brief
            d["sections"] = gen["sections"]
            d["content"] = gen["content"]
            d["ai_provenance"] = gen["ai_provenance"]
            d["updated_at"] = now
            d.setdefault("versions", []).append({"brief": brief, "content": gen["content"],
                                                 "ai_provenance": gen["ai_provenance"], "created_at": now})
            _save(rows)
            return d
    raise HTTPException(status_code=404, detail=f"Deliverable {deliverable_id} not found.")
