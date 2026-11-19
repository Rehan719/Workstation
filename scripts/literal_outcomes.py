"""P5.10 clause 4 (W966) - THE LITERAL-OUTCOME SCREEN.

The Owner's ruling of 2026-10-12 (P5.10): "a commit-time check that lists every typed outcome word and figure in an
answer, each on an allow-list with its reason, or it fails"; ACCEPT: it "fails on a typed outcome added to a handler".
An outcome typed into a handler ("status": "signed", "score": 0.82) is said whatever happened. Some are true where they
are said: the handler returns "reversed" on the branch where it has just reversed. Some are not: a vote "recorded"
where nothing records it. This screen does not decide which. It lists every one in the answer of every route the
application mounts, and fails on any the allow-list does not carry with its reason.

    python scripts/literal_outcomes.py      # ok, or each typed outcome with no reason, each stale or short entry

WHAT IS READ: every route the application mounts (its HTTP routes; a websocket's frames and the documentation pages
are not answers of this kind), each handler unwrapped to the function written in this tree, and in that function every
dict literal whose key is one of OUTCOME_KEYS and whose value is a constant: a string, a number or a boolean. None is
not read, since it states nothing. A value built by an expression is computed, not typed, and is not read. A helper's
dict that a handler returns by name is read only where that helper is itself a route's handler.

THE ALLOW-LIST is docs/LITERAL_OUTCOMES.json: one entry for each (file, function, key, literal), with how many times it
is typed there and the reason it is true where it is said. An entry may instead carry `defect`, an open row of the
register: the literal is NOT true where it is said, and that row holds the fix. Once the row is closed, the entry
excuses nothing, so the fix must remove the literal or give it a reason.
"""
from __future__ import annotations

import ast
import inspect
import json
import pathlib
import sys
import textwrap
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOW = ROOT / "docs" / "LITERAL_OUTCOMES.json"
REGISTER = ROOT / "docs" / "FOLLOWUPS.json"
OUTCOME_KEYS = ("status", "state", "outcome", "verdict", "result", "decision", "passed", "approved", "success",
                "score", "confidence", "grade", "rating", "compliant", "valid", "ok", "healthy", "verified")
REASON_SHORTEST = 30


def census(app: Any, root: pathlib.Path = ROOT) -> Tuple[int, List[Dict[str, Any]], List[str]]:
    """(handlers examined, every typed outcome, the handlers whose source could not be read). Each typed outcome is
    {file, function, key, literal, line, routes}."""
    from fastapi.routing import APIRoute
    routes_of: Dict[Tuple[str, str], List[str]] = {}
    order: List[Tuple[Tuple[str, str], Any]] = []
    for r in getattr(app, "routes", []) or []:
        if not isinstance(r, APIRoute):
            continue
        fn = inspect.unwrap(r.endpoint)
        k = (getattr(fn, "__module__", "") or "", getattr(fn, "__qualname__", "") or "")
        if k not in routes_of:
            routes_of[k] = []
            order.append((k, fn))
        routes_of[k].append(f"{'/'.join(sorted(r.methods or ()))} {r.path}")
    found: List[Dict[str, Any]] = []
    unread: List[str] = []
    for k, fn in order:
        try:
            lines, first = inspect.getsourcelines(fn)
            file = pathlib.Path(inspect.getsourcefile(fn) or "").resolve().relative_to(root.resolve()).as_posix()
            tree = ast.parse(textwrap.dedent("".join(lines)))
        except (OSError, TypeError, ValueError, SyntaxError) as e:
            unread.append(f"{k[0]}.{k[1]} ({type(e).__name__})")
            continue
        for d in ast.walk(tree):
            if not isinstance(d, ast.Dict):
                continue
            for key, val in zip(d.keys, d.values):
                if (isinstance(key, ast.Constant) and key.value in OUTCOME_KEYS and isinstance(val, ast.Constant)
                        and val.value is not None):
                    found.append({"file": file, "function": fn.__name__, "key": key.value, "literal": val.value,
                                  "line": first + val.lineno - 1, "routes": routes_of[k]})
    return len(order), found, unread


def _place(file: str, function: str, key: str, literal: Any) -> Tuple[str, str, str, str]:
    return (file, function, key, json.dumps(literal))


def check(found: List[Dict[str, Any]], allow: Dict[str, Any], open_rows: set) -> List[str]:
    """Every reason the census and the allow-list disagree. Empty means none."""
    problems: List[str] = []
    counts = Counter(_place(f["file"], f["function"], f["key"], f["literal"]) for f in found)
    first_line = {}
    for f in found:
        first_line.setdefault(_place(f["file"], f["function"], f["key"], f["literal"]), f["line"])
    entries: Dict[Tuple[str, str, str, str], Dict[str, Any]] = {}
    for e in allow.get("entries") or []:
        p = _place(e.get("file"), e.get("function"), e.get("key"), e.get("literal"))
        if p in entries:
            problems.append(f"the allow-list carries {p[0]} {p[1]} {p[2]}={p[3]} twice")
        entries[p] = e
    for p, n in sorted(counts.items()):
        e = entries.get(p)
        where = f"{p[0]}:{first_line[p]} {p[1]} {p[2]}={p[3]}"
        if e is None:
            problems.append(f"a typed outcome no reason allows: {where}")
            continue
        if e.get("occurrences") != n:
            problems.append(f"{where} is typed {n} time(s), and the allow-list says {e.get('occurrences')}")
        if len(str(e.get("reason") or "").strip()) < REASON_SHORTEST:
            problems.append(f"{where} has no reason of at least {REASON_SHORTEST} characters")
        if e.get("defect") is not None and e.get("defect") not in open_rows:
            problems.append(f"{where} is excused as defect {e.get('defect')}, which is not an open row, so it "
                            "excuses nothing: remove the literal or give it a reason")
    for p in sorted(entries):
        if p not in counts:
            problems.append(f"the allow-list carries {p[0]} {p[1]} {p[2]}={p[3]}, which no mounted handler types")
    return problems


def _app() -> Any:
    sys.path.insert(0, str(ROOT))
    from agentic_core.app_mvp import app
    return app


def main(argv: Optional[List[str]] = None) -> int:
    examined, found, unread = census(_app())
    if examined == 0:
        print("REFUSING: examined nothing - the application mounted no route handler this screen could read, so no "
              "answer was screened. That is not a pass.")
        return 2
    try:
        allow = json.loads(ALLOW.read_text(encoding="utf-8"))
        rows = json.loads(REGISTER.read_text(encoding="utf-8"))["items"]
    except Exception as e:                                # noqa: BLE001 - said, never read as an empty allow-list
        print(f"REFUSING: the allow-list or the register could not be read ({type(e).__name__}: {e}), so no typed "
              "outcome can be said to have a reason. That is not a pass.")
        return 2
    open_rows = {r.get("id") for r in rows if r.get("status") == "open"}
    problems = check(found, allow, open_rows) + [f"a handler whose source could not be read: {u}" for u in unread]
    if problems:
        for p in problems:
            print(f"  {p}")
        print(f"FAIL - {len(problems)} problem(s) across {examined} mounted route handler(s)")
        return 1
    places = len({_place(f["file"], f["function"], f["key"], f["literal"]) for f in found})
    defects = sum(1 for e in allow.get("entries") or [] if e.get("defect"))
    print(f"ok - examined {examined} mounted route handler(s): {len(found)} typed outcome(s) in {places} place(s), "
          f"each on the allow-list with its reason; {defects} of those places are registered defects")
    return 0


if __name__ == "__main__":
    sys.exit(main())
