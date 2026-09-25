"""
Virtual double-entry ledger (per VSB) — denominated in WST (internal unit).

VIRTUAL/SIMULATED by design: these are internal accounting entries only. No real
money moves. The ledger backs the economic metabolism's statements and audit.
"""
from __future__ import annotations

import json
import math
import time
from contextlib import contextmanager
from pathlib import Path
from agentic_core.config import atomic_write_json, data_path, store_lock
from typing import Any, Dict, List, Optional

_STORE = data_path("economy")


class LedgerUnavailable(RuntimeError):
    """W468 (register FU-041) — a VSB's ledger file exists but cannot be read whole (not UTF-8, not JSON, not a ledger's
    shape, or unreadable on disk). Nothing is written to it: the tolerant loader it replaces read such a file as EMPTY
    books, and the next posting saved those empty books over the real ones. (Deliberately not a ValueError: the transfer
    route reads ValueError as a refused funds check.)"""


class LedgerWriteRefused(RuntimeError):
    """W468 (refutation) — a write would save books in a shape the strict read refuses (e.g. a posting that overflows a
    balance to Infinity): nothing is saved. The writer keeps the reader's shape, so the ledger's own writes can never
    freeze it."""


def _read_ledger_file(path: Path) -> bytes:
    """The ledger's bytes. A Windows reader can meet PermissionError while another process replaces the file
    (os.replace), so a few retries come first."""
    for attempt in range(5):
        try:
            return path.read_bytes()
        except (PermissionError, FileNotFoundError):
            if attempt == 4:
                raise
            time.sleep(0.05)
    raise PermissionError(str(path))


def _new_books(vsb_id: str) -> Dict[str, Any]:
    return {"vsb_id": vsb_id, "currency": "WST", "entries": [],
            "balances": {a: 0.0 for a in ACCOUNTS},
            "postings": [], "accounts": {}, "closes": []}


def _number_ok(v: Any) -> bool:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return False
    try:
        return math.isfinite(v)
    except OverflowError:          # an integer too large for a float is no amount any writer produces
        return False


def _shape_problem(data: Any) -> Optional[str]:
    """What makes a parsed file not a ledger this code can post to, or None. A key that is present must be
    well-formed; a missing key takes its default (ledgers written before a key existed stay readable)."""
    if not isinstance(data, dict):
        return f"not a ledger object ({type(data).__name__})"
    entries = data.get("entries", [])
    if not (isinstance(entries, list) and all(isinstance(e, dict) for e in entries)):
        return "'entries' is not a list of entries"
    for key in ("balances", "accounts"):
        book = data.get(key, {})
        if not isinstance(book, dict):
            return f"'{key}' is not an account map"
        bad = [k for k, v in book.items() if not _number_ok(v)]
        if bad:
            return f"'{key}' holds a non-finite or non-numeric balance ({str(bad[0])[:40]})"
    postings = data.get("postings", [])
    if not isinstance(postings, list):
        return "'postings' is not a list"
    for i, p in enumerate(postings):
        if not (isinstance(p, dict) and isinstance(p.get("debit"), str) and isinstance(p.get("credit"), str)
                and _number_ok(p.get("amount"))):
            return f"posting {i} is not a balanced posting (debit, credit, finite amount)"
    # W468 (refutation) — a key is defaulted only where some writer could have left it out: postings and accounts have
    # always been written together (W256), entries with balances, and a period close's postings with its close marker.
    # Defaulting them instead read books whose map was lost as EMPTY double-entry books.
    if postings and "accounts" not in data:
        return "postings without the 'accounts' they were posted to"
    if entries and "balances" not in data:
        return "entries without the 'balances' they were recorded to"
    if "closes" not in data and any(str(p.get("memo") or "").startswith("period close") for p in postings):
        return "period-close postings without the 'closes' that mark them"
    closes = data.get("closes", [])
    if not isinstance(closes, list):
        return "'closes' is not a list"
    for i, c in enumerate(closes):
        idx = c.get("posting_index") if isinstance(c, dict) else None
        if not (isinstance(idx, int) and not isinstance(idx, bool) and 0 <= idx <= len(postings)):
            return f"close {i} does not name a posting index within the postings"
    return None


def read_strict(path: Path, vsb_id: str) -> Dict[str, Any]:
    """W468 (register FU-041) — THE ledger read. A file that does not exist is new, empty books; a file that exists is
    read whole or refused (LedgerUnavailable) — never answered with empty books or a valid prefix."""
    path = Path(path)
    try:
        if not path.exists():
            return _new_books(vsb_id)
        raw = _read_ledger_file(path)
    except FileNotFoundError as err:
        # gone for every retry: new books only when it is really gone (a file seen during a replace is not "no ledger")
        try:
            gone = not path.exists()
        except OSError:
            gone = False
        if gone:
            return _new_books(vsb_id)
        raise LedgerUnavailable(f"{vsb_id}'s ledger could not be read ({type(err).__name__})") from err
    except OSError as err:
        raise LedgerUnavailable(f"{vsb_id}'s ledger could not be read ({type(err).__name__})") from err
    try:
        data = json.loads(raw.decode("utf-8"))
        problem = _shape_problem(data)
    except Exception as err:
        # W468 (refutation) — not UTF-8, not JSON, nested too deep to parse (RecursionError) or a number no float holds:
        # every way a file cannot be read whole is the same refusal (these used to escape and make construction raise)
        raise LedgerUnavailable(f"{vsb_id}'s ledger could not be read whole ({type(err).__name__}: "
                                f"{str(err)[:80]})") from err
    if problem:
        raise LedgerUnavailable(f"{vsb_id}'s ledger could not be read whole: {problem}")
    fresh = _new_books(vsb_id)
    for key in ("vsb_id", "currency", "entries", "balances", "postings", "accounts", "closes"):
        data.setdefault(key, fresh[key])
    return data


def repair(path: Path, vsb_id: str) -> Dict[str, Any]:
    """W472 (register FU-056) — the way back for a ledger the strict read refuses. The bytes are QUARANTINED first
    (a copy beside the ledger, never deleted), then what can be recovered without inventing a figure is recovered: a
    byte-order mark stripped; the valid JSON prefix when the tail is garbage or a truncation; postings whose amount
    no float holds dropped and COUNTED. A balance that is non-finite is not reset — that needs a hand audit, and the
    repair refuses. The recovered books must pass the strict read before they are written, and what was lost is
    said in the answer and on the constitutional ledger."""
    import codecs
    import shutil
    from agentic_core.config import atomic_write_json, store_lock
    path = Path(path)
    with store_lock(path):
        try:
            read_strict(path, vsb_id)
            return {"vsb_id": vsb_id, "repaired": False, "reason": "the ledger reads whole — nothing to repair"}
        except LedgerUnavailable as err:
            problem = str(err)
        if not path.exists():
            return {"vsb_id": vsb_id, "repaired": False, "reason": "no ledger file"}
        raw = _read_ledger_file(path)
        ts = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime())
        quarantine = path.with_name(f"{path.stem}.quarantine-{ts}.json")
        shutil.copyfile(path, quarantine)
        lost: List[str] = []
        text = raw
        if text.startswith(codecs.BOM_UTF8):
            text = text[len(codecs.BOM_UTF8):]
            lost.append("a byte-order mark (removed)")
        try:
            s = text.decode("utf-8")
        except UnicodeDecodeError as e:
            raise LedgerUnavailable(f"{vsb_id}'s ledger is not UTF-8 (byte {e.start}); quarantined as "
                                    f"{quarantine.name}, nothing recovered") from e
        try:
            data = json.loads(s)
        except ValueError:
            try:
                data, end = json.JSONDecoder().raw_decode(s.lstrip())
                tail = len(s.lstrip()) - end
                lost.append(f"{tail} trailing byte(s) after the valid JSON (a truncation or garbage)")
            except ValueError as e:
                raise LedgerUnavailable(f"{vsb_id}'s ledger holds no valid JSON prefix; quarantined as "
                                        f"{quarantine.name}, nothing recovered") from e
        if not isinstance(data, dict):
            raise LedgerUnavailable(f"{vsb_id}'s ledger is not a ledger object ({type(data).__name__}); "
                                    f"quarantined as {quarantine.name}, nothing recovered")
        # (refutation) the three W468 'written together' rules are refused BEFORE any key is defaulted: defaulting
        # 'accounts' or 'balances' here wrote exactly the empty books the strict read exists to refuse
        postings = data.get("postings")
        entries = data.get("entries")
        if isinstance(postings, list) and postings and "accounts" not in data:
            raise LedgerUnavailable(f"{vsb_id}'s ledger holds postings without the accounts they were posted to — a hand "
                                    f"audit is needed; quarantined as {quarantine.name}, nothing written")
        if isinstance(entries, list) and entries and "balances" not in data:
            raise LedgerUnavailable(f"{vsb_id}'s ledger holds entries without the balances they were recorded to — a hand "
                                    f"audit is needed; quarantined as {quarantine.name}, nothing written")
        if isinstance(postings, list) and "closes" not in data and any(
                isinstance(p, dict) and str(p.get("memo") or "").startswith("period close") for p in postings):
            raise LedgerUnavailable(f"{vsb_id}'s ledger holds period-close postings without the closes that mark them — a "
                                    f"hand audit is needed; quarantined as {quarantine.name}, nothing written")
        if isinstance(postings, list):
            # a posting whose amount is finite is never dropped: its figure is already in the accounts (a malformed
            # debit/credit on a finite amount needs a hand audit); only an amount no float holds is dropped
            malformed = [i for i, p in enumerate(postings)
                         if not (isinstance(p, dict) and isinstance(p.get("debit"), str) and isinstance(p.get("credit"), str))
                         and _number_ok((p or {}).get("amount") if isinstance(p, dict) else None)]
            if malformed:
                raise LedgerUnavailable(f"{vsb_id}'s posting {malformed[0]} is malformed but its amount is finite and "
                                        f"already in the accounts — a hand audit is needed; quarantined as "
                                        f"{quarantine.name}, nothing written")
            drop = [i for i, p in enumerate(postings) if not (isinstance(p, dict) and _number_ok(p.get("amount")))]
            if drop:
                keep = [p for i, p in enumerate(postings) if i not in set(drop)]
                lost.append(f"{len(drop)} posting(s) whose amount no float holds (dropped; the accounts were not "
                            "adjusted — a non-finite amount was never applied to them)")
                data["postings"] = keep
                closes = data.get("closes")
                if isinstance(closes, list):
                    # a period boundary names a posting index: every boundary after a dropped posting moves back by
                    # the number dropped before it, so no posting silently changes period; a boundary ON a dropped
                    # posting is refused
                    reindexed = []
                    for c in closes:
                        idx = c.get("posting_index") if isinstance(c, dict) else None
                        if not isinstance(idx, int):
                            continue
                        if idx in drop:
                            raise LedgerUnavailable(f"{vsb_id}'s period close marks a posting whose amount no float holds "
                                                    f"— a hand audit is needed; quarantined as {quarantine.name}, nothing "
                                                    "written")
                        shift = sum(1 for d in drop if d < idx)
                        reindexed.append(dict(c, posting_index=idx - shift))
                    if reindexed != closes:
                        lost.append(f"{len(reindexed)} period close boundary(ies) re-indexed after the dropped posting(s)")
                        data["closes"] = reindexed
        for key in ("balances", "accounts"):
            book = data.get(key, {})
            if isinstance(book, dict) and any(not _number_ok(v) for v in book.values()):
                raise LedgerUnavailable(f"{vsb_id}'s '{key}' holds a balance no float holds — a hand audit is needed; "
                                        f"quarantined as {quarantine.name}, nothing written")
        fresh = _new_books(vsb_id)
        for key in ("vsb_id", "currency", "entries", "balances", "postings", "accounts", "closes"):
            data.setdefault(key, fresh[key])
        still = _shape_problem(data)
        if still:
            raise LedgerUnavailable(f"{vsb_id}'s ledger is still not a ledger after recovery ({still}); quarantined as "
                                    f"{quarantine.name}, nothing written")
        atomic_write_json(path, data)
        read_strict(path, vsb_id)                     # what was written reads whole — or the raise says it did not
    record = {"vsb_id": vsb_id, "repaired": True, "problem": problem, "quarantine": quarantine.name, "lost": lost,
              "postings": len(data.get("postings") or []), "entries": len(data.get("entries") or []),
              "note": "recovered without inventing a figure; the original bytes are kept in the quarantine copy"}
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "economy.ledger_repaired", **record})
        record["ueg_logged"] = True
    except Exception:
        record["ueg_logged"] = False
    return record


# Chart of accounts (simplified, biomimetic-aware).
ACCOUNTS = ["revenue", "reserves", "owner", "self_investment",
            "capital_fund", "user_projects", "charity"]

# ── Double-entry chart (VSB_ECONOMIC_LEGAL_MODEL §3/§9.1) ─────────────────────
# account → type; asset/expense are DEBIT-normal, income/equity/liability are CREDIT-normal.
CHART: Dict[str, str] = {
    "cash":                          "asset",
    "reserve_fund":                  "asset",
    "revenue":                       "income",
    "distribution_owner":            "expense",
    "distribution_self_investment":  "expense",
    "distribution_capital_fund":     "expense",
    "distribution_user_projects":    "expense",
    "distribution_charity":          "expense",
    "transfer_out":                  "expense",   # inter-VSB transfers (federation seed, W262)
    "operating_costs":               "expense",   # W475 (ledger v4 R6.1) — a cycle's declared costs
    "retained_earnings":             "equity",
}
_DEBIT_NORMAL = ("asset", "expense")

# Legacy single-sided record(account, …) → the balanced posting it really means.
_COMPAT_POSTING: Dict[str, tuple] = {
    "revenue":         ("cash", "revenue"),                        # intake: Dr Cash / Cr Revenue
    "reserves":        ("reserve_fund", "cash"),                   # homeostasis: Dr Reserve Fund / Cr Cash
    "costs":           ("operating_costs", "cash"),                # W475: declared costs: Dr Operating Costs / Cr Cash
    "owner":           ("distribution_owner", "cash"),             # circulation: Dr Distribution / Cr Cash
    "self_investment": ("distribution_self_investment", "cash"),
    "capital_fund":    ("distribution_capital_fund", "cash"),
    "user_projects":   ("distribution_user_projects", "cash"),
    "charity":         ("distribution_charity", "cash"),
}


class VirtualLedger:
    """Append-only virtual ledger for one VSB. WST units; never real money."""

    def __init__(self, vsb_id: str):
        self.vsb_id = vsb_id
        _STORE.mkdir(parents=True, exist_ok=True)
        self.path = _STORE / f"{vsb_id}_ledger.json"
        # W468 (register FU-041) — construction never raises (entity establishment builds a metabolism only for its
        # template): an unreadable ledger is held as `load_error`, every reader says so, and every write re-reads
        # strictly under the lock and is refused.
        self.load_error: Optional[str] = None
        try:
            self._data = read_strict(self.path, vsb_id)
        except LedgerUnavailable as err:
            self.load_error = str(err)
            self._data = _new_books(vsb_id)

    def _load(self) -> Dict[str, Any]:
        # W468 (register FU-041) — strict. The W442 tolerant loader's comment said "quarantine, never silent-wipe", but a
        # file it could not parse (a BOM, a truncation, a list, UTF-16, a sharing violation) read as EMPTY books and the
        # next posting saved them over the real ones — one heartbeat cycle wiped a ledger by itself.
        return read_strict(self.path, self.vsb_id)

    def require_readable(self) -> None:
        """Raise LedgerUnavailable when this ledger could not be read at construction."""
        if self.load_error:
            raise LedgerUnavailable(self.load_error)

    def check_readable(self) -> None:
        """A fresh strict read (no lock): raises LedgerUnavailable when the file cannot be read whole now."""
        try:
            read_strict(self.path, self.vsb_id)
        except LedgerUnavailable as err:
            self.load_error = str(err)
            raise

    def _save(self) -> None:
        # W468 (refutation) — the writer keeps the reader's shape: two ordinary cycles could overflow a balance to
        # Infinity, and the strict read then refused the ledger's own file for good
        problem = _shape_problem(self._data)
        if problem:
            raise LedgerWriteRefused(f"{self.vsb_id}'s ledger was not saved: the books would hold {problem}")
        atomic_write_json(self.path, self._data)

    @contextmanager
    def _locked(self):
        """W442 — the money store had NO lock: /transfer, /close-period and heartbeat cycles all
        construct independent instances on the same file, and last-writer-wins silently lost
        postings (the shared-store concurrency class). Every mutation now re-loads INSIDE the
        cross-process lock — the __init__ snapshot is never trusted for a write. W468: the re-load is
        strict, so a ledger that cannot be read whole raises here and nothing is saved over it."""
        with store_lock(self.path):
            self._data = read_strict(self.path, self.vsb_id)
            self.load_error = None
            yield
            try:
                self._save()
            except LedgerWriteRefused:
                self._data = read_strict(self.path, self.vsb_id)     # this instance keeps the books as saved
                raise

    # ── double-entry core ─────────────────────────────────────────────────────
    def post(self, debit: str, credit: str, amount: float, memo: str = "",
             save: bool = True) -> Dict[str, Any]:
        """One BALANCED posting (VSB_ECONOMIC_LEGAL_MODEL §3): every movement debits one account and
        credits another for the same amount, so the books always balance (trial_balance).
        save=True runs under the store lock; save=False assumes the CALLER holds the lock
        (record/close_period batch postings inside one locked mutation)."""
        if save:
            with self._locked():
                return self._apply_posting(debit, credit, amount, memo)
        return self._apply_posting(debit, credit, amount, memo)

    def _apply_posting(self, debit: str, credit: str, amount: float, memo: str = "") -> Dict[str, Any]:
        amount = round(float(amount), 2)
        accts = self._data.setdefault("accounts", {})
        for name, side in ((debit, "debit"), (credit, "credit")):
            atype = CHART.get(name, "asset")
            normal_debit = atype in _DEBIT_NORMAL
            delta = amount if (side == "debit") == normal_debit else -amount
            accts[name] = round(accts.get(name, 0.0) + delta, 2)
        posting = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "debit": debit, "credit": credit, "amount": amount, "memo": memo,
        }
        self._data.setdefault("postings", []).append(posting)
        return posting

    def record(self, account: str, amount: float, memo: str = "", kind: str = "credit",
               ref: Optional[str] = None) -> Dict[str, Any]:
        """Record an entry (LEGACY single-sided surface — kept intact for existing readers). Also
        makes the corresponding BALANCED double-entry posting, so the real books stay double-entry
        while the legacy balances/statement remain byte-compatible."""
        with self._locked():
            if account not in self._data["balances"]:
                self._data["balances"][account] = 0.0
            delta = amount if kind == "credit" else -amount
            self._data["balances"][account] = round(self._data["balances"][account] + delta, 2)
            entry = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "account": account, "kind": kind, "amount": round(amount, 2),
                "memo": memo, "balance_after": self._data["balances"][account],
                **({"ref": ref} if ref else {}),
            }
            self._data["entries"].append(entry)
            # the balanced posting this legacy entry really means
            dr, cr = _COMPAT_POSTING.get(account) or (
                (account, "cash") if kind == "debit" else ("cash", account))
            self.post(dr, cr, amount, memo=memo or f"legacy:{account}", save=False)
            return entry

    def trial_balance(self) -> Dict[str, Any]:
        """The double-entry invariant, GENUINELY verified: the sum of debit-normal account balances
        (assets + expenses) must equal the sum of credit-normal balances (income + equity + liabilities)."""
        self.require_readable()
        accts = self._data.get("accounts", {})
        debit_side = round(sum(v for k, v in accts.items() if CHART.get(k, "asset") in _DEBIT_NORMAL), 2)
        credit_side = round(sum(v for k, v in accts.items() if CHART.get(k, "asset") not in _DEBIT_NORMAL), 2)
        return {"debit_side_total": debit_side, "credit_side_total": credit_side,
                "balanced": abs(debit_side - credit_side) < 0.02,
                "postings": len(self._data.get("postings", []))}

    def balances(self) -> Dict[str, float]:
        self.require_readable()
        return dict(self._data["balances"])

    # ── statements + period close (§9.1: P&L · balance sheet · cash flow, CFO-prepared) ──
    def _period_start_index(self) -> int:
        closes = self._data.get("closes", [])
        return int(closes[-1]["posting_index"]) if closes else 0

    def statements(self) -> Dict[str, Any]:
        """The three statements for the CURRENT period (postings since the last close), computed ONLY
        from the real double-entry postings — nothing estimated, nothing fabricated."""
        self.require_readable()
        start = self._period_start_index()
        period = self._data.get("postings", [])[start:]

        def _sum(pred) -> float:
            return round(sum(p["amount"] for p in period if pred(p)), 2)

        # P&L — income vs expenses this period
        income_by = {a: 0.0 for a, t in CHART.items() if t == "income"}
        expense_by = {a: 0.0 for a, t in CHART.items() if t == "expense"}
        for p in period:
            if CHART.get(p["credit"]) == "income":
                income_by[p["credit"]] = round(income_by.get(p["credit"], 0.0) + p["amount"], 2)
            if CHART.get(p["debit"]) == "income":   # closing/contra entries reduce income
                income_by[p["debit"]] = round(income_by.get(p["debit"], 0.0) - p["amount"], 2)
            if CHART.get(p["debit"]) == "expense":
                expense_by[p["debit"]] = round(expense_by.get(p["debit"], 0.0) + p["amount"], 2)
            if CHART.get(p["credit"]) == "expense":
                expense_by[p["credit"]] = round(expense_by.get(p["credit"], 0.0) - p["amount"], 2)
        total_income = round(sum(income_by.values()), 2)
        total_expense = round(sum(expense_by.values()), 2)
        net_profit = round(total_income - total_expense, 2)

        # Balance sheet — LIVE account balances (all periods); equity includes the unclosed period's
        # net profit so the sheet always balances (assets = liabilities + equity).
        accts = self._data.get("accounts", {})
        assets = {k: v for k, v in accts.items() if CHART.get(k, "asset") == "asset" and abs(v) > 0.005}
        liabilities = {k: v for k, v in accts.items() if CHART.get(k) == "liability" and abs(v) > 0.005}
        equity = {k: v for k, v in accts.items() if CHART.get(k) == "equity" and abs(v) > 0.005}
        equity["current_period_net_profit"] = net_profit
        assets_total = round(sum(assets.values()), 2)
        liab_equity_total = round(sum(liabilities.values()) + sum(equity.values()), 2)

        # Cash flow — movements through the cash account this period
        receipts = _sum(lambda p: p["debit"] == "cash")
        payments = _sum(lambda p: p["credit"] == "cash")

        return {
            "period": {"from_posting": start, "postings": len(period),
                       "opened_after_close": len(self._data.get("closes", []))},
            "profit_and_loss": {"income": income_by, "expenses": expense_by,
                                "total_income_wst": total_income, "total_expenses_wst": total_expense,
                                "net_profit_wst": net_profit},
            "balance_sheet": {"assets": assets, "liabilities": liabilities, "equity": equity,
                              "assets_total_wst": assets_total,
                              "liabilities_and_equity_total_wst": liab_equity_total,
                              "balanced": abs(assets_total - liab_equity_total) < 0.02},
            "cash_flow": {"operating_receipts_wst": receipts, "operating_payments_wst": payments,
                          "net_cash_movement_wst": round(receipts - payments, 2)},
            "trial_balance": self.trial_balance(),
            "prepared_by": "CFO agent (AI C-Suite) — computed from the double-entry postings",
            "disclaimer": "Virtual/simulated WST units — not real money.",
        }

    def close_period(self) -> Dict[str, Any]:
        """PERIOD CLOSE (§9.1): produce the statements, then post the closing entries — income and
        expense balances roll into retained_earnings — so the next period starts clean. Append-only:
        the close itself is recorded as real postings + a close marker."""
        with self._locked():
            stmts = self.statements()
            accts = self._data.get("accounts", {})
            for name, atype in CHART.items():
                bal = round(accts.get(name, 0.0), 2)
                if abs(bal) < 0.005:
                    continue
                if atype == "income":
                    self.post(name, "retained_earnings", bal, memo="period close — income → retained earnings",
                              save=False)
                elif atype == "expense":
                    self.post("retained_earnings", name, bal, memo="period close — expenses → retained earnings",
                              save=False)
            close = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "posting_index": len(self._data.get("postings", [])),
                "net_profit_wst": stmts["profit_and_loss"]["net_profit_wst"],
            }
            self._data.setdefault("closes", []).append(close)
        return {"close": close, "statements": stmts,
                "retained_earnings_wst": round(self._data.get("accounts", {}).get("retained_earnings", 0.0), 2)}

    def statement(self) -> Dict[str, Any]:
        if self.load_error:
            # W468 — no figures at all rather than zeros: empty books read as "this entity has nothing"
            return {"vsb_id": self.vsb_id, "currency": "WST (virtual)", "available": False,
                    "error": self.load_error,
                    "note": "this ledger could not be read whole, so no balance is shown and nothing is posted to it "
                            "until it can be",
                    "disclaimer": "Virtual/simulated WST units — not real money."}
        bal = self._data["balances"]
        return {
            "vsb_id": self.vsb_id,
            "currency": "WST (virtual)",
            "available": True,
            "balances": bal,
            # W442 — TWO BOOKS, disclosed: 'balances' is the legacy cumulative intake/distribution
            # view (record()-driven flows only) — transfers out and period closes never touch it,
            # so after a transfer it still shows the pre-transfer reserves. The live double-entry
            # balance is reported beside it so no reader mistakes the cumulative view for funds.
            "reserve_fund_wst": round((self._data.get("accounts") or {}).get("reserve_fund", 0.0), 2),
            "balances_note": ("'balances' is the cumulative legacy view (excludes transfers/closes); "
                              "'reserve_fund_wst' is the live double-entry reserve balance."),
            "total_revenue": round(bal.get("revenue", 0.0), 2),
            "total_distributed": round(sum(bal.get(a, 0.0) for a in
                                       ("owner", "self_investment", "capital_fund",
                                        "user_projects", "charity")), 2),
            "entry_count": len(self._data["entries"]),
            # W491 (FU-192) — the BOOKS' own count of metabolic cycles. The living roster's
            # `operating_cycles` counts only the cycles that roster itself ran, so an entity cycled
            # through any other path showed a smaller number beside a fuller ledger. Counted here from
            # what a cycle actually writes: one intake entry per cycle, carrying its cycle token.
            **self._cycles_posted(),
            "recent": self._data["entries"][-10:],
            "disclaimer": "Virtual/simulated WST units — not real money.",
        }

    def _cycles_posted(self) -> Dict[str, Any]:
        """Cycles as the LEDGER records them: distinct cycle tokens on the intake entries a cycle writes,
        plus the untokened intake entries (a cycle whose governance produced no token still posts intake).
        Not a count of roster visits, and not a count of postings."""
        tokens, untokened = set(), 0
        for e in (self._data.get("entries") or []):
            if not isinstance(e, dict) or not str(e.get("memo", "")).startswith("cycle intake"):
                continue
            ref = e.get("ref")
            if ref:
                tokens.add(str(ref))
            else:
                untokened += 1
        return {
            "cycles_posted": len(tokens) + untokened,
            "cycles_posted_basis": ("counted on these books: one intake entry per metabolic cycle "
                                    f"({len(tokens)} carrying a distinct cycle token, {untokened} without one). "
                                    "Cycles run before intake entries carried a token are not distinguishable "
                                    "and are counted once each."),
        }
