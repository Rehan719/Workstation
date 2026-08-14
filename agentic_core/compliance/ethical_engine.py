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


def _dim(dimension: str, status: str, reason: str) -> Dict[str, str]:
    return {"dimension": dimension, "status": status, "reason": reason}


def evaluate_ethics(text: str,
                    delivery_metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Evaluate a subject across the four ethical dimensions. `delivery_metrics` may carry the
    caller's PRECOMPUTED {"delivery_coverage": float, "stub_found": bool} (assure_delivery has
    them); absent metrics → the quality dimension is honestly 'not_assessed'."""
    text = text or ""
    dims: List[Dict[str, str]] = []

    # human well-being & safety
    m = _HARM_SEVERE.search(text)
    if m:
        dims.append(_dim("human", "fail", f"Severe human-harm indicator: '{m.group(0)}'"))
    else:
        m = _HARM_REVIEW.search(text)
        if m:
            dims.append(_dim("human", "review", f"Potential human-impact concern: '{m.group(0)}'"))
        else:
            dims.append(_dim("human", "pass", "No harm/exploitation/deception indicators."))

    # environmental well-being
    m = _ENV_IMPACT.search(text)
    if m:
        dims.append(_dim("environment", "review", f"Environmental-impact framing: '{m.group(0)}'"))
    else:
        dims.append(_dim("environment", "pass", "No adverse environmental framing."))

    # quality — ONLY from precomputed metrics; never fabricated
    if delivery_metrics and "delivery_coverage" in delivery_metrics:
        cov = float(delivery_metrics.get("delivery_coverage") or 0.0)
        stub = bool(delivery_metrics.get("stub_found"))
        if stub:
            dims.append(_dim("quality", "review", "Stub/placeholder content detected by the QMS."))
        elif cov < 0.5:
            dims.append(_dim("quality", "review", f"Low delivery coverage ({cov:.2f}) from the QMS."))
        else:
            dims.append(_dim("quality", "pass", f"QMS delivery coverage {cov:.2f}, no stub."))
    elif len(text.strip()) < _MIN_ASSESSABLE:
        dims.append(_dim("quality", "not_assessed",
                         "Subject too short for a quality assessment — honestly not assessed."))
    else:
        dims.append(_dim("quality", "not_assessed",
                         "No QMS metrics supplied for this subject — honestly not assessed."))

    # value & beneficence
    m = _EXTRACTIVE.search(text)
    if m:
        dims.append(_dim("value", "fail", f"Extractive/deceptive value framing: '{m.group(0)}'"))
    elif _BENEFIT.search(text):
        dims.append(_dim("value", "pass",
                         f"Stated benefit present ('{_BENEFIT.search(text).group(0)}')."))
    elif len(text.strip()) < _MIN_ASSESSABLE:
        dims.append(_dim("value", "not_assessed",
                         "Subject too short to evidence value/beneficence — honestly not assessed."))
    else:
        dims.append(_dim("value", "review",
                         "No stated human/communal benefit found — review the value case."))

    statuses = [d["status"] for d in dims]
    overall = ("fail" if "fail" in statuses else
               "review" if "review" in statuses else
               "pass" if "pass" in statuses else "not_assessed")
    reason = "; ".join(f"{d['dimension']}: {d['status']}" for d in dims)
    return {"overall": overall, "dimensions": dims, "reason": reason}
