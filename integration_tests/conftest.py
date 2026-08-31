"""
Clean conftest for integration tests.
Does NOT mock pydantic, psutil, or other real dependencies
that the MVP spine requires.
"""
import os
import pytest

# Use isolated test data directories so tests don't pollute real data.
os.environ["PROJECTS_DIR"] = "data/test_projects"
os.environ["SYNTHESIS_OUTPUT_DIR"] = "data/test_synthesis"
os.environ["PROPOSALS_DIR"] = "data/test_proposals"

# W394 — the three lines above promised isolation they did not deliver. DATA_DIR was never set, and
# DATA_DIR is where the things that actually accumulate live: VSB entities, the token ledger, the UEG
# chain, marketplace listings. Running the suite wrote straight into the developer's real store.
#
# The evidence: 1,552 VSB entities across only 45 distinct names, 1,526 of them sitting on a
# duplicated name — "pytest VSB business-plan seed check" ×185, "pytest per-vsb swarm" ×184,
# "list-flags test" ×184, "avatar grounding test" ×183. Every local run added more, and the VSB
# Cockpit's entity picker rendered all of them.
#
# Set BEFORE any agentic_core import, because the stores capture their directory at import time.
# An explicit DATA_DIR from the environment always wins, so the isolated-run recipe used for release
# checks (DATA_DIR + WORKSTATION_DATA_DIR + WORKSTATION_UEG_PATH pointing at a temp dir) is unaffected.
_TEST_STORE = os.path.abspath(os.path.join("data", "_test_store"))
os.makedirs(_TEST_STORE, exist_ok=True)
os.environ.setdefault("DATA_DIR", _TEST_STORE)
os.environ.setdefault("WORKSTATION_DATA_DIR", _TEST_STORE)
os.environ.setdefault("WORKSTATION_UEG_PATH", os.path.join(_TEST_STORE, "ueg.jsonl"))
os.environ.setdefault("LISTINGS_DIR", os.path.join(_TEST_STORE, "marketplace"))
