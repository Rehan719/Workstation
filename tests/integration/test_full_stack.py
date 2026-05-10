import pytest
import asyncio
from agentic_core.organism.jules_omega_organism_v138 import JulesOmegaOrganismV138
from agentic_core.agents.c_suite_v138 import CSuiteV138
from agentic_core.agents.coe_leads import CoELeads
from agentic_core.agents.bto_director import BTODirector
from agentic_core.vbs.bms import BusinessManagementSystem
from agentic_core.vbs.qms import QualityManagementSystem
from agentic_core.vbs.dcms import DocumentControlManagementSystem
from agentic_core.vbs.ems import EnvironmentalManagementSystem
from agentic_core.quantum.surrogate import OAM_QKDSurrogate
from agentic_core.realms.legal_realm_v138 import LegalRealmV138
from agentic_core.realms.biofoundry_realm import BiofoundryRealm
from agentic_core.realms.climate_realm import ClimateRealm

@pytest.mark.asyncio
async def test_full_organism_orchestration():
    organism = JulesOmegaOrganismV138()
    await organism.initialize()

    # Test C-Suite
    c_suite = CSuiteV138()
    consensus = await c_suite.reach_consensus("EXPAND_V138")
    assert consensus is True

    # Test CoE Ensemble
    coe = CoELeads()
    ensemble_results = await coe.run_ensemble({})
    assert len(ensemble_results) == 4

    # Test VSB Suite
    bms = BusinessManagementSystem("configs/business/bms.yaml")
    econ = await bms.calculate_unit_economics(5, 100.0)
    assert econ["roi"] > 0

    qms = QualityManagementSystem("configs/quality/qms.yaml")
    gate = await qms.run_quality_gates({"coverage": 0.98, "stubs_found": False})
    assert gate is True

    dcms = DocumentControlManagementSystem("configs/documents/dcms.yaml")
    doc_hash = await dcms.commit_artifact("v138_spec", {"data": "secure"}, "CEO")
    assert len(doc_hash) == 128

    ems = EnvironmentalManagementSystem("configs/environment/ems.yaml")
    gain = ems.get_resource_gain()
    assert gain >= 0.20

    # Test Quantum Surrogate
    oam = OAM_QKDSurrogate(n_modes=48)
    key_res = oam.generate_key("test_plaintext", "internal")
    assert key_res["security_metrics"]["qber_percentage"] < 5.0

    # Test Realms
    legal = LegalRealmV138()
    audit = await legal.audit_case("99", {"pattern": "neutral"})
    assert audit["compliance"] == "GREEN"

    await organism.run_macro_cycle()
    await organism.shutdown()

@pytest.mark.asyncio
async def test_bto_lifecycle():
    bms = BusinessManagementSystem("configs/business/bms.yaml")
    bto = BTODirector(bms)
    lifecycle = await bto.optimize_lifecycle({"insights": 2, "energy": 10.0})
    assert lifecycle["roadmap"] == "ACCELERATED"
