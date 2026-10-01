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

from agentic_core.cognitive.registry import (CognitiveEngineRegistry, ENGINE_TIERS, EngineTier,
                                             EngineType)

# EngineType value -> (module, class). Only engines with a module appear here.
_IMPLEMENTED = {
    EngineType.AQAL: ("agentic_core.cognitive.aqal_engine", "AqalEngine"),
    EngineType.HOSHIYARI: ("agentic_core.cognitive.hoshiyari_engine", "HoshiyariEngine"),
    EngineType.IMAN: ("agentic_core.cognitive.iman_engine", "ImanEngine"),
    EngineType.INKASHAF: ("agentic_core.cognitive.inkashaf_engine", "InkashafEngine"),
    EngineType.SAMAJH: ("agentic_core.cognitive.samajh_engine", "SamajhEngine"),
    EngineType.SOCH: ("agentic_core.cognitive.soch_engine", "SochEngine"),
    # ── meta-regulative (P3.13). These COMPUTE — a Pareto frontier, a quorum counted from the signatures
    #    supplied, and drift against a recorded baseline — or refuse with a stated basis. They are NOT in
    #    the cascade: they are regulative, consumed by the clearance chain (P3.14), which is why
    #    `engines_run` stays 6 on /cascade after this.
    EngineType.TAWAZUN: ("agentic_core.cognitive.meta.tawazun_engine", "TawazunEngine"),
    EngineType.NIYYAH: ("agentic_core.cognitive.meta.niyyah_engine", "NiyyahEngine"),
    EngineType.TAFAKKUR: ("agentic_core.cognitive.meta.tafakkur_engine", "TafakkurEngine"),
    # ── auxiliary (P3.16, architecture doc C6). Two of the three sit behind clearance-chain gates that
    #    W525 taught to refuse: Mushawara is gate 1, which previously RAISED on a missing field, and
    #    Tahqeeq is gate 5, which approved on one. Mudrik bridges a cleared emission to Change Control and
    #    refuses to carry an uncleared one. NOT in the cascade: the cascade runs the six foundational
    #    engines, which is why engines_run stays 6.
    EngineType.TAHQEEQ: ("agentic_core.cognitive.auxiliary.tahqeeq_engine", "TahqeeqEngine"),
    EngineType.MUSHAWARA: ("agentic_core.cognitive.auxiliary.mushawara_engine", "MushawaraEngine"),
    EngineType.MUDRIK: ("agentic_core.cognitive.auxiliary.mudrik_engine", "MudrikEngine"),
}

#  One reason per TIER, because the four unbuilt tiers are in four different situations and a single
#  sentence across all of them would be false for three. Each says what exists today, not just what is planned.
_ABSENT_BASIS_BY_TIER = {
    EngineTier.META: ("declared in EngineType and has NO module: agentic_core/cognitive/meta/ holds only an "
                      "__init__.py. Built by P3.13 as a refusal by default. The archived version at "
                      "_archive/jules-unwired/ is NOT recovered: all three fabricate (a graded balance score, "
                      "three invented signatories, a hardcoded drift with its formula in a comment)"),
    EngineTier.AUXILIARY: ("declared in EngineType and has NO module. Built by P3.16. Mushawara is gate 1 of "
                           "the clearance chain, which currently calls it through an orchestrator the avatar "
                           "API bypasses, so nothing consults it even where it is named"),
    EngineTier.MJM: ("declared in EngineType and has no engine module: Mushahida, Jaiza and Muaina exist "
                     "today as METHODS on MJMOrchestratorV4, which the Owner ruled stays as their composer "
                     "(2026-09-30). Two of the three fabricate as methods - a hardcoded entropy and a "
                     "compliance of 1.0 - so registering them is not the same as making them honest"),
    EngineTier.BME: ("declared in EngineType and has no registered module. Built by P3.17. Its state is "
                     "mixed rather than absent: entropic optimal transport has LIVE code with no solver "
                     "(POT is not installed), the Omega-functional and Schrodinger bridge are archived, the "
                     "diffusion process needs torchsde which is not installed, and the Landauer meter "
                     "already exists at core/transcendent_subsystems/tfel.py fed hardcoded bit counts"),
}


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

    absent = [e for e in EngineType if e not in _IMPLEMENTED]
    declared_absent = sorted(e.value for e in absent)

    #  Per tier, so a reader can see WHERE the gap is rather than only how big it is. Before the Owner's
    #  2026-09-30 rulings this enum declared nine of twenty-three and the whole auxiliary tier was missing,
    #  so "6 of 9" read as near-complete coverage of a set it could not describe.
    by_tier = {}
    for _t in EngineTier:
        _members = [e for e in EngineType if ENGINE_TIERS.get(e) == _t]
        _reg = [e.value for e in _members if e.value in registered]
        by_tier[_t.value] = {
            "declared": len(_members),
            "registered": len(_reg),
            "registered_names": sorted(_reg),
            "absent": sorted(e.value for e in _members if e.value not in registered),
        }

    return {
        "registered": sorted(registered),
        "registered_count": len(registered),
        "unavailable": unavailable,
        "declared_but_absent": declared_absent,
        "declared_but_absent_basis": {
            e.value: _ABSENT_BASIS_BY_TIER.get(
                ENGINE_TIERS.get(e),
                "declared in EngineType, absent, and in no tier - which is itself a defect: see ENGINE_TIERS")
            for e in absent},
        "engine_type_declares": len(list(EngineType)),
        "by_tier": by_tier,
        "tiers_declared": [t.value for t in EngineTier],
        "basis": (f"{len(registered)} of {len(list(EngineType))} declared engines have a module and are "
                  f"registered; {len(declared_absent)} are declared and absent, across "
                  f"{sum(1 for v in by_tier.values() if v['absent'])} of {len(by_tier)} tiers"
                  + (f"; {len(unavailable)} failed to import" if unavailable else "")),
        "what_the_denominator_means": (
            f"{len(list(EngineType))} is what the ARCHITECTURE declares, not what works. Only the "
            f"{by_tier[EngineTier.FOUNDATIONAL.value]['registered']} foundational engines have modules, and "
            "each of those returns a fixed marker with confidence=None rather than computing"),
        "what_registration_does_not_mean": ("registration is not computation, and the two registered tiers "
                                            "differ: the six FOUNDATIONAL engines return a fixed marker with "
                                            "confidence=None because they have no path to a model (FU-275), "
                                            "while the three META engines (P3.13) genuinely compute their "
                                            "named quantity - a Pareto frontier, a quorum counted from the "
                                            "signatures supplied, drift against a recorded baseline - or "
                                            "refuse with a stated basis, and so do the three AUXILIARY "
                                            "engines (P3.16). None of them reports a confidence, because "
                                            "none of them estimates: a frontier, a quorum, a drift, a "
                                            "constraint check and a consensus are all computations over "
                                            "the inputs supplied"),
    }
