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

from agentic_core.api._ai_provenance import ai_text
from agentic_core.religious_domain.subject_screen import screen_subject

router = APIRouter(prefix="/api/v1/education", tags=["education"])

_FRAMEWORKS = [
    {"id": "bloom", "name": "Bloom's Taxonomy", "region": "International"},
    {"id": "uk_national", "name": "UK National Curriculum", "region": "England"},
    {"id": "cambridge_igcse", "name": "Cambridge IGCSE", "region": "International"},
    {"id": "ib", "name": "International Baccalaureate (IB)", "region": "International"},
    {"id": "montessori", "name": "Montessori Method", "region": "International"},
    {"id": "stem", "name": "STEM Framework", "region": "International"},
    {"id": "competency_based", "name": "Competency-Based Education", "region": "International"},
    {"id": "ubd", "name": "Understanding by Design (UbD)", "region": "International"},
]

_ASSESSMENT_TYPES = {
    "quiz": "Create a 10-question quiz with answer key. Mix question types: multiple choice (5), short answer (3), and true/false (2). Include a marking scheme.",
    "rubric": "Design a detailed assessment rubric with 5 performance levels (Distinction, Merit, Pass, Developing, Not Yet). Include descriptors for each criterion at each level.",
    "exam": "Create a formal examination paper with 3 sections: Section A (10 MCQs, 1 mark each), Section B (4 short answer questions, 5 marks each), Section C (1 essay question, 20 marks). Include mark scheme.",
    "project_brief": "Write a detailed project brief for an assessed project. Include: learning objectives, task description, deliverables, word/time limits, assessment criteria, and a worked example.",
    "formative": "Design 5 formative assessment activities (exit tickets, think-pair-share prompts, diagnostic questions) that check understanding at key points in the lesson.",
}


@router.get("/frameworks")
async def list_frameworks():
    return {"frameworks": _FRAMEWORKS, "total": len(_FRAMEWORKS)}


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
    _screen = screen_subject(req.subject, req.level, req.framework)
    if _screen["flagged"]:
        #  THE DETAIL IS SHAPED FOR THE READER IT REACHES. apps/.../lib/api.ts turns a non-string
        #  `detail` into JSON.stringify(detail).slice(0, 300) and EducationHub renders that through
        #  errorMessage(), so a long explanatory basis here would arrive on a teacher's screen as JSON
        #  cut off mid-sentence. `message` therefore carries ONE readable sentence and comes first, and
        #  the whole dict stringifies well inside the 300 characters that survive.
        raise HTTPException(
            status_code=409,
            detail={
                "message": (
                    f"Not composed here: \"{req.subject}\" is religious teaching content, which needs a "
                    f"named scholar's approval before a learner sees it. Use /api/v1/qep/curriculum, "
                    f"which submits it for review. Matched: {', '.join(_screen['matched'][:3])}."),
                "where_instead": "/api/v1/qep/curriculum",
                "matched": _screen["matched"],
                "ruling": "2026-10-05b R7 (§A.12.3)",
            },
        )
    n_weeks = min(max(req.duration_weeks, 4), 52)
    n_objectives = min(max(req.learning_objectives_count, 3), 10)

    prompt = (
        f"You are a master curriculum designer with expertise in {req.framework.replace('_', ' ')}.\n"
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

    curriculum, provenance = await ai_text(prompt, "education_curriculum", realm=req.realm)

    return {
        "curriculum_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "level": req.level,
        "duration_weeks": n_weeks,
        "framework": req.framework,
        "curriculum": curriculum,
        "ai_provenance": provenance,
        #  P3.10 — the screen's result travels WITH the output. It did not clear this subject; it only
        #  failed to flag it, and those are different facts. A reader who sees a curriculum served here
        #  should not infer that anything certified it as outside the scholar gate's scope.
        "religious_subject_screen": _screen,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


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
    duration = min(max(req.duration_minutes, 20), 180)

    prompt = (
        f"You are an outstanding teacher and lesson planning expert. "
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

    plan, provenance = await ai_text(prompt, "education_lesson_plan", realm=req.realm)

    return {
        "plan_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "topic": req.topic,
        "level": req.level,
        "duration_minutes": duration,
        "lesson_plan": plan,
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
    prompt = (
        "You are an experienced, fair teacher and examiner. Mark the student's work against the task and any "
        "rubric, and give warm but honest, actionable feedback. Be specific and point to evidence in the work.\n\n"
        f"Subject: {req.subject}\nLevel: {req.level}\nFeedback tone: {req.tone}\n"
        + (f"Task / question:\n{req.task}\n\n" if req.task else "")
        + (f"Rubric / marking criteria:\n{req.rubric}\n\n" if req.rubric else "")
        + f"STUDENT WORK:\n{req.student_work[:6000]}\n\n"
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

    feedback, provenance = await ai_text(prompt, "education_feedback", realm=req.realm)

    return {
        "feedback_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "level": req.level,
        "tone": req.tone,
        "feedback": feedback,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "disclaimer": (
            "AI-assisted marking and feedback is an aid for the teacher's professional judgement — indicative "
            "only, NOT a final or official grade. The teacher remains responsible for the mark awarded."
        ),
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
    type_prompt = _ASSESSMENT_TYPES.get(
        req.assessment_type,
        f"Create a comprehensive {req.assessment_type.replace('_', ' ')} assessment."
    )

    objectives_context = ""
    if req.learning_objectives:
        objectives_context = f"Learning objectives being assessed:\n" + "\n".join(f"- {o}" for o in req.learning_objectives) + "\n\n"

    prompt = (
        f"You are an expert assessment designer.\n"
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

    assessment, provenance = await ai_text(prompt, "education_assessment", realm=req.realm)

    return {
        "assessment_id": uuid.uuid4().hex[:10],
        "subject": req.subject,
        "topic": req.topic,
        "level": req.level,
        "assessment_type": req.assessment_type,
        "assessment": assessment,
        "ai_provenance": provenance,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
