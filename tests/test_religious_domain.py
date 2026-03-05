import pytest
import os
import json
from datetime import datetime
from agentic_core.religious_domain.governance.middleware import TazkiyahEngine, DawahReadinessEngine
from agentic_core.religious_domain.tajwid.coach import TajwidCoach
from agentic_core.religious_domain.memorization.engine import MemorizationEngine
from agentic_core.religious_domain.finops.sharia_finops import IslamicFinanceAdapter
from agentic_core.db.manager import DatabaseManager
from agentic_core.ueg.ledger import BlockchainLedger

@pytest.fixture
def db():
    db_name = "test_qep_unit.db"
    if os.path.exists(db_name):
        os.remove(db_name)
    manager = DatabaseManager(f"sqlite:///{db_name}")
    yield manager
    if os.path.exists(db_name):
        os.remove(db_name)

@pytest.fixture
def ledger():
    ledger_file = "test_ledger_unit.json"
    if os.path.exists(ledger_file):
        os.remove(ledger_file)
    bl = BlockchainLedger(ledger_file)
    yield bl
    if os.path.exists(ledger_file):
        os.remove(ledger_file)

def test_tazkiyah_calculation(db):
    engine = TazkiyahEngine(db)
    user_id = "user_test_1"

    # 1. Test initial score
    score = engine.calculate_tazkiyah_score(user_id)
    assert score == 0.0

    # 2. Test update and recalculation
    db.update_spiritual_metrics(user_id, "prayer", 1.0) # weight 0.30
    score_updated = engine.calculate_tazkiyah_score(user_id)
    assert score_updated == 30.0

    db.update_spiritual_metrics(user_id, "memorization", 1.0) # weight 0.25
    score_final = engine.calculate_tazkiyah_score(user_id)
    assert score_final == 55.0

def test_dawah_readiness(db):
    te = TazkiyahEngine(db)
    de = DawahReadinessEngine(db, te)
    user_id = "user_test_2"

    # 1. Default should be false
    assert de.is_ready(user_id) is False

    # 2. Set metrics to pass threshold (75.0)
    db.save_spiritual_metrics(user_id, 80.0, {"prayer": 1.0, "memorization": 1.0})

    # Still false because foundational not complete
    assert de.is_ready(user_id) is False

    # Pass all
    profile = {
        "foundational_modules_complete": True,
        "community_feedback_ratio": 0.9
    }
    res = de.evaluate_readiness(user_id, profile)
    assert res["is_ready"] is True

def test_tajwid_coach():
    coach = TajwidCoach()
    # Test bytes
    result_bytes = coach.analyze_recitation(b"Bismillah", b"Bismillah")
    assert result_bytes["accuracy"] == 1.0

    # Test strings
    result_str = coach.analyze_recitation("Bismillah", "Bismillah")
    assert result_str["accuracy"] == 1.0

def test_memorization_engine():
    engine = MemorizationEngine()
    # Quality 5 (Perfect), Repetition 0
    interval, ef = engine.calculate_next_review(5, 0, 1, 2.5)
    assert interval == 1

    # Quality 5, Repetition 2
    interval, ef = engine.calculate_next_review(5, 2, 6, 2.6)
    assert interval == math.ceil(6 * ef)

import math

def test_sharia_finops(ledger):
    adapter = IslamicFinanceAdapter(ledger)
    zakat = adapter.calculate_zakat(20000, 5000)
    assert zakat == 500.0

    tx_id = adapter.record_charity_transaction("user_1", 500.0, "ZAKAT")
    assert tx_id.startswith("TX_")

    # Verify ledger persist
    assert len(ledger.chain) > 1
    assert ledger.chain[-1]["data"]["amount"] == 500.0
