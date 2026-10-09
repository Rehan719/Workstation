"""The live matter's ONE named folder: resolved, measured, and the only place a document may be opened from.

P3.23 (W605). The Owner's terms of 2026-10-03c: read-only indexing of ONE NAMED FOLDER, never sent to any external
service, provenance per document, and NO PATH OUTSIDE THAT FOLDER IS EVER OPENED. Before this module the terms
lived only as prose in legal/matter.json, beside a stored `bundle_indexing_may_start: false` whose own basis said
it must be a measurement of the folder, never an Owner switch, and nothing measured it. So:

  * resolve_bundle_dir() says which of three states the folder is in, and never creates, guesses or infers one;
  * may_start() is COMPUTED from the folder's contents every time it is asked;
  * open_document() is the only reader, and it refuses anything whose REAL path is not inside the REAL folder.

Containment is decided on resolved real paths with os.path.commonpath, not on a string prefix: a sibling folder
named `legal-matter-x` shares the prefix `legal-matter`, and a symlink inside the folder can point anywhere.
"""
from __future__ import annotations

import json
import os
import pathlib
from typing import Any, Dict, List, Optional

_MATTER_FILE = pathlib.Path(__file__).resolve().parent / "matter.json"

CONFIGURED_PRESENT = "configured_present"
CONFIGURED_ABSENT = "configured_absent"
UNSET = "unset"

#  the environment wins over matter.json, so a guard can drive a scratch folder; nothing else overrides it
ENV_VAR = "LEGAL_BUNDLE_DIR"


def _matter() -> Dict[str, Any]:
    try:
        return json.loads(_MATTER_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def resolve_bundle_dir() -> Dict[str, Any]:
    """Which folder, in which state, and why. Never creates the folder and never guesses one."""
    env = os.environ.get(ENV_VAR, "").strip()
    named = env or str(_matter().get("bundle_dir") or "").strip()
    source = (f"the {ENV_VAR} environment variable" if env else "agentic_core/legal/matter.json")
    if not named:
        return {"state": UNSET, "path": None, "source": None,
                "basis": "no folder is named, so no document can be read - which is the safe default"}
    p = pathlib.Path(named)
    if not p.is_dir():
        return {"state": CONFIGURED_ABSENT, "path": named, "source": source,
                "basis": (f"{named!r} is named by {source} but is not a folder on THIS machine, so nothing is "
                          f"read from it. That is not an empty folder: an empty folder exists and holds nothing, "
                          f"this one is not here at all. It is never created on the Owner's behalf")}
    return {"state": CONFIGURED_PRESENT, "path": os.path.realpath(str(p)), "source": source,
            "basis": f"the folder named by {source} exists on this machine"}


def list_documents() -> Dict[str, Any]:
    """Every regular file inside the folder, walked from inside it only. Symlinks are not followed out."""
    r = resolve_bundle_dir()
    if r["state"] != CONFIGURED_PRESENT:
        return {"documents": None, "count": None, "folder": r, "basis": r["basis"]}
    root = r["path"]
    docs: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            if os.path.isfile(full) and _inside(os.path.realpath(full), root):
                docs.append(os.path.relpath(full, root))
    docs.sort()
    return {"documents": docs, "count": len(docs), "folder": r,
            "basis": f"{len(docs)} document(s) found by walking the named folder and nothing outside it"}


def may_start() -> Dict[str, Any]:
    """Whether there is anything to index: a MEASUREMENT of the folder, never an Owner switch."""
    ls = list_documents()
    if ls["documents"] is None:
        return {"may_start": False, "count": None, "folder_state": ls["folder"]["state"],
                "basis": (f"false: {ls['basis']}. This is a measurement of the folder and NOT an Owner switch - "
                          f"the Owner approved the terms in 2026-10-03c; this says whether anything has been "
                          f"placed there")}
    n = ls["count"]
    return {"may_start": n > 0, "count": n, "folder_state": ls["folder"]["state"],
            "basis": (f"{'true' if n else 'false'}: the named folder holds {n} document(s), measured just now. "
                      f"This is NOT an Owner switch; copying a file in is the consent for that file")}


def _inside(real: str, root: str) -> bool:
    try:
        return os.path.commonpath([real, root]) == root
    except ValueError:            # different drives on Windows, or a relative/absolute mix
        return False


def open_document(path: str) -> Dict[str, Any]:
    """Read ONE document, read-only, or REFUSE naming the rule. The only reader of the matter's documents."""
    r = resolve_bundle_dir()
    if r["state"] != CONFIGURED_PRESENT:
        return {"opened": False, "refused": "no_folder", "text": None, "document": path, "basis": r["basis"]}
    root = r["path"]
    raw = str(path or "").strip()
    if not raw:
        return {"opened": False, "refused": "no_path", "text": None, "document": path,
                "basis": "REFUSED: no document was named"}
    candidate = raw if os.path.isabs(raw) else os.path.join(root, raw)
    real = os.path.realpath(candidate)
    if not _inside(real, root):
        return {"opened": False, "refused": "outside_the_named_folder", "text": None, "document": path,
                "basis": (f"REFUSED: {raw!r} resolves to a path outside the one named folder, and no document "
                          f"outside it is ever opened (Owner ruling 2026-10-03c). It was not read")}
    if not os.path.isfile(real):
        return {"opened": False, "refused": "not_a_document", "text": None, "document": path,
                "basis": f"REFUSED: {raw!r} is not a regular file inside the folder"}
    with open(real, "rb") as fh:        # read-only: nothing here writes, renames or deletes
        data = fh.read()
    return {"opened": True, "refused": None, "document": os.path.relpath(real, root),
            "text": data.decode("utf-8", errors="replace"),
            "basis": "read-only, from inside the one named folder"}


def status() -> Dict[str, Any]:
    """The surface's view: the folder's state, whether indexing may start, and the count. Never contents."""
    ms = may_start()
    r = resolve_bundle_dir()
    return {"folder_state": r["state"], "folder": r["path"], "folder_source": r["source"],
            "folder_basis": r["basis"], "bundle_indexing_may_start": ms["may_start"],
            "document_count": ms["count"], "bundle_indexing_basis": ms["basis"],
            "never": list(_matter().get("never") or [])}
