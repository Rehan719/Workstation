"""
Management Systems API — QMS, BMS, DCS, EMS for VSB entities.

Drafts management-system documentation and governance tools that can be attached to any VSB entity
or project. W488 (sweep S2.4, C5) — this said "AI-generated", and on a deployment where the
deterministic floor serves every generator that is not what comes back: the floor composes the
requested headings and the response's own floor_note says "it is not model analysis. Review every
clause before use." What a caller gets is named by that response, never by this docstring.

  POST /api/v1/mgmt/qms/generate     — generate QMS framework (ISO 9001-aligned)
  POST /api/v1/mgmt/bms/generate     — generate BMS with OKRs and Balanced Scorecard
  POST /api/v1/mgmt/dcs/generate     — generate Document Control System framework
  POST /api/v1/mgmt/audit/schedule   — generate internal audit schedule
  POST /api/v1/mgmt/risk-register    — generate organisational risk register
  GET  /api/v1/mgmt/standards        — list supported management standards
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text, person_said
from agentic_core.auth.core import get_current_user
from agentic_core.organism.biobus import biobus


async def _compose(prompt: str, agent: str, said: str | None = None):
    """W475 (ledger v4 R1.2) — a generated document is composed WITHOUT memory recall (the QMS for one organisation
    carried another's recalled interaction as its 'salient terms') and carries its provenance; on the native floor
    the response says the frame is not model analysis."""
    #  W640 - `said` is what the person typed for this document; each generator names its fields
    text, prov = await ai_text(prompt, agent, augment=False, user_text=(said or None))
    prov = dict(prov or {})
    if (prov.get("served_by") or "native") == "native":
        #  W640 - "from your inputs" is said only when the generator told the floor what they were
        prov["floor_note"] = (("structured floor — the owned fabric composed this frame from the inputs you "
                               "typed; it is not model analysis. Review every clause before use.") if said else
                              ("structured floor — a generic frame: this generator did not tell the floor "
                               "which inputs were yours, so nothing in it is drawn from them. It is not "
                               "model analysis. Review every clause before use."))
    # (refutation) the delivery is recorded by the living QMS like every other generated document; on the floor it is
    # 'not assessable', never a pass
    try:
        from agentic_core.vbs.quality import assure_delivery
        qa = await assure_delivery(text, None, label=agent, served_by=prov.get("served_by"))
        prov["quality"] = (qa or {}).get("quality")
    except Exception as exc:
        prov["quality"] = {"qms_gate_passed": None,
                           "qms_basis": f"no quality record was produced ({exc.__class__.__name__})"}
    return text, prov

router = APIRouter(prefix="/api/v1/mgmt", tags=["management-systems"])

#  OWNER RULING 2026-10-12 - A STANDARD IS NAMED WITHOUT AN EDITION. The list named editions typed years ago;
#  two of them their publisher has since replaced. An edition is a fact with a date: it belongs to the register
#  of sources, read at the publisher's page, and is never typed here. A level or a grade of attainment is not
#  a standard's name: the list named a maturity level and a certification grade as if either were held.
STANDARD_NOTE = ("A generated outline to complete and review - not a conformity assessment, and not a statement "
                 "that anything is aligned to, compliant with or certified against a standard. This platform holds "
                 "no standard's text; check the current edition at its publisher.")
EDITIONS_READ = {"read_on": "2026-10-12", "read_by": "round W676, in a browser at the publisher's pages",
                 "says": "the publisher lists 2026 editions of its quality and environmental management standards as current"}
_STANDARDS = [
    {"id": "iso9001", "name": "ISO 9001", "type": "QMS", "description": "Quality Management Systems"},
    {"id": "iso14001", "name": "ISO 14001", "type": "EMS", "description": "Environmental Management Systems"},
    {"id": "iso27001", "name": "ISO/IEC 27001", "type": "ISMS", "description": "Information Security Management"},
    {"id": "iso45001", "name": "ISO 45001", "type": "OH&S", "description": "Occupational Health and Safety"},
    {"id": "bsc", "name": "Balanced Scorecard", "type": "BMS", "description": "Strategic performance management"},
    {"id": "okr", "name": "OKRs", "type": "BMS", "description": "Objectives and Key Results framework"},
    {"id": "cmmi", "name": "CMMI", "type": "Process", "description": "Capability Maturity Model Integration"},
    {"id": "gdpr", "name": "UK GDPR / GDPR", "type": "Compliance", "description": "Data protection compliance framework"},
    {"id": "cyber_essentials", "name": "Cyber Essentials", "type": "Security", "description": "UK government cybersecurity scheme"},
]


@router.get("/standards")
async def list_standards():
    return {"standards": _STANDARDS, "total": len(_STANDARDS), "note": STANDARD_NOTE, "editions": EDITIONS_READ}


class QMSRequest(BaseModel):
    organisation_name: str
    domain: str = "general"
    products_services: str = ""
    size: str = "small"  # micro | small | medium | large
    existing_certifications: list[str] = []


@router.post("/qms/generate")
async def generate_qms(req: QMSRequest):
    """Generate a complete ISO 9001-aligned Quality Management System framework."""
    prompt = (
        f"Draft a QMS framework outline.\n\n"
        f"Organisation: {req.organisation_name}\n"
        f"Domain: {req.domain}\n"
        f"Size: {req.size}\n"
        + (f"Products/Services: {req.products_services}\n" if req.products_services else "")
        + (f"Existing certifications: {', '.join(req.existing_certifications)}\n" if req.existing_certifications else "")
        + "\nDraft an outline of a quality management system under these headings (name no edition of any "
          "standard and claim no alignment, compliance or certification):\n"
        "## 1. Quality Policy Statement\n"
        "## 2. Quality Objectives (5 SMART objectives with KPIs)\n"
        "## 3. Process Map (key processes with SIPOC for top 3)\n"
        "## 4. Document Control Procedure\n"
        "## 5. Non-Conformance and CAPA Procedure\n"
        "## 6. Internal Audit Programme (annual schedule)\n"
        "## 7. Management Review Agenda Template\n"
        "## 8. Customer Satisfaction Measurement Approach\n"
        "## 9. Supplier Evaluation Criteria\n"
        "## 10. Continual Improvement Log Template\n"
        "## 11. Certification Readiness Checklist\n\n"
        "Tailor everything specifically to a {size}-sized {domain} organisation. "
        "Be practical and immediately usable."
    )

    biobus.fire_signal("sensory", "mgmt.qms", f"QMS generation: {req.organisation_name}", 0.5)
    framework, _prov = await _compose(prompt, "mgmt_qms", said=person_said(req.organisation_name, req.products_services))
    biobus.record_operation("qms_generate", "mgmt.qms", success=True, payload=f"{req.organisation_name} QMS")

    return {
        "ai_provenance": _prov,
        "doc_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "standard": "ISO 9001",
        "standard_note": STANDARD_NOTE,
        "editions": EDITIONS_READ,
        "framework": (framework or "") + "\n\n_" + STANDARD_NOTE + "_",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class BMSRequest(BaseModel):
    organisation_name: str
    mission: str
    domain: str = "general"
    planning_horizon: str = "annual"  # quarterly | annual | 3-year


@router.post("/bms/generate")
async def generate_bms(req: BMSRequest):
    """Generate a Business Management System with Balanced Scorecard and OKRs."""
    prompt = (
        f"Draft a Business Management System outline.\n\n"
        f"Organisation: {req.organisation_name}\n"
        f"Mission: {req.mission}\n"
        f"Domain: {req.domain}\n"
        f"Planning horizon: {req.planning_horizon}\n\n"
        "Deliver:\n"
        "## Strategic Vision and Mission Alignment\n"
        "## Balanced Scorecard\n"
        "   - Financial Perspective (3 objectives, KPIs, targets)\n"
        "   - Customer Perspective (3 objectives, KPIs, targets)\n"
        "   - Internal Process Perspective (3 objectives, KPIs, targets)\n"
        "   - Learning & Growth Perspective (3 objectives, KPIs, targets)\n"
        "## OKR Framework (3 Objectives, 3 Key Results each)\n"
        "## Strategy Map (cause-and-effect diagram — described textually)\n"
        "## Performance Review Cadence (daily/weekly/monthly/quarterly rhythms)\n"
        "## Dashboard Metrics (top 10 metrics to display)\n"
        "## Decision Rights Matrix (RACI for strategic decisions)\n"
    )

    biobus.fire_signal("sensory", "mgmt.bms", f"BMS generation: {req.organisation_name}", 0.5)
    framework, _prov = await _compose(prompt, "mgmt_bms", said=person_said(req.organisation_name, req.mission))
    biobus.record_operation("bms_generate", "mgmt.bms", success=True, payload=f"{req.organisation_name} BMS")

    return {
        "ai_provenance": _prov,
        "doc_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "framework_type": "BMS",
        "framework": framework,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class DCSRequest(BaseModel):
    organisation_name: str
    domain: str = "general"
    document_types: list[str] = []


@router.post("/dcs/generate")
async def generate_dcs(req: DCSRequest):
    """Generate a Document Control System framework."""
    doc_types = req.document_types or ["policies", "procedures", "work instructions", "records", "forms"]

    prompt = (
        f"Draft a document control system outline for:\n\n"
        f"Organisation: {req.organisation_name}\nDomain: {req.domain}\n"
        f"Document types: {', '.join(doc_types)}\n\n"
        "Deliver:\n"
        "## Document Taxonomy and Hierarchy\n"
        "## Naming Convention Standard (with examples)\n"
        "## Version Control Protocol (major/minor versioning, revision history)\n"
        "## Approval Workflow (draft → review → approve → release)\n"
        "## Document Register Template (fields: ID, title, type, owner, version, review date, status)\n"
        "## Controlled Copy Distribution Protocol\n"
        "## Retention and Disposal Schedule\n"
        "## Change Control Process\n"
        "## Obsolescence Management\n"
        "## Digital DCS Tool Recommendations\n"
    )

    biobus.fire_signal("sensory", "mgmt.dcs", f"DCS generation: {req.organisation_name}", 0.4)
    framework, _prov = await _compose(prompt, "mgmt_dcs", said=person_said(req.organisation_name, req.document_types))
    biobus.record_operation("dcs_generate", "mgmt.dcs", success=True, payload=f"{req.organisation_name} DCS")

    return {
        "ai_provenance": _prov,
        "doc_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "framework_type": "DCS",
        "framework": framework,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class AuditScheduleRequest(BaseModel):
    organisation_name: str
    processes: list[str] = []
    audit_standard: str = "ISO 9001"
    year: int = 2026


@router.post("/audit/schedule")
async def generate_audit_schedule(req: AuditScheduleRequest):
    """Generate a risk-based internal audit programme."""
    processes = req.processes or ["Sales", "Operations", "Finance", "HR", "IT", "Quality"]

    prompt = (
        f"Draft a risk-based internal audit programme.\n\n"
        f"Organisation: {req.organisation_name}\n"
        f"Standard: {req.audit_standard}\nYear: {req.year}\n"
        f"Processes to audit: {', '.join(processes)}\n\n"
        "Provide:\n"
        "## Risk Assessment Matrix (table: Process | Risk Level | Audit Frequency | Rationale)\n"
        "## Annual Audit Schedule (month-by-month: process | auditor role | scope | days required)\n"
        "## Audit Methodology (document review, interviews, process observation)\n"
        "## Audit Report Template (structure for findings and recommendations)\n"
        "## Non-Conformance Tracking Process\n"
        "## Auditor Competency Requirements\n"
        "## Management Review Input from Audits\n"
    )

    biobus.fire_signal("sensory", "mgmt.audit", f"Audit schedule: {req.organisation_name}", 0.4)
    schedule, _prov = await _compose(prompt, "mgmt_audit", said=person_said(req.organisation_name, req.processes))
    biobus.record_operation("audit_schedule", "mgmt.audit", success=True)

    return {
        "ai_provenance": _prov,
        "schedule_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "standard": req.audit_standard,
        "year": req.year,
        "schedule": schedule,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class RiskRegisterRequest(BaseModel):
    organisation_name: str
    domain: str = "general"
    context: str = ""
    num_risks: int = 10


@router.post("/risk-register")
async def generate_risk_register(req: RiskRegisterRequest):
    """Generate a comprehensive organisational risk register."""
    n = min(max(req.num_risks, 5), 20)

    prompt = (
        f"Draft a risk register.\n\n"
        f"Organisation: {req.organisation_name}\nDomain: {req.domain}\n"
        + (f"Context: {req.context}\n" if req.context else "")
        + f"Number of risks to identify: {n}\n\n"
        "For each risk provide a table row:\n"
        "Risk ID | Category | Risk Description | Likelihood (1-5) | Impact (1-5) | "
        "Risk Score | Current Controls | Residual Risk | Owner | Treatment | Review Date\n\n"
        "Categories to cover: Strategic, Operational, Financial, Legal/Compliance, "
        "Reputational, Technology, People, Environmental\n\n"
        "After the table, provide:\n"
        "## Risk Heat Map Summary (narrative)\n"
        "## Top 3 Priority Risks (detailed analysis)\n"
        "## Risk Appetite Statement\n"
        "## Risk Review Cadence\n"
    )

    biobus.fire_signal("cognitive", "mgmt.risk", f"Risk register: {req.organisation_name}", 0.6)
    register, _prov = await _compose(prompt, "mgmt_risk", said=person_said(req.organisation_name, req.context))
    biobus.record_operation("risk_register", "mgmt.risk", success=True)

    return {
        "ai_provenance": _prov,
        "register_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "domain": req.domain,
        "register": register,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ── EMS — ISO 14001 Environmental Management System ──────────────────────────

class EMSRequest(BaseModel):
    organisation_name: str
    domain: str = "general"
    sector: str = "services"   # manufacturing | services | technology | healthcare
    scope: str = ""            # environmental scope (optional)


@router.post("/ems/generate")
async def generate_ems(req: EMSRequest):
    """Generate an ISO 14001-aligned Environmental Management System framework."""
    prompt = (
        f"Draft an environmental management system outline.\n\n"
        f"Organisation: {req.organisation_name}\n"
        f"Domain: {req.domain}\nSector: {req.sector}\n"
        + (f"Scope: {req.scope}\n" if req.scope else "")
        + "\nDraft an outline of an environmental management system under these headings (name no edition of "
          "any standard and claim no alignment, compliance or certification):\n"
        "## 1. Environmental Policy Statement\n"
        "## 2. Environmental Aspects and Impacts Register\n"
        "   (List top 10 aspects: activity | aspect | impact | significance)\n"
        "## 3. Legal and Regulatory Register\n"
        "   (Relevant UK/international environmental legislation)\n"
        "## 4. Environmental Objectives and Targets (5 SMART objectives)\n"
        "## 5. Environmental Management Programmes (actions, owners, timelines)\n"
        "## 6. Energy Management Plan\n"
        "## 7. Waste Management Framework\n"
        "## 8. Carbon Footprint Assessment Methodology\n"
        "## 9. Emergency Preparedness and Response Procedure\n"
        "## 10. Environmental Monitoring and Measurement Plan\n"
        "## 11. Internal Audit Programme\n"
        "## 12. Management Review Agenda for Environmental Performance\n\n"
        f"Tailor to a {req.sector}-sector {req.domain} organisation. Be practical and immediately usable."
    )

    biobus.fire_signal("sensory", "mgmt.ems", f"EMS generation: {req.organisation_name}", 0.5)
    framework, _prov = await _compose(prompt, "mgmt_ems", said=person_said(req.organisation_name, req.scope))
    biobus.record_operation("ems_generate", "mgmt.ems", success=True, payload=f"{req.organisation_name} EMS")

    return {
        "ai_provenance": _prov,
        "doc_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "standard": "ISO 14001",
        "standard_note": STANDARD_NOTE,
        "editions": EDITIONS_READ,
        "framework_type": "EMS",
        "framework": (framework or "") + "\n\n_" + STANDARD_NOTE + "_",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class NonConformanceRequest(BaseModel):
    organisation_name: str
    vsb_id: str | None = None
    description: str
    severity: str = "minor"   # minor | major | critical


@router.post("/nonconformance")
async def record_nonconformance(req: NonConformanceRequest, user: dict | None = Depends(get_current_user)):
    """
    Record a quality non-conformance — feeds directly into the immune system.
    Major/critical non-conformances elevate immune threat level.
    """
    #  OWNER RULING 2026-10-12 - a severity that is not one of the three was treated as minor. Refused.
    if req.severity not in ("minor", "major", "critical"):
        raise HTTPException(status_code=422, detail=(
            f"'{req.severity}' is not a severity. Use minor, major or critical. Nothing was signalled."))
    # Feed into immune system — non-conformances are organism errors
    error_type = {
        "minor": "quality_minor",
        "major": "quality_major",
        "critical": "quality_critical",
    }.get(req.severity, "quality_minor")

    immune_endpoint = f"qms.{req.vsb_id or 'org'}"
    biobus.record_error(immune_endpoint, error_type)

    # Higher intensity signal for severe non-conformances
    intensity = {"minor": 0.3, "major": 0.6, "critical": 0.9}.get(req.severity, 0.3)
    biobus.fire_signal(
        "reflex", "mgmt.nonconformance",
        f"NC [{req.severity.upper()}]: {req.description[:100]}",
        intensity,
    )

    #  W733 (FU-986) - THE NONCONFORMANCE IS KEPT: it opens a defect in the quality system's durable loop, owned
    #  by the caller, before anything is composed - so a model that fails cannot lose the record.
    from agentic_core.vbs.registry import qms as _qms
    _u = user if isinstance(user, dict) else None
    _defect = _qms.open_reported_defect(req.description, req.severity, req.organisation_name, req.vsb_id,
                                        owner_id=(_u or {}).get("username"))
    # A draft CAPA (corrective and preventive action). No role is claimed in the prompt (Owner ruling 2026-10-11).
    prompt = (
        f"Draft a CAPA (corrective and preventive action) for this non-conformance:\n\n"
        f"Organisation: {req.organisation_name}\n"
        f"Non-conformance: {req.description}\n"
        f"Severity: {req.severity.upper()}\n\n"
        f"Provide:\n"
        f"1. Root cause analysis (5-Why)\n"
        f"2. Immediate containment actions\n"
        f"3. Corrective actions (what and by when)\n"
        f"4. Preventive actions (systemic changes)\n"
        f"5. Effectiveness verification method\n"
    )
    capa, _prov = await _compose(prompt, "mgmt_capa", said=person_said(req.organisation_name, req.description))

    return {
        "ai_provenance": _prov,
        "nc_id": _defect["id"],
        "severity": req.severity,
        "description": req.description,
        #  the sentence that stood here said the nonconformance was kept. Nothing keeps it: the id above is
        #  made for this answer and stored nowhere. What happened is a signal, and that is what is said.
        "immune_response": f"signalled as {error_type} to the immune sensor",
        "stored": True,
        "defect": _defect,
        "stored_basis": (f"STORED as defect {_defect['id']} in the quality system's defect loop, marked as reported "
                         f"by a person: list it at GET /api/v1/vbs/qms/defects, then correct it and re-verify it "
                         f"there. It is not a gate run, so the non-conformance rate does not move."),
        "capa": capa,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
