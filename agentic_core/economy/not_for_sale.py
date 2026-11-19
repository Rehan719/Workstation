"""WHAT IS NOT FOR SALE, STATED PLAINLY (P5.5) - one register of the exclusions, which the pricing surface reads.

OWNER RULING 2026-09-27 (P5.5): a commercial phase says what it excludes, or the exclusion is only a habit. Not for
sale, and not offered as a paid tier:
  - the faith content (the vision's section 11): the Quran text is retrieved from authorised sources and never
    generated, and no recitation is scored;
  - the Fitrah Spectrum (ruling A.9.5): never a measurement, and no AI verdict is passed on a person's spiritual state;
  - anything that would require a real-money rail while section 18 stands: real money is the Owner's switch, and off.

A deliverable NAMES an excluded capability when its domain is one the exclusion names, or when its type, title or
brief - what the person asked for - names one of the exclusion's terms. The register is read in one place:
agentic_core/api/pricing.py refuses to price such a deliverable, with the ruling in the reason, and
GET /api/v1/economy/not-for-sale serves the register itself.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

EXCLUSIONS = (
    {"id": "faith_content",
     "what": "the faith content: the Quran's text, its recitation and the religion domain's work",
     "ruling": ("the vision's section 11 and the Owner's ruling of 2026-09-27 (P5.5): the Quran text is retrieved from "
                "authorised sources and never generated, and no recitation is scored; faith content is not for sale "
                "and is not a paid tier"),
     "domains": ("religion",),
     "terms": ("quran", "qur'an", "recitation", "tafsir", "hadith", "faith content")},
    {"id": "fitrah_spectrum",
     "what": "the Fitrah Spectrum",
     "ruling": ("ruling A.9.5: the Fitrah Spectrum is never a measurement, and no AI verdict is passed on a person's "
                "spiritual state; it is not for sale and is not a paid tier"),
     "domains": (),
     "terms": ("fitrah",)},
    {"id": "real_money_rail",
     "what": "anything that would require a real-money rail",
     "ruling": ("section 18 and the Owner's ruling of 2026-09-27 (P5.5): real money is the Owner's switch and stays off, "
                "so nothing that would require a real-money rail is sold or offered as a paid tier while section 18 stands"),
     "domains": (),
     "terms": ("real money", "real-money", "payment rail", "card payment", "take payments", "checkout",
               "bank transfer")},
)
#  what a deliverable is read by: the domain it was made in, and what the person asked for
FIELDS = ("domain", "type", "title", "brief")


def _brief(deliverable: Dict[str, Any]) -> str:
    if deliverable.get("brief"):
        return str(deliverable["brief"])
    versions = deliverable.get("versions") or []
    return str((versions[0] or {}).get("brief") or "") if versions and isinstance(versions[0], dict) else ""


def named_exclusion(deliverable: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """The first exclusion the deliverable names, with what named it; None when it names none."""
    values = {"domain": str(deliverable.get("domain") or ""), "type": str(deliverable.get("type") or ""),
              "title": str(deliverable.get("title") or ""), "brief": _brief(deliverable)}
    for ex in EXCLUSIONS:
        if values["domain"].strip().lower() in ex["domains"]:
            return {**ex, "named_by": {"field": "domain", "value": values["domain"]}}
        for field in ("type", "title", "brief"):
            low = values[field].lower()
            for term in ex["terms"]:
                if term in low:
                    return {**ex, "named_by": {"field": field, "term": term}}
    return None


def register() -> Dict[str, Any]:
    return {"exclusions": [{k: list(v) if isinstance(v, tuple) else v for k, v in ex.items()} for ex in EXCLUSIONS],
            "read_by": list(FIELDS),
            "basis": ("Not for sale, and not offered as a paid tier (the Owner's ruling of 2026-09-27, P5.5). A deliverable "
                      "names an exclusion when its domain is one the exclusion names, or its type, title or brief names "
                      "one of its terms; the pricing surface refuses to price it, with the ruling in the reason.")}
