"""Reach audit — measure which backend routes the frontend can actually reach.

Run:  python scripts/reach_audit.py [--json out.json]

Enumerates every route on the live FastAPI app (imported in-process, so this measures
HEAD, not a possibly-stale server), extracts every /api reference in the frontend
source, and matches them. Template-built URLs are the known trap (exact-literal
matching produced 21 false "unreached" in one audit): a frontend fragment like
`/api/v1/heartbeat/${id}/beat` is matched by SEGMENTS, where a template hole matches
exactly one path parameter segment. A TRAILING template hole additionally marks the
whole prefix reachable-by-template (the code can compose deeper paths at runtime),
which is reported separately from exact reach so the honest number stays visible.

Output: reachable / unreached, split legacy (non-v1 namespace) vs owner-gated vs
genuine, clustered by first path segment after /api/v1/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_SRC = ROOT / "apps" / "workstation-superapp" / "src"

# Routes a frontend page must never call directly: gated or infrastructure.
OWNER_GATED_PREFIXES = (
    "/api/v1/economy/real-money",
    "/api/v1/payments/stripe",
)


def backend_routes():
    """Import the app and walk its route table. Requires isolated env vars set by caller."""
    from agentic_core.app_mvp import app  # noqa: PLC0415

    out = []
    for r in app.routes:
        path = getattr(r, "path", None)
        methods = getattr(r, "methods", None)
        if not path or not methods:
            continue
        for m in sorted(methods - {"HEAD", "OPTIONS"}):
            out.append((m, path))
    return sorted(set(out))


_API_FRAG = re.compile(r"/api/[A-Za-z0-9_\-./${}:]*")


def frontend_fragments():
    """Every /api… string fragment in the frontend source, template holes normalised to {}."""
    frags = set()
    for ext in ("*.ts", "*.tsx", "*.js", "*.jsx"):
        for f in FRONTEND_SRC.rglob(ext):
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in _API_FRAG.finditer(text):
                frag = m.group(0).rstrip(".")
                frag = re.sub(r"\$\{[^}]*\}", "{}", frag)
                frags.add(frag.rstrip("/") or frag)
    return sorted(frags)


def _segs(path: str):
    return [s for s in path.strip("/").split("/") if s]


def match(route_path: str, frag: str):
    """Does this frontend fragment reach this route path?

    Returns "exact" (segment-for-segment, holes matching {param} segments),
    "template-prefix" (fragment ends in a hole and its fixed segments prefix the
    route — reachable only if runtime data composes the tail), or None.
    """
    rsegs = _segs(route_path)
    fsegs = _segs(frag)
    trailing_hole = bool(fsegs) and fsegs[-1] == "{}"
    body = fsegs[:-1] if trailing_hole else fsegs

    def seg_ok(rs: str, fs: str) -> bool:
        if fs == "{}":
            return rs.startswith("{")
        # a fragment segment may itself contain an inline hole: "v{}" etc.
        if "{}" in fs:
            pat = "^" + ".+".join(re.escape(p) for p in fs.split("{}")) + "$"
            return re.match(pat, rs) is not None
        return rs == fs

    if len(body) > len(rsegs):
        return None
    if not all(seg_ok(rs, fs) for rs, fs in zip(rsegs, body)):
        return None
    if len(body) == len(rsegs):
        return "exact" if not trailing_hole else "exact"
    # fragment is shorter than the route: only a trailing hole may extend it,
    # and only into {param} or deeper segments — this is reach-by-template.
    if trailing_hole:
        return "template-prefix"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the full result as JSON here")
    args = ap.parse_args()

    routes = backend_routes()
    frags = frontend_fragments()
    print(f"backend: {len(routes)} method+path operations, "
          f"{len({p for _, p in routes})} distinct paths")
    api_routes = [(m, p) for m, p in routes if p.startswith("/api")]
    print(f"frontend: {len(frags)} distinct /api fragments")

    reach: dict[tuple[str, str], str] = {}
    for m, p in api_routes:
        best = None
        for frag in frags:
            r = match(p, frag)
            if r == "exact":
                best = "exact"
                break
            if r == "template-prefix":
                best = best or "template-prefix"
        if best:
            reach[(m, p)] = best

    unreached = [(m, p) for m, p in api_routes if (m, p) not in reach]
    exact = sum(1 for v in reach.values() if v == "exact")
    tmpl = sum(1 for v in reach.values() if v == "template-prefix")
    print(f"\nreach: {len(reach)}/{len(api_routes)} ops "
          f"({exact} exact, {tmpl} template-prefix) · unreached: {len(unreached)}")

    legacy = [(m, p) for m, p in unreached if not p.startswith("/api/v1/")]
    gated = [(m, p) for m, p in unreached
             if p.startswith("/api/v1/") and p.startswith(OWNER_GATED_PREFIXES)]
    genuine = [x for x in unreached if x not in legacy and x not in gated]
    print(f"unreached split: {len(legacy)} legacy(non-v1) · {len(gated)} owner-gated "
          f"· {len(genuine)} genuine")

    clusters: dict[str, list] = defaultdict(list)
    for m, p in genuine:
        segs = _segs(p)
        key = segs[2] if len(segs) > 2 else segs[-1]
        clusters[key].append(f"{m} {p}")
    print(f"\ngenuine unreached, clustered ({len(clusters)} clusters):")
    for key in sorted(clusters, key=lambda k: -len(clusters[k])):
        print(f"  {key:28s} {len(clusters[key]):3d}")

    if args.json:
        Path(args.json).write_text(json.dumps({
            "backend_ops": len(routes),
            "api_ops": len(api_routes),
            "frontend_fragments": len(frags),
            "reached": {f"{m} {p}": v for (m, p), v in sorted(reach.items())},
            "unreached_legacy": [f"{m} {p}" for m, p in legacy],
            "unreached_owner_gated": [f"{m} {p}" for m, p in gated],
            "unreached_genuine_clusters": {k: sorted(v) for k, v in clusters.items()},
        }, indent=2), encoding="utf-8")
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    os.environ.setdefault("AI_DISABLE_LOCAL", "1")
    main()
