"""Niyyah — intent ratification whose quorum is COUNTED from the signatures supplied, and never invented.

P3.13. The archived version (_archive/jules-unwired/agentic_core/cognitive/meta/niyyah_engine.py, 7 lines)
returned `{"ratified": True, "signatures": [...three names...], "intent_status": "COMMITTED"}` — it
FABRICATED three signatories and ratified unconditionally. That is the worst of the three archived meta
engines, because a clearance chain consuming it would clear on evidence that does not exist. It is not
recovered; only its metadata is kept (engine id, the anterior-cingulate analogue, bindings 2/14/17).

THE ONE INVARIANT THIS ENGINE EXISTS TO HOLD: every name it reports came out of its input. There is no code
path here that can produce a signatory the caller did not supply, and the guard asserts that directly.

MISSING IS NOT ZERO, and this is the distinction the whole engine turns on. An absent `signatures` key is a
REFUSAL — nothing was recorded, so nothing can be counted. A `signatures` list that is PRESENT and empty is a
measured zero: assessable, counted, and not ratified. Collapsing those two into "0 signatures" is how a
missing record comes to read as a negative finding.

A QUORUM IS NEVER DEFAULTED. If the caller states no quorum, this refuses, because any default would decide
ratification by itself — the number is the whole verdict.
"""
from typing import Any, Dict, List

from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.consultation.interface import (ConsultationRequest, ConsultationResponse,
                                                 ValidationResult)
from agentic_core.consultation.constitutional_screen import screen as _constitutional_screen

ENGINE_ID = "niyyah"
BIOLOGICAL_ANALOGUE = "anterior_cingulate_cortex"
CONSTITUTIONAL_BINDING = [2, 14, 17]


class NiyyahEngine:
    """Intent ratification. Counts what it was given; names nobody it was not given."""

    def __init__(self, ueg=None):
        self.ueg = ueg

    @constitutional_guard
    async def ratify(self, signatures: Any, quorum_required: Any) -> Dict[str, Any]:
        """Count distinct signatories against a stated quorum, or refuse and say which input was missing."""
        if signatures is None:
            return {"assessable": False,
                    "basis": ("no signatures were recorded at all: an absent record is not an empty one, "
                              "so this cannot be counted as zero signatories")}
        if not isinstance(signatures, list):
            return {"assessable": False,
                    "basis": f"signatures is not a list but a {type(signatures).__name__}"}
        if quorum_required is None:
            return {"assessable": False,
                    "basis": ("no quorum was stated, and a quorum cannot be assumed: the number IS the "
                              "verdict, so a default would decide ratification by itself")}
        if isinstance(quorum_required, bool) or not isinstance(quorum_required, int) or quorum_required < 1:
            return {"assessable": False,
                    "basis": f"the stated quorum is not a positive whole number: {quorum_required!r}"}

        signatories: List[str] = []
        unusable = 0
        for entry in signatures:
            name = entry.get("signatory") if isinstance(entry, dict) else None
            if isinstance(name, str) and name.strip():
                signatories.append(name.strip())
            else:
                unusable += 1

        distinct = sorted(set(signatories))
        duplicates = len(signatories) - len(distinct)

        return {
            "assessable": True,
            "ratified": len(distinct) >= quorum_required,
            # EVERY name in this list was read out of `signatures`. Nothing here is generated.
            "signatories": distinct,
            "distinct_count": len(distinct),
            "quorum_required": quorum_required,
            "duplicates_ignored": duplicates,
            "unusable_entries": unusable,
            "basis": (
                f"{len(distinct)} distinct signator{'y' if len(distinct) == 1 else 'ies'} counted from "
                f"{len(signatures)} supplied entr{'y' if len(signatures) == 1 else 'ies'}, against a stated "
                f"quorum of {quorum_required}"
                + (f"; {duplicates} duplicate signature(s) counted once" if duplicates else "")
                + (f"; {unusable} entr{'y' if unusable == 1 else 'ies'} named no signatory and "
                   "were not counted" if unusable else "")
                + ("; the list was present and empty, which is a measured zero rather than a missing record"
                   if not signatures else "")),
            "what_this_does_not_establish": (
                "that a signature is authentic. This counts distinct names as supplied; it performs no "
                "signature verification, so a ratification here means a quorum of NAMES was recorded, not "
                "that a quorum of parties was cryptographically proven (that is P3.15)"),
        }

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        ctx = request.context or {}
        res = await self.ratify(ctx.get("signatures"), ctx.get("quorum_required"))
        ok = res.get("assessable") is True

        if not ok:
            answer = f"Not assessable: {res['basis']}"
        else:
            answer = (f"Intent {'RATIFIED' if res['ratified'] else 'NOT ratified'}: "
                      f"{res['distinct_count']} of {res['quorum_required']} required")

        _resp = ConsultationResponse(
            engine=ENGINE_ID,
            answer=answer,
            confidence=None,
            confidence_basis=(
                "not applicable: a quorum count is arithmetic over the signatures supplied, not an "
                "estimate, so there is no confidence to state"
                if ok else f"nothing was counted: {res['basis']}"),
            served_by="native-computed" if ok else "native-refused",
            is_external=False,
            constitutional_validation=ValidationResult(),
            reasoning_trace=res["basis"],
            metadata=res,
        )
        #  P3.28 clause (1) — the verdict is COMPUTED by gaas.v5's own checks over the request and
        #  this answer, replacing a literal that said no check ran. A screen may refuse, never clear:
        #  a non-refusal keeps passed=None and states its coverage (consultation/constitutional_screen.py).
        _resp.constitutional_validation = _constitutional_screen(ENGINE_ID, request.query, _resp.answer)
        return _resp
