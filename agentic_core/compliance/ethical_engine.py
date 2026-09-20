"""
Ethical Engine (§11, W286) — deterministic, explainable, per-dimension ethical evaluation.

Replaces the old hardcoded "pass — no violations detected" (a standing fabrication: nothing was
ever checked) with four REAL sub-verdicts:

  human      — human well-being & safety (harm / exploitation / deception lexicons, severity-tiered)
  environment— environmental well-being (impact framing over the EHS vocabulary)
  quality    — accepts the PRECOMPUTED delivery metrics (coverage / stub) threaded in by the caller
               (assure_delivery computes them); NEVER calls back into the quality gate — that would
               be a circular import. With no metrics supplied the dimension is honestly
               'not_assessed', never a fabricated pass.
  value      — value & beneficence: stated benefit vs extractive framing.

Verdict semantics per dimension: pass | review | fail | not_assessed. Overall: worst-of
(fail > review > pass), where not_assessed never improves nor worsens the overall but is
always ENUMERATED in the reason — silence is not a verdict.

§11 (W483, ledger v5 R1.0 / R2.1) — WHAT A LEXICON CAN AND CANNOT SAY.
A word list is an indicator, not an assessment, and the three things it cannot do are now refused:

  1. It cannot convict. 'kill' matched "varroa mites are killing a third of my colonies" and the
     platform recorded 'human: fail — Severe human-harm indicator', which made the whole §11 screen
     FAIL: candidates vetoed, the first economic cycle held 'compliance_fail_hold', four ship commit
     messages reading 'compliance fail', and an export stamped NOT CLEARED FOR USE. These verbs take
     an object, and the lexicon cannot see the object. A severe hit is now `review` carrying
     `escalate: True` and the matched term — the delivery still goes to a human, which is what a
     flag is for; it is no longer reported as a finding of harm.
  2. It cannot clear. The absence of a word is not evidence of safety, so no dimension returns
     `pass` off an empty match: it returns `not_assessed` naming the lexicon that found nothing.
  3. It cannot take the subject's word for it. A text calling itself beneficial ('halal', 'care',
     'community') was scored `value: pass` on its own vocabulary. That is the subject's claim about
     itself, and it is recorded as `not_assessed` with the term quoted.

The one dimension that still returns pass/fail is `quality`, and only because it reads MEASURED
figures the QMS computed. Each dimension therefore carries `coverage`: 'metrics' (measured here) ·
'lexicon' (a term matched — a fact about the text, not about the venture) · 'none'. Callers must
decide by coverage, never by status alone: `agentic_core.vbs.quality` records the §10 'compliant'
and 'safe' criteria as met only where a row could actually assess.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

# severity-tiered human-impact lexicons (deterministic + explainable — the match IS the reason)
_HARM_SEVERE = re.compile(
    r"\b(kill|murder|assault|traffick|abuse|torture|terror|weaponi[sz]|self[- ]harm|suicide)\w*",
    re.IGNORECASE)
_HARM_REVIEW = re.compile(
    r"\b(exploit|coerc|manipulat|deceiv|deceptive|mislead|surveil|addict|discriminat|harass)\w*",
    re.IGNORECASE)
_ENV_IMPACT = re.compile(
    r"\b(pollut|deforest|dump(?:ing)?|contaminat|over[- ]?fish|strip[- ]?min|carbon[- ]intensive|"
    r"non[- ]recyclable|single[- ]use plastic)\w*", re.IGNORECASE)
_EXTRACTIVE = re.compile(
    r"\b(dark pattern|lock[- ]in|hidden fee|bait[- ]and[- ]switch|planned obsolescence|"
    r"predatory|price goug|spam)\w*", re.IGNORECASE)
_BENEFIT = re.compile(
    r"\b(benefit|well[- ]?being|charit|educat|health|nourish|empower|accessib|sustain|halal|"
    r"community|care|safety|transparent|beneficen)\w*", re.IGNORECASE)

_MIN_ASSESSABLE = 40   # chars — shorter subjects (charity cause names, /check probes) cannot be
                       # meaningfully quality-assessed; that dimension reports not_assessed.


ASSESSING_COVERAGE = frozenset({"metrics"})   # the only coverage that can clear a subject here


def _dim(dimension: str, status: str, reason: str, coverage: str = "lexicon",
         escalate: bool = False) -> Dict[str, Any]:
    d: Dict[str, Any] = {"dimension": dimension, "status": status, "reason": reason,
                         "coverage": coverage}
    if escalate:
        d["escalate"] = True
    return d


_LEXICON_NOT_A_VERDICT = "a word-list indicator, not an assessment"


def evaluate_ethics(text: str,
                    delivery_metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Evaluate a subject across the four ethical dimensions. `delivery_metrics` may carry the
    caller's PRECOMPUTED {"delivery_coverage": float, "stub_found": bool} (assure_delivery has
    them); absent metrics → the quality dimension is honestly 'not_assessed'."""
    text = text or ""
    dims: List[Dict[str, str]] = []

    # human well-being & safety — a matched verb ('kill', 'abuse') takes an object this lexicon
    # cannot see, so a hit ESCALATES for a human to read; it never convicts, and a miss never clears.
    m = _HARM_SEVERE.search(text)
    if m:
        dims.append(_dim("human", "review",
                         f"Severe-harm term present: '{m.group(0)}' — {_LEXICON_NOT_A_VERDICT}; the "
                         "term's object is not read here, so this is escalated for a human to assess",
                         escalate=True))
    else:
        m = _HARM_REVIEW.search(text)
        if m:
            dims.append(_dim("human", "review",
                             f"Potential human-impact concern: '{m.group(0)}' — {_LEXICON_NOT_A_VERDICT}"))
        else:
            dims.append(_dim("human", "not_assessed",
                             "No harm/exploitation/deception term matched — the absence of a word is "
                             "not evidence of safety, so nothing is cleared here."))

    # environmental well-being
    m = _ENV_IMPACT.search(text)
    if m:
        dims.append(_dim("environment", "review",
                         f"Environmental-impact framing: '{m.group(0)}' — {_LEXICON_NOT_A_VERDICT}"))
    else:
        dims.append(_dim("environment", "not_assessed",
                         "No adverse-environment term matched — a word list cannot say a venture is "
                         "environmentally sound."))

    # quality — ONLY from precomputed metrics; never fabricated
    if delivery_metrics and "delivery_coverage" in delivery_metrics:
        cov = float(delivery_metrics.get("delivery_coverage") or 0.0)
        stub = bool(delivery_metrics.get("stub_found"))
        if stub:
            dims.append(_dim("quality", "review", "Stub/placeholder content detected by the QMS.",
                             coverage="metrics"))
        elif cov < 0.5:
            dims.append(_dim("quality", "review", f"Low delivery coverage ({cov:.2f}) from the QMS.",
                             coverage="metrics"))
        else:
            dims.append(_dim("quality", "pass", f"QMS delivery coverage {cov:.2f}, no stub.",
                             coverage="metrics"))
    elif len(text.strip()) < _MIN_ASSESSABLE:
        dims.append(_dim("quality", "not_assessed",
                         "Subject too short for a quality assessment — honestly not assessed.",
                         coverage="none"))
    else:
        dims.append(_dim("quality", "not_assessed",
                         "No QMS metrics supplied for this subject — honestly not assessed.",
                         coverage="none"))

    # value & beneficence — an extractive term is an indicator to escalate; the subject's OWN
    # benefit vocabulary is its claim about itself and clears nothing.
    m = _EXTRACTIVE.search(text)
    if m:
        dims.append(_dim("value", "review",
                         f"Extractive/deceptive value framing: '{m.group(0)}' — "
                         f"{_LEXICON_NOT_A_VERDICT}; escalated for a human to assess",
                         escalate=True))
    elif _BENEFIT.search(text):
        dims.append(_dim("value", "not_assessed",
                         f"The subject describes itself with benefit vocabulary "
                         f"('{_BENEFIT.search(text).group(0)}') — its own claim, which is not evidence "
                         f"of beneficence; nothing here assessed the value case."))
    elif len(text.strip()) < _MIN_ASSESSABLE:
        dims.append(_dim("value", "not_assessed",
                         "Subject too short to evidence value/beneficence — honestly not assessed.",
                         coverage="none"))
    else:
        dims.append(_dim("value", "not_assessed",
                         "No stated human/communal benefit found — the absence of benefit vocabulary "
                         "is not a finding against the venture; the value case was not assessed."))

    # W483 (refutation) — the overall is the worst of the ETHICAL dimensions only. `quality` reads
    # the QMS's section-coverage and stub figures: a real measurement, but of the DELIVERY, not of
    # the ethics. It used to carry the overall to 'pass', and through it the whole §11 screen, on a
    # clean document whose human, environment and value dimensions had all said not_assessed. A
    # figure may only carry the name of what it measured, so the quality dimension is reported
    # beside the verdict, never as one.
    _ethical_dims = [d for d in dims if d["dimension"] != "quality"]
    statuses = [d["status"] for d in _ethical_dims]
    overall = ("fail" if "fail" in statuses else
               "review" if "review" in statuses else
               "pass" if "pass" in statuses else "not_assessed")
    _quality = next((d for d in dims if d["dimension"] == "quality"), None)
    reason = "; ".join(f"{d['dimension']}: {d['status']}" for d in dims)
    return {"overall": overall, "dimensions": dims, "reason": reason,
            # What the QMS measured, named as what it is and kept out of the ethical verdict.
            "delivery_quality": (_quality or {}).get("status"),
            "delivery_quality_measured": bool(_quality and _quality.get("coverage") in ASSESSING_COVERAGE
                                              and _quality["status"] != "not_assessed"),
            # No ethical dimension in this engine can assess a subject today: all three are word
            # lists. `assessed` says so rather than borrowing the quality figure's credibility.
            "assessed": False,
            "escalate": [d["dimension"] for d in dims if d.get("escalate")],
            "basis": ("the verdict is the worst of three word-list INDICATORS over the text — human · "
                      "environment · value — which flag for a human and never clear a subject. The "
                      "fourth dimension, quality, is measured from the QMS's own delivery figures and "
                      "is reported beside the verdict, never as one: document coverage is not ethics")}
