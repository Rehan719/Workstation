"""
VBS Living Systems API — Workstation's OWN deterministic management systems, exposed + integrated.

Surfaces the real VBS management systems (BMS / QMS / EMS / DCMS + the Mycelial backbone) as owned
in-house capabilities. Every operation is genuine computation (real arithmetic, real SHA3-512
versioning, real quality gates); placeholder constants are declared honestly via /vbs/systems and the
per-response `simulated` fields. The in-house AI fabric uses QMS + DCMS to govern its workflow-tree
output (see agentic_core/ai/native/orchestrator.orchestrate_tree).
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from agentic_core.auth.core import get_current_user, user_can_access
from agentic_core.vbs.registry import bms, qms, ems, dcms, backbone, CATALOGUE
from agentic_core.vbs.backbone import ProtocolType
from agentic_core.vbs.qms import LIVE_GATE_LABELS, label_is_live

router = APIRouter(prefix="/api/v1/vbs", tags=["vbs-living-systems"])


@router.get("/systems")
async def list_systems():
    """Catalogue of the OWNED VBS living systems, with an honest real-vs-simulated breakdown."""
    return {"posture": "in-house", "owned": True, "count": len(CATALOGUE), "systems": CATALOGUE,
            "integrated_into_ai": "QMS + DCMS govern the native workflow-tree synthesis"}


class QMSGate(BaseModel):
    # W440 refuter catch: coverage was unbounded — a percent-style 97 trivially PASSED the
    # "ISO-9001-aligned" gate (97 >= 0.95), converting failing deliveries into green chips
    coverage: float = Field(default=0.0, ge=0.0, le=1.0)
    stubs_found: bool = False


@router.post("/qms/gate")
async def qms_gate(req: QMSGate, user: dict | None = Depends(get_current_user)):
    """Run the quality gate's RULE (>= min coverage AND zero stubs) as a what-if over figures the caller types.
    Nothing is measured here: no delivery is read.

    W440 refuter catch: this route stamped no owner, so under auth a tenant's failed gate opened
    a platform-level defect THEY COULD NEVER SEE — while the summary counted it. The defect now
    belongs to the tenant that ran the gate."""
    _u = user if isinstance(user, dict) else None
    #  W678 (OWNER RULING 2026-10-12) - NO FIGURE, NO GATE. An empty body ran the rule at this route's defaults
    #  (coverage 0.0) and opened a what-if defect for figures nobody typed. Refused BEFORE anything is recorded.
    if not (getattr(req, "model_fields_set", None) or set()):
        raise HTTPException(status_code=422, detail=(
            "No figure was supplied, so no what-if gate was run and nothing was recorded. Send 'coverage' "
            "(0 to 1), 'stubs_found' (true or false), or both."))
    # W489 (sweep S9.4, C3) — this gate runs on metrics the CALLER TYPES (the panel defaults to 0.97,
    # which passes), so it is a what-if, not a delivery. It used to count into the platform-wide
    # non-conformance rate that the cockpit then labelled "a real rate".
    passed = await qms.run_quality_gates(
        {"coverage": req.coverage, "stubs_found": req.stubs_found},
        label="cockpit-what-if", owner_id=(_u or {}).get("username"), count_in_rate=False)
    #  ledger v17 (FU-936) - which of the two figures the caller actually sent. An empty body ran the rule at
    #  the model's defaults and the answer still spoke of "the figures you supplied".
    _sent936 = sorted(getattr(req, "model_fields_set", None) or [])
    _defaulted936 = sorted({"coverage", "stubs_found"} - set(_sent936))
    return {"passed": passed, "min_coverage": qms.min_coverage,
            "figures_supplied": _sent936, "figures_defaulted": _defaulted936,
            "figures_basis": (
                (f"typed by the caller: {', '.join(_sent936)}" if _sent936 else "the caller typed NO figure")
                + (f"; taken from this route's defaults, not from any delivery: {', '.join(_defaulted936)} "
                   f"(coverage {req.coverage}, stubs_found {req.stubs_found})" if _defaulted936 else "")),
            "counted_in_rate": False,
            "basis": ("a what-if gate over the coverage and stub figures you supplied — it is recorded "
                      "separately and does not move the platform non-conformance rate"),
            "non_conformance_rate": qms.get_non_conformance_rate(),
            # W534 (FU-298) — the rate is printed HERE, so the disclosure has to be here. get_non_conformance_rate
            # returns a bare float and a float cannot carry a reason, which is why this reads the summary's.
            **({k: qms.defect_summary()[k] for k in ("store_incomplete", "counts_are_incomplete")}
               if "store_incomplete" in qms.defect_summary() else {}),
            #  ledger v17 (FU-936) - this flag answered the opposite of what the re-verify route below defines:
            #  there, a gate run on typed figures is NOT real and NOT measured. One definition, both routes.
            "real": False, "measured": False,
            "real_basis": ("NOT measured here: the gate's rule was run on a coverage figure and a stub flag "
                           "that were typed into the request (or defaulted), not read from a delivery. It is a "
                           "what-if and is not counted in the non-conformance rate")}


# ── §10 (W307) — the defect → correction → re-verify loop (ISO 9001 §8.7 / §10.2) ──

@router.get("/qms/defects")
async def qms_defects(status: str = "", user: dict | None = Depends(get_current_user)):
    """Persistent, traceable QMS defects + the REAL non-conformance posture (failures / gates run).
    §14 (W320): under auth the listing is tenant-scoped — a user sees their OWN defects; unowned
    (platform-level) defects are admin-only; single-user mode unchanged."""
    _u = user if isinstance(user, dict) else None
    rows = [d for d in qms.defects if user_can_access(_u, d.get("owner_id"))]
    if status:
        rows = [d for d in rows if d.get("status") == status]
    _sum = qms.defect_summary()
    # W534 (FU-298) — a truncated store yields FEWER defect rows, so the list is short for a reason the
    # reader cannot see from its length. The reason is lifted beside the rows, not left inside the summary
    # only, because a caller rendering the list may never look at the summary.
    #  W853 (FU-1038) - each row says whether its label is one a live surface still opens defects under
    return {"summary": _sum,
            "defects": [{**d, "label_live": label_is_live(d.get("label"))} for d in rows[-100:][::-1]],
            **({"store_incomplete": _sum["store_incomplete"], "listing_is_incomplete": True}
               if _sum.get("store_incomplete") else {}),
            "real": True}


def _require_defect_access(defect_id: str, user: dict | None) -> None:
    """§14 (W320) — defect mutations are owner-scoped: 404 (never 403) when scoped out; unowned
    defects are admin-only under auth; auth-off unguarded."""
    _u = user if isinstance(user, dict) else None
    for d in qms.defects:
        if d.get("id") == defect_id:
            if not user_can_access(_u, d.get("owner_id")):
                raise HTTPException(status_code=404, detail=f"No defect '{defect_id}'.")
            return


class DefectCorrection(BaseModel):
    correction: str
    actor: str = "owner"


@router.post("/qms/defects/{defect_id}/correct")
async def qms_correct_defect(defect_id: str, req: DefectCorrection,
                             user: dict | None = Depends(get_current_user)):
    """Record the correction taken for an OPEN defect. Closure requires re-verification —
    a correction alone never closes a defect."""
    _require_defect_access(defect_id, user)
    d = qms.correct_defect(defect_id, req.correction, req.actor)
    if not d:
        raise HTTPException(status_code=404, detail=f"No OPEN defect '{defect_id}'.")
    return {"defect": d, "next": "POST /qms/defects/{id}/reverify with the corrected delivery's real metrics"}


class DefectReverify(BaseModel):
    coverage: float | None = Field(default=None, ge=0.0, le=1.0)   # caller-attested (recorded as such)
    stubs_found: bool = False
    content: str | None = None         # §10 (W316) — the corrected delivery ITSELF: measured here


@router.post("/qms/defects/{defect_id}/reverify")
async def qms_reverify_defect(defect_id: str, req: DefectReverify,
                              user: dict | None = Depends(get_current_user)):
    """Re-run the SAME gate on the corrected delivery: closes only on a genuine pass; a failed
    re-verification REOPENS the defect (and counts as a gate failure — W316). Pass `content` to
    have the platform MEASURE the corrected delivery with the same instruments as the original
    gate (against the defect's stored delivery reference); bare caller-typed metrics are still
    accepted but honestly recorded as `caller_attested`."""
    _require_defect_access(defect_id, user)
    if req.content is not None:
        target = next((d for d in qms.defects if d.get("id") == defect_id), None)
        if not target:
            raise HTTPException(status_code=404, detail=f"No defect '{defect_id}'.")
        from agentic_core.vbs.quality import _delivery_coverage, _STUB_RE, _MIN_SUBSTANTIVE
        secs = ((target.get("delivery_ref") or {}).get("required_sections")) or None
        if not secs:
            # §10 (W497, FU-201, class C1) — "RE-RUN THE SAME GATE" CANNOT BE DONE when the gate's own
            # criteria were never stored. This path used to close the defect on a coverage of 1.0 that
            # the length check produced, so 220 characters of "x x x" closed a defect whose correction
            # said "nothing was actually corrected" — and the panel reported it as a measured gate pass.
            raise HTTPException(status_code=409, detail=(
                f"'{defect_id}' records no required sections, so the gate that opened it cannot be "
                f"re-run on content: there is nothing to measure coverage against, and a length check "
                f"is not that gate. Re-verify with explicit `coverage` (recorded as caller_attested), "
                f"or open the defect through a gate that stores the delivery's structure."))
        cov = _delivery_coverage(req.content, secs)
        stub = (bool(_STUB_RE.search(req.content or ""))
                or len((req.content or "").strip()) < _MIN_SUBSTANTIVE)
        # W440 refuter catch: with no stored section requirements the coverage instrument
        # degenerates to length+stub checks — the basis must say which instruments actually ran,
        # or "measured" overclaims for exactly the defects the cockpit gate runner creates
        res = qms.reverify_defect(defect_id, {"coverage": cov, "stubs_found": stub,
                                              "basis": ("measured_from_content" if secs else
                                                        "measured_from_content (no stored section "
                                                        "requirements — length + stub instruments only)")})
    else:
        if req.coverage is None:
            raise HTTPException(status_code=422,
                                detail="Provide `content` (measured re-verify) or `coverage`.")
        res = qms.reverify_defect(defect_id, {"coverage": req.coverage,
                                              "stubs_found": req.stubs_found,
                                              "basis": "caller_attested"})
    if not res:
        raise HTTPException(status_code=404, detail=f"No CORRECTED defect '{defect_id}' awaiting re-verification.")
    #  T2B (row 2) - `real` WAS TRUE ON EVERY ANSWER, including a re-verification run on a coverage figure
    #  the caller typed - which the QMS itself records as caller_attested and, since P3.30, counts apart.
    #  It is now read from the basis the defect records. `measured` and `real_basis` are added; the basis is
    #  also lifted to the top level, where the panel already looks for it first.
    _d_t2b = res.get("defect") or {}
    _basis_t2b = str(_d_t2b.get("reverify_basis") or "")
    _measured_t2b = _basis_t2b.startswith("measured_from_content")
    return {**res, "real": _measured_t2b, "measured": _measured_t2b, "reverify_basis": _basis_t2b,
            "real_basis": (
                (f"MEASURED here: the corrected delivery's own content was run through the gate's "
                 f"instruments ({_basis_t2b})") if _measured_t2b else
                (f"NOT measured here: the gate was run on a coverage figure the caller typed "
                 f"({_basis_t2b or 'no basis recorded'}), so `real` is false. "
                 + ("The defect is a what-if, so this gate is outside the non-conformance rate and outside "
                    "the count of attested re-verifications in it." if _d_t2b.get("what_if") else
                    "By ruling it stays in the non-conformance rate, and it is counted in "
                    "`attested_reverifications` beside that rate.")))}


# ── W853 (FU-1038; OWNER RULING 2026-10-12) - the two ways out of the loop that are not a re-verification ──

class DefectRetired(BaseModel):
    reason: str = Field(min_length=12, max_length=2000)
    actor: str = "owner"                      # with sign-in off: typed, and recorded as unverified
    retired_route: str | None = None          # the route it came through; needed when its label is still in use


class DefectNotReproducible(BaseModel):
    tried: str = Field(min_length=12, max_length=2000)   # what was done to reproduce it
    actor: str = "owner"


def _disposer(actor: str, user: dict | None) -> tuple[str, bool]:
    """Who takes a defect out of the loop: the signed-in user; with sign-in off, the typed name, unverified."""
    _u = user if isinstance(user, dict) else None
    if _u and _u.get("username"):
        return str(_u["username"]), True
    return (str(actor or "").strip() or "owner"), False


def _api_route_mounted(app: Any, path: str) -> bool:
    for r in getattr(app, "routes", []) or []:
        rx = getattr(r, "path_regex", None)
        if rx is not None and str(getattr(r, "path", "")).startswith("/api/") and rx.match(path):
            return True
    return False


@router.post("/qms/defects/{defect_id}/close-source-retired")
async def qms_close_source_retired(defect_id: str, req: DefectRetired, request: Request,
                                   user: dict | None = Depends(get_current_user)):
    """Close an open or corrected defect because the surface that opened it has been retired, with the reason. Not a
    re-verification: nothing in the rate moves. A defect whose label a live surface still uses closes this way only
    when the route it came through is named and is not a route this platform mounts."""
    _require_defect_access(defect_id, user)
    target = next((d for d in qms.defects if d.get("id") == defect_id), None)
    if not target or target.get("status") not in ("open", "corrected"):
        raise HTTPException(status_code=404, detail=f"No OPEN or CORRECTED defect '{defect_id}'.")
    label = str(target.get("label") or "")
    live = label_is_live(label)
    route = (req.retired_route or "").split("?")[0].strip() or None
    if route is not None and not route.startswith("/api/"):
        raise HTTPException(status_code=422, detail=(
            "retired_route is the path the defect came through, starting /api/ - it is checked against the routes "
            "this platform mounts"))
    if route is not None and _api_route_mounted(request.app, route):
        raise HTTPException(status_code=409, detail=(
            f"'{route}' is mounted on this platform: the surface is live, so the defect is not closed as retired. "
            f"Correct and re-verify it, or report it not reproducible with what was tried."))
    if live is not False and route is None:
        raise HTTPException(status_code=409, detail=(
            (f"'{label}' is a label a live surface still opens defects under" if live else
             f"'{label}' is composed at run time, so whether its surface is live cannot be read from it")
            + ": name the route it came through (retired_route), which is checked against the routes this platform "
              "mounts, or correct and re-verify it, or report it not reproducible."))
    _fixed = f"the {len(LIVE_GATE_LABELS)} fixed labels live surfaces open a defect under"
    check = "; ".join(s for s in (
        (f"checked: '{route}' is not a route this platform mounts" if route else ""),
        (f"checked: '{label}' is not among {_fixed}" if live is False else
         f"its label '{label}' is " + ("still used by a live surface" if live else "composed at run time")
         + ", so the route is what was checked")) if s)
    by, verified = _disposer(req.actor, user)
    d = qms.dispose_defect(defect_id, "closed_source_retired", req.reason, by, verified,
                           source_check=check, retired_route=route)
    if not d:
        raise HTTPException(status_code=404, detail=f"No OPEN or CORRECTED defect '{defect_id}'.")
    return {"defect": d, "source_check": check, "measured": False, "counted_in_rate": False,
            "basis": d["closure"]["basis"]}


@router.post("/qms/defects/{defect_id}/not-reproducible")
async def qms_not_reproducible(defect_id: str, req: DefectNotReproducible,
                               user: dict | None = Depends(get_current_user)):
    """Report an open or corrected defect as not reproducible, with what was tried. Not a re-verification: nothing in
    the rate moves, and the row keeps who reported it and when."""
    _require_defect_access(defect_id, user)
    by, verified = _disposer(req.actor, user)
    d = qms.dispose_defect(defect_id, "not_reproducible", req.tried, by, verified)
    if not d:
        raise HTTPException(status_code=404, detail=f"No OPEN or CORRECTED defect '{defect_id}'.")
    return {"defect": d, "measured": False, "counted_in_rate": False, "basis": d["closure"]["basis"]}


class DCMSCommit(BaseModel):
    artifact_id: str
    content: Dict[str, Any] = {}
    actor: str = "chief"


@router.post("/dcms/commit")
async def dcms_commit(req: DCMSCommit):
    """Commit + version an artifact with real SHA3-512 cryptographic hashing + an audit trail."""
    h = await dcms.commit_artifact(req.artifact_id, req.content, req.actor)
    versions = dcms.registry.get(req.artifact_id, [])
    return {"hash": h, "algo": "sha3_512", "version": len(versions),
            "audit_integrity": dcms.get_audit_integrity(), "real": True}


@router.get("/qms/document-control")
async def qms_document_control():
    """The QMS OWNS the DCMS (ISO 9001 §7.5): document control is a function of the QMS. This exposes the
    QMS's document-control posture — proving the DCMS is operated as the QMS's subsystem."""
    return {"qms_owns_dcms": qms.dcms is dcms, **qms.document_control_status(), "real": True,
            "note": ("registered_artifacts and audit_integrity are PERSISTENT (dcms store); "
                     "controlled_documents is a per-process counter since start")}


class BMSEcon(BaseModel):
    # W440 refuter catch: negative energy produced cost_per_insight -0.00075 with status
    # EFFICIENT and a roi_basis claiming "no energy cost recorded" when a (negative) figure WAS
    # recorded; zero insights yielded a per-insight figure with no units to divide over
    insights_count: int = Field(default=1, ge=1)
    wh_consumed: float = Field(default=0.0, ge=0.0)


@router.post("/bms/economics")
async def bms_economics(req: BMSEcon):
    """Compute real unit economics (cost-per-insight, ROI). Energy $/Wh rate is a simulated constant."""
    econ = await bms.calculate_unit_economics(req.insights_count, req.wh_consumed)
    return {**econ, "unit_cost_target": bms.unit_cost_target,
            "real_arithmetic": True,
            # W440 — the ROI's $0.50/insight value constant was undisclosed here
            "simulated": ["energy $/Wh rate constant", "insight $0.50 value constant (inside ROI)"]}


class EMSEff(BaseModel):
    # W440 refuter catch: one negative request drove the SHARED singleton's total_co2_kg below
    # zero — corrupting the platform-wide figure every viewer sees
    energy_wh: float = Field(default=0.0, ge=0.0)


@router.post("/ems/efficiency")
async def ems_efficiency(req: EMSEff):
    """Accrue real CO2 (kgCO2/Wh). Efficiency-gain + resource-gain are simulated constants."""
    eff = await ems.monitor_efficiency(req.energy_wh)
    return {"efficiency_gain": eff, "total_co2_kg": ems.total_co2_kg, "resource_gain": ems.get_resource_gain(),
            "real": ["co2 accumulation"], "simulated": ["efficiency-gain constant", "resource-gain constant"],
            "scope": "co2 accrues in-memory, this server process since start"}


@router.get("/backbone/health")
async def backbone_health():
    """Live Mycelial-backbone health (DID agent registry + failover). Transport latency is simulated."""
    return backbone.get_backbone_health()


class BackboneRegister(BaseModel):
    agent_id: str = Field(min_length=1, max_length=128)
    capabilities: list = Field(default_factory=list, max_length=50)


@router.post("/backbone/register")
async def backbone_register(req: BackboneRegister):
    """DID-labelled registration into the in-memory backbone registry (real registry write).

    W440 refuter catch: "zero-trust" was advertising — no authentication is performed and nothing
    verifies the caller or the DID; the label is minted here. Re-registration replaces the
    existing card, disclosed."""
    replaced = req.agent_id in backbone.registry
    ok = await backbone.register_agent(req.agent_id, {"capabilities": req.capabilities})
    return {"registered": ok, "agent_id": req.agent_id, "replaced_existing": replaced,
            "active_nodes": len(backbone.registry),
            "auth_note": "no authentication is performed on registration — the DID is a minted label",
            "protocols": [p.name for p in ProtocolType]}
