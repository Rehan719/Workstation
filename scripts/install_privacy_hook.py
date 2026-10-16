"""Install the privacy check as this clone's pre-commit hook (W732). Every commit made in this clone, or in any
worktree of it, is then refused when it would record a credential or the Owner's private material.

    python scripts/install_privacy_hook.py

It writes <git common dir>/hooks/pre-commit. An existing hook that is not this one is kept beside it as
pre-commit.before-privacy and still runs first. Bypassing the hook (`git commit --no-verify`) is the Owner's
call alone; the suite and CI run the same check over the whole tree regardless.
"""
from __future__ import annotations

import pathlib
import stat
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = "# workstation privacy check (W732)"
HOOK = f"""#!/bin/sh
{MARK}
HOOKS="$(dirname "$0")"
if [ -x "$HOOKS/pre-commit.before-privacy" ]; then "$HOOKS/pre-commit.before-privacy" "$@" || exit $?; fi
TOP="$(git rev-parse --show-toplevel)"
PY="$TOP/venv/Scripts/python.exe"; [ -x "$PY" ] || PY="$TOP/venv/bin/python"; [ -x "$PY" ] || PY=python
"$PY" "$TOP/scripts/privacy_check.py" --staged
"""


def install(root: pathlib.Path = ROOT) -> int:
    r = subprocess.run(["git", "-C", str(root), "rev-parse", "--git-common-dir"], capture_output=True, text=True)
    if r.returncode != 0:
        print("not a git clone - nothing installed")
        return 2
    common = pathlib.Path(r.stdout.strip())
    if not common.is_absolute():
        common = (root / common).resolve()
    hooks = common / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-commit"
    if hook.exists() and MARK not in hook.read_text(encoding="utf-8", errors="replace"):
        keep = hooks / "pre-commit.before-privacy"
        if keep.exists():
            print(f"an earlier hook is already kept at {keep}; nothing changed")
            return 2
        hook.rename(keep)
    hook.write_bytes(HOOK.encode("utf-8"))
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"installed: {hook}")
    return 0


if __name__ == "__main__":
    sys.exit(install())
