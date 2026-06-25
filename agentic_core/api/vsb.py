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
from fastapi.responses import StreamingResponse, HTMLResponse
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


# ── §13 — VSB IDBO Entity Repository generator (increment 1) ──────────────────
# Scaffolds a coherent, version-controlled repo for an established VSB from its REAL entity data, on the
# native fabric, in-house — quality-gated (§10) + compliance-screened (§11) + document-controlled (§6).
# HONEST: docs/config are real, generated from the entity; web/webapp/mobile are clearly-labelled
# scaffolds for later increments — never fabricated as built/compiled/running apps.
_REPO_STORE = data_path("vsb_repos")


def _repo_slug(s: str) -> str:
    out = "".join(ch if (ch.isalnum() or ch in "-_") else "-" for ch in (s or "vsb").lower())
    return out.strip("-")[:40] or "vsb"


def _build_repo_files(vsb: dict) -> dict:
    """Build the bespoke repo file-set (path -> content) from REAL VSB entity data."""
    name = vsb.get("name") or vsb.get("vsb_id")
    domain, realm = vsb.get("domain", "enterprise"), vsb.get("realm", "enterprise")
    challenge = vsb.get("challenge", "")
    bp = vsb.get("genesis_blueprint") if isinstance(vsb.get("genesis_blueprint"), dict) else {}
    concept = (bp.get("phase_1_conceptualisation") or {}).get("concept", "") if bp else ""
    design = bp.get("phase_2_design_development", "") if bp else ""
    commercial = bp.get("phase_3_commercialisation", "") if bp else ""
    f: dict = {}
    f["README.md"] = (
        f"# {name}\n\n> Living, intelligently autonomous VSB IDBO enterprise — bespoke to: {challenge}\n\n"
        f"- **Domain:** {domain} · **Realm:** {realm} · **Entity:** `{vsb.get('vsb_id')}`\n"
        f"- **Stage:** {vsb.get('stage')} · **Status:** {vsb.get('status')}\n\n"
        "This repository is the enterprise's living body — genome/identity, business plan, organisation, "
        "digital resources, AI-swarm cascades, compliance + quality record, and the integrated "
        "Website / Web app / Phone app surfaces. Generated in-house on Workstation's own AI fabric; "
        "quality-gated (§10), compliance-screened (§11), document-controlled (§6).\n\n"
        "## Structure\n"
        "- `IDENTITY.md` · `genome.json` — genome / identity\n"
        "- `BUSINESS_PLAN.md` — Executive Summary · Concept · Vision · Mission · Strategy\n"
        "- `ORGANISATION.md` — Chief → Board → AI CEO → C-Suite → CoE → Build-to-Order\n"
        "- `resources/cascades.json` — native AI-swarm cascades (reconfigurable, re-runnable)\n"
        "- `compliance/QUALITY.md` — live compliance + quality record (see `manifest.json`)\n"
        "- `web/`, `webapp/`, `mobile/` — integrated Website / Web app / Phone app (scaffold)\n")
    f["IDENTITY.md"] = (f"# Identity — {name}\n\nGenome spec:\n\n```json\n"
                        f"{json.dumps(vsb.get('genome_spec') or {}, indent=2)[:4000]}\n```\n\n"
                        f"Epigenetic traits: {vsb.get('epigenetic_traits')}\n")
    f["genome.json"] = json.dumps({"vsb_id": vsb.get("vsb_id"), "name": name, "domain": domain,
                                   "realm": realm, "generation": vsb.get("generation"),
                                   "genome_spec": vsb.get("genome_spec")}, indent=2)
    f["BUSINESS_PLAN.md"] = (f"# Business Plan — {name}\n\n## Executive Summary\n{(concept or challenge)[:1200]}\n\n"
                             f"## Concept\n{concept[:2000]}\n\n## Vision\n{challenge}\n\n"
                             f"## Design & Development\n{str(design)[:2000]}\n\n"
                             f"## Commercialisation\n{str(commercial)[:2000]}\n")
    f["ORGANISATION.md"] = (f"# Organisation — {name}\n\nChief → Board → AI CEO → C-Suite → Centres of "
                            f"Excellence → Build-to-Order.\n\n## AI CEO\n```json\n"
                            f"{json.dumps(vsb.get('ceo_specification') or {}, indent=2)[:2000]}\n```\n\n"
                            f"## Board\n```json\n{json.dumps(vsb.get('board') or {}, indent=2)[:2000]}\n```\n")
    f["resources/cascades.json"] = json.dumps({"native_swarm": vsb.get("native_swarm"),
                                               "swarm_config": vsb.get("swarm_config")}, indent=2)[:6000]
    f["compliance/QUALITY.md"] = ("# Compliance & Quality Record\n\nThe living QMS quality record (gate · "
                                  "§10 bar · §11 compliance verdicts · document-control hash) for this "
                                  "repository is in `manifest.json` → `quality_assurance`.\n")
    f["web/index.html"] = (f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
                           f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
                           f"<title>{name}</title></head><body><h1>{name}</h1><p>{challenge}</p>"
                           f"<p><em>Integrated Website — scaffold; full site generated in a later increment.</em></p>"
                           f"</body></html>")
    f["webapp/README.md"] = (f"# {name} — Web app (scaffold)\n\nReconfigurable web-app surface for the VSB "
                             "entity. Spec → scaffold; built in a later increment (not a compiled app).\n")
    f["mobile/README.md"] = (f"# {name} — Phone app (scaffold)\n\nMobile (PWA / native) surface for the VSB "
                             "entity. Spec → scaffold; built in a later increment (not a compiled app).\n")
    f["mobile/manifest.webmanifest"] = json.dumps({"name": name, "short_name": str(name or "VSB")[:12],
                                                    "start_url": "/", "display": "standalone"}, indent=2)
    return f


@router.post("/{vsb_id}/repo")
async def generate_vsb_repo(vsb_id: str):
    """Generate the bespoke VSB IDBO Entity Repository (§13) for an established VSB — real scaffold files on
    the native fabric, QMS-gated + compliance-screened + document-controlled. The Website/Web-app/Phone-app
    directories are honest scaffolds (later increments), never claimed as built/running apps."""
    vsb = _load_vsb(vsb_id)
    if not vsb:
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")
    files = _build_repo_files(vsb)
    from agentic_core.vbs.quality import assure_delivery
    combined = "\n".join(v for k, v in files.items() if k.endswith(".md"))
    # required sections = content headings that genuinely appear in the repo docs (not filenames)
    qa = await assure_delivery(combined, ["Business Plan", "Organisation", "Identity", "Executive Summary"],
                               label="vsb_repo")
    root = _REPO_STORE / vsb_id
    written = []
    for path, content in files.items():
        fp = root / path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        written.append({"path": path, "bytes": len(content.encode("utf-8"))})
    manifest = {
        "vsb_id": vsb_id, "name": vsb.get("name"), "slug": _repo_slug(vsb.get("name") or vsb_id),
        "domain": vsb.get("domain"), "realm": vsb.get("realm"),
        "repo_root": str(root), "file_count": len(written),
        "total_bytes": sum(x["bytes"] for x in written),
        "tree": sorted(x["path"] for x in written), "files": written,
        "integrated_surfaces": {"website": "web/index.html (scaffold)", "webapp": "webapp/ (scaffold)",
                                "mobile": "mobile/ (scaffold)"},
        "quality_assurance": qa, "posture": "in-house-first",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": ("Bespoke VSB IDBO entity repository — real scaffold files generated in-house from the "
                 "entity's own data; web/webapp/mobile are scaffolds for later increments (NOT built/"
                 "compiled/running apps)."),
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _REPO_STORE.mkdir(parents=True, exist_ok=True)
    (_REPO_STORE / f"{vsb_id}.manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    try:
        biobus.fire_signal("motor", "vsb.repo.generate", f"{vsb.get('name')}: {len(written)} files", 0.6)
    except Exception:
        pass
    return manifest


@router.get("/{vsb_id}/repo")
async def get_vsb_repo(vsb_id: str):
    """Retrieve the generated repo manifest (tree + per-file bytes + quality record) for a VSB."""
    p = _REPO_STORE / f"{vsb_id}.manifest.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No repository generated for VSB {vsb_id} yet.")
    return json.loads(p.read_text(encoding="utf-8"))


# ── §13 D1 increment 2 — integrated Website generator (real multi-page static HTML/CSS) ──────────
def _esc(s) -> str:
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def _website_page(title: str, active: str, body: str) -> str:
    nav = "".join(
        f'<a href="{href}" class="{ "active" if active == key else "" }">{label}</a>'
        for key, href, label in (("index", "index.html", "Home"), ("about", "about.html", "About"),
                                  ("solution", "solution.html", "Solution")))
    return (f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{_esc(title)}</title><link rel=\"stylesheet\" href=\"styles.css\"></head><body>"
            f"<header class=\"nav\"><nav>{nav}</nav></header><main>{body}</main>"
            f"<footer>Living VSB IDBO enterprise · generated in-house on Workstation's own AI fabric · "
            f"quality-gated, compliance-screened, document-controlled.</footer></body></html>")


def _build_website_files(vsb: dict, copy: dict) -> dict:
    """Build a real, multi-page static website (path -> content) from REAL entity data + in-house copy."""
    name = vsb.get("name") or vsb.get("vsb_id")
    challenge = vsb.get("challenge", "")
    domain, realm = vsb.get("domain", "enterprise"), vsb.get("realm", "enterprise")
    bp = vsb.get("genesis_blueprint") if isinstance(vsb.get("genesis_blueprint"), dict) else {}
    concept = (bp.get("phase_1_conceptualisation") or {}).get("concept", "") if bp else ""
    design = str(bp.get("phase_2_design_development", "")) if bp else ""
    commercial = str(bp.get("phase_3_commercialisation", "")) if bp else ""
    hero, about, solution = copy.get("hero", ""), copy.get("about", ""), copy.get("solution", "")
    f: dict = {}
    f["web/styles.css"] = (
        ":root{--ink:#0f172a;--bg:#fff;--mut:#475569;--accent:#4f46e5;--soft:#eef2ff}"
        "*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;"
        "color:var(--ink);background:var(--bg);line-height:1.6}"
        ".nav{border-bottom:1px solid #e2e8f0;padding:14px 24px}.nav nav{display:flex;gap:18px;max-width:980px;margin:0 auto}"
        ".nav a{color:var(--mut);text-decoration:none;font-weight:600;font-size:14px}.nav a.active{color:var(--accent)}"
        "main{max-width:980px;margin:0 auto;padding:32px 24px}"
        ".hero{background:var(--soft);border-radius:18px;padding:48px 32px;margin-bottom:28px}"
        ".hero h1{font-size:34px;margin:0 0 8px}.hero p.tag{font-size:18px;color:var(--accent);font-weight:700;margin:0 0 12px}"
        ".meta{color:var(--mut);font-size:13px}h2{margin-top:28px}section p{color:#1e293b}"
        ".cta{display:inline-block;margin-top:18px;background:var(--accent);color:#fff;padding:10px 18px;border-radius:10px;"
        "text-decoration:none;font-weight:700}footer{max-width:980px;margin:24px auto;padding:16px 24px;color:#94a3b8;"
        "font-size:12px;border-top:1px solid #e2e8f0}")
    f["web/index.html"] = _website_page(name, "index",
        f"<div class=\"hero\"><p class=\"tag\">{_esc(hero) or 'A living, intelligently autonomous enterprise'}</p>"
        f"<h1>{_esc(name)}</h1><p>{_esc(challenge)}</p>"
        f"<p class=\"meta\">Domain: {_esc(domain)} · Realm: {_esc(realm)}</p>"
        f"<a class=\"cta\" href=\"solution.html\">See the solution →</a></div>"
        f"<section><h2>What we do</h2><p>{_esc((about or concept or challenge)[:600])}</p></section>")
    f["web/about.html"] = _website_page(f"About — {name}", "about",
        f"<h1>About {_esc(name)}</h1>"
        f"<section><h2>Concept</h2><p>{_esc((concept or challenge)[:900])}</p></section>"
        f"<section><h2>Our approach</h2><p>{_esc(about[:900])}</p></section>"
        f"<section><h2>Commercialisation</h2><p>{_esc(commercial[:600])}</p></section>")
    f["web/solution.html"] = _website_page(f"Solution — {name}", "solution",
        f"<h1>The Solution</h1>"
        f"<section><h2>Overview</h2><p>{_esc(solution[:900])}</p></section>"
        f"<section><h2>Design &amp; delivery</h2><p>{_esc(design[:900])}</p></section>"
        f"<a class=\"cta\" href=\"index.html\">← Back home</a>")
    return f


@router.post("/{vsb_id}/website")
async def generate_vsb_website(vsb_id: str):
    """§13 (D1 increment 2) — generate the VSB's integrated WEBSITE: a real, multi-page static HTML/CSS
    site built from the entity's data + in-house copy, written into the repo's `web/` dir, QMS-gated +
    compliance-screened + document-controlled. HONEST: a static info/marketing site (real HTML/CSS) — NOT
    a running web app (increment 3) and not deployed/hosted."""
    vsb = _load_vsb(vsb_id)
    if not vsb:
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")
    name, challenge, domain = vsb.get("name"), vsb.get("challenge", ""), vsb.get("domain", "enterprise")
    bp = vsb.get("genesis_blueprint") if isinstance(vsb.get("genesis_blueprint"), dict) else {}
    concept = (bp.get("phase_1_conceptualisation") or {}).get("concept", "") if bp else ""
    prov: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    async def _q(prompt: str) -> str:
        m = await gateway.query_meta(prompt, agent="vsb-website")
        sb = m.get("served_by", "native")
        prov["served_by"][sb] = prov["served_by"].get(sb, 0) + 1
        prov["any_external"] = prov["any_external"] or bool(m.get("is_external"))
        return (m.get("output", "") or "").strip()

    copy = {
        "hero": await _q(f"Write ONE compelling website hero tagline (max 16 words, no quotes, one line) "
                         f"for '{name}', which addresses: {challenge}."),
        "about": await _q(f"Write 2 short plain-prose paragraphs of website 'About' copy for '{name}' "
                          f"(domain {domain}); concept: {concept[:500]}. No headings, no markdown."),
        "solution": await _q(f"Write 2 short plain-prose paragraphs of website 'Solution' copy for '{name}' "
                             f"addressing: {challenge}. No headings, no markdown."),
    }
    files = _build_website_files(vsb, copy)
    from agentic_core.vbs.quality import assure_delivery
    combined = "\n".join(c for p, c in files.items() if p.endswith(".html"))
    qa = await assure_delivery(combined, ["About", "Solution", "What we do"], label="vsb_website")

    root = _REPO_STORE / vsb_id
    written = []
    for path, content in files.items():
        fp = root / path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        written.append({"path": path, "bytes": len(content.encode("utf-8"))})
    manifest = {
        "vsb_id": vsb_id, "name": name, "kind": "static_website",
        "pages": [w for w in written if w["path"].endswith(".html")],
        "assets": [w for w in written if not w["path"].endswith(".html")],
        "page_count": sum(1 for w in written if w["path"].endswith(".html")),
        "total_bytes": sum(w["bytes"] for w in written),
        "nav": [{"label": "Home", "href": "index.html"}, {"label": "About", "href": "about.html"},
                {"label": "Solution", "href": "solution.html"}],
        "entry": "web/index.html", "preview": f"/api/v1/vsb/{vsb_id}/website/page/index",
        "repo_root": str(root), "quality_assurance": qa, "ai_provenance": prov, "posture": "in-house-first",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": ("Bespoke static website (real HTML/CSS) generated in-house from the VSB entity, written "
                 "into the repo's web/ dir. Static info site — NOT a running web app (increment 3), not "
                 "deployed/hosted."),
    }
    (root / "web" / "site.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _REPO_STORE.mkdir(parents=True, exist_ok=True)
    (_REPO_STORE / f"{vsb_id}.website.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    try:
        biobus.fire_signal("motor", "vsb.website.generate", f"{name}: {manifest['page_count']} pages", 0.6)
    except Exception:
        pass
    return manifest


@router.get("/{vsb_id}/website")
async def get_vsb_website(vsb_id: str):
    """Retrieve the generated website manifest (pages · nav · quality record · preview link)."""
    p = _REPO_STORE / f"{vsb_id}.website.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No website generated for VSB {vsb_id} yet.")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/{vsb_id}/website/page/{name}", response_class=HTMLResponse)
async def get_vsb_website_page(vsb_id: str, name: str):
    """Serve a generated website page (real HTML) for preview. Known pages only (no path traversal)."""
    if name not in {"index", "about", "solution", "styles"}:
        raise HTTPException(status_code=404, detail="Unknown page.")
    fname = "styles.css" if name == "styles" else f"{name}.html"
    fp = _REPO_STORE / vsb_id / "web" / fname
    if not fp.exists():
        raise HTTPException(status_code=404, detail=f"Website not generated for VSB {vsb_id} yet.")
    media = "text/css" if name == "styles" else "text/html"
    return HTMLResponse(fp.read_text(encoding="utf-8"), media_type=media)


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
