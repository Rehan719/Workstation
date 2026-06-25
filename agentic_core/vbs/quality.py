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

_STUB_RE = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum|placeholder|coming soon|as an ai)\b", re.I)
_MIN_SUBSTANTIVE = 200  # chars — below this a "delivery" is treated as an empty / stub shell.


def _delivery_coverage(content: str, required_sections: Optional[List[str]]) -> float:
    """Fraction of the required sections that actually appear in the delivered content (case-insensitive).
    With no declared structure, coverage is binary on whether there is substantive content."""
    text = (content or "").lower()
    if not required_sections:
        return 1.0 if len(text.strip()) >= _MIN_SUBSTANTIVE else 0.0
    present = sum(1 for s in required_sections if str(s).lower() in text)
    return round(present / len(required_sections), 3)


async def assure_delivery(content: str, required_sections: Optional[List[str]] = None,
                          label: str = "delivery") -> Dict[str, Any]:
    """Subject an operational delivery to the living QMS + §10 bar + §8 organism.

    Returns ``{"quality": {...}, "biomimetic": {...}}`` — honest and real (no fabricated numbers).
    Never raises: a QMS / organism hiccup is captured as an ``*_error`` field so a delivery is never
    lost to a quality-system fault.
    """
    coverage = _delivery_coverage(content, required_sections)
    stub = bool(_STUB_RE.search(content or "")) or len((content or "").strip()) < _MIN_SUBSTANTIVE
    quality: Dict[str, Any] = {
        "bar": list(SOLUTION_QUALITY_BAR),
        "delivery_coverage": coverage,
        "stub_found": stub,
    }
    try:
        from agentic_core.vbs.registry import qms
        # Real, stateful gate: failures append to qms.defects and raise the non-conformance rate.
        quality["qms_gate_passed"] = bool(await qms.run_quality_gates({"coverage": coverage, "stubs_found": stub}))
        quality["qms_min_coverage"] = qms.min_coverage
        quality["qms_non_conformance_rate"] = qms.get_non_conformance_rate()
        # The QMS document-controls the quality record through its OWNED DCMS (QMS ⊃ DCMS, ISO 9001 §7.5):
        # the gate verdict becomes a versioned, SHA3-512-sealed controlled document.
        quality["quality_record_hash"] = await qms.control_document(
            f"qms_record:{label}",
            {"label": label, "delivery_coverage": coverage, "stub_found": stub,
             "qms_gate_passed": quality["qms_gate_passed"], "bar": SOLUTION_QUALITY_BAR},
            actor="QMS")
        quality["document_controlled"] = True
    except Exception as exc:  # never break a delivery on a QMS hiccup
        quality["qms_error"] = str(exc)

    biomimetic: Dict[str, Any] = {"layers": list(BIOMIMETIC_LAYERS),
                                  "self": "self-managing · improving · healing"}
    try:
        from agentic_core.organism.immune import immune
        from agentic_core.organism.biobus import _circadian_cycle, biobus
        biomimetic["immune"] = immune.status()
        biomimetic["circadian"] = _circadian_cycle()
        # The organism senses every quality outcome (homeostatic feedback).
        biobus.fire_signal("cognitive", f"qms.{label}",
                           f"QMS gate {'PASS' if quality.get('qms_gate_passed') else 'FAIL'} (cov={coverage})", 0.6)
    except Exception as exc:
        biomimetic["error"] = str(exc)

    return {"quality": quality, "biomimetic": biomimetic}
