"""
IDBO Self-Healing System — circuit-breaker pattern for endpoint health.

When an endpoint fails repeatedly, the circuit opens and returns a graceful
degraded response rather than hammering a broken provider.

States:
  CLOSED   — normal operation, requests pass through
  OPEN     — too many failures, requests short-circuit immediately
  HALF_OPEN — testing recovery, ONE probe allowed through (enforced since W438)

Also provides the /api/v1/organism/self-healing/status endpoint.

W438 honesty pass: open_circuits/overall_health were computed by substring match over DECORATED
display strings, so a QUARANTINED circuit (definitely open, under immune containment) counted as
healthy — engaging the quarantine lever RAISED reported health — while HALF_OPEN (recovering)
counted as broken. Health is now computed from raw states before decoration; an empty registry
reports health null (a fresh process was asserting perfect health having measured nothing); and
HALF_OPEN genuinely admits one probe (the docstring claimed it, the code let everyone through).
"""
from __future__ import annotations

import os
import time
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/organism", tags=["idbo-organism"])


@dataclass
class _CircuitState:
    failures: int = 0
    last_failure: float = 0.0
    state: str = "CLOSED"   # CLOSED | OPEN | HALF_OPEN
    last_success: float = 0.0   # 0.0 = never (the old default_factory minted a success that never happened)
    total_calls: int = 0
    total_failures: int = 0
    quarantine_logged: bool = False   # §8 (W318) — containment engagement logged once
    probe_in_flight: bool = False     # W438 — HALF_OPEN admits ONE probe, as documented
    probe_started_at: float = 0.0     # W438 refuter catch: a probe holds a LEASE, never the circuit


class SelfHealingSystem:
    """
    Per-endpoint circuit breaker.

    Thresholds (configurable):
      failure_threshold  — consecutive failures (each within window of the previous) before opening (default 5)
      window_seconds     — max gap between failures for the count to continue (default 60)
      recovery_timeout   — seconds to wait in OPEN before trying HALF_OPEN (default 30)
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        window_seconds: float = 60.0,
        recovery_timeout: float = 30.0,
    ):
        self._threshold = failure_threshold
        self._window = window_seconds
        self._recovery = recovery_timeout
        self._circuits: dict[str, _CircuitState] = defaultdict(_CircuitState)
        self._lock = threading.Lock()
        self._healing_log: list[dict] = []  # last 50 healing events
        self._events_ever = 0
        self._process_started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        # W438 — the quarantine lever is a disk read (reconfig JSON); cache it briefly so the
        # model-routing hot path (is_open per candidate model per request) does not pay a
        # serialized file read per consult while a circuit is open
        self._quarantine_cache: tuple[bool, float] = (False, 0.0)

    def record_success(self, endpoint: str) -> None:
        with self._lock:
            c = self._circuits[endpoint]
            c.total_calls += 1
            c.last_success = time.monotonic()
            c.probe_in_flight = False
            if c.state in ("OPEN", "HALF_OPEN"):
                c.state = "CLOSED"
                c.failures = 0
                self._log_event(endpoint, "CLOSED", "Circuit recovered after successful call")

    def record_failure(self, endpoint: str) -> None:
        with self._lock:
            c = self._circuits[endpoint]
            c.total_calls += 1
            c.total_failures += 1
            c.probe_in_flight = False
            now = time.monotonic()

            # Reset failure count if outside window
            if now - c.last_failure > self._window:
                c.failures = 0

            c.failures += 1
            c.last_failure = now

            if c.state == "CLOSED" and c.failures >= self._threshold:
                c.state = "OPEN"
                # W438 — the old reason claimed "N failures in {window}s window", but the counter
                # only resets on a single gap > window, so a slow drip each 59s apart accumulates
                # past any window; say what is actually measured
                self._log_event(endpoint, "OPEN",
                                f"{c.failures} consecutive failures, each within "
                                f"{self._window:.0f}s of the previous")
            elif c.state == "HALF_OPEN":
                c.state = "OPEN"
                self._log_event(endpoint, "OPEN", "Half-open test failed — re-opening circuit")

    def set_quarantine(self, value: bool) -> None:
        """W438 refuter catch: the 2s TTL cache admitted recovery probes for up to 2s AFTER the
        Owner engaged containment. The single write path (reconfiguration.apply_config_change)
        now PUSHES the lever value here the moment it changes, so containment is immediate."""
        self._quarantine_cache = (bool(value), time.monotonic())

    def _quarantine_active(self) -> bool:
        """§8 (W318) — the CRITICAL immune lever's real consumer: while the Owner-governed
        `organism.immune_quarantine` lever is set (via the CCA), OPEN circuits are fully
        CONTAINED — no half-open recovery probes reach a failing backend. Cached ~2s (W438)."""
        val, at = self._quarantine_cache
        now = time.monotonic()
        if now - at < 2.0:
            return val
        try:
            from agentic_core.organism.reconfiguration import _load_config
            val = bool(((_load_config() or {}).get("organism") or {}).get("immune_quarantine"))
        except Exception:
            val = False
        self._quarantine_cache = (val, now)
        return val

    def is_open(self, endpoint: str) -> bool:
        with self._lock:
            c = self._circuits[endpoint]
            if c.state == "OPEN":
                if self._quarantine_active():
                    if not c.quarantine_logged:
                        c.quarantine_logged = True   # log the engagement once per containment
                        self._log_event(endpoint, "QUARANTINED",
                                        "immune_quarantine lever active — containment holds "
                                        "(no half-open probes until the lever clears)")
                        try:
                            from agentic_core.gaas.v5 import UEGLogger
                            UEGLogger().log({"type": "immune.quarantine_engaged",
                                             "endpoint": endpoint})
                        except Exception:
                            pass
                    return True
                # Try half-open after recovery timeout — admitting exactly ONE probe (W438: the
                # module always documented single-probe semantics; the code let every concurrent
                # caller through, so a broken backend could absorb N parallel 180s model budgets)
                if time.monotonic() - c.last_failure > self._recovery:
                    c.state = "HALF_OPEN"
                    c.quarantine_logged = False
                    c.probe_in_flight = True
                    c.probe_started_at = time.monotonic()
                    self._log_event(endpoint, "HALF_OPEN", "Testing recovery (one probe admitted)")
                    return False  # allow THIS one request through
                return True
            if c.state == "HALF_OPEN":
                # W438 refuter catch: a probe whose caller never reports back must not block the
                # circuit FOREVER — the probe slot is a LEASE. A probe outstanding longer than the
                # recovery window (min 30s) is presumed dead and the slot is re-granted.
                lease = max(self._recovery, 30.0)
                if c.probe_in_flight and time.monotonic() - c.probe_started_at <= lease:
                    return True   # a live probe is testing recovery — everyone else waits
                if c.probe_in_flight:
                    self._log_event(endpoint, "HALF_OPEN",
                                    f"probe lease expired after {lease:.0f}s — re-granting the slot")
                c.probe_in_flight = True
                c.probe_started_at = time.monotonic()
                return False
            return False

    def attempt_heal(self) -> dict:
        """Proactive self-healing: actively probe circuits that have been OPEN past the recovery window
        (flip them to HALF_OPEN so the next call tests recovery) rather than only waiting passively for the
        next request to trigger it. Called autonomously on the circadian heartbeat — the immune→self-healing
        reflex (§3 'defends and heals itself'). Returns which circuits were probed."""
        probed: list[str] = []
        if self._quarantine_active():
            # §8 (W318) — while the immune_quarantine lever holds, containment beats healing:
            # the organism does NOT probe quarantined circuits (honest no-op, recorded).
            with self._lock:
                self._log_event("(all)", "QUARANTINE_HOLD",
                                "attempt_heal held — immune containment active, no probes")
            return {"probed": [], "count": 0, "quarantine_hold": True}
        with self._lock:
            now = time.monotonic()
            for ep, c in self._circuits.items():
                if c.state == "OPEN" and now - c.last_failure > self._recovery:
                    c.state = "HALF_OPEN"
                    c.probe_in_flight = False   # the next real call takes the probe slot
                    self._log_event(ep, "HALF_OPEN", "Proactive heal — organism probing recovery (heartbeat)")
                    probed.append(ep)
        return {"probed": probed, "count": len(probed), "quarantine_hold": False}

    def _log_event(self, endpoint: str, new_state: str, reason: str) -> None:
        self._events_ever += 1
        self._healing_log.append({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "endpoint": endpoint,
            "state": new_state,
            "reason": reason,
        })
        if len(self._healing_log) > 50:
            self._healing_log.pop(0)

    def log(self) -> dict:
        """The healing log, honestly framed: a snapshot copy (never the live mutable list), with
        the cap and the true events-ever count (the old `total` was len() of a 50-capped list)."""
        with self._lock:
            return {"events": list(self._healing_log), "count": len(self._healing_log),
                    "capacity": 50, "events_ever": self._events_ever,
                    "scope": "in-memory, this server process since start",
                    "process_started_at": self._process_started_at}

    def status(self) -> dict:
        _q = self._quarantine_active()
        with self._lock:
            circuits = {}
            open_count = 0
            for ep, c in self._circuits.items():
                # W438 — count from the RAW state, decorate for display: the old code counted
                # 'OPEN' as a substring of the DISPLAY string, so "QUARANTINED (immune
                # containment)" read as healthy (health ROSE when containment engaged on failing
                # endpoints) and "HALF_OPEN (pending test)" read as broken
                raw_open = c.state == "OPEN"
                if raw_open:
                    open_count += 1
                state = c.state
                if raw_open and _q:
                    state = "OPEN (quarantined — immune containment)"
                elif raw_open and time.monotonic() - c.last_failure > self._recovery:
                    state = "OPEN (half-open pending)"
                circuits[ep] = {
                    "state": state,
                    "failures_in_window": c.failures,
                    "total_failures": c.total_failures,
                    "total_calls": c.total_calls,
                    "failure_rate": round(c.total_failures / c.total_calls, 3) if c.total_calls else 0.0,
                }

            tracked = len(circuits)
            # W438 refuter catch, second round: a bare is_open() consult mints a CLOSED circuit
            # with zero calls, and the first version then asserted health 1.0 "over 1 circuit" —
            # perfect health from zero measurements, the same shape one step past N=0. Health is
            # computed over circuits that have actually CARRIED calls.
            measured = sum(1 for ep, c in self._circuits.items() if c.total_calls > 0)
            open_measured = sum(1 for ep, c in self._circuits.items()
                                if c.total_calls > 0 and c.state == "OPEN")
            health = round(max(0.0, 1.0 - (open_measured / measured)), 3) if measured else None

            return {
                "overall_health": health,
                "health_basis": (f"1 − open/measured over {measured} circuits that carried calls"
                                 + (f" ({tracked - measured} consulted but never called)"
                                    if tracked > measured else "") if measured else
                                 "no circuit has carried a call yet — nothing measured, health unknown"),
                "measured_endpoints": measured,
                "circuits": circuits,
                "open_circuits": open_count,
                "tracked_endpoints": tracked,
                "healing_log": self._healing_log[-10:],  # last 10 events
                "thresholds": {
                    "failure_threshold": self._threshold,
                    "window_seconds": self._window,
                    "recovery_timeout": self._recovery,
                },
                "scope": "in-memory, this server process since start",
                "process_started_at": self._process_started_at,
                "pid": os.getpid(),
            }


# Singleton
self_healer = SelfHealingSystem()


# ── Status endpoint ───────────────────────────────────────────────────────────

@router.get("/self-healing/status")
async def self_healing_status():
    """Return circuit breaker status for all tracked endpoints."""
    return self_healer.status()


@router.get("/self-healing/log")
async def self_healing_log():
    """Return the healing event log (capped snapshot + true events-ever count)."""
    return self_healer.log()
