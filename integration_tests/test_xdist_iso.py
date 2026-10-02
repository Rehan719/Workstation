"""W507 (FU-249) — every parallel worker must own its store, or a parallel run proves nothing.

The suite runs in parallel only because each xdist worker gets its own DATA_DIR. Parallel workers over ONE
store is the documented corruption mode: two concurrent suites once produced ~40 false failures on shared
memory.json and UEG ledgers, and a green parallel run over a shared store would be meaningless rather than
merely slow. So this asserts the precondition every other test's result now depends on.

It also covers the trap the isolation was written for: conftest uses `os.environ.setdefault`, so an EXPLICIT
DATA_DIR wins — and the isolated-run recipe used for every verification run sets one. Without subdividing an
explicit root, `-n 8` would point all eight workers at the same directory while looking correctly isolated.
"""
import os

import pytest


@pytest.mark.parametrize("i", list(range(4)))   # several cases, so more than one worker is exercised
def test_each_worker_owns_its_store(i, tmp_path):
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    data_dir = os.environ["DATA_DIR"]
    ueg = os.environ.get("WORKSTATION_UEG_PATH") or ""

    if not worker:
        pytest.skip("serial run — there is no worker to isolate from")

    assert f"__{worker}" in data_dir, (
        f"worker {worker} is using {data_dir}, which is not its own — a parallel run over a shared store "
        f"corrupts the stores and its result means nothing")
    assert f"__{worker}" in ueg, (
        f"worker {worker}'s UEG path is {ueg}, shared with the other workers — the chain would interleave")

    # W537 — THIS PROBE PROVES WRITABILITY, AND SAYS SO. It used to assert "another worker overwrote this
    # worker's file", which CANNOT FIRE even under the condition it names: the file is named for this worker
    # inside a directory named for this worker, so the filenames differ whether or not the directories are
    # shared and no overwrite is possible either way. The SHARING property is established by the two path
    # assertions above, which do fail on a shared root. The claim is corrected rather than replaced by a
    # cross-worker detector: that would have to race two workers against one filename, and a flaky guard is
    # worse than an honest one.
    probe = os.path.join(data_dir, f"xdist_probe_{worker}.txt")
    with open(probe, "w", encoding="utf-8") as f:
        f.write(worker)
    with open(probe, encoding="utf-8") as f:
        assert f.read() == worker, (
            "this worker's own store is not writable and readable as its own — which is a precondition for "
            "every other test's result, and is all this probe establishes: isolation itself is asserted on "
            "the PATHS above, not here")
