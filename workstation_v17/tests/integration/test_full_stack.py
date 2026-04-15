import pytest
import asyncio
from workstation_v17.core.jules_omega_organism_v17 import JulesOmegaOrganismV17
from workstation_v17.agents.c_suite_v17 import CSuiteV17
from workstation_v17.agents.coe_leads import CoELeads
from workstation_v17.agents.bto_director import BTODirector
from workstation_v17.core.vbs.bms import BusinessManagementSystem
from workstation_v17.core.vbs.qms import QualityManagementSystem
from workstation_v17.core.vbs.dcms import DocumentControlManagementSystem
from workstation_v17.core.vbs.ems import EnvironmentalManagementSystem
from workstation_v17.core.quantum.surrogate import OAM_QKDSurrogate
from workstation_v17.realms.realm_implementations import LegalRealmV17, BiofoundryRealm, ClimateRealm

@pytest.mark.asyncio
async def test_full_organism_orchestration():
    organism = JulesOmegaOrganismV17()
    await organism.initialize()

    # Test C-Suite
    c_suite = CSuiteV17()
    consensus = await c_suite.reach_consensus({"intent": "EXPAND_V17"})
    assert consensus is True

    # Test CoE Ensemble
    coe = CoELeads()
    ensemble_results = await coe.run_ensemble({})
    assert len(ensemble_results) == 4

    # Test VSB Suite
    bms = BusinessManagementSystem("workstation_v17/config/business/bms.yaml")
    econ = await bms.calculate_unit_economics(100.0, 5)
    assert econ["ROI"] > 0

    qms = QualityManagementSystem("workstation_v17/config/quality/qms.yaml")
    gate = await qms.run_quality_gates({"coverage": 0.98, "stubs_detected": False})
    assert gate is True

    dcms = DocumentControlManagementSystem("workstation_v17/config/documents/dcms.yaml")
    doc_hash = await dcms.commit_artifact("v17_spec", {"data": "secure"}, "CEO")
    assert len(doc_hash) == 128

    ems = EnvironmentalManagementSystem("workstation_v17/config/environment/ems.yaml")
    routing = await ems.optimize_routing({"energy_footprint_wh": 50})
    assert routing == "SUSTAINABLE_ACTIVE"

    # Test Quantum Surrogate
    oam = OAM_QKDSurrogate(n_modes=48)
    key_res = oam.generate_key("test_plaintext", "internal")
    assert key_res["security_metrics"]["qber_percentage"] < 5.0

    # Test Realms
    legal = LegalRealmV17()
    audit = await legal.audit_case("99", {"pattern": "neutral"})
    assert audit["compliance"] == "GREEN"

    await organism.run_macro_cycle()
    await organism.shutdown()

@pytest.mark.asyncio
async def test_bto_lifecycle():
    bms = BusinessManagementSystem("workstation_v17/config/business/bms.yaml")
    bto = BTODirector(bms)
    lifecycle = await bto.optimize_lifecycle({"energy": 10.0, "insights": 2})
    assert lifecycle["roadmap_status"] == "ACCELERATED"
