import pytest
import asyncio
from agentic_core.intelligence.opportunity_scanner import OpportunityScanner
from agentic_core.business.feedback_engine import FeedbackEngine
from agentic_core.business.profit_distributor import ProfitDistributor
from agentic_core.governance.audit_trail import UnifiedEvidenceGraph
from agentic_core.governance.crisis_management import CrisisManager

def test_opportunity_sensing():
    scanner = OpportunityScanner()
    leads = scanner.scan_academic_funding()
    assert len(leads) > 0
    score = scanner.score_lead(leads[0])
    assert score >= 0.8

def test_market_feedback():
    engine = FeedbackEngine()
    engine.record_feedback("client_77", {"nps": 9})
    assert engine.get_market_sentiment() == 9.0

def test_profit_distribution_zakat():
    distributor = ProfitDistributor()
    distributor.total_revenue = 2000.0
    distributor.operational_costs = 500.0
    # Net profit 1500. Zakat 37.5. Reserve 292.5. Distributable 1170.
    res = distributor.distribute_profits(method="stablecoin")
    assert res["status"] == "success"
    assert res["zakat_paid"] == 37.5
    assert res["distributed"] == 1170.0

def test_audit_trail_attestation():
    ueg = UnifiedEvidenceGraph()
    ueg.record_event("commander", "Pivoted strategy", {"new_domain": "Biotech"})
    assert len(ueg.ledger) == 1
    assert "attestation" in ueg.ledger[0]

def test_crisis_playbook():
    manager = CrisisManager()
    assert manager.detect_threat({"security_breach": True}) is True
