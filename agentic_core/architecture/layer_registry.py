from typing import Dict, Any

# agentic_core/architecture/layer_registry.py
# HISTORICAL (W781, FU-1096) - this is the 14-layer table of a Jules-era document, kept because
# governance/uci_interceptor.py builds the manager in enriched_layers.py that reads it. It is NOT the
# architecture: the SEVEN layers are the canon (docs/WORKSTATION_IDBO_WHOLE_VISION.md). Many module paths
# below do not exist; `exists` is read from the tree at import, never assumed.
import pathlib as _pl

LAYER_SPEC = {
    0: {"name": "Substrate Attestation", "module": "agentic_core/substrate/attestation.py", "required": True},
    1: {"name": "Identity", "module": "agentic_core/layers/l1_identity/", "required": True},
    2: {"name": "Hardware", "module": "agentic_core/layers/l2_hardware/", "required": True},
    3: {"name": "Expression", "module": "agentic_core/layers/l3_expression/", "required": True},
    4: {"name": "Regulation", "module": "agentic_core/layers/l4_regulation/", "required": True},
    5: {"name": "Resilience", "module": "agentic_core/layers/l5_resilience/", "required": True},
    6: {"name": "Propagation", "module": "agentic_core/layers/l6_propagation/", "required": False},
    7: {"name": "Module Library", "module": "agentic_core/layers/l7_module_library/", "required": False},
    8: {"name": "Recombination", "module": "agentic_core/layers/l8_recombination/", "required": False},
    9: {"name": "Orchestration", "module": "agentic_core/layers/l9_orchestration/", "required": True},
    10: {"name": "Evolution", "module": "agentic_core/layers/l10_evolution/", "required": False},
    11: {"name": "Civilisation", "module": "agentic_core/layers/l11_civilisation/", "required": False},
    12: {"name": "User Experience", "module": "agentic_core/layers/l12_ux/", "required": False},
    13: {"name": "Civilizational Reflection", "module": "agentic_core/layers/l13_civilizational_reflection/", "required": True},
}

_ROOT = _pl.Path(__file__).resolve().parents[2]
for _spec in LAYER_SPEC.values():
    _spec["exists"] = (_ROOT / _spec["module"]).exists()
HISTORICAL = True
CANON_LAYERS = 7


def get_layer_metadata(layer_id: int) -> Dict[str, Any]:
    return LAYER_SPEC.get(layer_id, {"name": f"Layer {layer_id}", "module": "unknown", "required": False})
