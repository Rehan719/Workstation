import pytest
from realms.learner_realm_v137 import LearnerRealmV137

def test_v137_pacing_adaptation():
    realm = LearnerRealmV137()
    # High engagement (needs decrease challenge?) per spec logic:
    # if engagement > 0.8: action = "DECREASE_CHALLENGE"
    interaction = {"avg_response_time": 500, "quiz_accuracy": 0.95}
    result = realm.adapt_pace("user_1", interaction)
    assert result["pacing_action"] == "DECREASE_CHALLENGE"

    # Low engagement
    interaction = {"avg_response_time": 6000, "quiz_accuracy": 0.5}
    result = realm.adapt_pace("user_1", interaction)
    assert result["pacing_action"] == "INCREASE_CHALLENGE"

def test_v137_garden_bloom():
    realm = LearnerRealmV137()
    result = realm.grow_garden("user_2", "PID_Control")
    assert result["visual_event"] == "FLOWER_BLOOM"

def test_idbo_needs_implementation():
    realm = LearnerRealmV137()
    assert realm.calculate_contentment("idbo-1") > 0.9

    rest = realm.initiate_rest_protocol("idbo-1")
    assert rest["notifications"] == "silenced"

    play = realm.provide_play_activities("idbo-1")
    assert "virtual_art_studio" in play
