import pytest
from agentic_core.evolution.ueg_merkle_dag import MerkleDAGV137

def test_ueg_dag_logic():
    dag = MerkleDAGV137()
    h1 = dag.add_event({"type": "GENESIS"})
    h2 = dag.add_event({"type": "UPGRADE"}, parents=[h1])

    assert h2 in dag.heads
    assert dag.verify_chain(h1, h2) == True

def test_ueg_tamper_detection():
    dag = MerkleDAGV137()
    h1 = dag.add_event({"v": 1})
    h2 = dag.add_event({"v": 2}, parents=[h1])

    # Tamper
    dag.nodes[h1]["v"] = 99
    assert dag.verify_chain(h1, h2) == False

def test_merkle_proof_spec():
    dag = MerkleDAGV137()
    h = dag.add_event({"data": "secure"})
    proof = dag.get_event_proof(h)
    assert proof["event_hash"] == h
    assert proof["v137_certified"] == True
