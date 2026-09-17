"""§3/§8 economic governance (VSB_ECONOMIC_LEGAL_MODEL.md).

Three binding rules the model states, previously unenforced on the always-on paths:
  • "every distribution passes the gaas.v5 gate" — including the heartbeat-driven autonomous cycles
    (the API path was gated but its failure fallback silently ran ungated; the heartbeat path had
    no gate at all).
  • "Every cycle's split is logged to the UEG" — an explicit tamper-evident event carrying the
    per-stage WST amounts, not just a generic checkpoint.
  • "material/large actions route to Change Control" — distributions (and inter-VSB transfers) whose estimated
    amount meets the materiality threshold are HELD until the Change Control hold the economy itself filed for
    that action is approved — W464: by the Owner's explicit decision only, the hold being CRITICAL (W463: one
    approval releases one action of the same kind — same VSB, and the same
    counterparty for a transfer — for at most the amount and intake it was filed for, and is spent once;
    below-threshold actions proceed ungated-by-CC as designed).

All amounts are virtual/simulated WST — no real funds move (real-money rails stay Owner-gated).
"""
from __future__ import annotations

import os
import re
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

# Materiality threshold (WST). Estimated distributable profit at/above this requires a Change
# Control approval before the cycle may run. Env-configurable for deployments/tests.
MATERIALITY_WST = float(os.getenv("ECONOMY_MATERIALITY_WST", "250000"))

_HOLD_TITLE_PREFIX = "[economy] material distribution — "


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class _Moved(Exception):
    """W459 — raised inside a locked change mutation when the record moved since the scan that
    chose it; the caller decides honestly instead of overwriting the newer decision."""

    def __str__(self) -> str:
        return str(self.args[0] if self.args else "unknown")


def _ueg_log(event: Dict[str, Any]) -> Optional[str]:
    try:
        from agentic_core.gaas.v5 import UEGLogger
        return UEGLogger().log(event)
    except Exception:
        return None


def _log_split(report: Dict[str, Any], waterfall_source: str, source: str) -> None:
    """The binding '§4: every cycle's split is logged to the UEG' — explicit per-stage amounts."""
    circ = report.get("circulation") or {}
    _ueg_log({
        "type": "economy.cycle_split",
        "vsb_id": report.get("vsb_id"),
        "entity_type": report.get("entity_type"),
        "source": source,
        "intake_revenue_wst": report.get("intake_revenue"),
        "distributable_wst": report.get("distributable_profit"),
        "splits_wst": {k: (v or {}).get("amount_wst") for k, v in circ.items()},
        "waterfall_source": waterfall_source,
        "reserve_rate_applied": report.get("reserve_rate_applied"),
        "disclaimer": "Virtual/simulated WST — no real funds moved.",
    })


def _estimate_distributable(revenue: float, costs: float, reserve_rate: float) -> float:
    reserves = costs + max(0.0, float(revenue)) * float(reserve_rate)
    return round(max(0.0, float(revenue) - reserves), 2)


def _pending_parts(vsb_id: str) -> Tuple[float, float]:
    """W442 — the §3 gate estimated from the REQUEST's revenue only, while run_cycle adds pending
    venture returns AND inter-VSB receipts AFTER the gate: queueing 1M WST via /ventures/return
    then cycling with revenue=0 distributed the whole 1M ungated. The gate now sees (read-only)
    everything the cycle will consume — and W463: the cycle consumes AT MOST what the gate saw
    (run_cycle's caps), so a receipt landing between the gate and the cycle waits for the next one
    instead of being distributed without the hold its size would have required."""
    returns, transfers = 0.0, 0.0
    try:
        from agentic_core.economy.ventures import peek_pending_returns
        returns = peek_pending_returns(vsb_id)
    except Exception:
        pass
    try:
        from agentic_core.economy.transfers import peek_pending_transfers
        transfers = peek_pending_transfers(vsb_id)
    except Exception:
        pass
    return round(returns, 2), round(transfers, 2)


def _pending_intake(vsb_id: str) -> float:
    return round(sum(_pending_parts(vsb_id)), 2)


def _hold_title(vsb_id: str, source: str) -> str:
    return (("[economy] material transfer — " + vsb_id) if source == "transfer"
            else _HOLD_TITLE_PREFIX + vsb_id)


def _restore_consumed_approval(consumed: Optional[Dict[str, Any]], *, vsb_id: str, reason: str) -> Optional[str]:
    """W442 refuter catch: _materiality_gate consumes the Owner's approval at gate time, BEFORE
    the constitutional gate or the action runs. When the action then never runs (gate blocked, or
    the atomic funds re-check refused a raced transfer), the approval must not stay spent.

    W463 — the restore used to RE-DISCOVER its target by scan (the latest 'implemented' record with
    the hold's title) and ran whether or not this action had consumed anything: a blocked NON-material
    transfer or cycle re-approved an approval an EARLIER successful action had spent (or one an admin
    implemented), and the next material action spent it a second time. It now restores exactly the
    consumption the gate handed back — `consumed` = {cca_id, consume_id, release, gate} (gate = the action's
    source/counterparty, whose lock the restore takes), or None when nothing was
    consumed (then nothing is touched) — and only while that record's latest spend is still THIS one.

    W465 — it returns what happened, so no answer claims a give-back that did not happen: "restored", "superseded"
    (a newer record for the action replaced it), "moved" (the record changed meanwhile), "failed" (busy or
    unreadable; the approval stays spent), or None when nothing was consumed."""
    if not consumed:
        return None
    cca_id, consume_id = consumed.get("cca_id"), consumed.get("consume_id")
    gate = consumed.get("gate") if isinstance(consumed.get("gate"), dict) else None
    try:
        from agentic_core.api import change_control as cca
        if gate is None:
            return _restore_locked(cca, cca_id, consume_id, vsb_id, reason, None)
        # W463 (third refutation) — the restore ran outside the gate's per-action lock: between the spend and the
        # give-back another request (another worker) could file a fresh hold for the same action, and the restore
        # then revived the older approval beside it — two live records, and the revived approval was spent even
        # after the Owner rejected the newer hold. It now holds the same lock and gives nothing back when a newer
        # live or rejected record exists for the action.
        try:
            with _gate_lock(vsb_id, gate.get("source"), gate.get("counterparty")):
                return _restore_locked(cca, cca_id, consume_id, vsb_id, reason, gate)
        except Exception as err:
            _ueg_log({"type": "economy.materiality_approval_restore_failed", "vsb_id": vsb_id, "cca_id": cca_id,
                      "error": f"gate lock: {str(getattr(err, 'detail', None) or err)[:180]}", "reason": reason[:200]})
            return "failed"
    except Exception:
        return "failed"


def _restore_locked(cca, cca_id: Optional[str], consume_id: Optional[str], vsb_id: str, reason: str,
                    gate: Optional[Dict[str, Any]]) -> str:
    withdrawn: List[Dict[str, Any]] = []
    if gate is not None:
        mine = cca._load_change(cca_id)
        if not mine:
            # W465 (fourth refutation) — compared against {}, every OLDER record for the action read as newer and the
            # answer said a newer record replaced the approval; the approval stays spent and the answer says it failed
            _ueg_log({"type": "economy.materiality_approval_restore_failed", "vsb_id": vsb_id, "cca_id": cca_id,
                      "error": "the spent approval's record could not be read", "reason": reason[:200]})
            return "failed"
        source, counterparty = str(gate.get("source") or ""), gate.get("counterparty")
        title = _hold_title(vsb_id, source)
        newer = [c for c in (cca._load_change(x["cca_id"]) or {} for x in cca._list_changes())
                 if c and c.get("cca_id") != cca_id and c.get("status") in _LIVE + ("rejected", "implemented")
                 and _is_economy_hold(c, vsb_id, title, source, counterparty)
                 and _order_ns(c) > _order_ns(mine)]
        if newer:
            # W463 (sixth refutation) — every live record for the action is newer than the spend that withdrew the rest,
            # so these were filed while it was in flight. An undecided (submitted) hold the returned approval CAN
            # release was asked only because the spend might have run; nothing ran, so it is withdrawn and the approval
            # comes back (skipping left the Owner's approval spent on nothing). W463 (seventh refutation): a hold the
            # approval cannot release (a larger transfer, other intake) is a different request — it stays live, as the
            # gate's own step 4 keeps a fresh hold over a stale approval. Anything under review, approved, rejected or
            # not releasable keeps the skip, and the spent record says in its own trail that its action never ran.
            # W463 (eighth refutation): a newer record already SPENT counts too — the Owner's later approval replaced this
            # one, and giving this one back beside it left two approvals for one action (or released a second action).
            def _releasable_by_mine(c: Dict[str, Any]) -> bool:
                # W464 — an approval that is not the Owner's releases nothing: it never displaces a newer hold
                b = _bound_est(c)
                return _owner_decided(mine) and b is not None and _fits(mine, b, c.get("intake")) is not None
            blocking = [c for c in newer if c.get("status") != "submitted" or not _releasable_by_mine(c)]
            if not blocking:
                for c in newer:
                    if _withdraw_if_submitted(cca, c, vsb_id, cca_id,
                                              "the approval spent for this action is given back — its action never ran"):
                        withdrawn.append(c)
                    else:
                        blocking.append(c)
                        break
            if blocking:
                _revert_withdrawals(cca, withdrawn, cca_id, vsb_id)
                _ueg_log({"type": "economy.materiality_approval_restore_skipped", "vsb_id": vsb_id, "cca_id": cca_id,
                          "skip_reason": "superseded_by_newer_record", "status_now": str(mine.get("status") or ""),
                          "newer_cca_id": blocking[0].get("cca_id"), "reason": reason[:200]})
                try:
                    def _note(fresh: dict) -> None:
                        fresh.setdefault("audit_trail", []).append(
                            {"event": "approval_spent_action_never_ran", "ts": _now(), "consume_id": consume_id,
                             "newer_cca_id": blocking[0].get("cca_id"), "by": "economy", "by_verified": False,
                             "reason": reason[:200]})
                    cca._update_change(cca_id, _note)
                except Exception:
                    pass
                return "superseded"
    def _restore(fresh: dict) -> None:
        if fresh.get("status") != "implemented":
            raise _Moved("status_moved", fresh.get("status"))
        spends = [e for e in (fresh.get("audit_trail") or [])
                  if e.get("event") in ("consumed_by_economy_cycle", "implemented", "approval_restored_action_never_ran")]
        last = spends[-1] if spends else {}
        if last.get("event") != "consumed_by_economy_cycle" or last.get("consume_id") != consume_id:
            raise _Moved("spent_by_another_action", fresh.get("status"))
        fresh["status"] = "approved"
        fresh.pop("implemented_at", None)
        fresh.setdefault("audit_trail", []).append(
            {"event": "approval_restored_action_never_ran", "ts": _now(), "consume_id": consume_id,
             "by": "economy", "by_verified": False, "reason": reason[:200]})
    try:
        cca._update_change(cca_id, _restore)
    except _Moved as moved:
        _revert_withdrawals(cca, withdrawn, cca_id, vsb_id)
        _ueg_log({"type": "economy.materiality_approval_restore_skipped", "vsb_id": vsb_id,
                  "cca_id": cca_id, "skip_reason": moved.args[0],
                  "status_now": str(moved.args[1] if len(moved.args) > 1 else ""), "reason": reason[:200]})
        return "moved"
    except Exception as err:
        # W459 (refuter) — the record was busy or unreadable: the approval stays consumed, so
        # say so durably (the docstring promises an AUDIBLE restore), never silently
        _revert_withdrawals(cca, withdrawn, cca_id, vsb_id)
        _ueg_log({"type": "economy.materiality_approval_restore_failed", "vsb_id": vsb_id,
                  "cca_id": cca_id,
                  "error": str(getattr(err, "detail", None) or err)[:200], "reason": reason[:200]})
        return "failed"
    _ueg_log({"type": "economy.materiality_approval_restored", "vsb_id": vsb_id,
              "cca_id": cca_id, "consume_id": consume_id, "reason": reason[:200]})
    return "restored"


def _spent_on_a_raised_cycle(consumed: Optional[Dict[str, Any]], vsb_id: str, source: str,
                             err: BaseException) -> None:
    """W463 — a cycle that RAISED after the approval was spent is not known to have posted nothing
    (run_cycle writes the ledger in steps), so the approval is NOT given back — a second release would
    be the worse error. It is said loudly instead, naming the record, so the Owner can re-approve
    knowingly."""
    if consumed:
        _ueg_log({"type": "economy.materiality_approval_spent_cycle_failed", "vsb_id": vsb_id,
                  "source": source, "cca_id": consumed.get("cca_id"), "consume_id": consumed.get("consume_id"),
                  "error": f"{type(err).__name__}: {str(err)[:160]}",
                  "note": "the action raised after the approval was spent; it stays spent (it may have "
                          "partly posted) — re-approve the action if it should run again"})


# ── W463: what an approval authorises ─────────────────────────────────────────────────────────────
# A material economy action is held until the Owner approves a Change Control record the ECONOMY filed
# for it. One approval releases the intake it was filed for — no more — and only for the same kind of
# action: a transfer to the same counterparty for at most the approved amount; an API cycle on at most
# the revenue it declared (and at most the pending returns/receipts the gate measured then); a heartbeat
# cycle on exactly the recognised revenue events it was filed for. Intake that arrives later waits for
# the next cycle instead of voiding the approval. There is at most ONE live record per (VSB, action
# kind, counterparty): an undecided hold is re-estimated as the intake grows (the Owner decides the
# current amount), and an approval that cannot release a new request is withdrawn — never left live to
# release some later, unrelated action. A rejection answers exactly the action it was filed for; a
# changed action is asked again.

_LIVE = ("submitted", "under_review", "approved")


def _order_ns(c: Dict[str, Any]) -> int:
    """W463 — when a record was filed, as one number: its filed_ns, or (a record filed before W463) its
    second-resolution submitted_at in ns. filed_ns is serialised per action by the gate lock and never decreases
    (a new record is filed after every record it can see, whatever the wall clock says), so a backward clock step
    cannot reorder two records — ordering on submitted_at first let it (fourth refutation)."""
    try:
        ns = int(c.get("filed_ns") or 0)
    except (TypeError, ValueError):
        ns = 0
    if ns > 0:
        return ns
    try:
        import calendar
        return calendar.timegm(time.strptime(str(c.get("submitted_at") or ""), "%Y-%m-%dT%H:%M:%SZ")) * 10**9
    except (TypeError, ValueError, OverflowError):
        return 0


def _order_key(c: Dict[str, Any]) -> Tuple[int, bool]:
    """W463 — the order records for one action were filed in. submitted_at has second resolution, and one second
    easily holds a rejection and the hold filed after it (the order then fell to the directory listing, and "has an
    approved action run since the rejection?" was answered by chance). An exact tie that remains (records filed
    before W463 in the same second) resolves to the rejection — the most restrictive reading."""
    return (_order_ns(c), c.get("status") == "rejected")


_SPEND_EVENTS = ("consumed_by_economy_cycle", "implemented", "approval_restored_action_never_ran")
_REJECTED_BY_WORDS = {"admin_override": "by an explicit decision",
                      "model_decision_marker": "by the reviewing model's decision marker",
                      "health_threshold_rule": "by the organism-health threshold rule"}


def _rejected_by(c: Dict[str, Any]) -> str:
    """W463 (fifth refutation) — what rejected a record. A rejection is not always the Owner's: before W464 a MEDIUM
    hold could be rejected by the reviewing model's marker or the organism-health rule, and the answer and the pages
    said "the Owner rejected" regardless. W464: every hold is CRITICAL now (only the Owner decides one), but those
    earlier rejections still stand — refusing an action is the restrictive side — and still say what made them."""
    from agentic_core.api.change_control import approval_source
    src = approval_source(c)                       # W464 — the same reading as the Change Control pages
    return src if src in _REJECTED_BY_WORDS else "change_control"


def _owner_decided(c: Dict[str, Any]) -> bool:
    """W464 (FU-014, the Owner's ruling of 2026-09-14) — a material economy action is released only by the Owner's
    explicit decision. An approval recorded any other way — by the reviewing model's marker or the organism-health rule
    (holds were MEDIUM before the ruling), or with no decision recorded at all — releases nothing: fail closed. One
    reading for the whole system: Change Control's approval_source (an override made before W459 recorded a source is
    still recognised by its "Manual override:" review text)."""
    from agentic_core.api.change_control import approval_source
    return approval_source(c) == "admin_override"


_NOT_OWNER_DECIDED = ("it was approved {by}, not by the Owner's explicit decision, and a material economy action is "
                      "released only by the Owner's decision")


def _not_owner_reason(c: Dict[str, Any]) -> str:
    from agentic_core.api.change_control import approval_source
    by = {"model_decision_marker": "by the reviewing model's decision marker",
          "health_threshold_rule": "by the organism-health threshold rule"}.get(
        str(approval_source(c) or ""), "with no explicit decision recorded")
    return _NOT_OWNER_DECIDED.format(by=by)


def _action_ran(c: Dict[str, Any]) -> bool:
    """W463 (fourth refutation) — whether an implemented record's approved action is known to have RUN. The gate
    marks an approval implemented when it SPENDS it, before the constitutional gate or the action runs; counting
    that spend as "an approved action ran since the rejection" let a request for exactly the rejected action,
    arriving from another worker while the spent action was still in flight (and then blocked), file a plain hold a
    model review could approve (before W464 made every hold CRITICAL; the link now keeps the Owner told that the
    hold follows a rejection). A spend counts once the action marked it started (see _mark_action_ran). A record
    implemented some other way, or spent before W463 (no consume handle), counts as it always did."""
    if c.get("status") != "implemented":
        return False
    trail = c.get("audit_trail") or []
    spends = [e for e in trail if e.get("event") in _SPEND_EVENTS]
    last = spends[-1] if spends else {}
    if last.get("event") != "consumed_by_economy_cycle" or not last.get("consume_id"):
        return True
    return any(e.get("event") == "released_action_ran" and e.get("consume_id") == last.get("consume_id")
               for e in trail)


def _mark_action_ran(consumed: Optional[Dict[str, Any]], vsb_id: str, how: str) -> None:
    """Record on the spent approval that the action it released has started (a cycle that started may have
    posted; a transfer whose debit posted, or cannot be ruled out). Never given back after this."""
    if not consumed:
        return
    cca_id, consume_id = consumed.get("cca_id"), consumed.get("consume_id")
    try:
        from agentic_core.api import change_control as cca

        def _mutate(fresh: dict) -> None:
            fresh.setdefault("audit_trail", []).append(
                {"event": "released_action_ran", "ts": _now(), "consume_id": consume_id, "by": "economy",
                 "by_verified": False, "how": how[:120]})
        cca._update_change(cca_id, _mutate)
    except Exception as err:
        # unrecorded, the spend reads as still in flight: an older rejection keeps standing (the restrictive side)
        _ueg_log({"type": "economy.materiality_action_ran_unrecorded", "vsb_id": vsb_id, "cca_id": cca_id,
                  "consume_id": consume_id, "error": str(getattr(err, "detail", None) or err)[:160]})


def unreleasable_reason(c: Dict[str, Any]) -> Optional[str]:
    """W463 (fourth/fifth refutation) — why the materiality gate can never release this economy record, or None when
    it can: the identity a live request would present must match it (the gate's own test — an empty VSB id is a VSB
    id), it must state an amount, and a transfer must name a receiver that is a registered living VSB (the transfer
    route refuses any other). An unreadable or empty roster is never read as "the receiver is gone"."""
    if not isinstance(c, dict) or c.get("change_type") != "economy_material":
        return "it is not an economy materiality hold"
    filer = str(c.get("submitted_by") or "")
    vsb_id = c.get("vsb_id")
    if not filer.startswith("economy:") or not isinstance(vsb_id, str) or _bound_est(c) is None:
        return "it was not filed by the economy's gate for a VSB and an amount"
    source = _source_class(filer.split(":", 1)[1])
    counterparty = c.get("counterparty")
    if source == "transfer" and not counterparty:
        return "a transfer hold filed before W463 names no receiver, so no transfer can match it"
    if not _is_economy_hold(c, vsb_id, _hold_title(vsb_id, source), source, counterparty):
        return "no economy action presents this record's identity"
    if c.get("status") == "approved" and not _owner_decided(c):
        # W464 (FU-014) — the gate never spends it (see _owner_decided), so it can be retired
        return _not_owner_reason(c)
    if source in ("transfer", "heartbeat"):
        try:
            from agentic_core.economy.living_vsbs import _STORE as _ROSTER, _load as _living
            roster = _living() if _ROSTER.exists() else None
        except Exception:
            roster = None
        if roster and source == "transfer" and counterparty not in roster:
            return f"its receiver {counterparty} is not a registered living VSB, so the transfer cannot run"
        if roster and source == "heartbeat" and vsb_id not in roster:
            # W463 (sixth refutation) — only the heartbeat runs a heartbeat cycle, and it tends only the living roster
            return f"{vsb_id} is no longer on the living roster, so no heartbeat cycle can run for it"
    return None


def releasable_by_gate(c: Dict[str, Any]) -> bool:
    return unreleasable_reason(c) is None


def _gate_lock(vsb_id: str, source: str, counterparty: Optional[str]):
    """The lock serialising every decision about one (VSB, action kind, counterparty)."""
    import hashlib
    from agentic_core.config import data_path, store_lock
    key = hashlib.sha1(f"{vsb_id}|{_source_class(source)}|{counterparty}".encode("utf-8")).hexdigest()
    lock_dir = data_path("economy_gate_locks")
    lock_dir.mkdir(parents=True, exist_ok=True)
    return store_lock(lock_dir / f"{key}.json")
_OPEN = ("submitted", "under_review")
# W464 (FU-014) — every material economy hold is CRITICAL: said on every held answer, not only a follows-rejection one
_OWNER_DECIDES = (" A review never decides a material economy action: only an explicit decision of the Owner does (the "
                  "Governance hub's Sovereign Sanctum).")
_EXPLICIT = " It follows a rejection of this action."
# keys only submit_change writes: a record carrying one was minted by a submitter, not by the economy
_SUBMIT_ONLY_KEYS = ("submitted_by_verified", "immune_threat_at_submit", "config_change")
_LEGACY_EST = re.compile(r"estimated distributable ([0-9]+(?:\.[0-9]+)?) WST")


def _source_class(source: str) -> str:
    source = str(source or "")
    return "transfer" if source == "transfer" else ("heartbeat" if source == "heartbeat" else "api")


def _is_economy_hold(c: Dict[str, Any], vsb_id: str, title: str, source: str,
                     counterparty: Optional[str] = None) -> bool:
    """W463 — a hold is identified by what FILED it, not by its title alone. The gate used to accept any
    record whose title matched: a LOW 'config_minor' change submitted through /cca/submit with the hold's
    title was auto-approved at submit and released a 4,000,000-WST distribution nobody reviewed. Only a
    record the economy itself filed — change_type economy_material, submitted_by economy:<same kind of
    action>, exactly this VSB, none of the keys submit_change writes — for this counterparty governs."""
    if c.get("title") != title or c.get("change_type") != "economy_material":
        return False
    if any(k in c for k in _SUBMIT_ONLY_KEYS) or c.get("vsb_id") != vsb_id:
        return False
    filer = str(c.get("submitted_by") or "")
    if not filer.startswith("economy:") or _source_class(filer.split(":", 1)[1]) != _source_class(source):
        return False
    # a transfer hold names its counterparty; a record filed before W463 carries none and is not honoured
    return c.get("counterparty") == counterparty


def _bound_est(c: Dict[str, Any]) -> Optional[float]:
    """The amount a record was filed for: its est_distributable_wst, or — for a record filed before W463 —
    the estimate its description states. None when neither exists (such a record releases nothing)."""
    v = c.get("est_distributable_wst")
    if v is None:
        m = _LEGACY_EST.search(str(c.get("description") or ""))
        v = m.group(1) if m else None
    try:
        return None if v is None else float(v)
    except (TypeError, ValueError):
        return None


def _release_estimate(filed: Dict[str, Any], intake: Dict[str, Any],
                      event_ids: Optional[List[str]] = None) -> Tuple[float, float, float]:
    """What a release would actually distribute: its revenue/costs (the released events, or the request's own),
    pending returns/receipts capped at what the approval was filed with, at the REQUEST's reserve rate."""
    returns = min(float(intake.get("returns_wst") or 0.0), float(filed.get("returns_wst") or 0.0))
    transfers = min(float(intake.get("transfers_wst") or 0.0), float(filed.get("transfers_wst") or 0.0))
    if event_ids is not None:
        items = intake.get("event_items") or {}
        revenue = sum(float((items.get(i) or {}).get("amount_wst") or 0.0) for i in event_ids
                      if (items.get(i) or {}).get("kind") == "revenue")
        costs = sum(float((items.get(i) or {}).get("amount_wst") or 0.0) for i in event_ids
                    if (items.get(i) or {}).get("kind") != "revenue")
    else:
        revenue, costs = float(intake.get("revenue_wst") or 0.0), float(intake.get("costs_wst") or 0.0)
    reserve = float(intake.get("reserve_rate", 0.20))
    return _estimate_distributable(revenue + returns + transfers, costs, reserve), round(returns, 2), round(transfers, 2)


def _fits(c: Dict[str, Any], est: float, intake: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """If approval `c` can release this request, return the release (what the action may take); else None.
    Every release is checked against the amount the approval was filed for — whatever changed since (a lower
    reserve rate, a cost event that is no longer pending, a larger declared revenue), it never distributes more."""
    bound = _bound_est(c)
    if bound is None:
        return None
    filed = c.get("intake")
    if isinstance(filed, dict) and intake is not None and "event_ids" in filed:
        # a heartbeat approval releases exactly the recognised events it was filed for that are still pending
        filed_ids = list(filed.get("event_ids") or [])
        pending = [i for i in (intake.get("event_ids") or []) if i in set(filed_ids)]
        if filed_ids and not pending:
            return None
        released, returns, transfers = _release_estimate(filed, intake, pending)
        if released > bound + 0.005:
            return None
        if not pending and returns <= 0.005 and transfers <= 0.005:
            # W463 (third refutation) — filed with no events (material only through pending returns/receipts) and
            # those are gone: spending it would mark the Owner's approval "implemented" on a cycle of nothing
            return None
        return {"event_ids": pending, "max_returns_wst": returns, "max_transfers_wst": transfers,
                "release_est_wst": released}
    if isinstance(filed, dict) and intake is not None and "revenue_wst" in filed:
        # an API cycle approval: at most the revenue it declared, costs at least as declared, drains capped
        if float(intake.get("revenue_wst") or 0.0) > float(filed.get("revenue_wst") or 0.0) + 0.005:
            return None
        if float(intake.get("costs_wst") or 0.0) + 0.005 < float(filed.get("costs_wst") or 0.0):
            return None
        released, returns, transfers = _release_estimate(filed, intake)
        if released > bound + 0.005:
            return None
        if float(intake.get("revenue_wst") or 0.0) <= 0.005 and returns <= 0.005 and transfers <= 0.005:
            # W463 (fourth refutation) — the receipts it was filed for are gone and the request declares no revenue:
            # spending it would mark the Owner's approval "implemented" on a cycle of nothing (as GATE-4 for the heartbeat)
            return None
        return {"max_returns_wst": returns, "max_transfers_wst": transfers, "release_est_wst": released}
    # a transfer, or a record filed before W463: the amount it was filed for bounds the action
    if est > bound + 0.005:
        return None
    return {}


def _same_action(c: Dict[str, Any], est: float, intake: Optional[Dict[str, Any]]) -> bool:
    """A rejection stands only against the action it was filed for."""
    bound = _bound_est(c)
    if bound is None or abs(bound - est) > 0.005:
        return False
    filed = c.get("intake")
    if isinstance(filed, dict) and intake is not None and "event_ids" in filed:
        return set(filed.get("event_ids") or []) == set(intake.get("event_ids") or [])
    if isinstance(filed, dict) and intake is not None and "revenue_wst" in filed:
        # W463 (third refutation) — an API cycle declaring different revenue/costs (or draining different pending
        # intake, or at another reserve rate) is a different action even at the same estimate: it is asked again
        if any(abs(float(filed.get(k) or 0.0) - float(intake.get(k) or 0.0)) > 0.005
               for k in ("revenue_wst", "costs_wst", "returns_wst", "transfers_wst")):
            return False
        return abs(float(filed.get("reserve_rate", 0.20)) - float(intake.get("reserve_rate", 0.20))) <= 1e-9
    return True


def _held(c: Dict[str, Any], est: float, note: str, status: str = "held_for_change_control", **extra) -> Dict[str, Any]:
    # W463 (third refutation) — a hold filed after a rejection says so (the pages show the link). W464: the tier is the
    # one the hold is decided under (CRITICAL), not the MEDIUM a hold filed before the ruling was stamped with
    from agentic_core.api.change_control import effective_tier
    follows = c.get("follows_rejection") if status == "held_for_change_control" else None
    return {"status": status, "cca_id": c.get("cca_id"), "impact_tier": effective_tier(c),
            "est_distributable_wst": est, "approved_or_filed_wst": _bound_est(c),
            "materiality_threshold_wst": MATERIALITY_WST, "note": note,
            **({"follows_rejection": follows.get("cca_id")} if isinstance(follows, dict) else {}), **extra}


def _describe(vsb_id: str, source: str, est: float, counterparty: Optional[str],
              follows: Optional[Dict[str, Any]] = None) -> str:
    what = (f"Material virtual transfer from {vsb_id} to {counterparty}" if source == "transfer"
            else f"Material virtual distribution for {vsb_id} ({_source_class(source)} cycle)")
    after = ""
    if follows:
        again = follows.get("event_ids")
        after = (f" FOLLOWS A REJECTION: {follows.get('cca_id')} (for {follows.get('est_distributable_wst')} WST) was "
                 "rejected" + (f"; {len(again)} of its recognised events are included again here" if again else "")
                 + ". Only an explicit decision can approve this.")
    return (f"{what}: estimated {est} WST ≥ materiality threshold {MATERIALITY_WST} WST. Held until approved "
            "(virtual WST only — no real funds). An approval releases ONE action on the intake recorded on this "
            "record" + (" to this counterparty" if counterparty else "") + " — at most this amount; intake that "
            "arrives later waits for the next cycle. While submitted, the amount is kept current." + after)


def _withdraw(cca, c: Dict[str, Any], vsb_id: str, replaced_by: Optional[str], reason: str) -> None:
    """Retire a live record that can no longer release anything (compare-and-set; left alone if it moved)."""
    def _mutate(fresh: dict) -> None:
        if fresh.get("status") not in _LIVE:
            raise _Moved(fresh.get("status"))
        fresh["status"] = "withdrawn"
        fresh.setdefault("audit_trail", []).append(
            {"event": "withdrawn_superseded", "ts": _now(), "by": "economy", "by_verified": False,
             "superseded_by": replaced_by, "reason": reason[:200]})
    try:
        cca._update_change(c["cca_id"], _mutate)
        _ueg_log({"type": "economy.materiality_hold_withdrawn", "vsb_id": vsb_id, "cca_id": c["cca_id"],
                  "superseded_by": replaced_by, "reason": reason[:200]})
    except _Moved:
        pass
    except Exception as err:
        _ueg_log({"type": "economy.materiality_gate_error", "vsb_id": vsb_id, "cca_id": c.get("cca_id"),
                  "error": f"withdraw failed: {str(getattr(err, 'detail', None) or err)[:160]}"})


def _revert_withdrawals(cca, withdrawn: List[Dict[str, Any]], replaced_by: Optional[str], vsb_id: str) -> None:
    """W463 (seventh refutation) — a give-back withdraws the holds it replaces before it writes the approval back; when
    that write does not land (the record busy, or moved), the holds it withdrew are put back to submitted — only while
    their last trail entry is still this give-back's withdrawal — so the action is never left with no live record."""
    for c in withdrawn:
        def _mutate(fresh: dict) -> None:
            trail = fresh.get("audit_trail") or []
            last = trail[-1] if trail else {}
            if (fresh.get("status") != "withdrawn" or last.get("event") != "withdrawn_superseded"
                    or last.get("superseded_by") != replaced_by):
                raise _Moved(fresh.get("status"))
            fresh["status"] = "submitted"
            trail.append({"event": "withdrawal_reverted", "ts": _now(), "by": "economy", "by_verified": False,
                          "reason": f"the approval {replaced_by} could not be given back, so this hold stays live"})
            fresh["audit_trail"] = trail
        try:
            cca._update_change(c["cca_id"], _mutate)
            _ueg_log({"type": "economy.materiality_hold_withdrawal_reverted", "vsb_id": vsb_id, "cca_id": c["cca_id"],
                      "approval_cca_id": replaced_by})
        except Exception as err:
            _ueg_log({"type": "economy.materiality_gate_error", "vsb_id": vsb_id, "cca_id": c.get("cca_id"),
                      "error": f"withdrawal revert failed: {str(getattr(err, 'detail', None) or err)[:160]}"})


def _withdraw_if_submitted(cca, c: Dict[str, Any], vsb_id: str, replaced_by: Optional[str], reason: str) -> bool:
    """Withdraw a record only while it is still SUBMITTED (compare-and-set). True when withdrawn."""
    def _mutate(fresh: dict) -> None:
        if fresh.get("status") != "submitted":
            raise _Moved(fresh.get("status"))
        fresh["status"] = "withdrawn"
        fresh.setdefault("audit_trail", []).append(
            {"event": "withdrawn_superseded", "ts": _now(), "by": "economy", "by_verified": False,
             "superseded_by": replaced_by, "reason": reason[:200]})
    try:
        cca._update_change(c["cca_id"], _mutate)
    except Exception:
        return False
    _ueg_log({"type": "economy.materiality_hold_withdrawn", "vsb_id": vsb_id, "cca_id": c["cca_id"],
              "superseded_by": replaced_by, "reason": reason[:200]})
    return True


def retire_heartbeat_holds_for_consumed_events(vsb_id: str) -> int:
    """W463 (refuter) — a heartbeat hold is filed for specific recognised events. When a later cycle consumes
    all of them (the estimate fell below the threshold, say), the hold can release nothing, but it used to sit
    in the Change Control queue stating an amount that was already distributed — and approving it wasted the
    Owner's decision. It is withdrawn instead (compare-and-set), saying why."""
    try:
        from agentic_core.api import change_control as cca
        from agentic_core.economy.revenue import _read_rows, peek_pending
        pending = set(peek_pending(vsb_id).get("ids") or [])
        # W467 (second refutation) — an event a cycle consumed but never settled (its cyc- token is still on it: the
        # cycle wrote nothing and its give-back failed, or the process stopped) is STUCK, not distributed; the
        # stranded-consume pass gives it back, so the hold filed for it is not retired as "consumed by a cycle"
        # W467 (third refutation) — …but only when that cycle did NOT post: a cycle that wrote its ledger (its intake
        # entry carries the token) and only failed to settle distributed them, and its hold is retired as before. An
        # unreadable ledger keeps them counted as stuck (the restrictive side).
        stuck: Dict[str, List[str]] = {}
        for ev in _read_rows():
            tok = str(ev.get("consume_token") or "")
            if ev.get("vsb_id") == vsb_id and ev.get("consumed") and tok.startswith("cyc-"):
                stuck.setdefault(tok, []).append(ev["id"])
        if stuck:
            from agentic_core.economy.transfers import _ledger_path, _read_ledger_strict
            path = _ledger_path(vsb_id)
            try:
                refs = {e.get("ref") for e in ((_read_ledger_strict(path).get("entries") or []) if path.exists() else [])
                        if isinstance(e, dict)}
            except Exception:
                refs = set()
            pending |= {i for tok, ids in stuck.items() if tok not in refs for i in ids}
        title = _hold_title(vsb_id, "heartbeat")
        retired = 0
        for c in (cca._load_change(x["cca_id"]) or {} for x in cca._list_changes()):
            if not c or c.get("status") not in _LIVE or not _is_economy_hold(c, vsb_id, title, "heartbeat"):
                continue
            filed = (c.get("intake") or {}).get("event_ids") if isinstance(c.get("intake"), dict) else None
            if filed and not (set(filed) & pending):
                _withdraw(cca, c, vsb_id, None, "every recognised event this hold was filed for was consumed by a cycle")
                retired += 1
        return retired
    except Exception:
        return 0


def _materiality_gate(vsb_id: str, est_distributable: float, source: str,
                      counterparty: Optional[str] = None,
                      intake: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """§3 'material actions route to Change Control'. Returns (held, consumed):
      held      — None → proceed; a dict → the action is HELD (or was rejected) and must NOT run;
      consumed  — None unless an approval was spent for this action, then {cca_id, consume_id, release, gate}:
                  `release` bounds what the action may take (see _fits); cca_id/consume_id plus `gate` =
                  {source, counterparty} are the exact handle _restore_consumed_approval needs if the action
                  does not run after all (the gate names the per-action lock the give-back takes and the action
                  whose newer records it checks).
    `intake` describes what the action would take: {revenue_wst, costs_wst, returns_wst, transfers_wst}
    plus reserve_rate for an API cycle; the same plus event_ids and event_items (the per-event amounts a release
    re-estimates from) for a heartbeat cycle; None for a transfer (its amount is the estimate)."""
    if est_distributable < MATERIALITY_WST:
        return None, None
    try:
        # W463 — the scan and the filing are not atomic: concurrent first requests for the same action each
        # filed a hold. The whole decision for one (VSB, action kind, counterparty) is serialised.
        with _gate_lock(vsb_id, source, counterparty):
            return _materiality_gate_locked(vsb_id, est_distributable, source, counterparty, intake)
    except Exception as e:
        # never silently skip the gate on a material amount — hold, loudly
        _ueg_log({"type": "economy.materiality_gate_error", "vsb_id": vsb_id, "error": str(e)[:200]})
        return ({"status": "held_for_change_control", "cca_id": None,
                 "note": f"Materiality gate errored ({str(e)[:120]}); the material action is held."}, None)


def _materiality_gate_locked(vsb_id: str, est_distributable: float, source: str, counterparty: Optional[str],
                             intake: Optional[Dict[str, Any]]) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    from agentic_core.api import change_control as cca
    # W442 — the action kind is part of the hold's identity (a cycle approval never releases a transfer)
    title = _hold_title(vsb_id, source)
    records = [c for c in (cca._load_change(x["cca_id"]) or {} for x in cca._list_changes())
               if c and _is_economy_hold(c, vsb_id, title, source, counterparty)]
    newest = lambda rows: sorted(rows, key=_order_key, reverse=True)       # see _order_key (same-second ties)
    live = [c for c in records if c.get("status") in _LIVE]

    # 1 — an approval that can release this request is spent (compare-and-set; never spent twice). W464 (FU-014): only
    # the Owner's explicit approval; any other approval is withdrawn below (steps 2 and 4) and the action asked again
    for c in newest([c for c in live if c.get("status") == "approved" and _owner_decided(c)]):
        release = _fits(c, est_distributable, intake)
        if release is None:
            continue
        consume_id = f"consume-{uuid.uuid4().hex[:12]}"

        def _consume(fresh: dict) -> None:
            if fresh.get("status") != "approved":
                raise _Moved(fresh.get("status"))
            fresh["status"] = "implemented"
            fresh["implemented_at"] = _now()
            fresh.setdefault("audit_trail", []).append(
                {"event": "consumed_by_economy_cycle", "ts": _now(), "source": source,
                 "by": f"economy:{source}", "by_verified": False, "consume_id": consume_id,
                 "est_distributable_wst": est_distributable, "release": release,
                 **({"counterparty": counterparty} if counterparty else {}),
                 **({"amount_from_description": True} if fresh.get("est_distributable_wst") is None else {})})
        try:
            cca._update_change(c["cca_id"], _consume)
        except _Moved as moved:
            # W464 (refutation) — flagged, so no page tells the Owner a decision is pending on a record that was just decided
            return _held(c, est_distributable, "The approval was consumed or changed concurrently (status now "
                         f"{moved}) — this action is held rather than spending it twice.", decided_concurrently=True), None
        for other in live:
            if other["cca_id"] != c["cca_id"]:
                _withdraw(cca, other, vsb_id, c["cca_id"], "another record for the same action was spent")
        _ueg_log({"type": "economy.materiality_approved_consumed", "vsb_id": vsb_id, "cca_id": c["cca_id"],
                  "consume_id": consume_id, "est_distributable_wst": est_distributable, "release": release,
                  **({"amount_from_description": True} if c.get("est_distributable_wst") is None else {})})
        return None, {"cca_id": c["cca_id"], "consume_id": consume_id, "release": release,
                      "gate": {"source": source, "counterparty": counterparty}}

    # 2 — an undecided hold for this action is kept current (never a sibling per new receipt)
    open_ = newest([c for c in live if c.get("status") in _OPEN])
    stale_approvals = [c for c in live if c.get("status") == "approved"]
    if open_:
        hold = open_[0]
        for other in open_[1:] + stale_approvals:
            _withdraw(cca, other, vsb_id, hold["cca_id"],
                      "superseded by the current hold for this action"
                      if other.get("status") != "approved" or _owner_decided(other) else _not_owner_reason(other))
        if hold.get("status") == "under_review":
            # W463 (refuter) — a hold under review is NOT re-estimated: the decider decides the amount they
            # were shown. Intake that arrived meanwhile waits for the next hold.
            return _held(hold, est_distributable,
                         f"Material action — the hold {hold['cca_id']} is under review for the amount it was filed "
                         "with; intake that arrived since waits for the next hold."
                         + (_EXPLICIT if hold.get("follows_rejection") else "") + _OWNER_DECIDES), None
        before = _bound_est(hold)

        def _rebound(fresh: dict) -> None:
            if fresh.get("status") != "submitted":
                raise _Moved(fresh.get("status"))
            cca._stamp_effective_tier(fresh)      # W464 — a hold filed as MEDIUM before the ruling reads CRITICAL
            if before is None or abs(float(before) - est_distributable) > 0.005 or fresh.get("intake") != intake:
                fresh["est_distributable_wst"] = est_distributable
                fresh["intake"] = intake
                fresh["description"] = _describe(vsb_id, source, est_distributable, counterparty,
                                                 fresh.get("follows_rejection"))
                fresh.setdefault("audit_trail", []).append(
                    {"event": "amount_rebound", "ts": _now(), "by": "economy", "by_verified": False,
                     "from_wst": before, "to_wst": est_distributable})
        try:
            hold = cca._update_change(hold["cca_id"], _rebound)
        except _Moved as moved:
            if str(moved) in _OPEN:
                # W464 (second refutation) — a review started meanwhile: nothing was decided, the Owner still decides it
                return _held(hold, est_distributable,
                             f"Material action — the hold {hold['cca_id']} is under review for the amount it was filed "
                             "with; intake that arrived since waits for the next hold."
                             + (_EXPLICIT if hold.get("follows_rejection") else "") + _OWNER_DECIDES), None
            return _held(hold, est_distributable, f"The hold was decided concurrently (status now {moved}) — "
                         "retry the action.", decided_concurrently=True), None
        return _held(hold, est_distributable,
                     f"Material action — awaiting the Owner's decision on Change Control hold {hold['cca_id']}; "
                     "the hold's amount is kept current until it is decided."
                     + (_EXPLICIT if hold.get("follows_rejection") else "") + _OWNER_DECIDES), None

    # 3 — a rejection answers exactly the action it was filed for, while no approved action has run since it.
    # W463 (third refutation): it used to be checked against the newest rejection alone, so once an approved action
    # ran afterwards the rejected amount stayed refused for ever and never reached the Owner again.
    # W463 (fifth refutation): the refusal stands only while the newest decided record — any spend included, run or
    # still in flight — is the rejection. The follows link (step 4) counts only spends whose action is KNOWN to have
    # run: a request for the rejected action during an unmarked spend (in flight, or a worker that died before
    # marking it) is asked again as a hold that says it follows the rejection — never refused for ever. (W464: every
    # hold is decided only by the Owner, so the link is information for the Owner, no longer the only protection.)
    decided_any = newest([c for c in records if c.get("status") in ("rejected", "implemented")])
    decided = newest([c for c in records if c.get("status") == "rejected" or _action_ran(c)])
    if (decided_any and decided_any[0].get("status") == "rejected"
            and _same_action(decided_any[0], est_distributable, intake)):
        r_ = decided_any[0]
        by = _rejected_by(r_)
        return _held(r_, est_distributable,
                     f"Change Control rejected exactly this action ({_REJECTED_BY_WORDS.get(by, 'decided by Change Control')}); "
                     "nothing runs. It is asked again, as a fresh hold, when the action changes (a different amount or "
                     "new intake).", status="rejected_by_change_control", rejected_by=by), None

    # 4 — file a hold through the real CCA machinery (same store the CCA UI reviews). W463 (refuter): a hold
    # filed after a rejection of this action says so — the Owner sees the earlier refusal. W464 (FU-014): every hold is
    # filed CRITICAL, so Change Control decides it only by the Owner's explicit decision (never the model or the rule).
    follows = None
    if decided and decided[0].get("status") == "rejected":           # no approved action has run since
        r0 = decided[0]
        follows = {"cca_id": r0.get("cca_id"), "est_distributable_wst": _bound_est(r0),
                   **({"event_ids": list((r0.get("intake") or {}).get("event_ids") or [])}
                      if isinstance(r0.get("intake"), dict) and "event_ids" in r0["intake"] else {})}
    now = _now()
    cca_id = f"cca-{uuid.uuid4().hex[:10]}"
    change = {
        "cca_id": cca_id, "title": title, "change_type": "economy_material",
        "est_distributable_wst": est_distributable, "intake": intake,
        **({"counterparty": counterparty} if counterparty else {}),
        **({"follows_rejection": follows} if follows else {}),
        "description": _describe(vsb_id, source, est_distributable, counterparty, follows),
        "rationale": "VSB_ECONOMIC_LEGAL_MODEL §3: material/large actions route to Change Control.",
        "affected_systems": ["economy", "capital"], "submitted_by": f"economy:{source}",
        "submitted_at": now,
        "filed_ns": max([time.time_ns()] + [_order_ns(c) + 1 for c in records]),
        "impact_tier": cca._determine_tier("economy_material", ""),
        "status": "submitted", "vsb_id": vsb_id, "rollback_plan": "No action taken while held.",
        "review_result": None, "decision": None, "reviewed_at": None, "implemented_at": None,
        "audit_trail": [{"event": "submitted", "ts": now, "by": f"economy:{source}", "by_verified": False}],
    }
    cca._save_change(change)
    for other in stale_approvals:
        _withdraw(cca, other, vsb_id, cca_id,
                  "the approval could not release this request; a fresh hold replaces it"
                  if _owner_decided(other) else _not_owner_reason(other) + "; a fresh hold replaces it")
    _ueg_log({"type": "economy.materiality_hold_filed", "vsb_id": vsb_id, "cca_id": cca_id,
              "est_distributable_wst": est_distributable, "threshold_wst": MATERIALITY_WST})
    return _held(change, est_distributable, f"Material action — Change Control hold {cca_id} was filed and the "
                 "action is held until the Owner approves it."
                 + (_EXPLICIT if follows else "") + _OWNER_DECIDES), None


async def governed_cycle(vsb_id: str, entity_type: str, owner: str, revenue: float,
                         costs: float = 0.0, reserve_rate: float = 0.20,
                         source: str = "api") -> Dict[str, Any]:
    """The governed metabolic cycle (async/API path): materiality → gaas.v5 gate → run → UEG split log."""
    from agentic_core.economy.metabolism import EconomicMetabolism
    metab = EconomicMetabolism(vsb_id, entity_type, owner)

    peek_returns, peek_transfers = _pending_parts(vsb_id)
    intake = {"revenue_wst": round(float(revenue), 2), "costs_wst": round(float(costs), 2),
              "returns_wst": peek_returns, "transfers_wst": peek_transfers, "reserve_rate": float(reserve_rate)}
    held, consumed = _materiality_gate(vsb_id, _estimate_distributable(
        revenue + peek_returns + peek_transfers, costs, reserve_rate), source, intake=intake)
    if held is not None:
        return {"cycle": None, "governance": held}
    release = (consumed or {}).get("release") or {}
    cap_returns = min(peek_returns, release.get("max_returns_wst", peek_returns))
    cap_transfers = min(peek_transfers, release.get("max_transfers_wst", peek_transfers))

    # W442 refuter catch: the except-fallback below used to call run_cycle AGAIN — if the
    # interceptor raised AFTER the action executed (its post-validation/checkpoint steps can),
    # one request posted the whole distribution twice. The action records its own execution so
    # no fallback path can ever re-run it — W463: nor re-run an action that STARTED and raised
    # (it may have posted part of the intake; running it again posted it twice, "ungated").
    executed = {"started": False, "done": False, "report": None}
    # W467 (refutation) — the released action counts as run only once the cycle has WRITTEN its ledger (the first
    # write is one atomic save); a cycle that raised before it hands the approval back, as the heartbeat path does
    progress: Dict[str, Any] = {"on_ledger_written": lambda: _mark_action_ran(consumed, vsb_id, f"{source} cycle wrote its ledger")}

    def _run():
        # W463 — consume at most what the gate measured (and what an approval was filed for)
        return metab.run_cycle(revenue, costs, reserve_rate,
                               max_returns_wst=cap_returns, max_transfers_wst=cap_transfers, progress=progress)

    def _raised(err: BaseException) -> None:
        if progress.get("ledger_written"):
            _spent_on_a_raised_cycle(consumed, vsb_id, source, err)
        else:
            _restore_consumed_approval(consumed, vsb_id=vsb_id,
                                       reason="the cycle raised before its first ledger write — nothing was posted")

    async def _action():
        executed["started"] = True
        executed["report"] = _run()
        executed["done"] = True
        return executed["report"]

    def _never_ran(why: str) -> None:
        # the materiality gate may have spent the Owner's approval for THIS cycle; if nothing ran,
        # give back exactly that consumption (never on a cycle that started)
        if not executed["started"]:
            _restore_consumed_approval(consumed, vsb_id=vsb_id, reason=why)

    try:
        from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
        gov = UnifiedConstitutionalInterceptorV16Omega("economy-node", UEGLogger())
        result = await gov.intercept({"intent": "economy_distribution", "vsb_id": vsb_id,
                                      "revenue_wst": revenue, "source": source}, _action)
        # W442 — a BLOCKED/HALTED verdict used to fall into the missing-output fallback and run
        # the cycle anyway: the response said "blocked" while the money moved. The sibling
        # /transfer handled the same verdict correctly ("never fabricate a transfer") — now the
        # cycle does too: blocked means NOTHING ran, NOTHING posted.
        if str(getattr(result, "status", "")).lower() in ("blocked", "halted"):
            _ueg_log({"type": "economy.cycle_blocked", "vsb_id": vsb_id, "source": source,
                      "gate": "gaas.v5", "status": result.status})
            _never_ran(f"gaas gate {result.status} — nothing ran")
            return {"cycle": None,
                    "governance": {"status": result.status, "checkpoint": result.checkpoint_id,
                                   "note": "the constitutional gate blocked this distribution — "
                                           "nothing ran, nothing was posted"}}
        if not getattr(result, "output", None) and not executed["done"]:
            executed["started"] = True
        report = (result.output if getattr(result, "output", None)
                  else (executed["report"] if executed["done"] else _run()))
        governance: Dict[str, Any] = {"status": result.status, "checkpoint": result.checkpoint_id}
    except Exception as e:
        if executed["started"] and not executed["done"]:
            # the gate ran and allowed the action, which then raised: never re-run it
            _raised(e)
            raise
        # §3 demands the gate; if the gate itself fails we do NOT hide it — run the (virtual) cycle
        # but emit a LOUD tamper-evident bypass event and say so in the response. NEVER a re-run:
        # if the action already executed inside the failed intercept, its report is reused.
        try:
            if not executed["done"]:
                executed["started"] = True
            report = executed["report"] if executed["done"] else _run()
        except BaseException as err:
            _raised(err)
            raise
        _ueg_log({"type": "economy.governance_bypass", "vsb_id": vsb_id, "source": source,
                  "error": str(e)[:200], "note": "gaas.v5 gate unavailable — cycle ran ungated (logged loudly)."})
        governance = {"status": "ungated_bypass_logged", "error": str(e)[:160]}

    _log_split(report, metab.waterfall_source, source)
    return {"cycle": report, "governance": governance}


def governed_cycle_sync(vsb_id: str, entity_type: str, owner: str, revenue: float,
                        costs: float = 0.0, reserve_rate: float = 0.20,
                        source: str = "heartbeat",
                        events: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """The governed cycle for SYNC callers (the heartbeat's autonomous ticks). Uses the genuine
    constitutional policy PRE-gate synchronously (the async interceptor cannot be awaited here);
    materiality + UEG split logging are identical to the async path.

    W463 — `events` is the revenue store's peek (ids + per-event amounts). When given, the cycle's
    revenue/costs are those events, a hold is filed for exactly those event ids, and an approval releases
    exactly the events it was filed for (later events wait). The result names `consumed_event_ids`: the
    caller consumes those, never the whole peek."""
    from agentic_core.economy.metabolism import EconomicMetabolism
    metab = EconomicMetabolism(vsb_id, entity_type, owner)

    # W463 — the side-effect-free policy pre-gate runs FIRST. It used to run after the materiality
    # gate had already spent the Owner's approval, and a refusal never gave it back: the approval was
    # burned with nothing distributed. Refusing before anything is consumed leaves nothing to restore
    # (restoring instead would consume-and-restore on every heartbeat beat while a refusal persists).
    governance: Dict[str, Any]
    try:
        from agentic_core.gaas.v5.policy_gate import ConstitutionalPolicyGate
        pre = ConstitutionalPolicyGate("economy").validate(
            "economy_distribution", {"intent": "economy_distribution", "vsb_id": vsb_id,
                                     "revenue_wst": revenue, "source": source})
        if isinstance(pre, dict) and pre.get("allowed") is False:
            _ueg_log({"type": "economy.cycle_blocked", "vsb_id": vsb_id, "source": source,
                      "gate": "policy_pre_gate(sync)", "reason": str(pre.get("reason"))[:200]})
            return {"cycle": None, "governance": {"status": "blocked_by_gate",
                                                  "gate": "policy_pre_gate(sync)",
                                                  "reason": pre.get("reason")}}
        governance = {"status": "passed", "gate": "policy_pre_gate(sync)"}
    except Exception as e:
        _ueg_log({"type": "economy.governance_bypass", "vsb_id": vsb_id, "source": source,
                  "error": str(e)[:200], "note": "sync policy gate unavailable — cycle ran ungated (logged loudly)."})
        governance = {"status": "ungated_bypass_logged", "error": str(e)[:160]}

    items = (events or {}).get("items") or {}
    event_ids = list((events or {}).get("ids") or [])
    if events is not None:
        revenue = sum(float(items.get(i, {}).get("amount_wst") or 0.0) for i in event_ids
                      if items.get(i, {}).get("kind") == "revenue")
        costs = sum(float(items.get(i, {}).get("amount_wst") or 0.0) for i in event_ids
                    if items.get(i, {}).get("kind") != "revenue")
    peek_returns, peek_transfers = _pending_parts(vsb_id)
    intake: Dict[str, Any] = {"revenue_wst": round(float(revenue), 2), "costs_wst": round(float(costs), 2),
                              "returns_wst": peek_returns, "transfers_wst": peek_transfers,
                              "reserve_rate": float(reserve_rate)}
    if events is not None:
        intake["event_ids"] = event_ids
        intake["event_items"] = {i: items.get(i) for i in event_ids}
    gate_est = _estimate_distributable(revenue + peek_returns + peek_transfers, costs, reserve_rate)
    held, consumed = _materiality_gate(vsb_id, gate_est, source, intake=intake)
    if held is not None:
        return {"cycle": None, "governance": held}

    release = (consumed or {}).get("release") or {}
    consumed_event_ids = event_ids
    if "event_ids" in release:
        consumed_event_ids = list(release["event_ids"])
        revenue = sum(float(items.get(i, {}).get("amount_wst") or 0.0) for i in consumed_event_ids
                      if items.get(i, {}).get("kind") == "revenue")
        costs = sum(float(items.get(i, {}).get("amount_wst") or 0.0) for i in consumed_event_ids
                    if items.get(i, {}).get("kind") != "revenue")
    cap_returns = min(peek_returns, release.get("max_returns_wst", peek_returns))
    cap_transfers = min(peek_transfers, release.get("max_transfers_wst", peek_transfers))
    if events is None:
        plain: Dict[str, Any] = {"on_ledger_written": lambda: _mark_action_ran(consumed, vsb_id, f"{source} cycle wrote its ledger")}
        try:
            report = metab.run_cycle(revenue, costs, reserve_rate, max_returns_wst=cap_returns,
                                     max_transfers_wst=cap_transfers, progress=plain)
        except BaseException as err:
            if plain.get("ledger_written"):
                _spent_on_a_raised_cycle(consumed, vsb_id, source, err)
            else:
                _restore_consumed_approval(consumed, vsb_id=vsb_id,
                                           reason="the cycle raised before its first ledger write — nothing was posted")
            raise
        _log_split(report, metab.waterfall_source, source)
        return {"cycle": report, "governance": governance, "consumed_event_ids": consumed_event_ids}

    # W467 (register FU-022) — the recognised events are CONSUMED BEFORE the cycle runs, under a token, after every gate
    # has passed. They used to be consumed by the caller AFTER run_cycle had posted, so a consume that failed (its lock
    # busy past the timeout) left them pending and the next beat distributed them a second time. Now: a consume that
    # fails runs nothing; a cycle that raises before its first ledger write gives back exactly its own events (and the
    # Owner's approval); a cycle that wrote anything keeps them consumed and the approval spent (it may have partly
    # posted — the W463 rule).
    from agentic_core.economy.revenue import consume_events, settle_consume_token, unconsume_events
    token = f"cyc-{uuid.uuid4().hex[:12]}"

    def _give_back_events(ids: List[str]) -> Optional[bool]:
        # exactly this cycle's events go back; a partial or failed give-back is recorded, naming what is missing
        try:
            back = set(unconsume_events(vsb_id, token).get("ids") or [])
        except Exception as uerr:
            back, why_back = set(), f"{type(uerr).__name__}: {str(uerr)[:160]}"
        else:
            why_back = "some of this cycle's events were no longer in the store"
        missing = [i for i in ids if i not in back]
        if missing:
            _ueg_log({"type": "economy.cycle_events_unconsume_failed", "vsb_id": vsb_id, "source": source,
                      "event_ids": missing, "token": token, "error": why_back,
                      "note": "the cycle wrote nothing, but these consumed events could not be put back now. They "
                              "keep this cycle's token, so they are never distributed twice; with autonomous economy on "
                              "the stranded-consume pass puts them back after 15 minutes "
                              "(economy.cycle_intake_reconciled), otherwise they must be put back to pending by hand. "
                              "Do not re-record them."})
        return not missing
    try:
        took = consume_events(vsb_id, consumed_event_ids, token=token)
    except Exception as err:
        why = f"{type(err).__name__}: {str(err)[:160]}"
        _restore_consumed_approval(consumed, vsb_id=vsb_id,
                                   reason="the cycle's recognised events could not be consumed — nothing ran")
        _ueg_log({"type": "economy.cycle_intake_unavailable", "vsb_id": vsb_id, "source": source, "error": why,
                  "event_ids": consumed_event_ids,
                  "note": "the events stay pending and nothing was distributed; the next cycle takes them"})
        return {"cycle": None, "governance": {"status": "intake_unavailable", "error": why,
                                              "note": "the recognised revenue events could not be consumed, so no "
                                                      "cycle ran; they stay pending for the next one"}}
    flipped = list(took.get("ids") or [])
    if set(flipped) != set(consumed_event_ids):
        # another consumer took some of them first: this cycle would run on exactly what IT consumed
        consumed_event_ids = flipped
        revenue = sum(float(items.get(i, {}).get("amount_wst") or 0.0) for i in flipped
                      if items.get(i, {}).get("kind") == "revenue")
        costs = sum(float(items.get(i, {}).get("amount_wst") or 0.0) for i in flipped
                    if items.get(i, {}).get("kind") != "revenue")
        # W467 (refutation) — re-sized, it is gated again: losing COST events to the other consumer can raise the
        # distributable above what the gate measured (above the threshold, or above what an approval released)
        new_est = _estimate_distributable(revenue + cap_returns + cap_transfers, costs, reserve_rate)
        if consumed:
            bound = release.get("release_est_wst")
            over = new_est > float(bound if bound is not None else gate_est) + 0.005
        else:
            over = new_est >= MATERIALITY_WST
        if over or (consumed and not flipped and cap_returns <= 0 and cap_transfers <= 0):
            events_back = _give_back_events(flipped) if flipped else True
            returned = _restore_consumed_approval(
                consumed, vsb_id=vsb_id, reason="another cycle consumed events this one was gated on — nothing ran")
            said = ("" if not consumed else
                    " and the approval was handed back" if returned == "restored" else
                    " and the approval could not be handed back (it stays spent)")
            _ueg_log({"type": "economy.cycle_intake_consumed_elsewhere", "vsb_id": vsb_id, "source": source,
                      "event_ids": flipped, "events_given_back": events_back, "approval_returned": returned,
                      "estimate_after_wst": new_est})
            return {"cycle": None, "governance": {"status": "intake_consumed_elsewhere", "approval_returned": returned,
                                                  "note": "another cycle consumed some of the recognised events first; "
                                                          "nothing ran" + said}}
    _ueg_log({"type": "economy.cycle_intake_consumed", "vsb_id": vsb_id, "source": source, "token": token,
              "event_ids": flipped, "revenue_wst": revenue, "costs_wst": costs,
              "cca_id": (consumed or {}).get("cca_id"), "consume_id": (consumed or {}).get("consume_id"),
              "note": "consumed before the cycle runs; the cycle's first ledger entry carries this token"})
    progress: Dict[str, Any] = {"cycle_token": token,
                                "on_ledger_written": lambda: _mark_action_ran(consumed, vsb_id, f"{source} cycle wrote its ledger")}
    try:
        report = metab.run_cycle(revenue, costs, reserve_rate, max_returns_wst=cap_returns,
                                 max_transfers_wst=cap_transfers, progress=progress)
    except BaseException as err:
        why = f"{type(err).__name__}: {str(err)[:160]}"
        written = bool(progress.get("ledger_written"))
        events_back: Optional[bool] = None
        returned = None
        if not written:
            events_back = _give_back_events(flipped) if flipped else True
            returned = _restore_consumed_approval(consumed, vsb_id=vsb_id,
                                                  reason="the cycle raised before its first ledger write — nothing was posted")
        else:
            _spent_on_a_raised_cycle(consumed, vsb_id, source, err)
            try:
                settle_consume_token(vsb_id, token)
            except Exception:
                pass
        intake_back = progress.get("intake_given_back") or {}
        if written:
            note = "the cycle wrote part of its ledger: its events stay consumed and are never distributed again"
        else:
            lost = ([] if events_back else ["some of its events"]) + [k.replace("_", " ") for k, ok in intake_back.items() if not ok]
            note = ("the cycle wrote nothing: its events and the intake it drained were given back" if not lost else
                    "the cycle wrote nothing, but " + " and ".join(lost) + " could not be given back (see the "
                    "give-back records)")
        _ueg_log({"type": "economy.cycle_raised", "vsb_id": vsb_id, "source": source, "error": why,
                  "ledger_written": written, "event_ids": flipped, "events_given_back": events_back,
                  "intake_given_back": intake_back, "approval_returned": returned,
                  "returns_drained_wst": progress.get("returns_drained_wst"),
                  "receipts_drained_wst": progress.get("receipts_drained_wst"), "note": note})
        raise
    try:
        settle_consume_token(vsb_id, token)
    except Exception:
        pass                       # the token only keeps these events past the cap a while longer
    _log_split(report, metab.waterfall_source, source)
    return {"cycle": report, "governance": governance, "consumed_event_ids": consumed_event_ids, "consumed": took}
