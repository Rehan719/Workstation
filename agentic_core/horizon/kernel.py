"""The Horizon kernel: observe, compress (three-state), decide from stated terms.

Every state this module can report is reachable through agentic_core/api/horizon.py, which is what the
item's bar means by REACHABLE — a state a guard can only produce by calling an internal function is a
state no user ever meets.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

#  The three compression states. NOT_COMPRESSED is the ORDINARY one on this deployment.
COMPRESSED = "COMPRESSED"
NOT_COMPRESSED = "NOT_COMPRESSED"

#  The three decision states. There is no fourth, and no score.
PROCEED = "PROCEED"
ESCALATE = "ESCALATE"
NOT_ASSESSABLE = "NOT ASSESSABLE"

#  The domains on which a request that was NOT compressed must escalate rather than proceed. FAIL CLOSED:
#  not understanding a request about money, the law or faith content is precisely when guessing is worst.
#  Taxonomy-free by the Owner's ruling — these are the domains the platform already treats as grave, not
#  a new classification scheme.
ESCALATION_DOMAINS = ("money", "legal", "faith", "medical", "safety")

#  The fields a compression produces. They exist on a record ONLY where a compression produced them: a
#  default in any of these is a claim about a request nobody read.
_COMPRESSION_FIELDS = ("asked_for", "domain", "stakes", "missing", "escalations")

#  served_by values that are NOT a compression. The deterministic floor composes structured output from
#  the request; it infers nothing, so a floor-served run has not compressed anything. 'failed' is a call
#  that raised, and 'none' a call that never happened — neither is a compression either.
_NOT_A_COMPRESSOR = ("native", "template", "failed", "none", "verbatim-ingest", "real-engine")


def _store():
    return data_path("horizon/intent.json")


def _read() -> List[Dict[str, Any]]:
    """STRICT: a store that cannot be read is an error, not an empty history.

    A tolerant read would answer [] for a truncated store, and every figure computed from it would then
    describe a store nobody could read while looking like a quiet period.
    """
    return read_json_strict(_store(), missing=[], expect=list)


def observe(source: str, raw_text: str, surface: str) -> Dict[str, Any]:
    """Record what arrived. NOTHING IS INTERPRETED HERE — that is the whole contract of this step.

    No classification, no domain guess, no stakes estimate. The raw text is kept as given, because the
    only honest account of an observation is the observation.
    """
    return {
        "observation_id": f"obs-{uuid.uuid4().hex[:12]}",
        "source": source,
        "raw_text": raw_text,
        "surface": surface,
        "observed_at": time.time(),
        "basis": ("recorded as received. Nothing is interpreted at this step: no domain, no stakes and "
                  "no intent are inferred from this text here"),
    }


def _compression_of(served_by: Optional[str], is_external: bool, failed: bool,
                    text: str, compressor_called: bool = True) -> Dict[str, Any]:
    """Decide the compression STATE from the provenance of the call that was made.

    This is the function the whole package turns on. It reads WHO SERVED the call rather than whether a
    string came back, because a string always comes back: the deterministic floor returns composed
    structured output for any prompt, and treating that as a compression is exactly the defect the
    brief's hard-coded `compress_noise_to_meaning` committed.
    """
    #  W554 — A FOURTH REASON, and it is a different fact from the other three. The observing seam
    #  (membrane.py) records requests and run outcomes WITHOUT asking any model what they meant, so no
    #  compressor was called at all. Collapsing that into "the floor served it" would attribute the
    #  absence to a component that never ran, and collapsing it into "the call did not produce text"
    #  would describe a call nobody made. The parameter defaults to True, so every existing caller is
    #  unchanged.
    if not compressor_called:
        return {"compression": NOT_COMPRESSED, "served_by": None,
                "compression_basis": (
                    "NOT COMPRESSED: NO COMPRESSOR WAS CALLED ON THIS PATH. This record comes from the "
                    "observing seam, which watches domain requests and run outcomes without asking a "
                    "model what any of them meant — a model call in front of every domain request would "
                    "make each one wait on an LLM, and the only answer available on this deployment "
                    "would come from the deterministic floor, which composes rather than compresses. The "
                    "absence here is the seam's design and is DISTINCT from a call that was made and "
                    "did not compress")}
    if failed or not str(text or "").strip():
        return {"compression": NOT_COMPRESSED, "served_by": served_by,
                "compression_basis": (
                    f"NOT COMPRESSED: the call did not produce text (served_by={served_by!r}, "
                    f"failed={failed}). An absent answer is not a compression")}
    if not served_by or served_by in _NOT_A_COMPRESSOR:
        return {"compression": NOT_COMPRESSED, "served_by": served_by,
                "compression_basis": (
                    f"NOT COMPRESSED: this run was served by {served_by or 'nothing recorded'}, which "
                    f"composes structured output from the request rather than inferring anything. THIS "
                    f"IS THE ORDINARY PATH on this deployment, not an edge case — no model is "
                    f"provisioned, so the honest state is that nobody compressed this request")}
    return {"compression": COMPRESSED, "served_by": served_by,
            "compression_basis": (f"COMPRESSED by {served_by}"
                                  + (" (EXTERNAL accelerant, opt-in)" if is_external else " (in-house)"))}


def _fields_from(text: str) -> Dict[str, Any]:
    """The compression's own fields, parsed from what the model returned.

    Only ever called on a COMPRESSED run. Anything it cannot find is ABSENT from the result rather than
    defaulted, so a model that answered partially cannot have the rest filled in on its behalf.
    """
    out: Dict[str, Any] = {}
    for line in str(text or "").splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower().replace(" ", "_")
        val = val.strip()
        if key in _COMPRESSION_FIELDS and val:
            if key in ("missing", "escalations"):
                out[key] = [p.strip() for p in val.split(";") if p.strip()]
            else:
                out[key] = val
    return out


def build_record(observation: Dict[str, Any], served_by: Optional[str], is_external: bool,
                 failed: bool, text: str, compressor_called: bool = True) -> Dict[str, Any]:
    """An IntentRecord. On a NOT_COMPRESSED run the compression fields are ABSENT, not empty."""
    comp = _compression_of(served_by, is_external, failed, text, compressor_called)
    rec: Dict[str, Any] = {
        "intent_id": f"intent-{uuid.uuid4().hex[:12]}",
        "observation_id": observation.get("observation_id"),
        "surface": observation.get("surface"),
        "source": observation.get("source"),
        "created_at": time.time(),
        **comp,
        "is_external": bool(is_external),
        #  THE USER'S OWN WORDS, and nothing else may write them. None here means the user has not set
        #  one — distinguishable from "" which a writer could mistake for a cleared tag they themselves
        #  stored. Cleared is also None, and `reflection_tag_by` records who last set it.
        "reflection_tag": None,
        "reflection_tag_by": None,
        "reflection_tag_at": None,
        "reflection_tag_basis": (
            "NOT SET: this field holds the USER'S OWN WORDS about their intent and no AI ever writes it. "
            "There is no default, no suggestion is persisted as a value, and nothing is inferred from "
            "the observation's text. Post to /api/v1/horizon/reflection to set or clear it"),
    }
    if comp["compression"] == COMPRESSED:
        _f = _fields_from(text)
        rec.update(_f)
        rec["fields_present"] = sorted(_f)
        rec["fields_absent"] = sorted(set(_COMPRESSION_FIELDS) - set(_f))
        rec["fields_basis"] = (
            f"{len(_f)} of {len(_COMPRESSION_FIELDS)} field(s) came from the compression. Any field not "
            f"listed in fields_present is ABSENT from this record rather than defaulted — a default in "
            f"any of them would be a claim about a request nobody read")
    else:
        rec["fields_present"] = []
        rec["fields_absent"] = sorted(_COMPRESSION_FIELDS)
        rec["fields_basis"] = (
            "NO FIELD IS FILLED: nothing compressed this request, so asked_for, domain, stakes, missing "
            "and escalations are absent rather than empty. An empty string or an empty list here would "
            "read as a finding — that there is nothing missing, or nothing to escalate")
    return rec


def decide(record: Dict[str, Any]) -> Dict[str, Any]:
    """PROCEED | ESCALATE | NOT ASSESSABLE from STATED TERMS, each with its own basis.

    There is no blended score. Three of the four terms the brief wanted to average have no instrument in
    this repository, and averaging an instrument that does not exist with one that does produces a figure
    whose provenance nobody can state. Every term below is reported whether or not it fired, so a reader
    can see which ones were even available.
    """
    terms: List[Dict[str, Any]] = []

    def _term(name: str, fired: Optional[bool], basis: str):
        terms.append({"term": name, "fired": fired, "basis": basis})

    if not isinstance(record, dict) or not record.get("compression"):
        #  NOT ASSESSABLE is not a polite PROCEED. A record this function cannot read yields no decision.
        _term("record_readable", None,
              "the record carries no compression state, so no term below could be evaluated")
        return {"decision": NOT_ASSESSABLE, "terms": terms,
                "basis": ("NOT ASSESSABLE: this is not a request to proceed with. A decision over a "
                          "record that could not be read would be a decision about nothing")}

    _esc = record.get("escalations")
    _has_esc = bool(_esc) if isinstance(_esc, list) else None
    _term("guardrail_escalation", _has_esc,
          (f"the compression raised {len(_esc)} escalation(s): {_esc}" if _has_esc else
           "the compression raised no escalation" if _has_esc is False else
           "NOT AVAILABLE: nothing compressed this request, so no escalation list exists. Its absence is "
           "not an absence of escalations"))

    _missing = record.get("missing")
    _has_missing = bool(_missing) if isinstance(_missing, list) else None
    _term("required_field_missing", _has_missing,
          (f"the compression named {len(_missing)} missing input(s): {_missing}" if _has_missing else
           "the compression named no missing input" if _has_missing is False else
           "NOT AVAILABLE: nothing compressed this request, so no missing-input list exists"))

    _uncompressed = record.get("compression") == NOT_COMPRESSED
    _dom = record.get("domain")
    _grave = (isinstance(_dom, str) and any(d in _dom.lower() for d in ESCALATION_DOMAINS))
    #  FAIL CLOSED, and the honest reading of an unknown domain. On this deployment nothing compresses,
    #  so the domain is usually ABSENT — and an absent domain on an uncompressed request cannot be shown
    #  to be outside the grave set, so it escalates.
    _fail_closed = _uncompressed and (_grave or _dom is None)
    _term("uncompressed_and_grave_or_unknown_domain", _fail_closed,
          (f"nothing compressed this request and its domain is "
           + (f"{_dom!r}, which is on the escalation list" if _grave else
              "UNKNOWN, so it cannot be shown to be outside the escalation list")
           + ". Fail closed: not understanding a request is precisely when proceeding is worst"
           if _fail_closed else
           f"the request was compressed" if not _uncompressed else
           f"nothing compressed this request and its stated domain {_dom!r} is outside the escalation "
           f"list"))

    _fired = [t["term"] for t in terms if t["fired"] is True]
    if _fired:
        return {"decision": ESCALATE, "terms": terms, "fired": _fired,
                "basis": (f"ESCALATE on {len(_fired)} stated term(s): {', '.join(_fired)}. Each term's "
                          f"own basis is above; no term was weighted against another and no score was "
                          f"computed")}
    return {"decision": PROCEED, "terms": terms, "fired": [],
            "basis": ("PROCEED: no stated term fired. The terms that could not be evaluated are reported "
                      "above with fired=None — a term with no instrument is not a term that passed")}


#  W554 — THE STORE IS CAPPED, and it was not before the seam existed. save() appended and rewrote every
#  row, which was tolerable while the only writer was a user POSTing to /observe and became a liability
#  the moment a middleware and a run-outcome hook began writing: an uncapped whole-file read-modify-write
#  grows the cost of every subsequent write. The cap is OLDEST-FIRST, and the listing route says the
#  history is bounded — a reader who is not told a store is capped will read its oldest row as the first
#  thing that ever happened.
_CAP = 2000


def save(record: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    """Persist the record with its decision, under the store lock."""
    row = {**record, "decision": decision.get("decision"), "decision_terms": decision.get("terms"),
           "decision_basis": decision.get("basis")}
    with store_lock(_store()):
        rows = _read()
        rows.append(row)
        atomic_write_json(_store(), rows[-_CAP:])
    return row


def get(intent_id: str) -> Optional[Dict[str, Any]]:
    return next((r for r in _read() if r.get("intent_id") == intent_id), None)


def listing(limit: int = 50) -> List[Dict[str, Any]]:
    return _read()[-limit:][::-1]


def set_reflection_tag(intent_id: str, text: Optional[str], by: str) -> Dict[str, Any]:
    """Set or CLEAR the user's own reflection tag. Nothing but a user may call this.

    `by` must name a user. An AI-written value here would be the platform's account of the person
    replacing the person's own, which is the one thing this field exists to prevent — so a caller that
    cannot name a user is refused rather than defaulted to one.
    """
    if not isinstance(by, str) or not by.strip():
        raise ValueError("a reflection tag records WHO set it; an unattributed write is refused")
    _by = by.strip()
    if not _by.startswith("user:"):
        raise ValueError(
            f"the reflection tag holds the user's own words, so only a user may set it; {_by!r} is not a "
            f"user identity. No AI, agent or engine may write this field")
    _text = None if text is None or not str(text).strip() else str(text).strip()
    with store_lock(_store()):
        rows = _read()
        for r in rows:
            if r.get("intent_id") != intent_id:
                continue
            r["reflection_tag"] = _text
            r["reflection_tag_by"] = _by if _text is not None else None
            r["reflection_tag_at"] = time.time() if _text is not None else None
            r["reflection_tag_basis"] = (
                f"set by {_by} in their own words" if _text is not None else
                "CLEARED by the user. The field is None again, which is the same state as never set — a "
                "cleared tag leaves no trace of what it said, which is the user's to decide")
            atomic_write_json(_store(), rows)
            return r
    raise KeyError(f"no intent record {intent_id}")
