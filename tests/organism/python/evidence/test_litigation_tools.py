import pytest
import os
import shutil
import json
from src.organism.python.evidence.graph_schema import EvidenceGraph, LegalEvent
from src.organism.python.agents.schedule_of_loss import ScheduleOfLossAgent
from src.organism.python.utils.bundler import TribunalBundleGenerator

@pytest.fixture
def evidence_setup():
    test_path = "data/test_evidence_graph.json"
    if os.path.exists(test_path):
        os.remove(test_path)
    graph = EvidenceGraph(storage_path=test_path)
    return graph, test_path

def test_evidence_graph_chronology(evidence_setup):
    graph, _ = evidence_setup

    event1 = LegalEvent(id="e1", date="2026-06-01", description="Dismissal", source_document="doc1.txt")
    event2 = LegalEvent(id="e2", date="2026-01-01", description="Grievance", source_document="doc2.txt")

    graph.add_event(event1)
    graph.add_event(event2)

    chronology = graph.get_chronology()
    assert chronology[0].id == "e2" # January before June
    assert chronology[1].id == "e1"

def test_schedule_of_loss_2026_caps():
    agent = ScheduleOfLossAgent()
    employee_data = {
        "age": 45,
        "years_of_service": 10,
        "gross_weekly_pay": 1000, # Above cap
        "net_weekly_pay": 800
    }

    graph = None # Simplified for test
    df = agent.calculate(employee_data, graph)

    # Basic Award check
    basic_award = df[df["Head of Claim"] == "Basic Award (Unfair Dismissal)"]["Amount"].values[0]
    # 45 yrs old = 1.5 factor. 10 years service. Cap is 751.
    # 1.5 * 10 * 751 = 11265
    assert float(basic_award) == 11265.0

def test_bundle_generation():
    generator = TribunalBundleGenerator()
    output_dir = "data/test_bundles"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    documents = [{"name": "witness_statement.pdf", "content": b"Witness content"}]
    audit_trail = [{"action": "AI_Inference", "hash": "abc123"}]

    bundle_path = generator.generate("MINHAS-001", documents, audit_trail, output_dir)

    assert os.path.exists(bundle_path)
    assert bundle_path.endswith(".zip")
