import pytest
import asyncio
from workstation_v17.core.jules_omega_organism_v17 import JulesOmegaOrganismV17
from workstation_v17.agents.c_suite_v17 import CSuiteV17
from workstation_v17.agents.coe_leads import CoELeads
from workstation_v17.agents.bto_director import BTODirector
from workstation_v17.core.vsb.bms import BusinessManagementSystem
from workstation_v17.core.vsb.qms import QualityManagementSystem
from workstation_v17.core.vsb.dms import DocumentControlSystem
from workstation_v17.core.vsb.ems import EnvironmentalManagementSystem
from workstation_v17.core.quantum.surrogate import ClassicalOAMQKDSurrogate
from workstation_v17.realms.legal_realm_v17 import LegalRealmV17
from workstation_v17.realms.biofoundry_realm import BiofoundryRealm
from workstation_v17.realms.climate_realm import ClimateRealm

@pytest.mark.asyncio
async def test_full_organism_orchestration():
    organism = JulesOmegaOrganismV17()
    await organism.initialize()

    # Test C-Suite
    c_suite = CSuiteV17()
    consensus = await c_suite.get_consensus("EXPAND_V17", {"cycle": 1})
    assert consensus["verdict"] == "PROCEED"

    # Test CoE Ensemble
    coe = CoELeads()
    ensemble_results = await coe.run_ensemble({})
    assert len(ensemble_results) == 3

    # Test VSB Suite
    bms = BusinessManagementSystem("config/business/bms.yaml")
    econ = await bms.calculate_unit_economics({"energy_wh": 100, "insights": 5})
    assert econ["ROI"] > 0

    qms = QualityManagementSystem("config/quality/qms.yaml")
    gate = await qms.run_quality_gates({"test_coverage": 0.98, "placeholder_check": False})
    assert gate["coverage_gate"] is True

    dms = DocumentControlSystem("config/documents/dms.yaml")
    doc_hash = await dms.commit_artifact("v17_spec", {"data": "secure"}, "CEO")
    assert len(doc_hash) == 128

    ems = EnvironmentalManagementSystem("config/environment/ems.yaml")
    routing = await ems.route_task({}, {"total_energy_wh": 50})
    assert routing == "BALANCED"

    # Test Quantum Surrogate
    oam = ClassicalOAMQKDSurrogate(n_modes=48)
    key_res = await oam.generate_secure_key(64)
    assert key_res["validation"] == "PASSED"

    # Test Realms
    legal = LegalRealmV17()
    audit = await legal.audit_case({"worker_id": "99"})
    assert audit["compliance"] == "CERTIFIED"

    await organism.run_macro_cycle({"trigger": "TEST"})
    await organism.shutdown()

@pytest.mark.asyncio
async def test_bto_lifecycle():
    bms = BusinessManagementSystem("config/business/bms.yaml")
    bto = BTODirector(bms)
    lifecycle = await bto.evaluate_lifecycle({"energy_wh": 10, "insights": 2, "truth_score": 0.99})
    assert lifecycle["action"] == "EXPAND"
