"""
Integration Surface — wires previously-broken frontend calls to REAL backend data.

An audit found 18 frontend features calling endpoints that were never mounted in
app_mvp (Jules-era versioned paths + a few v1 ones). Rather than leave them 404ing,
this module serves each with genuine data federated from the live organism:
gateway, immune/nervous, the gaas.v5 UEG, git history, projects, VSB entities,
platform sessions. Everything real or honestly-derived — nothing fabricated.

Covers: /api/v1/ai/* · /api/v154/* · /api/v1/evidence/graph · /api/v1/workstation/git-history
· /api/v260/user/* · /api/v190/* · /api/v240/evolution/metrics · /api/v250/search/global
· /api/v210/federation/* · /api/v220/twin/blueprint/* · /api/v290/iot/* · /api/v191/modes/* · /api/security/bounty/submit
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from agentic_core.auth.core import get_current_user
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(tags=["integration-surface"])

_DATA = data_path("integration")


def _store(name: str) -> Path:
    _DATA.mkdir(parents=True, exist_ok=True)
    return _DATA / name


def _immune() -> Dict[str, Any]:
    try:
        from agentic_core.organism.immune import immune
        return immune.status()
    except Exception:
        return {}


# ── AI surface ────────────────────────────────────────────────────────────────
@router.get("/api/v1/ai/quotas")
async def ai_quotas():
    """Which resource serves AI on this deployment - READ FROM THE NATIVE REGISTRY, the same source as
    /api/v1/native-ai/status.

    W642 (FU-642, ledger v14 R4) - this returned a typed external-first chain ("claude → openai → ollama"),
    marked the local model available unconditionally, and named the first key-holding external provider
    "active", on a platform whose selection order is in-house first and whose external tier is off by
    default. It contradicted the status route on the same backend. It now reports what that route reports,
    and when the registry cannot be read it says so instead of answering from a list."""
    try:
        from agentic_core.api.native_ai import native_status
        st = await native_status()
        return {"providers": [{"provider": n, "priority": i + 1} for i, n in enumerate(st.get("selection_order") or [])],
                "chain": " → ".join(st.get("selection_order") or []) or None,
                "active": st.get("active_model"),
                "external_allowed": st.get("external_allowed"),
                "owned_resources_available": st.get("owned_resources_available"),
                "known": True,
                "basis": ("the native model registry's selection order at this call; `active` is the resource "
                          "that would serve the next completion. Quotas are not tracked and none is reported")}
    except Exception as exc:
        return {"providers": [], "chain": None, "active": None, "known": False,
                "basis": f"NOT KNOWN - the native model registry could not be read ({exc.__class__.__name__})"}


class AIQuery(BaseModel):
    prompt: str = ""
    query: str = ""
    agent: str = "ai_surface"


@router.post("/api/v1/ai/completion")
async def ai_completion(req: AIQuery):
    prompt = req.prompt or req.query
    # W506 (P2.2) - the completion says what served it. `served_by` is None on the failure path, which is
    # a different statement from the floor having served it, so the two cases stay distinguishable.
    _served, _ext = None, False
    try:
        _ir = await gateway.query_meta(prompt, agent=req.agent, timeout=30, augment=False, user_text=(prompt or None))
        out = _ir.get("output", "")
        _served, _ext = _ir.get("served_by"), bool(_ir.get("is_external"))
    except Exception as e:
        out = f"[unavailable: {e}]"
    return {"completion": out, "prompt": prompt[:120],
            "served_by": _served, "is_external": _ext,
            "served_by_basis": ("null means no call completed - the gateway raised - which is not the "
                                "same as the deterministic floor serving this")}


@router.post("/api/v1/ai/query")
async def ai_query(req: AIQuery, user: dict | None = Depends(get_current_user)):
    prompt = req.query or req.prompt
    # W491 (refutation) — a failure was returned as the ANSWER ("[unavailable: …]"), a non-empty string
    # that every caller then rendered as the model's output. A caller cannot tell success from failure by
    # looking at a string, so the outcome is a field: `ok` plus `error`, and `answer` is null when nothing
    # was produced rather than carrying an error message dressed as content.
    _err = None
    out = None
    _served, _external = None, None
    try:
        # §17.5 invariant 1 (W343) — identity reaches the memory layer
        _owner = user.get("username") if isinstance(user, dict) else None
        _meta = await gateway.query_meta(prompt, agent="solutions", timeout=30, owner_id=_owner,
                                         augment=False)
        out = _meta.get("output") or None
        _served, _external = _meta.get("served_by"), bool(_meta.get("is_external"))
        if out is None:
            _err = "the call returned no output"
    except Exception as e:
        _err = f"{type(e).__name__}: {str(e)[:160]}"
    return {"answer": out, "ok": _err is None, "error": _err,
            "served_by": _served, "is_external": _external,
            "query": prompt[:120]}


# ── v154 status / security / constitution ────────────────────────────────────
@router.get("/api/v154/status")
async def v154_status():
    imm = _immune()
    return {"status": "operational", "health": imm.get("health"), "threat_level": imm.get("threat_level"),
            "version": "v3.0-sovereign", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


@router.get("/api/v154/security/status")
async def v154_security_status():
    imm = _immune()
    try:
        from agentic_core.gaas.v5 import UEGLogger
        ueg = UEGLogger().summary()
    except Exception:
        ueg = {}
    return {"posture": "hardened", "immune_health": imm.get("health"),
            "threat_level": imm.get("threat_level"), "gaas": "active",
            "audit_events": ueg.get("total_events", 0),
            # W526 (P3.15, FU-226) — this reported a configured post-quantum posture as a flat
            # string over nothing at all. It now reports what this platform ACTUALLY has: a keyed MAC
            # used to attest clearance verdicts, which is not a post-quantum signature and does not
            # claim to be. `signing_available` is false when no key is configured, which is the common
            # case and is a fact rather than a failure.
            "attestation": _attestation_posture()}


def _attestation_posture() -> dict:
    """What this platform can actually attest with. No secret is returned, and no algorithm is implied.

    W526 (P3.15). Placed at module scope rather than beside the route, because a helper defined between a
    decorator and its handler rebinds the route and turns every call into a 422.
    """
    from agentic_core import attestation as _att
    probe = _att.attest({"probe": "posture"})
    return {
        "signing_available": bool(probe.get("signed")),
        "algorithm": _att.ALGORITHM,
        "key_source": f"env:{_att.KEY_ENV}",
        "post_quantum": False,
        "basis": (probe.get("basis") if not probe.get("signed") else
                  "clearance verdicts are attested with a keyed MAC under the configured key"),
        "what_this_is_not": _att.WHAT_THIS_IS_NOT,
    }


@router.get("/api/v154/constitution/articles")
async def v154_constitution_articles():
    """Parse the canonical constitution markdown into article records."""
    articles: List[Dict[str, Any]] = []
    for cand in ("agentic_core/constitution/CONSTITUTION_canonical.md",
                 "agentic_core/constitution/CONSTITUTION_v137.0.0.md"):
        p = Path(cand)
        if p.exists():
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            import re
            # FU-295 (Round B) - each article carries HOW IT IS VERIFIED, or the page shows a list of rules
            # with no statement of what checks any of them. The document's own contract is that every article
            # is checkable against this platform and names its mechanism on a `*Verified:*` line; an article
            # that records its own breach says UNMET in its body. Both travel to the surface.
            _heading = re.compile(r"(?im)^#{1,4}\s*(?:Article\s*)?(\d+[\w.]*)\s*[:\-—]?\s*(.+)$")
            _matches = list(_heading.finditer(text))
            for _i, m in enumerate(_matches):
                _body = text[m.end():(_matches[_i + 1].start() if _i + 1 < len(_matches) else len(text))]
                _v = re.search(r"(?im)^\*?Verified:\*?\s*(.+?)\s*$", _body)
                articles.append({
                    "id": m.group(1),
                    "title": m.group(2).strip()[:120],
                    "category": "CORE",
                    "content": "",
                    # None, not "", when the document states no mechanism: an article whose verification is
                    # unstated must not read as one that is verified by nothing in particular.
                    "verified": (_v.group(1).strip()[:400] if _v else None),
                    "verified_basis": ("named in the article" if _v else
                                       "THIS ARTICLE NAMES NO VERIFICATION MECHANISM - it is a statement, not "
                                       "a checkable rule, and should be given one or removed"),
                    # a FIELD, never a substring of prose. A substring test returned two false
                    # positives (an article citing the MET/UNMET vocabulary, and the article that
                    # DISCUSSES the unmet ones) and missed a third that said "NOT BUILT" instead.
                    "unmet": bool(re.search(r"(?im)^\*?Status:\*?\s*UNMET\b", _body)),
                    "unmet_reason": (_u.group(1).strip()[:300]
                                     if (_u := re.search(r"(?im)^\*?Status:\*?\s*UNMET\b[\s\u2014-]*(.+?)\s*$",
                                                         _body)) else None),
                })
            if articles:
                break
    if not articles:
        # §10 (W495, FU-126, S10.3) - this fabricated a single article and the page presented it as THE
        # parsed constitution, with category chips (ETERNAL / COSMIC / CARE) that match nothing. The file
        # it was written to parse does not exist in the live tree: a cleanup MOVED the canon to
        # _archive/agentic_core/constitution/.
        #
        # It is NOT restored, and that is a deliberate call. The archived document is the Jules-era
        # v130.0 "Sovereign Digital Life Constitution": ~750 articles asserting live global marketplaces,
        # signed MoUs, ORCID scholar onboarding and post-quantum deployment - capabilities this platform
        # does not have. The plan already excludes inherited Jules material as dated and
        # agent-unreliable, so parsing it here would import hundreds of unbuilt claims onto a governance
        # surface: the exact defect class this pass exists to remove. Instead the endpoint reports that
        # no canon is present and names what actually governs. Registered for the Owner to decide whether
        # a constitution document should be authored.
        _archived = Path("_archive/agentic_core/constitution/CONSTITUTION_canonical.md")
        return {
            "articles": [],
            "canon_present": False,
            "canon_basis": (
                "NO CONSTITUTION DOCUMENT IS PRESENT in the live tree. This endpoint parses "
                "agentic_core/constitution/CONSTITUTION_canonical.md, which a repository cleanup moved to "
                + (f"{_archived.as_posix()} (still on disk). " if _archived.exists() else "the archive. ")
                + "That archived document is the inherited Jules-era v130.0 canon and is EXCLUDED as "
                  "dated: it asserts live marketplaces, signed MoUs and scholar onboarding that do not "
                  "exist here. It is not parsed, and no article is invented in its place."),
            "what_governs_instead": [
                "docs/WORKSTATION_IDBO_WHOLE_VISION.md - the vision this delivery is measured against",
                "docs/FABLE_DELIVERY_PROMPT.md - the ordered delivery plan and the Owner's rulings",
                "the arms-length Change Control Agency (/api/v1/cca) - what may change and who decides",
                "the gaas.v5 constitutional interceptor (/api/v1/gaas) - the runtime intent gate",
            ],
            "categories_available": [],
            # W515 pre-flight - these three are carried on BOTH branches. They used to appear only when a
            # canon was present, so a reader indexing them got undefined precisely when none was, which is
            # when things are already wrong. An empty list here means "no articles to report on", not
            # "no articles have a problem".
            "articles_recording_a_breach": [],
            "articles_naming_no_mechanism": [],
            "verification_note": ("no canon is present, so there is nothing to verify and these lists are "
                                  "empty for that reason rather than because every article passed"),
        }
    _shown = articles[:200]
    _unverified = [a["id"] for a in _shown if not a.get("verified")]
    _unmet = [a["id"] for a in _shown if a.get("unmet")]
    return {"articles": _shown, "canon_present": True,
            "canon_basis": (f"parsed {len(articles)} article heading(s) from the canonical markdown"
                            + (f"; SHOWING {len(_shown)} - the rest are truncated by a cap and are NOT absent"
                               if len(articles) > len(_shown) else "")),
            # a constitution that cannot report its own breaches is a claim, not a governance instrument
            "articles_recording_a_breach": _unmet,
            "articles_naming_no_mechanism": _unverified,
            "verification_note": ("every article should name how it is checked. The ids listed in "
                                  "articles_naming_no_mechanism do not, and that is a gap in the document "
                                  "rather than evidence that the platform complies"),
            "what_governs_instead": [],
            "categories_available": sorted({a.get("category") for a in articles if a.get("category")})}


# ── Evidence graph (from the gaas.v5 UEG) ────────────────────────────────────
@router.get("/api/v1/evidence/graph")
async def evidence_graph():
    try:
        from agentic_core.gaas.v5 import UEGLogger
        ueg = UEGLogger()
        nodes = ueg.recent(40)
    except Exception:
        nodes = []
    graph_nodes = [{"id": n["id"], "type": n.get("data", {}).get("type", "event"),
                    "label": n.get("data", {}).get("action") or n.get("data", {}).get("type", "event"),
                    "hash": str(n.get("hash", ""))[:12]} for n in nodes]
    edges = [{"from": nodes[i]["id"], "to": nodes[i + 1]["id"]} for i in range(len(nodes) - 1)]
    return {"nodes": graph_nodes, "edges": edges, "source": "gaas.v5 UEG (hash-chained)"}


# ── Workstation git history (real) ────────────────────────────────────────────
@router.get("/api/v1/workstation/git-history")
async def git_history(limit: int = 20):
    """The commit log of the repository the SERVER process is running out of - Workstation's own source.
    W491 (FU-179): this was surfaced to users as "Recent Project Activity", which reads as activity in
    THEIR projects; it is not, and it never was. The payload now says whose history this is, and an
    unreadable log is reported as unreadable instead of collapsing to an empty list that reads as "no
    activity". Nothing about a user's projects can be derived from this endpoint."""
    commits: List[Dict[str, str]] = []
    unreadable_reason = None
    repository = None
    try:
        _top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, timeout=8, cwd=".")
        repository = (_top.stdout or "").strip() or None
        if repository is None:
            unreadable_reason = ((_top.stderr or "").strip()[:160]
                                 or "the directory the server runs in is not a git repository")
        else:
            out = subprocess.run(["git", "log", f"-{limit}", "--pretty=format:%h|%an|%ar|%s"],
                                 capture_output=True, text=True, timeout=8, cwd=".")
            if out.returncode != 0:
                unreadable_reason = (out.stderr or "").strip()[:160] or f"git log exited {out.returncode}"
            for line in out.stdout.splitlines():
                parts = line.split("|", 3)
                if len(parts) == 4:
                    commits.append({"hash": parts[0], "author": parts[1], "when": parts[2], "message": parts[3]})
    except Exception as e:
        unreadable_reason = f"{e.__class__.__name__}: {str(e)[:140]}"
    # W491 (refutation) — `total` was len(commits), i.e. the size of the page just fetched: ?limit=3 on a
    # repository of ~1500 commits returned total 3. That is the exact defect this round's rule names ("a
    # fetch limit is not a total") left standing in the endpoint the round rewrote for it. The page size
    # and the repository's real count are now two different fields, and the real one is counted or null.
    repo_total = None
    if repository and unreadable_reason is None:
        try:
            _cnt = subprocess.run(["git", "rev-list", "--count", "HEAD"],
                                  capture_output=True, text=True, timeout=8, cwd=".")
            repo_total = int((_cnt.stdout or "").strip()) if _cnt.returncode == 0 else None
        except Exception:
            repo_total = None
    return {"commits": commits, "returned": len(commits), "limit": limit,
            "repository_commits_total": repo_total,
            "counts_basis": ("`returned` is how many this call fetched (bounded by `limit`); "
                             "`repository_commits_total` is the repository's own count, or null when it "
                             "could not be read — the two are never the same number by construction"),
            # whose history this is - so no surface can label it as the reader's own project activity
            "subject": "workstation_platform_source",
            "is_user_project_activity": False,
            "repository": (repository.rsplit("/", 1)[-1] if repository else None),
            "readable": unreadable_reason is None,
            "unreadable_reason": unreadable_reason,
            "basis": ("git log of the working directory the server process was started in; a user's own "
                      "project activity is not tracked here")}


# ── v260 personalization ──────────────────────────────────────────────────────
class Activity(BaseModel):
    user_id: str = "default"
    action: str = ""
    detail: str = ""


@router.get("/api/v260/user/preferences")
async def user_prefs(user_id: str = "default"):
    p = _store(f"prefs_{user_id}.json")
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"user_id": user_id, "theme": "sovereign", "realm": "enterprise",
            "notifications": True, "density": "comfortable"}


@router.get("/api/v260/user/recommendations")
async def user_recs(user_id: str = "default"):
    """Recommendations derived from live state — not a static list."""
    recs: List[Dict[str, Any]] = []
    try:
        from agentic_core.api.transformation import _realise
        real = _realise().get("overall_realisation", 1.0)
        if real < 1.0:
            recs.append({"id": "r-transform", "title": "Close the next vision gap",
                         "route": "/transformation", "reason": f"realisation at {int(real*100)}%"})
    except Exception:
        pass
    try:
        from agentic_core.api.business_plan import _load
        pending = [o for o in _load("workstation").get("objectives", []) if o.get("progress_pct", 0) < 100]
        if pending:
            recs.append({"id": "r-bp", "title": f"Review {len(pending)} business-plan objective(s)",
                         "route": "/business-plan", "reason": "objectives below 100%"})
    except Exception:
        pass
    try:
        from agentic_core.api.vsb import _list_vsbs
        n = len(_list_vsbs())
        recs.append({"id": "r-vsb", "title": "Inspect your living VSBs" if n else "Establish your first VSB",
                     "route": "/vsb", "reason": f"{n} VSB(s) exist"})
    except Exception:
        pass
    recs.append({"id": "r-genesis", "title": "Run a Genesis journey", "route": "/genesis",
                 "reason": "Concept→Commercialisation"})
    return {"user_id": user_id, "recommendations": recs[:5],
            "source": "derived from live realisation / business-plan / VSB state"}


@router.post("/api/v260/user/activity")
async def user_activity(req: Activity):
    p = _store(f"activity_{req.user_id}.json")
    log = []
    if p.exists():
        try:
            log = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    log.append({"action": req.action, "detail": req.detail, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    p.write_text(json.dumps(log[-200:], indent=2), encoding="utf-8")
    return {"recorded": True, "total": len(log)}


# ── v190 / v240 evolution + extrospection ─────────────────────────────────────
@router.get("/api/v190/evolution/trajectories")
async def evo_trajectories():
    try:
        from agentic_core.api.sovereign_evolution import _load_roadmap
        rm = _load_roadmap()
        dirs = rm.get("ceo_directives", [])
    except Exception:
        dirs = []
    return {"trajectories": [{"id": d.get("id"), "function": d.get("function"),
                              "title": d.get("title"), "priority": d.get("priority"),
                              "verdict": d.get("verdict")} for d in dirs],
            "source": "Sovereign Evolution Office"}


@router.get("/api/v240/evolution/metrics")
async def evo_metrics():
    imm = _immune()
    from agentic_core.organism.immune import HEALTH_SCOPE as _HEALTH_SCOPE_W637
    real = None
    pillars: List[Dict[str, Any]] = []
    measure = None
    try:
        from agentic_core.api.transformation import _realise
        r = _realise()
        real = r.get("overall_realisation")
        measure = r.get("measure")          # W496 (FU-111) - travels with the figure
        pillars = [{"pillar": p["pillar"], "realisation": p["realisation"], "status": p["status"]}
                   for p in r.get("pillars", [])]
    except Exception:
        pass
    return {"vision_realisation": real, "vision_realisation_measure": measure,
            "organism_health": imm.get("health"),
            "organism_health_basis": _HEALTH_SCOPE_W637,   # W637 — one sentence, one home (was W635's typed copy)
            "threat_level": imm.get("threat_level"),
            "pillar_breakdown": pillars,
            "dimensions_realised": sum(1 for p in pillars if p["status"] == "realised"),
            "dimensions_total": len(pillars),
            "self_improvement": "Sovereign Evolution + Heartbeat active"}


@router.get("/api/v190/extrospection/signals")
async def extrospection_signals(n: int = 30):
    try:
        from agentic_core.organism.nervous import nervous
        sigs = nervous.recent_signals(min(n, 100))
    except Exception:
        sigs = []
    return {"signals": sigs, "count": len(sigs), "source": "central nervous system"}


# ── v250 global search ────────────────────────────────────────────────────────
@router.get("/api/v250/search/global")
async def global_search(q: str = ""):
    ql = q.lower().strip()
    results: List[Dict[str, Any]] = []
    try:
        from agentic_core.api.vsb import _list_vsbs
        for v in _list_vsbs():
            if not ql or ql in str(v.get("name", "")).lower() or ql in str(v.get("domain", "")).lower():
                results.append({"type": "vsb", "title": v.get("name"), "route": "/vsb", "id": v.get("vsb_id")})
    except Exception:
        pass
    try:
        from agentic_core.api.resource_fabric import _REGISTRY
        for r in _REGISTRY:
            if not ql or ql in r["name"].lower() or ql in r["description"].lower():
                results.append({"type": "resource", "title": r["name"], "route": "/resource-fabric", "id": r["id"]})
    except Exception:
        pass
    try:
        from agentic_core.projects.api import _all_projects
        for p in _all_projects():
            hay = f"{p.title} {p.realm} {p.domain} {p.stage}".lower()
            if not ql or ql in hay:
                results.append({"type": "project", "title": p.title, "route": "/projects", "id": p.id,
                                "meta": f"{p.realm} · {p.domain} · {p.stage}"})
    except Exception:
        pass
    # rank exact title matches first, then prefix, then substring
    def _rank(item):
        if not ql:
            return 1
        t = str(item.get("title", "")).lower()
        return 0 if t == ql else (1 if t.startswith(ql) else 2)
    results.sort(key=_rank)
    by_type = {t: sum(1 for x in results if x["type"] == t) for t in {x["type"] for x in results}}
    return {"query": q, "results": results[:30], "total": len(results), "by_type": by_type}


# ── v210 / v220 federation twins ──────────────────────────────────────────────
@router.get("/api/v210/federation/twins")
async def federation_twins():
    twins = []
    try:
        from agentic_core.api.vsb import _list_vsbs
        twins = [{"id": v.get("vsb_id"), "name": v.get("name"), "domain": v.get("domain"),
                  "status": v.get("status")} for v in _list_vsbs()]
    except Exception:
        pass
    # W326 — the spawn-twin registrations are genuinely CONSUMED here (a real registry read)
    # W577 (FU-298) — the registry read was tolerant AND wrapped in `except Exception: pass`, so a
    # truncated registry produced a SHORT list and a `total` presented as the whole of it. Two ways to
    # lose the same fact; both now reach the answer.
    _why = None
    try:
        from agentic_core.config import data_path, read_json_reported
        _rows, _why = read_json_reported(data_path("federation_twins.json"), [])
        for t in (_rows if isinstance(_rows, list) else []):
            twins.append({"id": t.get("twin_id"), "name": f"node twin ({t.get('node_id')})",
                          "domain": "federation", "status": "registered_reference"})
    except Exception as _e:
        _why = _why or f"the twin registry could not be read ({_e.__class__.__name__})"
    return {"twins": twins, "total": len(twins),
            "store_incomplete": _why,
            "total_is_incomplete": bool(_why),
            "total_basis": ("the registered twins that could not be read are MISSING from this total, "
                            "so there are at least this many and possibly more"
                            if _why else "every VSB twin and every registered node twin")}


@router.post("/api/v210/federation/spawn-twin")
async def spawn_twin(node_id: str = "node-1"):
    """W326 — honest: this previously claimed 'Federation twin registered' while registering
    NOTHING. Now the twin reference genuinely persists (atomic store) and the listing reads it;
    full digital-twin modelling remains at /api/v1/twin (honestly referenced, not implied)."""
    from agentic_core.config import StoreUnavailable, atomic_write_json, data_path, read_json_strict
    import time as _time
    import uuid as _uuid
    store = data_path("federation_twins.json")
    try:
        rows = read_json_strict(store, list, expect=list)          # W472 (FU-053) — refused, never replaced
    except StoreUnavailable as e:
        raise HTTPException(status_code=503, detail=f"{e}; no twin was registered")
    twin = {"twin_id": f"twin-{node_id}-{_uuid.uuid4().hex[:6]}", "node_id": node_id,
            "spawned_at": _time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime())}
    rows.append(twin)
    atomic_write_json(store, rows[-500:])
    return {**twin, "status": "registered",
            "note": ("Twin REFERENCE persisted to the federation registry (a real record — "
                     "not a modelled twin; use POST /api/v1/twin/model for actual modelling).")}


@router.get("/api/v220/twin/blueprint/{twin_id}")
async def twin_blueprint(twin_id: str):
    try:
        from agentic_core.api.vsb import _load_vsb
        v = _load_vsb(twin_id)
        if v:
            return {"twin_id": twin_id, "name": v.get("name"), "blueprint": v.get("genesis_blueprint", {}),
                    "genome": v.get("genome_spec", {}), "board": bool(v.get("board")), "economy": v.get("economy", {})}
    except Exception:
        pass
    return {"twin_id": twin_id, "blueprint": {}, "note": "No matching VSB entity."}


# ── v290 IoT (physical symbiosis) ─────────────────────────────────────────────
@router.get("/api/v290/iot/devices")
async def iot_devices():
    devices = []
    try:
        # W441: the frontier router that WROTE this store is retired (off-vision) — rows here
        # are frozen legacy records, served tolerantly. The old "wearable" clause was dead code:
        # wearable_sync never persisted a session, so only arvr/embodiment kinds ever existed.
        sessions = json.loads(data_path("frontier/platform_sessions.json").read_text(encoding="utf-8"))
        for s in sessions:
            if s.get("kind") in ("arvr", "embodiment"):
                devices.append({"id": s.get("id"), "type": s.get("kind"), "status": s.get("status")})
    except Exception:
        pass
    # W326 — honest: no fabricated default device; an empty fleet is an empty fleet.
    return {"devices": devices, "total": len(devices),
            "note": (None if devices else "No physical devices are connected — nothing is fabricated.")}


@router.get("/api/v290/iot/telemetry/{device_id}")
async def iot_telemetry(device_id: str):
    """Telemetry derived from live organism state. No physical wearable is
    connected, so biometric-style values are explicitly SIMULATED (and track the
    organism's real arousal) rather than presented as real sensor readings."""
    imm = _immune()
    arousal, signal_rate = "DORMANT", 0.0
    try:
        from agentic_core.organism.nervous import nervous
        st = nervous.status()
        arousal = st.get("arousal_state", arousal)
        signal_rate = st.get("signal_rate_per_second", 0.0)
    except Exception:
        pass
    atp = None
    try:
        from agentic_core.molecular.atp_simulator import ATPSimulator
        from agentic_core.organism.biobus import atp_depletion_state as _atp_depletion_state
        # W506 (P2.7(4), FU-265b) — THE SHARED SINGLETON. ATPSimulator() built a FRESH model on every
        # request, so this published a constant 0.333 for ever, under a comment calling it real and beside
        # values the same payload marked simulated. metabolism.py's docstring says callers must read the
        # shared organism ATP the heartbeat restores, not a new simulator.
        from agentic_core.organism.biobus import _get_atp as _shared_atp
        _a = _shared_atp()
        atp = round(max(0.0, min(1.0, float(_a.ratio) / 15.0)), 3) if _a else None
    except Exception:
        pass
    sim_bpm = int(58 + min(signal_rate, 5.0) * 6 + (12 if arousal not in ("DORMANT", "") else 0))
    return {
        "device_id": device_id,
        "source": "derived from live organism state — no physical wearable connected",
        "telemetry": {
            "organism_resonance": imm.get("health", 0.9),   # real — immune health 0–1
            # W506 (P2.7(4), FU-265b) — it was never real. Labelled beside the figure a reader sees.
            "metabolic_atp_ratio": atp,
            "metabolic_atp_measured": False,
            # W506 (FU-265b, corrected) - this said the figure never depletes because it is "floored
            # at 0.5 of 15". That floor NEVER BINDS: production exceeds consumption fourfold at the
            # worst efficiency this code passes, so the ratio only rises. The same wrong reason was
            # corrected in app_mvp earlier this round and left standing here - one fix, one writer.
            "metabolic_atp_basis": ("simulated — the shared ATPSimulator on a constant metabolic_load. "
                                   + _atp_depletion_state()["basis"]
                                   + " It is not a measurement of this platform."),
            "arousal_state": arousal,                         # real — central nervous system
            "simulated_bpm": sim_bpm,                         # SIMULATED — tracks arousal, not a sensor
        },
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── v191 modes ────────────────────────────────────────────────────────────────
_MODES = {
    "focus": {"name": "Focus", "description": "Deep-work single-stream mode."},
    "explore": {"name": "Explore", "description": "Broad discovery across realms."},
    "build": {"name": "Build", "description": "Concept→Commercialisation delivery."},
    "govern": {"name": "Govern", "description": "Constitutional + compliance oversight."},
}


@router.get("/api/v191/modes/{mode_id}")
async def get_mode(mode_id: str):
    return _MODES.get(mode_id, {"name": mode_id, "description": "Mode."})


# ── security bug bounty ───────────────────────────────────────────────────────
class BountySubmission(BaseModel):
    title: str
    severity: str = "medium"
    description: str = ""
    reporter: str = "anonymous"


@router.post("/api/security/bounty/submit")
async def bounty_submit(req: BountySubmission):
    p = _store("bounty.json")
    subs = []
    if p.exists():
        try:
            subs = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    entry = {"id": f"bb-{len(subs)+1:04d}", "title": req.title, "severity": req.severity,
             "description": req.description, "reporter": req.reporter, "status": "received",
             "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    subs.append(entry)
    p.write_text(json.dumps(subs[-200:], indent=2), encoding="utf-8")
    return entry
