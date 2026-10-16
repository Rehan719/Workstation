"""RESOLVE AN EXPOSURE (W732) - move tracked files out of this public repository into a private folder, without
losing a byte. Generalised from the move W731 made on the Owner's word.

    python scripts/move_to_private_store.py --dest <private folder> <path or folder/> [...]          (dry run)
    python scripts/move_to_private_store.py --dest <private folder> <path or folder/> [...] --apply

For every tracked file under the given paths: COPY to <dest>/<same relative path>, prove the copy byte-identical
by sha256, write MANIFEST_<n>.json beside the copies, and only then `git rm` it here. It refuses a destination
inside the repository, and refuses to overwrite a file already at the destination. Git HISTORY still holds the
files afterwards: rewriting history is the Owner's own decision (docs/PRIVACY_EXPOSURE_RUNBOOK.md). Add the
moved folders to .gitignore and to agentic_core/privacy_exposure.PRIVATE_FOLDERS in the same commit.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]


def plan(root: pathlib.Path, targets):
    r = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("the tracked files could not be listed - nothing moved")
    tracked = [x for x in r.stdout.decode("utf-8", "replace").split("\0") if x]
    out = sorted(f for f in tracked if any(f == t or (t.endswith("/") and f.startswith(t)) for t in targets))
    empty = [t for t in targets if not any(f == t or (t.endswith("/") and f.startswith(t)) for f in tracked)]
    return out, empty


def move(root: pathlib.Path, dest: pathlib.Path, targets, apply: bool = False) -> dict:
    dest = dest.resolve()
    if str(dest).lower().startswith(str(root.resolve()).lower()):
        raise SystemExit("the destination is inside the repository - that would not make anything private")
    files, empty = plan(root, targets)
    if empty:
        raise SystemExit(f"nothing tracked under: {empty} - nothing moved")
    clash = [f for f in files if (dest / f).exists()]
    if clash:
        raise SystemExit(f"{len(clash)} file(s) already at the destination (first: {clash[0]}) - nothing moved")
    if not apply:
        return {"applied": False, "files": len(files), "dest": str(dest)}
    manifest = []
    for rel in files:
        src, dst = root / rel, dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        a, b = (hashlib.sha256(p.read_bytes()).hexdigest() for p in (src, dst))
        if a != b:
            raise SystemExit(f"the copy of {rel} differs from the original - stopped; nothing was removed")
        manifest.append({"path": rel, "sha256": a, "bytes": src.stat().st_size})
    n = len(list(dest.glob("MANIFEST_*.json"))) + 1
    (dest / f"MANIFEST_{n}.json").write_text(json.dumps({
        "moved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "from": str(root),
        "history": "git history still holds these files; rewriting it is the Owner's own decision",
        "files": manifest}, indent=2), encoding="utf-8")
    for i in range(0, len(files), 100):
        r = subprocess.run(["git", "-C", str(root), "rm", "-q", "--"] + files[i:i + 100], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"git rm failed after the copies were verified (they are kept at {dest}): {r.stderr[:200]}")
    return {"applied": True, "files": len(files), "dest": str(dest), "manifest": f"MANIFEST_{n}.json"}


def main(argv) -> int:
    if "--dest" not in argv:
        print(__doc__)
        return 2
    i = argv.index("--dest")
    dest = pathlib.Path(argv[i + 1])
    targets = [a.replace("\\", "/") for j, a in enumerate(argv) if j not in (i, i + 1) and a != "--apply"]
    if not targets:
        print("name at least one tracked path or folder/ to move")
        return 2
    res = move(ROOT, dest, targets, apply="--apply" in argv)
    print(("moved " if res["applied"] else "dry run: would move ") + f"{res['files']} file(s) to {res['dest']}"
          + (f"; manifest {res['manifest']}" if res.get("manifest") else " (add --apply)"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
