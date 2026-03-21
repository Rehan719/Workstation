import pytest
import asyncio
from agentic_core.layers.l1_identity.validator import validator_l1
from agentic_core.layers.l6_propagation.propagation import replication_engine
from agentic_core.layers.l11_civilisation.civilisation import mesh_controller
from agentic_core.layers.l1_identity.genome_engine import genome_engine
from agentic_core.governance.economy import economic_hub
from agentic_core.governance.dao import dao_framework

def test_autonomous_replication():
    offspring_id = replication_engine.spawn_offspring("hardware-node-infinity")
    assert "did:vsb:offspring-" in offspring_id
    assert replication_engine.certify_offspring(offspring_id) == True

def test_inter_civilization_diplomacy():
    alliance_id = mesh_controller.establish_alliance("did:external:alpha-system", {"trade": "WST"})
    assert "alliance-" in alliance_id
    status = mesh_controller.get_mesh_status()
    assert status["alliances"] >= 1
    assert status["p99_latency_ms"] < 20

def test_infinite_adaptation_self_healing():
    initial_article_count = len(genome_engine.genome["constitution"]["articles"])
    genome_engine.run_self_healing_cycle("high_latency_detected")

    # Check for autonomous amendment
    new_count = len(genome_engine.genome["constitution"]["articles"])
    assert new_count > initial_article_count

    # Test Rollback
    genome_engine.rollback()
    assert len(genome_engine.genome["constitution"]["articles"]) == initial_article_count

def test_economic_independence():
    status = economic_hub.get_economy_status()
    assert status["financials"]["independence_certified"] == True
    assert status["enterprise_users"] >= 100

def test_eternal_ai_led_governance():
    report = dao_framework.get_governance_report()
    assert "AI-LED" in report["mode"]
    assert report["self_healing"] == "Active"

def test_floor_24_eternal_gaas():
    # Article 1115: Lineage required
    res = validator_l1.validate_action("spawn_offspring", {"lineage_registered": False})
    assert res["valid"] == False

    # Article 1118: Trust threshold
    validator_l1.trust_factors["default"] = 0.5
    res = validator_l1.validate_action("amend_constitution", {"self_healing_trigger": False})
    assert res["valid"] == False

if __name__ == "__main__":
    test_autonomous_replication()
    test_inter_civilization_diplomacy()
    test_infinite_adaptation_self_healing()
    test_economic_independence()
    test_eternal_ai_led_governance()
    test_floor_24_eternal_gaas()
    print("v3.0 Recombinant Phase 4 Eternal Sovereignty Tests PASSED.")
