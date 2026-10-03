"""The path from a cognitive engine to a model — through the tier router (FU-275, P3.20).

WHAT WAS MEASURED, AND IT IS WHY THIS FILE EXISTS. A grep for gateway|orchestrator|complete( across all
six cognitive engine modules returned ZERO for every one of them: no disabled call, no try/except
around a model, no injection point. The engines were never wired to anything, so this is new wiring
rather than repair, and the item's own diagnosis was "the architecture routes and the cognition does not
compute".

WHAT WIRING IT DOES AND DOES NOT MEAN, said plainly because the difference is the whole point. An engine
now HAS a path. On this machine that path currently ends at the deterministic floor, because the tier
router finds no tier above the floor holding a resource — no local model is pulled and reachable, and
every higher tier is not runnable here for a measured reason. SO THE ANSWERS DO NOT CHANGE TODAY. What
changes is that the engine can say WHY: it carries the tier that was chosen, what was rejected on the
way down, and what served the text. A reasoning step with no provenance cannot be told from the floor
composing headings, and until now there was nothing to tell them apart with.

AND NO CONFIDENCE IS INVENTED. Nothing here computes one, so `confidence` stays None with its basis —
the three-state field P3.12 fought for. A path to a model is not a reason to start producing a number.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

#  What an engine is asking for, so the router can choose a tier. Keyed by engine, because an engine
#  knows what KIND of work it does and the router knows what the machine can serve.
ENGINE_DOMAIN: Dict[str, str] = {
    "aqal": "classification",       # formal logic over stated goals — a routing-shaped task
    "inkashaf": "research",         # discovery across sources
    "samajh": "classification",     # comprehension of a stated input
    "soch": "research",             # deliberate reasoning
    "hoshiyari": "classification",  # vigilance / signal detection
    "iman": "classification",       # coherence against stated principles
}


async def serve(engine: str, prompt: str, *, risk: str = "normal",
                owner_id: Optional[str] = None) -> Tuple[Optional[str], Dict[str, Any]]:
    """Ask the router for a tier and, if one holds a model, call it. Returns (text|None, provenance).

    text is None when no tier above the floor could serve — which is the ordinary outcome here, and the
    provenance says exactly why rather than leaving the caller to guess. NEVER RAISES into an engine: a
    reasoning step must not fail because the fabric could not be consulted, and a failure to consult is
    recorded as a provenance fact instead.
    """
    prov: Dict[str, Any] = {"engine": engine, "served_by": None, "is_external": False}
    try:
        from agentic_core.ai.native.tiers import route as _route
    except Exception as e:                       # noqa: BLE001
        prov["routing_basis"] = (
            f"NOT ROUTED: the tier router could not be imported ({e.__class__.__name__}), so no tier "
            f"was chosen and nothing was asked. This is a statement about the fabric, not about the "
            f"request")
        return None, prov

    domain = ENGINE_DOMAIN.get(engine, "classification")
    try:
        decision = _route(domain, risk)
    except Exception as e:                       # noqa: BLE001
        #  THE CALL, NOT ONLY THE IMPORT. The first version of this function guarded the import and
        #  left the call bare, so a router that raised went straight into the engine — while this
        #  module's own docstring said it never raises into one. Caught by the guard that drives a
        #  broken router, which is the only way an over-claim like that gets found.
        prov["routing_basis"] = (
            f"NOT ROUTED: the tier router raised {e.__class__.__name__} when asked, so no tier was "
            f"chosen and nothing was asked of any model. A reasoning step does not fail because the "
            f"fabric could not be consulted; the failure is recorded here instead")
        prov["model_asked"] = False
        prov["basis"] = prov["routing_basis"]
        return None, prov
    prov["tier"] = decision.get("tier")
    prov["tier_wanted"] = decision.get("wanted")
    prov["tier_fell_back"] = decision.get("fell_back")
    prov["rejected_tiers"] = [{"tier": c["tier"], "why_not": c["why_not"]}
                              for c in decision.get("considered") or []]
    prov["routing_basis"] = decision.get("basis")

    if decision.get("tier") == "deterministic_logic":
        #  THE ORDINARY OUTCOME ON THIS MACHINE, and it is a routed decision rather than an absence.
        prov["served_by"] = "native-floor"
        prov["model_asked"] = False
        prov["basis"] = (
            "NO MODEL WAS ASKED. The router walked down from the tier this engine's work wants and "
            "reached the deterministic floor, rejecting each tier above it for a measured reason "
            "(above). The engine HAS a path now; the path ends at the floor on this machine. That is "
            "different from having no path, which is what was measured here before: a grep for a "
            "gateway, an orchestrator or a generate call across all six engines returned zero")
        return None, prov

    #  A tier above the floor holds a resource, so ask it.
    prov["model_asked"] = True
    try:
        from agentic_core.api._ai_provenance import ai_text
        text, served = await ai_text(prompt, agent=f"cognitive_{engine}", owner_id=owner_id,
                                     augment=False)
        prov["served_by"] = served.get("served_by")
        prov["is_external"] = bool(served.get("is_external"))
        prov["basis"] = (
            f"the router chose {decision.get('tier')} and the call was served by "
            f"{prov['served_by']!r}. The tier's choice and every rejection above it are recorded, so a "
            f"reader can tell this from the floor composing headings")
        return (text or None), prov
    except Exception as e:                       # noqa: BLE001
        prov["served_by"] = None
        prov["model_asked"] = True
        prov["basis"] = (
            f"the router chose {decision.get('tier')} and THE CALL FAILED "
            f"({e.__class__.__name__}). A failed call is not a floor serve and is not an answer; it is "
            f"recorded as a failure so that nothing downstream reads the absence as a composition")
        return None, prov


def floor_basis(prov: Dict[str, Any]) -> str:
    """The sentence an engine puts on a response when no model served it.

    It replaces the one P3.12 wrote — "this engine has no path to a model" — which was TRUE then and is
    not true now. Keeping it would be the stale-claim defect this programme removes everywhere else.
    """
    return (prov.get("basis")
            or prov.get("routing_basis")
            or "not computed, and no routing decision was recorded — which is itself a gap")
