"""Back up, verify and restore Workstation's file stores (W918, FU-742 part 1).

Every store is a file under one data root: WORKSTATION_DATA_DIR where it is set, otherwise DATA_DIR, otherwise the
repository's data/ folder (agentic_core/store_paths.py; W893). This tool reads that root the way the stores do, by
importing the same two modules, never by a path of its own.

    python scripts/backup_stores.py backup --to D:\\workstation-backups
    python scripts/backup_stores.py verify D:\\workstation-backups\\workstation-stores-<time>.zip
    python scripts/backup_stores.py restore D:\\workstation-backups\\workstation-stores-<time>.zip --into D:\\restored-data

Stop the backend first. A store written during the copy is copied as it was at that moment, and two stores that
change together can be caught between their writes.

backup writes one archive holding every file under the data root and a manifest of each file's size and SHA-256,
computed from the bytes written into the archive. It refuses, and writes nothing, when:
- the destination is inside the repository: the archive holds the stores, personal data among them, and data/ is
  never committed;
- the destination is inside the data root, where the next backup would contain this one;
- the data root holds no file: a backup of nothing is not a backup;
- a store is configured outside the data root (a second data root, WORKSTATION_UEG_PATH or PROJECTS_DIR): the
  archive would leave it out, so it is named instead.

verify checks every file in an archive against its manifest: missing, extra and changed files are each named.

restore refuses a folder that is not empty, so nothing is ever overwritten. It checks the archive before it writes
anything, then checks every file it wrote against the manifest. Point DATA_DIR at the folder to use the restored
stores.

Nothing here schedules a backup, copies one off the machine, or deletes one. Exit codes: 0 done; 1 a check failed;
2 refused: no archive written by backup, nothing written by restore."""
import argparse
import hashlib
import json
import os
import sys
import time
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = "MANIFEST.json"
PREFIX = "data/"
CHUNK = 1 << 20


def _say(text: str) -> None:
    print(text, flush=True)


def _roots():
    """The data root as the stores resolve it: agentic_core.config.data_path and agentic_core/store_paths.py."""
    sys.path.insert(0, str(REPO))
    from agentic_core.config import data_path
    from agentic_core.store_paths import DATA_DIR
    return Path(data_path()).resolve(), Path(DATA_DIR).resolve()


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _outside_stores(root: Path, other: Path):
    """Every store configured outside the data root, with what it is."""
    out = []
    if other != root:
        out.append(("a second data root (agentic_core/store_paths.py)", other))
    for label, env in (("the tamper-evident trail (WORKSTATION_UEG_PATH)", "WORKSTATION_UEG_PATH"),
                       ("the projects store (PROJECTS_DIR)", "PROJECTS_DIR")):
        value = os.environ.get(env)
        if value and not _inside(Path(value).resolve(), root):
            out.append((label, Path(value).resolve()))
    return out


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def backup(to: Path) -> int:
    root, other = _roots()
    to = to.resolve()
    if _inside(to, REPO):
        _say(f"REFUSED: {to} is inside the repository ({REPO}). The archive holds the stores, personal data among "
             f"them, and data/ is never committed. Choose a folder outside the repository. No archive was written.")
        return 2
    if _inside(to, root):
        _say(f"REFUSED: {to} is inside the data root ({root}), so the next backup would contain this one. Choose a "
             f"folder outside it. No archive was written.")
        return 2
    outside = _outside_stores(root, other)
    if outside:
        _say("REFUSED: these stores are configured outside the data root, and a backup of the root would leave them "
             "out: " + "; ".join(f"{label} at {path}" for label, path in outside)
             + f". Point them inside {root} (one data root, W893), or back them up on their own. No archive was written.")
        return 2
    files = sorted(p for p in root.rglob("*") if p.is_file()) if root.is_dir() else []
    if not files:
        _say(f"REFUSED: examined nothing - the data root {root} holds no file, so there is nothing to back up. A "
             f"backup of nothing is not a backup. No archive was written.")
        return 2
    to.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = to / f"workstation-stores-{stamp}.zip"
    n = 1
    while out.exists():
        n += 1
        out = to / f"workstation-stores-{stamp}-{n}.zip"
    partial = out.with_name(out.name + ".partial")
    entries = []
    with zipfile.ZipFile(partial, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as z:
        for p in files:
            rel = p.relative_to(root).as_posix()
            info = zipfile.ZipInfo.from_file(p, PREFIX + rel)
            info.compress_type = zipfile.ZIP_DEFLATED
            h, size = hashlib.sha256(), 0
            #  the manifest hashes the bytes written into the archive, read once, never a second read of the file
            with open(p, "rb") as src, z.open(info, "w", force_zip64=True) as dst:
                for chunk in iter(lambda: src.read(CHUNK), b""):
                    h.update(chunk)
                    dst.write(chunk)
                    size += len(chunk)
            entries.append({"path": rel, "bytes": size, "sha256": h.hexdigest()})
        manifest = {"tool": "scripts/backup_stores.py", "made_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "data_root": str(root), "file_count": len(entries),
                    "total_bytes": sum(e["bytes"] for e in entries), "files": entries,
                    "note": ("every file under the data root, as read during the copy; stop the backend first. "
                             "Restore with: python scripts/backup_stores.py restore <this archive> --into <empty folder>")}
        z.writestr(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False))
    os.replace(partial, out)
    _say(f"backed up {len(entries)} files ({manifest['total_bytes']} bytes) from {root} into {out}. Verify it with: "
         f"python scripts/backup_stores.py verify \"{out}\"")
    return 0


def _check(z: zipfile.ZipFile):
    """What is wrong with an archive against its own manifest, each fault named; [] when nothing is."""
    try:
        manifest = json.loads(z.read(MANIFEST).decode("utf-8"))
        listed = {PREFIX + e["path"]: e for e in manifest["files"]}
    except (KeyError, ValueError, TypeError) as exc:
        return None, [f"the archive's manifest cannot be read ({exc.__class__.__name__})"]
    held = {n for n in z.namelist() if n != MANIFEST}
    if not listed:                    # W919 - a check of an archive that lists no file examined nothing
        return manifest, ["examined nothing - the archive's manifest lists no file, so there is nothing to check"]
    faults = [f"missing from the archive: {n[len(PREFIX):]}" for n in sorted(set(listed) - held)]
    faults += [f"in the archive and not in its manifest: {n}" for n in sorted(held - set(listed))]
    for name, e in sorted(listed.items()):
        if name not in held:
            continue
        h, size = hashlib.sha256(), 0
        try:
            with z.open(name) as f:
                for chunk in iter(lambda: f.read(CHUNK), b""):
                    h.update(chunk)
                    size += len(chunk)
        except (zipfile.BadZipFile, OSError) as exc:
            faults.append(f"cannot be read from the archive: {e['path']} ({exc})")
            continue
        if h.hexdigest() != e["sha256"] or size != e["bytes"]:
            faults.append(f"changed since the backup: {e['path']}")
    return manifest, faults


def verify(archive: Path) -> int:
    try:
        with zipfile.ZipFile(archive) as z:
            manifest, faults = _check(z)
    except (zipfile.BadZipFile, OSError) as exc:
        _say(f"FAILED: {archive} cannot be opened as an archive ({exc}).")
        return 1
    for f in faults:
        _say(f"FAILED: {f}")
    if faults:
        _say(f"{archive} does not match its manifest ({len(faults)} fault(s)). Do not restore from it.")
        return 1
    _say(f"verified {manifest['file_count']} files ({manifest['total_bytes']} bytes) in {archive} against its "
         f"manifest, made {manifest['made_at']} from {manifest['data_root']}.")
    return 0


def restore(archive: Path, into: Path) -> int:
    into = into.resolve()
    if into.exists() and (not into.is_dir() or any(into.iterdir())):
        _say(f"REFUSED: {into} is not empty, and a restore never overwrites anything. Restore into an empty or new "
             f"folder. Nothing was written.")
        return 2
    try:
        with zipfile.ZipFile(archive) as z:
            manifest, faults = _check(z)
            if faults:
                for f in faults:
                    _say(f"FAILED: {f}")
                _say(f"{archive} does not match its manifest, so nothing was restored.")
                return 1
            for e in manifest["files"]:
                target = into.joinpath(*e["path"].split("/"))
                if not _inside(target.resolve(), into):
                    _say(f"FAILED: {e['path']} would be written outside {into}, so nothing more was restored.")
                    return 1
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(PREFIX + e["path"]) as src, open(target, "wb") as dst:
                    for chunk in iter(lambda: src.read(CHUNK), b""):
                        dst.write(chunk)
    except (zipfile.BadZipFile, OSError) as exc:
        _say(f"FAILED: {archive} cannot be read ({exc}).")
        return 1
    #  every file written is read back and checked against the manifest
    wrong = [e["path"] for e in manifest["files"]
             if _sha256(into.joinpath(*e["path"].split("/"))) != e["sha256"]]
    for w in wrong:
        _say(f"FAILED: restored, and does not match the manifest: {w}")
    if wrong:
        return 1
    _say(f"restored {manifest['file_count']} files ({manifest['total_bytes']} bytes) into {into}, each checked against "
         f"the manifest. To use them, stop the backend, set DATA_DIR to {into}, and start it again.")
    return 0


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(errors="backslashreplace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("backup", help="write one archive of every file under the data root")
    b.add_argument("--to", required=True, type=Path, help="a folder outside the repository and the data root")
    v = sub.add_parser("verify", help="check an archive against its manifest")
    v.add_argument("archive", type=Path)
    r = sub.add_parser("restore", help="restore an archive into an empty folder")
    r.add_argument("archive", type=Path)
    r.add_argument("--into", required=True, type=Path, help="an empty or new folder")
    a = ap.parse_args(argv)
    if a.cmd == "backup":
        return backup(a.to)
    if a.cmd == "verify":
        return verify(a.archive)
    return restore(a.archive, a.into)


if __name__ == "__main__":
    sys.exit(main())
