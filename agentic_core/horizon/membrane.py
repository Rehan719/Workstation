"""The Horizon seam: a middleware in front of the domain routes, and a hook at record_outcome.

WHAT THIS IS, SAID FIRST, BECAUSE THE WORD MEMBRANE INVITES THE WRONG READING. This seam OBSERVES. It
does not gate, block, delay, re-route or modify a single request, and nothing downstream consults what it
records. P2.11's own analysis is why: on this deployment nothing compresses a request, and the kernel's
fail-closed rule escalates an uncompressed request whose domain is unknown — so a membrane that GATED on
its own decision would refuse every request this platform serves. Observe-and-record is the smaller
claim and the true one, and it means the decision becomes a FACT ON THE RECORD rather than a block.

WHICH MAKES ONE FIELD LOAD-BEARING. Every row this seam writes carries `gated: False` with a basis
saying so in plain words, because a stored ESCALATE that nothing acted on is the most dangerous record
in this store: it looks exactly like evidence that the platform stopped and reviewed a request. It did
not. The request was served exactly as it would have been with no seam present.

WHAT IT OBSERVES, AND WHAT IT DELIBERATELY DOES NOT:

  * THE METHOD AND PATH OF A MUTATING DOMAIN REQUEST — never the body. A domain request body may hold
    someone's medical note, legal matter or financial detail, and this store is a long-lived history with
    no reader-level access rules of its own. Reading the body would also mean consuming the request
    stream and replaying it, which is a correctness risk taken for data nobody needs. So the raw text is
    the method and the path, and the record says the body was not read.
  * A GET IS NOT OBSERVED. A read is not a request to act, and observing every listing call would fill
    the store with rows carrying no decision worth recording.
  * `model_attempt` IS NOT OBSERVED at the record_outcome hook. It is a mechanism INSIDE one run — the
    orchestrator records one row per model tried — so observing it would write several intents for a
    single request and the count of observed intents would stop meaning the number of requests.

ALL OF THESE ARE STATED ON /api/v1/horizon/seam rather than left in this docstring, because a limit a
user cannot read is a limit only its author knows.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from agentic_core.horizon import kernel

#  The six domain route prefixes, read from app_mvp.py's own router registrations (law, science,
#  education, care, religion, career). Each router declares this prefix itself.
DOMAIN_PREFIXES: Tuple[str, ...] = (
    "/api/v1/law", "/api/v1/science", "/api/v1/education",
    "/api/v1/care", "/api/v1/religion", "/api/v1/career",
)

#  Mutating methods only. See the module docstring for why a GET is not observed.
OBSERVED_METHODS: Tuple[str, ...] = ("POST", "PUT", "PATCH", "DELETE")

#  The run kinds record_outcome passes that represent A REQUEST TO ACT.
OBSERVED_KINDS: Tuple[str, ...] = (
    "ai_call", "deliverable", "swarm_run", "composition_run", "transformation",
)

#  And the kinds that are excluded, each with the reason. An exclusion nobody can see is
#  indistinguishable from a path the seam failed to reach (the rule P2.13's archive index was built on).
NOT_OBSERVED_KINDS: Dict[str, str] = {
    "model_attempt": (
        "a model attempt is a MECHANISM INSIDE ONE RUN — agentic_core/ai/native/orchestrator.py records "
        "one row per model it tries, and the gateway one per stream — so observing it would write "
        "several intents for a single request and the number of observed intents would stop meaning the "
        "number of requests. The run itself is observed under its own kind"),
}

NOT_A_GATE = (
    "OBSERVED, NOT ENFORCED. This record was written by the Horizon seam, which watches and records. "
    "Nothing acted on its decision: the request was served exactly as it would have been with no seam "
    "present, and no downstream component reads this row. AN ESCALATE HERE DID NOT ESCALATE ANYTHING — "
    "it is the decision the kernel's stated terms reach over what was observed, recorded as a fact, and "
    "it must never be read as evidence that this platform stopped, reviewed, re-routed or refused the "
    "request. Whether the seam should gate a named list of grave routes is an open question (P2.11); "
    "gating on this decision as it stands would refuse every request this platform serves, because "
    "nothing compresses and an uncompressed request of unknown domain fails closed"
)

ROUTE_DOMAIN_BASIS = (
    "the domain this request's ROUTE belongs to, recorded under its own key and deliberately NOT written "
    "into the kernel's `domain` field. `domain` is a COMPRESSION field — it means 'the domain a model "
    "determined this request to be about' — and the kernel's escalation test matches that vocabulary: its "
    "list is money / legal / faith / medical / safety. Writing a route name there would make a request on "
    "the LAW route stop failing closed, because the string 'law' contains none of those words, so the "
    "record would read PROCEED on a legal matter nobody compressed. A route name is a true fact about "
    "where a request arrived and a false answer to what it was about"
)

DECISION_IS_CONSTANT = (
    "EVERY row this seam writes decides ESCALATE, and it does so BY CONSTRUCTION rather than by "
    "assessment: nothing compressed the request, so its domain is absent, and the kernel fails closed on "
    "an uncompressed request whose domain cannot be shown to be outside the grave set. So the decision on "
    "these rows carries no information about any individual request, and a reader must not read variation "
    "into a column that cannot vary. What the rows DO carry is the observation itself — what arrived, "
    "where, whether it was served — and the fact that nothing acted on any of it"
)

BODY_NOT_READ = (
    "the request BODY was not read. A domain request body may carry a medical note, a legal matter or a "
    "financial detail, and this is a long-lived store with no reader-level rules of its own, so the "
    "observation is the method and the path only. This is a deliberate narrowing of what is recorded, "
    "not a failure to capture it"
)


def domain_of(path: str) -> Optional[str]:
    """The domain prefix this path belongs to, or None. Substring-free: a prefix match on a path SEGMENT.

    `startswith` alone would make /api/v1/lawyers a law request. The boundary is checked explicitly.
    """
    p = str(path or "")
    for pref in DOMAIN_PREFIXES:
        if p == pref or p.startswith(pref + "/"):
            return pref.rsplit("/", 1)[-1]
    return None


def observes(method: str, path: str) -> Tuple[bool, str]:
    """Whether this request is observed, and WHY NOT when it is not. Both halves are reported."""
    dom = domain_of(path)
    if dom is None:
        return False, ("not a domain route: the seam fronts the six domain prefixes only, and this path "
                       "is not under one of them")
    if str(method or "").upper() not in OBSERVED_METHODS:
        return False, (f"method {str(method or '').upper()!r} is a read, and a read is not a request to "
                       f"act. Observing it would fill the store with rows carrying no decision")
    return True, f"a mutating request on the {dom} domain route"


def _record(source: str, raw_text: str, surface: str, extra: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Build, decide and store one observed row. NEVER raises into a caller.

    The seam sits on the request path and in a best-effort telemetry function; a failure to OBSERVE must
    never become a failure to serve. What it must not do is fail silently in a way nobody can measure,
    which is why `errors` is counted and reported on /api/v1/horizon/seam.
    """
    global _errors
    try:
        obs = kernel.observe(source, raw_text, surface)
        #  compressor_called=False: no model was asked what this meant. See kernel._compression_of.
        rec = kernel.build_record(obs, None, False, False, "", compressor_called=False)
        rec = {**rec, "gated": False, "gating_basis": NOT_A_GATE, **extra}
        dec = kernel.decide(rec)
        row = kernel.save(rec, dec)
        _counts[str(dec.get("decision"))] = _counts.get(str(dec.get("decision")), 0) + 1
        if extra.get("served") is False:
            _counts["_not_served"] = _counts.get("_not_served", 0) + 1
        return row
    except Exception as exc:                     # noqa: BLE001 — counted, never raised, never silent
        _errors.append(f"{exc.__class__.__name__}: {exc}")
        del _errors[:-20]
        return None


#  Observed-decision counts and the errors, so "the seam is running" is a measurement rather than a claim.
_counts: Dict[str, int] = {}
_errors: List[str] = []


def observe_request(method: str, path: str, status: Optional[int] = None,
                    raised: Optional[str] = None,
                    wall_ms: Optional[float] = None) -> Optional[Dict[str, Any]]:
    """The middleware's half: one observed row for a mutating domain request.

    THE OUTCOME IS PART OF THE OBSERVATION, and the first draft of this seam left it out. Observing
    before the request was routed recorded a 405 Method Not Allowed as a law-domain request — driven, not
    imagined: the probe's first POST hit a path that takes a different method, and the row looked exactly
    like a request the platform served. A reader counting observed intents would have counted it. So the
    middleware observes AFTER the handler, carrying the status; and in a `finally`, so a handler that
    RAISED is still observed — a run failure is precisely what P2.11's body says belongs in this store.
    """
    ok, why = observes(method, path)
    if not ok:
        return None
    _served = raised is None and isinstance(status, int) and status < 400
    #  W556 (P2.14) — A RAISED HANDLER is the first of the three triggers that writes a LessonRecord.
    #  OBSERVATION ONLY: the lesson is APPLIED_AND_LOGGED, so no change is filed. A 500 storm must not
    #  become a governance storm, and filing is a deliberate act taken afterwards through the route.
    if raised:
        try:
            from agentic_core.horizon import muhasabah
            _rec = muhasabah.observe(
                "raised_handler",
                {"method": str(method).upper(), "path": path, "exception": raised,
                 "route_domain": domain_of(path)},
                subject=None)
            muhasabah.save(_rec, muhasabah.route(_rec, "APPLIED_AND_LOGGED"), None)
        except Exception as _exc:                # noqa: BLE001 — counted, never raised into the request
            _errors.append(f"lesson: {_exc.__class__.__name__}: {_exc}")
            del _errors[:-20]
    _row = _record(
        source="domain_route", surface=f"{str(method).upper()} {path}",
        raw_text=f"{str(method).upper()} {path}",
        #  route_domain, NOT `domain`. See ROUTE_DOMAIN_BASIS — writing it into the kernel's own field
        #  would turn a legal request into a PROCEED.
        extra={"observed_because": why, "body_read": False, "body_basis": BODY_NOT_READ,
               "route_domain": domain_of(path), "route_domain_basis": ROUTE_DOMAIN_BASIS,
               "response_status": status, "handler_raised": raised, "served": _served,
               "served_basis": (
                   f"the handler answered {status}" if _served else
                   f"NOT SERVED: the handler raised {raised}, so no response was produced"
                   if raised else
                   f"NOT SERVED: the application answered {status} — a request that reached no handler, "
                   f"or one a handler refused, is not domain activity and must not be counted as such"
                   if isinstance(status, int) else
                   "NOT KNOWN: no status was supplied to this observation, so whether the request was "
                   "served cannot be stated")})
    #  W558 (P2.15) — A CONSUMPTION RECORD JOINED TO THE RUN. The seam is the only place that holds a
    #  clock around the handler, so wall time is measured here and nowhere else. Everything it cannot
    #  measure is reported as NOT MEASURED rather than as zero: no provenance map reaches this layer, so
    #  `calls` is null and says why — a run nobody instrumented is not a run that made no calls.
    if _row is not None:
        try:
            from agentic_core.horizon import consumption as _consumption
            _consumption.save(_consumption.build(
                run_id=None, wall_ms=wall_ms, provenance=None, stores_read=None, whose_data=None,
                intent_id=_row.get("intent_id")))
        except Exception as _exc:                # noqa: BLE001 — counted, never raised into the request
            _errors.append(f"consumption: {_exc.__class__.__name__}: {_exc}")
            del _errors[:-20]
    return _row


def observe_outcome(kind: str, resource: str, *, served_by: Optional[str] = None,
                    success: Optional[bool] = None) -> Optional[Dict[str, Any]]:
    """The record_outcome hook's half: one observed row for a run that happened.

    `served_by` is recorded as the RUN's provenance and is NOT used as the compression's. Who served a
    run and who compressed the request that led to it are different facts, and reading one as the other
    would manufacture COMPRESSED records for runs where nobody compressed anything.
    """
    k = str(kind or "")
    if k not in OBSERVED_KINDS:
        return None
    return _record(
        source="run_outcome", surface=f"record_outcome:{k}", raw_text=f"{k} {resource}",
        extra={"run_kind": k, "run_resource": str(resource or ""), "run_served_by": served_by,
               "run_success": success,
               "run_provenance_basis": (
                   "run_served_by names who served THE RUN. It is deliberately not used as the "
                   "compression's provenance: nobody compressed this request, and treating a run's "
                   "server as a compressor would manufacture a COMPRESSED record for a compression that "
                   "never happened")})


def report() -> Dict[str, Any]:
    """What the seam observes, what it excludes and what it has recorded. Stated, not implied."""
    return {
        "gates": False,
        "gating_basis": NOT_A_GATE,
        "domain_prefixes": list(DOMAIN_PREFIXES),
        "observed_methods": list(OBSERVED_METHODS),
        "observed_kinds": list(OBSERVED_KINDS),
        "not_observed_kinds": dict(NOT_OBSERVED_KINDS),
        "body_read": False,
        "body_basis": BODY_NOT_READ,
        "decision_is_constant": DECISION_IS_CONSTANT,
        "route_domain_basis": ROUTE_DOMAIN_BASIS,
        "observed_decisions": {k: v for k, v in _counts.items() if not k.startswith("_")},
        "observed_total": sum(v for k, v in _counts.items() if not k.startswith("_")),
        "observed_not_served": _counts.get("_not_served", 0),
        "errors": list(_errors),
        "error_count": len(_errors),
        "store_cap": kernel._CAP,
        "basis": (
            f"{sum(v for k, v in _counts.items() if not k.startswith('_'))} observation(s) recorded by "
            f"this seam in this process; the counts are per decision. "
            f"{_counts.get('_not_served', 0)} of them were NOT SERVED — the application answered 4xx/5xx "
            f"or the handler raised — and they are counted separately because an observed request that "
            f"reached no handler is not domain activity. THE COUNTS ARE PER PROCESS AND NOT A HISTORY: a "
            f"restart begins them again, and the stored rows in data/horizon/intent.json are the history "
            f"(capped at {kernel._CAP}, oldest dropped first). {len(_errors)} observation(s) FAILED and "
            f"were counted rather than swallowed — the seam must never turn a failure to observe into a "
            f"failure to serve, and a failure nobody counts is indistinguishable from a path it never "
            f"reached"),
    }
