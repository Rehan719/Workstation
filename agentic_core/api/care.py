"""
Care Domain API — Healthcare pathway and support tools.

  POST /api/v1/care/care-plan       — generate a personalised care plan
  POST /api/v1/care/risk-assess     — AI-assisted risk assessment (NEWS2 / falls / pressure)
  POST /api/v1/care/safeguarding    — triage a safeguarding concern (Care Act 2014 process guidance)
  POST /api/v1/care/handover        — generate a clinical handover document (SBAR format)
  GET  /api/v1/care/tools           — list available care assessment tools
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import functools

from agentic_core.api._ai_provenance import ai_text as _ai_text, person_said, disclaimer_for
from agentic_core.api._ai_provenance import note_withheld      # the coverage figure follows the text returned

#  W637 (FU-597) — this router's domain, bound once. Every ai_text call below carries it, so the native floor
#  prints the real domain instead of "the request named no domain".
ai_text = functools.partial(_ai_text, domain="care")
from agentic_core.care.scoring import compute_score, score_summary

router = APIRouter(prefix="/api/v1/care", tags=["care"])

_TOOLS = [
    #  `does` is what this platform DOES with the entry: "computes" a published table in code, or returns a
    #  "frame" (a narrative with no score). `standard` names a publication only where one was read; a source
    #  not yet read at its publisher's page says so instead of naming something that is not a publication.
    {"id": "news2", "name": "NEWS2 Early Warning Score", "type": "risk_score", "does": "computes",
     "standard": "Royal College of Physicians, NEWS2 (December 2017)"},
    {"id": "must", "name": "MUST Malnutrition Screening", "type": "screening", "does": "computes", "standard": "BAPEN"},
    {"id": "waterlow", "name": "Waterlow Pressure Ulcer Risk", "type": "risk_score", "does": "computes",
     "standard": "Waterlow (its source and reuse terms have not been read at their owner's page)"},
    {"id": "falls_risk", "name": "Falls count (retired)", "type": "retired", "does": "nothing - retired",
     "standard": "NICE CG161, replaced by NICE NG249 on 29 April 2025"},
    {"id": "dementia_care", "name": "Dementia Care Planning", "type": "care_plan", "does": "frame", "standard": "NICE NG97"},
    {"id": "mental_health", "name": "Mental Health Care Plan", "type": "care_plan", "does": "frame",
     "standard": "no source has been read for this entry"},
    {"id": "discharge", "name": "Discharge Planning Checklist", "type": "checklist", "does": "frame",
     "standard": "no single published standard is held for this entry"},
    {"id": "safeguarding", "name": "Safeguarding process guidance (adults, England)", "type": "process_guidance",
     "does": "frame", "standard": "Care Act 2014"},
]


@router.get("/tools")
async def list_tools():
    return {"tools": _TOOLS, "total": len(_TOOLS)}


#  W676 - typed, never generated: the first thing a person reporting a safeguarding concern reads.
IMMEDIATE_DANGER_FIRST = ("**If anyone is in immediate danger, call 999 now - before reading on and before "
                          "recording anything.** Nothing below replaces that call. What follows is general "
                          "process guidance, not a decision about this concern.")


#  typed, never generated; the children's sentence was read at its publisher's page on the date it carries
ADULT_ROUTE_ONLY = ("**This form follows the ADULT safeguarding route for England.** If the concern is about a child or young person, do not use this form: contact the children's social care team at the child's local council, or call 999 if the child is at immediate risk "
                    "(read at https://www.gov.uk/report-child-abuse on 2026-10-12).")


#  what only a clinician may write: never asked for, and cut if a composer returns it
CLINICIAN_ONLY_SUBJECTS = ("medicines and doses", "risk management", "consent and capacity", "what to do in a crisis")
CLINICIAN_ONLY_SECTIONS = ("Medication Management", "Medication", "Medicines", "Risk Management Plan", "Risk Management",
                           "Crisis Plan", "Consent and Capacity Considerations", "Consent and Capacity", "Capacity")
CARE_PLAN_NOTE = ("A DRAFT ORGANISER of what was supplied - not a care plan, and reviewed by nobody. It says nothing "
                  "about " + ", ".join(CLINICIAN_ONLY_SUBJECTS[:-1]) + " or " + CLINICIAN_ONLY_SUBJECTS[-1] +
                  ": those are for a qualified professional who knows the person.")


class CarePlanRequest(BaseModel):
    patient_profile: dict = {}
    care_needs: list[str] = []
    setting: str = "community"  # community | hospital | care_home | mental_health
    duration_weeks: int = 4
    care_model: str = "person_centred"
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


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
        f"Claim no professional role. "
        f"Arrange what is supplied below as a DRAFT organiser for a care plan. Use only what is supplied: where "
        f"something is not supplied write NOT SUPPLIED and invent nothing - no history, no preference, no "
        f"name of a responsible person, no date. Write NOTHING about medicines or doses, about risk, about "
        f"capacity or consent, or about what to do in a crisis: list those only as questions for a professional.\n\n"
        + profile_text
        + needs_text
        + f"Care setting: {req.setting.replace('_', ' ')}\n"
        f"Plan duration: {req.duration_weeks} weeks\n"
        f"Care model: {req.care_model.replace('_', ' ')}\n\n"
        "Produce a care plan with these sections:\n"
        "## My Goals (in the person's own voice — what they want to achieve)\n"
        "## My Strengths and Support Network\n"
        "## What I Need Help With (table: Need, as the person said it | What is already arranged, if supplied | NOT SUPPLIED otherwise)\n"
        "## Questions for a Professional (medicines, risks, consent and capacity, what to do if things get worse - as questions only)\n"
        "## Review Schedule (only dates that were supplied)\n\n"
        "Use the person's own words where they were supplied. Name no guideline. "
        "Mark every part that was not supplied with NOT SUPPLIED."
    )

    plan, provenance = await ai_text(prompt, "care_planner", realm=req.realm,
        user_text=person_said(req.care_needs))
    #  IF A COMPOSER WRITES SUCH A SECTION ANYWAY, IT IS CUT AND NAMED. The prompt no longer asks for one; this
    #  is the floor under that, because what a model returns is not decided by what it was asked.
    from agentic_core.api.religion import _withhold_sections
    plan, _cut_sections = _withhold_sections(plan or "", CLINICIAN_ONLY_SECTIONS)
    plan = ((plan + "\n\n") if plan else "") + "_" + CARE_PLAN_NOTE + (
        f" Removed from this draft because only a clinician may write them: {' · '.join(_cut_sections)}." if _cut_sections else "") + "_"

    return {
        "plan_id": uuid.uuid4().hex[:10],
        "setting": req.setting,
        "duration_weeks": req.duration_weeks,
        "care_plan": plan,
        "draft": True,
        "sections_withheld": _cut_sections,
        "not_written_here": list(CLINICIAN_ONLY_SUBJECTS),
        "ai_provenance": note_withheld(provenance, _cut_sections),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": disclaimer_for(
            provenance, "This care plan is AI-generated as a planning aid only.",
            "It must be reviewed and validated by a qualified healthcare professional before use."),
    }


class RiskAssessRequest(BaseModel):
    tool: str = "news2"
    patient_data: dict = {}
    clinical_context: str = ""
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/risk-assess")
async def risk_assessment(req: RiskAssessRequest):
    """
    AI-assisted risk assessment using a specified clinical tool.
    """
    tool_info = next((t for t in _TOOLS if t["id"] == req.tool), None)
    #  Care item, clause 7 - AN ID THE CATALOGUE DOES NOT HOLD IS REFUSED. It was given a title made from its
    #  id, and a model would have been asked to interpret an assessment under a name nobody published.
    if tool_info is None:
        raise HTTPException(status_code=422, detail=(
            f"'{req.tool}' is not a tool this platform holds. The tools are: "
            + ", ".join(t["id"] for t in _TOOLS if t["type"] != "retired") + "."))
    #  Care item, clause 2 - THE FALLS COUNT IS RETIRED: nothing is computed and nothing is composed about it.
    if tool_info["type"] == "retired":
        from agentic_core.care.scoring import FALLS_RETIRED as _fr
        raise HTTPException(status_code=410, detail=(
            f"The falls count is retired. It implemented {_fr['replaced']}, which its publisher replaced with "
            f"{_fr['replaced_by']}; the replacement says: {_fr['says']} Read it at {_fr['page']} "
            f"(read by this platform on {_fr['read_on']}). No count, trigger or reassurance is returned."))
    tool_name = tool_info["name"]

    # W457 (P1.9, ledger 1.9 / R5.3) — the score is COMPUTED here from the published table (NEWS2 /
    # MUST / Waterlow; NICE CG161 as a labelled factor count). The old route asked the AI to "show
    # working" and forwarded the observations verbatim — the assessor's case (NEWS2 6, urgent) came
    # back with no score under a green pass. The AI now narrates INTERPRETATION of a score it is told
    # not to recompute; the block is returned first and the page renders it first.
    score = compute_score(req.tool, req.patient_data or {})
    summary = score_summary(score)
    heading = "COMPUTED SCORE"

    patient_context = ""
    if req.patient_data:
        patient_context = "Patient observations/data (as recorded):\n" + "\n".join(
            f"  {k}: {v}" for k, v in req.patient_data.items()
        ) + "\n"

    prompt = (
        f"Describe what a {tool_name} result of this kind means in general terms, for a qualified "
        f"clinician to read. Claim no professional role and make no decision about this patient.\n\n"
        + patient_context
        + (f"Clinical context: {req.clinical_context}\n" if req.clinical_context else "")
        + f"\n{heading} (authoritative — computed in-house from the published table; do NOT recompute "
          f"or restate a different total): {summary}\n"
        + (f"Missing observations: {', '.join(score.get('missing') or [])} — say what recording them would change.\n"
           if score.get("available") and score.get("missing") else "")
        + "\nProvide:\n"
        "## Clinical Interpretation (of the computed score and its components)\n"
        "## Recommended Actions (prioritised, with urgency, consistent with the computed band)\n"
        "## Escalation Triggers (what changes would move the score to the next band)\n"
        "## Documentation Guidance\n\n"
        "Reference current clinical guidelines. Be specific about thresholds and actions."
    )

    #  P3.30 (ledger v15 R5[8]) - THE RECORDED OBSERVATIONS ARE THE PERSON'S WORDS TOO. Only the clinical
    #  context was named, so a request carrying observations and no context told the floor nothing had been
    #  said. Each observation the person recorded is passed as its own line, "key: value", exactly as the
    #  prompt above already prints it; a value that is not text or a number is left out, not stringified.
    _observed = [f"{k}: {v}" for k, v in (req.patient_data or {}).items()
                 if isinstance(k, str) and isinstance(v, (str, int, float)) and not isinstance(v, bool)
                 and str(v).strip()]
    assessment, provenance = await ai_text(prompt, "care_risk_assess", realm=req.realm,
        user_text=person_said(req.clinical_context, _observed))

    return {
        "assessment_id": uuid.uuid4().hex[:10],
        "tool": req.tool,
        "tool_name": tool_name,
        "score": score,                         # the deterministic block — rendered FIRST
        "score_summary": summary,
        "assessment": assessment,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        #  W642 (FU-651) - TWO claims, each following its own fact: whether a score was computed at all (three
        #  tools have no published arithmetic and said "computed from the published table" anyway), and what
        #  served the narrative.
        "disclaimer": (
            ("The score is computed in-house from the published table (NEWS2 RCP 2017 · MUST BAPEN · "
             "Waterlow) and is a decision aid, not a diagnosis; "
             if isinstance(score, dict) and score.get("available") else
             "NO SCORE WAS COMPUTED: this tool has no published arithmetic here, so nothing below is a score; ")
            + ("the narrative is a structured frame from the native floor, not an interpretation by AI or by "
               "a clinician. " if provenance.get("floor_note") else "the narrative is an AI interpretation aid only. ")
            + "Clinical judgement by a qualified professional is required."),
    }


SAFEGUARDING_JURISDICTION = "England (Care Act 2014)"


class SafeguardingRequest(BaseModel):
    concern: str                          # the safeguarding concern, described
    setting: str = "community"            # community | hospital | care_home | domiciliary
    person_context: str = ""              # relevant context (adult at risk, capacity, etc.)
    jurisdiction: str = "England (Care Act 2014)"
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/safeguarding")
async def safeguarding_triage(req: SafeguardingRequest):
    """Structure a safeguarding concern under the relevant statutory framework (Care Act 2014 by default):
    immediate-safety check, likely category of abuse/neglect, who to notify, what to record, consent & Making
    Safeguarding Personal, and next steps. This is PROCESS guidance to help a worker act correctly — NOT a
    determination, legal/clinical advice, or a substitute for local safeguarding procedures and professional
    judgement. If anyone is in immediate danger, emergency services (999) come first."""
    #  Care item, clause 4 - THE ADULT ROUTE FOR ENGLAND AND NOTHING ELSE. Any string was accepted as the
    #  framework and printed back. Another jurisdiction is refused before anything is composed.
    if (req.jurisdiction or "").strip() != SAFEGUARDING_JURISDICTION:
        raise HTTPException(status_code=422, detail=(
            f"This form covers the adult safeguarding route for England only ('{SAFEGUARDING_JURISDICTION}'). "
            f"For another nation or framework this platform holds no route: ask the local council for the "
            f"area, or call 999 if anyone is in immediate danger."))
    prompt = (
        "Set out the general PROCESS a frontline worker follows for an ADULT safeguarding concern in England. "
        "Claim no professional role, decide nothing about this concern, and name no contact details.\n\n"
        f"Concern: {req.concern}\nSetting: {req.setting.replace('_', ' ')}\nFramework: {req.jurisdiction}\n"
        + (f"Context: {req.person_context}\n" if req.person_context else "")
        + "\nProduce:\n"
        "## Immediate Safety (is anyone in immediate danger? if so, the first action is to contact emergency "
        "services — 999 — before anything else)\n"
        "## Likely Category (map to the framework's categories of abuse / neglect)\n"
        "## Who to Notify (organisation's safeguarding lead, local authority adult safeguarding team, and the "
        "police if a crime may have occurred) and the urgency of each\n"
        "## What to Record (factual account in the person's own words, dates/times) — and what NOT to do "
        "(do not investigate, confront the alleged perpetrator, or promise secrecy)\n"
        "## Consent & Making Safeguarding Personal (mental capacity, the person's own wishes, and the limited "
        "circumstances where action proceeds without consent — vital interests, others at risk, a serious crime)\n"
        "## Immediate Next Steps (a short, ordered checklist)\n"
        "\n"
        "Be clear and calm. This is process guidance — defer to local procedures and professional judgement, "
        "and never identify or accuse a specific individual as a conclusion."
    )

    guidance, provenance = await ai_text(prompt, "care_safeguarding", realm=req.realm,
        user_text=person_said(req.concern))
    #  W676 - THE EMERGENCY LINE COMES FIRST, IN THE TEXT, AND IS NOT COMPOSED. It was only in the `disclaimer`
    #  field after the text; on the floor the text's "Immediate Safety" heading held the concern's own words
    #  and the number appeared nowhere in what a person reads, copies or saves.
    guidance = IMMEDIATE_DANGER_FIRST + "\n\n" + ADULT_ROUTE_ONLY + "\n\n" + (guidance or "")

    return {
        "triage_id": uuid.uuid4().hex[:10],
        "setting": req.setting,
        "jurisdiction": req.jurisdiction,
        "guidance": guidance,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
            "General safeguarding PROCESS guidance only — not legal or clinical advice, and not a substitute "
            "for your organisation's safeguarding policy or professional judgement. If anyone is in immediate "
            "danger, call 999."
        ),
    }


class HandoverRequest(BaseModel):
    patient_summary: str
    current_situation: str
    background: str = ""
    assessment: str = ""
    recommendation: str = ""
    handover_type: str = "sbar"  # sbar | isbar | nursing | medical
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/handover")
async def generate_handover(req: HandoverRequest):
    """
    Generate a structured clinical handover document (SBAR format).
    """
    prompt = (
        f"Arrange the information supplied below as a handover DRAFT using the {req.handover_type.upper()} "
        f"framework. Claim no professional role. Use only what is supplied: where a part is not supplied, "
        f"write 'NOT SUPPLIED' and invent nothing.\n\n"
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

    handover, provenance = await ai_text(prompt, "care_handover", realm=req.realm,
        user_text=person_said(req.current_situation, req.patient_summary))

    return {
        "handover_id": uuid.uuid4().hex[:10],
        "handover_type": req.handover_type.upper(),
        "handover": handover,
        "disclaimer": disclaimer_for(
            provenance, "An AI-arranged DRAFT of the information supplied.",
            "It has not been reviewed by anyone, has not been sent to or received by anyone, and is not a "
            "clinical record. The person handing over remains responsible for every word."),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
