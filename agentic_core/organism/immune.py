"""
IDBO Immune System — error rate monitoring that feeds the organism's health state.

Tracks:
- Failed AI gateway calls per endpoint (sliding 5-minute window)
- HTTP 5xx error counts
- Rate-limit throttle events

Exposes read API for biometrics endpoint to incorporate immune health into organism vitals.
"""
from __future__ import annotations

import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Deque


@dataclass
class _ErrorEvent:
    ts: float
    endpoint: str
    error_type: str  # "ai_failure" | "http_5xx" | "rate_limit" | "timeout"


class ImmuneSystem:
    """
    Ring-buffer of error events over a sliding window.
    Thread-safe — called from async FastAPI middleware and gateway.
    """

    WINDOW_SECONDS = 300  # 5-minute sliding window

    def __init__(self):
        self._events: Deque[_ErrorEvent] = deque()
        #  W658 (Owner ruling 2026-10-10) - WHAT WAS SEEN, not only what failed: one timestamp per call observed
        self._seen: Deque[float] = deque()
        self._lock = threading.Lock()

    def observe(self, endpoint: str = "") -> None:
        """W658 - a call was SEEN (it succeeded, failed, or the floor served it). Without this the sensor hears
        only failures, and "no failure" reads as full health whether a thousand calls ran or none did."""
        with self._lock:
            self._seen.append(time.monotonic())
            self._purge()

    def record(self, endpoint: str, error_type: str = "ai_failure") -> None:
        with self._lock:
            self._seen.append(time.monotonic())          # a failure is an observation too
            self._events.append(_ErrorEvent(
                ts=time.monotonic(),
                endpoint=endpoint,
                error_type=error_type,
            ))
            self._purge()

    def _purge(self) -> None:
        cutoff = time.monotonic() - self.WINDOW_SECONDS
        while self._events and self._events[0].ts < cutoff:
            self._events.popleft()
        while self._seen and self._seen[0] < cutoff:
            self._seen.popleft()

    def status(self) -> dict:
        with self._lock:
            self._purge()
            events = list(self._events)
            observed = len(self._seen)

        total = len(events)
        by_type: dict[str, int] = {}
        by_endpoint: dict[str, int] = {}
        for e in events:
            by_type[e.error_type] = by_type.get(e.error_type, 0) + 1
            if e.error_type not in REVIEW_FLAG_TYPES:      # W637 — the hot endpoint is hot with FAILURES
                by_endpoint[e.endpoint] = by_endpoint.get(e.endpoint, 0) + 1

        #  W637 (FU-592, FU-599) — A REVIEW FLAG IS NOT AN ERROR. This computed health from EVERY event, and
        #  vbs/quality.py records a compliance ESCALATION here (W483: it must reach a human) beside real
        #  failures. So ten §11 review flags on floor-served output — flags for a person to look at, not
        #  findings of harm — read as health 0.0 and threat CRITICAL: Change Control terminally rejected a HIGH
        #  change on it and the heartbeat engaged immune quarantine. The flag is still recorded and still
        #  reported, as a review flag; it does not move the threat ladder. A compliance FAIL still does.
        review_flags = sum(n for t, n in by_type.items() if t in REVIEW_FLAG_TYPES)
        failures = total - review_flags
        # Immune health: 1.0 = fully healthy, degrades with the FAILURE rate
        # 0 failures → 1.0; 10+ failures in window → 0.0
        health = max(0.0, 1.0 - (failures / 10.0))

        # Threat level based on health
        if health >= 0.8:
            threat_level = "NOMINAL"
        elif health >= 0.5:
            threat_level = "ELEVATED"
        elif health >= 0.2:
            threat_level = "HIGH"
        else:
            threat_level = "CRITICAL"

        # Most affected endpoint.
        # §4.5 class (W433) — `max(by_endpoint, key=...)` returns the FIRST maximal key in dict
        # order, and these are INTEGER error counts in a 5-minute window, so ties are the norm
        # rather than the exception: two endpoints with one error each made the earlier-inserted one
        # "the most affected". The count was never reported either, so a single stray error read
        # exactly like a genuinely hot endpoint.
        hot_endpoint, hot_errors, hot_tied = None, 0, []
        if by_endpoint:
            hot_errors = max(by_endpoint.values())
            hot_tied = sorted(e for e, n in by_endpoint.items() if n == hot_errors)
            hot_endpoint = hot_tied[0] if len(hot_tied) == 1 else None

        return {
            "health": round(health, 3),
            "threat_level": threat_level,
            # the count travels with the name: one stray error is not a hot endpoint
            "hot_endpoint_errors": hot_errors,
            "hot_endpoint_tied": hot_tied if len(hot_tied) > 1 else [],
            #  `errors_in_window` now counts what its name says. The old total is kept as
            #  `events_in_window` so no reader loses a figure, and the split is stated rather than implied.
            "errors_in_window": failures,
            "review_flags_in_window": review_flags,
            "events_in_window": total,
            "health_basis": (f"health and threat are computed from {failures} failure(s) in the window; "
                             f"{review_flags} compliance review flag(s) are reported beside them and are NOT "
                             f"counted — a flag asks a human to look, it is not a finding of harm"),
            "window_seconds": self.WINDOW_SECONDS,
            #  W658 - how much this reading rests on. Zero is not "healthy": it is "nothing was observed".
            "observations_in_window": observed,
            "observed_basis": (f"{observed} call(s) were observed in the last {self.WINDOW_SECONDS // 60} minutes"
                               if observed else
                               f"NO call was observed in the last {self.WINDOW_SECONDS // 60} minutes, so the "
                               f"health figure is the absence of failures and not a reading of anything"),
            "by_type": by_type,
            "hot_endpoint": hot_endpoint,
            "response_playbook": _response_playbook(threat_level),
        }


def _response_playbook(threat_level: str) -> list[str]:
    """W438 — the old field `active_responses` returned constant strings claiming "Adaptive routing
    engaged" / "Fallback providers activated" / "Emergency quarantine mode" when nothing engages,
    activates, or checks any of those — advertising presented as live action. The rename + phrasing
    say what a threat-level lookup can honestly say: the RECOMMENDED posture. The one real response
    that exists (immune_quarantine containment) is CCA-governed and reported by self-healing, not
    invented here."""
    playbook = {
        "NOMINAL": ["recommended: passive surveillance"],
        "ELEVATED": ["recommended: increased monitoring", "recommended: review recent error patterns"],
        "HIGH": ["recommended: throttle metabolic load (CCA immune-reconfigure)",
                 "recommended: review failing endpoints before they trip breakers"],
        "CRITICAL": ["recommended: engage immune_quarantine via POST /api/v1/cca/immune-reconfigure",
                     "recommended: owner review — the organism is under sustained threat"],
    }
    return playbook.get(threat_level, [])


#  W637 — event types that are REVIEW FLAGS, not failures. Recorded, reported, never on the threat ladder.
REVIEW_FLAG_TYPES = frozenset({"compliance_escalation"})


# Singleton — imported by gateway and middleware
#  W637 — WHAT THE HEALTH FIGURE IS, said once. W635 typed this sentence in four places; every reader of
#  `health` that prints a basis imports this one, so the description cannot drift from the computation above.
HEALTH_SCOPE = ("the immune system's health: AI-call failures and compliance regressions only - compliance "
                "review flags are reported beside it and do not lower it, and route 5xx failures are not "
                "tracked, so this is not the health of the whole platform")

immune = ImmuneSystem()


def health_fields(status: "dict | None" = None) -> dict:
    """W658 (Owner ruling 2026-10-10) - the health figure WITH what it rests on, for every response that carries
    it. One function, so a carrier cannot copy the figure and leave behind the count that says whether it is a
    reading. `organism_health_basis` is unchanged (the scope sentence); the two fields after it are new."""
    st = status if isinstance(status, dict) else immune.status()
    return {"organism_health": st.get("health"),
            "organism_health_basis": HEALTH_SCOPE,
            "organism_health_observations": st.get("observations_in_window"),
            "organism_health_observed_basis": st.get("observed_basis")}
