from agentic_core.mesh.aggregator.federated_aggregator import FederatedAggregator
def test_agg():
    a = FederatedAggregator()
    res = a.aggregate([{"legal_precision": 0.1}, {"legal_precision": 0.2}])
    assert res["legal_precision"] >= 0.15
