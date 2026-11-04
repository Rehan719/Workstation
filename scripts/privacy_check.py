"""THE PRIVACY CHECK (W732) - refuses a commit, or a tree, that would put the Owner's private material or a
credential in this PUBLIC repository. Reports path, line and kind; never the matched text.

    python scripts/privacy_check.py            every tracked file
    python scripts/privacy_check.py --staged   only what the next commit would record (the pre-commit hook)

Exit 0: nothing found among the kinds that were checked (the output says which kinds were NOT checked).
Exit 1: a finding - do not commit or push; follow docs/PRIVACY_EXPOSURE_RUNBOOK.md.
Exit 2: the check could not run (no git) - nothing was scanned, which is never a pass.

The Owner's own names and markers are read from a list OUTSIDE the repository (WORKSTATION_PRIVATE_MARKERS,
default ~/.workstation/private_markers.txt), so the check never publishes what it protects. A false positive is
allowed by exact path and kind, with a reason, in config/privacy_allow.json.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agentic_core import privacy_exposure as pe  # noqa: E402


def main(argv) -> int:
    try:
        files = pe.staged(ROOT) if "--staged" in argv else None
        report = pe.scan(ROOT, files=files, markers=pe.load_markers(), allowed=pe.load_allowed(ROOT))
    except RuntimeError as exc:
        print(f"PRIVACY CHECK COULD NOT RUN: {exc}. Nothing was scanned, so this is not a pass.")
        return 2
    for f in report["findings"]:
        where = f"{f['path']}:{f['line']}" if f["line"] else f["path"]
        print(f"  {f['kind']:<18} {where}  ({f['what']})")
    scope = "staged file(s)" if "--staged" in argv else "tracked file(s)"
    print(f"privacy check: {report['count']} finding(s) over {report['files_read']} {scope}; "
          f"checked: {', '.join(report['checked'])}")
    if report["not_checked"]:
        print(f"NOT CHECKED: {', '.join(report['not_checked'])} - {report['not_checked_basis']}")
    if "--staged" not in argv:
        print(f"NOT SCANNED: {report['history_basis']}")
    if report["count"]:
        print(f"STOP: do not commit or push this. Follow {pe.RUNBOOK}.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
