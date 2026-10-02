"""Did the run actually FINISH? — P2.17 bar (b)2b, FU-301.

THE MEASURED PROBLEM. FU-301 records six parallel runs of this suite: three completed and three STALLED, at
74%, 89% and 57%, with every worker in flight at once and no CPU. store_lock, the shared register lock, the
round's own guards and order dependence were each ruled out; what all workers block on simultaneously is still
unexplained. The row's closing line is the point — a tool that fails silently a third of the time is the
instrument-that-cannot-fail defect inverted.

WHY THIS IS A SEPARATE PROCESS. On a stall the session NEVER FINISHES: pytest_sessionfinish never fires, no
summary line is printed, and any in-process reporter is exactly as stuck as the run it is watching. A reader
piping to `tail` sees a truncated log and no verdict, which is how three stalls were first read as runs still in
progress. So integration_tests/conftest.py writes progress AS IT HAPPENS, and this file pronounces afterwards.

THREE VERDICTS, and the middle one is the one that did not exist:
  COMPLETE   — every collected test reported a terminal outcome. Only then does a pass/fail set mean anything.
  INCOMPLETE — fewer reported than collected. NOT a pass and NOT a failure: the tests that never reported are
               UNKNOWN, not green. A stall reads as this.
  NOT KNOWN  — no progress file, or it names no collected count. Said, rather than assumed either way.

WHAT THIS DOES NOT DO, stated because it would be easy to over-read: it does not explain the stall, does not fix
it, and does not make a parallel run trustworthy. It makes a stall VISIBLE. FU-301 stays open on the cause and
the SERIAL run remains what a commit is trusted to.

Usage:
    WORKSTATION_RUN_PROGRESS=/c/tmp/run.json python -m pytest integration_tests/ -q
    python scripts/run_verdict.py /c/tmp/run.json        # exits non-zero unless COMPLETE
"""
from __future__ import annotations

import io
import json
import os
import sys
from typing import Any, Dict

COMPLETE = "COMPLETE"
INCOMPLETE = "INCOMPLETE"
NOT_KNOWN = "NOT KNOWN"


def verdict(progress_path: str) -> Dict[str, Any]:
    """COMPLETE / INCOMPLETE / NOT KNOWN for the run that wrote `progress_path`."""
    if not progress_path:
        return {"verdict": NOT_KNOWN, "collected": None, "reported": None,
                "basis": ("no progress path was given, so whether a run finished is NOT KNOWN. This is not a "
                          "pass: it is the absence of a measurement")}
    if not os.path.exists(progress_path):
        return {"verdict": NOT_KNOWN, "collected": None, "reported": None,
                "basis": (f"no progress file at {progress_path}, so whether the run finished is NOT KNOWN. A "
                          f"run that wrote nothing is indistinguishable from one that never started, and "
                          f"neither is a pass")}
    try:
        d = json.loads(io.open(progress_path, encoding="utf-8").read())
    except (OSError, ValueError) as e:
        return {"verdict": NOT_KNOWN, "collected": None, "reported": None,
                "basis": (f"the progress file could not be read ({e.__class__.__name__}), so completeness is "
                          f"NOT KNOWN rather than assumed either way")}
    collected, reported = d.get("collected"), d.get("reported")
    if not isinstance(collected, int) or not isinstance(reported, int):
        return {"verdict": NOT_KNOWN, "collected": collected, "reported": reported,
                "basis": ("the progress file names no collected count, so completeness cannot be decided. "
                          "Collection may not have finished, which is itself not a pass")}
    if reported >= collected:
        return {"verdict": COMPLETE, "collected": collected, "reported": reported, "unreported": 0,
                "basis": (f"all {collected} collected test(s) reported a terminal outcome, so the run's "
                          f"pass/fail set covers everything it collected")}
    return {"verdict": INCOMPLETE, "collected": collected, "reported": reported,
            "unreported": collected - reported,
            "basis": (f"{reported} of {collected} collected test(s) reported — {collected - reported} never "
                      f"did. The run did NOT finish, so its pass/fail set is incomplete and the tests that "
                      f"never reported are UNKNOWN rather than green. A stall reads as this, never as a pass")}


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("WORKSTATION_RUN_PROGRESS", "")
    v = verdict(path)
    print("%s - %s" % (v["verdict"], v["basis"]))
    #  Non-zero unless COMPLETE, so a caller chaining on this cannot proceed past an unfinished run.
    return 0 if v["verdict"] == COMPLETE else 1


if __name__ == "__main__":
    sys.exit(main())
