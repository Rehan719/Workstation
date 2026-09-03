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

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agentic_core.auth.core import get_current_user, user_can_access
from agentic_core.vbs.registry import bms, qms, ems, dcms, backbone, CATALOGUE
from agentic_core.vbs.backbone import ProtocolType

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
    """Run a real ISO-9001-aligned quality gate (>= min coverage AND zero stubs).

    W440 refuter catch: this route stamped no owner, so under auth a tenant's failed gate opened
    a platform-level defect THEY COULD NEVER SEE — while the summary counted it. The defect now
    belongs to the tenant that ran the gate."""
    _u = user if isinstance(user, dict) else None
    passed = await qms.run_quality_gates(
        {"coverage": req.coverage, "stubs_found": req.stubs_found},
        label="cockpit-gate", owner_id=(_u or {}).get("username"))
    return {"passed": passed, "min_coverage": qms.min_coverage,
            "non_conformance_rate": qms.get_non_conformance_rate(), "real": True}


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
    return {"summary": qms.defect_summary(), "defects": rows[-100:][::-1], "real": True}


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
    return {**res, "real": True}


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
