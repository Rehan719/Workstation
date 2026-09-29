"""
Owner-Payments Ledger (§7) — the Owner's accrued share, VIRTUAL/simulated WST only.

Each metabolic cycle's Owner stage (the §4 waterfall's `owner` split) accrues here. The Owner can record a
payout, but **real-money rails are intentionally DISABLED and gated**: no real funds move — a payout is a
virtual ledger entry until the Owner explicitly authorises real rails AND a compliance/KYC review passes.
This keeps a clean seam so real rails can be added later behind that gate, without ever representing simulated
finance as real.

W465 (register FU-016) — the store follows the shared-store convention. It used to be read with every error
swallowed (a corrupt or momentarily locked file read as EMPTY, and the next accrual or even a page view then wrote
back a store holding only one account — every other account's history gone), written with a bare, non-atomic
write_text, with no lock (two accruals lost one; two payouts could both pass the balance check), and a GET wrote
the file. Now: every change is a read-modify-write under the store lock with an atomic write; the read is STRICT —
a store that exists but cannot be read is refused (OwnerPaymentsUnavailable) and never overwritten; status() only
reads, and an account that has never accrued is answered as zeros without creating it.
"""
from __future__ import annotations

import json
import math
import time
import uuid
from typing import Any, Callable, Dict

from agentic_core.config import data_path

_STORE = data_path("economy_owner_payments.json")
# W505 (FU-036) — missed accruals wait HERE, not in the store above: an accrual fails precisely when that store
# cannot be read or locked, so parking the claim in it would lose the claim for the same reason.
_PENDING = data_path("economy_owner_accruals_pending.json")

# BINDING SAFEGUARD — real-money payout rails are OFF until the Owner explicitly authorises them AND a
# compliance/KYC review passes. Until then every payout is a virtual ledger entry; no real funds move.
REAL_MONEY_ENABLED = False


class OwnerPaymentsUnavailable(RuntimeError):
    """The owner-payments store exists but cannot be read (or is not an owner-payments document). Nothing was
    written; the caller answers honestly (503) instead of reporting zero balances."""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))


def _account_ok(a: Any) -> bool:
    return (isinstance(a, dict) and _number(a.get("accrued")) and _number(a.get("paid_out"))
            and isinstance(a.get("entries"), list))


def _read() -> Dict[str, Any]:
    """STRICT read: a missing store is empty; anything else that cannot be read whole is refused."""
    if not _STORE.exists():
        return {}
    raw = None
    for attempt in range(5):
        try:
            raw = _STORE.read_text(encoding="utf-8")
            break
        except FileNotFoundError:
            return {}
        except UnicodeDecodeError as e:       # not an OSError: without this a re-encoded store escaped as a 500/400
            raise OwnerPaymentsUnavailable(f"the owner-payments store is not valid UTF-8 ({e}); nothing was written") from e
        except PermissionError as e:          # Windows: a read that meets an atomic replace mid-flight — retry
            if attempt == 4:
                raise OwnerPaymentsUnavailable(f"the owner-payments store stayed locked ({e})") from e
            time.sleep(0.05 * (attempt + 1))
        except OSError as e:
            raise OwnerPaymentsUnavailable(f"the owner-payments store could not be read ({e})") from e
    try:
        d = json.loads(raw)
    except ValueError as e:
        raise OwnerPaymentsUnavailable(f"the owner-payments store is unreadable ({e}); nothing was written") from e
    if not isinstance(d, dict) or not all(_account_ok(a) for a in d.values()):
        raise OwnerPaymentsUnavailable("the owner-payments store is not an owner-payments document; nothing was written")
    return d


def _mutate(change: Callable[[Dict[str, Any]], Any]) -> Any:
    """Read-modify-write under the store lock. `change` raises to refuse (nothing is written); it must not call
    anything that takes this lock again (store_lock is not re-entrant on its lockfile)."""
    from agentic_core.config import atomic_write_json, store_lock
    with store_lock(_STORE):
        d = _read()
        out = change(d)
        atomic_write_json(_STORE, d)
    return out


def _new_account(vsb_id: str, owner: str) -> Dict[str, Any]:
    return {"vsb_id": vsb_id, "owner": owner, "currency": "WST", "accrued": 0.0, "paid_out": 0.0, "entries": []}


def _pending_read() -> list:
    """The missed accruals waiting to be applied. A store that cannot be read whole is refused rather than
    answered as empty: answering empty would report the Owner as fully paid while credits are outstanding."""
    from agentic_core.config import read_json_strict
    rows = read_json_strict(_PENDING, list, expect=list)
    return [r for r in rows if isinstance(r, dict)]


def record_missed(vsb_id: str, amount: float, owner: str, memo: str, why: str) -> Dict[str, Any] | None:
    """W505 (FU-036) — park an accrual that could not be applied, so it can be applied later.

    Never raises: this runs on the failure path of a cycle that has already posted its waterfall, and a cycle
    must not be turned into an exception by its own bookkeeping. A failure to park is returned, so the caller
    can say the credit is neither applied nor recoverable, which is the worst case and must not be silent.
    """
    from agentic_core.config import atomic_write_json, store_lock
    amount = round(max(0.0, float(amount or 0)), 2)
    if amount <= 0:
        return None
    row = {"id": uuid.uuid4().hex[:12], "vsb_id": vsb_id, "owner": owner, "amount_wst": amount,
           "memo": memo, "why": why, "at": _now(), "attempts": 0}
    try:
        with store_lock(_PENDING):
            rows = _pending_read() if _PENDING.exists() else []
            rows.append(row)
            atomic_write_json(_PENDING, rows)
        return row
    except Exception as exc:
        import logging
        logging.getLogger("owner_payments").error(
            "a missed owner accrual for %s (%s WST) could not even be PARKED: %s — the Owner's balance is "
            "short by this amount and there is no durable claim on it", vsb_id, amount, exc)
        return {"parked": False, "why": f"{type(exc).__name__}: {exc}", "amount_wst": amount}


def reconcile_missed(vsb_id: str | None = None) -> Dict[str, Any]:
    """W505 (FU-036) — apply the missed accruals, idempotently.

    For each pending row: if an entry with its ref is ALREADY on the account it was applied by an attempt that
    died before clearing, so the row is only dropped. Otherwise it is accrued with its id as the ref and then
    dropped. A row whose accrual fails again stays pending with its attempt count raised - it is a claim on the
    Owner's money and must not be discarded for failing twice.
    """
    from agentic_core.config import atomic_write_json, store_lock
    out = {"applied": [], "already_applied": [], "still_pending": [], "store_unreadable": None}
    try:
        rows = _pending_read() if _PENDING.exists() else []
    except Exception as exc:
        out["store_unreadable"] = f"{type(exc).__name__}: {exc}"
        return out
    if not rows:
        return out
    try:
        accounts = _read()
    except OwnerPaymentsUnavailable as exc:
        out["store_unreadable"] = f"{type(exc).__name__}: {exc}"
        return out

    keep, changed = [], False
    for row in rows:
        if vsb_id is not None and row.get("vsb_id") != vsb_id:
            keep.append(row)
            continue
        rid = row.get("id")
        acct = accounts.get(row.get("vsb_id")) or {}
        if any((e or {}).get("ref") == rid for e in (acct.get("entries") or [])):
            out["already_applied"].append({"id": rid, "amount_wst": row.get("amount_wst")})
            changed = True
            continue
        try:
            accrue(row["vsb_id"], row["amount_wst"], row.get("owner") or "Rehan",
                   memo=f"{row.get('memo') or 'missed cycle owner share'} (reconciled)", ref=rid)
            out["applied"].append({"id": rid, "amount_wst": row.get("amount_wst")})
            changed = True
        except Exception as exc:
            row["attempts"] = int(row.get("attempts") or 0) + 1
            row["last_attempt_error"] = f"{type(exc).__name__}: {str(exc)[:160]}"
            keep.append(row)
            out["still_pending"].append({"id": rid, "amount_wst": row.get("amount_wst"),
                                         "attempts": row["attempts"], "why": row["last_attempt_error"]})
            changed = True
    if changed:
        try:
            with store_lock(_PENDING):
                atomic_write_json(_PENDING, keep)
        except Exception as exc:
            # the credits ARE applied; the pending file still names them. Said, because the next run would
            # otherwise re-apply them - which it will not, because the ref check above catches it.
            out["pending_not_cleared_because"] = f"{type(exc).__name__}: {exc}"
    return out


def pending_missed(vsb_id: str | None = None) -> Dict[str, Any]:
    """READ-ONLY: what the Owner is still owed from accruals that failed."""
    try:
        rows = _pending_read() if _PENDING.exists() else []
    except Exception as exc:
        return {"unreadable": f"{type(exc).__name__}: {exc}", "rows": [], "total_wst": None}
    rows = [r for r in rows if vsb_id is None or r.get("vsb_id") == vsb_id]
    return {"rows": rows, "total_wst": round(sum(float(r.get("amount_wst") or 0) for r in rows), 2),
            "unreadable": None}


def accrue(vsb_id: str, amount: float, owner: str = "Rehan", memo: str = "cycle owner share",
           ref: str | None = None) -> Dict[str, Any] | None:
    """Accrue the Owner's share from a cycle (virtual WST). Returns the account, or None for a zero amount.
    Raises ValueError for a non-finite amount and OwnerPaymentsUnavailable / TimeoutError when the store cannot be
    read or locked — the caller must say so (an accrual is never silently dropped)."""
    if not math.isfinite(float(amount)):
        raise ValueError("An owner accrual must be a finite amount.")
    amount = round(max(0.0, float(amount)), 2)
    if amount <= 0:
        return None

    def change(d: Dict[str, Any]) -> Dict[str, Any]:
        a = d.get(vsb_id) or _new_account(vsb_id, owner)
        d[vsb_id] = a
        a["accrued"] = round(a["accrued"] + amount, 2)
        a["entries"].append({"id": uuid.uuid4().hex[:8], "type": "accrual",
                             "amount_wst": amount, "memo": memo, "at": _now(),
                             # W505 (FU-036) — the reconciliation's idempotence key: a re-applied accrual
                             # carries the pending row's id, so a second attempt can see its own work.
                             **({"ref": ref} if ref else {})})
        a["entries"] = a["entries"][-200:]
        return json.loads(json.dumps(a))
    return _mutate(change)


def status(vsb_id: str, owner: str = "Rehan") -> Dict[str, Any]:
    """READ-ONLY: the account as stored, or zeros for an account that has never accrued (nothing is created)."""
    a = _read().get(vsb_id) or _new_account(vsb_id, owner)
    balance = round(a["accrued"] - a["paid_out"], 2)
    return {
        "vsb_id": vsb_id, "owner": a.get("owner", owner), "currency": "WST",
        "accrued_total_wst": a["accrued"], "paid_out_total_wst": a["paid_out"],
        "balance_wst": balance, "entries": a["entries"][-50:][::-1],
        # W505 (FU-036) - what the Owner is OWED from accruals that failed. Without this the balance reads as
        # the whole picture while credits sit unapplied in the pending store, which is the same silence the row
        # is about one layer along.
        "pending_from_failed_accruals": pending_missed(vsb_id),
        "real_money_rails": "DISABLED", "real_money_enabled": REAL_MONEY_ENABLED,
        "note": "Virtual/simulated WST only. Real-money payouts are gated until the Owner explicitly "
                "authorises real rails AND a compliance/KYC review passes — no real funds move.",
    }


def payout(vsb_id: str, amount: float, owner: str = "Rehan") -> Dict[str, Any]:
    """Record a VIRTUAL payout (reduces the accrued balance). Never moves real funds — rails are disabled. The
    balance check and the write happen under one lock, so two payouts can never both spend the same balance."""
    if not math.isfinite(float(amount)):
        raise ValueError("Payout amount must be a finite number.")
    amount = round(max(0.0, float(amount)), 2)
    if amount <= 0:
        raise ValueError("Payout amount must be positive.")

    def change(d: Dict[str, Any]) -> float:
        a = d.get(vsb_id)
        balance = round(a["accrued"] - a["paid_out"], 2) if a else 0.0
        if amount > balance:
            raise ValueError(f"Insufficient balance: {balance} WST available, {amount} WST requested.")
        a["paid_out"] = round(a["paid_out"] + amount, 2)
        a["entries"].append({"id": uuid.uuid4().hex[:8], "type": "payout_virtual", "amount_wst": amount,
                             "memo": "virtual payout — no real funds moved (rails disabled)", "at": _now()})
        a["entries"] = a["entries"][-200:]
        return round(a["accrued"] - a["paid_out"], 2)
    remaining = _mutate(change)
    return {
        "paid_wst": amount, "remaining_balance_wst": remaining,
        "real_money_moved": False, "real_money_rails": "DISABLED",
        "note": "Virtual payout recorded. No real money moved — real rails are gated pending Owner "
                "authorisation + a compliance/KYC review.",
    }
