"""
Clean conftest for integration tests.
Does NOT mock pydantic, psutil, or other real dependencies
that the MVP spine requires.
"""
import json
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
# W507 (FU-249) — EVERY XDIST WORKER GETS ITS OWN STORE, or the suite cannot run in parallel at all.
#
# The suite is 42-50 minutes at ~24% CPU, and a sample showed one end-to-end test taking 115s of 173s:
# the wall time is a few tests waiting on sequential I/O, which parallel workers fix. But every test
# shares ONE DATA_DIR, and parallel workers over one store is the documented corruption mode (two
# concurrent suites once produced ~40 false failures on shared memory.json / UEG ledgers).
#
# `PYTEST_XDIST_WORKER` is set by xdist in each worker process ("gw0", "gw1", ...) and is absent on a
# serial run, so a serial run keeps exactly the path it had.
_XDIST_WORKER = os.environ.get("PYTEST_XDIST_WORKER") or ""


def _per_worker(path: str) -> str:
    """The same path, made this worker's own. Unchanged when not running under xdist."""
    if not _XDIST_WORKER:
        return path
    base, ext = os.path.splitext(path)
    return f"{base}__{_XDIST_WORKER}{ext}"


_TEST_STORE = _per_worker(os.path.abspath(os.path.join("data", "_test_store")))
# W507 — created only if it is actually going to be USED. This ran unconditionally, so a run with an
# explicit DATA_DIR (the recipe every verification run uses) still made the default directory it would never
# write to — and under `-n 8` it made eight of them, leaving data/_test_store__gw0..gw7 behind in the repo.
if not os.environ.get("DATA_DIR"):
    os.makedirs(_TEST_STORE, exist_ok=True)
os.environ.setdefault("DATA_DIR", _TEST_STORE)
os.environ.setdefault("WORKSTATION_DATA_DIR", _TEST_STORE)
os.environ.setdefault("WORKSTATION_UEG_PATH", os.path.join(_TEST_STORE, "ueg.jsonl"))
os.environ.setdefault("LISTINGS_DIR", os.path.join(_TEST_STORE, "marketplace"))

# AN EXPLICIT ROOT IS SUBDIVIDED, NOT SHARED. `setdefault` above means an explicit DATA_DIR wins, and the
# isolated-run recipe used for every verification run sets one — so without this, `-n 8` with that recipe
# would have pointed all eight workers at the SAME directory and corrupted them while looking isolated.
# An explicit value defeating the isolation is W394's original defect one layer over.
if _XDIST_WORKER:
    for _var, _leaf in (("DATA_DIR", None), ("WORKSTATION_DATA_DIR", None),
                        ("PROJECTS_DIR", None), ("LISTINGS_DIR", None),
                        ("SYNTHESIS_OUTPUT_DIR", None), ("PROPOSALS_DIR", None),
                        ("WORKSTATION_UEG_PATH", "file")):
        _val = os.environ.get(_var)
        if not _val or _val.endswith(f"__{_XDIST_WORKER}") or f"__{_XDIST_WORKER}" in _val:
            continue
        os.environ[_var] = _per_worker(_val)
        if _leaf != "file":
            os.makedirs(os.environ[_var], exist_ok=True)
        else:
            os.makedirs(os.path.dirname(os.environ[_var]) or ".", exist_ok=True)
    # re-derive the ones computed from the store root, so a UEG path inside an explicit root follows it
    _TEST_STORE = os.environ["DATA_DIR"]

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


# ── W537 (FU-301, P2.17 bar (b)2b) — A STALLED RUN MUST NOT READ AS A PASS ──────────────────────
# Three of six parallel runs stalled at 74%, 89% and 57% with every worker in flight, and NOTHING
# reported it: on a stall the session never finishes, so pytest_sessionfinish never fires and no summary
# is printed. A reader piping to `tail` sees a truncated log and no verdict, which is how those three were
# first read as runs still in progress. So progress is written AS IT HAPPENS here and scripts/run_verdict.py
# pronounces COMPLETE / INCOMPLETE / NOT KNOWN from the file afterwards.
#
# Opt-in on WORKSTATION_RUN_PROGRESS: with the variable unset nothing is written and no existing
# invocation changes behaviour, which is why this cannot slow or perturb the serial run a commit is
# trusted to.
_RUN_PROGRESS = os.environ.get("WORKSTATION_RUN_PROGRESS") or ""
_reported_nodes = set()
_collected_total = {"n": None}
_xdist_ids = set()          # W539 — the union of every worker's collected ids
#  W567 — AM I A WORKER? Only the controller may write the progress file. It is a dict rather than a bare
#  name so the hook that sets it needs no `global`, and it defaults to False so a SERIAL run writes
#  normally. The only way a process can know is the attribute xdist attaches to a worker's config.
_IS_WORKER = {"v": False}


#  W567 — THE STALL WATCHDOG. FU-301 has carried an unexplained parallel stall since W507: every worker
#  idle at once, no CPU, no slow test, and the row's stated next step was to get a stack from a live
#  stalled worker. MEASURED THIS ROUND: py-spy installs and CANNOT WORK against this Python — the Windows
#  Store (MSIX) install blocks process inspection ("A device attached to the system is not functioning",
#  os error 31) — so the external-profiler route is closed, not merely unattempted, and a later round
#  should not spend itself retrying it.
#
#  faulthandler works from INSIDE the process, so the sandbox is irrelevant, and it dumps EVERY thread
#  with full stacks. The timer is RE-ARMED on each terminal report, which turns a periodic dump into a
#  stall detector: it fires only when no test has finished for the whole timeout. The default is well
#  above the slowest test measured on this suite (158s), so a legitimately slow test cannot trip it.
#
#  OPT-IN, like the progress file, and it never breaks the run it is watching.
_STALL_DIR = os.environ.get("WORKSTATION_STALL_DUMP") or ""
_STALL_AFTER_S = float(os.environ.get("WORKSTATION_STALL_DUMP_S") or "300")
_STALL_FH = {"f": None}


def _arm_stall_dump():
    """(Re)start the countdown. Called at configure and after every terminal report."""
    if not _STALL_DIR or _STALL_FH["f"] is None:
        return
    try:
        import faulthandler
        #  repeat=False, AND THAT IS A SAFETY DECISION RATHER THAN A PREFERENCE. Driven at a pathological
        #  3s threshold with repeat=True, this fired about thirty times in a hundred seconds — 233 KB of
        #  tracebacks taken while the interpreter was importing and rewriting test modules — and that run
        #  also printed "Windows fatal exception: access violation", which a control run at the same
        #  selector with the watchdog off did not. I could not prove the watchdog caused the crash, and
        #  that is precisely why it does not repeat: ONE stack at the moment of a stall is what FU-301
        #  needs, and a watchdog that might take down the run it is watching is worse than none. The timer
        #  is re-armed after every terminal report, so a long run never accumulates pending dumps.
        faulthandler.dump_traceback_later(_STALL_AFTER_S, repeat=False, file=_STALL_FH["f"])
    except Exception:          # noqa: BLE001 — a watchdog must never break the run it watches
        pass


def pytest_configure(config):
    #  RUNS IN EVERY PROCESS, controller and workers alike — which is exactly what is needed, because each
    #  one must decide for itself whether it may write the shared progress file, and each must arm its own
    #  watchdog: a stalled WORKER is the thing FU-301 needs a stack from, and only that worker can take it.
    _IS_WORKER["v"] = hasattr(config, "workerinput")
    if _STALL_DIR:
        try:
            os.makedirs(_STALL_DIR, exist_ok=True)
            _who = "controller"
            if _IS_WORKER["v"]:
                _who = str(config.workerinput.get("workerid") or "worker")
            #  ONE FILE PER PROCESS. Six workers sharing one file would interleave six tracebacks into
            #  something nobody could read, which is the shape of defect this round is already fixing in
            #  the progress file one layer along.
            _STALL_FH["f"] = open(os.path.join(_STALL_DIR, f"stall-{_who}.txt"),
                                  "w", encoding="utf-8", buffering=1)
            _STALL_FH["f"].write(f"# {_who}: armed, dumps every thread if no test finishes for "
                                 f"{_STALL_AFTER_S:.0f}s\n")
            _arm_stall_dump()
        except Exception:      # noqa: BLE001
            _STALL_FH["f"] = None


def _write_progress():
    if not _RUN_PROGRESS:
        return
    try:
        tmp = _RUN_PROGRESS + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump({"collected": _collected_total["n"], "reported": len(_reported_nodes)}, fh)
        os.replace(tmp, _RUN_PROGRESS)
    except OSError:
        # A progress file that cannot be written must never break the run it is observing.
        pass


def pytest_xdist_node_collection_finished(node, ids):
    # W539 — THE PARALLEL DENOMINATOR. Under xdist each WORKER collects its own shard, so the
    # controller's pytest_collection_finish sees no items and `collected` stayed null: run_verdict
    # answered NOT KNOWN for a parallel run that finished perfectly. Measured on W539's proof run.
    # That is the mode this detector exists for — FU-301's stalls are PARALLEL stalls — so being blind
    # here made it blind where it matters. xdist fires this on the CONTROLLER once per worker with that
    # worker's ids; their union is the true total, and a union rather than a sum because a reruns or
    # re-collection must not double-count.
    if _RUN_PROGRESS:
        _xdist_ids.update(ids or ())
        _collected_total["n"] = len(_xdist_ids)
        _write_progress()


def pytest_collection_finish(session):
    # THE CONTROLLER OWNS THE TOTAL. Each xdist worker collects only its own shard, so a worker writing
    # here would report its shard as the whole run and a stall would read as a complete short run.
    #
    # AND IT MUST BE THE SELECTED SET, NOT THE COLLECTED ONE. This first used
    # pytest_collection_modifyitems, which runs BEFORE -k deselection: a filtered run then reported 532
    # collected against 1 reported, so every selector read as INCOMPLETE. That is a false positive on
    # exactly the runs each round depends on, and it would have made this detector useless while
    # appearing to work. pytest_collection_finish runs after every modifyitems hook, so session.items
    # is what will actually RUN.
    if _RUN_PROGRESS and not hasattr(session.config, "workerinput"):
        # W539 — do not overwrite a total the xdist hook already established from the workers'
        # ids. On the controller of a parallel run session.items is empty, and writing 0 here
        # would turn a correct denominator back into a wrong one.
        if not _xdist_ids:
            _collected_total["n"] = len(session.items)
        _write_progress()


def pytest_runtest_logreport(report):
    """One terminal outcome per test: the call phase, or a setup that skipped or failed without one.

    THE CONTROLLER OWNS THIS FILE, and W567 measured what it cost that this hook did not say so. It had
    no controller guard, so under xdist it fired in every worker too and all seven processes wrote the
    same path. A worker never sets the collected total — both hooks that do are controller-only — so a
    worker writes `collected: null`, and it counts only its OWN shard. WHOSE WRITE IS LAST IS A RACE, and
    on a run that never finishes there is no `pytest_sessionfinish` to settle it.

    DRIVEN, BEFORE AND AFTER. A parallel run sampled mid-flight read {collected: 564, reported: 70} —
    correct, because a controller write happened to be last. The same run, once its processes were gone,
    left {collected: null, reported: 10} on disk: a worker's shard count, at a multiple of ten from the
    gate below, with no total. That is FU-362's live-stall measurement reproduced exactly, and the
    consequence is the row's own words: run_verdict then answers NOT KNOWN *because no collected count
    exists*, rather than INCOMPLETE *because a short reported count was compared against a known total*,
    which is the route it was designed to detect a stall by. A gate that reaches the right answer by the
    wrong route gives the wrong answer when the route changes.

    xdist forwards every worker's report to the controller, so the controller sees them all: guarding the
    write loses no counts and makes the numerator and the denominator come from one process.
    """
    _terminal = (report.when == "call"
                 or (report.when == "setup" and report.outcome in ("skipped", "failed")))
    #  THE WATCHDOG IS RE-ARMED IN EVERY PROCESS, before the controller guard below. A stalled WORKER is
    #  what FU-301 needs a stack from and only that worker can take one, so this must not be behind a
    #  guard that silences workers.
    if _terminal:
        _arm_stall_dump()
    if not _RUN_PROGRESS or _IS_WORKER["v"]:
        return
    if _terminal:
        _reported_nodes.add(report.nodeid)
        if len(_reported_nodes) % 10 == 0:
            _write_progress()


def pytest_sessionfinish(session, exitstatus):
    # Writes the final count when the run DOES finish. Its ABSENCE is what the verdict reader detects.
    _write_progress()
    #  AND DISARM THE WATCHDOG, in every process. A run that finished must leave no pending timer: with
    #  repeat=True an un-cancelled one would dump tracebacks into a file after the session was over,
    #  which reads as a stall that never happened. An instrument that reports a defect it did not observe
    #  is worse than one that is silent.
    if _STALL_FH["f"] is not None:
        try:
            import faulthandler
            faulthandler.cancel_dump_traceback_later()
            _STALL_FH["f"].write(f"# disarmed: the session finished with exit status {exitstatus}\n")
            _STALL_FH["f"].flush()
        except Exception:      # noqa: BLE001
            pass
