import pytest
import os
import json
from src.organism.python.core.governance import SovereignIdentity, SovereignAuditLog

def test_identity_signature():
    id_layer = SovereignIdentity(key_path="data/test_state/test_key.pem")
    action = {"goal": "test", "params": {"a": 1}}
    signature = id_layer.sign_action(action)
    assert isinstance(signature, str)
    assert id_layer.verify_action(action, signature) == True
    tampered_action = {"goal": "test", "params": {"a": 2}}
    assert id_layer.verify_action(tampered_action, signature) == False

def test_audit_log_chaining():
    log_path = "data/test_state/test_audit.jsonl"
    if os.path.exists(log_path):
        os.remove(log_path)
    audit = SovereignAuditLog(log_path=log_path)
    entry1 = {"id": "1", "data": "first"}
    audit.log_entry(entry1)
    entry2 = {"id": "2", "data": "second"}
    audit.log_entry(entry2)
    with open(log_path, "r") as f:
        lines = f.readlines()
    log1 = json.loads(lines[0])
    log2 = json.loads(lines[1])
    assert log2["prev_hash"] == log1["hash"]
    assert log1["prev_hash"] == "0" * 64
