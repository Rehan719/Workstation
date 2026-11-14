#!/usr/bin/env python3
"""Move a test double's rows out of the operations record. A REVERSIBLE MOVE, never a delete (FU-1040).

THE RULING (Owner, 2026-10-12). 162 of the 2,000 rows of the operations record on the Owner's store were served by a
provider named for a test double. Find the writer, and move those rows aside reversibly, under the rule already ruled
for test entities (scripts/quarantine_test_entities.py, 2026-10-09).

THE WRITER. test_orchestrator_adapts_to_model_health (integration_tests/test_mvp_spine.py) records six failed model
attempts served by "flaky", to show that a model with a poor record is moved behind the floor. It writes through
POST /api/v1/operations/record into whatever store the run resolves. Before W394 (2026-08-31) the suite ran on the
real store, and the rows of 2026-06-28..30 are from then. Since W394, W507 and W748 every run, and every xdist
worker, has its own store, and the suite refuses to run on data/.

THE RULE. A row is a test double's when the provider it was served by, or the resource it names, is one of the
suite's test doubles (TEST_DOUBLES). Nothing else is touched. The native floor's rows from the same window are left:
nothing marks them as tests, and moving them is the Owner's decision (recommended no).

WHAT THIS DOES, AND DOES NOT
  - DRY RUN BY DEFAULT. It prints the plan and writes it to a file. `--apply` is required to move anything.
  - NOTHING IS DELETED. The rows are taken out of the record under its store lock and written whole into
    <data>/_pruned_ops_<stamp>/manifest.json, each with the position it held. The record is rewritten atomically.
  - `--restore <manifest>` puts every row back where it was. If the record has changed since, the rows go back in
    time order, and it says which.
  - It REFUSES to write while a backend answers on its port, since two writers of one record lose data. It refuses
    a record it cannot read whole, and a record it did not find (it examined nothing).

USAGE
    python scripts/quarantine_test_double_rows.py                      # the plan; moves nothing
    python scripts/quarantine_test_double_rows.py --apply              # move, and write the manifest
    python scripts/quarantine_test_double_rows.py --restore <manifest> # put it all back
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import time
from collections import Counter
from typing import Any, Dict, List

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from agentic_core.config import (StoreUnavailable, atomic_write_json, data_path, read_json_strict,  # noqa: E402
                                 store_lock)

RECORD = "operations_outcomes.json"
#  the providers the suite's own test doubles are named. "flaky" is the one test_orchestrator_adapts_to_model_health
#  records; a guard holds this set against that test
TEST_DOUBLES = frozenset({"flaky"})


def is_test_double(row: Any) -> bool:
    if not isinstance(row, dict):
        return False
    served = str(row.get("served_by") or "")
    resource = str(row.get("resource") or "")
    return served in TEST_DOUBLES or resource in {f"model:{n}" for n in TEST_DOUBLES}


def _rule_module():
    """The test-entity rule's own script, loaded from its file (scripts/ is not put on the import path)."""
    import importlib.util
    name = "quarantine_test_entities"
    mod = sys.modules.get(name)
    if mod is None:
        spec = importlib.util.spec_from_file_location(name, pathlib.Path(__file__).resolve().parent / f"{name}.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    return mod


def _busy() -> str:
    """Why this must not write now, or '': the test-entity rule's own refusal (a backend answering on its port)."""
    return _rule_module()._busy()


def _digest(rows: List[Any]) -> str:
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode("utf-8")).hexdigest()


def plan(root: pathlib.Path) -> Dict[str, Any]:
    """What would move. A record that is not there is examined=False; one that cannot be read whole raises."""
    path = root / RECORD
    if not path.exists():
        return {"root": str(root), "record": RECORD, "examined": False, "eligible": [], "counts": {"rows": 0}}
    rows = read_json_strict(path, None, expect=list)
    eligible = [{"index": i, "row": r} for i, r in enumerate(rows) if is_test_double(r)]
    served = Counter(str((e["row"] or {}).get("served_by")) for e in eligible)
    return {"root": str(root), "record": RECORD, "examined": True, "rule": {"test_doubles": sorted(TEST_DOUBLES)},
            "eligible": eligible,
            "counts": {"rows": len(rows), "eligible": len(eligible), "left": len(rows) - len(eligible),
                       "eligible_by_served_by": dict(served)}}


def apply(root: pathlib.Path, stamp: str) -> pathlib.Path:
    """Take the rows out, under the record's lock, re-reading it there: the plan may be older than the record."""
    path = root / RECORD
    qdir = root / f"_pruned_ops_{stamp}"
    with store_lock(path):
        rows = read_json_strict(path, [], expect=list)
        taken = [{"index": i, "row": r} for i, r in enumerate(rows) if is_test_double(r)]
        if not taken:
            raise SystemExit("REFUSING: no row in the record is a test double's, so there is nothing to move")
        left = [r for r in rows if not is_test_double(r)]
        qdir.mkdir(parents=True, exist_ok=False)
        manifest = {"stamp": stamp, "root": str(root), "record": RECORD, "rule": {"test_doubles": sorted(TEST_DOUBLES)},
                    "taken": taken, "rows_before": len(rows), "left_digest": _digest(left),
                    "note": ("a reversible move under the Owner's ruling of 2026-10-12 (FU-1040); "
                             "--restore puts every row back")}
        atomic_write_json(qdir / "manifest.json", manifest)        # the rows are kept before the record changes
        atomic_write_json(path, left)
    return qdir / "manifest.json"


def restore(manifest_path: pathlib.Path) -> str:
    m = read_json_strict(manifest_path, None, expect=dict)
    path = pathlib.Path(m["root"]) / m["record"]
    with store_lock(path):
        rows = read_json_strict(path, [], expect=list) if path.exists() else []
        back = [t["row"] for t in m["taken"]]
        if any(r in rows for r in back):
            raise SystemExit("REFUSING: the record already holds rows this manifest took out (restored already?)")
        if _digest(rows) == m["left_digest"]:
            for t in sorted(m["taken"], key=lambda t: t["index"]):
                rows.insert(t["index"], t["row"])
            how = "each where it was"
        else:
            #  the record changed since, so the positions no longer hold: every row in time order
            rows = sorted(rows + back, key=lambda r: str((r or {}).get("created_at") or ""))
            how = "in time order (the record changed after they were moved)"
        atomic_write_json(path, rows)
    return f"restored {len(back)} row(s), {how}"


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", metavar="MANIFEST")
    ap.add_argument("--root", default="", help="the data root (default: the configured data directory)")
    ap.add_argument("--list-out", default="", help="where to write the plan (default: <data>/_prune_ops_plan.json)")
    a = ap.parse_args(argv)
    if a.restore:
        why = _busy()
        if why:
            print(f"REFUSING to restore: {why}")
            return 1
        print(restore(pathlib.Path(a.restore)))
        return 0
    root = pathlib.Path(a.root or str(data_path("."))).resolve()
    try:
        pl = plan(root)
    except StoreUnavailable as e:
        print(f"REFUSING: the record cannot be read whole, so nothing is planned or moved ({e})")
        return 1
    if not pl["examined"]:
        print(f"REFUSING: examined nothing - there is no {RECORD} under {root}, so there is nothing to plan.")
        return 1
    out = pathlib.Path(a.list_out) if a.list_out else root / "_prune_ops_plan.json"
    atomic_write_json(out, pl)
    c = pl["counts"]
    print(f"rows {c['rows']} · a test double's {c['eligible']} {c['eligible_by_served_by']} · left {c['left']}")
    print(f"the exact plan is in {out}")
    if not a.apply:
        print("DRY RUN - nothing moved.")
        return 0
    busy = _busy()
    if busy:
        print(f"REFUSING to apply: {busy}")
        return 1
    print(f"moved {c['eligible']} row(s) aside; manifest: {apply(root, time.strftime('%Y%m%d-%H%M%S'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
