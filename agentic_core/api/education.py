"""
Education Domain API — Curriculum design and learning tools.

  POST /api/v1/education/curriculum    — design a full curriculum for a topic
  POST /api/v1/education/lesson-plan   — generate a detailed lesson plan
  POST /api/v1/education/assessment    — create assessments (quiz, rubric, exam)
  POST /api/v1/education/feedback      — mark student work + give constructive feedback (indicative)
  GET  /api/v1/education/frameworks    — list supported curriculum frameworks
"""
from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import functools

from agentic_core.api._ai_provenance import ai_text as _ai_text, person_said, disclaimer_for
from agentic_core.api._ai_provenance import note_withheld      # P3.30 - the coverage figure follows the text returned

#  W637 (FU-597) — this router's domain, bound once. Every ai_text call below carries it, so the native floor
#  prints the real domain instead of "the request named no domain".
ai_text = functools.partial(_ai_text, domain="education")
from agentic_core.religious_domain.subject_screen import refuse_if_religious_teaching, screen_subject

router = APIRouter(prefix="/api/v1/education", tags=["education"])

#  OWNER RULING 2026-10-12 - ONLY THE NAME OF A FRAMEWORK IS HELD. No content of any framework is in this
#  platform, so nothing is checked against one and nothing is "aligned" to one. The id `uk_national` is kept
#  for saved records; its name was a curriculum that does not exist (the national curriculum is England's).
FRAMEWORK_HELD = ("only this framework's NAME is held: none of its content is in this platform, so nothing "
                  "below was checked against it")
_FRAMEWORKS = [
    {"id": "bloom", "name": "Bloom's Taxonomy", "region": "International"},
    {"id": "uk_national", "name": "National Curriculum (England)", "region": "England",
     "page": "https://www.gov.uk/national-curriculum", "read_on": "2026-10-12",
     "says": "the national curriculum of England's maintained schools; academies and private schools need not follow it"},
    {"id": "cambridge_igcse", "name": "Cambridge IGCSE", "region": "International"},
    {"id": "ib", "name": "International Baccalaureate (IB)", "region": "International"},
    {"id": "montessori", "name": "Montessori Method", "region": "International"},
    {"id": "stem", "name": "STEM Framework", "region": "International"},
    {"id": "competency_based", "name": "Competency-Based Education", "region": "International"},
    {"id": "ubd", "name": "Understanding by Design (UbD)", "region": "International"},
]
for _f in _FRAMEWORKS:
    _f["held"] = "name only"
_FRAMEWORK_IDS = tuple(f["id"] for f in _FRAMEWORKS)
#  typed once: what the religion screen's silence means, and who these tools are for
SCREEN_NOT_CLEARED = ("Not reviewed as religious teaching content: this platform's subject screen did not "
                      "flag it. The screen cannot certify a subject as secular - it can only flag one.")
FOR_WHOM = "For a teacher or an adult learner."
WORK_LIMIT = 6000          # characters of a student's work handed to the composer

_ASSESSMENT_TYPES = {
    "quiz": "Create a 10-question quiz with answer key. Mix question types: multiple choice (5), short answer (3), and true/false (2). Include a marking scheme.",
    "rubric": "Design a detailed assessment rubric with 5 performance levels (Distinction, Merit, Pass, Developing, Not Yet). Include descriptors for each criterion at each level.",
    "exam": "Create a formal examination paper with 3 sections: Section A (10 MCQs, 1 mark each), Section B (4 short answer questions, 5 marks each), Section C (1 essay question, 20 marks). Include mark scheme.",
    "project_brief": "Write a detailed project brief for an assessed project. Include: learning objectives, task description, deliverables, word/time limits, assessment criteria, and a worked example.",
    "formative": "Design 5 formative assessment activities (exit tickets, think-pair-share prompts, diagnostic questions) that check understanding at key points in the lesson.",
}


@router.get("/frameworks")
async def list_frameworks():
    return {"frameworks": _FRAMEWORKS, "total": len(_FRAMEWORKS), "held_basis": FRAMEWORK_HELD}


class CurriculumRequest(BaseModel):
    subject: str
    level: str  # e.g. "GCSE", "A-Level", "University Year 1", "Primary KS2"
    duration_weeks: int = 12
    framework: str = "bloom"
    learning_objectives_count: int = 6
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/curriculum")
async def design_curriculum(req: CurriculumRequest):
    """
    Design a complete curriculum structure for a subject/level.

    P3.10 — A RELIGIOUS SUBJECT IS REFUSED HERE AND REFERRED, not composed with a caveat.
    Owner ruling 2026-10-05b R7 (§A.12.3): a named human scholar approves AI-composed religious content
    before a learner sees it, and A DISCLAIMER IS NOT A REVIEW. This route is general - it serves
    mathematics and history too - so it is not gated; what it does is decline the requests that belong
    behind the gate and say where they go. The screen can only FLAG, never clear, and the response says so.
    """
    _screen = refuse_if_religious_teaching("curriculum", req.subject, req.level, req.framework)   # W659 - one function, four routes
    if req.framework not in _FRAMEWORK_IDS:
        raise HTTPException(status_code=422, detail=(
            f"'{req.framework}' is not a framework this platform lists. The listed names are: "
            + ", ".join(_FRAMEWORK_IDS) + ". Only names are held - no framework's content."))
    n_weeks = min(max(req.duration_weeks, 4), 52)
    n_objectives = min(max(req.learning_objectives_count, 3), 10)
    _adjusted = ([f"duration: {req.duration_weeks} weeks was asked for and {n_weeks} was used (the range is 4 to 52)"]
                 if n_weeks != req.duration_weeks else []) + (
                [f"objectives: {req.learning_objectives_count} was asked for and {n_objectives} was used (the range is 3 to 10)"]
                 if n_objectives != req.learning_objectives_count else [])

    prompt = (
        f"Claim no professional role.\n"
        f"Design a complete {n_weeks}-week curriculum.\n\n"
        f"Subject: {req.subject}\n"
        f"Level: {req.level}\n"
        f"Framework: {req.framework.replace('_', ' ')}\n"
        f"Duration: {n_weeks} weeks\n\n"
        "Produce:\n"
        f"## Learning Objectives ({n_objectives} SMART objectives)\n"
        "## Prerequisites (what students must know before starting)\n"
        f"## Week-by-Week Plan (all {n_weeks} weeks: week number | topic | key concepts | activities | assessment)\n"
        "## Assessment Strategy (formative and summative methods)\n"
        "## Differentiation Strategy (support for lower and higher attainers)\n"
        "## Resources Required (textbooks, tools, software)\n"
        "## Success Metrics (how to measure curriculum effectiveness)\n\n"
        "Be specific and practical. Each week entry should be actionable for a teacher."
    )

    curriculum, provenance = await ai_text(prompt, "education_curriculum", realm=req.realm,
        user_text=person_said(req.subject))

    return {
        "curriculum_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "level": req.level,
        "duration_weeks": n_weeks,
        "framework": req.framework,
        "framework_basis": FRAMEWORK_HELD,
        "adjusted": _adjusted,
        "curriculum": (curriculum or "") + "\n\n_" + FOR_WHOM + " Framework: " + FRAMEWORK_HELD + "."
                      + ((" Adjusted: " + "; ".join(_adjusted) + ".") if _adjusted else "") + "_",
        "ai_provenance": provenance,
        #  P3.10 — the screen's result travels WITH the output. It did not clear this subject; it only
        #  failed to flag it, and those are different facts. A reader who sees a curriculum served here
        #  should not infer that anything certified it as outside the scholar gate's scope.
        "religious_subject_screen": _screen,
        #  FU-456 — THE RENDERED HALF. The structured key above is the record; until this round nothing on
        #  any surface read it, so the sentence saying the subject was not cleared reached nobody while the
        #  comment above claimed it travelled with the output. `screen_note` goes through DomainTool's
        #  `withDisclosures`, the channel every domain surface already shares and the one that also writes
        #  the saved history record - so the note travels with the TEXT, not as a badge beside it.
        #  ONE LINE on purpose: the full basis is right for an audit trail and noise on a mathematics
        #  curriculum.
        "screen_note": ("Not reviewed as religious teaching content: this platform's subject screen did not "
                        "flag it. The screen cannot certify a subject as secular - it can only flag one."
                        if not _screen.get("flagged") else
                        "Flagged as religious teaching content - a named human scholar must approve it "
                        "before a learner sees it (R7 / §A.12.3)."),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


_LESSON_NOTE = (FOR_WHOM + " A draft for a teacher to check and adapt: nothing in it was checked against a "
                "curriculum or by a person. " + SCREEN_NOT_CLEARED)
_NEEDS_NOTE = (" The needs you typed were sent to the composer exactly as typed - do not name a pupil in "
               "that field.")
_ASSESSMENT_NOTE = (FOR_WHOM + " A draft: the answer key and mark scheme were checked by nobody - check every "
                    "answer before use. Not an official paper of any awarding body. " + SCREEN_NOT_CLEARED)


class LessonPlanRequest(BaseModel):
    subject: str
    topic: str
    level: str
    duration_minutes: int = 60
    class_size: int = 30
    special_needs: str = ""
    prior_knowledge: str = ""
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/lesson-plan")
async def generate_lesson_plan(req: LessonPlanRequest):
    """
    Generate a detailed, structured lesson plan ready for classroom delivery.
    """
    _screen = refuse_if_religious_teaching("lesson plan", req.subject, req.topic, req.level)      # W659 (ledger v15 FU-689)
    duration = min(max(req.duration_minutes, 20), 180)

    prompt = (
        f"Claim no professional role. "
        f"Create a detailed, classroom-ready lesson plan.\n\n"
        f"Subject: {req.subject}\n"
        f"Topic: {req.topic}\n"
        f"Level: {req.level}\n"
        f"Duration: {duration} minutes\n"
        f"Class size: {req.class_size} students\n"
        + (f"Special educational needs: {req.special_needs}\n" if req.special_needs else "")
        + (f"Prior knowledge: {req.prior_knowledge}\n" if req.prior_knowledge else "")
        + "\nProduce:\n"
        "## Learning Objectives (3-4, SMART, Bloom's verbs)\n"
        "## Success Criteria (student-facing 'I can...' statements)\n"
        "## Starter Activity (10% of time — hook/retrieval practice)\n"
        "## Main Teaching Sequence (70% of time — with timings, activities, teacher and student actions)\n"
        "## Plenary (10% of time — consolidation and assessment for learning)\n"
        "## Assessment Points (when and how you check understanding during the lesson)\n"
        "## Differentiation (stretch questions, scaffolding, SEND adaptations)\n"
        "## Resources Needed\n"
        "## Homework Task\n"
        "## Key Questions (6 questions at different Bloom's levels)\n\n"
        "Format timings as [MM:SS] inline. Be specific and practical."
    )

    plan, provenance = await ai_text(prompt, "education_lesson_plan", realm=req.realm,
        user_text=person_said(req.topic, req.subject))

    return {
        "plan_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "topic": req.topic,
        "level": req.level,
        "duration_minutes": duration,
        "lesson_plan": (plan or "") + "\n\n_" + _LESSON_NOTE + (_NEEDS_NOTE if req.special_needs.strip() else "") + "_",
        "religious_subject_screen": _screen,
        "screen_note": SCREEN_NOT_CLEARED,
        "disclaimer": disclaimer_for(provenance, "An AI-drafted lesson plan.", _LESSON_NOTE),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class FeedbackRequest(BaseModel):
    student_work: str
    task: str = ""                  # the question / task the work responds to
    level: str = ""                 # e.g. GCSE, A-Level, KS2
    rubric: str = ""                # marking criteria / rubric (optional)
    subject: str = "general"
    tone: str = "constructive"      # constructive | encouraging | rigorous
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/feedback")
async def marking_feedback(req: FeedbackRequest):
    """Mark a piece of student work against the task and any rubric, and give constructive, actionable
    feedback — strengths, areas to develop, criterion-by-criterion notes, next steps, and an INDICATIVE
    level/grade. An AID for the teacher's professional judgement — indicative only, never a final or
    official mark; the teacher remains responsible."""
    #  W659 - marking is teaching content too. The SUBJECT and the TASK are screened; the student's own work is not
    #  (a history essay that mentions a faith is not a religious-teaching request).
    refuse_if_religious_teaching("marking feedback", req.subject, req.task)
    #  OWNER RULING 2026-10-12 - BLANK WORK IS REFUSED, AND WORK NOT READ WHOLE IS NOT GRADED. The work was cut
    #  at a fixed length inside the prompt and a grade returned with nothing said; blank work was graded too.
    _work = req.student_work or ""
    if not _work.strip():
        raise HTTPException(status_code=422, detail=(
            "No student work was supplied, so there is nothing to mark. Paste the work and try again."))
    _cut = len(_work) > WORK_LIMIT
    prompt = (
        "Claim no professional role. Mark the student's work against the task and any "
        "rubric, and give warm but honest, actionable feedback. Be specific and point to evidence in the work.\n\n"
        f"Subject: {req.subject}\nLevel: {req.level}\nFeedback tone: {req.tone}\n"
        + (f"Task / question:\n{req.task}\n\n" if req.task else "")
        + (f"Rubric / marking criteria:\n{req.rubric}\n\n" if req.rubric else "")
        + f"STUDENT WORK:\n{_work[:WORK_LIMIT]}\n\n"
        "Produce:\n"
        "## Overall Impression (2-3 sentences)\n"
        "## Strengths (specific, with evidence from the work)\n"
        "## Areas to Develop (specific, prioritised)\n"
        "## Criterion-by-Criterion (if a rubric was provided, assess the work against each criterion)\n"
        "## Actionable Next Steps (3-4 concrete things the student can do to improve)\n"
        "## Indicative Level / Grade (a RANGE with a one-line justification — explicitly indicative, to be "
        "confirmed by the teacher; never present it as a final or official mark)\n\n"
        "Be encouraging and developmental. Mark ONLY what is present — never invent content the student did "
        "not write, and do not penalise for things outside the stated task."
    )

    feedback, provenance = await ai_text(prompt, "education_feedback", realm=req.realm,
        user_text=person_said(req.task, req.subject))

    #  P3.30 (ledger v13 R5[3]) - ON THE FLOOR THE TWO MARKING SECTIONS ARE WITHHELD. The floor composes the
    #  headings it is given and is told only the task and the subject as the person's words - the student's
    #  work never reaches it as something to read - so a section headed as a criterion-by-criterion
    #  assessment or as a level and grade was the shape of a mark with nothing behind it. Both are cut, named
    #  in `sections_withheld`, and SAID IN THE TEXT ITSELF, so the statement travels with a copy, a download
    #  and a saved version. (No top-level floor note is added: the page prints the provenance's own floor
    #  note, and stops printing it when the response carries one of its own.)
    sections_withheld: list = []
    _on_floor = bool((provenance or {}).get("floor_note"))
    if _on_floor or _cut:
        from agentic_core.api.religion import _withhold_sections
        feedback, sections_withheld = _withhold_sections(
            feedback, ("Criterion-by-Criterion", "Indicative Level / Grade"))
        if sections_withheld and _on_floor:
            feedback = ((feedback + "\n\n") if feedback else "") + (
                f"_Withheld on the native floor: {' · '.join(sections_withheld)}. The floor does not read the "
                f"student's work, so no assessment against criteria and no level or grade is offered here; "
                f"what remains above is a structured frame, not marking._")

    if _cut:
        #  said in the TEXT, so it travels with a copy, a download and a saved version
        feedback = ((feedback + "\n\n") if feedback else "") + (
            f"_ONLY PART OF THE WORK WAS READ: the first {WORK_LIMIT:,} of {len(_work):,} characters. "
            + (f"Withheld for that reason: {' · '.join(sections_withheld)} - an assessment against criteria "
               f"or a level for work that was not read whole would be of something else. "
               if sections_withheld and not _on_floor else "")
            + "Shorten the work or mark it in parts._")
    return {
        "feedback_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "level": req.level,
        "tone": req.tone,
        "feedback": feedback,
        "sections_withheld": sections_withheld,
        "work_read": {"chars": len(_work), "read_chars": min(len(_work), WORK_LIMIT), "read_whole": not _cut},
        "ai_provenance": note_withheld(provenance, sections_withheld),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": disclaimer_for(
            provenance, "AI-assisted marking and feedback.",
            "An aid for the teacher's professional judgement — indicative only, NOT a final or official grade. "
            "The teacher remains responsible for the mark awarded."),
    }


class AssessmentRequest(BaseModel):
    subject: str
    topic: str
    level: str
    assessment_type: str = "quiz"  # quiz | rubric | exam | project_brief | formative
    learning_objectives: list[str] = []
    realm: str = ""          # W505 (P2.5) — the taxonomy realm; empty means "unchanged"


@router.post("/assessment")
async def create_assessment(req: AssessmentRequest):
    """
    Create a complete assessment instrument (quiz, rubric, exam, etc.)
    """
    _screen = refuse_if_religious_teaching("assessment", req.subject, req.topic, req.level)       # W659 (ledger v15 FU-689)
    if req.assessment_type not in _ASSESSMENT_TYPES:
        raise HTTPException(status_code=422, detail=(
            f"'{req.assessment_type}' is not an assessment type this platform drafts. The types are: "
            + ", ".join(_ASSESSMENT_TYPES) + "."))
    type_prompt = _ASSESSMENT_TYPES[req.assessment_type]

    objectives_context = ""
    if req.learning_objectives:
        objectives_context = f"Learning objectives being assessed:\n" + "\n".join(f"- {o}" for o in req.learning_objectives) + "\n\n"

    prompt = (
        f"Claim no professional role.\n"
        f"Subject: {req.subject}\n"
        f"Topic: {req.topic}\n"
        f"Level: {req.level}\n"
        f"Assessment type: {req.assessment_type.replace('_', ' ')}\n\n"
        + objectives_context
        + type_prompt
        + "\n\nEnsure the assessment is:\n"
        "- Aligned to the stated topic and level\n"
        "- Clearly formatted and ready to use\n"
        "- Accompanied by a complete answer key/mark scheme\n"
        "- Free of ambiguity"
    )

    assessment, provenance = await ai_text(prompt, "education_assessment", realm=req.realm,
        user_text=person_said(req.topic, req.subject))

    return {
        "assessment_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "topic": req.topic,
        "level": req.level,
        "assessment_type": req.assessment_type,
        "assessment": (assessment or "") + "\n\n_" + _ASSESSMENT_NOTE + "_",
        "religious_subject_screen": _screen,
        "screen_note": SCREEN_NOT_CLEARED,
        "disclaimer": disclaimer_for(provenance, "An AI-drafted assessment.", _ASSESSMENT_NOTE),
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
