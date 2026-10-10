"""
Living-QMS Quality Assurance — the single, reusable capability that subjects EVERY operational delivery
to the OWNED Quality Management System (continual operational delivery within the living QMS), holds it to
the §10 Solution-Quality Bar, and records it within the §8 biomimetic living-organism.

Honest by construction: the QMS gate runs on REAL metrics computed from the actual delivery content
(coverage = required sections present; stub = placeholder / empty content); the QMS is stateful, so
defects accumulate and a non-conformance rate is tracked across deliveries (this is what makes it
*continual*); the organism snapshot is the live immune health + circadian phase (no fabricated numbers).

Used by the org cascade (`/api/v1/swarm/cascade`), the living deliverables pipeline
(`/api/v1/deliverables/*`), and any other operational-delivery surface — so the whole platform delivers
within one living QMS, to one quality bar, inside one organism.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

# §10 — the Solution-Quality Bar every operational delivery is held to.
SOLUTION_QUALITY_BAR: List[str] = [
    "specifically designed", "modelled", "simulated", "optimised", "categorised", "ranked",
    "best-in-class", "innovative", "effective", "safe", "efficient", "commercially viable",
    "compliant", "verified", "tested", "validated",
]

# §8 — the biomimetic living-organism the delivery happens within.
BIOMIMETIC_LAYERS: List[str] = ["Genome", "Nervous", "Immune", "Cardiovascular", "Respiratory",
                                "Musculoskeletal", "Endocrine"]

# W506 (P2.7(1)) — what each declared layer actually IS, measured against the tree rather than asserted.
# FOUR states, because two could not tell "a file exists" from "the code runs":
#   engaged_with_value            contributed a measured value to the record in hand
#   engaged_no_value              ran on this path and contributed no value (a different thing from doing nothing)
#   implemented_not_on_this_path  real, reachable code that this path does not exercise
#   measurement_under_this_name   a genuine measurement published under an anatomical name — not an organ
#   code_exists_unreached         a module exists and NOTHING IMPORTS IT, so the layer does not run anywhere
#   code_unloadable               a module exists and CANNOT BE IMPORTED, so nothing could call it even if
#                                 something tried - stronger than unreached, and the difference between
#                                 "one wiring away" and code that can never run at all (W574, M1 R4.6)
# `test_w506_p27_layers` asserts the reachability claims against the tree, so none of this can rot the way
# the W434 sentence did.
LAYER_STATE: Dict[str, Dict[str, str]] = {
    "Immune": {"state": "engaged_with_value",
               "basis": "agentic_core/organism/immune.py — immune.status() is read into this record"},
    "Nervous": {"state": "engaged_no_value",
                "basis": "agentic_core/organism/nervous.py — the fire_signal below routes into the "
                         "NervousSystem; it contributes no value to this record"},
    "Genome": {"state": "implemented_not_on_this_path",
               "basis": "agentic_core/organism/genome.py — encode/crossover/mutate, mounted under "
                        "/api/v1/organism/genome; a quality record does not exercise it"},
    "Musculoskeletal": {"state": "implemented_not_on_this_path",
                        "basis": "agentic_core/api/resource_fabric.py — composable facilities that run real "
                                 "engines, EXCEPT the composed Digital Twin stage, which is a model-written "
                                 "scenario narrative and runs no simulator; a quality record does not "
                                 "exercise them"},
    "Cardiovascular": {"state": "measurement_under_this_name",
                       "basis": "agentic_core/app_mvp.py serves resource_flow = 100 - cpu_percent as "
                                "'cardiovascular'. That is host CPU headroom, honestly measured, under an "
                                "anatomical name — there is no circulatory subsystem"},
    #  W655 (ledger v15 R4.2; Owner 2026-10-10: adopt the vision's map) - THE LAYER IS THE SIGNAL BUS. This entry
    #  pointed at geospheric/regulator.py and so told every run's reader the Endocrine layer "does not run
    #  anywhere", while the vision's 17.2 map names organism/biobus.py - which this record itself fires on.
    "Endocrine": {"state": "engaged_no_value",
                  #  W593 (FU-436, M1 R6.0) — this said "a real HomeostaticRegulator with an integral term".
                  #  FU-307's correction reached the regulator's docstring (W515) and a comment in this
                  #  file, and NOT the string that ships with every delivery's quality record: the
                  #  second-writer class, where the explanation was fixed and the claim was not.
                  #  `integral_error` is assigned once as zeros and never accumulated, `dt` is computed
                  #  and never read, and the corrective action is returned as a STRING.
                  "basis": "agentic_core/organism/biobus.py — the signal bus and shared context (the vision's "
                           "17.2 map); this record's own fire_signal travels on it and it contributes no "
                           "value to the record. NOT THE LAYER, though it carries a similar name: "
                           "agentic_core/biomimicry/geospheric/regulator.py holds a HomeostaticRegulator that "
                           "does a PROPORTIONAL THRESHOLD COMPARISON and names a corrective action as a "
                           "string - no integral accumulates, no derivative is read, nothing actuates - "
                           "and NOTHING IMPORTS IT; a second copy of the same class sits "
                           "in geospheric/homeostatic_regulator.py. W434's note vouched for this layer and "
                           "W446 measured that vouching as the overclaim"},
    #  W655 (R4.2) - THE LAYER IS THE AGENT HUB, as the vision's 17.2 map and the Agent Hub page both say.
    "Respiratory": {"state": "implemented_not_on_this_path",
                    "basis": "agentic_core/api/agent_hub.py — the Agent Hub (the vision's 17.2 map): a bus that "
                             "RECORDS messages between agents; nothing is subscribed to execute what it "
                             "records, and a quality record does not exercise it. NOT THE LAYER: "
                             "agentic_core/molecular/triad_integration.py CANNOT BE IMPORTED: it imports six "
                             "siblings from agentic_core/molecular/ and only atp_simulator still exists "
                             "(p53_oscillator, ubiquitin_system, hsp_network, redox_sensor and "
                             "chaperone_cascade were archived), so it raises ModuleNotFoundError and the "
                             "TriadIntegrator can never be instantiated. Nothing imports it either, but that "
                             "is the weaker of the two facts - this basis used to say it held a REAL "
                             "TriadIntegrator, which is what code_exists_unreached is meant to mean"},
}

_STUB_RE = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum|placeholder|coming soon|as an ai)\b", re.I)
_MIN_SUBSTANTIVE = 200  # chars — below this a "delivery" is treated as an empty / stub shell.

# §10 (W449, ledger 1.1) — servers whose output THIS GATE CANNOT ASSESS. The deterministic floor
# composes its reply out of the caller's own requested headings (engine.py:153), so "declared
# sections present" is 1.0 by construction and _STUB_RE never matches its vocabulary; a deterministic
# template (the composition simulate plan) is the same shape. On these the gate does not run — the
# record says "not assessable" with the reason, and nothing is certified. 174 of 174 native
# deliverables in the store had been sealed "pass · verified" before this existed.
_NOT_ASSESSABLE_SERVERS = {"native", "template"}
NOT_ASSESSABLE_BASIS = ("not assessable — floor-served: the deterministic floor emits the requested "
                        "headings, so coverage cannot fail by construction and the stub regex never "
                        "matches its vocabulary; no instrument here can say whether this content is good")
# W449 (refuter F1) — "verbatim-ingest" is NOT in this set: content a caller supplies with no
# declared origin is judged as the caller's own writing (the old gate); a caller that knows the
# producer passes it as source_served_by and the gate judges by THAT (a floor journey → None).

# §11 — the frameworks the §10 'safe' criterion is drawn from. Named here and imported by genesis.py
# so §10 and §4.5 cannot drift apart (they had been the same tuple written out in two files).
SAFETY_FRAMEWORKS = ("ethical", "ehs", "sharia_halal")


def _assessed(verdict: Dict[str, Any]) -> bool:
    """Could this §11 row actually assess the subject? Delegates to the screen's own rule so the two
    modules cannot disagree about what a clearance is."""
    try:
        from agentic_core.api.compliance import assessed
        return assessed(verdict)
    except Exception:
        return False        # a screen that cannot be imported has assessed nothing — fail closed


def floor_served(served_by: Any) -> bool:
    """True when EVERY call that produced the content was served by a non-assessable server.

    Accepts the orchestrator's served_by string, a provenance count map ({"native": 3}), a list of
    per-agent servers, or None. None means UNKNOWN and is treated as assessable — the pre-W449
    behaviour — so a caller that does not know who served the content gets the old gate, not a
    silent "not assessable"; the honest fix at such a caller is to thread served_by through.
    A MIXED provenance (some model, some floor) is assessable: a model produced part of it."""
    if served_by is None:
        return False
    if isinstance(served_by, str):
        return served_by.strip().lower() in _NOT_ASSESSABLE_SERVERS
    if isinstance(served_by, dict):
        keys = [str(k).strip().lower() for k, n in served_by.items() if (n or 0) > 0]
        return bool(keys) and all(k in _NOT_ASSESSABLE_SERVERS for k in keys)
    if isinstance(served_by, (list, tuple, set)):
        vals = [str(v).strip().lower() for v in served_by if v is not None]
        return bool(vals) and all(v in _NOT_ASSESSABLE_SERVERS for v in vals)
    return False


def describe_served(served_by: Any) -> str:
    """One string for the record: 'native', 'native×3', 'ollama:llama3.2, native', or 'unspecified'."""
    if served_by is None:
        return "unspecified"
    if isinstance(served_by, str):
        return served_by
    if isinstance(served_by, dict):
        return ", ".join(f"{k}×{n}" for k, n in served_by.items() if (n or 0) > 0) or "unspecified"
    if isinstance(served_by, (list, tuple, set)):
        return ", ".join(sorted({str(v) for v in served_by if v is not None})) or "unspecified"
    return str(served_by)


def gate_word(verdict: Optional[bool]) -> str:
    """The three honest words for a gate verdict — a renderer must never collapse None to 'fail'."""
    return "pass" if verdict is True else "fail" if verdict is False else "not assessable"


def _measure_bar(coverage: float, stub: bool, qms_passed: Optional[bool], min_coverage: float,
                 compliance: Dict[str, Any], evidence: Optional[Dict[str, Any]],
                 floor_served: bool = False,
                 not_assessable_basis: Optional[str] = None,
                 withheld: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """§10 — the Solution-Quality Bar resolved PER-CRITERION, honestly, in THREE distinct states.

    W307 made "not measured" representable, which fixed the implied-16 problem. It left a hole at the
    INPUT, closed here (W419): a caller could pass ``evidence={"best-in-class": "trust me"}`` and the
    criterion was recorded ``measured: True`` — indistinguishable in the sealed record from a figure
    this gate computed itself. Twelve of the sixteen were assertable that way.

    Now every criterion carries ``source``:
      ``gate``     this function measured it from real delivery metrics. ``measured=True``.
      ``caller``   the caller ATTESTED it. ``attested=True``, ``measured=False`` — an attestation is
                   a claim about a run, not a measurement, and the record must never conflate them.
      ``none``     nothing established it. ``met=None``.

    The counts are reported separately for the same reason, so a reader sees "4 measured · 5 attested
    · 7 not measured" rather than a single "9 measured" that hides which is which.

    W449 adds two states the record could not express: ``floor_served`` — the two criteria this gate
    measures from coverage/stub are NOT measurable on floor output (coverage 1.0 by construction), so
    they are recorded ``met: None`` with the reason, never ``met: True``; and ``withheld`` — criteria the
    caller DECLINES to attest, with its reason (a tie, identical candidates, an empty twin), recorded
    ``source: none`` with ``basis: "not attested: …"`` instead of silently counting as attested.
    """
    ev = evidence or {}
    crit: Dict[str, Dict[str, Any]] = {}

    def measured(name: str, met, basis: str) -> None:
        # §10 (W497, FU-201) - THREE-STATE. `bool(met)` turned "the instrument could not produce a
        # figure" into "measured and FAILED", which is a different claim: a delivery that declared no
        # structure has no coverage, so the criterion computed from it is not measured either way.
        crit[name] = {"met": None if met is None else bool(met),
                      "basis": (basis if met is not None else
                                "NOT MEASURED - this criterion is computed from the delivery's coverage "
                                "against its declared sections, and this delivery declared none, so "
                                "there was nothing to compute it from"),
                      "measured": met is not None, "attested": False,
                      "source": "gate" if met is not None else "none"}

    def unmeasured(name: str) -> None:
        crit[name] = {"met": None, "basis": "not measured by this gate", "measured": False,
                      "attested": False, "source": "none"}

    def not_assessable(name: str) -> None:
        crit[name] = {"met": None, "basis": not_assessable_basis or NOT_ASSESSABLE_BASIS, "measured": False,
                      "attested": False, "source": "none"}

    if floor_served:
        not_assessable("specifically designed")
        not_assessable("verified")
    else:
        measured("specifically designed",
                 None if coverage is None else (coverage >= min_coverage and not stub),
                 f"delivery coverage {coverage} against the declared structure (min {min_coverage}), "
                 f"stub_found={stub}")
        if qms_passed is not None:
            measured("verified", bool(qms_passed), "QMS gate on real coverage/stub metrics")
        else:
            unmeasured("verified")
    # §10 (W483, ledger v5 R1.1 / R3.3) — 'compliant' and 'safe' were recorded met=True, measured=True,
    # source=gate whenever no §11 row said 'fail'. The inputs are keyword screens that describe
    # themselves as "not an EHS assessment" and "not a certification", and a run where every framework
    # returned 'review' was certified compliant AND safe. A screen can refuse; it cannot clear. So:
    #   met=False  a row that could assess FAILED (a refusal is always reportable)
    #   met=True   every row in scope PASSED and each of them could actually assess (coverage 'engine')
    #   met=None   otherwise — recorded source 'screen', naming the rows that could not assess
    _rows = list(compliance.get("verdicts") or [])

    def _bar_from_rows(name: str, rows: List[Dict[str, Any]], label: str) -> None:
        if not rows:
            unmeasured(name)
            return
        _st = {r.get("framework"): r.get("status") for r in rows}
        _gaps = sorted(r.get("framework") for r in rows if not _assessed(r))
        if any(r.get("status") == "fail" for r in rows):
            crit[name] = {"met": False, "basis": f"{label}: {_st} — a §11 row failed", "measured": True,
                          "attested": False, "source": "gate"}
        elif not _gaps and all(r.get("status") == "pass" for r in rows):
            crit[name] = {"met": True, "basis": f"{label}: {_st} — every row passed and could assess",
                          "measured": True, "attested": False, "source": "gate"}
        else:
            crit[name] = {"met": None, "measured": False, "attested": False, "source": "screen",
                          "basis": (f"{label}: {_st} — not established: "
                                    + (f"{', '.join(_gaps)} could not assess this subject (a keyword "
                                       f"screen can refuse, not clear)" if _gaps else
                                       "no row returned a pass"))}

    if _rows:
        _bar_from_rows("compliant", _rows, "§11 screen verdicts")
        _bar_from_rows("safe", [r for r in _rows if r.get("framework") in SAFETY_FRAMEWORKS],
                       "§11 safety-bearing frameworks")
    else:
        unmeasured("compliant")
        unmeasured("safe")
    _wh = withheld or {}
    for name in SOLUTION_QUALITY_BAR:
        if name in crit:
            continue
        if name in _wh:
            crit[name] = {"met": None, "basis": f"not attested: {str(_wh[name])[:200]}",
                          "measured": False, "attested": False, "source": "none"}
            continue
        if ev.get(name):
            # The caller ATTESTS this criterion. Recorded, attributed, and deliberately NOT counted
            # as measured: nothing here verifies that the step named actually ran, or ran well. An
            # empty simulation and a rich one attest identically, so the record says "attested".
            crit[name] = {"met": True, "basis": f"caller evidence: {str(ev[name])[:200]}",
                          "measured": False, "attested": True, "source": "caller"}
        else:
            unmeasured(name)
    _m = [c for c in crit.values() if c["source"] == "gate"]
    _a = [c for c in crit.values() if c["source"] == "caller"]
    _s = [c for c in crit.values() if c["source"] == "screen"]
    _n = [c for c in crit.values() if c["source"] == "none"]
    return {"criteria": crit,
            "measured": len(_m), "met": sum(1 for c in _m if c["met"]),
            "attested": len(_a), "not_measured": len(_n) + len(_s),
            # W483 — the screen-only criteria are counted OUT of 'measured' and named in their own
            # bucket, so a reader is never shown a §11 keyword screen as a measurement.
            "screen_only": len(_s),
            "screen_only_criteria": sorted(k for k, c in crit.items() if c["source"] == "screen"),
            #  W617 (FU-479) — the summary's buckets PARTITION the bar. Screen-only criteria were printed in
            #  their own bucket AND again inside "not measured", so the chip read 18 counts against a 16-item
            #  bar. `not_measured` keeps its meaning for existing readers (screen-only is also unmeasured);
            #  the printed line counts each criterion once and says out of how many.
            "summary": (f"{len(_m)} measured · {len(_a)} attested · "
                        + (f"{len(_s)} screen-only · " if _s else "")
                        + f"{len(_n)} not measured (of {len(crit)})"),
            "total": len(crit),
            "measured_criteria": sorted(k for k, c in crit.items() if c["source"] == "gate"),
            "attested_criteria": sorted(k for k, c in crit.items() if c["source"] == "caller")}


def _delivery_coverage(content: str, required_sections: Optional[List[str]]) -> Optional[float]:
    """Fraction of the required sections that actually appear in the delivered content (case-insensitive).

    §10 (W497, FU-201, class C1) — WITH NO DECLARED STRUCTURE THERE IS NO COVERAGE TO MEASURE. This
    returned 1.0 for any content past a length threshold, so "delivery coverage 1.0 against the declared
    structure" was reported for deliveries that declared none, and a QMS defect opened by the cockpit
    gate (which stores no sections) closed on 220 characters of "x x x" with coverage 1.0 — the page
    then said the correction "PASSED the same gate, measured from the content itself". A length check is
    a length check. It returns None, and every caller must say so rather than reading it as a full pass.
    """
    text = (content or "").lower()
    if not required_sections:
        return None
    present = sum(1 for s in required_sections if str(s).lower() in text)
    return round(present / len(required_sections), 3)


def _substantive(content: str) -> bool:
    """The length instrument, named for what it is: content past the substantive threshold. It is what
    remains when no structure was declared, and it is never reported as coverage."""
    return len((content or "").strip()) >= _MIN_SUBSTANTIVE


async def assure_delivery(content: str, required_sections: Optional[List[str]] = None,
                          label: str = "delivery",
                          evidence: Optional[Dict[str, Any]] = None,
                          owner_id: Optional[str] = None,
                          served_by: Any = None,
                          withheld: Optional[Dict[str, str]] = None,
                          sections_by_construction: Optional[str] = None,
                          echoed_text: Optional[str] = None) -> Dict[str, Any]:
    """Subject an operational delivery to the living QMS + §10 bar + §8 organism.

    ``served_by`` (W449) is who produced the content — the orchestrator's served_by string, a
    provenance count map, or a list per agent. When every producer is the deterministic floor the
    gate does NOT run: ``qms_gate_passed`` is None, ``qms_basis`` says why, and the two
    coverage-derived bar criteria are ``met: None`` — the record is still sealed, so the DCMS holds
    the not-assessable verdict rather than nothing. ``withheld`` names bar criteria the caller
    declines to attest, with reasons.

    Returns ``{"quality": {...}, "biomimetic": {...}}`` — honest and real (no fabricated numbers).
    Never raises: a QMS / organism hiccup is captured as an ``*_error`` field so a delivery is never
    lost to a quality-system fault.
    """
    coverage = _delivery_coverage(content, required_sections)
    stub = bool(_STUB_RE.search(content or "")) or len((content or "").strip()) < _MIN_SUBSTANTIVE
    # §10 (W497, FU-201) — the figure says what instrument produced it. A delivery that declared no
    # structure has NO coverage: what ran was the length and stub screen, and the basis says that.
    _cov_basis = (f"{len(required_sections)} declared section(s) checked against the delivered content"
                  if required_sections else
                  "NOT MEASURED — this delivery declared no required sections, so there is no coverage "
                  "to compute; what ran was the length and stub screen, which cannot stand in for it")
    #  W616 (FU-480, M1 v8 R2.0) — A COVERAGE THE GENERATOR GUARANTEES IS NOT A MEASUREMENT. The repo, web-app
    #  and phone-app gates checked for section names their own templates write ("Business Plan", "Overview" …),
    #  so coverage was 1.0 by construction and the gate recorded PASS and "specifically designed: met" over a
    #  repo whose Design and Commercialisation were blank. That is the floor's case exactly - a check that
    #  cannot fail - reached by a different route, so it takes the floor's path: the gate does not run and the
    #  record says why. The caller states the reason; the gate cannot discover that a heading is templated.
    _floor_real = floor_served(served_by)
    _floor = _floor_real or bool(sections_by_construction)
    #  both can be true at once, and then both are said: neither reason is a substitute for the other
    _na_basis = "; and ".join(
        ([NOT_ASSESSABLE_BASIS] if _floor_real or not sections_by_construction else [])
        + (["not assessable — " + str(sections_by_construction)] if sections_by_construction else []))
    _served_label = describe_served(served_by)
    quality: Dict[str, Any] = {
        "bar": list(SOLUTION_QUALITY_BAR),
        "delivery_coverage": coverage,
        "delivery_coverage_basis": _cov_basis,
        "substantive_length": _substantive(content),
        "stub_found": stub,
        "served_by": _served_label,
        "not_assessable": _floor,
    }

    # §11 (W287) — the compliance screen runs BEFORE the QMS seal (it used to run after, so the
    # tamper-evident quality record — and every board pack's DCS registration — omitted §11
    # verdicts entirely). Deterministic + explainable; flags, never silently blocks. W286 threads
    # the PRECOMPUTED QMS figures into the Ethical engine (no circular call back into this gate).
    try:
        from agentic_core.api.compliance import screen_compliance
        # FU-160 (W515) — a figure this gate has declared unassessable is NOT threaded into the screen.
        # `_floor` means the deterministic floor produced every part of this content, and
        # NOT_ASSESSABLE_BASIS says why neither figure can speak for it: the floor emits the requested
        # headings, so coverage is 1.0 by construction, and the stub regex never matches its vocabulary.
        # Sending them anyway produced a `quality: pass` carrying a coverage percentage on a delivery whose
        # own record said the gate could not run. The REASON travels instead of the numbers, and the basis
        # is the imported constant rather than a second copy of the sentence.
        # WHO READS THIS KEY (the pre-flight asks, and the answer is narrow): only
        # compliance/ethical_engine.py, and NO page. That is deliberate and worth stating, because it bounds
        # what this fix claims. The compliance layer flattens each verdict to framework/status/reason and
        # discards the inner dimensions, and W483 had already removed the quality dimension from the ethical
        # OVERALL - so the framework-level status a page renders is unchanged either way. What this corrects is
        # the DCMS-sealed quality record and the API payload, which board packs and exports consume. It does
        # not change a pixel, and claiming otherwise would be the badge-in-the-DOM error inverted.
        _metrics = ({"coverage_not_assessable": _na_basis} if _floor else
                    {"delivery_coverage": coverage, "stub_found": stub})
        screen = screen_compliance(content or "", delivery_metrics=_metrics)
        #  W643 (FU-620, ledger v14 R1) - AN ECHO OF THE PERSON'S OWN WORDS IS NOT GENERATED CONTENT THAT FAILED.
        #  On the floor the output repeats what the person typed, so a fiqh question that asks about riba, or a
        #  halal review of a product declaring pork gelatin, was failed by the word list, stamped FAIL on the
        #  person's own question, and filed as an immune failure that lowered organism health elsewhere.
        #  `echoed_text` is the caller's statement of what the person wrote (W640). The content is screened
        #  AGAIN with every word of theirs taken out: if what remains - the platform's own wording - does not
        #  fail, the fail came from the echo alone and the verdict is REVIEW. Never pass: a screen may refuse,
        #  never clear. A prohibited term the person did NOT write is still in the remainder and still fails;
        #  model-served content is not touched by this at all.
        _echo_only = False
        if _floor and screen.get("overall") == "fail" and isinstance(echoed_text, str) and echoed_text.strip():
            import re as _re_echo
            _words = sorted({w for w in _re_echo.findall(r"[^\W\d_]{3,}", echoed_text.lower())}, key=len, reverse=True)
            _residual = content or ""
            for _w in _words:
                _residual = _re_echo.sub(r"(?i)(?<![^\W\d_])" + _re_echo.escape(_w) + r"(?![^\W\d_])", " ", _residual)
            _rescreen = screen_compliance(_residual, delivery_metrics=_metrics)
            _echo_only = _rescreen.get("overall") != "fail"
        if _echo_only:
            screen = {**screen, "overall": "review", "compliant": False, "screened_overall": "fail",
                      "echo_only": True,
                      "basis": ("REVIEW, not a finding about generated content: the terms the screen matched are in "
                                "the text you wrote, which the native floor repeated; with your words taken out, "
                                "what the platform itself composed does not match. Nothing here was cleared - a "
                                "word list can flag, never clear.")}
        # W483 (R1.1) — coverage_gaps and basis were dropped here, so every downstream reader (the
        # Deliverables chip, the board pack, the sealed record) saw an overall with no way to know
        # which frameworks had actually read the subject. They travel with the verdict now.
        quality["compliance"] = {"overall": screen["overall"], "compliant": screen["compliant"],
                                 "verdicts": screen["verdicts"],
                                 "coverage_gaps": screen.get("coverage_gaps") or [],
                                 "assessed_by": screen.get("assessed_by") or [],
                                 "basis": screen.get("basis"),
                                 **({"echo_only": True, "screened_overall": screen.get("screened_overall")}
                                    if screen.get("echo_only") else {})}
    except Exception as exc:
        quality["compliance_error"] = str(exc)
    _comp = quality.get("compliance") or {}

    try:
        from agentic_core.vbs.registry import qms
        # Real, stateful gate: failures open PERSISTENT, traceable defects (W307) and move the real
        # non-conformance rate (gate failures / gates run — no normalised constants).
        # §10 (W316) — a failure's defect carries the REAL delivery reference (content hash +
        # the sections it was measured against) so the close leg can RE-MEASURE, not self-attest.
        import hashlib as _hashlib
        _ref = {"content_sha3": _hashlib.sha3_256((content or "").encode("utf-8")).hexdigest()[:24],
                "required_sections": [str(s) for s in (required_sections or [])], "label": label}
        if _floor:
            # §10 (W449, ledger 1.1) — THE GATE CANNOT FAIL ON FLOOR OUTPUT, so it does not run and
            # nothing is counted as a gate run or a pass. Genesis has said "not assessable" for its
            # own stage checks since W436; the SHARED gate every other surface uses said "pass".
            quality["qms_gate_passed"] = None
            quality["qms_basis"] = _na_basis
        elif coverage is None:
            # §10 (W497, FU-201) — the gate compares coverage against a minimum. With no declared
            # structure there is no coverage, so the comparison cannot be made: it is NOT ASSESSABLE,
            # never a pass on a length check dressed as coverage.
            quality["qms_gate_passed"] = None
            quality["qms_basis"] = (
                "not assessable — this delivery declared no required sections, so the gate's coverage "
                "comparison has nothing to compare; the length and stub screen ran and "
                + ("found a stub or too little content" if stub else "found substantive content")
                + f", which is not a gate pass (served_by={_served_label})")
        else:
            quality["qms_gate_passed"] = bool(await qms.run_quality_gates(
                {"coverage": coverage, "stubs_found": stub}, label=label, owner_id=owner_id,
                delivery_ref=_ref))
            quality["qms_basis"] = (f"QMS gate on real coverage/stub metrics "
                                    f"(served_by={_served_label})")
        quality["qms_min_coverage"] = qms.min_coverage
        quality["qms_non_conformance_rate"] = qms.get_non_conformance_rate()
        quality["qms_defects"] = qms.defect_summary()
        # §10 (W307) — the bar measured PER-CRITERION (measured / caller-attested / honestly
        # not-measured), replacing the bare 16-name list that implied a measurement that never ran.
        quality["bar_measured"] = _measure_bar(coverage, stub, quality["qms_gate_passed"],
                                               qms.min_coverage, _comp, evidence,
                                               floor_served=_floor, withheld=withheld,
                                               not_assessable_basis=_na_basis)
        # The QMS document-controls the quality record through its OWNED DCMS (QMS ⊃ DCMS, ISO 9001 §7.5):
        # the gate verdict becomes a versioned, SHA3-512-sealed controlled document — W287: the §11
        # verdicts are IN the sealed payload now (the §13 repo's 'compliance + quality record').
        quality["quality_record_hash"] = await qms.control_document(
            f"qms_record:{label}",
            {"label": label, "delivery_coverage": coverage, "stub_found": stub,
             "qms_gate_passed": quality["qms_gate_passed"], "bar": SOLUTION_QUALITY_BAR,
             # W449 — the seal is PER DELIVERY: the content hash and the server are in the sealed
             # payload (163 of 176 historical records shared one hash because it sealed only the
             # verdict shape, so one seal certified a scaffold and a real document alike).
             "content_sha3": _ref["content_sha3"], "served_by": _served_label,
             "qms_basis": quality["qms_basis"],
             "bar_measured": quality["bar_measured"],
             "compliance": {"overall": _comp.get("overall"),
                            "verdicts": _comp.get("verdicts"),
                            "coverage_gaps": _comp.get("coverage_gaps") or [],
                            "assessed_by": _comp.get("assessed_by") or []}},
            actor="QMS")
        quality["document_controlled"] = True
    except Exception as exc:  # never break a delivery on a QMS hiccup
        quality["qms_error"] = str(exc)

    # §11×§6 (W287) — every screen SEALS to the tamper-evident UEG ledger (there were ZERO
    # compliance UEG events repo-wide), and a FAIL registers with the living organism's immune
    # system — compliance is a sensed condition, not just a response field.
    # W483 — an ESCALATION (a severe-harm or extractive term matched, whose object the lexicon cannot
    # read) is what replaced the old lexicon 'fail'. It must not be quieter than what it replaced: it
    # is recorded on the delivery and sealed to the UEG, so downgrading the verdict does not
    # downgrade the signal.
    _escalations = sorted({f"{v['framework']}:{d}" for v in (_comp.get("verdicts") or [])
                           for d in (v.get("escalate") or [])})
    if _escalations:
        quality["compliance_escalations"] = _escalations
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "compliance.screen", "label": label,
                         "overall": _comp.get("overall"),
                         "coverage_gaps": _comp.get("coverage_gaps") or [],
                         "escalations": _escalations,
                         "verdicts": {v["framework"]: v["status"] for v in (_comp.get("verdicts") or [])}})
    except Exception:
        pass
    # W483 (refutation) — AN ESCALATION MUST REACH A HUMAN. The severe-harm and extractive lexicon
    # hits used to produce a 'fail', and a fail did three things: it recorded with the immune system,
    # it routed a material delivery to the arms-length Change Control Agency, and it was visible as a
    # red verdict. Downgrading it to 'review' was right — the lexicon cannot see the object of
    # "killing" — but it took all three away and left a tooltip. An escalation now travels the same
    # road as the fail it replaced; what changed is the WORDS (a flag for a human, not a finding of
    # harm), not whether anyone is told.
    _escalated = bool(_escalations)
    if _comp.get("overall") == "fail" or _escalated:
        try:
            from agentic_core.organism.immune import immune
            immune.record(f"compliance:{label}",
                          "compliance_fail" if _comp.get("overall") == "fail" else "compliance_escalation")
        except Exception:
            pass
        # §11 (W287) — a genuine VIOLATION on a MATERIAL delivery routes to the arms-length Change
        # Control Agency at MEDIUM tier (above LOW auto-approve → a real human decision), instead of
        # dying as a response field. Calibrated: only FAIL routes (post-W286 'review' is common and
        # is already surfaced in the response + UEG — routing reviews would proliferate ceremony).
        # §11 (W322) — the FAIL-routing list GROWS with the material surfaces: the entity's
        # PUBLIC faces (website/webapp/mobile) and its living deliverables are material too —
        # an engine-backed FAIL on any of them routes to Change Control, never just a flag.
        _MATERIAL = ("cascade", "vsb_repo", "board_pack",
                     "vsb_website", "vsb_webapp", "vsb_mobile", "deliverable")
        if label in _MATERIAL or label.startswith("economy"):
            try:
                from agentic_core.api.change_control import SubmitChangeRequest, submit_change
                _failed = _comp.get("overall") == "fail"
                _fails = "; ".join(f"{v['framework']}: {v['reason'][:120]}"
                                   for v in (_comp.get("verdicts") or []) if v["status"] == "fail")
                _cca = await submit_change(SubmitChangeRequest(
                    title=(f"Compliance FAIL on {label} delivery" if _failed else
                           f"Compliance escalation on {label} delivery — a human must read it"),
                    change_type="config_major",   # MEDIUM tier — never auto-approved
                    description=(f"§11 screen failed on a material '{label}' delivery "
                                 f"(content sha3 {_ref['content_sha3']}). {_fails}") if _failed else
                                (f"A §11 screen matched a severe-harm or extractive term on a material "
                                 f"'{label}' delivery (content sha3 {_ref['content_sha3']}): "
                                 f"{', '.join(_escalations)}. The lexicon cannot read the term's object, "
                                 f"so this is NOT a finding of harm — it is a flag that a person must "
                                 f"judge. Reasons: "
                                 + "; ".join(f"{v['framework']}: {v['reason'][:160]}"
                                             for v in (_comp.get("verdicts") or []) if v.get("escalate"))),
                    rationale=("Automatic routing of a compliance violation to arms-length review (W287)."
                               if _failed else
                               "W483 — a lexicon hit is escalated to a human instead of being reported as "
                               "a violation; routing it keeps the signal the old FAIL carried."),
                    affected_systems=["compliance", label], submitted_by="compliance_screen"))
                quality["compliance_routed_to_cca"] = True
                # W455 (R1.3) — the review's id travels with the artifact (it was discarded here)
                quality["compliance_cca_id"] = (_cca or {}).get("cca_id") if isinstance(_cca, dict) else None
            except Exception:
                pass

    # §8 · §17.2 (W422, corrected W434) — the record used to write `"layers": list(BIOMIMETIC_LAYERS)`,
    # naming all seven on EVERY delivery regardless of what participated. `layers` now means what it
    # says: the layers that contributed a value to THIS record. The spec's full set is kept beside it.
    #
    # W434 CORRECTION. The W422 comment claimed three of the seven "have no implementation at all
    # system-wide". That was taken from an audit summary and written here as fact without being
    # checked, and it is FALSE — the exact failure this module exists to prevent. Verified:
    #   Endocrine        biomimicry/geospheric/regulator.py — NOT a PID regulator, and this line used
    #                    to say it was. FU-307 (W515) measured the module: `integral_error` is assigned
    #                    once in __init__ as zeros and never accumulated, so there is no integral term;
    #                    `dt` occurs exactly once, on the line that computes it, and is never read, so
    #                    there is no derivative term; and the corrective action returns a STRING, so
    #                    nothing actuates. It is a threshold comparison. The file EXISTS and is not a
    #                    stub — that much was true — but naming it a controller is the same class this
    #                    correction was written to remove, committed by the correction itself. The
    #                    LAYER_STATE table below had it right all along (`code_exists_unreached`), so
    #                    one file contradicted itself for eighty rounds.
    #   Musculoskeletal  resource_fabric.py:799 names composable facilities that run real engines.
    #   Respiratory      molecular/triad_integration.py — the metabolic-respiratory core.
    #   Nervous          IS engaged on THIS path: the fire_signal below routes into the
    #                    NervousSystem. It contributes no value to the record, which is a different
    #                    statement from doing nothing.
    # So `layers_not_contributing` means exactly "contributed nothing to THIS record" — never
    # "unimplemented", and never "did nothing".
    biomimetic: Dict[str, Any] = {"layers": [],
                                  "layers_declared": list(BIOMIMETIC_LAYERS),
                                  "self": "self-managing · improving · healing"}
    try:
        from agentic_core.organism.immune import immune
        from agentic_core.organism.biobus import _circadian_cycle, biobus
        biomimetic["immune"] = immune.status()
        biomimetic["circadian"] = _circadian_cycle()
        biomimetic["layers"].append("Immune")   # the only layer that contributes a measured value
        # The organism senses every quality outcome (homeostatic feedback).
        biobus.fire_signal("cognitive", f"qms.{label}",
                           f"QMS gate {gate_word(quality.get('qms_gate_passed')).upper()} (cov={coverage})", 0.6)
    except Exception as exc:
        biomimetic["error"] = str(exc)

    # Say plainly which declared layers contributed nothing, so a reader is never left to infer
    # participation from a list that names all seven whatever happened.
    biomimetic["layers_not_contributing"] = [l for l in BIOMIMETIC_LAYERS
                                             if l not in biomimetic["layers"]]
    # W506 (P2.7(1), FU-160 S3.8) — PER LAYER, and the W434 sentence is gone. That sentence said Endocrine,
    # Musculoskeletal and Respiratory were vouched for as implemented elsewhere, which W446 measured as an
    # overclaim and this round reproduced: the Endocrine regulator has NO importer and exists in two copies,
    # and the Respiratory TriadIntegrator has no importer either. A file is not an implementation if nothing
    # calls it. Four states, because two cannot tell those cases apart.
    biomimetic["layer_states"] = {l: LAYER_STATE[l]["state"] for l in BIOMIMETIC_LAYERS}
    biomimetic["layer_basis"] = {l: LAYER_STATE[l]["basis"] for l in BIOMIMETIC_LAYERS}
    _engaged = [l for l in BIOMIMETIC_LAYERS if l in biomimetic["layers"]]
    _reachable = [l for l in BIOMIMETIC_LAYERS
                  if LAYER_STATE[l]["state"] == "implemented_not_on_this_path"]
    _unreached = [l for l in BIOMIMETIC_LAYERS if LAYER_STATE[l]["state"] == "code_exists_unreached"]
    #  W574 (M1 R4.6) — a layer whose module CANNOT BE IMPORTED is reported separately from one that
    #  merely has no importer. Collapsing them is how "holds a real TriadIntegrator" survived on a
    #  reached surface: `code_exists_unreached` promises real code one wiring away, and that module
    #  raises ModuleNotFoundError. A reader who is told a layer is unreached will ask what it would
    #  take to reach it; this one cannot be reached at all.
    _unloadable = [l for l in BIOMIMETIC_LAYERS if LAYER_STATE[l]["state"] == "code_unloadable"]
    _relabelled = [l for l in BIOMIMETIC_LAYERS if LAYER_STATE[l]["state"] == "measurement_under_this_name"]
    biomimetic["layers_note"] = (
        f"{len(biomimetic['layers'])} of {len(BIOMIMETIC_LAYERS)} declared layers contributed a value to this "
        f"record: {', '.join(_engaged) or 'none'}. "
        + (f"Engaged on this path without contributing a value: "
           f"{', '.join(l for l in BIOMIMETIC_LAYERS if LAYER_STATE[l]['state'] == 'engaged_no_value')}. "
           if any(LAYER_STATE[l]['state'] == 'engaged_no_value' for l in BIOMIMETIC_LAYERS) else "")
        + (f"Implemented and reachable, but not on this path: {', '.join(_reachable)}. " if _reachable else "")
        + (f"A measurement published under this anatomical name, not an organ: {', '.join(_relabelled)}. "
           if _relabelled else "")
        + (f"CODE EXISTS BUT NOTHING CALLS IT — so the layer does not run anywhere: {', '.join(_unreached)}. "
           if _unreached else "")
        + (f"CODE EXISTS BUT CANNOT BE IMPORTED — so the layer could not run even if something called "
           f"it: {', '.join(_unloadable)}. " if _unloadable else "")
        + "`layer_basis` names the module behind each claim.")

    return {"quality": quality, "biomimetic": biomimetic}
