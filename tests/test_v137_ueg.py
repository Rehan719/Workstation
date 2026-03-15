import pytest
from agentic_core.evolution.ueg_merkle_dag import MerkleDAGV137

def test_ueg_dag_integrity():
    dag = MerkleDAGV137()
    h1 = dag.add_event("GENESIS", {"v": 1})
    h2 = dag.add_event("EVOLUTION_1", {"v": 2})

    assert h2 in dag.heads
    assert h1 not in dag.heads # h1 is parent of h2

    assert dag.verify_event(h1) == True
    assert dag.verify_event(h2) == True

def test_ueg_chain_verification():
    dag = MerkleDAGV137()
    h1 = dag.add_event("G1", {})
    h2 = dag.add_event("G2", {}, parents=[h1])
    h3 = dag.add_event("G3", {}, parents=[h2])

    # Verify leaf to root
    assert dag.verify_chain(h3, h1) == True
    # Tamper with h2 data
    dag.nodes[h2]["data"]["tampered"] = True
    assert dag.verify_event(h2) == False

def test_merkle_proof():
    dag = MerkleDAGV137()
    h = dag.add_event("TEST", {"data": "secure"})
    proof = dag.get_merkle_proof(h)
    assert proof["target"] == h
    assert proof["v137_certified"] == True
