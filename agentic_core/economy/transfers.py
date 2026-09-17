"""Inter-VSB transfers (§federation seed) — generated Enterprise IDBOs TRANSACT with each other.

Semantics (virtual WST only — no real funds, real-money rails stay Owner-gated):
  • The SENDER pays from its reserve fund — a balanced double-entry posting
    (Dr transfer_out expense / Cr reserve_fund), refused when the fund can't cover it
    (no negative virtual balances, no money from nothing).
  • The RECEIVER's amount queues as PENDING and is consumed by its NEXT metabolic cycle as
    intake revenue — so the received WST genuinely enters the receiver's §4 waterfall
    (the same recycle pattern as venture returns, W259).
  • The receiver must be a REGISTERED living VSB (no transfers into the void).
"""
from __future__ import annotations

import math
import time
import uuid
from typing import Any, Dict, Optional

from agentic_core.config import atomic_write_json, data_path, load_json_tolerant, store_lock

_PENDING_STORE = data_path("economy_pending_transfers.json")


class PendingStoreUnavailable(RuntimeError):
    """The pending-transfers store exists but cannot be read whole. Nothing is written. (Deliberately not a ValueError:
    the transfer route reads ValueError as a refused funds check.)"""


def _read_pending() -> Dict[str, Any]:
    """W465 — STRICT read of the pending-transfers store for every WRITER. The tolerant read answered {} for a store it
    could not read (re-encoded, a BOM, an OSError), and the write that followed replaced every receiver's pending
    intake and credited-id record with one receiver's — destroying queued receipts, and letting a settlement's late
    replay credit its provider a second time."""
    import json as _json
    if not _PENDING_STORE.exists():
        return {}
    raw = None
    for attempt in range(5):
        try:
            raw = _PENDING_STORE.read_text(encoding="utf-8")
            break
        except FileNotFoundError:
            return {}
        except UnicodeDecodeError as e:
            raise PendingStoreUnavailable(f"the pending-transfers store is not valid UTF-8 ({e}); nothing was written") from e
        except PermissionError as e:
            if attempt == 4:
                raise PendingStoreUnavailable(f"the pending-transfers store stayed locked ({e})") from e
            time.sleep(0.05 * (attempt + 1))
        except OSError as e:
            raise PendingStoreUnavailable(f"the pending-transfers store could not be read ({e})") from e
    try:
        d = _json.loads(raw)
    except ValueError as e:
        raise PendingStoreUnavailable(f"the pending-transfers store is unreadable ({e}); nothing was written") from e
    if not isinstance(d, dict):
        raise PendingStoreUnavailable("the pending-transfers store is not a pending-transfers document; nothing was written")
    # W465 (fifth refutation) — every record's shape too: a record the intake could not do arithmetic on (a null
    # consumed total, a string, NaN or negative amount, a non-list queue) passed the document check, so the gate
    # measured receipts the cycle then refused (an Owner approval spent on a cycle that took nothing), and a transfer
    # to that receiver debited the sender before failing. The store is refused whole, before any debit or estimate.
    bad = next((k for k, rec in d.items() if not _record_ok(rec)), None)
    if bad is not None:
        raise PendingStoreUnavailable(f"the pending-transfers store holds a malformed record for {str(bad)[:80]}; "
                                      "nothing was written")
    return d


def _amount_ok(v: Any) -> bool:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return False
    try:
        return math.isfinite(v) and v >= 0
    except OverflowError:          # an integer too large for a float is no amount any writer produces
        return False


def _record_ok(rec: Any) -> bool:
    """A receiver's pending record as record_transfer and consume_pending_transfers write it — down to the ids,
    which record_transfer hashes after the debit (an unhashable id failed there, leaving the sender debited)."""
    if not isinstance(rec, dict):
        return False
    if not _amount_ok(rec.get("pending_wst", 0.0)) or not _amount_ok(rec.get("consumed_total_wst", 0.0)):
        return False
    transfers = rec.get("transfers")
    if transfers is not None and not (isinstance(transfers, list) and all(
            isinstance(t, dict) and isinstance(t.get("transfer_id"), (str, type(None))) for t in transfers)):
        return False
    credited = rec.get("credited_ids")
    return credited is None or (isinstance(credited, list) and all(isinstance(i, str) for i in credited))


def _receiver_id_ok(to_vsb: Any, transfer_id: str = "xfer-0000000000") -> None:
    """W465 (register FU-046) — a debit is recognised by its system memo head, which ends at the first ' — '. The
    memo record_transfer WRITES is checked, not the bare id: a receiver or transfer id that puts the separator into
    that memo (inside the id, or a dash at its edge, which the template's spaces complete) would hide the transfer's own
    debit from a replay, which would then debit again."""
    if not _memo_names(f"inter-VSB transfer → {to_vsb} ({transfer_id})", transfer_id):
        raise ValueError("A receiver or transfer id cannot put ' — ' into the transfer's memo (it would hide the "
                         "transfer's own debit from a replay).")


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _validate_shape(from_vsb: str, to_vsb: str, amount: float) -> float:
    # W442 — NaN passed EVERY guard below (nan <= 0 and reserve < nan are both False), and one
    # NaN posting set reserve_fund=NaN, permanently disabling the insufficient-funds check.
    if not math.isfinite(float(amount)):
        raise ValueError("Transfer amount must be a finite number.")
    amount = round(float(amount), 2)
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if from_vsb == to_vsb:
        raise ValueError("A VSB cannot transfer to itself.")
    _receiver_id_ok(to_vsb)
    from agentic_core.economy.living_vsbs import _load as _living
    if to_vsb not in _living():
        raise KeyError(f"Receiver '{to_vsb}' is not a registered living VSB — no transfers into the void.")
    return amount


def validate_transfer(from_vsb: str, to_vsb: str, amount: float) -> float:
    """Side-effect-free validation (callable BEFORE the governance gate so errors map to clean HTTP
    codes). Raises ValueError (→400) on bad amounts/self-transfer/insufficient funds, KeyError
    (→404) when the receiver is not a registered living VSB. Returns the rounded amount."""
    # W442 — NaN passed EVERY guard below (nan <= 0 and reserve < nan are both False), and one
    # NaN posting set reserve_fund=NaN, permanently disabling the insufficient-funds check.
    amount = _validate_shape(from_vsb, to_vsb, amount)
    from agentic_core.economy.ledger import VirtualLedger
    reserve = round((VirtualLedger(from_vsb)._data.get("accounts") or {}).get("reserve_fund", 0.0), 2)
    if reserve < amount:
        raise ValueError(f"Insufficient virtual funds: {from_vsb} reserve fund holds {reserve} WST "
                         f"< transfer {amount} WST.")
    return amount


def record_transfer(from_vsb: str, to_vsb: str, amount: float, memo: str = "",
                    transfer_id: str | None = None) -> Dict[str, Any]:
    """One inter-VSB transfer: checks the amount's shape and refuses a self-transfer, then — only for a
    transfer id not yet debited — checks the receiver's liveness and the sender's funds inside the ledger lock
    (a replay skips both and repairs a missing receiver leg), posts the sender's books, queues
    the receiver's intake. Virtual funds are conserved — nothing created, nothing negative.

    W442 — the funds check now runs ATOMICALLY with the debit (inside the ledger's store lock):
    two concurrent transfers both reading reserve=100 used to both pass validation and both post.
    A caller-supplied transfer_id makes the posting IDEMPOTENT (the gaas fallback path could
    retry after the action had already executed — one request, two debits)."""
    from agentic_core.economy.ledger import VirtualLedger
    sender = VirtualLedger(from_vsb)
    transfer_id = transfer_id or f"xfer-{uuid.uuid4().hex[:10]}"
    # W465 — refuse BEFORE debiting while the receiver's queue cannot be read (a debit then had nowhere to land)
    _read_pending()
    # W463 — a REPLAY of a transfer whose debit already posted must reach the W442 receiver-leg repair. The
    # funds pre-check (the post-debit reserve can be below the amount) and the receiver-liveness check (the
    # receiver was checked when the debit posted; a later deregistration or a raced registry read would
    # strand the debited WST) used to refuse it first. So only the amount's own shape is checked up front;
    # liveness and funds are checked INSIDE the ledger lock, and only for a transfer not yet debited.
    if not math.isfinite(float(amount)):
        raise ValueError("Transfer amount must be a finite number.")
    amount = round(float(amount), 2)
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if from_vsb == to_vsb:
        raise ValueError("A VSB cannot transfer to itself.")
    _receiver_id_ok(to_vsb, transfer_id)
    with store_lock(sender.path):
        sender._data = sender._load()
        reserve = round((sender._data.get("accounts") or {}).get("reserve_fund", 0.0), 2)
        already = any(_posting_names(p, transfer_id) for p in sender._data.get("postings", []))
        if already:
            posted = False
        else:
            from agentic_core.economy.living_vsbs import _load as _living
            if to_vsb not in _living():
                raise KeyError(f"Receiver '{to_vsb}' is not a registered living VSB — no transfers into the void.")
            if reserve < amount:
                raise ValueError(f"Insufficient virtual funds: {from_vsb} reserve fund holds "
                                 f"{reserve} WST < transfer {amount} WST.")
            sender._apply_posting("transfer_out", "reserve_fund", amount,
                                  memo=f"inter-VSB transfer → {to_vsb} ({transfer_id})"
                                       + (f" — {memo}" if memo else ""))
            sender._save()
            posted = True

    # queue the receiver's intake (consumed by its next metabolic cycle → enters its waterfall)
    repaired = False
    with store_lock(_PENDING_STORE):
        d = _read_pending()
        rec = d.get(to_vsb) or {"vsb_id": to_vsb, "pending_wst": 0.0, "transfers": []}
        # W442 refuter catch: a first attempt can die BETWEEN the sender's debit and this queue
        # write; the replay then found the debit, skipped the queue unconditionally, and reported
        # green — sender debited, receiver never credited. A replay now REPAIRS the missing leg.
        # W465 — whether this id was already credited is read from a DURABLE, untrimmed record. The display list keeps
        # only the last 50 transfers, and a settlement now replays its persisted transfer id after any delay: once 50
        # other transfers had reached the receiver, the replay found nothing and credited the receiver again (virtual
        # WST created). Records written before W465 seed the durable list from the display list (a late replay was
        # impossible then: every id was minted per request).
        credited = rec.get("credited_ids")
        if not isinstance(credited, list):
            credited = [t.get("transfer_id") for t in (rec.get("transfers") or []) if t.get("transfer_id")]
        queued = transfer_id in set(credited)
        # never credit an id already credited, even on a fresh debit: once a settlement retries under the id its claim
        # persisted, two requests can carry one id, and "posted" alone credited the receiver a second time when the
        # other request had queued it first
        if not queued:
            repaired = (not posted) and (not queued)
            rec["pending_wst"] = round(rec.get("pending_wst", 0.0) + amount, 2)
            rec["transfers"] = (rec.get("transfers") or [])[-49:] + [{
                "transfer_id": transfer_id, "from_vsb": from_vsb, "amount_wst": amount,
                "memo": memo, "at": _now()}]
            rec["credited_ids"] = credited + [transfer_id]
            d[to_vsb] = rec
            atomic_write_json(_PENDING_STORE, d)

    return {
        "transfer_id": transfer_id, "from_vsb": from_vsb, "to_vsb": to_vsb,
        "amount_wst": amount, "memo": memo, "at": _now(),
        # on an idempotent replay the debit already happened — reserve is already post-debit
        "idempotent_replay": not posted,
        "replay_repaired_receiver_leg": repaired,
        "sender_reserve_fund_after_wst": round(reserve - amount, 2) if posted else reserve,
        "receiver_pending_wst": rec["pending_wst"],
        "settlement": "the receiver's next metabolic cycle consumes this as intake revenue "
                      "(enters its §4 waterfall)",
        "disclaimer": "Virtual/simulated WST — no real funds moved.",
    }


def _memo_names(memo, transfer_id: str) -> bool:
    """Whether a posting memo is THE memo record_transfer wrote for this id: "inter-VSB transfer → <to> (<id>)",
    optionally followed by " — <caller's memo>". W465: the id used to be matched anywhere in the memo, and the
    caller's memo text is appended verbatim — a transfer whose memo merely CONTAINED "(<id>)" read as that id's
    debit (harmless while ids were minted per request; a settlement's id is persisted and reused on a retry).
    Only the system-written part before the caller's memo counts; the bracket keeps xfer-abc from matching xfer-abcd."""
    head = str(memo or "").split(" — ", 1)[0]
    return head.startswith("inter-VSB transfer → ") and head.endswith(f"({transfer_id})")


def _posting_names(posting, transfer_id: str) -> bool:
    """A posting is this transfer's DEBIT: the transfer_out/reserve_fund entry with its system memo."""
    return (isinstance(posting, dict) and posting.get("debit") == "transfer_out"
            and _memo_names(posting.get("memo"), transfer_id))


def debit_posted(from_vsb: str, transfer_id: str) -> bool:
    """W463 — whether the sender's books carry this transfer's debit. record_transfer posts the debit
    and queues the receiver in two steps, so a failure after the debit is not "nothing posted": a caller
    deciding whether to give back a spent approval must ask the ledger, not its own progress flag.
    Raises if the ledger cannot be read (the caller must then assume it posted).

    Reads STRICTLY: the ledger's own loader is tolerant by design (an unreadable or half-written file reads
    as empty books), and "empty" here would mean "never debited" — giving back an approval whose transfer
    did debit. Only a ledger file that does not exist is a genuine "no debit". It reads WITHOUT the store
    lock: every write of this transfer id was made by the asking request's own calls, which have returned,
    and atomic_write_json (os.replace) means an unlocked read sees a whole file — so a writer holding the
    lock for another transfer can no longer keep the answer (and the approval) hostage."""
    import json as _json
    from agentic_core.economy.ledger import VirtualLedger
    path = VirtualLedger(from_vsb).path
    if not path.exists():
        return False
    for attempt in range(5):
        try:
            data = _json.loads(path.read_text(encoding="utf-8"))
            break
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.05)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} is not a ledger object")
    return any(_posting_names(p, transfer_id) for p in data.get("postings", []))


def peek_pending_transfers(vsb_id: str) -> float:
    """W442 — READ-ONLY view of the queued receipts, for the §3 materiality estimate: the gate
    used to see only the request's revenue while run_cycle added these receipts AFTER the gate,
    so stuffing the queue bypassed Change Control entirely.

    W465 — it reads the store the way the cycle's intake does: a tolerant read measured receipts a store the
    intake refuses still held (a whole document followed by stray bytes), so the Owner was asked to approve — and
    spent an approval on — a cycle that then took nothing. A store the intake cannot read measures nothing."""
    try:
        d = _read_pending()
    except PendingStoreUnavailable:
        return 0.0
    rec = d.get(vsb_id)
    if not rec:
        return 0.0
    # the strict read has checked every record's shape, so this is exactly the amount consume_pending_transfers
    # can take — a store it would refuse measures nothing (above)
    return round(rec.get("pending_wst", 0.0), 2)


def consume_pending_transfers(vsb_id: str, max_amount: Optional[float] = None) -> float:
    """Drain the queued inter-VSB receipts for a VSB — called by the metabolic cycle at intake.
    Returns the consumed amount (0.0 when none pending). W463 — `max_amount` caps the drain at what the
    materiality gate measured; the remainder stays pending for the next cycle."""
    with store_lock(_PENDING_STORE):
        d = _read_pending()
        rec = d.get(vsb_id)
        if not rec:
            return 0.0
        pending = round(rec.get("pending_wst", 0.0), 2)
        take = pending if max_amount is None else round(min(pending, max(0.0, float(max_amount))), 2)
        if take <= 0:
            return 0.0
        rec["pending_wst"] = round(pending - take, 2)
        rec["consumed_total_wst"] = round(rec.get("consumed_total_wst", 0.0) + take, 2)
        d[vsb_id] = rec
        atomic_write_json(_PENDING_STORE, d)
    return take
