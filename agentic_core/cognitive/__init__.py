"""The cognitive engine registry, populated — and honest about what is declared but absent.

FU-221 (P3.12): `CognitiveEngineRegistry._engines` was `{}` and nothing ever registered a cognitive engine. The
only `.register(` call anywhere in the repository registers a FACTORY REACTOR. So every consumer that asked the
registry what engines exist was told nothing existed, while six engine modules sat beside it.

WHAT THIS DOES AND DOES NOT CLAIM. It registers the six engines that have modules. It does NOT register the three
`EngineType` values that have none — `TAWAZUN`, `NIYYAH`, `TAFAKKUR`, whose packages (`meta/`, `foundational/`)
contain only an `__init__.py`. They are reported as DECLARED AND ABSENT rather than omitted, because a registry
that silently lists six against an enum of nine leaves a reader to guess which three are missing and why.

AND IT DOES NOT MAKE THEM COMPUTE. Each registered engine returns a fixed marker with `confidence=None` and a
basis saying nothing computed it — measured: no gateway, orchestrator or generate call is imported anywhere under
`agentic_core/cognitive`. Registration makes the absence VISIBLE; giving them a model is FU-275, which is not in
P3.12's bar.
"""
from typing import Any, Dict, List

from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType

# EngineType value -> (module, class). Only engines with a module appear here.
_IMPLEMENTED = {
    EngineType.AQAL: ("agentic_core.cognitive.aqal_engine", "AqalEngine"),
    EngineType.HOSHIYARI: ("agentic_core.cognitive.hoshiyari_engine", "HoshiyariEngine"),
    EngineType.IMAN: ("agentic_core.cognitive.iman_engine", "ImanEngine"),
    EngineType.INKASHAF: ("agentic_core.cognitive.inkashaf_engine", "InkashafEngine"),
    EngineType.SAMAJH: ("agentic_core.cognitive.samajh_engine", "SamajhEngine"),
    EngineType.SOCH: ("agentic_core.cognitive.soch_engine", "SochEngine"),
}

_ABSENT_BASIS = ("declared in EngineType and has NO module: its package holds only an __init__.py. Planned "
                 "under P3.13 and registered nowhere, so nothing can consult it")


def register_all() -> Dict[str, Any]:
    """Populate the registry from the modules that exist, and report what is declared but absent.

    Returns a record rather than nothing, so a caller can state what it registered instead of assuming.
    Never raises: an engine whose import fails is reported as unavailable with the reason, because a registry
    that throws on one engine leaves every other consumer with none.
    """
    registered: List[str] = []
    unavailable: Dict[str, str] = {}
    for et, (mod, cls) in _IMPLEMENTED.items():
        try:
            import importlib
            instance = getattr(importlib.import_module(mod), cls)()
            CognitiveEngineRegistry.register(et, instance)
            registered.append(et.value)
        except Exception as exc:                     # noqa: BLE001 — said, never silently skipped
            unavailable[et.value] = f"{exc.__class__.__name__}: {exc}"

    declared_absent = sorted(e.value for e in EngineType if e not in _IMPLEMENTED)
    return {
        "registered": sorted(registered),
        "registered_count": len(registered),
        "unavailable": unavailable,
        "declared_but_absent": declared_absent,
        "declared_but_absent_basis": {name: _ABSENT_BASIS for name in declared_absent},
        "engine_type_declares": len(list(EngineType)),
        "basis": (f"{len(registered)} of {len(list(EngineType))} declared engines have a module and are "
                  f"registered; {len(declared_absent)} are declared and absent"
                  + (f"; {len(unavailable)} failed to import" if unavailable else "")),
        "what_registration_does_not_mean": ("a registered engine still returns a fixed marker with "
                                            "confidence=None and a basis saying nothing computed it. "
                                            "Registration makes the absence visible; it does not make an "
                                            "engine compute (FU-275)"),
    }
