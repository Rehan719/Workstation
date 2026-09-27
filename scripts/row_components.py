"""The follow-up register's rows, grouped into FILE-CONNECTED COMPONENTS — the natural bundle a round
can hold in its head at once.

W500 measured it; W501 moved the algorithm into `agentic_core.plan_followups` so the planner, the API
and this script all read ONE implementation. This file is an adapter and a report.

`followups.py batches` groups rows by SWEEP CLASS: one mechanism swept across its consumers. That is
the right unit for a mechanism and the wrong one for a round's cost. The expensive part of a round is
reading a subsystem well enough to measure it — so rows that touch the SAME files share the
measurement, the guard, the blinds and the refutation.

What this is NOT:
  · it does not say a component CLOSES an item. The closest measured was 23 of one item's 26 rows.
    A component ADVANCES items, and this script only ever says advances.
  · a single-row component may be genuinely isolated OR simply under-connected, because the graph is
    built from each row's DECLARED `files` list. Singletons are reported as possibly under-connected.

    python scripts/row_components.py            # the components, largest first
    python scripts/row_components.py --json      # the same, as data
"""
from __future__ import annotations

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
REGISTER = os.path.join(ROOT, "docs", "FOLLOWUPS.json")

from agentic_core import plan_followups as fu     # noqa: E402  (after sys.path)


def open_rows(register: dict | None = None) -> list:
    reg = register if register is not None else json.loads(
        io.open(REGISTER, encoding="utf-8").read())
    rows = reg.get("items") if isinstance(reg, dict) else reg
    return [r for r in (rows or []) if isinstance(r, dict) and r.get("status") == "open"]


def components(rows: list) -> list:
    """Adapter: the one implementation lives in plan_followups._components_of."""
    return fu._components_of([{"id": r.get("id"), "slot": r.get("slot"),
                               "files": (r.get("files") or [])} for r in rows])


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
    for c in [x for x in comps if x["size"] > 1]:
        print(f"  {c['size']:3d} row(s) \u00b7 {len(c['files']):3d} file(s) \u00b7 advances "
              f"{', '.join(c['items_advanced'])}")
    singles = [c for c in comps if c["size"] == 1]
    if singles:
        print(f"  {len(singles)} single-row component(s) \u2014 the residue tail, and each POSSIBLY "
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
