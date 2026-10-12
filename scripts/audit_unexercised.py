r"""W664 - the surfaces the PREVIOUS audit run did not exercise, as the next run's direction.

Owner ruling 2026-10-10: a run counts toward the two consecutive zero runs only with no region at the cap, and the
run after it must be pointed at what the one before did not exercise. Until now nothing could point a run: the
ledger LISTED the unexercised routes and pages, and the workflow took no such list.

    python scripts/audit_unexercised.py <run record .json> <census .json>  >  unexercised.json

Prints {"from_record": ..., "from_census": ..., "routes": [...], "pages": [{"path", "component"}, ...],
"counts": {...}}. It reads two files and imports ONE function from the renderer - the same rule the ledger's
coverage table uses - so "not exercised" here cannot drift from "not exercised" there.
It changes nothing and boots nothing.
"""
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _renderer():
    spec = importlib.util.spec_from_file_location("render_fidelity_ledger", ROOT / "scripts" / "render_fidelity_ledger.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    record_path, census_path = pathlib.Path(argv[1]), pathlib.Path(argv[2])
    regions = json.loads(record_path.read_text(encoding="utf-8"))
    census = json.loads(census_path.read_text(encoding="utf-8"))
    if not isinstance(regions, list) or not regions:
        print("the run record is not a list of regions", file=sys.stderr)
        return 1
    cov = _renderer().coverage(regions, census)
    if not cov["routes_total"] and not cov["pages_total"]:
        #  FU-671 - an empty census gives an empty "not exercised" list, which reads as full coverage
        print("REFUSING: examined nothing - the census names no route and no page, so an empty list here would "
              "mean nothing was looked at, not that nothing is left. A count from a run that does not say what "
              "it looked at cannot be scored.", file=sys.stderr)
        return 1
    out = {
        "from_record": record_path.name,
        "from_census": census_path.name,
        "routes": cov["routes_not_exercised"],
        "pages": cov["pages_not_exercised"],
        "counts": {"routes_in_census": cov["routes_total"], "routes_not_exercised": len(cov["routes_not_exercised"]),
                   "pages_in_census": cov["pages_total"], "pages_not_exercised": len(cov["pages_not_exercised"])},
    }
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
