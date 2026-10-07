#!/usr/bin/env python3
"""Which records name each VSB entity, across EVERY record kind in the data store. Read-only: it deletes nothing.

WHY THIS EXISTS (FU-459, Owner ruling 2026-10-07: "an accurate scan, no deletion"). The R13 entity split
offered 112 entities as "referenced ONLY by an auto-seeded business plan". The column behind that figure
checked a few artefact kinds, a repo and a business plan, and never looked at the economy records. Every one
of the 112 had non-zero owner-payment history. An absence in a coverage column is evidence only if it means
CHECKED AND NOT FOUND, and that column could not mean it.

So this scan does not choose which kinds to check. It walks every JSON file under the data root, derives each
file's KIND from its path, and reports for every entity which kinds name it. The kinds it scanned are printed
with their file counts, so a reader can see what "not found" covers. An entity's OWN footprint (a file whose
name carries its id, such as its ledger, repo or plan) is reported separately from a CROSS-REFERENCE (a
platform-level record such as owner payments or the ventures portfolio naming it). Deleting an entity a
cross-reference names would leave that record pointing at nothing.

It removes nothing and has no option to. A rule for what makes a fixture removable once it has accrued virtual
WST is the Owner's (FU-459). The prune, if ruled, goes through scripts/prune_test_entities.py and its guard.

USAGE
    python scripts/entity_coverage_scan.py              # summary + the kinds scanned
    python scripts/entity_coverage_scan.py --json       # the full per-entity report
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from agentic_core.config import data_path  # noqa: E402

_ID_RE = re.compile(r"vsb-[0-9a-f]{6,}")
#  any other id-like token in a PATH (a hash-named marketplace file, a per-worker suffix) is folded too, so one
#  record kind is reported once rather than once per file
_PATH_ID_RE = re.compile(r"vsb-[0-9a-f]{6,}|[0-9a-f]{8,}|__gw\d+")


def _kind(rel: pathlib.PurePath) -> str:
    """A file's record kind from its path: the top directory plus the file stem, with ids folded out."""
    parts = list(rel.parts)
    stem = _PATH_ID_RE.sub("<id>", rel.stem)
    return "/".join([_PATH_ID_RE.sub("<id>", p) for p in parts[:-1]] + [stem])


def scan(root: pathlib.Path) -> Dict[str, Any]:
    entities: Dict[str, Dict[str, Any]] = {}
    estore = root / "vsb_entities"
    for p in sorted(estore.glob("*.json")) if estore.exists() else []:
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            doc = {}
        vid = str((doc or {}).get("vsb_id") or p.stem)
        entities[vid] = {"vsb_id": vid, "name": (doc or {}).get("name"), "owner_id": (doc or {}).get("owner_id"),
                         "own_footprint": set(), "cross_references": set()}
    kinds: Dict[str, int] = {}
    unreadable: List[str] = []
    for p in sorted(root.rglob("*.json")):
        rel = p.relative_to(root)
        if rel.parts and rel.parts[0] == "vsb_entities":
            continue                       # the entity record itself is not a reference to it
        k = _kind(rel)
        kinds[k] = kinds.get(k, 0) + 1
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            unreadable.append(str(rel))
            continue
        own = set(_ID_RE.findall(str(rel)))
        #  a file names an entity in its CONTENT or in its PATH: an entity's own ledger is keyed by the filename
        #  and need not repeat the id inside, and missing it would report a footprint as absent
        named = set(_ID_RE.findall(text)) | own
        for vid in named & set(entities):
            (entities[vid]["own_footprint"] if vid in own else entities[vid]["cross_references"]).add(k)
    rows = []
    for e in entities.values():
        rows.append({**e, "own_footprint": sorted(e["own_footprint"]),
                     "cross_references": sorted(e["cross_references"]),
                     "referenced_by_nothing": not e["own_footprint"] and not e["cross_references"]})
    return {"root": str(root), "entities": rows, "kinds_scanned": dict(sorted(kinds.items())),
            "unreadable": unreadable,
            "counts": {"entities": len(rows),
                       "with_cross_references": sum(1 for r in rows if r["cross_references"]),
                       "own_footprint_only": sum(1 for r in rows if r["own_footprint"] and not r["cross_references"]),
                       "referenced_by_nothing": sum(1 for r in rows if r["referenced_by_nothing"])},
            "basis": ("every JSON file under the data root was read and every record kind found is listed in "
                      "kinds_scanned with its file count; 'not found' means not named by ANY of them. Nothing was "
                      "deleted, and this scan cannot delete.")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rep = scan(pathlib.Path(str(data_path("."))).resolve())
    if a.json:
        print(json.dumps(rep, indent=1, default=list))
        return 0
    c = rep["counts"]
    print(f"entities: {c['entities']} · named by a cross-reference: {c['with_cross_references']} · own footprint "
          f"only: {c['own_footprint_only']} · named by nothing: {c['referenced_by_nothing']}")
    print(f"record kinds scanned ({len(rep['kinds_scanned'])}):")
    for k, n in rep["kinds_scanned"].items():
        print(f"  {k}  ({n} file{'s' if n != 1 else ''})")
    if rep["unreadable"]:
        print(f"UNREADABLE, so not scanned: {rep['unreadable']}")
    print(rep["basis"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
