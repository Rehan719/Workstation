"""
Operational Excellence — the learning loop over Workstation's OWN resources.

Records the real OUTCOME of every meaningful run (native swarm cascades, deliverable
production/regeneration, transformation orchestrations) — which OWNED resource served it,
how long it took, and whether it succeeded — then aggregates those outcomes into honest
per-resource RANKINGS (success rate, speed, in-house rate, recency). This is the feedback
substrate the platform learns from: resources that perform are surfaced and can be preferred.

Honest by construction: only real, recorded runs are aggregated — nothing is fabricated, and
an empty store reports zero (never invented numbers).

  POST /api/v1/operations/record      — record an outcome (also callable in-process)
  GET  /api/v1/operations/outcomes     — recent outcomes (?resource= / ?vsb_id= / ?kind=)
  GET  /api/v1/operations/rankings     — per-resource aggregates, ranked
  GET  /api/v1/operations/summary      — platform-wide operational summary
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import atomic_write_json, data_path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/operations", tags=["operational-excellence"])

_STORE = data_path("operations_outcomes.json")
_CAP = 2000


def _load() -> List[Dict[str, Any]]:
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save(rows: List[Dict[str, Any]]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(_STORE, rows[-_CAP:])


def record_outcome(kind: str, resource: str, *, served_by: str = "native",
                   is_external: bool = False, duration_ms: int = 0, success: bool = True,
                   ref: Optional[str] = None, vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Append one real run outcome. Reusable in-process (the run paths call this best-effort)
    and via the /record endpoint. Never raises into a caller — recording is non-critical."""
    outcome = {
        "id": f"op-{uuid.uuid4().hex[:8]}",
        "kind": kind,
        "resource": resource,
        "served_by": served_by,
        "is_external": bool(is_external),
        "duration_ms": int(duration_ms),
        "success": bool(success),
        "ref": ref,
        "vsb_id": vsb_id,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        rows = _load()
        rows.append(outcome)
        _save(rows)
    except Exception:
        pass
    return outcome


def _rankings(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        key = r.get("resource", "unknown")
        a = agg.setdefault(key, {"resource": key, "kind": r.get("kind"), "runs": 0, "successes": 0,
                                 "total_ms": 0, "in_house": 0, "last_seen": ""})
        a["runs"] += 1
        a["successes"] += 1 if r.get("success") else 0
        a["total_ms"] += int(r.get("duration_ms", 0))
        a["in_house"] += 0 if r.get("is_external") else 1
        a["last_seen"] = max(a["last_seen"], r.get("created_at", ""))
    out = []
    for a in agg.values():
        runs = a["runs"] or 1
        out.append({
            "resource": a["resource"], "kind": a["kind"], "runs": a["runs"],
            "success_rate": round(a["successes"] / runs, 3),
            "avg_duration_ms": round(a["total_ms"] / runs),
            "in_house_rate": round(a["in_house"] / runs, 3),
            "last_seen": a["last_seen"],
        })
    # best operational performers first: success, then in-house, then speed, then volume
    out.sort(key=lambda x: (x["success_rate"], x["in_house_rate"], -x["avg_duration_ms"], x["runs"]), reverse=True)
    return out


_BASELINE_STORE = data_path("model_health_baselines.json")


def _load_baselines() -> Dict[str, Dict[str, Any]]:
    from agentic_core.config import load_json_tolerant
    return load_json_tolerant(_BASELINE_STORE, {}) or {}


def set_health_baseline(model: str, reason: str, at: str | None = None) -> Dict[str, Any]:
    """§6 (W378) — declare that a model's recorded history predates a FIX and should no longer
    score it.

    Why this exists: W375 found the owned model was being throttled into failure by a budget
    derived from its own timeouts. Fixing that did not clear the damage — the model's recorded
    success rate (14.8%) still demoted it below the deterministic floor, so users kept receiving
    thin template output for hours while probation healed it one attempt per ten minutes.

    Deleting those rows would erase evidence. Instead the rows are KEPT and a baseline timestamp is
    recorded with an explicit reason; `model_health` scores only rows at or after it. The full
    history remains readable, the decision is attributable, and the action is UEG-logged.
    """
    import time as _t
    from agentic_core.config import atomic_write_json as _awj, store_lock as _lock
    reason = (reason or "").strip()
    if not reason:
        raise ValueError("a reason is required — a baseline reset must say what changed")
    stamp = at or _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime())
    with _lock(_BASELINE_STORE):
        data = _load_baselines()
        data[model] = {"since": stamp, "reason": reason[:400],
                       "set_at": _t.strftime("%Y-%m-%dT%H:%M:%SZ", _t.gmtime())}
        _awj(_BASELINE_STORE, data)
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "ai.model_health_rebaselined", "model": model,
                         "since": stamp, "reason": reason[:200]})
    except Exception:
        pass
    return data[model]


def model_health(window: int = 40) -> Dict[str, Dict[str, Any]]:
    """Per-model-resource health from recorded attempts, keyed by the model name (served_by).
    The native orchestrator uses this to ADAPT selection. Honest: only real recorded rows.
    W275 — the score is RECENCY-WINDOWED (the last `window` attempts per model, so one bad hour
    doesn't condemn a model forever and old glory doesn't mask decay), carries `last_at` (enabling
    probation retries), and folds in measured QUALITY rows (kind="model_quality" — e.g. the QMS
    verdict of a cascade the model served) alongside raw attempt success."""
    # W378 — rows recorded BEFORE a declared baseline are preserved but do not score the model
    # (they measured a since-fixed defect). Nothing is deleted; see set_health_baseline.
    baselines = _load_baselines()
    rows_by_model: Dict[str, list] = {}
    for r in _load():
        if r.get("kind") not in ("model_attempt", "model_quality"):
            continue
        name = r.get("served_by", "")
        since = (baselines.get(name) or {}).get("since")
        if since and (r.get("created_at") or "") < since:
            continue
        rows_by_model.setdefault(name, []).append(r)
    out: Dict[str, Dict[str, Any]] = {}
    for name, rows in rows_by_model.items():
        recent = rows[-max(1, int(window)):]
        succ = sum(1 for r in recent if r.get("success"))
        total_ms = sum(int(r.get("duration_ms", 0)) for r in recent)
        # W375 — SUCCESS-only latency, exposed separately. `avg_ms` averages every row INCLUDING
        # timeouts, so using it to size a timeout budget is self-defeating: a budget that is too
        # small produces fast failures, those failures pull the average down, and the next budget
        # is smaller still. Measured live: ollama's all-row avg was 17.5s while a real generation
        # needs ~98s, so the derived budget (2x avg = 35s) killed every substantial completion and
        # drove the success rate to 15%.
        ok_ms = sorted(int(r.get("duration_ms", 0)) for r in recent if r.get("success"))
        p90 = ok_ms[min(len(ok_ms) - 1, int(round(0.9 * (len(ok_ms) - 1))))] if ok_ms else 0
        out[name] = {
            "runs": len(rows),                                    # all-time volume (context)
            "window_runs": len(recent),
            "success_rate": round(succ / len(recent), 3),         # WINDOWED — the score that routes
            "avg_ms": round(total_ms / len(recent)) if recent else 0,
            "success_runs": len(ok_ms),
            "success_avg_ms": round(sum(ok_ms) / len(ok_ms)) if ok_ms else 0,
            "success_p90_ms": p90,                                # what a budget must actually allow
            "last_at": max((r.get("created_at") or "" for r in recent), default=""),
        }
    return out


def last_successful_server() -> Dict[str, Any]:
    """W458 (P1.10, ledger 1.10 · R4.7) — the most recent recorded completion that actually
    SERVED (success=True). `model_health()` aggregates per model and cannot say whether the newest
    row was a failure, so /native-ai/status had taken a failed `served_by=ollama` attempt as "ollama
    served last" and reported `real_model` while the floor served every byte.

    This is a HISTORY question — "what served last" — so, unlike the scoring aggregate, it does NOT
    apply the health baselines: a baseline says an old row must not SCORE a model, not that the serve
    never happened (applying it made a rebaseline of `native` resurrect a stale real-model success as
    "served last" while the floor was serving every byte). A row with no `served_by` attributes the
    serve to nobody and is skipped rather than reported as an unnamed real model.

    Returns {"served_by", "at", "attempts_since"} — `attempts_since` counts the failed ATTEMPTS
    (kind="model_attempt") recorded after that success; a measured-quality row is a verdict on work
    already served, never an attempt that failed."""
    failed_after = 0
    for r in reversed(_load()):
        if r.get("kind") not in ("model_attempt", "model_quality"):
            continue
        name = (r.get("served_by") or "").strip()
        if not name:
            continue
        if r.get("success"):
            return {"served_by": name, "at": r.get("created_at"), "attempts_since": failed_after}
        if r.get("kind") == "model_attempt":
            failed_after += 1
    return {"served_by": None, "at": None, "attempts_since": failed_after}


class RecordRequest(BaseModel):
    kind: str
    resource: str
    served_by: str = "native"
    is_external: bool = False
    duration_ms: int = 0
    success: bool = True
    ref: Optional[str] = None
    vsb_id: Optional[str] = None


@router.post("/record")
async def record(req: RecordRequest):
    return record_outcome(req.kind, req.resource, served_by=req.served_by, is_external=req.is_external,
                          duration_ms=req.duration_ms, success=req.success, ref=req.ref, vsb_id=req.vsb_id)


@router.get("/outcomes")
async def outcomes(resource: Optional[str] = None, vsb_id: Optional[str] = None,
                   kind: Optional[str] = None, limit: int = 100):
    rows = _load()
    if kind:
        rows = [r for r in rows if r.get("kind") == kind]
    else:
        rows = [r for r in rows if r.get("kind") != "model_attempt"]   # infra-level; hidden by default
    if resource:
        rows = [r for r in rows if r.get("resource") == resource]
    if vsb_id:
        rows = [r for r in rows if r.get("vsb_id") == vsb_id]
    return {"outcomes": rows[-limit:][::-1], "total": len(rows)}


@router.get("/degradation")
async def degradation(resource: Optional[str] = None, cycles: int = 3, window: int = 5):
    """Real performance-degradation detection over the learning loop's recorded telemetry, via the OWNED
    agentic_core/self_improvement.PerformanceDegradationDetector: buckets recent outcomes into `cycles`
    windows (avg latency + success-rate each) and flags a >12.7% latency rise OR >9.3% accuracy drop.
    Real arithmetic over real recorded runs — not a guess."""
    cycles = max(3, int(cycles))
    # W458 — model-learning rows are INFRA telemetry (one per AI call, always success on the floor,
    # sub-millisecond). Counted in the unfiltered window they displace the business telemetry this
    # detector exists to measure and the verdict becomes noise — a false "healthy" in one run and a
    # false "degraded" in the next. /outcomes, /rankings and /summary already exclude them; this
    # window did not, and W458's own floor-serve recording widened the exposure.
    _infra = ("model_attempt", "model_quality")
    rows = [r for r in _load()
            if (r.get("resource") == resource if resource else r.get("kind") not in _infra)]
    recent = rows[-(cycles * max(1, int(window))):]
    telemetry: List[Dict[str, float]] = []
    if len(recent) >= cycles:
        size = len(recent) // cycles
        for i in range(cycles):
            chunk = recent[i * size:(i + 1) * size] if i < cycles - 1 else recent[i * size:]
            if not chunk:
                continue
            lat = sum(int(c.get("duration_ms", 0)) for c in chunk) / len(chunk)
            acc = sum(1 for c in chunk if c.get("success")) / len(chunk)
            telemetry.append({"latency": max(1.0, lat), "accuracy": acc})  # guard div-by-zero in detector

    score = 0.0
    lat_change = acc_change = None
    if len(telemetry) >= 3:
        from agentic_core.self_improvement.degradation_detector import PerformanceDegradationDetector
        score = float(PerformanceDegradationDetector().detect(telemetry))
        lat_change = round(telemetry[-1]["latency"] / telemetry[0]["latency"] - 1.0, 4)
        acc_change = round(telemetry[0]["accuracy"] - telemetry[-1]["accuracy"], 4)
    return {"degraded": score >= 1.0, "score": score, "cycles_built": len(telemetry),
            "latency_change": lat_change, "accuracy_change": acc_change,
            "thresholds": {"latency_rise": 0.127, "accuracy_drop": 0.093},
            "samples": len(recent), "resource": resource or "all",
            "method": "PerformanceDegradationDetector (owned self_improvement)"}


@router.get("/rankings")
async def rankings():
    return {"rankings": _rankings([r for r in _load() if r.get("kind") != "model_attempt"])}


class RebaselineRequest(BaseModel):
    model: str
    reason: str


@router.post("/model-health/rebaseline")
async def rebaseline_model_health(req: RebaselineRequest):
    """§6 (W378) — declare that a model's recorded history predates a FIX, so it stops scoring it.

    Owner-invoked and deliberately explicit: a `reason` is REQUIRED, the prior rows are KEPT (this
    records a baseline timestamp, it does not delete evidence), and the action is logged to the
    tamper-evident UEG ledger. Use it when recorded failures measured a defect that has since been
    fixed — otherwise a model stays demoted below the deterministic floor long after it works again,
    and users keep receiving thin output.
    """
    try:
        rec = set_health_baseline(req.model, req.reason)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    return {"model": req.model, "baseline": rec, "history": "preserved (excluded from scoring only)",
            "health_now": model_health().get(req.model, {})}


@router.get("/model-health")
async def model_health_view():
    """The fabric's LEARNING surface: per-model track records and which models the native
    orchestrator is currently deprioritising (moved below the always-available native floor)."""
    # W458 — the badge follows the rule that actually ROUTES (orchestrator._reorder_by_health:
    # windowed runs and the W380 floor rate), not a stale stricter copy of it
    from agentic_core.ai.native.orchestrator import _DEMOTE_BELOW_FLOOR_RATE
    h = model_health()
    models = [{"name": name, **stats,
               "deprioritised": (name != "native" and stats["window_runs"] >= 5
                                 and stats["success_rate"] < _DEMOTE_BELOW_FLOOR_RATE)}
              for name, stats in sorted(h.items(), key=lambda kv: kv[1]["runs"], reverse=True)]
    return {
        "models": models,
        "total_attempts": sum(m["runs"] for m in models),
        "rule": ("A non-native model is flagged here when its windowed runs >= 5 and windowed "
                 f"success_rate < {_DEMOTE_BELOW_FLOOR_RATE} — the router's own demotion test "
                 "(orchestrator._reorder_by_health). The router additionally grants a demoted model one "
                 "probation retry after 10 minutes untried, which this flag does not model: while that "
                 "retry is pending the router is trying the model although the flag still reads "
                 "'deprioritised'. Rows counted are recorded attempts AND measured-quality verdicts "
                 "(kind=model_attempt / model_quality, the same window the router scores); a resource "
                 "disabled by configuration or refused by the spend policy is never attempted, so it is "
                 "skipped and recorded nowhere."),
    }


@router.get("/summary")
async def summary():
    rows = [r for r in _load() if r.get("kind") != "model_attempt"]
    n = len(rows)
    successes = sum(1 for r in rows if r.get("success"))
    in_house = sum(1 for r in rows if not r.get("is_external"))
    ranks = _rankings(rows)
    return {
        "total_runs": n,
        "success_rate": round(successes / n, 3) if n else 0.0,
        "in_house_rate": round(in_house / n, 3) if n else 0.0,
        "distinct_resources": len(ranks),
        "top_resource": ranks[0]["resource"] if ranks else None,
        "kinds": sorted({r.get("kind") for r in rows if r.get("kind")}),
    }
