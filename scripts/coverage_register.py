"""THE COVERAGE REGISTER (the advice item clause 1, the Education item clause 7, the Care item clause 10).

    python scripts/coverage_register.py [--json] [--domain Law]

One instrument for every domain. A subject a person might bring is a ROW that says which nation it is for, what a
person can do here TODAY, and the state it is in:

    journey        a person can complete it here, and the row NAMES THE TEST that drives it end to end
    arithmetic     a computed answer from held data (a table, a dated rule) - also names its test
    frame          a form exists and returns an outline with nothing researched, checked or assessed
    route_only     the platform says where to go and builds nothing more (the row names the source row)
    nothing_built  nothing here serves it
    excluded       not built on purpose - the row names the ruling

The check FAILS on a row that claims a journey or arithmetic and names no test, or a test that is not in the suite;
on an excluded row with no ruling; on a state that is not one of the six. It counts by state, never as a
percentage "covered": a frame is not coverage, and the count of journeys is the only figure that may be called
what a person can do. It REFUSES when it examined nothing.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs" / "COVERAGE_REGISTER.json"
SUITE = ROOT / "integration_tests" / "test_mvp_spine.py"
STATES = ("journey", "arithmetic", "frame", "route_only", "nothing_built", "excluded")
PROVEN = ("journey", "arithmetic")


def load(path=None):
    d = json.loads((path or REGISTER).read_text(encoding="utf-8"))
    assert isinstance(d.get("rows"), list), "the register holds no rows list"
    return d


def tests_in_suite(suite=None):
    return set(re.findall(r"(?m)^def (test_\w+)\(", (suite or SUITE).read_text(encoding="utf-8")))


def check(d, suite_tests=None):
    tests = tests_in_suite() if suite_tests is None else suite_tests
    problems, seen = [], set()
    for r in d["rows"]:
        i = r.get("id") or "?"
        if i in seen:
            problems.append(f"{i}: the id is used twice")
        seen.add(i)
        st = r.get("state")
        if st not in STATES:
            problems.append(f"{i}: state {st!r} is not one of {', '.join(STATES)}")
            continue
        for k in ("domain", "subject", "nation", "today"):
            if not r.get(k):
                problems.append(f"{i}: does not say its {k}")
        if st in PROVEN:
            t = r.get("driven_by")
            if not t:
                problems.append(f"{i}: says a person can do this ({st}) and names no test that drives it")
            elif t not in tests:
                problems.append(f"{i}: names {t}, which is not a test in the suite")
        elif r.get("driven_by"):
            problems.append(f"{i}: is '{st}' and names a test - a row that is driven end to end is a journey or arithmetic")
        if st == "excluded" and not r.get("excluded_by"):
            problems.append(f"{i}: is excluded and names no ruling")
        if st == "route_only" and not r.get("route"):
            problems.append(f"{i}: is a route and names none")
    by = {}
    for r in d["rows"]:
        if r.get("state") in STATES:
            by.setdefault(r.get("domain") or "?", {s: 0 for s in STATES})[r["state"]] += 1
    return {"rows": len(d["rows"]), "tests_in_suite": len(tests), "by_domain": by, "problems": problems,
            "a_person_can_do": {dom: c["journey"] + c["arithmetic"] for dom, c in by.items()},
            "basis": ("a count of rows by state. Only 'journey' and 'arithmetic' rows are things a person can complete "
                      "here, each driven by the test it names; a frame is an outline and is not counted as coverage")}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    d = load()
    if "--domain" in argv:
        dom = argv[argv.index("--domain") + 1]
        d = {**d, "rows": [r for r in d["rows"] if r.get("domain") == dom]}
    res = check(d)
    if "--json" in argv:
        print(json.dumps(res, indent=1))
    else:
        print(f"examined {res['rows']} row(s) against {res['tests_in_suite']} test(s) in the suite")
        for dom, c in sorted(res["by_domain"].items()):
            print(f"  {dom}: " + " · ".join(f"{k} {v}" for k, v in c.items()) + f"   -> a person can do {res['a_person_can_do'][dom]} of {sum(c.values())}")
        for p in res["problems"]:
            print("  PROBLEM", p)
        print("  " + res["basis"])
    if not res["rows"] or not res["tests_in_suite"]:
        print("EXAMINED NOTHING - this is not a pass.")
        return 2
    return 1 if res["problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
