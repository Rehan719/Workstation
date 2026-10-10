"""
Shared helper: run a completion on Workstation's OWN native fabric and return the text plus
in-house provenance. Used by the Domain routers (Law/Science/Care/Education/Religion/Employment)
so every AI-mediated domain response demonstrably runs in-house (served_by) — same contract as
Forge/Genesis. In-house-first; never a dependency on an external provider.
"""
from __future__ import annotations

import contextvars
import re
import time
from typing import Any, Dict, Tuple

from agentic_core.ai.gateway import gateway


#  P3.6 clause (2) — THE REQUEST'S LANGUAGE, CAPTURED ONCE. DomainTool sends `Accept-Language`; the
#  middleware in app_mvp puts it here; `ai_text` reads it below. A ContextVar is used rather than a body
#  field because every domain route declares its own Pydantic model and an undeclared field is silently
#  dropped - so a body field would mean editing six models to carry one string, while this needs none.
#  ContextVars propagate into the request's own task, so this is per-request and not shared.
_REQUEST_LANGUAGE: "contextvars.ContextVar[str]" = contextvars.ContextVar("ws_request_language", default="")


#  W619 (FU-501, M2 v8 R5.2) — THE AUTHENTICATED CALLER, CAPTURED THE SAME WAY. The six domain routers declare
#  no user dependency, so with authentication on `ai_text` was called with owner_id=None, `profile_owner`
#  returned None ("an unidentified caller gets NO profile") and the saved profile reached none of the 35 tools,
#  while Settings says it shapes what the platform generates. The middleware resolves the bearer token it
#  already sees into this; a token that does not resolve leaves it empty, which is the old behaviour.
FLOOR_NOTE = ("Composed by the native floor, not by a model: the headings are a structure filled with terms "
              "taken from your input. NO research, legal or clinical analysis, guidance, marking, market data or "
              "safeguarding assessment was performed - read it as an outline to work from, not as an answer.")


def is_floor_served(served_by: Any) -> bool:
    return str(served_by or "native").startswith("native")


_REQUEST_USER: "contextvars.ContextVar[str]" = contextvars.ContextVar("ws_request_user", default="")


def set_request_user(username: str) -> None:
    _REQUEST_USER.set(str(username or "").strip())


def request_user() -> str:
    try:
        return _REQUEST_USER.get()
    except LookupError:          # pragma: no cover
        return ""


def set_request_language(value: str) -> None:
    """Called by the HTTP middleware, once per request."""
    _REQUEST_LANGUAGE.set(str(value or "").strip())


def request_language() -> str:
    """The language this request asked for, or "" when it asked for none."""
    try:
        return _REQUEST_LANGUAGE.get()
    except LookupError:          # pragma: no cover - a default is declared, so this cannot normally fire
        return ""


#  W642 (FU-651, ledger v14 R5) - ONE HOME FOR WHAT A FLOOR-SERVED TOOL SAYS ABOUT ITSELF. Six domain tools
#  printed a disclaimer written for model output ("AI-generated", "AI-assisted marking", "Reasoned ...") when
#  the native floor had served them, and the page appends that sentence to every copy, download and saved
#  record. The safety half of each disclaimer is true either way and is kept; the claim half follows what served.
FLOOR_DISCLAIMER = ("Composed by the native floor, not by a model: a structured frame, with nothing generated, "
                    "reasoned or interpreted by AI.")


def disclaimer_for(provenance: dict | None, model_claim: str, safety: str) -> str:
    """`model_claim` when a model served, the floor's own statement when the floor did; then `safety`."""
    on_floor = bool((provenance or {}).get("floor_note"))
    return f"{FLOOR_DISCLAIMER if on_floor else model_claim} {safety}".strip()


def person_said(*parts) -> str | None:
    """The person's OWN words for one call, from the request fields the handler names - the statement the
    native floor needs before it attributes a subject or a term to anybody (W640).

    Each handler names the fields; nothing is inferred here. Strings and lists of strings are joined; anything
    else is ignored rather than stringified, because the repr of a dict is not something a person wrote.
    Returns None when nothing was said, and None is what makes the floor withhold."""
    out: list[str] = []
    for part in parts:
        for item in (part if isinstance(part, (list, tuple)) else [part]):
            if isinstance(item, str) and item.strip():
                out.append(" ".join(item.split()))
    #  one field per LINE: the floor builds phrases within a line and never across two fields
    return chr(10).join(out) if out else None


async def ai_text(prompt: str, agent: str, timeout: float = 30.0,
                  owner_id: str | None = None, augment: bool = False,
                  realm: str = "", domain: str = "",
                  user_text: str | None = None) -> Tuple[str, Dict[str, Any]]:
    """Return (text, provenance) where provenance = {posture, served_by, is_external}.

    Every call is recorded into the operational-excellence learning loop (best-effort, non-critical)
    so rankings/summary reflect REAL platform AI usage — which OWNED resource served each domain tool,
    how often, how fast, in-house vs external — not just swarm runs.

    W332/W333 — Offering-1 output is a deliverable that the user SEES and SAVES, so recall injection
    (the cross-tenant leak) is off here (`augment=False`). Since W489 that is also the GATEWAY's
    default on all four entry points, so this is belt-and-braces rather than the only thing stopping
    it; when a caller opts into recall it is tenant-scoped by `owner_id`. Domain routers thread the
    authenticated user's id."""
    # W505 (P2.5) — THE REALM AXIS REACHES OFFERING-1. taxonomy.py states that "realm changes the DEPTH
    # and REGISTER of what is generated", and `realm_directive` reached deliverables, ceo_generate, genesis
    # and projects — never the six domain tools, which are the surfaces a user actually types into. This is
    # the seam every one of them calls, so the directive is applied once here. An empty realm changes
    # nothing, so a caller that has no realm to send behaves exactly as before.
    if str(realm or "").strip():
        from agentic_core.taxonomy import normalise_realm, realm_directive
        prompt = f"{realm_directive(normalise_realm(realm))}\n\n{prompt}"
    #  W637 (FU-597) — THE ROUTER SAYS WHICH DOMAIN IT IS. The native floor prints a `Domain:` field and
    #  otherwise "WITHHELD — the request named no domain"; none of the five domain routers wrote one, so a law
    #  analysis told its reader the request named no domain. Written here, once, from an argument each router
    #  binds explicitly — never inferred from the agent's name — and only when the prompt carries no Domain
    #  line of its own, so a tool that names a narrower domain keeps it.
    if str(domain or "").strip() and not re.search(r"(?m)^[ \t]*Domain[ \t]*:", prompt):
        prompt = f"Domain: {domain.strip()}\n{prompt}"
    t0 = time.monotonic()
    owner_id = owner_id or request_user() or None     # W619 (FU-501) — the authenticated caller, when there is one
    res = await gateway.query_meta(prompt, agent=agent, timeout=timeout,
                                   owner_id=owner_id, augment=augment, user_text=user_text,
                                   #  P3.6 clause (2) — the request's own language, so the output can be
                                   #  labelled when it is not delivered in it ("the defect is silent
                                   #  English"). One seam, so all six domain tools are covered at once.
                                   language=request_language())
    output = res.get("output", "")
    served_by = res.get("served_by", "native")
    is_external = bool(res.get("is_external"))
    try:
        from agentic_core.api.operational_excellence import record_outcome
        record_outcome("ai_call", f"agent:{agent}", served_by=served_by, is_external=is_external,
                       # W495 (FU-125, S7.3) — this wrapper sees no quality gate at all, so it records
                       # that the run PRODUCED output and leaves the verdict unset (NOT ASSESSED) rather
                       # than filing "the floor returned text" as a success.
                       duration_ms=int((time.monotonic() - t0) * 1000), success=bool(output),
                       quality_gate=None)
    except Exception:
        pass
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": served_by,
                                  "is_external": is_external,
                                  #  P3.6 clause (2) — the verdict travels WITH the provenance the page
                                  #  already renders, so a reader sees it rather than it sitting in the API
                                  "language_requested": res.get("language_requested"),
                                  "language_delivered": res.get("language_delivered"),
                                  "language_basis": res.get("language_basis"),
                                  #  W638 (FU-598) — the profile verdict travels the same way. The gateway
                                  #  computes it on every response and this fixed key set dropped it, so
                                  #  only the avatar told a user their saved profile had not shaped a
                                  #  floor-served answer.
                                  "profile_applied": res.get("profile_applied"),
                                  "profile_state": res.get("profile_state"),
                                  "profile_basis": res.get("profile_basis")}
    #  W627 (FU-536) - every domain tool's floor output said so only through a badge, while its headings
    #  ('Relevant Law', 'Who to Notify', 'Target Range') and a static "AI-generated" disclaimer described
    #  research, guidance and marking that did not happen. The note rides the provenance EVERY domain router
    #  returns, so no router can omit it; Religion's tools already withhold sections and say so.
    if is_floor_served(served_by):
        provenance["floor_note"] = FLOOR_NOTE
    # §10×§11 (W308) — Offering-1 GATED: every domain-tool / refine response passes the SAME living
    # QMS + compliance gate as the cascade and deliverables (assure_delivery). FLAG, never block:
    # the user always gets their output; the quality/compliance posture rides on the provenance the
    # UI already renders. Failures open traceable QMS defects (label = the serving agent).
    try:
        from agentic_core.vbs.quality import assure_delivery
        # §10 (W449, ledger 1.1) — coverage is measured against the sections the PROMPT declared (the
        # same "## " extraction the floor itself uses), never against None (which collapsed to a
        # 200-character length check); and served_by reaches the gate, so floor output is recorded
        # "not assessable" — never "pass" beside a clinical or Quranic scaffold.
        from agentic_core.ai.native.engine import _sections as _prompt_sections
        _qa = (await assure_delivery(output, _prompt_sections(prompt) or None, label=f"tool:{agent}",
                                     served_by=served_by))["quality"]
        provenance["quality_assurance"] = {
            "qms_gate_passed": _qa.get("qms_gate_passed"),
            "qms_basis": _qa.get("qms_basis"),
            "delivery_coverage": _qa.get("delivery_coverage"),
            "stub_found": _qa.get("stub_found"),
            "compliance_overall": (_qa.get("compliance") or {}).get("overall"),
            "quality_record_hash": _qa.get("quality_record_hash"),
        }
    except Exception as exc:   # the gate itself must never cost the user their output
        provenance["quality_assurance_error"] = str(exc)
    return output, provenance
