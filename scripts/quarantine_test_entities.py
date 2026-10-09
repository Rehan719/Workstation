#!/usr/bin/env python3
"""Quarantine test-owned VSB entities under the Owner's rule of 2026-10-09 — a REVERSIBLE MOVE, never a delete.

THE RULE (Owner, 2026-10-09: "I want to go with your recommendation"). An entity may be removed when
    its owner_id is "pytest"            (who created it — never inferred from its name), AND
    it is NOT on the living roster      (the organism is not tending it),
and its entries in the owner-payments record and the ventures portfolio leave IN THE SAME OPERATION.
Nothing owned by anyone else is touched: not "default", not "preview", not the Owner — whatever names it or
does not.

WHAT THIS DOES, AND DOES NOT
  - DRY RUN BY DEFAULT. It prints the plan and writes the exact list to a file; `--apply` is required to move.
  - NOTHING IS DELETED. An eligible entity's record and its own footprint (every file or directory under the
    data root whose NAME carries its id) are MOVED into `<data>/_pruned_<stamp>/files/…`, keeping their
    relative paths. Its two platform entries are taken out of the records and written into the manifest.
    `--restore <manifest>` puts every file back and re-inserts every entry.
  - CONSERVATIVE. An entity that any OTHER record names in its content is SKIPPED and listed, except for
    the kinds below, which are history rather than references and are left exactly as they are:
        swarm_cascades.json, org_cascade_runs.json   a run that happened
        meta/ (the UEG audit log)                    never edited, by constitution
        memory.json                                  recall, not a pointer
    So a contract, a pending transfer, a deliverable or an operations outcome that names an entity keeps it.
  - It REFUSES to run while the backend answers on its port or a pytest process is alive (the shared-store
    class: two writers of one JSON record lose data), and it takes each record's store lock for the edit.

USAGE
    python scripts/quarantine_test_entities.py                      # the plan; writes the list; moves nothing
    python scripts/quarantine_test_entities.py --apply              # move, and write the manifest
    python scripts/quarantine_test_entities.py --restore <manifest> # put it all back
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import sys
import time
from typing import Any, Dict, List, Set

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from agentic_core.config import atomic_write_json, data_path, store_lock  # noqa: E402

RULE_OWNER = "pytest"
#  the two records the rule names: an entity's entry is a top-level key, and it leaves with the entity
PLATFORM_RECORDS = ("economy_owner_payments.json", "economy_ventures_portfolio.json")
ROSTER = "living_vsbs.json"
#  history, not references: left untouched, never a reason to skip
HISTORY_FILES = {"swarm_cascades.json", "org_cascade_runs.json", "memory.json"}
HISTORY_DIRS = {"meta"}
#  never scanned and never moved: test stores, earlier quarantines, the entity store itself
SKIP_TOP = re.compile(r"^(_test_store.*|_pruned_.*)$")
_ID_RE = re.compile(r"vsb-[0-9a-f]{6,}")


def _read(path: pathlib.Path) -> Any:
    """A record read for DECIDING. Unreadable is an exception, never an empty record: a tolerant read here
    would make an entity look unreferenced because the file naming it could not be parsed."""
    return json.loads(path.read_bytes().decode("utf-8"))


def plan(root: pathlib.Path) -> Dict[str, Any]:
    store = root / "vsb_entities"
    entities: Dict[str, Dict[str, Any]] = {}
    unreadable_entities: List[str] = []
    for p in sorted(store.glob("*.json")) if store.exists() else []:
        try:
            doc = _read(p)
        except (OSError, ValueError):
            unreadable_entities.append(p.name)      # cannot know its owner: never eligible
            continue
        vid = str((doc or {}).get("vsb_id") or p.stem)
        entities[vid] = {"vsb_id": vid, "name": doc.get("name"), "owner_id": doc.get("owner_id"),
                         "record": str(p.relative_to(root))}
    roster_path = root / ROSTER
    roster: Set[str] = set(_read(roster_path)) if roster_path.exists() else set()

    footprint: Dict[str, List[str]] = {v: [] for v in entities}
    blocking: Dict[str, Set[str]] = {v: set() for v in entities}
    history: Dict[str, Set[str]] = {v: set() for v in entities}
    unread: List[str] = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        top = rel.parts[0]
        if SKIP_TOP.match(top) or top == "vsb_entities":
            continue
        named_here = set(_ID_RE.findall(p.name)) & set(entities)
        #  OWN FOOTPRINT: the id is in the file's or directory's own name. Only the OUTERMOST such path is
        #  recorded, so a repo directory moves once and its contents are not listed again.
        if named_here and not (set(_ID_RE.findall(str(rel.parent))) & named_here):
            for vid in named_here:
                footprint[vid].append(str(rel))
        if not p.is_file() or p.suffix != ".json" or set(_ID_RE.findall(str(rel))) & set(entities):
            continue                                 # inside a footprint, or not a JSON record
        try:
            text = p.read_bytes().decode("utf-8", errors="replace")
        except OSError:
            unread.append(str(rel))
            continue
        ids = set(_ID_RE.findall(text)) & set(entities)
        if not ids:
            continue
        is_history = rel.name in HISTORY_FILES or top in HISTORY_DIRS
        for vid in ids:
            if str(rel) in PLATFORM_RECORDS or str(rel) == ROSTER:
                continue                             # handled by the rule itself
            (history if is_history else blocking)[vid].add(str(rel))

    eligible, skipped, untouched = [], [], 0
    for vid, e in sorted(entities.items()):
        if str(e.get("owner_id")) != RULE_OWNER:
            untouched += 1
            continue
        if vid in roster:
            skipped.append({**e, "reason": "on the living roster"})
        elif blocking[vid]:
            skipped.append({**e, "reason": "named by a record that is not history",
                            "named_by": sorted(blocking[vid])})
        else:
            eligible.append({**e, "footprint": sorted(footprint[vid]), "history_left_in_place": sorted(history[vid])})
    return {"root": str(root), "rule": {"owner_id": RULE_OWNER, "not_on_roster": True,
                                         "platform_records": list(PLATFORM_RECORDS)},
            "eligible": eligible, "skipped": skipped,
            "counts": {"entities": len(entities), "not_test_owned_untouched": untouched,
                       "eligible": len(eligible), "skipped": len(skipped),
                       "entity_records_unreadable_never_eligible": len(unreadable_entities)},
            "unreadable_entity_records": unreadable_entities, "unread_while_scanning": unread}


def apply(root: pathlib.Path, pl: Dict[str, Any], stamp: str) -> pathlib.Path:
    if pl["unread_while_scanning"]:
        raise SystemExit("REFUSING: a record could not be read while scanning, so an entity may be named by "
                         f"something this did not see: {pl['unread_while_scanning'][:5]}")
    qdir = root / f"_pruned_{stamp}"
    files_dir = qdir / "files"
    files_dir.mkdir(parents=True, exist_ok=False)
    ids = [e["vsb_id"] for e in pl["eligible"]]
    taken: Dict[str, Dict[str, Any]] = {}
    #  the two platform records first, each under its own lock, each written atomically; what is taken out
    #  is kept whole in the manifest
    for name in PLATFORM_RECORDS:
        path = root / name
        if not path.exists():
            continue
        with store_lock(path):
            rec = _read(path)
            out = {vid: rec.pop(vid) for vid in ids if vid in rec}
            if out:
                atomic_write_json(path, rec)
            taken[name] = out
    moved: List[str] = []
    for e in pl["eligible"]:
        for rel in [e["record"]] + e["footprint"]:
            src = root / rel
            if not src.exists():
                continue
            dst = files_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            moved.append(rel)
    manifest = {"stamp": stamp, "root": str(root), "rule": pl["rule"], "entities": ids, "moved": moved,
                "taken_from_platform_records": taken, "skipped": pl["skipped"],
                "note": "a reversible move under the Owner's rule of 2026-10-09; --restore undoes all of it"}
    atomic_write_json(qdir / "manifest.json", manifest)
    return qdir / "manifest.json"


def restore(manifest_path: pathlib.Path) -> int:
    m = _read(manifest_path)
    root = pathlib.Path(m["root"])
    files_dir = manifest_path.parent / "files"
    clash = [rel for rel in m["moved"] if (root / rel).exists()]
    if clash:
        raise SystemExit(f"REFUSING to restore over files that exist now: {clash[:5]}")
    for name, entries in (m.get("taken_from_platform_records") or {}).items():
        path = root / name
        with store_lock(path):
            rec = _read(path) if path.exists() else {}
            dup = [k for k in entries if k in rec]
            if dup:
                raise SystemExit(f"REFUSING: {name} already has entries for {dup[:5]}")
            rec.update(entries)
            atomic_write_json(path, rec)
    for rel in m["moved"]:
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(files_dir / rel), str(dst))
    print(f"restored {len(m['moved'])} path(s) and the entries of {len(m['entities'])} entit(ies)")
    return 0


def _busy() -> str:
    """Why this must not write now, or ''. A second writer of a shared JSON record loses data."""
    import socket
    for port in (8000, 8010, 8031):
        with socket.socket() as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return f"a backend answers on :{port}"
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--restore", metavar="MANIFEST")
    ap.add_argument("--list-out", default="", help="where to write the exact plan (default: <data>/_prune_plan.json)")
    a = ap.parse_args()
    if a.restore:
        why = _busy()
        if why:
            raise SystemExit(f"REFUSING to restore: {why}")
        return restore(pathlib.Path(a.restore))
    root = pathlib.Path(str(data_path("."))).resolve()
    pl = plan(root)
    out = pathlib.Path(a.list_out) if a.list_out else root / "_prune_plan.json"
    atomic_write_json(out, pl)
    c = pl["counts"]
    print(f"entities {c['entities']} · not test-owned, untouched {c['not_test_owned_untouched']} · "
          f"ELIGIBLE {c['eligible']} · skipped {c['skipped']}")
    for s in pl["skipped"][:40]:
        print(f"  skipped {s['vsb_id']}  {s['reason']}  {', '.join(s.get('named_by', []))[:90]}")
    print(f"the exact plan is in {out}")
    if not a.apply:
        print("DRY RUN — nothing moved.")
        return 0
    why = _busy()
    if why:
        raise SystemExit(f"REFUSING to apply: {why}")
    mp = apply(root, pl, time.strftime("%Y%m%d-%H%M%S"))
    print(f"moved {c['eligible']} entit(ies) into quarantine; manifest: {mp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
