"""P5.22 (W972) - EARLIER LEDGERS STAY BYTE-IDENTICAL (ACCEPT property 6).

The final audit writes a new edition of the vision fidelity ledger, and it must not touch the editions before it. The
current edition is docs/VISION_FIDELITY_LEDGER.md, and each earlier one is kept whole at
docs/VISION_FIDELITY_LEDGER_v<N>.md. docs/LEDGER_BLOBS.json pins every edition by its git blob id. This check holds that:
  - each earlier edition is still the blob it was pinned at, in its own file;
  - the current edition is its pinned blob where it stands until a new edition replaces it. From then on it is kept
    whole in its own numbered file, and an audit that writes over it without keeping it fails;
  - a new edition written in its place is pinned, as the next edition, in the round that writes it;
  - every numbered edition in the tree is pinned, because one that is not would be unguarded.

It reads the tree as it stands: the files a round is about to commit, or a checkout of what was committed. A file is
its pinned blob when git would store that blob for it, read either way: with this machine's line-ending settings
applied, or with its bytes as they are. Raw bytes alone would not do. A checkout can convert line endings
(core.autocrlf), so the same edition can be different bytes on two machines while git holds one blob. Both readings
are needed because, with the conversion on, git converts a file's CRLF line endings back when it reads it, except in
a file committed with CRLF, which it leaves as it is (edition 3 is one).

    python scripts/ledger_blobs.py     # ok, or each edition that changed, went missing, was not kept or is not pinned

The audit run records under docs/fidelity_runs/ are not read here. Nothing here writes to git: it hashes files
without storing them."""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
PINS = ROOT / "docs" / "LEDGER_BLOBS.json"
CURRENT = "docs/VISION_FIDELITY_LEDGER.md"
NUMBERED = re.compile(r"^docs/VISION_FIDELITY_LEDGER_v(\d+)\.md$")
#  the repository is the one the tree is in, whatever a caller's environment points git at
_GIT_ENV_DROPPED = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE")


def kept_at(edition: int) -> str:
    """The file an edition is kept whole in once a newer one replaces it."""
    return f"docs/VISION_FIDELITY_LEDGER_v{edition}.md"


def _git(root: pathlib.Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if k not in _GIT_ENV_DROPPED}
    out = subprocess.run(["git", *args], cwd=root, env=env, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {args[0]} failed in {root}: {out.stderr.strip()[:300]}")
    return out.stdout


def numbered_editions(root: pathlib.Path = ROOT) -> Dict[int, str]:
    """Every numbered edition in the tree: its edition, and its file."""
    found = {}
    for p in (root / "docs").glob("VISION_FIDELITY_LEDGER_v*.md"):
        m = NUMBERED.match(f"docs/{p.name}")
        if m:
            found[int(m.group(1))] = m.group(0)
    return found


def on_disk(paths, root: pathlib.Path = ROOT) -> Dict[str, Tuple[str, str]]:
    """For each file that is there: the blob git would store for it with this machine's line-ending settings applied,
    and the blob of its bytes as they are."""
    there = sorted({p for p in paths if (root / p).is_file()})
    if not there:
        return {}
    filtered = _git(root, "hash-object", "--", *there).split()
    raw = _git(root, "hash-object", "--no-filters", "--", *there).split()
    return {p: (f, r) for p, f, r in zip(there, filtered, raw)}


def _kept(label: str, rel: str, blob: str, disk: Dict[str, Tuple[str, str]]) -> List[str]:
    """How the file at rel is not the pinned blob, if it is not."""
    if rel not in disk:
        return [f"{label} is not there: {rel}"]
    if blob not in disk[rel]:
        return [f"{label} changed: {rel} is not the blob {blob[:12]} it was pinned at"]
    return []


def check(doc: dict, root: pathlib.Path = ROOT) -> List[str]:
    """Every way the tree breaks the pins. Empty means none."""
    editions = {int(n): b for n, b in (doc.get("editions") or {}).items()}
    current = doc.get("current_edition")
    if current not in editions:
        return [f"the current edition {current} is not among the pinned editions {sorted(editions)}"]
    numbered = numbered_editions(root)
    disk = on_disk([CURRENT, *numbered.values(), *(kept_at(n) for n in editions)], root)
    problems: List[str] = []
    for n in sorted(editions):
        blob = editions[n]
        if n > current:
            problems.append(f"edition {n} is pinned, and is later than the current edition {current}")
        elif n < current:
            problems += _kept(f"edition {n}", kept_at(n), blob, disk)
        elif kept_at(n) in disk:
            #  replaced in this tree: kept whole in its own file, and what replaced it is a new edition, pinned
            problems += _kept(f"edition {n}", kept_at(n), blob, disk)
            if CURRENT not in disk:
                problems.append(f"{CURRENT} is not there, so the tree has no current edition")
            elif blob not in disk[CURRENT]:
                problems.append(f"{CURRENT} holds a new edition that is not pinned: pin it as edition {n + 1} and make "
                                "it the current edition")
        elif CURRENT in disk and blob not in disk[CURRENT]:
            problems.append(f"edition {n} (the current one) was written over in {CURRENT} and is not kept whole in "
                            f"{kept_at(n)}")
        else:
            problems += _kept(f"edition {n} (the current one)", CURRENT, blob, disk)
    for n, rel in sorted(numbered.items()):
        if n not in editions:
            problems.append(f"{rel} is an edition in the tree that is not pinned")
    return problems


def main(argv: List[str] | None = None) -> int:
    try:
        doc = json.loads(PINS.read_text(encoding="utf-8"))
        if not isinstance(doc, dict):
            raise ValueError("the pins are not an object")
    except Exception as e:                                   # noqa: BLE001 - said, never read as nothing pinned
        print(f"REFUSING: the pins could not be read ({type(e).__name__}: {e}). That is not a pass.")
        return 2
    editions = doc.get("editions") or {}
    if not editions:
        print("REFUSING: examined nothing - no edition of the ledger is pinned, so none was checked. That is not a pass.")
        return 2
    try:
        problems = check(doc)
    except RuntimeError as e:
        print(f"REFUSING: {e}. That is not a pass.")
        return 2
    if problems:
        for p in problems:
            print(f"  {p}")
        print(f"FAIL - {len(problems)} problem(s) across {len(editions)} pinned edition(s)")
        return 1
    print(f"ok - {len(editions)} edition(s) of the ledger are each the blob they were pinned at; the current one is "
          f"edition {doc.get('current_edition')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
