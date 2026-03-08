import pytest
from agentic_core.religious_domain.tajwid.coach import TajwidCoach
from agentic_core.religious_domain.memorization.engine import MemorizationEngine
from agentic_core.religious_domain.guidance.assistant import AIGuidance
from agentic_core.religious_domain.governance.middleware import DualMetricMiddleware
from agentic_core.religious_domain.finops.sharia_finops import IslamicFinanceAdapter
from unittest.mock import MagicMock

def test_tajwid_coach_analysis():
    coach = TajwidCoach(qiraat="Hafs")
    # Test perfect match
    ref = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
    res = coach.analyze_recitation(ref, ref)
    assert res["is_correct"] is True
    assert res["accuracy"] > 0.99

    # Test mismatch
    res_bad = coach.analyze_recitation(ref, "Wrong text")
    assert res_bad["is_correct"] is False
    assert res_bad["accuracy"] < 0.7

def test_memorization_srs_logic():
    engine = MemorizationEngine()
    # Quality 5 (Perfect recall), first time
    interval, ef = engine.calculate_next_review(quality=5, repetitions=0, previous_interval=0, previous_efactor=2.5)
    assert interval == 1
    assert ef > 2.5

    # Quality 5, second time
    interval_2, ef_2 = engine.calculate_next_review(quality=5, repetitions=1, previous_interval=1, previous_efactor=ef)
    assert interval_2 == 6
    assert ef_2 > ef

    # Quality 0 (Total blackout)
    interval_0, ef_0 = engine.calculate_next_review(quality=0, repetitions=5, previous_interval=30, previous_efactor=2.5)
    assert interval_0 == 1
    assert ef_0 < 2.5

def test_ai_guidance_escalation():
    scholar_board = MagicMock()
    guidance = AIGuidance(scholar_board)

    # Normal recommendation
    res_norm = guidance.get_recommendation({"tazkiyah_score": 60.0})
    assert res_norm["status"] == "SUCCESS"

    # Sensitive query escalation
    res_esc = guidance.get_recommendation({"query_type": "FATWA_REQUEST"})
    assert res_esc["status"] == "ESCALATED"
    assert "Article 246" in res_esc["message"]

def test_scholar_veto_simulation():
    # Scholar Board simulation via the Immune Layer/Middleware
    scholar_board = MagicMock()
    scholar_board.approve_major_decision.return_value = False # Vetoed

    middleware = DualMetricMiddleware(scholar_board_ref=scholar_board)
    # Actually, let's test the AR/VR engine's use of scholar board
    from agentic_core.religious_domain.immersive.engine import ARVRImmersiveEngine
    engine = ARVRImmersiveEngine(scholar_board)

    import asyncio
    res = asyncio.run(engine.validate_content("scene_1", {"has_prophetic_imagery": False}))
    assert res["status"] == "PENDING_REVIEW" # Since mock returned False

def test_sharia_finops_zakat():
    ledger = MagicMock()
    profile = MagicMock()
    profile.calculate_zakat_eligibility.return_value = {"is_eligible": True, "zakat_due": 25.0}

    finops = IslamicFinanceAdapter(ledger, profile)
    res = finops.process_zakat("user_1", 1000.0)
    assert res["status"] == "PROCESSED"
    assert res["amount_distributed"] == 25.0
