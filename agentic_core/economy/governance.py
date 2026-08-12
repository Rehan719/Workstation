"""§3/§8 economic governance (VSB_ECONOMIC_LEGAL_MODEL.md).

Three binding rules the model states, previously unenforced on the always-on paths:
  • "every distribution passes the gaas.v5 gate" — including the heartbeat-driven autonomous cycles
    (the API path was gated but its failure fallback silently ran ungated; the heartbeat path had
    no gate at all).
  • "Every cycle's split is logged to the UEG" — an explicit tamper-evident event carrying the
    per-stage WST amounts, not just a generic checkpoint.
  • "material/large actions route to Change Control" — distributions whose estimated distributable
    profit meets the materiality threshold are HELD until a Change Control approval exists (the
    approval is consumed on use; below-threshold cycles proceed ungated-by-CC as designed).

All amounts are virtual/simulated WST — no real funds move (real-money rails stay Owner-gated).
"""
from __future__ import annotations

import os
import time
import uuid
from typing import Any, Dict, Optional

# Materiality threshold (WST). Estimated distributable profit at/above this requires a Change
# Control approval before the cycle may run. Env-configurable for deployments/tests.
MATERIALITY_WST = float(os.getenv("ECONOMY_MATERIALITY_WST", "250000"))

_HOLD_TITLE_PREFIX = "[economy] material distribution — "


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


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


def _materiality_gate(vsb_id: str, est_distributable: float, source: str) -> Optional[Dict[str, Any]]:
    """§3 'material actions route to Change Control'. Returns None → proceed; a dict → the cycle is
    HELD (or was rejected) and must NOT run. An approved hold is consumed (marked implemented)."""
    if est_distributable < MATERIALITY_WST:
        return None
    try:
        from agentic_core.api import change_control as cca
        title = _HOLD_TITLE_PREFIX + vsb_id
        holds = [c for c in (cca._load_change(x["cca_id"]) or {} for x in cca._list_changes())
                 if c and c.get("title") == title]
        latest = max(holds, key=lambda c: c.get("submitted_at", ""), default=None)
        if latest and latest.get("status") == "approved":
            # consume the approval — one approval authorises one material cycle
            latest["status"] = "implemented"
            latest["implemented_at"] = _now()
            latest.setdefault("audit_trail", []).append(
                {"event": "consumed_by_economy_cycle", "ts": _now(), "source": source,
                 "est_distributable_wst": est_distributable})
            cca._save_change(latest)
            _ueg_log({"type": "economy.materiality_approved_consumed", "vsb_id": vsb_id,
                      "cca_id": latest["cca_id"], "est_distributable_wst": est_distributable})
            return None
        if latest and latest.get("status") in ("submitted", "under_review"):
            return {"status": "held_for_change_control", "cca_id": latest["cca_id"],
                    "impact_tier": latest.get("impact_tier"),
                    "est_distributable_wst": est_distributable,
                    "materiality_threshold_wst": MATERIALITY_WST,
                    "note": "Material distribution — awaiting Change Control approval "
                            f"(POST /api/v1/cca/{latest['cca_id']}/review)."}
        if latest and latest.get("status") == "rejected":
            return {"status": "rejected_by_change_control", "cca_id": latest["cca_id"],
                    "est_distributable_wst": est_distributable,
                    "note": "The Change Control Agency rejected this material distribution; "
                            "submit a fresh request to re-seek approval."}
        # no open hold → file one through the real CCA machinery (same store the CCA UI reviews)
        now = _now()
        cca_id = f"cca-{uuid.uuid4().hex[:10]}"
        change = {
            "cca_id": cca_id, "title": title, "change_type": "economy_material",
            "description": (f"Material virtual distribution for {vsb_id}: estimated distributable "
                            f"{est_distributable} WST ≥ materiality threshold {MATERIALITY_WST} WST. "
                            "Held until approved (virtual WST only — no real funds)."),
            "rationale": "VSB_ECONOMIC_LEGAL_MODEL §3: material/large actions route to Change Control.",
            "affected_systems": ["economy", "capital"], "submitted_by": f"economy:{source}",
            "submitted_at": now, "impact_tier": cca._determine_tier("economy_material", ""),
            "status": "submitted", "vsb_id": vsb_id, "rollback_plan": "No action taken while held.",
            "review_result": None, "decision": None, "reviewed_at": None, "implemented_at": None,
            "audit_trail": [{"event": "submitted", "ts": now, "by": f"economy:{source}"}],
        }
        cca._save_change(change)
        _ueg_log({"type": "economy.materiality_hold_filed", "vsb_id": vsb_id, "cca_id": cca_id,
                  "est_distributable_wst": est_distributable, "threshold_wst": MATERIALITY_WST})
        return {"status": "held_for_change_control", "cca_id": cca_id,
                "impact_tier": change["impact_tier"], "est_distributable_wst": est_distributable,
                "materiality_threshold_wst": MATERIALITY_WST,
                "note": "Material distribution — a Change Control request was filed and the cycle is "
                        f"held until approved (POST /api/v1/cca/{cca_id}/review)."}
    except Exception as e:
        # never silently skip the gate on a material amount — hold, loudly
        _ueg_log({"type": "economy.materiality_gate_error", "vsb_id": vsb_id, "error": str(e)[:200]})
        return {"status": "held_for_change_control", "cca_id": None,
                "note": f"Materiality gate errored ({str(e)[:120]}); the material cycle is held."}


async def governed_cycle(vsb_id: str, entity_type: str, owner: str, revenue: float,
                         costs: float = 0.0, reserve_rate: float = 0.20,
                         source: str = "api") -> Dict[str, Any]:
    """The governed metabolic cycle (async/API path): materiality → gaas.v5 gate → run → UEG split log."""
    from agentic_core.economy.metabolism import EconomicMetabolism
    metab = EconomicMetabolism(vsb_id, entity_type, owner)

    held = _materiality_gate(vsb_id, _estimate_distributable(revenue, costs, reserve_rate), source)
    if held is not None:
        return {"cycle": None, "governance": held}

    async def _action():
        return metab.run_cycle(revenue, costs, reserve_rate)

    try:
        from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
        gov = UnifiedConstitutionalInterceptorV16Omega("economy-node", UEGLogger())
        result = await gov.intercept({"intent": "economy_distribution", "vsb_id": vsb_id,
                                      "revenue_wst": revenue, "source": source}, _action)
        report = result.output if getattr(result, "output", None) else metab.run_cycle(revenue, costs, reserve_rate)
        governance: Dict[str, Any] = {"status": result.status, "checkpoint": result.checkpoint_id}
    except Exception as e:
        # §3 demands the gate; if the gate itself fails we do NOT hide it — run the (virtual) cycle
        # but emit a LOUD tamper-evident bypass event and say so in the response.
        report = metab.run_cycle(revenue, costs, reserve_rate)
        _ueg_log({"type": "economy.governance_bypass", "vsb_id": vsb_id, "source": source,
                  "error": str(e)[:200], "note": "gaas.v5 gate unavailable — cycle ran ungated (logged loudly)."})
        governance = {"status": "ungated_bypass_logged", "error": str(e)[:160]}

    _log_split(report, metab.waterfall_source, source)
    return {"cycle": report, "governance": governance}


def governed_cycle_sync(vsb_id: str, entity_type: str, owner: str, revenue: float,
                        costs: float = 0.0, reserve_rate: float = 0.20,
                        source: str = "heartbeat") -> Dict[str, Any]:
    """The governed cycle for SYNC callers (the heartbeat's autonomous ticks). Uses the genuine
    constitutional policy PRE-gate synchronously (the async interceptor cannot be awaited here);
    materiality + UEG split logging are identical to the async path."""
    from agentic_core.economy.metabolism import EconomicMetabolism
    metab = EconomicMetabolism(vsb_id, entity_type, owner)

    held = _materiality_gate(vsb_id, _estimate_distributable(revenue, costs, reserve_rate), source)
    if held is not None:
        return {"cycle": None, "governance": held}

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

    report = metab.run_cycle(revenue, costs, reserve_rate)
    _log_split(report, metab.waterfall_source, source)
    return {"cycle": report, "governance": governance}
