import sys
from types import ModuleType

# Mock missing modules globally
for mod_name in ['shap', 'jwt', 'casbin', 'alembic', 'pygit2', 'sigstore']:
    if mod_name not in sys.modules:
        mock = ModuleType(mod_name)
        sys.modules[mod_name] = mock

import pytest
from agentic_core.architecture.hox_patterns import HoxPatternRegistry
from agentic_core.architecture.phylotypic_core import PhylotypicCore
from agentic_core.governance.gene_regulatory_network import GeneRegulatoryNetwork
from agentic_core.compiler.biological_compiler import BiologicalCompiler

def test_hox_pattern_registry():
    assert HoxPatternRegistry.validate_module("test_module", "v99.0") is True

def test_phylotypic_core():
    assert PhylotypicCore.validate_stability("core_entity", 0.02) is True
    assert PhylotypicCore.validate_stability("core_entity", 0.10) is False

def test_grn_signaling():
    grn = GeneRegulatoryNetwork()
    grn.register_module("moduleA", None, receptors=["signal1"])
    grn.emit_signal("signal1", {"data": "test"}, source="moduleB")
    assert "signal1" in grn.signaling_protocols

def test_biological_compiler():
    compiler = BiologicalCompiler()
    artifact = compiler.compile("Create auth app")
    assert artifact["status"] == "DEPLOYABLE"
    assert "auth_module" in artifact["parts"]
