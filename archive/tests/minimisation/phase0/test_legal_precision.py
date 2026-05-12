import pytest
from agentic_core.legal.types import TribunalTask, LegalAgent
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl

def test_uklpe_assignment_validation():
    engine = UKLegalPrecisionEngineImpl(rules_path="non_existent.yaml")

    tasks = [
        TribunalTask(id="T1", statute="EqualityAct2010", claim_type="discrimination", priority=1.0, jurisdiction="England_Wales"),
        TribunalTask(id="T2", statute="ERA1996", claim_type="unfair_dismissal", priority=1.0, jurisdiction="Scotland")
    ]

    agents = [
        LegalAgent(id="A1", competencies=["EqualityAct2010"], available_capacity=1.0, jurisdiction="England_Wales"),
        LegalAgent(id="A2", competencies=["ERA1996"], available_capacity=1.0, jurisdiction="Scotland")
    ]

    # Correct assignment
    assignment_ok = {"T1": "A1", "T2": "A2"}
    coverage_ok = engine.validate_assignment(assignment_ok, tasks, agents)
    assert coverage_ok == 1.0

    # Incorrect assignment (jurisdiction mismatch A1 is Eng, T2 is Scot)
    assignment_bad = {"T1": "A2", "T2": "A1"}
    coverage_bad = engine.validate_assignment(assignment_bad, tasks, agents)
    assert coverage_bad == 0.0

def test_uklpe_agent_covers_statute():
    engine = UKLegalPrecisionEngineImpl(rules_path="non_existent.yaml")
    agent = LegalAgent(id="A1", competencies=["EqualityAct2010"], available_capacity=1.0, jurisdiction="England_Wales")
    assert engine.agent_covers_statute(agent, "EqualityAct2010")
    assert not engine.agent_covers_statute(agent, "ERA1996")

def test_uklpe_validate_intent_mismatch():
    engine = UKLegalPrecisionEngineImpl(rules_path="non_existent.yaml")
    intent = {"jurisdiction": "Scotland"}
    context = {"required_statutes": ["EqualityAct2010"], "jurisdiction": "England_Wales"}
    res = engine.validate(intent, context)
    assert not res.is_compliant
    assert any("JURISDICTION_MISMATCH" in v for v in res.violations)
    assert res.coverage_score < 1.0

def test_uklpe_validate_assignment_missing():
    engine = UKLegalPrecisionEngineImpl(rules_path="non_existent.yaml")
    assert engine.validate_assignment({}, [], []) == 1.0

    tasks = [TribunalTask(id="T1", statute="EA", claim_type="disc", priority=1.0)]
    assert engine.validate_assignment({"T1": "A-MISSING"}, tasks, []) == 0.0
