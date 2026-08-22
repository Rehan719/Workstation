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

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.vbs.registry import bms, qms, ems, dcms, backbone, CATALOGUE
from agentic_core.vbs.backbone import ProtocolType

router = APIRouter(prefix="/api/v1/vbs", tags=["vbs-living-systems"])


@router.get("/systems")
async def list_systems():
    """Catalogue of the OWNED VBS living systems, with an honest real-vs-simulated breakdown."""
    return {"posture": "in-house", "owned": True, "count": len(CATALOGUE), "systems": CATALOGUE,
            "integrated_into_ai": "QMS + DCMS govern the native workflow-tree synthesis"}


class QMSGate(BaseModel):
    coverage: float = 0.0
    stubs_found: bool = False


@router.post("/qms/gate")
async def qms_gate(req: QMSGate):
    """Run a real ISO-9001-aligned quality gate (>= min coverage AND zero stubs)."""
    passed = await qms.run_quality_gates({"coverage": req.coverage, "stubs_found": req.stubs_found})
    return {"passed": passed, "min_coverage": qms.min_coverage,
            "non_conformance_rate": qms.get_non_conformance_rate(), "real": True}


# ── §10 (W307) — the defect → correction → re-verify loop (ISO 9001 §8.7 / §10.2) ──

@router.get("/qms/defects")
async def qms_defects(status: str = ""):
    """Persistent, traceable QMS defects + the REAL non-conformance posture (failures / gates run)."""
    rows = qms.defects
    if status:
        rows = [d for d in rows if d.get("status") == status]
    return {"summary": qms.defect_summary(), "defects": rows[-100:][::-1], "real": True}


class DefectCorrection(BaseModel):
    correction: str
    actor: str = "owner"


@router.post("/qms/defects/{defect_id}/correct")
async def qms_correct_defect(defect_id: str, req: DefectCorrection):
    """Record the correction taken for an OPEN defect. Closure requires re-verification —
    a correction alone never closes a defect."""
    d = qms.correct_defect(defect_id, req.correction, req.actor)
    if not d:
        raise HTTPException(status_code=404, detail=f"No OPEN defect '{defect_id}'.")
    return {"defect": d, "next": "POST /qms/defects/{id}/reverify with the corrected delivery's real metrics"}


@router.post("/qms/defects/{defect_id}/reverify")
async def qms_reverify_defect(defect_id: str, req: QMSGate):
    """Re-run the SAME gate on the corrected delivery's REAL metrics: closes only on a genuine pass;
    a failed re-verification REOPENS the defect."""
    res = qms.reverify_defect(defect_id, {"coverage": req.coverage, "stubs_found": req.stubs_found})
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
    return {"qms_owns_dcms": qms.dcms is dcms, **qms.document_control_status(), "real": True}


class BMSEcon(BaseModel):
    insights_count: int = 1
    wh_consumed: float = 0.0


@router.post("/bms/economics")
async def bms_economics(req: BMSEcon):
    """Compute real unit economics (cost-per-insight, ROI). Energy $/Wh rate is a simulated constant."""
    econ = await bms.calculate_unit_economics(req.insights_count, req.wh_consumed)
    return {**econ, "unit_cost_target": bms.unit_cost_target,
            "real_arithmetic": True, "simulated": ["energy $/Wh rate constant"]}


class EMSEff(BaseModel):
    energy_wh: float = 0.0


@router.post("/ems/efficiency")
async def ems_efficiency(req: EMSEff):
    """Accrue real CO2 (kgCO2/Wh). Efficiency-gain + resource-gain are simulated constants."""
    eff = await ems.monitor_efficiency(req.energy_wh)
    return {"efficiency_gain": eff, "total_co2_kg": ems.total_co2_kg, "resource_gain": ems.get_resource_gain(),
            "real": ["co2 accumulation"], "simulated": ["efficiency-gain constant", "resource-gain constant"]}


@router.get("/backbone/health")
async def backbone_health():
    """Live Mycelial-backbone health (DID agent registry + failover). Transport latency is simulated."""
    return backbone.get_backbone_health()


class BackboneRegister(BaseModel):
    agent_id: str
    capabilities: list = []


@router.post("/backbone/register")
async def backbone_register(req: BackboneRegister):
    """Zero-trust DID registration of an agent into the mycelial backbone (real registry write)."""
    ok = await backbone.register_agent(req.agent_id, {"capabilities": req.capabilities})
    return {"registered": ok, "agent_id": req.agent_id, "active_nodes": len(backbone.registry),
            "protocols": [p.name for p in ProtocolType]}
