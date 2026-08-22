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
