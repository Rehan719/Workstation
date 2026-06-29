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
import time
from typing import Any, Dict, List, Optional

from agentic_core.config import data_path

_STORE = data_path("living_vsbs.json")

# Modest virtual baseline income per autonomous operating tick (simulated — labelled, never real money).
_TICK_REVENUE = 1000.0
_TICK_COSTS = 200.0


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load() -> Dict[str, Any]:
    try:
        return json.loads(_STORE.read_text()) if _STORE.exists() else {}
    except Exception:
        return {}


def _save(d: Dict[str, Any]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(d, indent=2))


def register(vsb_id: str, name: str = "", entity_type: str = "waqf_ltd_hybrid",
             domain: str = "enterprise", owner: str = "Rehan") -> Dict[str, Any]:
    """Register an established VSB as a living entity the organism will autonomously tend."""
    d = _load()
    if vsb_id not in d:
        d[vsb_id] = {"vsb_id": vsb_id, "name": name or vsb_id, "entity_type": entity_type,
                     "domain": domain, "owner": owner, "registered_at": _now(),
                     "operating_cycles": 0, "last_operated": None, "status": "living"}
        _save(d)
    return d[vsb_id]


def list_living() -> Dict[str, Any]:
    d = _load()
    rows = sorted(d.values(), key=lambda v: v.get("registered_at", ""), reverse=True)
    return {"living_vsbs": rows, "total": len(rows),
            "note": "Established VSB enterprises the organism autonomously tends (paced virtual economy "
                    "cycles on the circadian heartbeat). Virtual/simulated — no real funds."}


def operate_one() -> Optional[Dict[str, Any]]:
    """Autonomously operate the least-recently-operated living VSB: one virtual economy cycle. Round-robin,
    paced by the heartbeat. Returns a compact record, or None when there are no living VSBs. Best-effort."""
    d = _load()
    if not d:
        return None
    # pick the least-recently-operated (None sorts first)
    target = sorted(d.values(), key=lambda v: (v.get("last_operated") or ""))[0]
    vsb_id = target["vsb_id"]
    try:
        from agentic_core.economy.metabolism import EconomicMetabolism
        metab = EconomicMetabolism(vsb_id, target.get("entity_type", "waqf_ltd_hybrid"), target.get("owner", "Rehan"))
        report = metab.run_cycle(_TICK_REVENUE, _TICK_COSTS)
        target["operating_cycles"] = int(target.get("operating_cycles", 0)) + 1
        target["last_operated"] = _now()
        target["last_distributable"] = report.get("distributable_profit")
        d[vsb_id] = target
        _save(d)
        return {"vsb_id": vsb_id, "name": target.get("name"), "cycle": target["operating_cycles"],
                "distributable_wst": report.get("distributable_profit")}
    except Exception as e:
        return {"vsb_id": vsb_id, "error": str(e)[:160]}
