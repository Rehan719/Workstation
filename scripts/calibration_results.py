"""W1184 (FU-1054) - THE CARE REVIEWER'S CALIBRATION RUNS, COPIED INTO THE TREE, AND THE COPY CHECKED.

    python scripts/calibration_results.py export [--out PATH]
    python scripts/calibration_results.py check [--file PATH]

export copies, from this machine's record of calibration runs, each run the agent made through its own door with a
model serving (POST /api/v1/review/calibration/agent-run), merged by run id into the file and never dropping or
rewriting a run the file holds; a file that check finds wrong is never written over. check says what is wrong with
the file, or how many runs it checked. Both default to docs/CARE_REVIEW_CALIBRATION_RESULTS.json. The copy is
evidence for a person to read; the server counts only the runs in its own record. Nothing made where no model
serves is a run, and a typed run is never copied. The suite runs this only on files and records of its own scratch
store, never on the tracked file.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agentic_core.api import _review_calibration as cal  # noqa: E402

DEFAULT = ROOT / cal.RESULTS["care"]


def _write(path: pathlib.Path, doc) -> None:
    tmp = path.with_name(path.name + ".w1184tmp")
    tmp.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _export(out: pathlib.Path) -> int:
    try:
        existing = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
    except (OSError, ValueError) as exc:
        print(f"NOT EXPORTED: {out} could not be read ({type(exc).__name__}), so nothing was written over it")
        return 2
    #  the file merged into is checked first: one that is not the results, or holds what is not a run, is never
    #  written over, so nothing it holds is dropped
    if existing is not None:
        problems = cal.check_results(existing)
        if problems:
            for p in problems:
                print(f"NOT EXPORTED: {p}")
            return 1
    try:
        doc = cal.results_for_tree(existing)
    except RuntimeError as exc:
        print(f"NOT EXPORTED: {exc}")
        return 2
    held = len((existing or {}).get("runs") or [])
    if not doc["runs"]:
        print("examined nothing: this machine's record holds no run of care-reviewer made through its own door with "
              "a model serving, so nothing was exported and the file was not written")
        return 1
    problems = cal.check_results(doc)
    if problems:
        for p in problems:
            print(f"NOT EXPORTED: {p}")
        return 1
    _write(out, doc)
    print(f"exported: {len(doc['runs']) - held} new run(s), {len(doc['runs'])} in all, to {out}")
    return 0


def _check(path: pathlib.Path) -> int:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"PROBLEM: {path} could not be read ({type(exc).__name__})")
        return 2
    problems = cal.check_results(doc)
    for p in problems:
        print(f"PROBLEM: {p}")
    if problems:
        print(f"{len(problems)} problem(s) in {path}")
        return 1
    if not doc.get("runs"):
        print(f"examined nothing: {path} holds no run, and says why: {doc.get('no_run')}")
        return 1
    print(f"ok: {len(doc['runs'])} run(s) checked in {path}, each the agent's own and each score what score() gives")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the Care reviewer's calibration runs, copied into the tree and checked")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export", help="copy the agent's own runs from this machine's record into the file")
    e.add_argument("--out", default=str(DEFAULT))
    c = sub.add_parser("check", help="say what is wrong with the file, or how many runs it checked")
    c.add_argument("--file", default=str(DEFAULT))
    a = ap.parse_args(argv)
    return _export(pathlib.Path(a.out)) if a.cmd == "export" else _check(pathlib.Path(a.file))


if __name__ == "__main__":
    sys.exit(main())
