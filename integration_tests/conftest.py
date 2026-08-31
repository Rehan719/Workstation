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

# Setting the env is NOT sufficient on its own. agentic_core.config captures the directory ONCE, when
# its `settings` object is constructed at import time:
#     data_dir: str = field(default_factory=lambda: os.getenv("DATA_DIR", "data"))
# So if anything imports agentic_core before this file runs, the env change arrives too late and the
# suite writes to the real store anyway — silently. That is exactly what happened in CI: the same
# commit that isolated DATA_DIR locally left CI resolving to plain "data", which is why a test
# asserting the default kept passing there while failing locally.
#
# Isolation that depends on import order is not isolation. If config is already loaded, correct it.
import sys as _sys

if "agentic_core.config" in _sys.modules:
    _cfg = _sys.modules["agentic_core.config"]
    _s = getattr(_cfg, "settings", None)
    if _s is not None and getattr(_s, "data_dir", None) != os.environ["DATA_DIR"]:
        # Settings is @dataclass(frozen=True), so a plain assignment raises FrozenInstanceError.
        # A first attempt did exactly that and wrapped it in `except Exception: pass`, so the
        # correction failed SILENTLY and the suite still pointed at the real store while looking
        # fixed. No bare except here: if this cannot work, it must say so.
        object.__setattr__(_s, "data_dir", os.environ["DATA_DIR"])


@pytest.fixture(scope="session", autouse=True)
def _assert_store_is_isolated():
    """Fail loudly if the suite is about to write into the REAL data store.

    Without this the pollution is invisible: tests pass either way, and you only notice months later
    when an entity picker holds 1,552 rows.

    The check is "not the real store", NOT "equals _test_store". A first version demanded the latter
    and broke the documented isolated-run recipe (DATA_DIR=/tmp/... python -m pytest ...) - every
    test errored at setup. An explicitly chosen DATA_DIR is deliberate isolation by definition; the
    only thing worth rejecting is the default real store.
    """
    import os.path
    from agentic_core.config import data_path
    resolved = os.path.abspath(str(data_path("vsb_entities")))
    real = os.path.abspath(os.path.join("data", "vsb_entities"))
    assert resolved != real, (
        "integration tests are NOT isolated - they would write to the real store at "
        + resolved + ". agentic_core.config was probably imported before conftest ran."
    )
    yield
