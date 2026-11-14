"""W899 (FU-610) - WHAT AN EXTERNAL CALL CARRIES, declared and checked before anything leaves.

Every reply already said THAT it left the platform (is_external), and the Owner's switch (AI_ALLOW_EXTERNAL) gates
the call. Nothing said WHAT CLASS of data it carried. So with the switch on, a call could say it was external and
could not say whether it carried a person's words or the live legal matter, and no class could be barred from
leaving. This is that half of the switch's pre-flight (P4.3). The switch itself stays the Owner's.

  * A caller that can ask for an external model declares the class of what it sends.
  * The check runs where the provider's client would be built, so a refusal transmits nothing. A refusal is a
    SKIP, like the hourly cap's: the next resource or the floor serves, and nothing is recorded against the
    provider, because it did not fail.
  * A call that declares nothing is not sent: an external call must say what it carries.
  * The first barred class is the Owner's ruling of 2026-10-03c: the legal-matter folder is never sent to any
    external service. A call that declares it is not sent. Nor is any call that read a document from the folder,
    whatever it declared: the folder's one reader marks the call (agentic_core/legal/bundle.py).
  * The reply says what was declared and what each check decided.

Which other classes are barred is the Owner's to say (docs/REMAINING_WORK_MEASURED.md, P4.3)."""
from __future__ import annotations

import contextlib
import contextvars
from typing import Any, Dict, Iterator, List, Optional

#  the classes a caller may declare, and what each one is
CLASSES: Dict[str, str] = {
    "person_entered": ("what a person typed for this request, or saved in a design they run, with the platform's "
                       "own instructions and records composed around it"),
    "legal_matter": "text read from the live legal matter's one named folder, or composed from it",
}

#  the classes that never leave the platform, each with the ruling that bars it
BARRED: Dict[str, str] = {
    "legal_matter": ("the Owner's ruling of 2026-10-03c: the legal-matter folder is never sent to any external "
                     "service"),
}

_DECLARED: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("w899_data_class", default=None)
_LEGAL_READ: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("w899_legal_matter_read", default=None)


@contextlib.contextmanager
def declared(data_class: Optional[str]) -> Iterator[None]:
    """Declare the class of what the enclosed calls send. None keeps an outer declaration."""
    if data_class is None:
        yield
        return
    token = _DECLARED.set(str(data_class))
    try:
        yield
    finally:
        _DECLARED.reset(token)


def current() -> Optional[str]:
    """The class declared for this call, or None."""
    return _DECLARED.get()


def mark_legal_matter_read(document: str) -> None:
    """Called by the legal folder's one reader for every document it opens. Nothing this call sends after it leaves
    the platform. Each request runs in its own context, so the mark ends with the request that read the document."""
    _LEGAL_READ.set(str(document or "a document"))


def preflight(provider: str, data_class: Optional[str] = None) -> Dict[str, Any]:
    """Whether `provider` may be sent this call's material. Decided before its client is built."""
    cls = data_class if data_class is not None else _DECLARED.get()
    legal = _LEGAL_READ.get()
    if legal is not None:
        return {"provider": provider, "declared": cls, "send": False, "barred_class": "legal_matter",
                "why": (f"not sent: this call read {legal!r} from the legal matter's folder, and "
                        f"{BARRED['legal_matter']}")}
    if cls is None:
        return {"provider": provider, "declared": None, "send": False, "barred_class": None,
                "why": "not sent: the call declared no data class, and an external call must say what it carries"}
    if cls not in CLASSES:
        return {"provider": provider, "declared": cls, "send": False, "barred_class": None,
                "why": (f"not sent: {cls!r} is not a data class this platform names "
                        f"({', '.join(sorted(CLASSES))})")}
    if cls in BARRED:
        return {"provider": provider, "declared": cls, "send": False, "barred_class": cls,
                "why": f"not sent: {cls} is barred from leaving the platform - {BARRED[cls]}"}
    return {"provider": provider, "declared": cls, "send": True, "barred_class": None,
            "why": f"sent: the call declared {cls}, which is not barred"}


def provenance(data_class: Optional[str], checks: List[Dict[str, Any]], is_external: bool) -> Dict[str, Any]:
    """What a reply says about the class of what it carried: what was declared, and what each check decided."""
    cls = data_class if data_class is not None else _DECLARED.get()
    if is_external:
        external = "sent"
    elif any(not c.get("send") for c in checks):
        external = "refused before transmission"
    else:
        external = "not attempted"
    return {"declared": cls, "class_basis": CLASSES.get(cls) if cls else None,
            "legal_matter_read": _LEGAL_READ.get() is not None,
            "external": external, "checks": [dict(c) for c in checks],
            "barred": sorted(BARRED)}
