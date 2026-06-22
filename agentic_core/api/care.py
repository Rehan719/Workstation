"""
Care Domain API — Healthcare pathway and support tools.

  POST /api/v1/care/care-plan       — generate a personalised care plan
  POST /api/v1/care/risk-assess     — AI-assisted risk assessment (NEWS2 / falls / pressure)
  POST /api/v1/care/handover        — generate a clinical handover document (SBAR format)
  GET  /api/v1/care/tools           — list available care assessment tools
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.api._ai_provenance import ai_text

router = APIRouter(prefix="/api/v1/care", tags=["care"])

_TOOLS = [
    {"id": "news2", "name": "NEWS2 Early Warning Score", "type": "risk_score", "standard": "NHSI 2017"},
    {"id": "must", "name": "MUST Malnutrition Screening", "type": "screening", "standard": "BAPEN"},
    {"id": "waterlow", "name": "Waterlow Pressure Ulcer Risk", "type": "risk_score", "standard": "UK Clinical"},
    {"id": "falls_risk", "name": "Falls Risk Assessment", "type": "risk_score", "standard": "NICE CG161"},
    {"id": "dementia_care", "name": "Dementia Care Planning", "type": "care_plan", "standard": "NICE NG97"},
    {"id": "mental_health", "name": "Mental Health Care Plan", "type": "care_plan", "standard": "Care Programme Approach"},
    {"id": "discharge", "name": "Discharge Planning Checklist", "type": "checklist", "standard": "NHS Standard"},
    {"id": "safeguarding", "name": "Safeguarding Risk Indicators", "type": "risk_score", "standard": "Care Act 2014"},
]


@router.get("/tools")
async def list_tools():
    return {"tools": _TOOLS, "total": len(_TOOLS)}


class CarePlanRequest(BaseModel):
    patient_profile: dict = {}
    care_needs: list[str] = []
    setting: str = "community"  # community | hospital | care_home | mental_health
    duration_weeks: int = 4
    care_model: str = "person_centred"


@router.post("/care-plan")
async def generate_care_plan(req: CarePlanRequest):
    """
    Generate a personalised, evidence-based care plan.
    """
    profile_text = ""
    if req.patient_profile:
        profile_text = "Patient profile:\n" + "\n".join(f"  {k}: {v}" for k, v in req.patient_profile.items()) + "\n"

    needs_text = ""
    if req.care_needs:
        needs_text = "Identified care needs:\n" + "\n".join(f"  - {n}" for n in req.care_needs) + "\n"

    prompt = (
        f"You are a senior care coordinator and registered nurse. "
        f"Create a comprehensive, person-centred care plan.\n\n"
        + profile_text
        + needs_text
        + f"Care setting: {req.setting.replace('_', ' ')}\n"
        f"Plan duration: {req.duration_weeks} weeks\n"
        f"Care model: {req.care_model.replace('_', ' ')}\n\n"
        "Produce a care plan with these sections:\n"
        "## My Goals (in the person's own voice — what they want to achieve)\n"
        "## My Strengths and Support Network\n"
        "## Care Needs and How We Will Meet Them (table: Need | Intervention | Frequency | Responsible | Review date)\n"
        "## Medication Management\n"
        "## Risk Management Plan (top 3 risks with mitigation strategies)\n"
        "## Crisis Plan (what to do if things deteriorate)\n"
        "## Review Schedule\n"
        "## Consent and Capacity Considerations\n\n"
        "Use person-centred language. Reference relevant NICE guidelines where appropriate. "
        "Mark fields needing personalisation with [PERSONALISE]."
    )

    plan, provenance = await ai_text(prompt, "care_planner")

    return {
        "plan_id": uuid.uuid4().hex[:10],
        "setting": req.setting,
        "duration_weeks": req.duration_weeks,
        "care_plan": plan,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
            "This care plan is AI-generated as a planning aid only. "
            "It must be reviewed and validated by a qualified healthcare professional before use."
        ),
    }


class RiskAssessRequest(BaseModel):
    tool: str = "news2"
    patient_data: dict = {}
    clinical_context: str = ""


@router.post("/risk-assess")
async def risk_assessment(req: RiskAssessRequest):
    """
    AI-assisted risk assessment using a specified clinical tool.
    """
    tool_info = next((t for t in _TOOLS if t["id"] == req.tool), None)
    tool_name = tool_info["name"] if tool_info else req.tool.replace("_", " ").title()

    patient_context = ""
    if req.patient_data:
        patient_context = "Patient observations/data:\n" + "\n".join(
            f"  {k}: {v}" for k, v in req.patient_data.items()
        ) + "\n"

    prompt = (
        f"You are a clinical risk assessment specialist. "
        f"Conduct a {tool_name} assessment.\n\n"
        + patient_context
        + (f"Clinical context: {req.clinical_context}\n" if req.clinical_context else "")
        + "\nProvide:\n"
        "## Score Calculation (show working for each component)\n"
        "## Total Score and Risk Level (Low / Medium / High / Very High)\n"
        "## Clinical Interpretation\n"
        "## Recommended Actions (prioritised, with urgency)\n"
        "## Escalation Triggers (what changes would warrant immediate escalation)\n"
        "## Documentation Guidance\n\n"
        "Reference current clinical guidelines. Be specific about thresholds and actions."
    )

    assessment, provenance = await ai_text(prompt, "care_risk_assess")

    return {
        "assessment_id": uuid.uuid4().hex[:10],
        "tool": req.tool,
        "tool_name": tool_name,
        "assessment": assessment,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": "AI-generated risk assessment aid only. Clinical judgement by a qualified professional is required.",
    }


class HandoverRequest(BaseModel):
    patient_summary: str
    current_situation: str
    background: str = ""
    assessment: str = ""
    recommendation: str = ""
    handover_type: str = "sbar"  # sbar | isbar | nursing | medical


@router.post("/handover")
async def generate_handover(req: HandoverRequest):
    """
    Generate a structured clinical handover document (SBAR format).
    """
    prompt = (
        f"You are an experienced clinician. Generate a clear, structured clinical handover document "
        f"using the {req.handover_type.upper()} framework.\n\n"
        f"Patient summary: {req.patient_summary}\n"
        f"Current situation: {req.current_situation}\n"
        + (f"Background: {req.background}\n" if req.background else "")
        + (f"Assessment: {req.assessment}\n" if req.assessment else "")
        + (f"Recommendation: {req.recommendation}\n" if req.recommendation else "")
        + "\nFormat the handover clearly with SBAR headers. "
        "Include: patient identification placeholder, allergies reminder, outstanding tasks, "
        "immediate concerns flagged, and 'read-back' confirmation prompt at the end. "
        "Be concise — handovers should be completable in under 3 minutes verbally."
    )

    handover, provenance = await ai_text(prompt, "care_handover")

    return {
        "handover_id": uuid.uuid4().hex[:10],
        "handover_type": req.handover_type.upper(),
        "handover": handover,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
