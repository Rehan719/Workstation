import pytest
from datetime import datetime, timedelta
from agentic_core.collaboration.crdt_engine import CRDTState

def test_crdt_lww_merge():
    state = CRDTState("test_project")

    # 1. Basic Update
    state.update("title", "Initial Title")
    assert state.data["title"]["value"] == "Initial Title"

    # 2. Remote Merge (Older clock)
    remote_older = {
        "title": {
            "value": "Older Title",
            "clock": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    state.merge(remote_older)
    assert state.data["title"]["value"] == "Initial Title" # Local wins (clock 1 > 0)

    # 3. Remote Merge (Newer clock)
    remote_newer = {
        "title": {
            "value": "Newer Title",
            "clock": 2,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    state.merge(remote_newer)
    assert state.data["title"]["value"] == "Newer Title"

def test_crdt_collision_resolution():
    state = CRDTState("collision_project")

    # Force identical clock and timestamp for absolute ambiguity
    now = datetime.utcnow().isoformat()
    state.data["field"] = {"value": "Local", "clock": 5, "timestamp": now}

    remote_ambiguous = {
        "field": {"value": "Remote", "clock": 5, "timestamp": now}
    }

    # Default behavior: keep local
    state.merge(remote_ambiguous)
    assert state.data["field"]["value"] == "Local"

    # Hook behavior: custom resolver
    def resolver(key, local, remote):
        return {"value": "Resolved", "clock": 6, "timestamp": now}

    state.set_conflict_resolver(resolver)
    state.merge(remote_ambiguous)
    assert state.data["field"]["value"] == "Resolved"

def test_crdt_timestamp_tiebreak():
    state = CRDTState("tiebreak_project")
    base_time = datetime.utcnow()

    state.data["field"] = {
        "value": "Local",
        "clock": 10,
        "timestamp": base_time.isoformat()
    }

    remote_newer_ts = {
        "field": {
            "value": "Remote Newer",
            "clock": 10,
            "timestamp": (base_time + timedelta(seconds=1)).isoformat()
        }
    }

    state.merge(remote_newer_ts)
    assert state.data["field"]["value"] == "Remote Newer"
