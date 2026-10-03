"""What each of the six cycles is actually bound to — and, for three of them, that it is bound to nothing.

P3.19's bar: "every cycle reports a measured figure or says it cannot". The second half is not a fallback,
it is half the requirement, and it is the half this package has never been able to express.

WHAT WAS HERE BEFORE: nothing. Each cycle class set a `reservoirs` dict of literals in __init__ —
carbon's active_data 0.0 against a setpoint of 50.0, water's ocean 97.0, and so on — and no code anywhere
ever wrote to them. So `sense()` returned the literal, `deviation()` divided it by the setpoint, and a
cycle nobody had measured reported a precise fractional departure from target. carbon's was 1.0: a 100%
deviation, arithmetically correct, over a number that came from a source-code line. Three outside
specifications then described these six as a running PID control layer holding ±5%.

THE RULE THIS FILE FOLLOWS, taken from agentic_core/cognitive/auxiliary/mudrik_engine.py, which already
answers this way: every reader returns {assessable, value, measured_from, basis}. `assessable: False` is
never accompanied by a value, a 0.0 never stands in for "unknown", and `basis` always names which reader
was consulted and what it said. A binding that cannot read its source says so in the same shape as one
that can, so a consumer cannot tell them apart by accident.

AND IT OPENS NO STORE OF ITS OWN. Every figure below comes from the module that already owns it — the
economy's ledger, the organism's heartbeat. This file calls no data_path(), writes no JSON and defines no
state, because a second copy of a number is how two surfaces come to disagree about one fact. That is
P3.19's "no second store of numbers" clause, applied to the code that reads rather than to a store.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

#  The six cycles and the flow each is MEANT to track, from the mapping P3.19 adopts. Being named here is
#  not being bound: three of these have no verified reader on this platform today and report so.
CYCLE_SUBJECTS = {
    "water": "liquidity",
    "carbon": "growth",
    "nitrogen": "risk",
    "oxygen": "metabolism",
    "phosphorus": "allocation",
    "sulfur": "resilience",
}


def _unassessable(reader: str, why: str) -> Dict[str, Any]:
    """The refusal shape. No `value` key at all — not None, absent.

    A None value invites `value or 0`, which is how the figure comes back. The key is simply not there,
    so a consumer that wants a number has to confront the assessable flag to get one.
    """
    return {"assessable": False, "measured_from": None, "unit": None,
            "basis": f"NOT ASSESSED: {why} (reader consulted: {reader})"}


def _assessed(value: float, reader: str, what: str, unit: str) -> Dict[str, Any]:
    """W544 — `unit` is required, not optional.

    A reading with no unit cannot be compared to anything, and W543 proved what happens when it is tried
    anyway: a liquidity in virtual WST was divided by a setpoint that turned out to be a temperature. The
    surface now decides whether a deviation is meaningful by comparing this unit against the one the
    cycle's setpoint declares, which is a computation rather than a blanket rule.
    """
    return {"assessable": True, "value": float(value), "measured_from": reader, "unit": unit,
            "basis": f"{what} = {value} ({unit}), read from {reader}"}


def water(vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Liquidity: the VSB's own ledger balance. Virtual WST — no real-money rail is touched.

    The ledger refuses to answer over an unreadable store (`require_readable` raises StoreUnavailable),
    and that refusal is carried through as unassessable rather than swallowed into a zero. A corrupt store
    reporting a liquidity of 0.0 would be the worst available answer: it reads as insolvency.
    """
    if not vsb_id:
        return _unassessable("agentic_core/economy/ledger.py::VirtualLedger.balances",
                             "no VSB was named, and liquidity is a property of an entity's ledger rather "
                             "than of the platform")
    try:
        from agentic_core.economy.ledger import VirtualLedger
        bal = VirtualLedger(vsb_id).balances()
    except Exception as e:                       # noqa: BLE001 — the store's state is part of the answer
        return _unassessable("agentic_core/economy/ledger.py::VirtualLedger.balances",
                             f"the ledger for {vsb_id} could not be read ({e.__class__.__name__}: {e}), "
                             f"so there is no balance. An unreadable ledger is not an empty one")
    total = sum(v for v in bal.values() if isinstance(v, (int, float)))
    #  NAMED EXACTLY, because this ledger holds TWO sets of money figures and they are not the same set.
    #  `balances()` is the seven waterfall pots, maintained by `record()`. `_apply_posting` maintains a
    #  separate double-entry account chart, which `post()` writes and this figure does not include —
    #  measured W543: record(reserves, 750) leaves the chart at 0.0, and a subsequent
    #  post(revenue, reserves, 500) leaves the pots at 750 while the chart reads -500 on both sides.
    #  Reporting one of them as "the ledger balance" without saying which would be the over-claim.
    return _assessed(total, "agentic_core/economy/ledger.py::VirtualLedger.balances",
                     f"the sum of {len(bal)} WATERFALL POT balance(s) for {vsb_id} — the projection "
                     f"`record()` maintains, NOT the double-entry account chart that `post()` writes; the "
                     f"two are maintained separately and can disagree (see the register)",
                     unit="virtual WST")


def carbon(vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Growth: how much the ledger has actually recorded — the posting count, not a rate.

    A GROWTH RATE IS NOT AVAILABLE and is not invented here. A rate needs two readings separated in time,
    and nothing on this platform stores a historical series of this figure. What is honestly readable is
    the cumulative count of recorded postings, which is a measurement of activity; calling it growth
    would be the over-claim, so the basis says what it is.
    """
    if not vsb_id:
        return _unassessable("agentic_core/economy/ledger.py::VirtualLedger.trial_balance",
                             "no VSB was named, and recorded activity belongs to an entity's ledger")
    try:
        from agentic_core.economy.ledger import VirtualLedger
        tb = VirtualLedger(vsb_id).trial_balance()
    except Exception as e:                       # noqa: BLE001
        return _unassessable("agentic_core/economy/ledger.py::VirtualLedger.trial_balance",
                             f"the ledger for {vsb_id} could not be read ({e.__class__.__name__}: {e})")
    return _assessed(tb.get("postings", 0), "agentic_core/economy/ledger.py::VirtualLedger.trial_balance",
                     f"the cumulative count of recorded postings for {vsb_id} — ACTIVITY, not a growth "
                     f"rate: a rate needs two readings in time and no series of this figure is stored",
                     unit="postings (a count, not a rate)")


def oxygen(vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Metabolism: the organism's own beat count — a counter the heartbeat increments as it works."""
    try:
        from agentic_core.organism.heartbeat import heartbeat
        st = heartbeat.status()
    except Exception as e:                       # noqa: BLE001
        return _unassessable("agentic_core/organism/heartbeat.py::OrganismHeartbeat.status",
                             f"the heartbeat did not report ({e.__class__.__name__}: {e})")
    beats = st.get("beats")
    if not isinstance(beats, (int, float)):
        return _unassessable("agentic_core/organism/heartbeat.py::OrganismHeartbeat.status",
                             "the heartbeat reported no beat count")
    #  A STOPPED HEARTBEAT IS A REAL READING OF ZERO, and that is said rather than left to look like an
    #  absence: the beat is OFF by default on this platform, so 0 beats is the normal honest answer and
    #  must not be confused with "could not be measured".
    return _assessed(beats, "agentic_core/organism/heartbeat.py::OrganismHeartbeat.status",
                     f"beats completed by the organism heartbeat (running={st.get('running')}; a "
                     f"stopped beat genuinely measures 0, which is not the same as unmeasured)",
                     unit="beats (a count)")


def nitrogen(vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Risk: UNBOUND, and this names the reader that would bind it.

    The immune system exposes `evaluate_threat(sample)` (agentic_core/genetic_immune/immune_system.py),
    which SCORES A SAMPLE a caller supplies — it is not a standing measurement of platform risk, and
    feeding it a sample composed here would be this file measuring its own invention. There is no stored
    risk series to read instead.
    """
    return _unassessable("agentic_core/genetic_immune/immune_system.py::evaluate_threat",
                         "the immune system scores a SAMPLE a caller supplies and holds no standing risk "
                         "figure, so binding it here would mean scoring a sample this module invented. "
                         "To bind it: record each evaluate_threat result as it happens, then read that "
                         "series")


def phosphorus(vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Allocation: UNBOUND. The §4 waterfall's proportions are a SETTING, not a measurement.

    The six-stage waterfall is configurable per VSB and its shares are read back from configuration, so
    reporting them as an allocation reading would report what was asked for rather than what happened.
    The measurement would be the distributions actually executed against those shares.
    """
    return _unassessable("agentic_core/economy — the §4 waterfall configuration",
                         "the waterfall's shares are a configured SETTING; reading them back would report "
                         "the intention rather than the allocation. To bind it: read the distributions "
                         "actually executed against those shares")


def sulfur(vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Resilience: UNBOUND. Nothing on this platform measures recovery from a failure.

    Resilience is a property of behaviour under failure — how often something broke and how long it took
    to come back. The organism records healing and recovery TIMESTAMPS, which say that something happened
    and not how well it went, and a count of heals is not a resilience figure.
    """
    return _unassessable("agentic_core/organism/heartbeat.py — the healing and recovery timestamps",
                         "the organism records WHEN it last healed or recovered, which is not a measure "
                         "of resilience: a count of heals says nothing about time-to-recover or about "
                         "failures that never recovered. To bind it: record each failure with its "
                         "recovery, then read the distribution")


READERS = {"water": water, "carbon": carbon, "nitrogen": nitrogen,
           "oxygen": oxygen, "phosphorus": phosphorus, "sulfur": sulfur}


def read_all(vsb_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """Every cycle's binding, each answering for itself. One reader's failure is not another's."""
    out: Dict[str, Dict[str, Any]] = {}
    for name, fn in READERS.items():
        try:
            out[name] = {**fn(vsb_id), "subject": CYCLE_SUBJECTS[name]}
        except Exception as e:                   # noqa: BLE001 — a reader that raises is unassessable
            out[name] = {**_unassessable(f"{name} reader",
                                         f"the reader itself raised {e.__class__.__name__}: {e}"),
                         "subject": CYCLE_SUBJECTS[name]}
    return out
