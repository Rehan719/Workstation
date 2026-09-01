"""
§17.1 — the CANONICAL Workstation IDBO taxonomy (W311).

ONE module owns the Realm × Domain definitions; every other module imports from here instead of
re-declaring its own variant (the audit found drifted literals — five-realm lists, wrong names).
The Whole Vision §2: 4 Realms × 6 Domains.
"""
from __future__ import annotations

REALMS: tuple[str, ...] = ("enterprise", "learning", "developing", "scholarship")
DOMAINS: tuple[str, ...] = ("religion", "science", "education", "law", "employment", "care")

REALM_LABELS: dict[str, str] = {
    "enterprise": "Enterprise", "learning": "Learning",
    "developing": "Developing", "scholarship": "Scholarship",
}
DOMAIN_LABELS: dict[str, str] = {
    "religion": "Religion", "science": "Science", "education": "Education",
    "law": "Law", "employment": "Employment", "care": "Care",
}


# §17.1 (W427) — REALM WITH TEETH. Realm was validated, stored, echoed and displayed across ~46
# files while NOTHING branched on it: `deliverables._generate` took no realm at all, and not one of
# Genesis's eight stage prompts mentioned it. One of three axes of the product grid changed no
# decision anywhere.
#
# The Owner's approved scope is deliberately NARROW — realm changes the DEPTH and REGISTER of what
# is generated, not the structure. No per-realm routes, no per-realm stores, no forked journey.
#
# Two hard constraints, both measured against the owned native floor and both easy to get wrong:
#   · NEVER open with "You are …" / "As a …". engine.py:90 `_role` takes the FIRST match of
#     r"(?:You are|As)\s+(?:the|a|an)\s+…", and this text is PREPENDED — so a persona sentence here
#     would REPLACE the caller's own role and silently rewrite what the engine thinks it is doing.
#     Every directive below is imperative ("Write for …"), never a persona.
#   · One `Label: value` per line, and no value may contain a second `Label:`. engine.py:81 `_field`
#     reads to end of line and caps at 140 chars, so `Realm: x · Domain: y` fuses into one value.
REALM_REGISTER: dict[str, str] = {
    "enterprise": (
        "Write for a commercial operator who has to act on this. Lead with the decision and its "
        "cost, keep evidence tight, and prefer concrete numbers, timelines and owners over "
        "explanation of fundamentals."
    ),
    "learning": (
        "Write for someone building understanding. Define each term where it first appears, work "
        "from the familiar to the unfamiliar, and show the reasoning rather than only the "
        "conclusion. Prefer one worked example over three abstract ones."
    ),
    "developing": (
        "Write for a resource-constrained setting. Assume limited capital, intermittent "
        "infrastructure and thin specialist staffing; prefer what can be run and maintained "
        "locally, name what each step actually requires, and offer a low-resource path first."
    ),
    "scholarship": (
        "Write for a scholarly reader. State claims precisely, separate what is established from "
        "what is inferred, name the limits of the evidence and the competing readings, and prefer "
        "accuracy and qualification over confident summary."
    ),
}


def realm_directive(realm: str) -> str:
    """The DEPTH + REGISTER instruction for a realm — safe to prepend to any generation prompt.

    Routes through `normalise_realm`, so an unknown realm falls back to the canonical default
    rather than silently contributing nothing.
    """
    return REALM_REGISTER[normalise_realm(realm)]


def is_realm(value: str) -> bool:
    return str(value).strip().lower() in REALMS


def is_domain(value: str) -> bool:
    return str(value).strip().lower() in DOMAINS


def normalise_realm(value: str, default: str = "enterprise") -> str:
    v = str(value or "").strip().lower()
    return v if v in REALMS else default


def normalise_domain(value: str, default: str = "enterprise") -> str:
    """Domains normalise to themselves; anything else passes through unchanged when it is a
    genuine free-text domain (e.g. 'enterprise' used as a general workspace) — the taxonomy is
    canonical for the 6 named Domains, not a straitjacket on general-purpose flows."""
    v = str(value or "").strip().lower()
    return v if v in DOMAINS else (v or default)
