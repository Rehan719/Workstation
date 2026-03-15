import pytest
from agentic_core.realms.learner_realm_v137 import LearnerRealmV137

def test_v137_pacing_adaptation():
    realm = LearnerRealmV137()
    # High speed, high accuracy
    interaction = {"response_speed_ms": 500, "accuracy": 0.95}
    result = realm.process_interaction("user_1", interaction)
    assert result["pacing_adjustment"] == "INCREASE_CHALLENGE"

    # Low accuracy
    interaction = {"response_speed_ms": 1000, "accuracy": 0.5}
    result = realm.process_interaction("user_1", interaction)
    assert result["pacing_adjustment"] == "DECREASE_CHALLENGE"

def test_v137_knowledge_garden_blooming():
    realm = LearnerRealmV137()
    # Incrementally master concept
    realm.update_mastery("user_2", "PID_Control", 0.6)
    result = realm.update_mastery("user_2", "PID_Control", 0.5)

    assert result["progress"] == 1.0
    assert result["bloomed"] == True
    assert "PID_Control" in realm.get_garden_visuals("user_2")
