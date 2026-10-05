"""The user-satisfaction store: a person says what they think, and nothing is inferred from how they behaved.

WHY THIS FILE EXISTS. §8 names customer/user satisfaction as one of four measures the organism monitors
continuously, and P3.27 makes selection depend on it. Measured before building (W584): the only two
occurrences of "satisfaction" in the live tree were a heading in a generated document and
`biomimicry/geospheric/drad.py`, which holds `user_satisfaction: None` precisely BECAUSE it had no source —
its own comment says "A platform's claim about its users' satisfaction is the one figure it must never
invent". So there was no mechanism, and the honest `None` was the whole of it.

THE OWNER'S RULING OF 2026-10-03c, OPTION (a), DECIDES THE SHAPE, and it is narrower than the obvious
design: the signal is THE EXPLICIT RATING ONLY. A person says what they think and nothing is inferred from
how they behaved — no dwell time, no implicit signal, no per-individual preference model, and no aggregate
behavioural signal either, because option (b) offered exactly that and was not taken. The archived
mechanism W563 assessed would have passed the A.9.5 boundary — it forms no verdict about anyone — and was
still refused, because it would have been the first time this platform held a model OF AN INDIVIDUAL
fitted from that person's own behaviour. A.9.5 asks what is COMPUTED about a person; this asks what is
COLLECTED and KEPT about one. Same answer, separate question.

SO THE DIRECTION OF THE JUDGEMENT MATTERS AND IS THE SAFEGUARD. A rating here is a person's verdict about
the PLATFORM. Nothing in this module scores, ranks or infers anything about the person who gave it: there
is no per-user aggregate, no segmentation, and no field that characterises a rater. That is also why this
can never drift into the forbidden territory of A.9.5 — the subject of every record is a thing this
platform did, never a human being.

AND THE DENOMINATOR IS THE POINT, exactly as in `tickets.py` beside it: the mean is taken over ratings
somebody actually gave. There is no default, no zero for silence, and no "satisfied unless told
otherwise". With no ratings the figure is None with a basis that says so, because a platform reporting
0 — or worse, 1.0 — over an empty store is the defect this whole package was built against.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

#  The scale, stated once. An explicit rating is an INTEGER on a declared scale; a float would invite a
#  computed value to be passed in as though a person had given it.
SCALE_MIN = 1
SCALE_MAX = 5
SCALE_LABEL = f"{SCALE_MIN}-{SCALE_MAX}, given explicitly by a person"

#  Absence is its own state and is never a number. Nothing writes this value; it exists so that a reader
#  of this module cannot mistake "nobody rated it" for a low rating.
NOT_RATED = None


def _store():
    return data_path("user_satisfaction.json")


def _read() -> List[Dict[str, Any]]:
    """STRICT read: a store that cannot be read is an error, not an empty list.

    A tolerant read would answer [] for a truncated store, and the mean computed from it would then
    describe a store nobody could read while looking like a measurement of a contented week. This is the
    FU-395 class and the remedy for a WRITER's base is to refuse, not to recover.
    """
    return read_json_strict(_store(), missing=[], expect=list)


def record_rating(subject: str, rating: int, given_by: str,
                  comment: Optional[str] = None) -> Dict[str, Any]:
    """Record a rating a PERSON gave about something this platform did.

    `subject` names what was rated — a product, a route, an answer, the platform. `given_by` identifies
    who gave it, because a rating's source is part of the fact: a person saying what they think and a
    process reporting a number are not the same record, and without the source this store could not tell
    them apart. `rating` must be an INTEGER on the declared scale.

    It REFUSES rather than coercing, and the refusals are the clause:
      * a non-integer rating — a float is what a computed score looks like, and a computed score is not a
        person's opinion. `True` is rejected too, because bool is an int in Python and a boolean is not a
        rating on a scale;
      * a rating off the scale, since a number outside it was not given on this scale at all;
      * an empty `given_by`, because an unattributable rating cannot be shown to have come from a person,
        and an unattributable rating is indistinguishable from an invented one.
    None of these is recorded as a zero or clamped into range. Absence of a rating is simply not
    recording one.
    """
    if isinstance(rating, bool) or not isinstance(rating, int):
        raise TypeError(
            f"a rating is an integer on the {SCALE_MIN}-{SCALE_MAX} scale, given by a person; "
            f"{type(rating).__name__} is what a "
            f"COMPUTED score looks like, and this store holds only what a person said")
    if not (SCALE_MIN <= rating <= SCALE_MAX):
        raise ValueError(
            f"{rating} is outside the {SCALE_MIN}-{SCALE_MAX} scale, so it was not given on this scale - a rating "
            f"is refused rather than clamped, because a clamped value reads as one somebody gave")
    if not str(given_by or "").strip():
        raise ValueError(
            "a rating with no source cannot be shown to have come from a person, which makes it "
            "indistinguishable from an invented one")
    if not str(subject or "").strip():
        raise ValueError("a rating must say WHAT was rated, or it cannot be read back against anything")

    r = {
        "id": f"rate-{uuid.uuid4().hex[:12]}",
        "subject": str(subject).strip(),
        "rating": int(rating),
        "scale_min": SCALE_MIN,
        "scale_max": SCALE_MAX,
        "given_by": str(given_by).strip(),
        "comment": (str(comment).strip() or None) if comment is not None else None,
        "created_at": time.time(),
        #  the provenance of the SIGNAL, recorded on every row so that no later reader has to assume it.
        #  There is exactly one legal value: this store cannot hold an inferred rating, because
        #  record_rating is the only writer and it refuses anything that is not a person's integer.
        "signal": "explicit-rating-by-a-person",
    }
    with store_lock(_store()):
        rows = _read()
        rows.append(r)
        atomic_write_json(_store(), rows)
    return r


def summary(subject: Optional[str] = None) -> Dict[str, Any]:
    """The satisfaction figure, three-state, with a basis that says what it was taken over.

    With no ratings this returns `mean: None` and `state: "not_measured"` — never 0, never a default, and
    never a flattering 1.0. "Nobody has said anything" and "people are satisfied" are opposite facts, and
    a single number for both is the untruth this module exists to prevent.
    """
    rows = _read()
    if subject is not None:
        want = str(subject).strip()
        rows = [r for r in rows if str(r.get("subject") or "").strip() == want]

    #  only a row this module wrote counts: a row with any other signal would be an inferred one, and
    #  there is no path that writes such a row. Checking anyway means a hand-edited store cannot slip a
    #  behavioural signal into a figure the Owner's ruling says must contain none.
    explicit = [r for r in rows
                if r.get("signal") == "explicit-rating-by-a-person"
                and isinstance(r.get("rating"), int) and not isinstance(r.get("rating"), bool)]
    rejected = len(rows) - len(explicit)

    scope = f" for {subject!r}" if subject is not None else ""
    if not explicit:
        return {
            "mean": None,
            "count": 0,
            "state": "not_measured",
            "scale": SCALE_LABEL,
            "subject": subject,
            "distribution": {},
            "rejected_non_explicit": rejected,
            "basis": (
                f"NOT MEASURED: no person has given a rating{scope}. This is the absence of a signal, "
                f"not a low one - nothing is counted as a zero and no default stands in for silence, so "
                f"this figure says nothing about whether anyone is satisfied."
                + (f" {rejected} stored row(s) were excluded for not carrying an explicit-rating signal."
                   if rejected else "")),
        }

    vals = [int(r["rating"]) for r in explicit]
    dist = {str(v): vals.count(v) for v in sorted(set(vals))}
    return {
        "mean": round(sum(vals) / len(vals), 3),
        "count": len(vals),
        "state": "measured",
        "scale": SCALE_LABEL,
        "subject": subject,
        "distribution": dist,
        "rejected_non_explicit": rejected,
        "basis": (
            f"the mean of {len(vals)} rating(s) that a person gave explicitly on the {SCALE_MIN}-{SCALE_MAX} "
            f"scale{scope}. Nothing is inferred from how anyone behaved: no dwell time, no implicit "
            f"signal and no behavioural aggregate enters this figure (Owner's ruling 2026-10-03c, option "
            f"(a)). Silence is not counted on either side."
            + (f" {rejected} stored row(s) were excluded for not carrying an explicit-rating signal."
               if rejected else "")),
    }


def ratings(limit: int = 50, subject: Optional[str] = None) -> List[Dict[str, Any]]:
    """The most recent ratings, newest first — the records themselves, so a figure can be checked."""
    rows = _read()
    if subject is not None:
        want = str(subject).strip()
        rows = [r for r in rows if str(r.get("subject") or "").strip() == want]
    rows.sort(key=lambda r: float(r.get("created_at") or 0.0), reverse=True)
    return rows[:max(0, int(limit))]
