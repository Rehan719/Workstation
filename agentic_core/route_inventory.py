"""The one census of the routes this process serves (W613, FU-504, M1 v8 R6.0).

Three surfaces asked "is this router mounted?" by reading `app.routes` and taking each entry's `path`. On the
pinned FastAPI that is a flat list of routes. On FastAPI 0.142 an included router is ONE `_IncludedRouter`
entry with an empty path, so the census read 11 distinct paths out of 521, every prefix check came back
false, and the vision-realisation, heartbeat-coverage and cognition-wiring surfaces reported the heartbeat,
economy, GaaS gate, Board and Sovereign Evolution Office as NOT MOUNTED - 12% coverage, 0 of 13 tiers - on
a process that was serving all of them. Nothing failed loudly, because an empty set is a valid answer to
"which of these prefixes are present".

So the census reads the OpenAPI schema's paths - the public, version-stable list FastAPI itself serves at
/openapi.json - together with every flat route's path, and it says which it read. A census that reads
nothing is returned as None, never as an empty set, so a caller cannot report "not mounted" from a reading
that failed.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Set, Tuple


def mounted_paths() -> Tuple[Optional[Set[str]], Dict[str, Any]]:
    """(paths or None, census). None means the census could not be read - NOT that nothing is mounted."""
    census: Dict[str, Any] = {"flat_paths": 0, "schema_paths": 0, "paths": 0, "error": None}
    try:
        from agentic_core.app_mvp import app
    except Exception as exc:  # the app could not be imported, so nothing can be said about its routes
        census.update(error=f"the app could not be imported: {type(exc).__name__}: {exc}",
                      basis="NOT ASSESSABLE - the route census could not be read")
        return None, census
    flat = {p for p in (getattr(r, "path", "") for r in getattr(app, "routes", []) or []) if p}
    schema: Set[str] = set()
    try:
        schema = set(((app.openapi() or {}).get("paths") or {}).keys())
    except Exception as exc:
        census["error"] = f"the OpenAPI schema could not be built: {type(exc).__name__}: {exc}"
    paths = flat | schema
    census.update(flat_paths=len(flat), schema_paths=len(schema), paths=len(paths))
    if not paths:
        census["basis"] = ("NOT ASSESSABLE - the route census read zero paths, which means the reading failed, "
                           "not that nothing is mounted")
        return None, census
    census["basis"] = (f"{len(paths)} distinct paths: the OpenAPI schema's {len(schema)} plus the "
                       f"{len(flat)} flat routes' paths (a route hidden from the schema is counted if flat)")
    return paths, census
