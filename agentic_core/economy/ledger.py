"""
Virtual double-entry ledger (per VSB) — denominated in WST (internal unit).

VIRTUAL/SIMULATED by design: these are internal accounting entries only. No real
money moves. The ledger backs the economic metabolism's statements and audit.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List

_STORE = Path("data/economy")

# Chart of accounts (simplified, biomimetic-aware).
ACCOUNTS = ["revenue", "reserves", "owner", "self_investment",
            "capital_fund", "user_projects", "charity"]


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
                "balances": {a: 0.0 for a in ACCOUNTS}}

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def record(self, account: str, amount: float, memo: str = "", kind: str = "credit") -> Dict[str, Any]:
        """Record an entry. ``kind`` credit increases, debit decreases the account."""
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
        self._save()
        return entry

    def balances(self) -> Dict[str, float]:
        return dict(self._data["balances"])

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
