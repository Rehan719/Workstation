"""BOTH OPTIONS, WHERE A TOOL IS OFFERED - the tier of review it has reached, and the option of a qualified person
with when one is warranted.

OWNER RULING 2026-10-12 (P5.15, RELEASE): a free tool of Workstation's own may be released on the second tier
alone - every answer saying it was reviewed by Workstation's specialist agent and not by a qualified person, and
only once that agent is calibrated - except four that keep a person: religious content (a named scholar approves
model-written text), a clinical score used in someone's direct care, regulated advice (which stays a route), and
real money. BOTH OPTIONS ARE SHOWN wherever a tool is offered: the tier it has reached, and the option of a
qualified person with when one is warranted. Release itself remains the Owner's switch.

Until W925 the tier was said only UNDER an answer (W688), so a person chose a tool, typed into it and ran it before
reading what review stood behind it, and nothing anywhere said when a person should look at what it gave.

    GET /api/v1/review-options?endpoint=/api/v1/care/care-plan

THE TOOL. Each domain route DECLARES the tool it is, on its own decorator: openapi_extra {"x-review-tool": <name>},
the name its answers' provenance carries and the key the records of review are filed under. tool_at() reads that
declaration from the application's own routes, so nothing here keeps a second list of endpoints. test_w925 holds
every declaration to the name the route passes to ai_text, and every tool a page offers to an answer from here.

THE TIER is review_statement(), the one function every answer already passes through - never a second reading.

THE PERSON. One statement per discipline: what the option is, when a person is warranted, and what release
leaves with a person. The release sentences carry the Owner's four exceptions. When a person is warranted is
Workstation's own statement (W925): conservative, claiming no professional's role, and saying nothing about any
person having looked at anything. A discipline with no statement is said to have none; nothing is guessed for it.

This module reads and states. It records nothing, arranges no person, and releases nothing.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Request

from agentic_core.api._review_tier import review_statement

router = APIRouter(prefix="/api/v1/review-options", tags=["review-cell"])

TOOL_KEY = "x-review-tool"

OPTION = ("A qualified person's review is an option for anything this tool gives. Workstation does not arrange one. "
          "When a person signs a review of this tool, it is recorded as the third tier, with their credential as "
          "they stated it.")
#  the generic release sentence (the ruling's rule), and the four exceptions that keep a person (the ruling's own)
RELEASE = ("Release is the Owner's switch. A released tool may answer on the review of Workstation's calibrated "
           "specialist agent alone, and each answer then says that no qualified person reviewed it.")
BASIS = ("The release sentence is the Owner's ruling of 2026-10-12 (P5.15). When a person is warranted is "
         "Workstation's own statement (W925): it claims no professional's role, and it does not say that any "
         "person has reviewed anything.")

PERSON: Dict[str, Dict[str, Any]] = {
    "care": {
        "warranted_when": ("Before anything it gives is used in a person's direct care, a registered professional "
                           "who knows that person checks it."),
        "release": ("Release is the Owner's switch. Even then, a clinical score used in someone's direct care keeps "
                    "a qualified person."),
        "kept_by_the_ruling": "a clinical score used in someone's direct care",
    },
    "law": {
        "warranted_when": ("Before you act on it in your own matter, rely on it for a time limit, or sign or send "
                           "anything it drafts, take it to a solicitor or another regulated adviser."),
        "release": ("Release is the Owner's switch. Even then, regulated legal advice stays a route to people: this "
                    "tool does not give it."),
        "kept_by_the_ruling": "regulated advice, which stays a route",
    },
    "religion": {
        "warranted_when": "Before you rely on an answer for a ruling on your own situation, ask a qualified scholar.",
        "release": ("Release is the Owner's switch. Even then, model-written religious text keeps a named "
                    "scholar's approval."),
        "kept_by_the_ruling": "religious content: a named scholar approves model-written text",
    },
    "education": {
        "warranted_when": ("Before a mark, a judgement or a plan from it counts for a learner, or is used with a "
                           "child, a qualified teacher checks it."),
        "release": RELEASE,
        "kept_by_the_ruling": None,
    },
    "employment": {
        "warranted_when": ("Before you rely on it for a contract, pay, a dismissal or a dispute with an employer, "
                           "take it to an employment adviser or a solicitor: those are legal questions."),
        "release": RELEASE,
        "kept_by_the_ruling": None,
    },
    "science": {
        "warranted_when": ("Before a design from it is carried out with people or animals, or a result is relied "
                           "on for health or safety, a qualified person and any approval the work needs come first."),
        "release": RELEASE,
        "kept_by_the_ruling": None,
    },
}
#  the router a tool is mounted under, to the discipline whose statement it carries (the career tools are the
#  Employment page's own)
DISCIPLINE_OF_ROUTER = {"care": "care", "law": "law", "religion": "religion", "education": "education",
                        "employment": "employment", "career": "employment", "science": "science"}


def tool_at(app: Any, endpoint: str) -> Optional[str]:
    """The tool a POST route at `endpoint` declares, read from the application's own routes; None when none does."""
    from fastapi.routing import APIRoute
    for r in getattr(app, "routes", []) or []:
        if isinstance(r, APIRoute) and r.path == endpoint and "POST" in (r.methods or set()):
            declared = (r.openapi_extra or {}).get(TOOL_KEY)
            if declared:
                return str(declared)
    return None


def discipline_of(endpoint: str) -> Optional[str]:
    m = re.match(r"^/api/v1/([a-z0-9-]+)/", str(endpoint or ""))
    return DISCIPLINE_OF_ROUTER.get(m.group(1)) if m else None


def options(tool: str, endpoint: str) -> Dict[str, Any]:
    d = discipline_of(endpoint)
    said = PERSON.get(d or "")
    if said is None:
        person: Dict[str, Any] = {
            "option": OPTION, "warranted_when": None, "release": RELEASE, "kept_by_the_ruling": None,
            "basis": (f"no statement of when a qualified person is warranted exists for the {d or 'unnamed'} "
                      "discipline, so none is given here")}
    else:
        person = {"option": OPTION, **said, "basis": BASIS}
    return {"endpoint": endpoint, "tool": tool, "discipline": d, "review": review_statement(tool), "person": person}


@router.get("")
async def review_options(endpoint: str, request: Request):
    """Both options for the tool offered at `endpoint`: the tier of review it has reached, and the option of a
    qualified person with when one is warranted. An endpoint that declares no tool is refused by name - it is never
    answered with a default tier."""
    tool = tool_at(request.app, endpoint)
    if not tool:
        raise HTTPException(status_code=404, detail=(
            f"No tool is declared at {endpoint}, so no tier of review or option of a person can be stated for it."))
    return options(tool, endpoint)
