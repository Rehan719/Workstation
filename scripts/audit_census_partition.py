"""P5.22 (W970) - THE CENSUS, PARTITIONED INTO SLICES.

The final audit is uncapped and census-partitioned (the Owner's ruling of 2026-10-12; P5.22, chartered W754 on the
Owner's ruling of 2026-11-06). Each slice is assessed and refuted on its own, so the slices together must be the
census: no surface left out, and none counted twice unless that is said. This is the first instrument the final audit
needs. Its ACCEPT properties held here are (1) every census surface is in exactly one slice, or the overlap is stated,
(2) the union of the slices equals the census, and the empty half of (4): an empty slice blocks completeness.

    python scripts/audit_surface_census.py > census.json       # in the fresh-store environment (see that script)
    python scripts/audit_census_partition.py census.json       # the slices, or every way they fail the census

The slices are declared in docs/AUDIT_SLICES.json. Each names the router modules whose routes it holds (the module a
route's handler is written in, which the census now records) and the page folders whose pages it holds (the folder of
the file App.tsx imports the page from). A page App.tsx writes inline, with no file of its own, belongs to the slice
that names "inline". A stated overlap names the module or folder two slices share and why.

Each failure is refused with its own sentence:
  - a surface in no slice;
  - a surface in two slices with no stated overlap;
  - a slice that holds no surface;
  - a slice that names a module or folder the census does not hold.
A census with no surface is refused, and so is one that does not say which module serves each route."""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any, Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLICES = ROOT / "docs" / "AUDIT_SLICES.json"
INLINE = "inline"


def keys_of(census: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """(each route with the module that serves it, each page path with its folder or "inline")."""
    modules = census.get("route_modules") or {}
    routes = {r: modules.get(r) for r in census.get("routes") or []}
    files = census.get("page_files") or {}
    pages = {}
    for p in census.get("pages") or []:
        f = files.get(p.get("component"))
        pages[p.get("path")] = f.rsplit("/", 1)[0] if f else INLINE
    return routes, pages


def partition(census: Dict[str, Any], declared: Dict[str, Any]) -> Dict[str, Any]:
    """The slices, each with its routes and pages, and every way the declaration fails the census."""
    routes, pages = keys_of(census)
    problems: List[str] = []
    slices = declared.get("slices") or []
    overlap = {(o.get("key"), tuple(sorted(o.get("slices") or []))) for o in declared.get("overlap") or []}
    held: Dict[str, Dict[str, List[str]]] = {s["id"]: {"routes": [], "pages": []} for s in slices}
    route_mods, page_folders = set(routes.values()), set(pages.values())
    for s in slices:
        for m in s.get("modules") or []:
            if m not in route_mods:
                problems.append(f"slice {s['id']} names {m}, which the census does not hold")
        for f in s.get("pages") or []:
            if f not in page_folders:
                problems.append(f"slice {s['id']} names {f}, which the census does not hold")

    def place(surface: str, key: str, kind: str) -> None:
        named = lambda s: (s.get("modules") if kind == "routes" else s.get("pages")) or []   # noqa: E731
        inside = [s["id"] for s in slices if key in named(s)]
        if not inside:
            problems.append(f"a surface is in no slice: {surface} ({key})")
            return
        if len(inside) > 1 and (key, tuple(sorted(inside))) not in overlap:
            problems.append(f"{surface} is in {len(inside)} slices ({', '.join(inside)}) and no overlap is stated")
        for sid in inside:
            held[sid][kind].append(surface)

    for r, mod in sorted(routes.items()):
        place(r, mod, "routes")
    for p, folder in sorted(pages.items()):
        place(p, folder, "pages")
    for sid, h in held.items():
        if not h["routes"] and not h["pages"]:
            problems.append(f"slice {sid} holds no surface")
    return {"slices": held, "routes": len(routes), "pages": len(pages), "problems": problems}


def main(argv: List[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: audit_census_partition.py CENSUS.json")
        return 2
    try:
        census = json.loads(pathlib.Path(argv[0]).read_text(encoding="utf-8"))
        declared = json.loads(SLICES.read_text(encoding="utf-8"))
    except Exception as e:                                  # noqa: BLE001 - said, never read as an empty census
        print(f"REFUSING: the census or the slices could not be read ({type(e).__name__}: {e}). That is not a pass.")
        return 2
    if not census.get("routes") and not census.get("pages"):
        print("REFUSING: examined nothing - the census holds no route and no page, so there is nothing to slice. "
              "That is not a pass.")
        return 2
    if census.get("routes") and not census.get("route_modules"):
        print("REFUSING: the census does not say which module serves each route (it was made before W970), so its "
              "routes cannot be sliced. Make it again with scripts/audit_surface_census.py.")
        return 2
    out = partition(census, declared)
    for sid, h in out["slices"].items():
        print(f"  {sid}: {len(h['routes'])} route(s), {len(h['pages'])} page(s)")
    if out["problems"]:
        for p in out["problems"]:
            print(f"  {p}")
        print(f"FAIL - {len(out['problems'])} problem(s): the slices are not the census")
        return 1
    print(f"ok - {out['routes']} route(s) and {out['pages']} page(s) of census {census.get('head', '?')} in "
          f"{len(out['slices'])} slice(s), each surface in exactly one or in a stated overlap, and no slice empty")
    return 0


if __name__ == "__main__":
    sys.exit(main())
