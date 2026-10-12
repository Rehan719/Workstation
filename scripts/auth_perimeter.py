"""THE AUTHENTICATION PERIMETER, MEASURED (the readiness round; OWNER RULINGS 2026-10-11 and 2026-10-12: brought
forward; it turns nothing on).

    python scripts/auth_perimeter.py [--json] [--list] [--strict]

Reads the MOUNTED application: for every route, whether its dependency tree asks who is calling (the platform's
`get_current_user`, or a stricter dependency built on it) - read from the route's own resolved dependants, never
from a signature search. Each route is then one of:
  asks       its dependencies include the caller dependency
  public     it does not, and it is on the DECLARED list of routes that are public on purpose, with a reason
  UNDECIDED  it does not, and nobody has declared it public - this is the finding
A declared-public route that DOES ask is reported too (the list is stale). The check fails on any UNDECIDED route
once the declared list exists; until then it reports and exits 0 with the count, saying the list is absent.

WHAT THIS CANNOT SEE, said every run: that a handler USES the caller it asks for (a route may ask and ignore the
answer); what a route does with authentication ON (that is driven separately, in a test process); routes mounted
by something other than this application object. It reads state; it changes nothing and switches nothing.
"""
import collections
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DECLARED = ROOT / "docs" / "PUBLIC_ROUTES.json"
os.environ.setdefault("AI_DISABLE_LOCAL", "1")
os.environ.setdefault("WORKSTATION_DRIVE", "1")
sys.path.insert(0, str(ROOT))


def _caller_names():
    from agentic_core.auth import core as _core
    names = {"get_current_user"}
    for n in dir(_core):
        if n.startswith(("require_", "get_current_", "current_")) and callable(getattr(_core, n)):
            names.add(n)
    return names


def _asks(dependant, names, seen=None) -> bool:
    seen = seen if seen is not None else set()
    if id(dependant) in seen:
        return False
    seen.add(id(dependant))
    call = getattr(dependant, "call", None)
    if getattr(call, "__name__", "") in names:
        return True
    return any(_asks(d, names, seen) for d in (getattr(dependant, "dependencies", None) or []))


def measure(app=None, declared_path=None):
    """`app` and `declared_path` are arguments so a guard can drive each state on a small application of its
    own instead of reading whatever the ambient tree happens to hold."""
    if app is None:
        from agentic_core.app_mvp import app
    declared_path = pathlib.Path(declared_path) if declared_path else DECLARED
    names = _caller_names()
    declared = {}
    if declared_path.exists():
        declared = {(r["method"], r["path"]): r for r in json.loads(declared_path.read_text(encoding="utf-8")).get("routes", [])
                    if r.get("decision") in ("public", "must_ask", "retire") and str(r.get("why") or "").strip()}
    rows = []
    for route in app.routes:
        dep = getattr(route, "dependant", None)
        path = getattr(route, "path", None)
        if dep is None or not path:
            continue
        asks = _asks(dep, names)
        for method in sorted((getattr(route, "methods", None) or set()) - {"HEAD", "OPTIONS"}):
            d = declared.get((method, path))
            #  a declaration with no reason, or with a decision that is not one of the three, decides nothing
            state = "asks" if asks else ({"public": "public", "must_ask": "OWED", "retire": "OWED"}[d["decision"]] if d else "UNDECIDED")
            rows.append({"method": method, "path": path, "state": state,
                         "writes": method in ("POST", "PUT", "PATCH", "DELETE"),
                         "module": getattr(getattr(route, "endpoint", None), "__module__", ""),
                         "stale_declaration": bool(asks and d and d["decision"] == "public"),
                         "decision": (d or {}).get("decision"), "why": (d or {}).get("why")})
    return rows, sorted(names), declared_path.exists()


def verdict(rows, has_list, strict=False):
    """0 while the declared list is absent (it reports); once it exists, 1 on any undecided route or stale
    declaration. OWED routes (declared `must_ask` or `retire`, and not yet done) are counted and do not fail the
    everyday check; `strict` - the check to pass BEFORE authentication is turned on - fails on them too."""
    if not has_list:
        return 0
    bad = {"UNDECIDED", "OWED"} if strict else {"UNDECIDED"}
    return 1 if any(r["state"] in bad or r["stale_declaration"] for r in rows) else 0


def main():
    rows, names, has_list = measure()
    c = collections.Counter(r["state"] for r in rows)
    und = [r for r in rows if r["state"] == "UNDECIDED"]
    by_mod = collections.Counter(r["module"].rsplit(".", 1)[-1] for r in und)
    out = {"routes": len(rows), "by_state": dict(c), "undecided_that_write": sum(1 for r in und if r["writes"]),
           "undecided_by_module": by_mod.most_common(40), "caller_dependencies_looked_for": names,
           "declared_list_present": has_list, "stale_declarations": [f"{r['method']} {r['path']}" for r in rows if r["stale_declaration"]],
           "cannot_see": ("that a handler uses the caller it asks for; behaviour with authentication on; routes "
                          "mounted outside this application object")}
    if "--json" in sys.argv:
        print(json.dumps({**out, "rows": rows}, indent=1))
        return 0
    print(f"examined {len(rows)} mounted route-methods; caller dependencies looked for: {', '.join(names)}")
    print(f"  asks who is calling: {c['asks']} | declared public: {c['public']} | OWED (declared, not yet built): {c['OWED']} | UNDECIDED: {c['UNDECIDED']} "
          f"(of which {out['undecided_that_write']} WRITE)")
    print("  undecided, by module:", ", ".join(f"{m} {n}" for m, n in by_mod.most_common(18)))
    if "--list" in sys.argv:
        for r in sorted(und, key=lambda r: (not r["writes"], r["path"])):
            print(f"   {'WRITES ' if r['writes'] else 'reads  '}{r['method']:6} {r['path']}")
    print("  cannot see:", out["cannot_see"])
    if not has_list:
        print("  the declared list docs/PUBLIC_ROUTES.json is ABSENT, so nothing is failed yet: every undecided route is a finding to classify")
        return 0
    return verdict(rows, has_list, strict="--strict" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
