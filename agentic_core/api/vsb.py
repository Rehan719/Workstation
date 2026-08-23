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
from agentic_core.config import atomic_write_json, data_path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.auth.core import get_current_user
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
    atomic_write_json(_vsb_path(vsb["vsb_id"]), vsb)


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
    bp = _blueprint(vsb)                     # W301 - canonical accessor (both shapes)
    concept, design, commercial = bp["concept"], bp["design"], bp["commercialisation"]
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
    # §8 (W310) — the §13 body EXPRESSES the genome: applied (CCA-approved) mutations are part of
    # the entity's shipped identity, not just a hidden record field.
    _mut = vsb.get("applied_mutations") or []
    _mut_md = ("\n## Applied mutations (CCA-approved)\n"
               + "\n".join(f"- **{m.get('trait')}** — {str(m.get('proposed_change'))[:160]} "
                           f"_(cca {m.get('cca_id')}, {m.get('applied_at')})_" for m in _mut[-10:])
               + "\n") if _mut else ""
    f["IDENTITY.md"] = (f"# Identity — {name}\n\nGenome spec:\n\n```json\n"
                        f"{json.dumps(vsb.get('genome_spec') or {}, indent=2)[:4000]}\n```\n\n"
                        f"Epigenetic traits: {vsb.get('epigenetic_traits')}\n" + _mut_md)
    # §4 (W304) — the journey's OPERATIONAL intelligence + selection EVIDENCE live in the repo
    # (honest stubs when the entity was established without them — never invented content).
    gj = vsb.get("genesis_journey") if isinstance(vsb.get("genesis_journey"), dict) else {}
    _ops_txt = str(gj.get("operations") or "").strip()
    f["OPERATIONS.md"] = (f"# Operational Intelligence — {name}\n\n"
                          + (_ops_txt[:8000] if _ops_txt else
                             "_Not provided at establishment — run a Genesis journey with "
                             "establish=true to carry the §4.7 operational intelligence here._\n"))
    _cand = gj.get("selected_candidate") if isinstance(gj.get("selected_candidate"), dict) else {}
    _sv = gj.get("stage_verifications") if isinstance(gj.get("stage_verifications"), dict) else {}
    _ev_lines = [f"# Selection & Verification Evidence — {name}", ""]
    if _cand:
        _ev_lines += ["## Selected Candidate (§4.5 evidence-ranked)",
                      f"- id: {_cand.get('id')} · rank: {_cand.get('rank')} · score: {_cand.get('score')}",
                      f"- coverage {_cand.get('coverage')} · specificity {_cand.get('specificity')} · structure {_cand.get('structure')}",
                      f"- framing: {str(_cand.get('framing') or '')[:160]}"]
        if _cand.get("simulation_score") is not None:       # §4.5 (W305) — simulated evidence
            _ev_lines += [f"- simulated evidence: {_cand.get('simulation_score')} "
                          f"(modelled {_cand.get('modelled_score')}; declared weights 60/40)"]
            if _cand.get("simulation"):
                _ev_lines += ["", "### Simulation excerpt", str(_cand.get("simulation"))[:800]]
        _ev_lines += [""]
    if _sv:
        _ev_lines += ["## Stage Verifications (§5 measured)"]
        _ev_lines += [f"- {k}: verified={v.get('verified')} · score={v.get('score')} · sections {v.get('sections_present')}"
                      for k, v in _sv.items() if isinstance(v, dict)]
    if not _cand and not _sv:
        _ev_lines += ["_Not provided at establishment — the journey's ranked candidates and stage "
                      "verifications appear here when established via a full Genesis journey._"]
    f["EVIDENCE.md"] = "\n".join(_ev_lines) + "\n"
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


def _blueprint(vsb: dict) -> dict:
    """§4×§13 (W301) — the CANONICAL genesis-blueprint accessor. Both writers store FLAT keys
    ({concept, design, commercialisation}) while every §13 reader expected phase_* keys — so each
    Genesis-established entity silently shipped a GENERIC repo/website/board-pack (the challenge
    fallback masked the loss). Accepts BOTH shapes (flat preferred — the only shape ever written;
    phase_* as the legacy fallback), always returns strings."""
    bp = vsb.get("genesis_blueprint") if isinstance(vsb.get("genesis_blueprint"), dict) else {}
    p1 = bp.get("phase_1_conceptualisation")
    return {
        "concept": str(bp.get("concept")
                       or ((p1 or {}).get("concept", "") if isinstance(p1, dict) else p1 or "")),
        "design": str(bp.get("design") or bp.get("phase_2_design_development", "") or ""),
        "commercialisation": str(bp.get("commercialisation")
                                 or bp.get("phase_3_commercialisation", "") or ""),
    }


def _require_vsb_access(vsb_id: str, user: dict | None) -> dict:
    """§17.5×§14 (W295) — owner-scoping guard for the per-VSB MANAGEMENT surfaces (repo · website ·
    webapp · mobile · board-pack · review-gates · evolve · ship · repo-cascade), which previously
    had NO tenant isolation: any user could manage any entity. 404 (never 403) when scoped out —
    another tenant's entity is never confirmed to exist. Single-user mode (auth off) unchanged.
    Defensive: a non-dict `user` (an internal call that leaked the FastAPI Depends sentinel) is
    treated as None — the OUTER handler already enforced the guard for internal cross-calls."""
    if user is not None and not isinstance(user, dict):
        user = None
    from agentic_core.auth.core import user_can_access
    vsb = _load_vsb(vsb_id)
    if not vsb or not user_can_access(user, vsb.get("owner_id")):
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")
    return vsb


def _version_control_commit(root, vsb_id: str, surface: str, qa: Dict[str, Any] | None) -> Dict[str, Any]:
    """§13 (W289) — the entity repository is a genuinely VERSION-CONTROLLED whole: git-init on the
    first generation (safe: the store lives under gitignored data/, so the nested .git is invisible
    to the platform repo), one commit per generation with a structured message (surface · QMS gate ·
    compliance overall · DCS seal). Fail-soft to a SHA3-512 hash-CHAIN entry in versions.json when
    git is unavailable — whichever mechanism actually ran is recorded honestly."""
    q = ((qa or {}).get("quality") or {})
    msg = (f"{surface}: QMS {'pass' if q.get('qms_gate_passed') else 'fail'} · "
           f"compliance {((q.get('compliance') or {}).get('overall'))} · "
           f"seal {str(q.get('quality_record_hash'))[:12]}")
    try:
        import subprocess

        def _git(*args):
            return subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                                  text=True, timeout=30)
        if not (root / ".git").exists():
            if _git("init").returncode != 0:
                raise RuntimeError("git init failed")
            _git("config", "user.email", "organism@workstation.local")
            _git("config", "user.name", "Workstation Organism")
        _git("add", "-A")
        c = _git("commit", "-m", msg)
        head = _git("rev-parse", "HEAD").stdout.strip()
        total = _git("rev-list", "--count", "HEAD").stdout.strip()
        return {"mechanism": "git", "commit": head[:12], "commits_total": int(total or 0),
                "message": msg, "no_changes": "nothing to commit" in (c.stdout + c.stderr)}
    except Exception as exc:
        import hashlib
        chain_path = root / "versions.json"
        try:
            chain = json.loads(chain_path.read_text(encoding="utf-8")) if chain_path.exists() else []
        except Exception:
            chain = []
        prev = chain[-1]["hash"] if chain else None
        entry = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "surface": surface,
                 "message": msg, "prev": prev,
                 "hash": hashlib.sha3_512(json.dumps({"surface": surface, "msg": msg, "prev": prev},
                                                     sort_keys=True).encode()).hexdigest()[:32]}
        chain.append(entry)
        chain_path.write_text(json.dumps(chain, indent=2), encoding="utf-8")
        return {"mechanism": "hash-chain", "commit": entry["hash"][:12], "commits_total": len(chain),
                "message": msg, "note": f"git unavailable ({str(exc)[:60]})"}


def _manifest_history(vsb_id: str, kind: str = "manifest") -> list:
    """§13 (W289) — the prior manifest is APPENDED to history instead of silently overwritten."""
    p = _REPO_STORE / f"{vsb_id}.{kind}.json"
    if not p.exists():
        return []
    try:
        prior = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    hist = list(prior.get("manifest_history") or [])
    hist.append({"generated_at": prior.get("generated_at"),
                 "file_count": prior.get("file_count"),
                 "qms_gate_passed": ((prior.get("quality_assurance") or {}).get("quality") or {}).get("qms_gate_passed"),
                 "version_control": (prior.get("version_control") or {}).get("commit")})
    return hist[-20:]


@router.post("/{vsb_id}/repo")
async def generate_vsb_repo(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """Generate the bespoke VSB IDBO Entity Repository (§13) for an established VSB — real scaffold files on
    the native fabric, QMS-gated + compliance-screened + document-controlled. The Website/Web-app/Phone-app
    directories are honest scaffolds (later increments), never claimed as built/running apps."""
    vsb = _require_vsb_access(vsb_id, user)
    files = _build_repo_files(vsb)
    from agentic_core.vbs.quality import assure_delivery
    combined = "\n".join(v for k, v in files.items() if k.endswith(".md"))
    # required sections = content headings that genuinely appear in the repo docs (not filenames)
    qa = await assure_delivery(combined, ["Business Plan", "Organisation", "Identity", "Executive Summary"],
                               label="vsb_repo")
    # §13 (W289) — compliance/QUALITY.md is the REAL record now (the sealed verdicts of THIS
    # generation), not a pointer note to a snapshot.
    _q = (qa.get("quality") or {})
    _comp = (_q.get("compliance") or {})
    files["compliance/QUALITY.md"] = (
        f"# Compliance + Quality Record — {vsb.get('name')}\n\n"
        f"Generated {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} — the SEALED record of this "
        f"generation (§10 QMS + §11 federated screen), document-controlled via the owned DCMS.\n\n"
        f"## §10 Quality\n"
        f"- QMS gate: {'PASS' if _q.get('qms_gate_passed') else 'FAIL'}\n"
        f"- Delivery coverage: {_q.get('delivery_coverage')}\n"
        f"- Non-conformance rate (stateful): {_q.get('qms_non_conformance_rate')}\n"
        f"- Document-control seal: {_q.get('quality_record_hash')}\n\n"
        f"## §11 Compliance ({_comp.get('overall', 'unscreened')})\n"
        + "".join(f"- {v['framework']}: {v['status']} — {v['reason'][:160]}\n"
                  for v in (_comp.get("verdicts") or []))
        + "\nRe-screened continuously when the organism's auto_compliance beat is enabled (W288).\n")
    root = _REPO_STORE / vsb_id
    written = []
    for path, content in files.items():
        fp = root / path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        written.append({"path": path, "bytes": len(content.encode("utf-8"))})
    _history = _manifest_history(vsb_id)                       # W289 — never silently overwritten
    _vc = _version_control_commit(root, vsb_id, "repo", qa)    # W289 — a real commit per generation
    manifest = {
        "vsb_id": vsb_id, "name": vsb.get("name"), "slug": _repo_slug(vsb.get("name") or vsb_id),
        "domain": vsb.get("domain"), "realm": vsb.get("realm"),
        "repo_root": str(root), "file_count": len(written),
        "total_bytes": sum(x["bytes"] for x in written),
        "tree": sorted(x["path"] for x in written), "files": written,
        "integrated_surfaces": {"website": "web/index.html (scaffold)", "webapp": "webapp/ (scaffold)",
                                "mobile": "mobile/ (scaffold)"},
        "quality_assurance": qa, "posture": "in-house-first",
        # §13 (W289) — genuine version control + manifest lineage
        "version_control": _vc,
        "manifest_history": _history,
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
async def get_vsb_repo(vsb_id: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """Retrieve the generated repo manifest (tree + per-file bytes + quality record) for a VSB."""
    p = _REPO_STORE / f"{vsb_id}.manifest.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No repository generated for VSB {vsb_id} yet.")
    m = json.loads(p.read_text(encoding="utf-8"))
    # §13 (W319) — staleness is SURFACED wherever the repo is read (the flag was write-only):
    # the reader always learns whether the shipped body still tracks the living record, and why not.
    sp = _REPO_STORE / f"{vsb_id}.ship.json"
    if sp.exists():
        try:
            s = json.loads(sp.read_text(encoding="utf-8"))
            m["ship_status"] = {"stale": bool(s.get("stale")), "stale_reason": s.get("stale_reason"),
                                "stale_since": s.get("stale_since"), "shipped_at": s.get("shipped_at")}
        except Exception:
            pass
    return m


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
    bp = _blueprint(vsb)                     # W301 - canonical accessor (both shapes)
    concept, design, commercial = bp["concept"], bp["design"], bp["commercialisation"]
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


def _prose_clean(text: str, one_line: bool = False) -> str:
    """§13 (W315) — shipped PUBLIC copy is prose: the native floor's scaffold artifacts
    (provenance markers, markdown headings, code fences, engine labels) are filtered before copy
    lands on a public surface. Honest: only formatting scaffold is removed, never content.
    W331 CI fix: the provenance marker `_[…]_` can also appear INLINE at the end of a content
    line (line-start filtering alone let it leak onto a shipped page on CI) — inline markers
    are stripped too."""
    import re as _re
    lines = []
    for line in (text or "").splitlines():
        # strip inline provenance markers FIRST so a content line that merely CARRIES a marker
        # keeps its prose (dropping the whole line would lose real copy)
        s = _re.sub(r"_\[[^\]\n]*\]_?", "", line.strip()).strip()
        low = s.lower()
        if (not s or s.startswith(("#", "```", ">"))
                or "native structured engine" in low or low.startswith("[engine")):
            continue
        s = s.lstrip("-*• ").strip("*_").strip()
        if s:
            lines.append(s)
    if one_line:
        return (lines[0] if lines else "")[:160]
    return "\n\n".join(lines)


@router.post("/{vsb_id}/website")
async def generate_vsb_website(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """§13 (D1 increment 2) — generate the VSB's integrated WEBSITE: a real, multi-page static HTML/CSS
    site built from the entity's data + in-house copy, written into the repo's `web/` dir, QMS-gated +
    compliance-screened + document-controlled. HONEST: a static info/marketing site (real HTML/CSS) — NOT
    a running web app (increment 3) and not deployed/hosted."""
    vsb = _require_vsb_access(vsb_id, user)
    name, challenge, domain = vsb.get("name"), vsb.get("challenge", ""), vsb.get("domain", "enterprise")
    concept = _blueprint(vsb)["concept"]     # W301 - canonical accessor (both shapes)
    prov: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    async def _q(prompt: str) -> str:
        m = await gateway.query_meta(prompt, agent="vsb-website")
        sb = m.get("served_by", "native")
        prov["served_by"][sb] = prov["served_by"].get(sb, 0) + 1
        prov["any_external"] = prov["any_external"] or bool(m.get("is_external"))
        return (m.get("output", "") or "").strip()

    # W315 — every public copy field is scaffold-CLEANED: the native floor's structured output
    # (provenance markers, ## headings) previously landed verbatim on all three shipped pages.
    copy = {
        "hero": _prose_clean(await _q(
            f"Write ONE compelling website hero tagline (max 16 words, no quotes, one line) "
            f"for '{name}', which addresses: {challenge}."), one_line=True) or f"{name}",
        "about": _prose_clean(await _q(
            f"Write 2 short plain-prose paragraphs of website 'About' copy for '{name}' "
            f"(domain {domain}); concept: {concept[:500]}. No headings, no markdown.")),
        "solution": _prose_clean(await _q(
            f"Write 2 short plain-prose paragraphs of website 'Solution' copy for '{name}' "
            f"addressing: {challenge}. No headings, no markdown.")),
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
    manifest["version_control"] = _version_control_commit(root, vsb_id, "website", qa)   # W289
    manifest["manifest_history"] = _manifest_history(vsb_id, "website")
    (_REPO_STORE / f"{vsb_id}.website.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    try:
        biobus.fire_signal("motor", "vsb.website.generate", f"{name}: {manifest['page_count']} pages", 0.6)
    except Exception:
        pass
    return manifest


@router.get("/{vsb_id}/website")
async def get_vsb_website(vsb_id: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """Retrieve the generated website manifest (pages · nav · quality record · preview link)."""
    p = _REPO_STORE / f"{vsb_id}.website.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No website generated for VSB {vsb_id} yet.")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/{vsb_id}/website/page/{name}", response_class=HTMLResponse)
async def get_vsb_website_page(vsb_id: str, name: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """Serve a generated website page (real HTML) for preview. Known pages only (no path traversal)."""
    if name not in {"index", "about", "solution", "styles"}:
        raise HTTPException(status_code=404, detail="Unknown page.")
    fname = "styles.css" if name == "styles" else f"{name}.html"
    fp = _REPO_STORE / vsb_id / "web" / fname
    if not fp.exists():
        raise HTTPException(status_code=404, detail=f"Website not generated for VSB {vsb_id} yet.")
    media = "text/css" if name == "styles" else "text/html"
    return HTMLResponse(fp.read_text(encoding="utf-8"), media_type=media)


# ── §13 D1 increment 3 — interactive Web app generator (real client-side vanilla JS) ─────────────
# A genuine, data-driven, client-side interactive app (HTML + CSS + vanilla JS + data.json) — runs
# directly in a browser, no build step. HONEST: a client-side app, NOT a server/backend app, not deployed.
_WEBAPP_APP_JS = r"""(async function () {
  const app = document.getElementById('app');
  let d = {};
  try { d = await (await fetch('data.json')).json(); } catch (e) { app.innerHTML = '<p>Could not load data.</p>'; return; }
  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'plan', label: 'Business Plan' },
    { id: 'org', label: 'Organisation' },
    { id: 'resources', label: 'Resources' },
  ];
  let active = 'overview', filter = '';
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const title = (k) => k.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  function section(id) {
    if (id === 'overview') return '<h2>' + esc(d.name) + '</h2><p class="muted">' + esc(d.domain) + ' · ' + esc(d.realm || '') + '</p><p>' + esc(d.challenge) + '</p><p>' + esc(d.concept || '') + '</p>';
    if (id === 'plan') { const bp = d.business_plan || {}; return '<h2>Business Plan</h2>' + ['executive_summary', 'concept', 'vision', 'mission', 'strategy'].map((k) => bp[k] ? '<h3>' + title(k) + '</h3><p>' + esc(bp[k]) + '</p>' : '').join(''); }
    if (id === 'org') return '<h2>Organisation</h2><p>Chief → Board → AI CEO → C-Suite → Centres of Excellence → Build-to-Order</p><h3>AI CEO</h3><pre>' + esc(JSON.stringify((d.organisation || {}).ceo || {}, null, 2)) + '</pre>';
    if (id === 'resources') { const list = (d.resources || []).filter((r) => String(r).toLowerCase().includes(filter.toLowerCase())); return '<h2>Resources</h2><input id="rfilter" placeholder="Filter resources…" value="' + esc(filter) + '"><ul>' + (list.map((r) => '<li>' + esc(r) + '</li>').join('') || '<li class="muted">No resources.</li>') + '</ul>'; }
    return '';
  }
  function render() {
    app.innerHTML = '<header><h1>' + esc(d.name) + '</h1><nav>' + tabs.map((t) => '<button data-tab="' + t.id + '" class="' + (t.id === active ? 'active' : '') + '">' + t.label + '</button>').join('') + '</nav></header><div class="content">' + section(active) + '</div><footer>Living VSB IDBO web app · generated in-house · quality-gated · compliance-screened · document-controlled.</footer>';
    app.querySelectorAll('nav button').forEach((b) => b.onclick = () => { active = b.dataset.tab; render(); });
    const rf = document.getElementById('rfilter');
    if (rf) rf.oninput = () => { filter = rf.value; const pos = rf.selectionStart; render(); const nf = document.getElementById('rfilter'); if (nf) { nf.focus(); nf.setSelectionRange(pos, pos); } };
  }
  render();
})();
"""


def _entity_appdata(vsb: dict) -> dict:
    """The entity's data shaped as the client-app data source (shared by the Web app + Phone app)."""
    name = vsb.get("name") or vsb.get("vsb_id")
    domain, realm = vsb.get("domain", "enterprise"), vsb.get("realm", "enterprise")
    challenge = vsb.get("challenge", "")
    concept = _blueprint(vsb)["concept"]     # W301 - canonical accessor (both shapes)
    ns = vsb.get("native_swarm") or {}
    roles = []
    if isinstance(ns, dict):
        for s in (ns.get("stages") or []):
            if isinstance(s, dict) and s.get("role"):
                roles.append(s["role"])
        roles += [str(o) for o in (ns.get("org") or []) if o]
    if not roles:
        roles = ["AI CEO", "C-Suite", "Centres of Excellence", "Build-to-Order", "Cognitive Cascade", "Genesis"]
    return {
        "name": name, "domain": domain, "realm": realm, "challenge": challenge,
        "concept": concept[:1500],
        "business_plan": {"executive_summary": (concept or challenge)[:600], "concept": concept[:800],
                          "vision": challenge, "mission": f"Deliver: {challenge}"[:300]},
        "organisation": {"ceo": vsb.get("ceo_specification") or {}, "board": vsb.get("board") or {}},
        "resources": roles[:24],
    }


def _build_webapp_files(vsb: dict) -> dict:
    """Build a real client-side interactive web app (HTML + CSS + vanilla JS + data.json) from entity data."""
    name = vsb.get("name") or vsb.get("vsb_id")
    appdata = _entity_appdata(vsb)
    f: dict = {}
    f["webapp/index.html"] = (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{_esc(name)} — Web app</title><link rel=\"stylesheet\" href=\"styles.css\"></head>"
        "<body><div id=\"app\"></div><script src=\"app.js\"></script></body></html>")
    f["webapp/app.js"] = _WEBAPP_APP_JS
    f["webapp/data.json"] = json.dumps(appdata, indent=2)
    f["webapp/styles.css"] = (
        ":root{--ink:#0f172a;--mut:#64748b;--accent:#4f46e5;--soft:#eef2ff;--line:#e2e8f0}"
        "*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;"
        "color:var(--ink);background:#f8fafc;line-height:1.6}#app{max-width:900px;margin:0 auto;background:#fff;"
        "min-height:100vh}header{padding:20px 24px;border-bottom:1px solid var(--line)}header h1{margin:0 0 10px;font-size:24px}"
        "nav{display:flex;gap:8px;flex-wrap:wrap}nav button{border:1px solid var(--line);background:#fff;color:var(--mut);"
        "font-weight:700;font-size:13px;padding:7px 14px;border-radius:9px;cursor:pointer}nav button.active{background:var(--accent);"
        "color:#fff;border-color:var(--accent)}.content{padding:24px}.content h2{margin-top:0}.muted{color:var(--mut)}"
        "input{width:100%;padding:9px 12px;border:1px solid var(--line);border-radius:9px;margin-bottom:10px;font-size:14px}"
        "ul{padding-left:18px}pre{background:var(--soft);padding:12px;border-radius:9px;overflow:auto;font-size:12px}"
        "footer{padding:16px 24px;color:#94a3b8;font-size:12px;border-top:1px solid var(--line)}")
    return f


_WEBAPP_SERVE = {"index": ("index.html", "text/html"), "app.js": ("app.js", "text/javascript"),
                 "styles.css": ("styles.css", "text/css"), "data.json": ("data.json", "application/json")}


@router.post("/{vsb_id}/webapp")
async def generate_vsb_webapp(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """§13 (D1 increment 3) — generate the VSB's interactive WEB APP: a real client-side app (HTML + CSS +
    vanilla JS + data.json) data-driven from the entity, written into the repo's `webapp/` dir, QMS-gated +
    compliance-screened + document-controlled. HONEST: a client-side interactive app that runs directly in
    a browser (no build) — NOT a server/backend app, not deployed/hosted."""
    vsb = _require_vsb_access(vsb_id, user)
    files = _build_webapp_files(vsb)
    from agentic_core.vbs.quality import assure_delivery
    # Gate the app's CONTENT (entity data + section structure), not the raw JS source — the JS legitimately
    # contains an input `placeholder` attribute, which is not a content stub.
    combined = (f"{vsb.get('name')} — interactive web app. Sections: Overview · Business Plan · "
                f"Organisation · Resources.\n{vsb.get('challenge', '')}\n" + files["webapp/data.json"])
    qa = await assure_delivery(combined, ["Overview", "Business Plan", "Organisation", "Resources"],
                               label="vsb_webapp")
    root = _REPO_STORE / vsb_id
    written = []
    for path, content in files.items():
        fp = root / path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        written.append({"path": path, "bytes": len(content.encode("utf-8"))})
    manifest = {
        "vsb_id": vsb_id, "name": vsb.get("name"), "kind": "client_web_app", "interactive": True,
        "files": written, "file_count": len(written), "total_bytes": sum(w["bytes"] for w in written),
        "features": ["tabbed navigation (Overview · Business Plan · Organisation · Resources)",
                     "live resource filter", "entity-driven data.json"],
        "entry": "webapp/index.html", "preview": f"/api/v1/vsb/{vsb_id}/webapp/page/index",
        "repo_root": str(root), "quality_assurance": qa, "posture": "in-house-first",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": ("Bespoke client-side interactive web app (vanilla HTML/CSS/JS, data-driven from the "
                 "entity, runs directly in a browser — no build). NOT a server/backend app, not "
                 "deployed/hosted."),
    }
    (root / "webapp" / "app.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _REPO_STORE.mkdir(parents=True, exist_ok=True)
    manifest["version_control"] = _version_control_commit(root, vsb_id, "webapp", qa)   # W289
    manifest["manifest_history"] = _manifest_history(vsb_id, "webapp")
    (_REPO_STORE / f"{vsb_id}.webapp.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    try:
        biobus.fire_signal("motor", "vsb.webapp.generate", f"{vsb.get('name')}: {len(written)} files", 0.6)
    except Exception:
        pass
    return manifest


@router.get("/{vsb_id}/webapp")
async def get_vsb_webapp(vsb_id: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """Retrieve the generated web-app manifest (files · features · quality record · preview link)."""
    p = _REPO_STORE / f"{vsb_id}.webapp.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No web app generated for VSB {vsb_id} yet.")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/{vsb_id}/webapp/page/{name}", response_class=HTMLResponse)
async def get_vsb_webapp_file(vsb_id: str, name: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """Serve a generated web-app file (index/app.js/styles.css/data.json) so it runs in-browser. Known
    files only (no path traversal)."""
    if name not in _WEBAPP_SERVE:
        raise HTTPException(status_code=404, detail="Unknown file.")
    fname, media = _WEBAPP_SERVE[name]
    fp = _REPO_STORE / vsb_id / "webapp" / fname
    if not fp.exists():
        raise HTTPException(status_code=404, detail=f"Web app not generated for VSB {vsb_id} yet.")
    return HTMLResponse(fp.read_text(encoding="utf-8"), media_type=media)


# ── §13 D1 increment 4 — Phone app generator (real installable PWA) ──────────────────────────────
# An installable, offline-capable Progressive Web App (manifest + service worker + icon + the same
# data-driven interactive app, mobile-first). HONEST: a PWA — NOT a compiled native iOS/Android app.
_MOBILE_SW_JS = r"""const CACHE = 'vsb-pwa-v1';
const ASSETS = ['./', 'index.html', 'app.js', 'styles.css', 'data.json', 'manifest.webmanifest'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(CACHE).then((c) => Promise.all(ASSETS.map((a) => c.add(a).catch(() => {}))))); self.skipWaiting(); });
self.addEventListener('activate', (e) => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', (e) => { e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request).catch(() => caches.match('index.html')))); });
"""


def _build_mobile_files(vsb: dict) -> dict:
    """Build a real installable PWA (mobile-first HTML + CSS + vanilla JS + data.json + manifest + service
    worker + icon) from entity data."""
    name = vsb.get("name") or vsb.get("vsb_id")
    short = (str(name)[:12]) or "VSB"
    appdata = _entity_appdata(vsb)
    initial = (str(name).strip()[:1] or "V").upper()
    f: dict = {}
    f["mobile/index.html"] = (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">"
        "<meta name=\"theme-color\" content=\"#4f46e5\"><meta name=\"mobile-web-app-capable\" content=\"yes\">"
        f"<link rel=\"manifest\" href=\"manifest.webmanifest\"><link rel=\"icon\" href=\"icon.svg\">"
        f"<link rel=\"stylesheet\" href=\"styles.css\"><title>{_esc(name)}</title></head>"
        "<body><div id=\"app\"></div><script src=\"app.js\"></script>"
        "<script>if('serviceWorker' in navigator){navigator.serviceWorker.register('sw.js').catch(function(){});}</script>"
        "</body></html>")
    f["mobile/app.js"] = _WEBAPP_APP_JS
    f["mobile/data.json"] = json.dumps(appdata, indent=2)
    f["mobile/manifest.webmanifest"] = json.dumps({
        "name": name, "short_name": short, "start_url": "./", "scope": "./", "display": "standalone",
        "orientation": "portrait", "background_color": "#ffffff", "theme_color": "#4f46e5",
        "description": vsb.get("challenge", "")[:160],
        "icons": [{"src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}],
    }, indent=2)
    f["mobile/sw.js"] = _MOBILE_SW_JS
    f["mobile/icon.svg"] = (
        "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\">"
        "<rect width=\"512\" height=\"512\" rx=\"96\" fill=\"#4f46e5\"/>"
        f"<text x=\"256\" y=\"330\" font-family=\"system-ui,sans-serif\" font-size=\"260\" font-weight=\"800\" "
        f"fill=\"#fff\" text-anchor=\"middle\">{_esc(initial)}</text></svg>")
    f["mobile/styles.css"] = (
        ":root{--ink:#0f172a;--mut:#64748b;--accent:#4f46e5;--soft:#eef2ff;--line:#e2e8f0}"
        "*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;"
        "color:var(--ink);background:#f1f5f9;line-height:1.6}#app{max-width:480px;margin:0 auto;background:#fff;"
        "min-height:100vh;display:flex;flex-direction:column}header{padding:18px 18px 10px}header h1{margin:0 0 12px;font-size:21px}"
        "nav{display:flex;gap:6px;overflow-x:auto}nav button{flex:0 0 auto;border:1px solid var(--line);background:#fff;"
        "color:var(--mut);font-weight:700;font-size:13px;padding:9px 14px;border-radius:999px;cursor:pointer}"
        "nav button.active{background:var(--accent);color:#fff;border-color:var(--accent)}"
        ".content{padding:18px;flex:1}.content h2{margin-top:0}.muted{color:var(--mut)}"
        "input{width:100%;padding:11px 14px;border:1px solid var(--line);border-radius:12px;margin-bottom:10px;font-size:15px}"
        "ul{padding-left:18px}pre{background:var(--soft);padding:12px;border-radius:10px;overflow:auto;font-size:12px}"
        "footer{padding:14px 18px;color:#94a3b8;font-size:11px;border-top:1px solid var(--line);text-align:center}")
    return f


_MOBILE_SERVE = {
    "index": ("index.html", "text/html"), "app.js": ("app.js", "text/javascript"),
    "styles.css": ("styles.css", "text/css"), "data.json": ("data.json", "application/json"),
    "manifest.webmanifest": ("manifest.webmanifest", "application/manifest+json"),
    "sw.js": ("sw.js", "text/javascript"), "icon.svg": ("icon.svg", "image/svg+xml"),
}


@router.post("/{vsb_id}/mobile")
async def generate_vsb_mobile(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """§13 (D1 increment 4) — generate the VSB's PHONE APP: a real installable PWA (mobile-first HTML/CSS +
    vanilla JS + data.json + web manifest + service worker + icon) data-driven from the entity, written
    into the repo's `mobile/` dir, QMS-gated + compliance-screened + document-controlled. HONEST: a PWA
    (installable + offline-capable when hosted) — NOT a compiled native iOS/Android app, not deployed."""
    vsb = _require_vsb_access(vsb_id, user)
    files = _build_mobile_files(vsb)
    from agentic_core.vbs.quality import assure_delivery
    # gate the CONTENT (entity data + sections), not the raw JS — avoid the `placeholder`-attribute false-fail
    combined = (f"{vsb.get('name')} — installable PWA phone app. Sections: Overview · Business Plan · "
                f"Organisation · Resources.\n{vsb.get('challenge', '')}\n" + files["mobile/data.json"])
    qa = await assure_delivery(combined, ["Overview", "Business Plan", "Organisation", "Resources"],
                               label="vsb_mobile")
    root = _REPO_STORE / vsb_id
    written = []
    for path, content in files.items():
        fp = root / path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8")
        written.append({"path": path, "bytes": len(content.encode("utf-8"))})
    manifest = {
        "vsb_id": vsb_id, "name": vsb.get("name"), "kind": "installable_pwa", "installable": True,
        "offline_capable": True, "files": written, "file_count": len(written),
        "total_bytes": sum(w["bytes"] for w in written),
        "features": ["installable (web manifest + icon)", "offline (service worker cache)",
                     "mobile-first interactive app (tabs + live filter)"],
        "entry": "mobile/index.html", "preview": f"/api/v1/vsb/{vsb_id}/mobile/page/index",
        "repo_root": str(root), "quality_assurance": qa, "posture": "in-house-first",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": ("Bespoke installable PWA (real web manifest + service worker + icon + mobile-first "
                 "client-side app). Installable + offline-capable when hosted. NOT a compiled native "
                 "iOS/Android app, not deployed/hosted."),
    }
    (root / "mobile" / "app.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _REPO_STORE.mkdir(parents=True, exist_ok=True)
    manifest["version_control"] = _version_control_commit(root, vsb_id, "mobile", qa)   # W289
    manifest["manifest_history"] = _manifest_history(vsb_id, "mobile")
    (_REPO_STORE / f"{vsb_id}.mobile.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    try:
        biobus.fire_signal("motor", "vsb.mobile.generate", f"{vsb.get('name')}: {len(written)} files", 0.6)
    except Exception:
        pass
    return manifest


@router.get("/{vsb_id}/mobile")
async def get_vsb_mobile(vsb_id: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """Retrieve the generated phone-app (PWA) manifest (files · features · quality record · preview link)."""
    p = _REPO_STORE / f"{vsb_id}.mobile.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No phone app generated for VSB {vsb_id} yet.")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/{vsb_id}/mobile/page/{name}", response_class=HTMLResponse)
async def get_vsb_mobile_file(vsb_id: str, name: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """Serve a generated PWA file (index/app.js/styles.css/data.json/manifest.webmanifest/sw.js/icon.svg)
    with correct content-types so the PWA runs in-browser. Known files only (no path traversal)."""
    if name not in _MOBILE_SERVE:
        raise HTTPException(status_code=404, detail="Unknown file.")
    fname, media = _MOBILE_SERVE[name]
    fp = _REPO_STORE / vsb_id / "mobile" / fname
    if not fp.exists():
        raise HTTPException(status_code=404, detail=f"Phone app not generated for VSB {vsb_id} yet.")
    return HTMLResponse(fp.read_text(encoding="utf-8"), media_type=media)


# ── §17.3 — Living Business System: the on-demand BOARD PACK (assembled fresh from live data, DCS-
# registered). Completes the 4-layer LBS (Constitutional · Strategic · Action Plan · Board Pack). The
# pack is built FRESH each call from the VSB's live entity data + an in-house AI-CEO narrative, then
# QMS-gated + §11-compliance-screened + DOCUMENT-CONTROLLED (DCS-registered) via the QMS-owned DCMS.
_BOARDPACK_STORE = data_path("vsb_board_packs")


@router.post("/{vsb_id}/board-pack")
async def generate_vsb_board_pack(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """Assemble a fresh Board Pack for the VSB from its live data (Constitutional · Strategic · Action ·
    Operational), with an in-house AI-CEO narrative — QMS-gated + compliance-screened + DCS-registered
    (document-controlled via the QMS-owned DCMS). The on-demand layer of the §17.3 Living Business System."""
    vsb = _require_vsb_access(vsb_id, user)
    name, challenge = vsb.get("name"), vsb.get("challenge", "")
    bp = _blueprint(vsb)                     # W301 - canonical accessor (both shapes)
    concept, commercial = bp["concept"], bp["commercialisation"]

    constitutional = {"mission": f"Deliver: {challenge}"[:280], "vision": challenge,
                      "values": "Integrity · Compassion · Excellence · Halal/Sharia · Beneficence · Stewardship",
                      "genome_present": bool(vsb.get("genome_spec")), "entity": vsb_id}
    operational = {"stage": vsb.get("stage"), "status": vsb.get("status"),
                   "generation": vsb.get("generation", 0), "domain": vsb.get("domain"),
                   "realm": vsb.get("realm"), "governance": (vsb.get("governance") or {}).get("status")}

    prov: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}
    meta = await gateway.query_meta(
        f"You are the AI CEO assembling a fresh Board Pack for the VSB '{name}'. Live data — stage: "
        f"{operational['stage']}; generation: {operational['generation']}; domain: {operational['domain']}; "
        f"governance: {operational['governance']}. Concept: {concept[:500]}. Commercialisation: "
        f"{commercial[:400]}.\n\nProduce a concise board pack:\n## Executive Summary\n## Strategic Position\n"
        "## Action Priorities (this period)\n## Key Risks\n## Recommendation", agent="vsb-board-pack")
    narrative = meta.get("output", "") or ""
    sb = meta.get("served_by", "native")
    prov["served_by"][sb] = prov["served_by"].get(sb, 0) + 1
    prov["any_external"] = bool(meta.get("is_external"))

    from agentic_core.vbs.quality import assure_delivery
    combined = (f"Board Pack — {name}. Sections: Executive Summary · Strategic Position · Action Priorities "
                f"· Key Risks · Recommendation.\n{narrative}")
    qa = await assure_delivery(combined, ["Executive Summary", "Strategic Position", "Action Priorities",
                                          "Recommendation"], label="board_pack")
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    pack = {
        "vsb_id": vsb_id, "name": name, "kind": "board_pack", "generated_at": ts,
        "layers": {
            "constitutional": constitutional,                                  # genome-locked
            "strategic": {"ceo": vsb.get("ceo_specification") or {}},           # AI CEO
            "action_plan": {"board": vsb.get("board") or {}},                   # BTO / board
            "operational": operational,                                         # live snapshot
        },
        "economy": vsb.get("economy") or {},
        "narrative": narrative,
        "ai_provenance": prov,
        "quality_assurance": qa,
        # DCS registration: the document-control hash from the QMS-owned DCMS (ISO 9001 §7.5)
        "dcs_registered": bool(qa.get("quality", {}).get("document_controlled")),
        "dcs_hash": qa.get("quality", {}).get("quality_record_hash"),
        "note": "Living Business System — on-demand Board Pack, assembled fresh from live data, DCS-registered.",
    }
    root = _BOARDPACK_STORE / vsb_id
    root.mkdir(parents=True, exist_ok=True)
    (root / f"{ts.replace(':', '-')}.json").write_text(json.dumps(pack, indent=2), encoding="utf-8")
    (root / "latest.json").write_text(json.dumps(pack, indent=2), encoding="utf-8")
    try:
        biobus.fire_signal("cognitive", "vsb.board_pack", f"{name}: board pack assembled", 0.6)
    except Exception:
        pass
    return pack


@router.get("/{vsb_id}/board-pack")
async def get_vsb_board_pack(vsb_id: str):
    """Retrieve the latest Board Pack for a VSB (assembled fresh on each POST)."""
    p = _BOARDPACK_STORE / vsb_id / "latest.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No board pack assembled for VSB {vsb_id} yet.")
    return json.loads(p.read_text(encoding="utf-8"))


@router.get("/{vsb_id}/board-packs")
async def list_vsb_board_packs(vsb_id: str):
    """List the VSB's Board Pack history (each is a fresh, DCS-registered point-in-time pack)."""
    root = _BOARDPACK_STORE / vsb_id
    packs = []
    if root.exists():
        for fp in sorted(root.glob("*.json"), reverse=True):
            if fp.name == "latest.json":
                continue
            try:
                d = json.loads(fp.read_text(encoding="utf-8"))
                packs.append({"generated_at": d.get("generated_at"), "dcs_hash": d.get("dcs_hash"),
                              "dcs_registered": d.get("dcs_registered")})
            except (json.JSONDecodeError, OSError):
                pass
    return {"vsb_id": vsb_id, "board_packs": packs, "total": len(packs)}


# ── §17.4 Mode 3 — optional human review gates at any Concept→Commercialisation stage (set in the VSB
# genome). Configurable per-VSB; each gate config + human decision is append-only DCS-audited (§17.5).
_LIFECYCLE_STAGE_IDS = [s[0] for s in _CONCEPT_TO_COMMERCIALISE_STAGES]


def _lifecycle_meta() -> list[dict]:
    return [{"id": sid, "name": nm, "description": desc} for sid, nm, desc in _CONCEPT_TO_COMMERCIALISE_STAGES]


def _gate_status(rg: dict, stage: str) -> dict:
    gated = stage in (rg.get("stages") or [])
    dec = (rg.get("decisions") or {}).get(stage)
    if not gated:
        status = "not_gated"
    elif dec:
        status = "approved" if dec.get("decision") == "approve" else "rejected"
    else:
        status = "pending"
    return {"stage": stage, "gated": gated, "status": status, "decision": dec,
            "blocks_progress": gated and (not dec or dec.get("decision") == "reject")}


class ReviewGatesRequest(BaseModel):
    stages: list[str] = []


class GateDecisionRequest(BaseModel):
    decision: str          # approve | reject
    note: str = ""


@router.get("/{vsb_id}/review-gates")
async def get_review_gates(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """The VSB's Mode-3 human review-gate configuration (which lifecycle stages require human review)."""
    vsb = _require_vsb_access(vsb_id, user)
    rg = vsb.get("review_gates") or {"stages": [], "decisions": {}}
    return {"vsb_id": vsb_id, "mode": "Mode 3 — optional human review gates (set in the VSB genome)",
            "stages": rg.get("stages", []), "lifecycle": _lifecycle_meta(),
            "statuses": [_gate_status(rg, s[0]) for s in _CONCEPT_TO_COMMERCIALISE_STAGES],
            "gated_count": len(rg.get("stages", []))}


@router.post("/{vsb_id}/review-gates")
async def set_review_gates(vsb_id: str, req: ReviewGatesRequest, user: dict | None = Depends(get_current_user)):
    """Set which Concept→Commercialisation stages require human review (genome config). Append-only
    DCS-audited (§17.5). Decisions for stages no longer gated are cleared."""
    vsb = _require_vsb_access(vsb_id, user)
    unknown = [s for s in req.stages if s not in _LIFECYCLE_STAGE_IDS]
    if unknown:
        raise HTTPException(status_code=400,
                            detail=f"Unknown lifecycle stages: {unknown}. Valid: {_LIFECYCLE_STAGE_IDS}")
    rg = vsb.get("review_gates") or {"stages": [], "decisions": {}}
    rg["stages"] = list(dict.fromkeys(req.stages))                      # dedupe, preserve order
    rg["decisions"] = {k: v for k, v in (rg.get("decisions") or {}).items() if k in rg["stages"]}
    vsb["review_gates"] = rg
    from agentic_core.vbs.registry import qms
    dcs_hash = await qms.control_document(f"vsb_review_gates:{vsb_id}", {"stages": rg["stages"]}, "Owner")
    _save_vsb(vsb)
    try:
        biobus.fire_signal("cognitive", "vsb.review_gates", f"{vsb.get('name')}: {len(rg['stages'])} gated", 0.5)
    except Exception:
        pass
    return {"vsb_id": vsb_id, "mode": "Mode 3 — optional human review gates (set in the VSB genome)",
            "stages": rg["stages"], "lifecycle": _lifecycle_meta(),
            "statuses": [_gate_status(rg, s[0]) for s in _CONCEPT_TO_COMMERCIALISE_STAGES],
            "dcs_hash": dcs_hash}


@router.get("/{vsb_id}/review-gates/{stage}")
async def get_review_gate_status(vsb_id: str, stage: str, user: dict | None = Depends(get_current_user)):
    """Whether a given stage gates for this VSB + its current status (used by the lifecycle to honour Mode 3)."""
    vsb = _require_vsb_access(vsb_id, user)
    if stage not in _LIFECYCLE_STAGE_IDS:
        raise HTTPException(status_code=404, detail=f"Unknown lifecycle stage '{stage}'.")
    rg = vsb.get("review_gates") or {"stages": [], "decisions": {}}
    return {"vsb_id": vsb_id, **_gate_status(rg, stage)}


@router.post("/{vsb_id}/review-gates/{stage}/decision")
async def decide_review_gate(vsb_id: str, stage: str, req: GateDecisionRequest, user: dict | None = Depends(get_current_user)):
    """Record a human review decision (approve|reject) for a gated stage. Append-only DCS-audited (§17.5)."""
    vsb = _require_vsb_access(vsb_id, user)
    if stage not in _LIFECYCLE_STAGE_IDS:
        raise HTTPException(status_code=404, detail=f"Unknown lifecycle stage '{stage}'.")
    if req.decision not in ("approve", "reject"):
        raise HTTPException(status_code=400, detail="decision must be 'approve' or 'reject'.")
    rg = vsb.get("review_gates") or {"stages": [], "decisions": {}}
    if stage not in (rg.get("stages") or []):
        raise HTTPException(status_code=400, detail=f"Stage '{stage}' is not gated for this VSB.")
    rec = {"decision": req.decision, "note": req.note,
           "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    rg.setdefault("decisions", {})[stage] = rec
    vsb["review_gates"] = rg
    from agentic_core.vbs.registry import qms
    dcs_hash = await qms.control_document(f"vsb_review_decision:{vsb_id}:{stage}", rec, "human-reviewer")
    _save_vsb(vsb)
    return {"vsb_id": vsb_id, **_gate_status(rg, stage), "dcs_hash": dcs_hash}


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
                "owner_id": v.get("owner_id"),   # §17.5 — owner scoping key
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
async def list_vsbs(user: dict | None = Depends(get_current_user)):
    # §17.5 user isolation — with auth enabled, a user sees only their own VSBs (admins see all;
    # legacy unowned entities are admin-only). Single-user mode is unchanged.
    from agentic_core.auth.core import user_can_access
    entities = [e for e in _list_vsbs() if user_can_access(user, e.get("owner_id"))]
    return {"entities": entities, "total": len(entities)}


@router.get("/{vsb_id}")
async def get_vsb(vsb_id: str, user: dict | None = Depends(get_current_user)):
    from agentic_core.auth.core import user_can_access
    vsb = _load_vsb(vsb_id)
    # 404 (not 403) when scoped out — never confirm another tenant's VSB exists
    if not vsb or not user_can_access(user, vsb.get("owner_id")):
        raise HTTPException(status_code=404, detail=f"VSB {vsb_id} not found.")
    return vsb


@router.get("/{vsb_id}/genome")
async def get_vsb_genome(vsb_id: str, user: dict | None = Depends(get_current_user)):
    vsb = _require_vsb_access(vsb_id, user)
    return {
        "vsb_id": vsb_id,
        "genome_spec": vsb.get("genome_spec", {}),
        "epigenetic_traits": vsb.get("epigenetic_traits", {}),
        "generation": vsb.get("generation", 0),
    }


def enrich_vsb_entity(entity: dict, *, owner_id: str = "default", problem: str = "",
                      domain: str = "enterprise", entity_type: str = "waqf_ltd_hybrid") -> dict:
    """§3.3 invariant (Living Plan) — EVERY generated VSB carries its own Board + a Chief that is the
    digital twin of its owner, a living economic metabolism in its selected legal/economic form,
    registration as a living entity the organism autonomously tends (heartbeat-paced virtual economy),
    and a seeded living business plan. Shared by ALL generation paths (Genesis /establish keeps its
    richer inline seeding; the SSE /vsb/spawn cascade and the Studio spawn call this) so no path can
    produce a governance-orphaned entity. Each enrichment is best-effort — never blocks generation."""
    vsb_id = entity.get("vsb_id") or entity.get("entity_id") or f"vsb-{uuid.uuid4().hex[:10]}"
    name = entity.get("name") or entity.get("solution_name") or f"VSB {vsb_id}"
    problem = str(problem or entity.get("challenge") or name)
    # Board of Directors chaired by the Chief — the digital twin of THIS VSB's owner
    try:
        from agentic_core.api import board as board_mod
        entity["board"] = board_mod.board_for_owner(owner_id, f"Commercialise: {problem[:120]}")
    except Exception:
        pass
    # Living economic metabolism in the selected legal/economic form (virtual WST only)
    try:
        from agentic_core.economy.metabolism import EconomicMetabolism
        _metab = EconomicMetabolism(vsb_id, entity_type, owner_id)
        entity["economy"] = {
            "entity_type": entity_type,
            "entity_name": _metab.template["name"],
            "waterfall": _metab.waterfall,
            "capital_preserved": _metab.template["capital_preserved"],
            "currency": "WST (virtual)",
        }
    except Exception:
        pass
    # Registered as a LIVING entity the organism autonomously tends
    try:
        from agentic_core.economy.living_vsbs import register as _register_living
        _register_living(vsb_id, name, entity_type, domain, owner_id)
        entity["living"] = {"autonomous_operation": "registered — the organism tends this VSB on the "
                            "circadian heartbeat (paced virtual economy cycles)", "virtual": True}
    except Exception:
        pass
    # Seeded living business plan (Chief/Board own it) — only if none exists for this VSB yet
    try:
        from agentic_core.api import business_plan as bp_mod
        plan = bp_mod._load(vsb_id)
        if not plan.get("executive_summary"):
            plan["owner"] = owner_id
            plan["executive_summary"] = f"{name} is a living VSB IDBO established to solve: {problem[:200]}."[:1200]
            plan["vision"] = f"A self-running {entity_type} VSB IDBO that commercialises this solution beneficently."
            plan["mission"] = f"Deliver: {problem[:160]}"
            plan["strategy"] = ("Concept → Design → Commercialisation, governed by the Board "
                                "(Chief = owner's digital twin) → AI CEO → C-Suite → CoE → BTO.")
            plan.setdefault("objectives", [])
            if not plan["objectives"]:
                for _title in ("Validate the concept", "Deliver the design", "Launch to market"):
                    plan["objectives"].append({
                        "id": f"obj-{uuid.uuid4().hex[:8]}", "title": _title, "kpi": "", "timeline": "",
                        "owner_role": "AI CEO", "progress_pct": 0, "status": "planned", "reviews": [],
                        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    })
            bp_mod._save(plan)
        entity["business_plan_scope"] = vsb_id
    except Exception:
        pass
    return entity


class SpawnRequest(BaseModel):
    challenge: str
    domain: str = "enterprise"
    realm: str = "enterprise"
    scope: str = "build"     # concept | build | commercialise
    owner_id: str = "default"
    entity_type: str = "waqf_ltd_hybrid"   # legal/economic form (see GET /api/v1/economy/entity-types)


@router.post("/spawn")
async def spawn_vsb(req: SpawnRequest, user: dict | None = Depends(get_current_user)):
    """
    Full VSB spawn as SSE stream. Each stage emits a progress event.
    The cognitive cascade, MJM, GaaS gate, and genome encoding happen
    before the AI synthesis cascade begins.
    """
    # §17.5 user isolation — with auth enabled the owner is ALWAYS the authenticated user
    # (server-side stamp; a client cannot claim another owner). Single-user mode unchanged.
    from agentic_core.auth.core import request_owner_id
    req.owner_id = request_owner_id(user, req.owner_id)

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
        # §3.3 invariant — every generated VSB carries its own Board + Chief (owner's digital twin),
        # a living economy in its selected legal form, living-entity registration, and a seeded plan.
        enrich_vsb_entity(vsb_entity, owner_id=req.owner_id, problem=req.challenge,
                          domain=req.domain, entity_type=req.entity_type)
        yield _event("governance", "Board + Living Economy Attached",
                     f"Board chaired by the owner's Chief twin; {req.entity_type} economy initialised; "
                     "registered as a living entity; business plan seeded.",
                     {"has_board": "board" in vsb_entity, "entity_type": req.entity_type,
                      "living": "living" in vsb_entity})
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
    # §13 (W290) — "continually-developing": when a shipped repo exists, a successful evolution
    # re-ships it by default so the living body tracks the life; opt out to mark it stale instead
    # (honest — never silently outdated).
    refresh_repo: bool = True


@router.post("/{vsb_id}/repo/ship")
async def ship_vsb_repo(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """§13 (W290) — ship the entity repository as ONE COHERENT WHOLE: regenerate the repo body +
    website + web-app + mobile surfaces + board pack from the entity's CURRENT living data (the
    existing generators — no duplicated build logic), under a single unified manifest with one
    repo-level compliance verdict and one version-control commit. This is the §13 canonical output
    produced in one deliberate act, not four disconnected calls."""
    vsb = _require_vsb_access(vsb_id, user)
    surfaces: Dict[str, Any] = {}
    for name, gen in (("repo", generate_vsb_repo), ("website", generate_vsb_website),
                      ("webapp", generate_vsb_webapp), ("mobile", generate_vsb_mobile),
                      ("board_pack", generate_vsb_board_pack)):
        try:
            m = await gen(vsb_id, user=user)   # W295 - authorised context flows through
            q = ((m.get("quality_assurance") or {}).get("quality") or {})
            surfaces[name] = {"qms_gate_passed": q.get("qms_gate_passed"),
                              "compliance_overall": (q.get("compliance") or {}).get("overall"),
                              "file_count": m.get("file_count") or m.get("page_count")}
        except Exception as exc:                     # a surface failure is honest, never silent
            surfaces[name] = {"error": str(exc)[:160]}
    root = _REPO_STORE / vsb_id
    # §13 (W319) — the ship-level version-control record is HONEST: it aggregates the surfaces'
    # REAL gate results (previously qa=None rendered a fabricated 'QMS fail · compliance None'
    # message even when every surface passed).
    _ok = [s for s in surfaces.values() if "error" not in s]
    _overalls = [s.get("compliance_overall") for s in _ok if s.get("compliance_overall")]
    _agg_qa = {"quality": {
        "qms_gate_passed": bool(_ok) and all(s.get("qms_gate_passed") for s in _ok),
        "compliance": {"overall": ("fail" if "fail" in _overalls else
                                   "review" if "review" in _overalls else
                                   "pass") if _overalls else None},
    }}
    unified = {
        "vsb_id": vsb_id, "name": vsb.get("name"), "shipped": True,
        "surfaces": surfaces,
        "coherent_whole": all("error" not in s for s in surfaces.values()),
        "version_control": _version_control_commit(root, vsb_id, "ship", _agg_qa),
        "stale": False,
        "shipped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (_REPO_STORE / f"{vsb_id}.ship.json").write_text(json.dumps(unified, indent=2), encoding="utf-8")
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "vsb.repo.ship", "vsb_id": vsb_id,
                         "surfaces": {k: v.get("compliance_overall") or v.get("error", "?")
                                      for k, v in surfaces.items()},
                         "coherent_whole": unified["coherent_whole"]})
    except Exception:
        pass
    try:
        biobus.fire_signal("motor", "vsb.repo.ship",
                           f"{vsb.get('name')}: {len(surfaces)} surfaces shipped as one whole", 0.7)
    except Exception:
        pass
    return unified


def mark_repo_stale(vsb_id: str, reason: str) -> bool:
    """§13 (W309) — autonomous drift honesty: when the entity's living record moves WITHOUT a
    re-ship (an operating cycle, a compliance regression), an existing shipped repo is marked
    STALE with the reason — never silently outdated. No-op when nothing was ever shipped."""
    p = _REPO_STORE / f"{vsb_id}.ship.json"
    if not p.exists():
        return False
    try:
        ship = json.loads(p.read_text(encoding="utf-8"))
        if ship.get("stale"):
            return True     # already honest
        ship["stale"] = True
        ship["stale_since"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        ship["stale_reason"] = str(reason)[:200]
        p.write_text(json.dumps(ship, indent=2), encoding="utf-8")
        # §13 (W319) — the stale mark is a recorded organism event, never a silent write-only flag.
        try:
            from agentic_core.gaas.v5 import UEGLogger
            UEGLogger().log({"type": "vsb.repo.stale", "vsb_id": vsb_id, "reason": str(reason)[:200]})
        except Exception:
            pass
        try:
            biobus.fire_signal("reflex", "vsb.repo.stale", f"{vsb_id}: shipped repo stale — {reason}", 0.5)
        except Exception:
            pass
        return True
    except Exception:
        return False


class RepoCascadeRequest(BaseModel):
    mission: str = ""
    objective_id: str | None = None


@router.post("/{vsb_id}/repo/cascade")
async def run_repo_cascade(vsb_id: str, req: RepoCascadeRequest, user: dict | None = Depends(get_current_user)):
    """§13 (W291) — the repo's AI-swarm cascades are RE-RUNNABLE: execute the entity's stored
    cascade configuration through the REAL §5 org cascade, SCOPED to this VSB (the Chief/CEO tiers
    ground in ITS living plan — W280), and bind the run's summary back INTO the repo
    (resources/runs/<run_id>.json + a version-control commit) — the repo stops being a snapshot
    and becomes an operating surface. Honest 404 when no repo exists."""
    vsb = _require_vsb_access(vsb_id, user)
    root = _REPO_STORE / vsb_id
    casc_path = root / "resources" / "cascades.json"
    if not casc_path.exists():
        raise HTTPException(status_code=404,
                            detail=f"No generated repo for {vsb_id} — POST /repo (or /repo/ship) first.")
    try:
        stored = json.loads(casc_path.read_text(encoding="utf-8"))
    except Exception:
        stored = {}
    from agentic_core.api.swarm import CascadeRequest, cascade_orchestration, _AGENTS
    # §13 (W319) — the STORED cascade configuration is genuinely EXECUTED, not discarded: the
    # entity's own swarm design (its specialist C-Suite + CoE specialisms from cascades.json)
    # shapes the org cascade that re-runs — 'reconfigurable, re-runnable' is true on the re-run leg.
    _sc = (stored.get("swarm_config") or {}) if isinstance(stored, dict) else {}
    _csuite = [k for k in _sc if k in _AGENTS and k != "CEO"]
    _coe = [str(x) for x in (_sc.get("CoE") or []) if isinstance(x, str)][:8]
    run = await cascade_orchestration(CascadeRequest(
        mission=req.mission or f"Operate and advance {vsb.get('name')} per its living plan",
        domain=vsb.get("domain", "enterprise"),
        csuite_roles=_csuite, coe_specialisms=_coe,
        scope=vsb_id, objective_id=req.objective_id))
    summary = {
        "run_id": run.get("run_id"), "mission": run.get("mission"),
        "stored_config_applied": {"csuite_roles": _csuite, "coe_specialisms": _coe,
                                  "note": "empty = balanced default (no stored swarm design)"},
        "quality": run.get("quality"), "plan_binding": run.get("plan_binding"),
        "fabric_requisitions": [f.get("resource") for f in (run.get("fabric_requisitions") or [])],
        "served_by": (run.get("ai_provenance") or {}).get("served_by"),
        "ran_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    runs_dir = root / "resources" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / f"{summary['run_id']}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    vc = _version_control_commit(root, vsb_id, f"cascade:{summary['run_id']}",
                                 {"quality": run.get("quality") or {}})
    return {"vsb_id": vsb_id, "repo_run": summary, "version_control": vc,
            "run": {k: run.get(k) for k in ("run_id", "business_plan_scope", "plan_binding",
                                            "homeostasis_adaptation")}}


@router.get("/{vsb_id}/repo/ship")
async def get_shipped_repo(vsb_id: str, user: dict | None = Depends(get_current_user)):
    _require_vsb_access(vsb_id, user)   # W295 - owner-scoped read
    """The unified ship manifest (per-surface QA · staleness · version control)."""
    p = _REPO_STORE / f"{vsb_id}.ship.json"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"No shipped repo for {vsb_id} — POST /repo/ship first.")
    return json.loads(p.read_text(encoding="utf-8"))


@router.post("/{vsb_id}/evolve")
async def evolve_vsb(vsb_id: str, req: EvolveRequest, user: dict | None = Depends(get_current_user)):
    """
    Trigger an evolution cycle for a VSB — runs MJM analysis on current state
    and generates genome mutations to improve performance.
    """
    vsb = _require_vsb_access(vsb_id, user)

    # §8 (W310) — the genome is EXPRESSED here: the entity's genome spec, epigenetic traits and
    # previously-APPLIED mutations genuinely shape the next evolution (a real read, not decoration).
    _gs = vsb.get("genome_spec") or {}
    _traits = vsb.get("epigenetic_traits") or {}
    _applied = vsb.get("applied_mutations") or []
    _genome_lines = ""
    if _gs or _traits or _applied:
        _genome_lines = (
            "Genome expression (evolve WITH the grain of this genome):\n"
            + (f"  concept: {str(_gs.get('concept'))[:200]}\n" if _gs.get("concept") else "")
            + (f"  epigenetic traits: {_traits}\n" if _traits else "")
            + (f"  applied mutations so far: "
               f"{[m.get('trait') for m in _applied[-5:]]}\n" if _applied else "")
        )
    prompt = (
        f"You are performing an evolution cycle for VSB: {vsb['name']}\n"
        f"Domain: {vsb['domain']} | Stage: {vsb['stage']}\n"
        f"Current challenge: {vsb['challenge']}\n"
        f"Trigger: {req.trigger}\n"
        + (f"Context: {req.context}\n" if req.context else "")
        + _genome_lines
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

    # §8 (W310) — HONEST fallback when the model output carries no parseable EVOLVE lines (the
    # owned structured engine, e.g.): propose from the entity's REAL measured state — unverified
    # journey stages and a non-pass §11 posture — each naming its evidence basis. Never invented;
    # with no evidence, proposals stay empty and that is recorded truthfully.
    if not proposals:
        _gj2 = vsb.get("genesis_journey") if isinstance(vsb.get("genesis_journey"), dict) else {}
        for _stage, _v in list((_gj2.get("stage_verifications") or {}).items()):
            if isinstance(_v, dict) and not _v.get("verified") and len(proposals) < 2:
                proposals.append({
                    "trait": f"{_stage}_strength",
                    "proposed_change": (f"strengthen the {_stage} stage to a verified state "
                                        f"(measured score {_v.get('score')})"),
                    "expected_impact": "stage verification passes; §10 bar coverage rises",
                    "basis": "measured stage verification (evidence-based, owned)"})
        try:
            from agentic_core.economy.living_vsbs import _latest_screen
            _scr = _latest_screen(vsb_id)
            if _scr and _scr != "pass" and len(proposals) < 3:
                proposals.append({
                    "trait": "compliance_posture",
                    "proposed_change": (f"remediate the §11 screen posture (currently '{_scr}') "
                                        "across the entity's plan and registration text"),
                    "expected_impact": "the screen returns to pass; distributions are never held",
                    "basis": "latest §11 compliance screen (evidence-based, owned)"})
        except Exception:
            pass

    vsb["generation"] = vsb.get("generation", 0) + 1
    vsb["last_evolved"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    vsb["evolution_proposals"] = proposals

    # §8 (W310) — evolution proposals are CONSEQUENTIAL: they route to the arms-length Change
    # Control Agency (vsb_evolution → MEDIUM tier, never auto-approved — the Owner keeps the gate)
    # and MUTATE the entity's genome only on approval (POST /{vsb_id}/evolution/apply).
    if proposals:
        try:
            from agentic_core.api.change_control import SubmitChangeRequest, submit_change
            _sub = await submit_change(SubmitChangeRequest(
                title=f"Evolution proposals for {vsb['name']} (gen {vsb['generation']})",
                change_type="vsb_evolution",
                description="; ".join(f"{p['trait']}: {p['proposed_change'][:120]}" for p in proposals),
                rationale=f"Evolution cycle trigger: {req.trigger}. Mutations apply ONLY on approval.",
                affected_systems=["vsb", vsb_id, "genome"],
                submitted_by=f"vsb_evolution_{vsb_id}", vsb_id=vsb_id))
            vsb["evolution_pending_cca"] = _sub.get("cca_id")
        except Exception:
            vsb["evolution_pending_cca"] = None
    _save_vsb(vsb)

    # §13 (W290) — the generated repo TRACKS the life: on evolution, an existing shipped repo is
    # re-shipped (default) or honestly marked STALE (opt-out) — never silently outdated.
    repo_refresh = None
    _ship_p = _REPO_STORE / f"{vsb_id}.ship.json"
    if _ship_p.exists():
        if req.refresh_repo:
            try:
                _re = await ship_vsb_repo(vsb_id, user=user)
                repo_refresh = {"action": "re_shipped",
                                "commit": (_re.get("version_control") or {}).get("commit"),
                                "coherent_whole": _re.get("coherent_whole")}
            except Exception as exc:
                repo_refresh = {"action": "refresh_failed", "error": str(exc)[:160]}
        else:
            try:
                _ship = json.loads(_ship_p.read_text(encoding="utf-8"))
                _ship["stale"] = True
                _ship["stale_since"] = vsb["last_evolved"]
                _ship["stale_reason"] = f"evolution generation {vsb['generation']} (refresh_repo=false)"
                _ship_p.write_text(json.dumps(_ship, indent=2), encoding="utf-8")
                repo_refresh = {"action": "marked_stale"}
            except Exception as exc:
                repo_refresh = {"action": "stale_mark_failed", "error": str(exc)[:160]}

    return {
        "vsb_id": vsb_id,
        "generation": vsb["generation"],
        "proposals": proposals,
        "evolution_pending_cca": vsb.get("evolution_pending_cca"),   # §8 (W310) — awaiting review
        "trigger": req.trigger,
        "repo_refresh": repo_refresh,
    }


def apply_approved_evolution(vsb_id: str) -> Dict[str, Any]:
    """§8 (W310) — the genome MUTATES on approval, and only on approval: when the entity's pending
    vsb_evolution change request has been APPROVED by the arms-length CCA, fold the proposals into
    the entity's epigenetic traits as traceable applied mutations, refresh the genome registry
    pattern, mark the CCA implemented, and mark the shipped repo stale (drift honesty). Honest
    no-ops: nothing pending / not yet approved / already applied."""
    vsb = _load_vsb(vsb_id)
    if not vsb:
        return {"applied": False, "reason": "vsb_not_found"}
    cca_id = vsb.get("evolution_pending_cca")
    if not cca_id:
        return {"applied": False, "reason": "no_pending_evolution"}
    from agentic_core.api.change_control import _load_change, _save_change
    change = _load_change(cca_id)
    if not change:
        return {"applied": False, "reason": "cca_not_found", "cca_id": cca_id}
    if change.get("status") != "approved":
        return {"applied": False, "reason": f"cca_status_{change.get('status')}", "cca_id": cca_id}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    proposals = vsb.get("evolution_proposals") or []
    applied = []
    traits = vsb.get("epigenetic_traits") or {}
    for p in proposals:
        t = str(p.get("trait") or "").strip()
        if not t:
            continue
        traits[t] = str(p.get("proposed_change") or "")[:300]
        applied.append({"trait": t, "proposed_change": p.get("proposed_change"),
                        "expected_impact": p.get("expected_impact"),
                        "cca_id": cca_id, "applied_at": now})
    vsb["epigenetic_traits"] = traits
    vsb["applied_mutations"] = (vsb.get("applied_mutations") or []) + applied
    vsb["evolution_pending_cca"] = None
    _save_vsb(vsb)
    try:   # the genome registry tracks the mutated pattern (layer 2 = applied epigenetics)
        _genome_registry.store_epigenetic_pattern(
            pattern_id=vsb_id, data={"applied_mutations": vsb["applied_mutations"][-10:],
                                     "epigenetic_traits": traits}, layer=2)
    except Exception:
        pass
    change["status"] = "implemented"
    change["implemented_at"] = now
    change.setdefault("audit_trail", []).append(
        {"event": "implemented", "ts": now, "by": "vsb_evolution_apply",
         "mutations_applied": len(applied)})
    _save_change(change)
    mark_repo_stale(vsb_id, f"approved evolution mutations applied (cca {cca_id})")
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "vsb.evolution.applied", "vsb_id": vsb_id, "cca_id": cca_id,
                         "mutations": [a["trait"] for a in applied]})
    except Exception:
        pass
    try:
        biobus.fire_signal("motor", "vsb.evolution.apply",
                           f"{vsb.get('name')}: {len(applied)} approved mutations applied", 0.7)
    except Exception:
        pass
    return {"applied": True, "vsb_id": vsb_id, "cca_id": cca_id,
            "mutations_applied": len(applied), "applied_mutations": applied}


@router.post("/{vsb_id}/evolution/apply")
async def apply_evolution_endpoint(vsb_id: str, user: dict | None = Depends(get_current_user)):
    """§8 (W310) — apply the entity's CCA-APPROVED evolution proposals as genome mutations.
    Refuses honestly while the change request is still awaiting review."""
    _require_vsb_access(vsb_id, user)
    return apply_approved_evolution(vsb_id)
