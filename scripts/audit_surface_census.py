r"""W638 (FU-602) — the surface census: the DENOMINATOR of the fidelity audit's coverage.

Importing the app builds stores, so this is never run beside a suite and never against the live data directory.

The denominator of the audit's coverage: every API route the app itself registers and every page the superapp
routes to, computed from the tree rather than typed. Writes JSON to stdout:
    {"head": "<sha>", "routes": ["GET /api/v1/…", …], "pages": [{"path": "/x", "component": "X"}, …],
     "excluded": [{"surface": "...", "reason": "..."}]}

RULES (each is a way this instrument could report coverage it does not have):
  - routes come from `app.routes` on the app the audit boots (agentic_core.app_mvp:app), method + path TEMPLATE;
    HEAD/OPTIONS and the docs/openapi routes are EXCLUDED and LISTED with the reason, never silently dropped;
  - pages come from the <Route path=… element=…> table in App.tsx; a route whose element cannot be parsed is
    reported under "unparsed", and a non-zero unparsed count must be printed by the renderer;
  - the fresh-store environment is REQUIRED (the same variables scripts/boot_audit_backend.py sets); the script
    refuses to run if DATA_DIR is unset or points inside the repo;
  - make it fail first: a guard feeds it an App.tsx with one route removed and asserts the census shrinks by
    exactly one; and asserts len(routes) equals len of the app's own route table minus the listed exclusions.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXCLUDE_PATHS = {"/openapi.json": "framework schema route", "/docs": "framework docs page",
                 "/docs/oauth2-redirect": "framework docs helper", "/redoc": "framework docs page"}
EXCLUDE_METHODS = {"HEAD": "implicit on every GET", "OPTIONS": "CORS preflight"}


def api_routes():
    data_dir = os.environ.get("DATA_DIR", "")
    if not data_dir or pathlib.Path(data_dir).resolve().is_relative_to(ROOT):
        raise SystemExit("REFUSING: set the fresh-store environment first (DATA_DIR outside the repo) — "
                         "importing the app creates stores")
    sys.path.insert(0, str(ROOT))
    from agentic_core.app_mvp import app
    return routes_of(app)


def routes_of(app):
    """(routes, excluded) for an app object — separate from the import above so a guard can hand it the app
    the test client already holds, and compare the census with the app's own route table."""
    routes, excluded = set(), []
    for r in app.routes:
        path = getattr(r, "path", None)
        methods = getattr(r, "methods", None) or set()
        if not path:
            continue
        if path in EXCLUDE_PATHS:
            excluded.append({"surface": path, "reason": EXCLUDE_PATHS[path]})
            continue
        if not methods:                      # a mount or websocket: listed, with what it is
            excluded.append({"surface": path, "reason": f"not an HTTP method route ({type(r).__name__})"})
            continue
        for m in sorted(methods):
            if m in EXCLUDE_METHODS:
                continue
            routes.add(f"{m} {path}")
    return sorted(routes), excluded


#  A first draft used ONE regex with an optional element group behind a lazy prefix: it matched all 76 routes
#  and captured the component of NONE (the lazy prefix matched empty and the optional group was skipped) —
#  found by running it against the real App.tsx. Each tag is now cut out whole and read in two steps.
_TAG_RE = re.compile(r"<Route\b")
_PATH_RE = re.compile(r"\bpath=(?:\"([^\"]+)\"|'([^']+)')")
_ELEM_RE = re.compile(r"\belement=\{\s*<\s*([A-Za-z0-9_.]+)")


def parse_pages(src: str):
    """(pages, redirects, unparsed, declared). A <Navigate> element is a REDIRECT, not a page: it renders
    nothing of its own, so counting it as a surface would inflate the denominator with unreachable entries."""
    starts = [m.start() for m in _TAG_RE.finditer(src)]
    out, redirects, unparsed = [], [], []
    for i, s in enumerate(starts):
        tag = src[s: starts[i + 1] if i + 1 < len(starts) else len(src)]
        p, e = _PATH_RE.search(tag), _ELEM_RE.search(tag)
        path = (p.group(1) or p.group(2)) if p else None
        comp = e.group(1) if e else None
        if not path or not comp:
            unparsed.append({"path": path, "component": comp})
        elif comp == "Navigate":
            redirects.append({"path": path})
        else:
            out.append({"path": path, "component": comp})
    return out, redirects, unparsed, len(starts)


def pages():
    return parse_pages((ROOT / "apps/workstation-superapp/src/App.tsx").read_text(encoding="utf-8"))


def main() -> int:
    head = subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=str(ROOT), capture_output=True,
                          text=True).stdout.strip()
    routes, excluded = api_routes()
    pgs, redirects, unparsed, declared = pages()
    #  the census must account for every <Route> it saw, or it under-reports its own denominator
    assert len(pgs) + len(redirects) + len(unparsed) == declared, (len(pgs), len(redirects), len(unparsed), declared)
    json.dump({"head": head, "routes": routes, "pages": pgs, "redirects": redirects, "unparsed_pages": unparsed,
               "route_tags_declared": declared, "excluded": excluded}, sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
