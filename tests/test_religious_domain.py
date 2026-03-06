import pytest
import os
import json
import sqlite3
from agentic_core.religious_domain.governance.middleware import TazkiyahEngine, DawahReadinessEngine, DualMetricMiddleware
from agentic_core.religious_domain.tajwid.coach import TajwidCoach
from agentic_core.religious_domain.memorization.engine import MemorizationEngine
from agentic_core.religious_domain.finops.sharia_finops import IslamicFinanceAdapter
from agentic_core.religious_domain.auth.identity import ReligiousAuth
from agentic_core.religious_domain.community.forum import CommunityOrchestrator
from agentic_core.db.manager import DatabaseManager
from agentic_core.ueg.ledger import BlockchainLedger

@pytest.fixture
def db():
    db_name = "test_qep_refined.db"
    if os.path.exists(db_name): os.remove(db_name)
    manager = DatabaseManager(f"sqlite:///{db_name}")
    yield manager
    if os.path.exists(db_name): os.remove(db_name)

@pytest.fixture
def ledger():
    ledger_file = "test_ledger_refined.json"
    if os.path.exists(ledger_file): os.remove(ledger_file)
    bl = BlockchainLedger(ledger_file)
    yield bl
    if os.path.exists(ledger_file): os.remove(ledger_file)

def test_religious_auth():
    auth = ReligiousAuth(None)
    profile = auth.register_user({"user_id": "u1", "track": "MUSLIM"})
    assert profile["track"] == "MUSLIM"
    assert "tazkiyah_score" in profile["spiritual_markers"]

def test_community_orchestrator():
    from unittest.mock import MagicMock
    halal = MagicMock()
    halal.verify_content.return_value = True
    co = CommunityOrchestrator(halal)

    post = co.create_post("u1", "TAFSIR", "A test post content.")
    assert post["status"] == "APPROVED"
    assert co.request_dua("u1", "Help")["request"] == "Help"

def test_db_concurrency(db):
    # Stress WAL mode with multiple connections
    conn1 = db._get_connection()
    conn2 = db._get_connection()

    conn1.execute("INSERT INTO workspaces (ws_id, name, owner_id) VALUES ('ws1', 'N1', 'O1')")
    conn1.commit() # Ensure released
    conn2.execute("INSERT INTO workspaces (ws_id, name, owner_id) VALUES ('ws2', 'N2', 'O2')")

    conn1.commit()
    conn2.commit()

    rows = db.get_all_workspaces()
    assert len(rows) == 2
    conn1.close()
    conn2.close()

def test_tazkiyah_weights_from_config(db):
    te = TazkiyahEngine(db, "config/qep/policies.json")
    assert te.weights['prayer'] == 0.30

def test_tajwid_coach_robustness():
    coach = TajwidCoach()
    res = coach.analyze_recitation(b"abc", "abc")
    assert res["accuracy"] == 1.0

def test_sharia_finops_adapter(ledger):
    adapter = IslamicFinanceAdapter(ledger)
    zakat = adapter.calculate_zakat(100000, 5000)
    assert zakat == 2500.0
    adapter.record_charity_transaction("u1", zakat, "ZAKAT")
