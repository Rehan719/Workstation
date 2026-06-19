"""
Management Systems API — QMS, BMS, DCS, EMS for VSB entities.

Provides AI-generated management system documentation and governance tools
that can be attached to any VSB entity or project.

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

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/mgmt", tags=["management-systems"])

_STANDARDS = [
    {"id": "iso9001", "name": "ISO 9001:2015", "type": "QMS", "description": "Quality Management Systems"},
    {"id": "iso14001", "name": "ISO 14001:2015", "type": "EMS", "description": "Environmental Management Systems"},
    {"id": "iso27001", "name": "ISO 27001:2022", "type": "ISMS", "description": "Information Security Management"},
    {"id": "iso45001", "name": "ISO 45001:2018", "type": "OH&S", "description": "Occupational Health and Safety"},
    {"id": "bsc", "name": "Balanced Scorecard", "type": "BMS", "description": "Strategic performance management"},
    {"id": "okr", "name": "OKRs", "type": "BMS", "description": "Objectives and Key Results framework"},
    {"id": "cmmi", "name": "CMMI Level 3", "type": "Process", "description": "Capability Maturity Model Integration"},
    {"id": "gdpr", "name": "UK GDPR / GDPR", "type": "Compliance", "description": "Data protection compliance framework"},
    {"id": "cyber_essentials", "name": "Cyber Essentials Plus", "type": "Security", "description": "UK government cybersecurity certification"},
]


@router.get("/standards")
async def list_standards():
    return {"standards": _STANDARDS, "total": len(_STANDARDS)}


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
        f"You are a lead ISO 9001 quality consultant. Design a complete QMS framework.\n\n"
        f"Organisation: {req.organisation_name}\n"
        f"Domain: {req.domain}\n"
        f"Size: {req.size}\n"
        + (f"Products/Services: {req.products_services}\n" if req.products_services else "")
        + (f"Existing certifications: {', '.join(req.existing_certifications)}\n" if req.existing_certifications else "")
        + "\nGenerate a complete ISO 9001:2015-aligned QMS comprising:\n"
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

    framework = await gateway.query(prompt, agent="mgmt_qms")

    return {
        "doc_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "standard": "ISO 9001:2015",
        "framework": framework,
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
        f"You are a strategic management consultant. Build a Business Management System.\n\n"
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

    framework = await gateway.query(prompt, agent="mgmt_bms")

    return {
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
        f"You are a document control specialist. Design a complete DCS for:\n\n"
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

    framework = await gateway.query(prompt, agent="mgmt_dcs")

    return {
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
        f"You are an internal audit lead. Generate a risk-based internal audit programme.\n\n"
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

    schedule = await gateway.query(prompt, agent="mgmt_audit")

    return {
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
        f"You are a risk management consultant. Generate a comprehensive risk register.\n\n"
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

    register = await gateway.query(prompt, agent="mgmt_risk")

    return {
        "register_id": uuid.uuid4().hex[:10],
        "organisation_name": req.organisation_name,
        "domain": req.domain,
        "register": register,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
