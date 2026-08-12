"""
Virtual double-entry ledger (per VSB) — denominated in WST (internal unit).

VIRTUAL/SIMULATED by design: these are internal accounting entries only. No real
money moves. The ledger backs the economic metabolism's statements and audit.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from agentic_core.config import atomic_write_json, data_path
from typing import Any, Dict, List

_STORE = data_path("economy")

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
    "retained_earnings":             "equity",
}
_DEBIT_NORMAL = ("asset", "expense")

# Legacy single-sided record(account, …) → the balanced posting it really means.
_COMPAT_POSTING: Dict[str, tuple] = {
    "revenue":         ("cash", "revenue"),                        # intake: Dr Cash / Cr Revenue
    "reserves":        ("reserve_fund", "cash"),                   # homeostasis: Dr Reserve Fund / Cr Cash
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
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"vsb_id": self.vsb_id, "currency": "WST", "entries": [],
                "balances": {a: 0.0 for a in ACCOUNTS},
                "postings": [], "accounts": {}, "closes": []}

    def _save(self) -> None:
        atomic_write_json(self.path, self._data)

    # ── double-entry core ─────────────────────────────────────────────────────
    def post(self, debit: str, credit: str, amount: float, memo: str = "",
             save: bool = True) -> Dict[str, Any]:
        """One BALANCED posting (VSB_ECONOMIC_LEGAL_MODEL §3): every movement debits one account and
        credits another for the same amount, so the books always balance (trial_balance)."""
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
        if save:
            self._save()
        return posting

    def record(self, account: str, amount: float, memo: str = "", kind: str = "credit") -> Dict[str, Any]:
        """Record an entry (LEGACY single-sided surface — kept intact for existing readers). Also
        makes the corresponding BALANCED double-entry posting, so the real books stay double-entry
        while the legacy balances/statement remain byte-compatible."""
        if account not in self._data["balances"]:
            self._data["balances"][account] = 0.0
        delta = amount if kind == "credit" else -amount
        self._data["balances"][account] = round(self._data["balances"][account] + delta, 2)
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "account": account, "kind": kind, "amount": round(amount, 2),
            "memo": memo, "balance_after": self._data["balances"][account],
        }
        self._data["entries"].append(entry)
        # the balanced posting this legacy entry really means
        dr, cr = _COMPAT_POSTING.get(account) or (
            (account, "cash") if kind == "debit" else ("cash", account))
        self.post(dr, cr, amount, memo=memo or f"legacy:{account}", save=False)
        self._save()
        return entry

    def trial_balance(self) -> Dict[str, Any]:
        """The double-entry invariant, GENUINELY verified: the sum of debit-normal account balances
        (assets + expenses) must equal the sum of credit-normal balances (income + equity + liabilities)."""
        accts = self._data.get("accounts", {})
        debit_side = round(sum(v for k, v in accts.items() if CHART.get(k, "asset") in _DEBIT_NORMAL), 2)
        credit_side = round(sum(v for k, v in accts.items() if CHART.get(k, "asset") not in _DEBIT_NORMAL), 2)
        return {"debit_side_total": debit_side, "credit_side_total": credit_side,
                "balanced": abs(debit_side - credit_side) < 0.02,
                "postings": len(self._data.get("postings", []))}

    def balances(self) -> Dict[str, float]:
        return dict(self._data["balances"])

    # ── statements + period close (§9.1: P&L · balance sheet · cash flow, CFO-prepared) ──
    def _period_start_index(self) -> int:
        closes = self._data.get("closes", [])
        return int(closes[-1]["posting_index"]) if closes else 0

    def statements(self) -> Dict[str, Any]:
        """The three statements for the CURRENT period (postings since the last close), computed ONLY
        from the real double-entry postings — nothing estimated, nothing fabricated."""
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
        self._save()
        return {"close": close, "statements": stmts,
                "retained_earnings_wst": round(self._data.get("accounts", {}).get("retained_earnings", 0.0), 2)}

    def statement(self) -> Dict[str, Any]:
        bal = self._data["balances"]
        return {
            "vsb_id": self.vsb_id,
            "currency": "WST (virtual)",
            "balances": bal,
            "total_revenue": round(bal.get("revenue", 0.0), 2),
            "total_distributed": round(sum(bal.get(a, 0.0) for a in
                                       ("owner", "self_investment", "capital_fund",
                                        "user_projects", "charity")), 2),
            "entry_count": len(self._data["entries"]),
            "recent": self._data["entries"][-10:],
            "disclaimer": "Virtual/simulated WST units — not real money.",
        }
