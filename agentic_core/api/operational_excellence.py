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
                   quality_gate: Optional[bool] = None,
                   ref: Optional[str] = None, vsb_id: Optional[str] = None,
                   run_id: Optional[str] = None,
                   served_by_all: Optional[List[str]] = None) -> Dict[str, Any]:
    """Append one real run outcome. Reusable in-process (the run paths call this best-effort)
    and via the /record endpoint. Never raises into a caller — recording is non-critical.

    §7 (W495, FU-125, S7.3) — every caller passed `success=bool(output)`, i.e. "the run returned some
    text". The deterministic floor ALWAYS returns text, so the recorded success could not come out
    false: the Learning Loop showed "Success rate 100%" over 119 rows and every ranked resource at an
    emerald 100%, and deliverables whose QMS gate said NOT ASSESSABLE counted as successes. Producing
    output and passing a quality gate are different facts, so both are stored:

      produced          — the run returned something (this is what `success` has always meant here)
      success           — kept AS the call outcome, because it is what every existing reader means by
                          it: model_health() scores a model on it, the orchestrator's
                          _reorder_by_health routes on that score, and /api/v1/native-ai/status
                          reports `mode_measured` from it. Re-pointing this field at a gate verdict
                          (the first attempt at this fix) silently made every model attempt unassessed,
                          so model health became unmeasurable and the status route read "unmeasured".
                          A field's meaning belongs to its readers, not to the newest writer.
      quality_gate      — True / False / None: what a gate said, or that none assessed it
      quality_verdict   — the three-state QUALITY outcome: the gate's verdict, or None for
                          "nothing assessed this run". THIS is what the Learning Loop's success RATE is
                          computed from, because "the run returned text" is not a quality judgement.

    A rate computed over rows whose `quality_verdict` is None is a rate over a population nothing
    measured, so `summary()` and `_rankings()` count assessed rows only and say how many they left out.
    """
    # OWNER RULING 2026-09-30 (18.1) - the work budget is measured in wall-clock seconds actually
    # spent, and this is the ONE place every run path already reports its duration. Feeding it here
    # makes the budget measure real work; without a producer it would be a declared capability nothing
    # reaches. Best-effort: accounting never breaks the work it accounts for.
    try:
        from agentic_core.molecular import work_budget as _wb
        _wb.spend(seconds=max(0, int(duration_ms)) / 1000.0)
    except Exception:                                    # noqa: BLE001
        pass
    _produced = bool(success)
    _verdict = None if quality_gate is None else bool(quality_gate)
    outcome = {
        "id": f"op-{uuid.uuid4().hex[:8]}",
        "kind": kind,
        "resource": resource,
        "served_by": served_by,
        "is_external": bool(is_external),
        "duration_ms": int(duration_ms),
        "produced": _produced,
        "quality_gate": _verdict,
        # the CALL outcome — model_health() and the orchestrator's routing read this
        "success": _produced,
        # None means "no gate assessed this run" — never a pass, and never counted as one
        "quality_verdict": _verdict,
        "success_basis": ("the quality gate passed" if _verdict is True else
                          "the quality gate failed" if _verdict is False else
                          "NOT ASSESSED — no quality gate evaluated this run; it produced "
                          + ("output" if _produced else "nothing")),
        "ref": ref,
        "vsb_id": vsb_id,
        # W509 (FU-009) — the run this row came from, so an outcome can be cited by whatever produced it.
        # None means the caller recorded no run identity, which is different from a run with no id.
        "run_id": run_id,
        # W509 (FU-009) — EVERY server that took part, because `served_by` above names only one and a
        # multi-stage run is not served by one thing. model_health() and the router read `served_by`, so
        # that field keeps its meaning (M-EXEC-04) and this one is added beside it. None means the caller
        # did not say; a single-server run lists that one server.
        "served_by_all": sorted(set(served_by_all)) if served_by_all else None,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        rows = _load()
        rows.append(outcome)
        _save(rows)
    except Exception:
        pass
    #  W554 (P2.11) — THE HORIZON SEAM'S SECOND HALF, placed here because this is the one function the
    #  run paths already call: thirteen call sites across the gateway, the orchestrator, the board, the
    #  swarm, deliverables, resource_fabric and transformation, plus the /record endpoint. Hooking the
    #  function reaches all of them; hooking the call sites would have reached the ones I remembered.
    #  It OBSERVES AND RECORDS AND DOES NOT GATE, and it never raises: this function's own contract is
    #  that recording is non-critical, and an observer that could break a caller would be worse than no
    #  observer. `model_attempt` is deliberately NOT observed — see membrane.NOT_OBSERVED_KINDS.
    try:
        from agentic_core.horizon import membrane as _membrane
        _membrane.observe_outcome(kind, resource, served_by=served_by, success=_produced)
    except Exception:                            # noqa: BLE001 — guards the import; the seam counts its own
        pass
    return outcome


def _rankings(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        key = r.get("resource", "unknown")
        a = agg.setdefault(key, {"resource": key, "kind": r.get("kind"), "runs": 0, "successes": 0,
                                 "assessed": 0, "produced": 0,
                                 "total_ms": 0, "in_house": 0, "last_seen": ""})
        a["runs"] += 1
        # W495 (FU-125, S7.3) — the RATE is computed from the three-state quality verdict, never from
        # "the run returned text": the floor always returns text, so the old rate could not come out
        # below 1.0. A rate over rows nothing assessed is a rate over a population nothing measured,
        # so only assessed rows enter it. Legacy rows carry no `quality_verdict` key and are therefore
        # unassessed, which is the truth about them: no gate verdict was ever recorded.
        _v = r.get("quality_verdict")
        if _v is not None:
            a["assessed"] += 1
            a["successes"] += 1 if _v else 0
        if r.get("produced", r.get("success")):
            a["produced"] += 1
        a["total_ms"] += int(r.get("duration_ms", 0))
        a["in_house"] += 0 if r.get("is_external") else 1
        a["last_seen"] = max(a["last_seen"], r.get("created_at", ""))
    out = []
    for a in agg.values():
        runs = a["runs"] or 1
        out.append({
            "resource": a["resource"], "kind": a["kind"], "runs": a["runs"],
            # None when no run of this resource was ever gate-assessed: the page must not draw a bar
            "success_rate": (round(a["successes"] / a["assessed"], 3) if a["assessed"] else None),
            "assessed_runs": a["assessed"],
            "unassessed_runs": a["runs"] - a["assessed"],
            "produced_rate": round(a["produced"] / runs, 3),
            "success_basis": (
                f"{a['successes']} of {a['assessed']} gate-assessed run(s) passed"
                if a["assessed"] else
                f"NOT ASSESSED — no quality gate evaluated any of this resource's {a['runs']} run(s); "
                f"{a['produced']} produced output, which is not the same thing"),
            "avg_duration_ms": round(a["total_ms"] / runs),
            "in_house_rate": round(a["in_house"] / runs, 3),
            "last_seen": a["last_seen"],
        })
    # best operational performers first: success, then in-house, then speed, then volume
    # W495 — success_rate is None for a resource nothing assessed; an unassessed resource sorts below
    # every assessed one rather than crashing the comparison or ranking as a zero
    out.sort(key=lambda x: (x["success_rate"] is not None, x["success_rate"] or 0.0,
                            x["in_house_rate"], -x["avg_duration_ms"], x["runs"]), reverse=True)
    return out


_BASELINE_STORE = data_path("model_health_baselines.json")


def _load_baselines(strict: bool = False) -> tuple[Dict[str, Dict[str, Any]], str | None]:
    """The declared health baselines and WHY they could not be read whole, as `(data, reason)`.

    W577 (FU-395) — `strict=True` is for `set_health_baseline`, which writes this store back. A
    tolerant read returns the store's first complete JSON value and discards the rest, so declaring
    one model's baseline would have silently DELETED every other model's — and a deleted baseline
    does not fail, it just starts scoring a model on history that predates the fix the baseline was
    declared for. A writer refuses.

    W577 (FU-298) — the reason reaches `model_health`'s readers, because a baseline that could not be
    read does not make a model unscored; it makes it scored on rows that should not have counted, and
    nothing on the surface said which.
    """
    from agentic_core.config import read_json_reported, read_json_strict
    if strict:
        return (read_json_strict(_BASELINE_STORE, {}, expect=dict) or {}), None
    data, why = read_json_reported(_BASELINE_STORE, {})
    return (data if isinstance(data, dict) else {}), why


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
        data, _ = _load_baselines(strict=True)       # W577 (FU-395) — a writer refuses
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
    baselines, _bl_why = _load_baselines()
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
        # W577 (FU-298) — the reason rides on EACH MODEL'S ROW, never at the top level: this mapping
        # is keyed by model name and `board.py` reads `len(model_health())` as a resource count, so a
        # top-level key would have become a phantom model resource. A declared baseline that could not
        # be read does not leave a model unscored - it scores it on rows that should not have counted,
        # which moves `success_rate` in the direction of the defect the baseline was declared for.
        if _bl_why:
            # W577 — the pre-flight flagged a separate `baseline_store_incomplete` key as reaching no
            # surface. Rather than add a second render for the raw reason, or delete a true statement,
            # the reason is folded INTO the basis the page already shows in the chip's title. One key,
            # one surface, and the attribution is not lost.
            out[name]["success_rate_is_incomplete"] = True
            out[name]["success_rate_basis"] = (
                "a declared baseline could not be read, so rows this model should NOT be scored on "
                "may be counted here and the rate may read WORSE than the truth — " + str(_bl_why))
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


@router.get("/failures")
async def recent_failures(limit: int = 20):
    """W583 (P3.25) — the failures the platform recorded, with the basis of the count itself.

    THE EMPTY CASE IS THREE STATES, NOT TWO, and the item's bar names the reason: "nothing recorded" must
    read as its own state and never as health. No failures over a ledger holding 400 rows says recording
    works and nothing broke; no failures over an EMPTY ledger says nothing about reliability whatsoever,
    and rendering both as a green zero would be the defect this platform spends its rounds removing.

    AND NO CAUSE IS INVENTED HERE EITHER. The handler records the exception CLASS, the route and the time,
    because those are known; `cause_established` is False on every row, and this route carries that
    forward rather than quietly presenting a class name as a diagnosis.
    """
    rows = [r for r in _load() if r.get("kind") == "route_failure"]
    total_ledger = len(_load())
    recent = list(reversed(rows[-max(1, min(int(limit), 200)):]))
    out = []
    for r in recent:
        _ref = str(r.get("ref") or "")
        _method, _, _cls = _ref.partition(" ")
        out.append({
            "route": r.get("resource"),
            "method": _method or None,
            "failure_class": _cls or None,
            "at": r.get("created_at"),
            "cause_established": False,
            "basis": (f"an unhandled {_cls or 'exception'} reached the application boundary on "
                      f"{_method or 'a request'} {r.get('resource')}; the class, the route and the time "
                      f"are recorded and the cause is NOT established"),
        })
    if rows:
        state = "failures_recorded"
        basis = (f"{len(rows)} recorded failure(s) out of {total_ledger} outcome row(s); each names its "
                 f"route, its exception class and when, and none claims a cause")
    elif total_ledger:
        state = "none_recorded"
        basis = (f"no failure has been recorded across {total_ledger} outcome row(s), so recording is "
                 f"working and nothing reached the handler - this IS a statement about reliability")
    else:
        state = "nothing_recorded_at_all"
        basis = ("the outcome ledger is EMPTY, so no failure has been recorded because NOTHING has been "
                 "recorded. This says nothing about reliability and must not be read as health")
    return {"failures": out, "total_failures": len(rows), "ledger_rows": total_ledger,
            "state": state, "basis": basis,
            "recording_since": (_load()[0].get("created_at") if total_ledger else None)}


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
    # W495 (FU-125, S7.3) — this divided "rows that returned text" by "all rows", which on the
    # deterministic floor is 1.0 by construction and was shown as "Success rate 100%".
    # the QUALITY verdict decides the rate; `success` here is still the call outcome (see
    # record_outcome's docstring: its readers are model_health and the orchestrator's routing)
    assessed = [r for r in rows if r.get("quality_verdict") is not None]
    successes = sum(1 for r in assessed if r.get("quality_verdict"))
    produced = sum(1 for r in rows if r.get("produced", r.get("success")))
    in_house = sum(1 for r in rows if not r.get("is_external"))
    ranks = _rankings(rows)
    return {
        "total_runs": n,
        "assessed_runs": len(assessed),
        "unassessed_runs": n - len(assessed),
        "success_rate": (round(successes / len(assessed), 3) if assessed else None),
        "success_rate_basis": (
            f"{successes} of {len(assessed)} gate-assessed run(s) passed"
            if assessed else
            f"NOT ASSESSED — no quality gate evaluated any of these {n} run(s). {produced} returned "
            f"output, which the deterministic floor always does, so it is not a success measure."),
        "produced_rate": round(produced / n, 3) if n else 0.0,
        "in_house_rate": round(in_house / n, 3) if n else 0.0,
        "distinct_resources": len(ranks),
        "top_resource": ranks[0]["resource"] if ranks else None,
        "kinds": sorted({r.get("kind") for r in rows if r.get("kind")}),
    }
