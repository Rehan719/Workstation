"""
§4.2 (W428) — EXPLICIT user context for generation. The user's own words, never recall.

"Understand the person" never happened at the front door: no profile, goals, constraints or success
criteria reached any prompt, and there was no field to enter them.

This is deliberately NOT the recall path. `gateway._augment` retrieves prior interactions by token
overlap, and every generation-class caller passes `augment=False` under W332 because "recall was the
leak vector" — content the SYSTEM chose, drawn from other requests. What this module supplies is the
opposite: a short profile the USER wrote, can read back, and can delete. One is inference over other
people's traffic; the other is the person telling you about themselves.

THE LINE THAT DECIDES WHETHER THIS IS SAFE is `profile_owner`. With auth OFF every record is written
under "default". If this fell back to "default" when the caller is unidentified, then the day
AUTH_ENABLED is switched on, the single-user owner's private profile would be injected into EVERY
tenant's generation. So the auth-on branch returns None — no identity, no profile — and never a
fallback. That is the whole reason this function exists rather than a bare `owner_id or "default"`.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Optional

# The five fields §4.2 asks for. Capped hard: this is a preamble, not a document store, and an
# unbounded profile would push the real request out of a local model's context window.
PROFILE_FIELDS: tuple[str, ...] = (
    "about_you", "context", "goals", "constraints", "success_criteria",
)
FIELD_LABELS: Dict[str, str] = {
    "about_you": "About the person",
    "context": "Their situation",
    "goals": "What they are trying to achieve",
    "constraints": "Constraints they are working under",
    "success_criteria": "What success looks like to them",
}
MAX_FIELD_CHARS = 600
MAX_PREAMBLE_CHARS = 2_000


def profile_owner(owner_id: Optional[str]) -> Optional[str]:
    """Which stored profile (if any) may be applied to a request from this caller.

    Returns None when no profile may be applied. NEVER returns "default" under auth — see the
    module docstring; that fallback is the leak.
    """
    from agentic_core.auth.core import auth_enabled

    if auth_enabled():
        # Authenticated deployments: a profile belongs to exactly one username. An unidentified
        # caller gets NO profile — not the single-user one that happens to be sitting in the store.
        return owner_id or None
    # Single-user mode: one human, one profile, stored under the same "default" every other
    # single-user record uses.
    return owner_id or "default"


# engine.py:92 — r"(?:You are|As)\s+(?:the|a|an)\s+([A-Za-z]…)". It SEARCHES, so the trigger counts
# anywhere in the text, not just at the start. A first version of `_clean` only checked the start and
# was demonstrably defeated: a profile reading "As a busy founder…" changed the engine's role from
# "IDBO Conceptualisation engine" to "busy founder". Neutralise the trigger TOKEN wherever it sits.
_ROLE_TRIGGER = re.compile(r"\b(you\s+are|as)(\s+(?:the|a|an)\b)", re.I)
_ROLE_SAFE = {"you are": "they are", "as": "being"}


def _deperson(s: str) -> str:
    """Rewrite persona openers into equivalent non-trigger phrasing, preserving the meaning.

    "As a busy founder" -> "being a busy founder"; "You are the lead" -> "they are the lead".
    """
    return _ROLE_TRIGGER.sub(
        lambda m: _ROLE_SAFE[re.sub(r"\s+", " ", m.group(1).lower())] + m.group(2), s)


def _clean(value: Any) -> str:
    """One line, capped, with nothing that could be read as another field or a persona.

    Three rules, each a measured property of the owned native floor:
      · newlines collapse — engine.py:81 `_field` reads a labelled value to END OF LINE, so a
        newline inside a value silently truncates it and leaves the remainder floating as prose.
      · an interior "Label:" is neutralised — otherwise one field's text becomes another field.
      · persona triggers are rewritten ANYWHERE in the value, per `_deperson` above.
    """
    s = " ".join(str(value or "").split())
    if not s:
        return ""
    s = s.replace(":", " -")           # no interior label can be forged out of a value
    return _deperson(s)[:MAX_FIELD_CHARS]


def build_preamble(profile: Optional[Dict[str, Any]]) -> str:
    """Render a stored profile as a prompt PREFIX. Returns "" when nothing is set.

    Imperative framing, never a persona, for the `_role` reason above. Labelled one-per-line so the
    floor can read the fields rather than swallowing them into a single value.
    """
    if not isinstance(profile, dict):
        return ""
    lines = []
    for key in PROFILE_FIELDS:
        val = _clean(profile.get(key))
        if val:
            lines.append(f"{FIELD_LABELS[key]}: {val}")
    if not lines:
        return ""
    body = "\n".join(lines)[:MAX_PREAMBLE_CHARS]
    return ("Take the following into account; it was written by the person you are answering.\n"
            + body + "\n\n")


def load_preamble(owner_id: Optional[str]) -> str:
    """The explicit preamble for this caller, or "" — never raises, never guesses.

    A missing store, an unreadable document or no profile at all all mean the same thing: no
    preamble. Generation must never fail because a convenience store is unavailable.
    """
    owner = profile_owner(owner_id)
    if not owner:
        return ""
    try:
        from agentic_core.api.user_workspace import _load
        return build_preamble((_load(owner) or {}).get("profile"))
    except Exception:
        return ""
