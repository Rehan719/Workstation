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

W1129 (FU-1282): the folder is named ON THE MACHINE THAT HOLDS IT, by LEGAL_MATTER_FOLDER in that machine's own
.env, and never in a committed file; no answer carries its path.
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

#  a process names its own folder by this variable, and it wins, so a guard can drive a scratch folder: the suite,
#  the audit backend and the sign-in check set it to a folder of no one before anything is imported
ENV_VAR = "LEGAL_BUNDLE_DIR"
#  W1129 (FU-1282) - THE MACHINE'S OWN FOLDER is named by this, in that machine's own .env, and never in a committed
#  file: a committed path is a path on one person's machine, and P4.5's dry run (W1128) found it in the image and in
#  this module's answer. It is held back from a test, audit or drive process exactly as the committed path was (W676)
MACHINE_VAR = "LEGAL_MATTER_FOLDER"


def _matter() -> Dict[str, Any]:
    try:
        return json.loads(_MATTER_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


#  the names by which a process says it is not the Owner's own running platform
_NOT_THE_OWNERS = ("PYTEST_CURRENT_TEST", "PYTEST_XDIST_WORKER", "WORKSTATION_AUDIT_BACKEND", "WORKSTATION_DRIVE")


def _not_the_owners_process() -> str:
    """The first marker present, or ''. Also true when pytest is loaded in this interpreter."""
    for k in _NOT_THE_OWNERS:
        if os.environ.get(k):
            return k
    import sys as _sys
    return "pytest is loaded" if "pytest" in _sys.modules else ""


def resolve_bundle_dir() -> Dict[str, Any]:
    """Which folder, in which state, and why. Never creates the folder and never guesses one. The path is for the
    reader below: no basis names it, and status() does not answer with it (W1129)."""
    env = os.environ.get(ENV_VAR, "").strip()
    #  W676 - THE FLOOR. A test, audit or drive process is never handed the folder this machine names:
    #  what such a process reads ends up in a test log or an agent's transcript, and nothing about the matter
    #  leaves this machine. Such a process reads a folder only when ENV_VAR names one.
    held_back = not env and _not_the_owners_process()
    named = env or ("" if held_back else os.environ.get(MACHINE_VAR, "").strip())
    source = (f"the {ENV_VAR} environment variable" if env else f"this machine's {MACHINE_VAR} setting")
    if held_back:
        return {"state": UNSET, "path": None, "source": None, "held_back": True,
                "basis": (f"this is a test, audit or drive process ({_not_the_owners_process()}), so the folder "
                          f"this machine names in {MACHINE_VAR} is NOT opened; such a process reads a folder "
                          f"only when {ENV_VAR} names one")}
    if not named:
        return {"state": UNSET, "path": None, "source": None,
                "basis": (f"no folder is named, so no document can be read - which is the safe default. The folder "
                          f"is named on the machine that holds it, by {MACHINE_VAR} in that machine's own .env, and "
                          f"never in a committed file")}
    p = pathlib.Path(named)
    if not p.is_dir():
        return {"state": CONFIGURED_ABSENT, "path": named, "source": source,
                "basis": (f"the folder {source} names is not a folder on THIS machine, so nothing is read from it. "
                          f"That is not an empty folder: an empty folder exists and holds nothing, this one is not "
                          f"here at all. It is never created on the Owner's behalf")}
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
    #  W899 (FU-610) - nothing the call that read it sends leaves the platform: the folder is never sent to any
    #  external service. The mark is on this call's context, so it ends with the request that read the document
    from agentic_core.ai.data_class import mark_legal_matter_read
    mark_legal_matter_read(os.path.relpath(real, root))
    return {"opened": True, "refused": None, "document": os.path.relpath(real, root),
            "text": data.decode("utf-8", errors="replace"),
            "basis": "read-only, from inside the one named folder"}


def status() -> Dict[str, Any]:
    """The surface's view: the folder's state, whether indexing may start, and the count. Never contents, and never
    the folder's path (W1129, FU-1282): the page needs the state and which setting named it; the path is the
    machine's own."""
    ms = may_start()
    r = resolve_bundle_dir()
    return {"folder_state": r["state"], "folder_source": r["source"],
            "folder_basis": r["basis"], "bundle_indexing_may_start": ms["may_start"],
            "document_count": ms["count"], "bundle_indexing_basis": ms["basis"],
            "never": list(_matter().get("never") or [])}
