"""Check that every instrument the delivery method NAMES actually resolves.

M-LEARN-05: an `enforced_by` path is a CLAIM, and a claim about a tool is checkable. A lesson whose enforcer
names a guard that was renamed reads as enforced and catches nothing — the same shape as three external
assessments of this repository that named instruments which did not exist.

Checks three kinds of name:
  PATH   a file path with a known extension — must exist, unless it is under data/ (a runtime store exists
         only once something has written to it, and its absence is not a broken claim)
  GUARD  a test function, written as `::test_name` or as a bare `test_wNNN_...` — must be defined in the suite
  FUNC   a `name()` reference — must be defined somewhere under agentic_core/ or scripts/

Exit 1 and name every unresolved instrument. Exit 0 says every NAMED instrument resolves; it does NOT say the
guard would actually catch a breach of its rule, which is the harder half and is a reading of the guard.
"""
import io
import json
import os
import re
import sys

# json BEFORE js, or the alternation truncates docs/FOLLOWUPS.json to docs/FOLLOWUPS.js and reports a file
# that was never named. The first version of this script did exactly that, ten times.
EXT = r"\.(?:jsonl|json|mjs|js|py|tsx|ts|md)"
SUITE = "integration_tests/test_mvp_spine.py"


_ROUTES: set = set()


def _routes() -> set:
    """Every route path the app declares, normalised of {param} names. Empty when the app cannot be built."""
    global _ROUTES
    if _ROUTES:
        return _ROUTES
    try:
        from agentic_core.app_mvp import app
        _ROUTES = {re.sub(r"\{[^}]*\}", "{}", getattr(r, "path", "")) for r in app.routes}
    except Exception as e:                       # noqa: BLE001 - said, never a silent pass
        print(f"  (the app could not be built, so no endpoint is verified: {e.__class__.__name__}: {e})")
        _ROUTES = {"__unavailable__"}
    return _ROUTES


def _defines(name: str) -> bool:
    for base in ("agentic_core", "scripts"):
        for root, _, files in os.walk(base):
            for f in files:
                if not f.endswith(".py"):
                    continue
                try:
                    if f"def {name}" in io.open(os.path.join(root, f), encoding="utf-8",
                                                errors="replace").read():
                        return True
                except OSError:
                    continue
    return False


def main() -> int:
    try:
        d = json.load(io.open("docs/DELIVERY_METHOD.json", encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"docs/DELIVERY_METHOD.json could not be read ({e.__class__.__name__}: {e}); nothing is "
              f"reported as resolving in its absence.")
        return 1
    suite = io.open(SUITE, encoding="utf-8").read() if os.path.exists(SUITE) else ""
    bad, checked = [], 0
    for row in d.get("lessons", []) + d.get("mechanisms", []):
        src = (row.get("enforced_by") or "") + " " + " ".join(row.get("entry_points") or [])
        if not src.strip():
            continue
        for tok in re.findall(r"[A-Za-z0-9_./\-]+" + EXT, src):
            checked += 1
            if not os.path.exists(tok) and not tok.startswith("data/"):
                bad.append((row["id"], "PATH", tok))
        for tok in re.findall(r"::(test_[A-Za-z0-9_]+)", src) + re.findall(r"\b(test_w\d+_[A-Za-z0-9_]+)", src):
            checked += 1
            if f"def {tok}" not in suite:
                bad.append((row["id"], "GUARD", tok))
        for tok in re.findall(r"\b([a-z_][a-z0-9_]{3,})\(\)", src):
            checked += 1
            if not _defines(tok):
                bad.append((row["id"], "FUNC", tok))
        # ENDPOINT - added after a blind proved this script GREEN where the suite's guard went RED: it checked
        # only file-extension tokens, so a mechanism naming an endpoint that is not a route passed. M-LEARN-05
        # names this script as its enforcer, so its own claim was stronger than its tool.
        for ep in (row.get("entry_points") or []):
            ep = str(ep).strip()
            verb, _, rest = ep.partition(" ")
            if verb not in ("GET", "POST", "PUT", "PATCH", "DELETE") or not rest.startswith("/"):
                continue
            checked += 1
            want = re.sub(r"\{[^}]*\}", "{}", rest.split("?")[0])
            known = _routes()
            if "__unavailable__" in known:
                continue                          # the app could not be built; said above, not reported clean
            if want not in known:
                bad.append((row["id"], "ROUTE", ep))

    lessons, mechs = len(d.get("lessons", [])), len(d.get("mechanisms", []))
    print(f"{checked} named instrument(s) checked across {lessons} lesson(s) and {mechs} mechanism(s)")
    if bad:
        print("UNRESOLVED — each of these reads as enforced and may catch nothing:")
        for rid, kind, tok in bad:
            print(f"  {rid:14} {kind:6} {tok}")
        return 1
    print("every named path, guard and function resolves.")
    print("This does NOT say a guard would catch a breach of its rule - that is a reading of the guard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
