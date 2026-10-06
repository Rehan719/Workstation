"""
Living-VSB registry (§4) — established VSB IDBO enterprises that the organism tends AUTONOMOUSLY.

When a VSB is established (Genesis /establish), it is registered here. The circadian heartbeat then
periodically runs a light, paced operating tick — `operate_one()` runs ONE virtual economy cycle for the
least-recently-operated VSB (round-robin) — so each established enterprise "continually, intelligently and
autonomously operates" forever, led by the Chief. Cheap + deterministic (no AI) + virtual WST only; richer
self-improvement/evolution is handled by the Sovereign Evolution Office and the metabolism's `tune()`.
"""
from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional

from agentic_core.config import StoreUnavailable, atomic_write_json, data_path, read_json_strict

# W504 (FU-060) — this module moves virtual money and had no logger: a draw from the self-investment fund
# that failed left a UEG record and nothing an operator watching the process would see.
logger = logging.getLogger("economy.living_vsbs")

_STORE = data_path("living_vsbs.json")
_HISTORY = data_path("vsb_compliance_history.json")
HISTORY_UNREADABLE = "unreadable"          # W472 — _latest_screen's answer when the history cannot be read whole


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load() -> Dict[str, Any]:
    """W472 (register FU-050) — THE roster read: whole, or StoreUnavailable. The tolerant read answered {} for a roster
    it could not parse, and register() then wrote back a roster holding only the new entity (a BOM roster kept 1 of 3
    entries) — the heartbeat stopped tending every other enterprise."""
    return read_json_strict(_STORE, dict, expect=dict)


def _int0(v: Any) -> int:
    """A malformed entry's count never stops the rotation for every entity (FU-050)."""
    try:
        return int(v or 0)
    except (TypeError, ValueError):
        return 0


def _history() -> Dict[str, Any]:
    """W472 (register FU-049) — the compliance history, whole or StoreUnavailable (a BOM history read as {} lifted
    every FAIL hold and ran distributions for entities whose latest screen failed)."""
    return read_json_strict(_HISTORY, dict, expect=dict)


def _save(d: Dict[str, Any]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(_STORE, d)


def living_statement(rec: Optional[Dict[str, Any]] = None) -> dict:
    """W475 (ledger v4 R2.0) — what a newly registered entity is told about being tended, for EVERY writer (the
    blocking and streamed establishment, /vsb/spawn, the Studio): the present tense only when the heartbeat's economy
    lever is ON — it is off by default, so only the birth cycle ran and every founder was told otherwise."""
    try:
        from agentic_core.organism.heartbeat import heartbeat as _hb
        lever = bool(getattr(_hb, "auto_economy", False))
        beating = bool(getattr(_hb, "running", False))
        auto = lever and beating                    # (refutation) a stopped heartbeat tends nothing, lever or not
    except Exception:
        lever, beating, auto = False, False, False
    return {"autonomous_operation": ("registered — the organism tends this VSB on the circadian heartbeat (paced "
                                     "virtual economy cycles)" if auto else
                                     "registered on the living roster — autonomous economy cycles are OFF ("
                                     + ("the heartbeat's Self-run lever is off" if not lever else
                                        "the heartbeat is stopped, so nothing beats although Self-run is on")
                                     + "), so only the birth cycle ran; enable Self-run and start the heartbeat on the "
                                     "Heartbeat page for the organism to tend this VSB"),
            "autonomous_cycles": auto, "virtual": True,
            #  P3.2 clause (2) — TRUE OF THIS ENTITY, when one is given. `rec=None` keeps the global
            #  sentence exactly as four existing callers already receive it; a record makes the claim
            #  specific. An entity whose own flags are OFF is NOT tended even on a beating heartbeat with
            #  the lever on, which is the half of the clause a global sentence can never express.
            **({} if rec is None else {
                "entity_tending": (lambda _t: {
                    "tended": bool(auto and all(_t["flags"].values())),
                    "organism_beating": auto,
                    "entity_flags": _t["flags"],
                    "flags_stated": _t["stated"],
                    "flags_absent": _t["absent"],
                    "basis": (
                        ("the organism is tending THIS entity: its own flags allow it and the heartbeat is "
                         "beating with the Self-run lever on. "
                         if auto and all(_t["flags"].values()) else
                         ("this entity is NOT being tended. "
                          + ("Its own flags allow it, but " if all(_t["flags"].values()) else
                             "Its own flags do not allow it"
                             #  plural agreement: the four-state test of these sentences produced
                             #  "(auto_economy, auto_compliance IS off)" before this, which is a sentence a
                             #  reader sees. A basis string is code and gets tested like one.
                             + ((lambda _off: " (" + ", ".join(_off)
                                 + (" is off)" if len(_off) == 1 else " are off)"))(
                                    [k for k, v in _t["flags"].items() if not v])
                                if not all(_t["flags"].values()) else "")
                             + (", and " if not auto else ". "))
                          + ("the organism is not beating with its lever on. " if not auto else "")))
                        + _t["basis"]),
                })(tending(rec))}),
            }


def intake_note(what: str = "this") -> Dict[str, Any]:
    """§15 (W502, FU-163) — what to tell a caller whose money is queued for "the next metabolic cycle".

    Six live files promised that the next cycle would consume an intake. `living_statement` already
    knows whether a next cycle is coming: `autonomous_cycles` is the Self-run lever AND a beating
    heartbeat, and it is False by default — so the promise was made to every caller while the entity's
    own statement said cycles were OFF. The wording is computed from the same fact, and returns the fact
    beside it so a page can render its own version rather than hardcoding one.
    """
    st = living_statement()
    running = bool(st.get("autonomous_cycles"))
    if running:
        note = (f"the receiver's next metabolic cycle consumes {what} as intake revenue (enters its "
                f"§4 waterfall) — the organism is tending it on the heartbeat")
    else:
        note = (f"{what} is QUEUED as intake revenue and NO next cycle is scheduled: autonomous economy "
                f"cycles are OFF, so it waits until a cycle is run (enable Self-run and start the "
                f"heartbeat on the Heartbeat page, or run one with POST /api/v1/economy/cycle). It "
                f"enters the §4 waterfall when that cycle runs, not before")
    return {"note": note, "autonomous_cycles": running, "virtual": True}


#  P3.26 clause (1) — THE LINEAGE STATES, as three and not two.
#  "An entity with no parent must SAY it has none rather than carrying a null that reads as an answer."
#  A null cannot distinguish "no parent" from "nobody recorded one", and FIVE of P3.26's clauses are claims
#  ABOUT a lineage — mitosis inheriting a constitution, apoptosis returning what an entity held, the
#  never-auto-retire set protecting the last entity in its realm x domain. The difference is load-bearing.
NO_PARENT = "no_parent"
PARENT_RESOLVED = "resolved"
PARENT_UNRESOLVED = "unresolved"

#  P3.2 clause (1) — PER-ENTITY TENDING, and why absent means ON.
#  `auto_economy` and `auto_compliance` exist today only as GLOBAL heartbeat levers
#  (organism/heartbeat.py), so "switches them on FOR THE NEW ENTITY" had nowhere to be recorded. They are
#  now facts about an entity, and tending requires BOTH: the organism beating with its lever on, and the
#  entity's own flag.
#  EVERY ENTITY ALREADY ON THE ROSTER PREDATES THESE FIELDS. A default of False would silently stop the
#  organism tending all of them — a regression delivered as a feature — so readers must use
#  `rec.get(flag, True)` and this writer states the value explicitly rather than leaning on a default two
#  layers away. A record should SAY what is true of it.
TENDING_FLAGS = ("auto_economy", "auto_compliance")
TENDING_ABSENT_MEANS = ("an entity registered before these fields existed carries neither, and absent is "
                        "read as ON — the organism was tending it already and a new field must not quietly "
                        "stop that")


def resolve_parent(parent_vsb: str) -> Dict[str, Any]:
    """Three states for a claimed parent. A LOOKUP ONLY — it refuses nothing; the routes do that.

    It lives here so every creation path shares one answer to "does this parent exist" rather than each
    deciding for itself what resolving means and drifting apart.
    """
    pid = str(parent_vsb or "").strip()
    if not pid:
        return {"state": NO_PARENT, "parent_vsb": None, "generation": 0,
                "basis": ("no parent was stated, so this entity has NONE - which is a fact about it and "
                          "not a field somebody forgot. An entity established directly by its founder is "
                          "the root of its own lineage, which makes it generation 0.")}
    d = _load()
    if pid in d:
        #  P3.2 clause (5) — THE GENERATION, so "has evolved >= 1 generation" has a field to mean something.
        #  Measured W598: no evolutionary generation counter existed anywhere in the live tree (every
        #  `generation` was TEXT generation), so that clause's own stated test - "a guard drives generation
        #  0 and asserts NO re-score" - had nothing to drive. A generation is the DEPTH of the lineage chain
        #  this field creates, so it belongs here with the parent rather than in a second mechanism.
        _pg = d[pid].get("generation")
        _gen = (int(_pg) + 1) if isinstance(_pg, int) else 1
        return {"state": PARENT_RESOLVED, "parent_vsb": pid, "generation": _gen,
                "basis": (f"spawned from {pid}, which was resolved on the living roster at creation - so "
                          f"this lineage names an entity that exists rather than an id somebody typed. "
                          f"Generation {_gen}: one deeper than its parent"
                          + ("" if isinstance(_pg, int) else
                             ", whose own generation was not recorded (it predates the field), so this is "
                             "counted as 1 rather than guessed from a chain that cannot be walked")
                          + ".")}
    return {"state": PARENT_UNRESOLVED, "parent_vsb": None, "generation": None,
            "basis": (f"the stated parent {pid!r} is not on the living roster. A lineage field that "
                      f"accepted this would claim a parent that never existed, and every clause reasoning "
                      f"over the lineage would then be reasoning about a fiction. The generation is None "
                      f"rather than 0: an unresolvable parent leaves the depth UNKNOWN, and 0 would assert "
                      f"this entity is a root.")}


def tending(rec: Dict[str, Any]) -> Dict[str, Any]:
    """Is the organism tending THIS entity? Reads the entity's own flags, with absent meaning ON.

    One reader for both flags, so no surface invents its own default. The basis names which flags were
    STATED on the record and which were absent, because "on because it says so" and "on because nothing
    says otherwise" are different facts about an entity.
    """
    stated = [f for f in TENDING_FLAGS if f in rec]
    absent = [f for f in TENDING_FLAGS if f not in rec]
    on = {f: bool(rec.get(f, True)) for f in TENDING_FLAGS}
    return {
        "flags": on,
        "stated": stated,
        "absent": absent,
        "basis": (
            (f"stated on this entity: {', '.join(stated)}. " if stated else "")
            + (f"not stated and therefore read as ON: {', '.join(absent)} - " + TENDING_ABSENT_MEANS + ". "
               if absent else "")
            + "Whether a cycle actually runs needs the ORGANISM's lever on and its heartbeat beating too; "
              "these flags say whether this entity consents to be tended, not whether anything is beating."),
    }


def register(vsb_id: str, name: str = "", entity_type: str = "waqf_ltd_hybrid",
             domain: str = "enterprise", owner: str = "Rehan",
             parent_vsb: str = "", auto_economy: bool = True,
             auto_compliance: bool = True) -> Dict[str, Any]:
    """Register an established VSB as a living entity the organism will autonomously tend.
    §12 (W349) — serialised: the Round-10 concurrency audit lost 28 of 32 concurrent
    registrations to the unserialised load-modify-write.

    P3.26 clause (1) and P3.2 clause (1) are both written HERE, at the single roster writer, because the
    alternative is writing them at five creation paths and leaving two behind — which is what W475 found
    when `body_pending` had four writers and a one-site fix left three lies in place.

    NOTHING IN HERE THROWS, deliberately. `enrich_vsb_entity` calls this inside an `except Exception: pass`
    because enrichment must never block generation, so anything raised here would vanish. An unresolvable
    parent is REFUSED AT THE ROUTE, before enrichment; by the time this is reached the id has been resolved
    or was never stated.
    """
    from agentic_core.config import store_lock
    with store_lock(_STORE):
        d = _load()
        if vsb_id not in d:
            #  resolved INSIDE the lock, so the parent cannot be retired between the check and the write
            _lin = resolve_parent(parent_vsb)
            d[vsb_id] = {"vsb_id": vsb_id, "name": name or vsb_id, "entity_type": entity_type,
                         "domain": domain, "owner": owner, "registered_at": _now(),
                         "operating_cycles": 0, "last_operated": None, "status": "living",
                         #  ADDED, never folded into `status`: it already has readers.
                         "parent_vsb": _lin["parent_vsb"],
                         "lineage_state": _lin["state"],
                         "generation": _lin["generation"],
                         "lineage_basis": _lin["basis"],
                         #  stated explicitly, so the record says what is true of it
                         "auto_economy": bool(auto_economy),
                         "auto_compliance": bool(auto_compliance)}
            _save(d)
        return d[vsb_id]


def deregister(vsb_id: str) -> bool:
    """Remove an entity from the autonomous operating roster. Returns True if it was there.

    W417 — this module could register a VSB into the roster but never remove one, so anything that
    ever registered was tended by the organism forever. By 2026-08-31 the roster held 191 entries of
    which 157 were pytest fixtures, and the heartbeat had run 2,113 operating cycles round-robin —
    so the Owner's own entities received about a sixth of the attention while the rest went to test
    data. Deregistering does not delete the entity; it only stops the organism tending it.
    """
    from agentic_core.config import store_lock
    with store_lock(_STORE):          # W463 (sixth refutation) — serialised with every other roster write
        d = _load()
        if vsb_id not in d:
            return False
        del d[vsb_id]
        _save(d)
    return True


# W505 (FU-287) — how long a visit claim stands before it is treated as abandoned. A visit is one governed
# cycle: seconds of work, with the store lock's own 10s bound inside it. Two minutes is generous enough that a
# slow visit is never cut off and short enough that a killed process does not strand the entity.
_VISIT_TTL = 120.0

# W505 (FU-287, second pass) — visits that FINISHED in this process, whether or not their release could be
# written. `_claim_visit` takes the claim through store_lock + _save directly while `_release_visit` goes through
# _update_entry, so a roster write failure can leave a claim on the row for a visit that is long over: measured
# by test_w503h, where one forced write failure locked the entity out of every visit for the full TTL and the
# W503 hold-clearing therefore never ran. A running visit's id is never in this set, so the anti-interleaving
# guarantee is unchanged. Bounded so a long-lived process cannot grow it without limit.
_FINISHED_VISITS: "list[str]" = []
_FINISHED_CAP = 512


def _claim_visit(vsb_id: str, visit_id: str) -> Dict[str, Any]:
    """Claim an entity for the duration of one visit. Returns {claimed, holder, broke_stale}.

    W505 (FU-287) — without this, two visits of ONE entity interleave: one writes `last_hold` while the other
    pops it, so the row's outcome fields describe whichever finished last while `operating_cycles` counts
    both. With it there is exactly one writer of those fields per visit, which is the whole point: the row and
    the counter then describe the same visit.
    """
    from agentic_core.config import store_lock
    now = time.time()
    with store_lock(_STORE):
        d = _load()
        entry = d.get(vsb_id)
        if not entry:
            return {"claimed": False, "holder": None, "missing": True}
        held = entry.get("visit_claim") if isinstance(entry.get("visit_claim"), dict) else None
        broke_stale = None
        if held and held.get("visit_id") != visit_id:
            age = now - float(held.get("at") or 0)
            if held.get("visit_id") in _FINISHED_VISITS:
                # the holder FINISHED and only its release failed to write. Refusing here would lock the
                # entity out for the whole TTL over a bookkeeping failure, which is what test_w503h measured.
                broke_stale = {"visit_id": held.get("visit_id"), "age_s": round(age, 1),
                               "why": "the visit finished; its release could not be written"}
                logger.warning("living_vsbs: overriding a claim on %s whose visit %s finished but could not "
                               "release \u2014 the roster write failed, so its bookkeeping did not land",
                               vsb_id, held.get("visit_id"))
            elif age <= _VISIT_TTL:
                return {"claimed": False, "holder": held.get("visit_id"), "held_for_s": round(age, 1)}
            # a holder from ANOTHER process that died: the TTL is the only recourse there, because this
            # process cannot know whether that visit finished
            broke_stale = {"visit_id": held.get("visit_id"), "age_s": round(age, 1),
                           "why": f"no release seen for more than {_VISIT_TTL:.0f}s"}
            logger.warning("living_vsbs: breaking a visit claim on %s abandoned %.1fs ago by %s",
                           vsb_id, age, held.get("visit_id"))
        entry["visit_claim"] = {"visit_id": visit_id, "at": now}
        d[vsb_id] = entry
        _save(d)
        return {"claimed": True, "holder": visit_id, "broke_stale": broke_stale}


def _release_visit(vsb_id: str, visit_id: str) -> None:
    """Drop the claim, but ONLY this visit's. Releasing another visit's claim would reintroduce the overlap
    this exists to prevent (the case where a stale claim was broken while this visit still believed it held
    one). Never raises: a visit's outcome must not be lost to its own cleanup."""
    # recorded FIRST, and unconditionally: this visit is over whichever way the write below goes, and a
    # later claim must not be blocked by a claim whose holder has finished.
    _FINISHED_VISITS.append(visit_id)
    del _FINISHED_VISITS[:-_FINISHED_CAP]

    def _drop(e: Dict[str, Any]) -> None:
        c = e.get("visit_claim")
        if isinstance(c, dict) and c.get("visit_id") == visit_id:
            e.pop("visit_claim", None)
        e["last_visit_id"] = visit_id
    try:
        _update_entry(vsb_id, _drop)
    except Exception as exc:
        logger.warning("living_vsbs: the visit claim on %s could not be released: %s", vsb_id, exc)


def _update_entry(vsb_id: str, mutate) -> Optional[Dict[str, Any]]:
    """W463 (sixth refutation) — operate_vsb held a roster snapshot across a whole governed cycle and wrote it back,
    erasing registrations made meanwhile and undoing deregistrations. Its bookkeeping now re-reads the roster under
    the store lock and changes only this entry; an entry deregistered meanwhile stays gone (None is returned)."""
    from agentic_core.config import store_lock
    with store_lock(_STORE):
        d = _load()
        entry = d.get(vsb_id)
        if not entry:
            return None
        mutate(entry)
        d[vsb_id] = entry
        _save(d)
        return dict(entry)


# W504 (FU-064) — whether an entity's ledger parses, keyed on the FILE rather than re-read per call.
# `_ledger_hold_text` built a VirtualLedger purely to read `load_error`, and that constructor does a strict
# read of the whole file. `list_living` calls it once per held row and the heartbeat and pages call
# `list_living` often, so a roster of large held ledgers re-parsed all of them on every request (the row
# measured 4 s for 60 held rows of 4 MB, and said plainly that this is negligible at today's sizes — this is
# a cost fix, not a user-visible one).
#
# The correctness that must not break is W468's: a ledger REPAIRED since the last visit must stop being
# described as unreadable. The key is therefore the file's own (size, mtime_ns). Every store write in this
# codebase goes through `atomic_write_json`, which writes a temp file and os.replace()s it, so the result
# carries a fresh mtime and a repair always misses the cache. That is the assumption this rests on; a store
# written some other way, in place, preserving both size and mtime_ns, would be served a stale answer.
_LEDGER_READS: Dict[str, tuple] = {}
_LEDGER_READS_MAX = 512


def _ledger_path(vsb_id: str):
    """The ledger file for this entity, WITHOUT constructing a VirtualLedger — whose __init__ performs the
    strict read this cache exists to avoid. Mirrors the ledger module's own expression; a guard asserts the
    two stay in step, and a mismatch only costs a real read (it is never wrong)."""
    from agentic_core.economy import ledger as _led
    return _led._STORE / f"{vsb_id}_ledger.json"


def _ledger_reads_whole(vsb_id: str) -> bool:
    """True when this entity's ledger parses whole. Cached against the file's size and mtime.

    The stat comes FIRST. An earlier version of this built a VirtualLedger to reach `.path`, which meant the
    strict read had already happened before the cache was consulted — a cache after the expensive step saves
    nothing."""
    try:
        st = _ledger_path(vsb_id).stat()
        key = (st.st_size, st.st_mtime_ns)
    except Exception:
        key = None
    if key is not None:
        hit = _LEDGER_READS.get(vsb_id)
        if hit is not None and hit[0] == key:
            return bool(hit[1])
    try:
        from agentic_core.economy.ledger import VirtualLedger
        readable = VirtualLedger(vsb_id).load_error is None
    except Exception:
        return False
    if key is not None:
        if len(_LEDGER_READS) >= _LEDGER_READS_MAX:
            _LEDGER_READS.pop(next(iter(_LEDGER_READS)), None)
        _LEDGER_READS[vsb_id] = (key, readable)
    return readable


def _ledger_hold_text(vsb_id: Any, decision: Any = None) -> str:
    """W468 (refutation) — the hold is what the LAST visit found; the ledger is read now, so a repaired ledger is never
    still described as unreadable. A Change Control decision behind it is named (sixth refutation)."""
    behind = (f" — and a Change Control decision ({str(decision).replace('_', ' ')}) stands behind it" if decision else "")
    readable = _ledger_reads_whole(str(vsb_id))
    if readable:
        return ("its ledger could not be read whole at the last visit and reads whole now — the next visit tries its "
                "cycle again" + behind)
    return "its ledger could not be read whole — no cycle runs and nothing is posted to it until it can be" + behind


def _hold_consequence(r: Dict[str, Any]) -> tuple:
    """What a hold on this row MEANS for the entity, and which rule said so.

    W503 (FU-063) — this was a five-deep conditional inside the row literal, and two of its arms were
    wrong: it fell through to "held by governance" for ANY value in the hold position, so
    `intake_unavailable` and `intake_consumed_elsewhere` — stores the cycle could not use — were reported
    to the founder as a governance decision about their enterprise; and a decision hold with NO Change
    Control record (what a materiality gate that ERRORS produces) claimed a ruling nobody had made.

    The rules are checked in the same order as before, and the basis names which one answered, because a
    sentence about someone's enterprise should be traceable to the rule that produced it."""
    hold = r.get("last_hold")
    if not hold:
        return None, None
    if hold == "compliance_fail_hold":
        return ("distributions are held — no economy cycle runs until a re-screen clears it",
                "the latest §11 screen is FAIL: a judgement about this entity")
    if hold == "compliance_history_unavailable":
        return ("its compliance standing cannot be known — the compliance history could not be read "
                "whole; no cycle runs until it can be",
                "the compliance history could not be read: the platform cannot act")
    if hold == "ledger_unavailable":
        return (_ledger_hold_text(r.get("vsb_id"), r.get("decision_hold")),
                "the books could not be read: the platform cannot act")
    if hold in _DECISION_HOLDS:
        if r.get("last_hold_record", _RECORD_UNKNOWN) is None:
            return ("this entity's cycle is held, but no Change Control record was written — the gate "
                    "could not be reached. Nothing has been decided about this entity.",
                    "a decision hold with no record: the gate errored, so nothing was decided")
        return ("this entity's cycle is held by governance — a Change Control decision",
                "a Change Control decision, with its record")
    return (f"no cycle runs: {hold} — something this cycle needs could not be used. This is about the "
            "platform, not a judgement about this entity.",
            "an unavailability, not a decision")


def list_living() -> Dict[str, Any]:
    """§11 × §13 (W421) — each row now carries the entity's LIVE compliance standing and any economic
    hold it causes. Both existed only as side effects before: `_latest_screen` was read by
    `operate_vsb` to decide a hold, and the hold was written to the store and the UEG — but the
    entity's OWNER had no way to see either. A held enterprise looked simply idle."""
    try:
        d = _load()
    except StoreUnavailable as e:
        # W472 — a roster that cannot be read whole is said, never shown as an empty roster
        return {"living_vsbs": [], "total": 0, "roster_unavailable": str(e),
                "note": "the living roster could not be read whole — no entity is tended and nothing is written to "
                        "it until it can be read (virtual/simulated — no real funds)"}
    rows = sorted([v for v in d.values() if isinstance(v, dict)], key=lambda v: str(v.get("registered_at") or ""),
                  reverse=True)
    hist_error = None
    try:
        hist = _history()
    except StoreUnavailable as e:
        hist, hist_error = {}, str(e)
    for r in rows:
        h = hist.get(r.get("vsb_id")) or {}
        verdict = h.get("overall")
        r["compliance"] = {
            # None means NOT YET SCREENED — never rendered as a pass. An entity established before
            # auto_compliance was switched on has no verdict, and that is different from a clean one.
            "verdict": verdict,
            # W506 (P2.7(6)) - THE KEY THE WRITER ACTUALLY USES. This asked the top-level entry for
            # "screened_at", which is never written, then for "at", which exists only inside a history
            # item. The heartbeat persists the timestamp as "last_at", so every screened entity reported
            # a null here and a reader could not tell it from one never screened. The older names stay as
            # fallbacks: a history written before this round is not migrated by this change.
            "screened_at": h.get("last_at") or h.get("screened_at") or h.get("at"),
            # ...and the writer now persists these, having had them and dropped them. The COVERAGE
            # statement travels with the verdicts: these screens can refuse and escalate but cannot
            # clear, so a per-framework list without a statement of what was assessed overstates itself.
            "verdicts": h.get("verdicts") or [],
            "coverage_gaps": h.get("coverage_gaps"),
            "assessed_by": h.get("assessed_by"),
            "never_screened": (not bool(verdict)) if not hist_error else None,
            # W472 (FU-049) — a history that cannot be read whole: the standing is UNKNOWN, not clean
            "history_unavailable": hist_error,
        }
        # W503 — computed ONCE: the ledger-hold arm reads the books, so a call per field would read
        # them twice for every row in the roster.
        _cons = _hold_consequence(r)
        r["economy_held"] = {
            "held": bool(r.get("last_hold")),
            "reason": r.get("last_hold"),
            # W503 (FU-063) — a function, not five nested ternaries. See _hold_consequence.
            "consequence": _cons[0],
            "consequence_basis": _cons[1],
            # W503 (FU-063) — which of the four outcomes the row's standing hold is. Added beside
            # `held`, never replacing it: `held` means "there is a hold on this row" and is read elsewhere.
            "outcome": (_outcome_of_hold(r.get("last_hold"),
                                        r.get("last_hold_record", _RECORD_UNKNOWN)) if r.get("last_hold")
                        else ("raised" if r.get("last_error") else None)),
            # W468 — the last visit's raise, when that is what happened (a raise is not a hold)
            "last_visit_error": r.get("last_error"),
            # W468 (sixth refutation) — a Change Control decision (pending or already decided) the ledger hold stands
            # in front of
            "standing_decision": r.get("decision_hold"),
        }
        # W491 (FU-192) — `operating_cycles` counts the cycles THIS roster ran, which is not the number of
        # metabolic cycles the entity has: one run through any other path posts to the books and never
        # touches this counter, so a row read "1 cycles" beside a ledger holding three. The row now names
        # the population its own counter covers and carries the books' own count beside it.
        r["operating_cycles_basis"] = ("cycles this autonomous roster ran and booked; a cycle run through any "
                                       "other path is posted to the books but not counted here")
        try:
            from agentic_core.economy.metabolism import EconomicMetabolism
            _m = EconomicMetabolism(r.get("vsb_id"))
            if _m.ledger.load_error:
                r["ledger_cycles"] = None
                r["ledger_cycles_unavailable"] = str(_m.ledger.load_error)[:160]
            else:
                _st = _m.ledger.statement()
                r["ledger_cycles"] = _st.get("cycles_posted")
                r["ledger_cycles_basis"] = _st.get("cycles_posted_basis")
        except Exception as _le:
            r["ledger_cycles"] = None
            r["ledger_cycles_unavailable"] = f"{type(_le).__name__}: {str(_le)[:140]}"
    return {"living_vsbs": rows, "total": len(rows), "history_unavailable": hist_error,
            "cycle_counts_basis": ("`operating_cycles` is this roster's own tally; `ledger_cycles` is what the "
                                   "entity's books record. They differ whenever a cycle ran outside the roster."),
            "note": "Established VSB enterprises the organism autonomously tends (paced virtual economy "
                    "cycles on the circadian heartbeat). Virtual/simulated — no real funds."}


def operate_one() -> Optional[Dict[str, Any]]:
    """Autonomously operate the least-recently-operated living VSB: one virtual economy cycle. Round-robin,
    paced by the heartbeat. Returns a compact record, or None when there are no living VSBs. Best-effort."""
    try:
        d = _load()
    except StoreUnavailable as e:
        # W472 (FU-050) — an unreadable roster is a said outcome of the beat, never an empty roster.
        # W503 (FU-063) — this return never passes through operate_vsb, so it needs its own `outcome`:
        # the roster could not be used, which is a refusal by the platform, not a decision about anyone.
        return {"cycle_ran": False, "held": "roster_unavailable", "outcome": "refused", "note": str(e)}
    entries = [v for v in d.values() if isinstance(v, dict) and isinstance(v.get("vsb_id"), str)]
    if not entries:
        return None
    # pick the least-recently-operated (None sorts first). §8 (W340) — FAIR under bursts: the
    # second-resolution timestamps tie when beats fire sub-second (the audit observed 23×/8×/7×
    # starvation), so ties break by FEWEST operating cycles, then registration order — every
    # entity gets tended even under a burst of manual beats.
    target = sorted(entries, key=lambda v: (str(v.get("last_operated") or ""),
                                            _int0(v.get("operating_cycles")),        # W472 — one bad entry never stops all
                                            str(v.get("registered_at") or "")))[0]
    return operate_vsb(target["vsb_id"])


# W468 (refutations 2–4) — holds that record an Owner's decision (or a hold awaiting one): a heartbeat visit that raises
# does not change them. Every other hold is an earlier visit's outcome, which a later visit's raise supersedes.
_DECISION_HOLDS = frozenset({"held_for_change_control", "rejected_by_change_control", "governance_hold"})

# W503 (FU-063) — FOUR OUTCOMES, ONE FIELD. `operate_vsb` returns eight shapes and said what happened in
# none of them, so each consumer re-derived it differently and each was wrong in its own way (genesis
# announced "cycle ran" for a visit that only raised, because the raised return has no `cycle_ran` key and
# `None is not False`; the heartbeat counted a hold as an entity operated; list_living called an
# unavailable intake a governance hold). `outcome` is ADDED — `cycle_ran`, `held`, `governance` and `error`
# keep their exact meanings, because their readers depend on them (W495: re-pointing a field's meaning at
# something new broke six of nine suite failures).
#   ran     — a cycle posted to the books. A later bookkeeping raise does not unmake it.
#   held    — a DECISION held it: a FAIL §11 screen, or Change Control.
#   refused — the platform could not act: the roster, the ledger, the compliance history or the intake
#             could not be used. This is a fact about the platform, NOT a judgement about the entity.
#   raised  — the visit raised and no cycle posted.
VISIT_OUTCOMES = ("ran", "held", "refused", "raised")


_RECORD_UNKNOWN = object()   # W503 — "nobody told me", which is NOT the same as "there is none"


def _outcome_of_hold(hold: Optional[str], record: Any = _RECORD_UNKNOWN) -> str:
    """Classify whatever sits in the hold position. A Change Control decision or a FAIL screen is a
    JUDGEMENT, so the entity is held. Everything else there — an unreadable ledger, an unavailable
    roster or intake, an unreadable compliance history — is the platform unable to act, which is a
    refusal and must never be reported as a decision about the entity. `compliance_fail_hold` is named
    explicitly rather than added to _DECISION_HOLDS, which means Change Control specifically and is read
    elsewhere to decide what a later hold may overwrite.

    W503 (FU-063 part 5) — `record` is the Change Control record the hold names. A materiality gate that
    ERRORS returns status `held_for_change_control` with `cca_id` None: the action is held, correctly, but
    there is no decision, and reporting one is a claim about the entity that nothing supports. A decision
    hold whose record is explicitly None is therefore a REFUSAL. `_RECORD_UNKNOWN` (the default) keeps the
    old answer, because a caller that does not know the record has not established that none exists."""
    if hold in _DECISION_HOLDS and record is None:
        return "refused"
    return "held" if (hold in _DECISION_HOLDS or hold == "compliance_fail_hold") else "refused"

DEV_SPEND_WST = 50.0   # §12 (W330) — the per-action development cost drawn from self_investment


def spend_self_investment(vsb_id: str, purpose: str, amount: float = DEV_SPEND_WST) -> Dict[str, Any]:
    """§12 (W330) — 'reinvests in its own growth' becomes REAL: the waterfall's self_investment
    stage was the only stage with no consumer (pure accounting). The entity's OWN development
    actions (autonomous evolution · repo re-ship) now SPEND from it — a balanced double-entry
    posting (self_investment → development_spend), UEG-logged, honest zero-spend when the
    balance is empty (development never blocks on an empty fund; the spend is recorded as
    unfunded). Virtual WST only."""
    try:
        from agentic_core.economy.metabolism import EconomicMetabolism
        d = _load()
        reg = d.get(vsb_id) or {}
        m = EconomicMetabolism(vsb_id, reg.get("entity_type", "waqf_ltd_hybrid"),
                               reg.get("owner", "Rehan"))
        if m.ledger.load_error:
            # W468 (register FU-041) — an unreadable ledger read as empty books, and this reported "balance empty — ran
            # unfunded" for a fund whose balance is unknown
            rec = {"vsb_id": vsb_id, "purpose": purpose[:120], "requested_wst": float(amount), "spent_wst": 0.0,
                   "funded": False, "ledger_unavailable": True, "error": m.ledger.load_error[:200],
                   "note": "the entity's ledger could not be read whole, so nothing was drawn from self_investment and "
                           "whether the fund could have paid for this action is unknown"}
            try:
                # its own type (refutation): the audit views read "self_investment_spend" as a clean, recorded spend
                from agentic_core.economy.governance import _ueg_log
                _ueg_log({"type": "economy.self_investment_spend_refused", **rec,
                          "disclaimer": "Virtual/simulated WST — no real funds moved."})
            except Exception:
                pass
            return rec
        # §12 (W339) — the spend must hit the SAME surface the balance check reads: post() moves only the
        # double-entry `accounts`, so the `balances` fund never depleted and every spend reported
        # funded:true forever (audit-proven: 200 WST "spent" from a fund that never dropped).
        # W504 (FU-060) — and the check and the write happen under ONE hold of the ledger's lock. This
        # read the balance from statement() and then called record(), which locks separately: two
        # concurrent spends both saw the whole balance and both drew it, taking the fund negative.
        try:
            _drawn = m.ledger.spend_from("self_investment", float(amount),
                                         source="self_investment",
                                         memo=f"reinvestment: {purpose[:120]}")
        except Exception as _err:
            from agentic_core.economy.ledger import LedgerUnavailable as _LU, LedgerWriteRefused as _LWR
            if isinstance(_err, (_LU, _LWR)):
                # W504 — NOT MINE TO ANSWER. The outer handler below distinguishes these two, sets
                # `ledger_unavailable` / `ledger_write_refused` and emits
                # `economy.self_investment_spend_refused` — W468's contract, added so a refusal is
                # RECORDED and not merely returned. Catching them here silently replaced that answer with
                # a different flag and a different chain event.
                raise
            # W504 (FU-060) — A SPEND THAT FAILED IS SAID. Only an unreadable ledger was handled; a busy
            # lock or a refused write raised out of this helper, so the development action went ahead with
            # nothing recording that its funding never happened. This branch is for THOSE failures.
            rec = {"vsb_id": vsb_id, "purpose": purpose[:120], "requested_wst": float(amount),
                   "spent_wst": 0.0, "funded": False, "spend_failed": True,
                   "error": f"{type(_err).__name__}: {str(_err)[:160]}",
                   "note": "the self_investment fund could not be drawn from, so this development action is "
                           "UNFUNDED; the fund is unchanged and whether it could have paid is unknown"}
            try:
                from agentic_core.economy.governance import _ueg_log
                _ueg_log({"type": "economy.self_investment_spend_failed", **rec,
                          "disclaimer": "Virtual/simulated WST — no real funds moved."})
            except Exception:
                pass
            logger.warning("self_investment spend failed for %s: %s", vsb_id, str(_err)[:160])
            return rec
        spent = _drawn["spent_wst"]
        rec = {"vsb_id": vsb_id, "purpose": purpose[:120], "requested_wst": float(amount),
               "spent_wst": spent, "funded": spent > 0,
               # W504 — the fund's own figures, read under the lock that drew from it
               "fund_before_wst": _drawn["balance_before_wst"],
               "fund_after_wst": _drawn["balance_after_wst"],
               "posted_as": "development_spend (an expense of its own, not a second distribution)",
               "note": ("self_investment funded this development action" if spent > 0 else
                        "self_investment balance empty — action ran unfunded (recorded honestly)")}
        try:
            from agentic_core.economy.governance import _ueg_log
            _ueg_log({"type": "economy.self_investment_spend", **rec,
                      "disclaimer": "Virtual/simulated WST — no real funds moved."})
        except Exception:
            pass
        return rec
    except Exception as exc:
        from agentic_core.economy.ledger import LedgerUnavailable, LedgerWriteRefused
        out = {"vsb_id": vsb_id, "error": str(exc)[:160], "funded": False,
               **({"ledger_unavailable": True} if isinstance(exc, LedgerUnavailable) else {}),
               **({"ledger_write_refused": True} if isinstance(exc, LedgerWriteRefused) else {})}
        if isinstance(exc, (LedgerUnavailable, LedgerWriteRefused)):
            # W468 (second refutation) — refused at its write (the ledger broke after the balance was read): recorded,
            # never only returned to a caller that discards it
            try:
                from agentic_core.economy.governance import _ueg_log
                _ueg_log({"type": "economy.self_investment_spend_refused", **out, "purpose": purpose[:120],
                          "requested_wst": float(amount), "spent_wst": 0.0,
                          "note": "the spend was refused at its ledger write; nothing was drawn from self_investment",
                          "disclaimer": "Virtual/simulated WST — no real funds moved."})
            except Exception:
                pass
        return out


def _latest_screen(vsb_id: str) -> Optional[str]:
    """The entity's latest §11 screen verdict from the per-VSB compliance history (W288), None when never screened,
    or HISTORY_UNREADABLE (W472, FU-049) when the history exists and cannot be read whole — never None for that."""
    try:
        hist = _history()
    except StoreUnavailable:
        return HISTORY_UNREADABLE
    entry = hist.get(vsb_id)
    return entry.get("overall") if isinstance(entry, dict) else None


def operate_vsb(vsb_id: str) -> Optional[Dict[str, Any]]:
    """Operate ONE living VSB (one governed virtual economy cycle). §11×§12 (W309): an entity whose
    LATEST compliance screen is FAIL has its distributions HELD — the survival instinct has teeth;
    the hold lifts as soon as a re-screen clears it. Best-effort; honest records either way."""
    try:
        d = _load()
    except StoreUnavailable as e:
        return {"vsb_id": vsb_id, "cycle_ran": False, "held": "roster_unavailable",
                "outcome": "refused", "note": str(e)}
    target = d.get(vsb_id)
    if not target:
        return None
    # W505 (FU-287) — ONE visit at a time per entity. Everything below writes this entity's outcome fields
    # (last_hold, last_error, last_operated, operating_cycles), and two visits interleaving left the row
    # describing one of them while the counter reflected both.
    import uuid as _uuid
    _visit = _uuid.uuid4().hex[:12]
    _claim = _claim_visit(vsb_id, _visit)
    if _claim.get("missing"):
        return None
    if not _claim.get("claimed"):
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle_ran": False,
                "held": "visit_in_progress", "outcome": "refused",
                "held_by_visit": _claim.get("holder"), "held_for_s": _claim.get("held_for_s"),
                "note": ("another visit of this entity is in progress, so this one did nothing rather than "
                         "interleave with it — nothing was posted and no counter moved. Visit it again.")}
    try:
        return _operate_vsb_claimed(vsb_id, target, _visit, _claim)
    finally:
        _release_visit(vsb_id, _visit)


def _operate_vsb_claimed(vsb_id: str, target: Dict[str, Any], _visit: str,
                         _claim: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """The visit itself, with this entity claimed for its duration (see `operate_vsb`)."""
    if _claim.get("broke_stale"):
        # a previous visit's claim was abandoned and this one overrode it. Said, not silent: a reader of the
        # row needs to know an earlier visit of this entity stopped without finishing.
        logger.warning("living_vsbs: %s is being visited after an abandoned visit %s", vsb_id,
                       _claim["broke_stale"].get("visit_id"))
    screen = _latest_screen(vsb_id)
    if screen == HISTORY_UNREADABLE:
        # W472 (FU-049) — a history that cannot be read whole means the standing is UNKNOWN: held, said, no cycle
        target["last_operated"] = _now()

        def _hold_unknown(e: Dict[str, Any]) -> None:
            # (refutation) a Change Control decision this hold now stands in front of is kept apart, never overwritten
            prior = e.get("last_hold") if e.get("last_hold") in _DECISION_HOLDS else e.get("decision_hold")
            e.pop("decision_hold", None)
            if prior:
                e["decision_hold"] = prior
            e.update(last_operated=target["last_operated"], last_hold="compliance_history_unavailable")
            e.pop("last_error", None)
        _update_entry(vsb_id, _hold_unknown)
        try:
            from agentic_core.economy.governance import _ueg_log
            _ueg_log({"type": "economy.compliance_history_unavailable", "vsb_id": vsb_id,
                      "note": "the compliance history could not be read whole — standing unknown, cycle held"})
        except Exception:
            pass
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle_ran": False,
                "held": "compliance_history_unavailable", "outcome": "refused",
                "note": "the §11 compliance history could not be read whole — the entity's standing cannot be "
                        "known, so no cycle runs and nothing is posted until it can be read"}
    # §11 teeth (W309) — last screen FAIL → the economy is held, no cycle runs. The tending is
    # still RECORDED (last_operated advances) so a held entity never starves the round-robin —
    # the organism visited it; the visit's outcome was a hold.
    if screen == "fail":
        target["last_operated"] = _now()
        target["last_hold"] = "compliance_fail_hold"
        # W503 (FU-063) — this write sat outside any try, so a raise here left `operate_vsb` altogether:
        # the caller's `except Exception: pass` swallowed it and the visit left NO trace, neither the hold
        # it found nor the failure to record it. The hold is still returned when its bookkeeping fails,
        # because the screen said FAIL whether or not the roster could be written.
        _fail_booked = True
        try:
            _update_entry(vsb_id, lambda e: (e.update(last_operated=target["last_operated"], last_hold="compliance_fail_hold"),
                                             e.pop("last_error", None)))
        except Exception as _bk:
            _fail_booked = False
            try:
                from agentic_core.economy.governance import _ueg_log
                _ueg_log({"type": "economy.compliance_hold_not_recorded", "vsb_id": vsb_id,
                          "error": f"{type(_bk).__name__}: {str(_bk)[:160]}",
                          "note": "the FAIL screen holds this entity's distributions; the roster could not "
                                  "record the visit, so the hold is not on the row"})
            except Exception:
                pass
        try:
            from agentic_core.organism.biobus import biobus
            biobus.fire_signal("reflex", "economy.compliance_hold",
                               f"{vsb_id}: distributions held on FAIL screen", 0.8)
        except Exception:
            pass
        # §11×§13 (W319) — the teeth engaging is a TAMPER-EVIDENT record, not just a response field.
        try:
            from agentic_core.economy.governance import _ueg_log
            _ueg_log({"type": "economy.compliance_fail_hold", "vsb_id": vsb_id,
                      "note": "distributions held on latest FAIL screen (lifts on a clearing re-screen)"})
        except Exception:
            pass
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle_ran": False,
                "held": "compliance_fail_hold", "outcome": "held",
                **({} if _fail_booked else {"hold_recorded": False,
                                            "hold_record_note": "the hold stands, but the roster row could not "
                                                                "be written — see the UEG record"}),
                "note": "latest §11 screen is FAIL — distributions held until a re-screen clears it"}
    cycle_done: Dict[str, Any] = {"report": None, "booked": False, "held": None, "held_booked": False}
    try:
        # §3 — the ALWAYS-ON path is governed too: constitutional pre-gate + materiality hold +
        # per-cycle UEG split logging (previously this path ran completely ungated + unlogged).
        from agentic_core.economy.governance import governed_cycle_sync
        # §12 (W293) — the cycle's intake is the entity's REAL recorded activity (marketplace sales
        # attributed to it + QMS-passed delivery tariffs, consumed exactly once), NOT the old
        # fabricated flat 1000-WST constant. With no events: an honest ZERO-revenue maintenance
        # cycle — the organism still tends the entity, but distributes only what real work brought.
        # §12 (W313) — PEEK-then-consume: the cycle's intake is measured WITHOUT consuming, the
        # governance gates run on the peeked totals, and the events are consumed ONLY after every
        # gate passes. A materiality/policy hold therefore PRESERVES the recognised revenue it
        # holds (previously consume-before-gate destroyed it — the CCA approval then authorised a
        # distribution of nothing).
        from agentic_core.economy.revenue import peek_pending
        peek = peek_pending(vsb_id)
        res = governed_cycle_sync(vsb_id, target.get("entity_type", "waqf_ltd_hybrid"),
                                  target.get("owner", "Rehan"), peek["revenue"], peek["costs"],
                                  source="heartbeat", events=peek)
        report = res.get("cycle")
        if report is None:   # held/blocked by governance — revenue preserved, hold recorded,
            # and the visit still advances the rotation (a hold must intercept EVERY cycle,
            # not just the first — mirror of the W309 compliance-hold pattern).
            gov = res.get("governance") or {}
            target["last_operated"] = _now()
            target["last_hold"] = str(gov.get("status") or "governance_hold")
            # W503 (FU-063) — the record the hold NAMES. None here means the gate errored and held
            # without a Change Control record, which is not a decision about this entity.
            target["last_hold_record"] = gov.get("cca_id")
            def _held(e: Dict[str, Any]) -> None:
                # W468 (sixth refutation) — the row has one hold: a Change Control decision an unreadable ledger now
                # stands in front of is kept apart (decision_hold), never overwritten
                prior = e.get("last_hold") if e.get("last_hold") in _DECISION_HOLDS else e.get("decision_hold")
                e.pop("decision_hold", None)
                if target["last_hold"] == "ledger_unavailable" and prior:
                    e["decision_hold"] = prior
                e.update(last_operated=target["last_operated"], last_hold=target["last_hold"],
                         last_hold_record=target["last_hold_record"])
                e.pop("last_error", None)
            cycle_done["held"] = _held           # (seventh refutation) a raise from here on is this hold's bookkeeping
            _update_entry(vsb_id, _held)
            cycle_done["held_booked"] = True
            try:
                preserved = peek_pending(vsb_id)["revenue"]      # what is ACTUALLY pending now (never a stale peek)
            except Exception:
                preserved = None
            return {"vsb_id": vsb_id, "name": target.get("name"),
                    "governance": gov, "cycle_ran": False,
                    # a governance STATUS is not automatically a governance decision: intake_unavailable
                    # and ledger_unavailable arrive here too, and they are refusals
                    "outcome": _outcome_of_hold(target["last_hold"], target["last_hold_record"]),
                    "hold_names_a_decision": target["last_hold_record"] is not None,
                    **({"hold_basis": "held without a Change Control record — the gate could not be "
                                      "reached, so nothing has been decided about this entity"}
                       if target["last_hold"] in _DECISION_HOLDS and target["last_hold_record"] is None
                       else {}),
                    "pending_preserved_wst": preserved,
                    "note": ("recognised revenue events remain PENDING (unconsumed) while held"
                             if gov.get("status") not in ("intake_unavailable", "intake_consumed_elsewhere",
                                                          "ledger_unavailable") else
                             gov.get("note") or "no cycle ran; recognised revenue events were not distributed")}
        cycle_done["report"] = report       # the cycle ran: a later raise is its bookkeeping, not a failed visit
        # W467 (register FU-022) — the governed cycle consumed exactly what it ran on BEFORE it ran (W463: an approval
        # releases the events it was filed for); this path no longer consumes after the ledger has posted
        pend = res.get("consumed") or {"events": 0, "revenue": 0.0, "costs": 0.0}
        if pend["events"]:
            from agentic_core.economy.governance import retire_heartbeat_holds_for_consumed_events
            retire_heartbeat_holds_for_consumed_events(vsb_id)
        stamp = _now()

        def _ran(e: Dict[str, Any]) -> None:
            e["operating_cycles"] = int(e.get("operating_cycles", 0)) + 1
            e["last_operated"] = stamp
            e.pop("last_hold", None)   # a real cycle ran — no standing hold implied
            e.pop("last_error", None)
            e.pop("decision_hold", None)
            e["last_distributable"] = report.get("distributable_profit")
        fresh_entry = _update_entry(vsb_id, _ran)
        cycle_done["booked"] = True
        _ran(target)
        if fresh_entry:
            target["operating_cycles"] = fresh_entry["operating_cycles"]
        # §13 (W309/W340) — autonomous DRIFT is honest AND material: only a cycle that genuinely
        # moved the entity's shipped-visible state marks the repo stale. A zero-activity
        # maintenance cycle changed nothing a page shows — marking it stale caused a perpetual
        # stale→re-ship churn under auto_economy+auto_ship (full 5-surface regeneration + a git
        # commit per beat, audit-measured 81KB DCMS growth in 80s).
        if pend["events"] or (report.get("distributable_profit") or 0) > 0:
            try:
                from agentic_core.api.vsb import mark_repo_stale
                mark_repo_stale(vsb_id, f"autonomous operating cycle {target['operating_cycles']}")
            except Exception:
                pass
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle": target["operating_cycles"],
                # W503 (FU-063) - the SUCCESS return carried no `cycle_ran` key at all, so a reader
                # testing it got None and had to know that None meant yes. Stated, so a reader is right
                # whichever field it reads.
                "outcome": "ran", "cycle_ran": True,
                "distributable_wst": report.get("distributable_profit"),
                "revenue_events_consumed": pend["events"],
                "revenue_recognised_wst": pend["revenue"],
                "revenue_basis": ("recognised_events" if pend["events"]
                                  else "no_activity_maintenance_cycle"),
                "governance": (res.get("governance") or {}).get("status")}
    except Exception as e:
        # W468 — a visit that RAISED is still a visit: last_operated used to advance only on a cycle or a hold, so the
        # least-recently-operated pick chose the same failing entity on every beat and no other entity was tended again
        why = f"{type(e).__name__}: {str(e)[:160]}"
        stamp = _now()
        if cycle_done["report"] is not None:
            # (sixth refutation) the cycle RAN and posted; only the roster's bookkeeping of the visit raised. The row records
            # the cycle (the bookkeeping retried once), never a failed visit or a hold the cycle got past.
            if not cycle_done["booked"]:
                done = cycle_done["report"]

                def _late(en: Dict[str, Any]) -> None:
                    en["operating_cycles"] = int(en.get("operating_cycles", 0)) + 1
                    en["last_operated"] = stamp
                    for key in ("last_hold", "last_error", "decision_hold"):
                        en.pop(key, None)
                    en["last_distributable"] = done.get("distributable_profit")
                try:
                    _update_entry(vsb_id, _late)
                except Exception:
                    pass
            # the cycle POSTED — the outcome is `ran`, and the raise is reported as what it was. W503's
            # own FU-045 heartbeat branch read this as a failed visit until this row corrected it.
            return {"vsb_id": vsb_id, "error": str(e)[:160], "cycle_ran": True, "outcome": "ran",
                    "bookkeeping_raised": True,
                    "note": "the cycle ran and posted; only the roster's bookkeeping of the visit raised"}
        if cycle_done["held"] is not None:
            # (seventh refutation) the visit FOUND a hold; only the roster's bookkeeping of it raised. The row records that
            # hold (the bookkeeping retried once), never the previous visit's hold or a failed visit.
            if not cycle_done["held_booked"]:
                try:
                    _update_entry(vsb_id, cycle_done["held"])
                except Exception:
                    pass
            return {"vsb_id": vsb_id, "error": str(e)[:160], "cycle_ran": False, "held": target.get("last_hold"),
                    # W503 (FU-063) — the RECORD travels here too. Without it this fell back to
                    # "nobody told me" and answered "held", so one recordless gate-error hold was a
                    # DECISION when the roster write raised and a REFUSAL when it did not.
                    "outcome": _outcome_of_hold(target.get("last_hold"),
                                                target.get("last_hold_record", _RECORD_UNKNOWN)),
                    "bookkeeping_raised": True,
                    "note": "the visit found a hold; only the roster's bookkeeping of it raised"}
        # the ledger as it reads NOW decides the ledger hold (the raise may have come before this visit read it)
        try:
            from agentic_core.economy.ledger import VirtualLedger
            unreadable_now: Optional[bool] = VirtualLedger(vsb_id).load_error is not None
        except Exception:
            unreadable_now = None

        past_cc = bool(getattr(e, "past_change_control", False))     # the cycle got past the materiality gate

        def _raised(en: Dict[str, Any]) -> None:
            # (refutations 2–5) the row keeps only what is still true after a visit that raised: a ledger hold exactly
            # while the ledger cannot be read (it stops every cycle first); a Change Control hold unless this visit got
            # past Change Control; a ledger hold when the fresh read itself failed. Anything else — a compliance hold
            # (reaching the cycle proves the screen is not FAIL), an intake or gate hold — is an earlier outcome this
            # raise supersedes (last_error says the raise).
            en.update(last_operated=stamp, last_error=why)
            hold = en.get("last_hold")
            # (sixth refutation) a Change Control decision — the hold itself, or one kept behind a ledger hold — stands
            # unless this visit got past Change Control; it is kept apart while the ledger hold is in front of it
            # W503 (FU-063) — a decision hold with no record is NOT a standing decision. It was kept as
            # one here, so a gate that merely could not be reached left the row asserting Change Control
            # had ruled on this entity.
            _recordless = hold in _DECISION_HOLDS and en.get("last_hold_record", _RECORD_UNKNOWN) is None
            decision = None if (past_cc or _recordless) else (
                hold if hold in _DECISION_HOLDS else en.get("decision_hold"))
            en.pop("decision_hold", None)
            if unreadable_now or (unreadable_now is None and hold == "ledger_unavailable"):
                en["last_hold"] = "ledger_unavailable"
                if decision:
                    en["decision_hold"] = decision
            elif decision:
                en["last_hold"] = decision
            else:
                en.pop("last_hold", None)
        try:
            _update_entry(vsb_id, _raised)
        except Exception:
            pass
        return {"vsb_id": vsb_id, "error": str(e)[:160], "cycle_ran": False, "outcome": "raised"}
