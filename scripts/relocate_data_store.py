"""W473 (register FU-026) — relocate the live AI data store from the repository's PARENT directory to the repository.

config/paths.py resolved BASE_DIR one level above the repository, so the live memory store, the interactions
database, the L7 registry, the meeting log and the chroma store lived at <repo-parent>/data. W473 points
BASE_DIR at the repository. This script moves the store the only honest way: COPY each file into the new
location, VERIFY the copy byte for byte, and only then does the code SWITCH (paths.py reads the new location;
it also refuses to run silently while the legacy store is larger than the new one). Nothing is deleted.

    python scripts/relocate_data_store.py            # report what would move
    python scripts/relocate_data_store.py --apply    # copy + verify

A target that already holds real data (not a test stub) is never overwritten: the script reports it and
stops for the Owner to decide.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEGACY = REPO.parent / "data"
NEW = REPO / "data"
FILES = ["memory.json", "interactions.db", "l7_registry.json", "meeting_log.json", "ingestion_registry.json",
         "qep_production.json"]
DIRS = ["chroma_db", "career_outputs"]


def _sha(p: Path) -> str:
    h = hashlib.sha3_256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sqlite_empty(p: Path) -> bool | None:
    """True when every table is empty, False when any holds rows, None when it is not a SQLite database."""
    import sqlite3
    try:
        c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
        tables = [r[0] for r in c.execute("select name from sqlite_master where type='table'")]
        empty = all(c.execute(f"select count(*) from [{t}]").fetchone()[0] == 0 for t in tables)
        c.close()
        return empty
    except Exception:
        return None


def _is_stub(p: Path) -> bool:
    """A placeholder the repository accumulated: a missing file, an empty list/object, a tiny fixture, or a SQLite
    database whose every table is empty (8 KiB of schema and no rows)."""
    if not p.exists():
        return True
    if p.suffix == ".db":
        return _sqlite_empty(p) is True
    if p.stat().st_size > 4096:
        return False
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return p.stat().st_size <= 64
    return data in ([], {})


def _json_list(p: Path):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    return d if isinstance(d, list) else None


def _json_equal(a: Path, b: Path) -> bool:
    """The same JSON value under different formatting is the same data."""
    try:
        return json.loads(a.read_text(encoding="utf-8")) == json.loads(b.read_text(encoding="utf-8"))
    except Exception:
        return False


def _disjoint_maps(a: Path, b: Path):
    """Two JSON objects with no key in common: their union loses nothing. Returns the union, or None."""
    try:
        da, db = json.loads(a.read_text(encoding="utf-8")), json.loads(b.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not (isinstance(da, dict) and isinstance(db, dict)) or set(da) & set(db):
        return None
    return {**db, **da}                       # the repository's entries first; the legacy ones join them


def _record_count(d) -> tuple:
    """W506 (FU-220) - how many RECORD-BEARING files a destination holds, and why if that cannot be told.

    Returns `(count, basis)`, or `(None, why)` when the directory cannot be inspected. A vector store keeps
    index, metadata and lock files whether or not it holds anything, so counting files answers the wrong
    question: `any(dst.iterdir())` reported a conflict over a collection with zero embeddings.

    STRUCTURE, not records: sqlite headers with no rows are not counted, and neither are the index and lock
    files a store maintains for itself. A JSON file holding an empty list or object is structure too.
    """
    import json as _json
    if not d.exists():
        return 0, "the destination does not exist"
    _STRUCTURE_SUFFIXES = {".lock", ".tmp", ".log"}
    _STRUCTURE_NAMES = {"index", "header.bin", "data_level0.bin", "length.bin", "link_lists.bin"}
    records = 0
    try:
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix in _STRUCTURE_SUFFIXES or p.name in _STRUCTURE_NAMES:
                continue
            if p.stat().st_size == 0:
                continue
            if p.suffix == ".json":
                try:
                    val = _json.loads(p.read_text(encoding="utf-8"))
                except Exception:
                    records += 1          # unreadable: assume it holds something rather than discard it
                    continue
                if val in ([], {}, None):
                    continue              # structure, not records
                records += 1
                continue
            records += 1
    except OSError as exc:
        return None, f"the destination could not be walked ({exc.__class__.__name__}: {exc})"
    return records, (f"{records} record-bearing file(s)" if records else
                     "no record-bearing files - only structure or empty documents")


def plan() -> list[dict]:
    rows = []
    for name in FILES:
        src, dst = LEGACY / name, NEW / name
        if not src.exists():
            continue
        if _is_stub(src) and dst.exists():
            action = "skip (legacy holds nothing)"          # an emptier legacy file never overwrites anything
        elif dst.exists() and not _is_stub(dst) and _json_list(src) is not None and _json_list(dst) is not None:
            # (refutation F12) two non-empty lists: equal or CONFLICT — a memory list is never merged by rule
            action = "same" if _json_list(src) == _json_list(dst) else "CONFLICT (both lists hold entries)"
        elif dst.exists() and not _is_stub(dst):
            if (src.stat().st_size == dst.stat().st_size and _sha(src) == _sha(dst)) or _json_equal(src, dst):
                action = "same"
            elif _disjoint_maps(src, dst) is not None:
                action = "merge (disjoint keys)"
            else:
                action = "CONFLICT"
        else:
            action = "copy"
        rows.append({"item": name, "kind": "file", "src": str(src), "dst": str(dst), "size": src.stat().st_size, "action": action})
    for name in DIRS:
        src, dst = LEGACY / name, NEW / name
        if not src.exists():
            continue
        # W506 (FU-220) - decided on CONTENT, not on emptiness. `any(dst.iterdir())` made ANY file a
        # conflict, and a vector store always carries index and metadata files whether or not anything is
        # stored in it - which is how FU-079 was registered as "two populated copies" of chroma_db when one
        # held 0 embeddings and the other held 1. A destination holding only structure is not a conflict.
        dst_records, dst_why = _record_count(dst)
        row = {"item": name, "kind": "dir", "src": str(src), "dst": str(dst),
               "size": sum(p.stat().st_size for p in src.rglob("*") if p.is_file())}
        if dst_records is None:
            # a comparison was not possible. "I could not tell" is not "they both hold data", and only one
            # of those is a reason to stop, so the row says which it is.
            row["action"] = "CONFLICT (the destination could not be inspected)"
            row["basis"] = dst_why
        elif dst_records > 0:
            row["action"] = "CONFLICT (the destination holds records)"
            row["basis"] = f"{dst_records} record-bearing file(s) at the destination"
        else:
            row["action"] = "copy"
            row["basis"] = (dst_why or "the destination holds no records - only structure, or nothing at "
                            "all - so a copy does not overwrite anything")
        rows.append(row)
    return rows


def apply_plan(rows: list[dict]) -> int:
    """Copies and merges every row the rules settle; a CONFLICT row is NOT moved and is named at the end for the
    Owner to decide (both copies stay where they are)."""
    NEW.mkdir(parents=True, exist_ok=True)
    for r in rows:
        src, dst = Path(r["src"]), Path(r["dst"])
        if r["action"].startswith("merge"):
            union = _disjoint_maps(src, dst)
            assert union is not None
            tmp = dst.with_suffix(dst.suffix + ".merge.tmp")
            tmp.write_text(json.dumps(union, indent=2), encoding="utf-8")
            ok = set(json.loads(tmp.read_text(encoding="utf-8"))) == set(json.loads(src.read_text(encoding="utf-8"))) | set(json.loads(dst.read_text(encoding="utf-8")))
            if ok:
                tmp.replace(dst)
            print(("verified " if ok else "MISMATCH ") + r["item"], "(merged, no key lost) ->", dst)
            if not ok:
                return 3
            continue
        if r["action"] != "copy":
            continue
        if r["kind"] == "file":
            shutil.copyfile(src, dst)
            ok = _sha(src) == _sha(dst)
        else:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            ok = sorted(p.relative_to(src) for p in src.rglob("*") if p.is_file()) == \
                 sorted(p.relative_to(dst) for p in dst.rglob("*") if p.is_file()) and \
                 all(_sha(p) == _sha(dst / p.relative_to(src)) for p in src.rglob("*") if p.is_file())
        print(("verified " if ok else "MISMATCH ") + r["item"], "->", dst)
        if not ok:
            return 3
    conflicts = [r for r in rows if r["action"].startswith("CONFLICT")]
    for r in conflicts:
        print("NOT MOVED (conflict — both copies hold data; the Owner decides):", r["item"], "->", r["dst"])
    print("done — the legacy store at", LEGACY, "was left in place (never deleted by this script)")
    return 2 if conflicts else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    rows = plan()
    if not rows:
        print("nothing to relocate: no legacy store at", LEGACY)
        return 0
    for r in rows:
        print(f"{r['action']:9} {r['kind']:4} {r['item']:24} {r['size']:>12,} B  {r['src']} -> {r['dst']}")
    if not args.apply:
        print("(dry run — pass --apply to copy and verify)")
        return 0
    return apply_plan(rows)


if __name__ == "__main__":
    sys.exit(main())
