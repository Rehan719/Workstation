"""Recompute the figures the README states about this repo, and check or fix them.

W499. The README claimed "461 API endpoints (method+path; 440 distinct paths)" and "140+ routes
(64 verified operational end-to-end)". Measured: 471 / 449, and App.tsx defines 73 routes and is the
only file that defines any. Nothing in the tree recomputed either figure, so both drifted - and an
external audit of this repo built its whole baseline on them, inheriting the drift.

W500: the first fix asserted a figure that was ENVIRONMENT-DEPENDENT and CI failed with
('ops', 471, 469) - two routes mount only when the built frontend exists. The count is now
restricted to /api/, which is what the README's sentence claims, and is the same number with or
without dist/.

This plan says of every product surface that a figure nothing computed is not a measurement. The
README is the first surface anyone reads, so it is held to the same rule.

    python scripts/readme_figures.py            # print what is measured, and what the README says
    python scripts/readme_figures.py --check     # exit 1 if the README disagrees with the tree
    python scripts/readme_figures.py --fix       # rewrite the README's figures from the measurement

The figures are deliberately exact, not "140+": a range cannot be wrong, so it cannot be checked.
"""
from __future__ import annotations

import io
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
APP_TSX = os.path.join(ROOT, "apps", "workstation-superapp", "src", "App.tsx")
SRC = os.path.join(ROOT, "apps", "workstation-superapp", "src")

_HTTP = ("GET", "POST", "PUT", "PATCH", "DELETE")


def api_figures() -> tuple[int, int]:
    """(operations, distinct paths) as the booted app actually exposes them."""
    # the app writes to its data dir on import, so it is given a throwaway one: measuring must not
    # touch the live store (and CI sets no DATA_DIR).
    tmp = tempfile.mkdtemp(prefix="readme-figures-")
    for k in ("DATA_DIR", "WORKSTATION_DATA_DIR", "PROJECTS_DIR"):
        os.environ.setdefault(k, tmp)
    os.environ.setdefault("WORKSTATION_UEG_PATH", os.path.join(tmp, "ueg.json"))
    os.environ.setdefault("AI_DISABLE_LOCAL", "1")
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from agentic_core.app_mvp import app     # noqa: E402  (import after the env is set)
    ops, paths = set(), set()
    for r in app.routes:
        p = getattr(r, "path", None)
        # ONLY /api/, and this is not cosmetic. `GET /` and `GET /{full_path:path}` are mounted
        # only when the built frontend is present, so a TOTAL differs between a developer tree
        # (471) and CI (469), where the backend job runs before any dist/ exists - CI caught
        # exactly that. The README claims API operations, and the SPA catch-all, /docs, /redoc,
        # /health and /openapi.json are not any. Excluding them makes the figure mean what it
        # says, and makes it the same number in both environments.
        if not p or not p.startswith("/api/"):
            continue
        paths.add(p)
        for m in (getattr(r, "methods", None) or ()):
            if m in _HTTP:
                ops.add((m, p))
    return len(ops), len(paths)


def route_files() -> list[str]:
    """Every file under src/ that defines a router route, so "App.tsx is the only one" is measured."""
    out = []
    for base, _dirs, files in os.walk(SRC):
        if "node_modules" in base:
            continue
        for f in files:
            if not f.endswith((".tsx", ".ts")):
                continue
            p = os.path.join(base, f)
            if re.search(r"<Route\b", io.open(p, encoding="utf-8", errors="replace").read()):
                out.append(os.path.relpath(p, ROOT).replace("\\", "/"))
    return sorted(out)


def frontend_figures() -> tuple[int, int]:
    """(routes, distinct route paths) in App.tsx."""
    t = io.open(APP_TSX, encoding="utf-8").read()
    return len(re.findall(r"<Route\b", t)), len(set(re.findall(r'path="([^"]*)"', t)))


def measured() -> dict:
    ops, paths = api_figures()
    routes, route_paths = frontend_figures()
    return {"ops": ops, "paths": paths, "routes": routes, "route_paths": route_paths,
            "route_files": route_files()}


# the trailing clause after "distinct paths" is prose and may change; the pattern anchors on the
# two FIGURES and stops there, so a reworded sentence does not silently stop being checked
_API_RE = re.compile(r"(entrypoint; )(\d+)( API operations \(method\+path; )(\d+)( distinct paths)")
_FE_RE = re.compile(r"(src/App\.tsx\s+— )(\d+)( routes \(the only file in src/ that defines any)")


def stated() -> dict:
    t = io.open(README, encoding="utf-8").read()
    a, f = _API_RE.search(t), _FE_RE.search(t)
    return {"ops": int(a.group(2)) if a else None, "paths": int(a.group(4)) if a else None,
            "routes": int(f.group(2)) if f else None,
            "api_line_found": bool(a), "fe_line_found": bool(f)}


def main() -> int:
    m, s = measured(), stated()
    print(f"MEASURED  api: {m['ops']} operations over {m['paths']} distinct paths")
    print(f"          frontend: {m['routes']} routes ({m['route_paths']} distinct paths) in App.tsx")
    print(f"          files defining routes: {', '.join(m['route_files']) or 'none'}")
    print(f"STATED    api: {s['ops']} / {s['paths']}   frontend: {s['routes']}")
    if len(m["route_files"]) != 1 or not m["route_files"][0].endswith("src/App.tsx"):
        print("NOTE: App.tsx is no longer the only file defining routes - the README sentence that "
              "says it is must be rewritten by hand, not by --fix.")
    bad = [k for k in ("ops", "paths", "routes") if s[k] != m[k]]
    if "--fix" in sys.argv:
        t = io.open(README, encoding="utf-8", newline="").read()
        t2 = _API_RE.sub(lambda g: f"{g.group(1)}{m['ops']}{g.group(3)}{m['paths']}{g.group(5)}", t)
        t2 = _FE_RE.sub(lambda g: f"{g.group(1)}{m['routes']}{g.group(3)}", t2)
        if t2 != t:
            io.open(README, "w", encoding="utf-8", newline="").write(t2)
            print("README rewritten from the measurement.")
        else:
            print("README already matches (or the claim lines were not found - check the patterns).")
        return 0
    if not s["api_line_found"] or not s["fe_line_found"]:
        print("FAIL: the README's figure line(s) were not found - the patterns and the README have "
              "diverged, so nothing was checked.")
        return 1
    if bad:
        print("FAIL: the README disagrees with the tree on " + ", ".join(bad)
              + " - run `python scripts/readme_figures.py --fix`.")
        return 1
    print("ok: the README's figures match the tree.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
