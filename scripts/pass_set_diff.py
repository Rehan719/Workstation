"""Did two runs of the suite produce the SAME pass/fail set? — P2.17 bar (b)1.

WHY THIS EXISTS. The suite takes about 55 minutes serially. W507 measured the parallel alternative at 10m35s on
six workers — a 4.8x saving — with the pass sets matching exactly. It has NOT been adopted, and the reason is
FU-301: three of six parallel runs STALLED, at 74%, 89% and 57%, with every worker in flight and no CPU. W537
made a stall VISIBLE (scripts/run_verdict.py reports INCOMPLETE where a stall used to look like a run still in
progress), which removes the silence but not the question the bar actually asks.

THE BAR'S VERB IS "PROVEN". P2.17 (b)1 reads: the parallel suite "is proven to produce the SAME pass/fail set as
the serial one ON THE SAME TREE before it is adopted anywhere". W507 measured that once and the figure has been
TYPED ever since. A comparator is not that proof; it is what makes the proof checkable. The proof is two runs.

THREE VERDICTS, because two cannot carry the case:
  SAME        every node id appears in both runs with the same outcome.
  DIFFERENT   at least one node differs or is missing from one side. Each one is NAMED, because "the sets
              differ" is not actionable and a count hides whether it is one flaky test or a systematic split.
  INCOMPLETE  a run did not finish, so its set is not a set. A stalled run's pass/fail set is not a smaller
              answer, it is an absent one, and comparing against it would adopt the parallel suite on evidence
              that does not exist.

WHAT THIS DOES NOT ESTABLISH, stated because it is the easy over-read: one matching pair of runs does not make
the parallel suite trustworthy, and it does not explain FU-301's stall. It establishes that ON THIS TREE the two
runs agreed. The stall remains unexplained and the serial run remains what a commit is trusted to until the
Owner's own ordering says otherwise.

Usage:
    python -m pytest integration_tests/ -q -p no:warnings --junit-xml=/c/tmp/serial.xml
    python -m pytest integration_tests/ -q -p no:warnings -n 6 --junit-xml=/c/tmp/par.xml
    python scripts/pass_set_diff.py /c/tmp/serial.xml /c/tmp/par.xml
"""
from __future__ import annotations

import io
import json
import os
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, Tuple

SAME = "SAME"
DIFFERENT = "DIFFERENT"
INCOMPLETE = "INCOMPLETE"


def read_outcomes(path: str) -> Tuple[Dict[str, str], Dict[str, Any]]:
    """{node id: outcome} from a pytest junit-xml, plus the counts the file declares about itself."""
    if not os.path.exists(path):
        return {}, {"error": f"no report at {path}"}
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        # A TRUNCATED XML IS THE SIGNATURE OF A KILLED RUN: pytest writes the file at the end, so a stalled
        # run leaves either nothing or a partial document. Either way the set is absent, not small.
        return {}, {"error": f"the report could not be parsed ({e.__class__.__name__}): {e}"}
    suites = [root] if root.tag == "testsuite" else list(root)
    out: Dict[str, str] = {}
    declared = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for suite in suites:
        for k in declared:
            declared[k] += int(suite.get(k) or 0)
        for case in suite.iter("testcase"):
            node = "%s::%s" % (case.get("classname") or "", case.get("name") or "")
            outcome = "passed"
            for child in case:
                if child.tag in ("failure", "error"):
                    outcome = child.tag
                    break
                if child.tag == "skipped":
                    outcome = "skipped"
            out[node] = outcome
    return out, declared


def compare(a_path: str, b_path: str, a_label: str = "A", b_label: str = "B",
            expected: Dict[str, str] | None = None) -> Dict[str, Any]:
    """Compare two reports. `expected` DECLARES differences that are correct, each with its reason.

    W539 — without this, bar (b)1 is unsatisfiable by construction. Four nodes
    (test_each_worker_owns_its_store[0..3]) SKIP serially because there is no worker to isolate
    from, and PASS in parallel. That is right and can never change, so a comparator demanding
    identical outcome sets would answer DIFFERENT on every tree forever. A declaration is a claim,
    so it carries a reason, and an UNDECLARED difference still reads DIFFERENT.
    """
    a, a_meta = read_outcomes(a_path)
    b, b_meta = read_outcomes(b_path)
    if a_meta.get("error") or b_meta.get("error"):
        return {"verdict": INCOMPLETE, "a_count": len(a), "b_count": len(b),
                "basis": ("a run's report could not be read, so its pass/fail set is ABSENT rather than "
                          "smaller: " + "; ".join(x for x in (a_meta.get("error"), b_meta.get("error")) if x))}
    if not a or not b:
        return {"verdict": INCOMPLETE, "a_count": len(a), "b_count": len(b),
                "basis": (f"{a_label} reported {len(a)} test(s) and {b_label} reported {len(b)}; a run that "
                          f"reported nothing did not finish, and an empty set cannot be compared")}
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    differing = sorted(n for n in (set(a) & set(b)) if a[n] != b[n])
    #  a declared difference is moved aside WITH its reason, so the report still shows it rather than hiding it
    declared_hits = []
    if expected:
        kept = []
        for n in differing:
            why = next((r for pat, r in expected.items() if pat in n), None)
            (declared_hits if why else kept).append(
                {"node": n, a_label: a[n], b_label: b[n], "declared_because": why} if why else n)
        differing = kept
    if not only_a and not only_b and not differing:
        return {"verdict": SAME, "a_count": len(a), "b_count": len(b),
                "shared": len(a), "differing": [], "only_a": [], "only_b": [],
                "declared": declared_hits,
                "basis": (f"all {len(a)} node id(s) appear in both runs, and every outcome matches except "
                          f"{len(declared_hits)} DECLARED difference(s), each listed with its reason. This is "
                          f"a statement about THESE TWO RUNS on this tree, not about the parallel suite in "
                          f"general: one agreement does not explain the stall FU-301 records")}
    return {"verdict": DIFFERENT, "a_count": len(a), "b_count": len(b), "shared": len(set(a) & set(b)),
            "declared": declared_hits,
            "differing": [{"node": n, a_label: a[n], b_label: b[n]} for n in differing[:40]],
            "only_a": only_a[:40], "only_b": only_b[:40],
            "basis": (f"{len(differing)} node(s) differ in outcome, {len(only_a)} appear only in {a_label} "
                      f"and {len(only_b)} only in {b_label}. Each is named rather than counted, because a "
                      f"count cannot distinguish one flaky test from a systematic split")}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__.strip().splitlines()[-1])
        return 2
    expected = None
    if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
        expected = json.loads(io.open(sys.argv[3], encoding="utf-8").read())
    r = compare(sys.argv[1], sys.argv[2], "serial", "parallel", expected)
    print("%s — %s" % (r["verdict"], r["basis"]))
    for d in r.get("declared") or []:
        print("  DECLARED %s: serial=%s parallel=%s — %s"
              % (d["node"], d["serial"], d["parallel"], d["declared_because"]))
    for d in r.get("differing") or []:
        print("  DIFFERS  %s: serial=%s parallel=%s" % (d["node"], d["serial"], d["parallel"]))
    for n in r.get("only_a") or []:
        print("  ONLY IN SERIAL    %s" % n)
    for n in r.get("only_b") or []:
        print("  ONLY IN PARALLEL  %s" % n)
    return 0 if r["verdict"] == SAME else 1


if __name__ == "__main__":
    sys.exit(main())
