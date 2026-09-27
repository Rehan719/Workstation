"""The follow-up register's rows, grouped into FILE-CONNECTED COMPONENTS — the natural bundle a round
can hold in its head at once.

W500. `followups.py batches` groups rows by SWEEP CLASS: one mechanism swept across its consumers.
That is the right unit for a mechanism and the wrong one for a round's cost. The expensive part of a
round is not editing files, it is reading a subsystem well enough to measure it — so rows that touch
the SAME files share the measurement, the guard, the blinds and the refutation. Treating
"row cites file" as an edge and taking connected components finds those groups.

Measured when this was written: 42 components over 106 open rows, ONE of them 32 rows over 34 files
spanning five plan items — 30% of the backlog in a single connected piece — while `batches` was
proposing two rows across nine files. The four largest components were 48% of all open rows.

What this is NOT:
  · it does not say a component CLOSES an item. The closest measured was 23 of one item's 26 rows.
    A component ADVANCES items, and this script only ever says advances.
  · a single-row component may be genuinely isolated OR simply under-connected, because the graph is
    built from each row's DECLARED `files` list. Singletons are reported as possibly under-connected.

    python scripts/row_components.py            # the components, largest first
    python scripts/row_components.py --json      # the same, as data
"""
from __future__ import annotations

import collections
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTER = os.path.join(ROOT, "docs", "FOLLOWUPS.json")


def open_rows(register: dict | None = None) -> list:
    reg = register if register is not None else json.loads(
        io.open(REGISTER, encoding="utf-8").read())
    rows = reg.get("items") if isinstance(reg, dict) else reg
    return [r for r in (rows or []) if isinstance(r, dict) and r.get("status") == "open"]


def components(rows: list) -> list:
    """Each component: the rows whose files transitively connect them. Largest first.

    A row with NO files is its own component — it cannot be connected to anything, which is a fact
    about the row's record, not about the work.
    """
    adj: dict = collections.defaultdict(set)
    for r in rows:
        node = ("row", r["id"])
        adj[node]                                     # a fileless row still gets a node
        for f in (r.get("files") or []):
            adj[node].add(("file", f))
            adj[("file", f)].add(node)
    seen, out = set(), []
    for n in list(adj):
        if n in seen:
            continue
        stack, comp = [n], set()
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.add(x)
            stack.extend(adj[x] - seen)
        ids = sorted(i for kind, i in comp if kind == "row")
        files = sorted(f for kind, f in comp if kind == "file")
        out.append({"rows": ids, "files": files})
    by_id = {r["id"]: r for r in rows}
    for c in out:
        c["items_advanced"] = sorted({by_id[i]["slot"] for i in c["rows"]})
        c["size"] = len(c["rows"])
        c["possibly_under_connected"] = c["size"] == 1
    out.sort(key=lambda c: (-c["size"], c["items_advanced"]))
    return out


def main() -> int:
    rows = open_rows()
    comps = components(rows)
    # the components must PARTITION the rows: every open row in exactly one, none invented
    seen = [i for c in comps for i in c["rows"]]
    assert sorted(seen) == sorted(r["id"] for r in rows), "the components do not partition the rows"
    if "--json" in sys.argv:
        print(json.dumps(comps, indent=2))
        return 0
    print(f"{len(comps)} component(s) over {len(rows)} open row(s)")
    top = [c for c in comps if c["size"] > 1]
    for c in top:
        print(f"  {c['size']:3d} row(s) · {len(c['files']):3d} file(s) · advances "
              f"{', '.join(c['items_advanced'])}")
    singles = [c for c in comps if c["size"] == 1]
    if singles:
        print(f"  {len(singles)} single-row component(s) — the residue tail, and each POSSIBLY "
              f"under-connected rather than isolated (the graph is built from declared files)")
    if comps:
        big = comps[0]
        pct = round(100 * big["size"] / max(1, len(rows)))
        print(f"\nLARGEST: {big['size']} row(s) = {pct}% of the open backlog, over "
              f"{len(big['files'])} file(s), advancing {len(big['items_advanced'])} item(s). "
              f"It ADVANCES them; it does not close them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
