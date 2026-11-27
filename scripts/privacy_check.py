"""THE PRIVACY CHECK (W732) - refuses a commit, or a tree, that would put the Owner's private material or a
credential in this PUBLIC repository. Reports path, line and kind; never the matched text.

    python scripts/privacy_check.py            every tracked file
    python scripts/privacy_check.py --staged   only what the next commit would record (the pre-commit hook)
    python scripts/privacy_check.py --history  every blob in the repository's history, for credentials only

Exit 0: nothing found among the kinds that were checked (the output says which kinds were NOT checked).
Exit 1: a finding - do not commit or push; follow docs/PRIVACY_EXPOSURE_RUNBOOK.md.
Exit 2: the check could not run (no git) - nothing was scanned, which is never a pass.

--history (W1208, FU-1864) only reads: it changes no commit, ref or file, and never rewrites history. Each
finding is said by kind, commit, path and line. Exit 1 on a finding; 0 on none over a whole walk; 2 when it
could not run or examined nothing, and when the walk is partial (a shallow clone, a grafts file, a
single-branch fetch): partial is never a pass. A partial clone is refused, since reading it would fetch. It
covers the refs the clone holds, so the Owner's run is on a mirror clone. A known non-credential in history is
allowed by commit, path, kind and line, with a reason, in config/privacy_history_allow.json.

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


def _shown(path: str) -> str:
    """A path as it is safe to print: a control character, or a byte that is not UTF-8, is written as an escape."""
    return "".join(c if 32 <= ord(c) != 127 and not 0xDC80 <= ord(c) <= 0xDCFF
                   else f"\\x{ord(c) & 0xFF:02x}" for c in path)


def history(argv) -> int:
    """W1208 (FU-1864) - the read-only history mode: every blob reachable from every local ref, read once and whole
    for credentials. Each finding is said by kind, commit, path and line, never by the matched text."""
    if "--staged" in argv:
        print("PRIVACY CHECK COULD NOT RUN: --history and --staged are two modes; give one. Nothing was scanned, so "
              "this is not a pass.")
        return 2
    try:
        report = pe.scan_history(ROOT, allowed=pe.load_history_allowed(ROOT))
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"PRIVACY CHECK COULD NOT RUN: {exc}. Nothing was scanned, so this is not a pass.")
        return 2
    if not report.get("commits_walked") or not report.get("blobs_read"):
        print("PRIVACY CHECK REFUSING: examined nothing - the history walk found no commit or no file to read, so "
              "this is not a pass.")
        return 2
    for f in report["findings"]:
        at = "  (the walk stopped at this commit: introduced there or before it)" if f["at_boundary"] else ""
        more = [p for p in f["paths"] if p != f["path"]]
        also = f"  (also at {len(more)} other path(s): {', '.join(_shown(p) for p in more[:5])})" if more else ""
        print(f"  {f['kind']:<18} {(f['commit'] or 'no commit found')[:12]} {_shown(f['path'])}:{f['line']}  "
              f"({f['what']}){at}{also}")
    print(f"privacy check (history): {report['count']} finding(s) over {report['blobs_read']} blob(s) in "
          f"{report['commits_walked']} commit(s); checked: {', '.join(report['checked'])}; "
          f"{report['allowed_count']} allowed by commit, path, kind and line")
    print(f"HISTORY: {report['history_basis']}")
    print(f"READ-ONLY: {report['read_only']}")
    if report["count"]:
        print(f"STOP: a credential is in this repository's history. Follow {pe.RUNBOOK}: revoking it at its provider "
              "is the Owner's, and history is not rewritten.")
        return 1
    if not report["history_scanned"]:
        print("PARTIAL: the walk did not reach the whole history this clone could hold; this is not a pass. Run "
              "--history on a full clone.")
        return 2
    return 0


def main(argv) -> int:
    if "--history" in argv:
        return history(argv)
    try:
        files = pe.staged(ROOT) if "--staged" in argv else None
        report = pe.scan(ROOT, files=files, markers=pe.load_markers(), allowed=pe.load_allowed(ROOT))
    except (RuntimeError, OSError, ValueError) as exc:     # W1208: git missing is could not run, never exit 1
        print(f"PRIVACY CHECK COULD NOT RUN: {exc}. Nothing was scanned, so this is not a pass.")
        return 2
    #  W808 (FU-1154) - a scan that read no file has found nothing because it looked at nothing. For the hook
    #  (--staged) that is a commit that adds or changes no file - a deletion, say - which can carry no new text, so
    #  it is allowed and says nothing was scanned; refusing it would block a harmless commit. A whole-tree scan that
    #  read no file is refused: git listed no tracked file, and "0 findings" would be a reading of nothing.
    if not report.get("files_read"):
        if "--staged" in argv:
            print("privacy check: this commit adds or changes no file (nothing staged carries content), so it can "
                  "carry no new text; nothing was scanned.")
            return 0
        print("PRIVACY CHECK REFUSING: examined nothing - git listed no tracked file, so this is not a pass.")
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
