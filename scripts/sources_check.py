"""ONE REGISTER OF SOURCES FOR EVERY DOMAIN (Owner rulings 2026-10-12: Law item 8, Care item 3).

    python scripts/sources_check.py [--json] [--today YYYY-MM-DD]

A source this platform NAMES - a statute, a guideline, a standard, a public page - is a row of docs/SOURCES.json
with the publisher's page, the date it was read, who read it, its status, and what replaced it. Three checks:

  1. A NAME WITH NO ROW. Served code and pages are scanned for names of the kinds listed in `patterns`; every
     name found must be one of some row's `names`. A row may say honestly that it was `named_not_read`.
  2. A READER OF A REPLACED SOURCE. A row whose status is `replaced` or `withdrawn` may be named only where the
     row's `named_as_replaced_in` lists that file - that is, where the code SAYS it was replaced.
  3. A ROW SHOWN AS CURRENT PAST ITS REVIEW DATE is reported as not recently checked (it fails only with
     --strict-stale, because a date passing is not a defect in the tree; the pages say it themselves).

It states how many files, names and rows it examined, and REFUSES when it examined nothing. It reads no outside
page: a row's facts are entered by whoever read the page, in a round, with the date.
"""
import datetime as _dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs" / "SOURCES.json"
STATUSES = ("current", "replaced", "withdrawn", "named_not_read")


def load(path=None):
    d = json.loads((path or REGISTER).read_text(encoding="utf-8"))
    assert isinstance(d.get("rows"), list) and d["rows"], "the register holds no rows"
    return d


def row_problems(d):
    out = []
    seen = set()
    for r in d["rows"]:
        i = r.get("id") or "?"
        if i in seen:
            out.append(f"{i}: the id is used twice")
        seen.add(i)
        if r.get("status") not in STATUSES:
            out.append(f"{i}: status {r.get('status')!r} is not one of {', '.join(STATUSES)}")
        if not r.get("names") and not r.get("used_by"):
            out.append(f"{i}: neither a name nor a user is given, so nothing points at this row")
        for u in r.get("used_by") or []:
            if not (ROOT / u).exists():
                out.append(f"{i}: says it is used by {u}, which is not in the tree")
        if r.get("status") != "named_not_read":
            if not str(r.get("page") or "").startswith("https://"):
                out.append(f"{i}: no publisher's page")
            try:
                _dt.date.fromisoformat(str(r.get("read_on")))
            except ValueError:
                out.append(f"{i}: read_on is not a date")
            if not r.get("read_by"):
                out.append(f"{i}: does not say who read it")
        elif r.get("page") or r.get("read_on"):
            out.append(f"{i}: says it was not read and carries a page or a date - it is one or the other")
        #  W948 (FU-1066) - a row that names the hosts this platform would reach says what its terms permit
        if r.get("hosts") and not isinstance(r.get("permits"), list):
            out.append(f"{i}: names hosts and does not say what its terms permit")
        if r.get("status") in ("replaced", "withdrawn") and not r.get("replaced_by") and r.get("status") == "replaced":
            out.append(f"{i}: is replaced and does not say by what")
    return out


def scan(d, root=None):
    """Every name of a listed kind in the listed places: [(rel file, line number, name)]."""
    root = root or ROOT
    pats = [re.compile(p) for p in d.get("patterns") or []]
    found, files = [], 0
    for place in d.get("scan") or []:
        base = root / place["dir"]
        for ext in place["ext"]:
            for f in sorted(base.rglob("*" + ext)):
                if any(part in ("__pycache__", "node_modules", "dist") for part in f.parts):
                    continue
                files += 1
                rel = f.relative_to(root).as_posix()
                for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    for p in pats:
                        for m in p.finditer(line):
                            found.append((rel, n, " ".join(m.group(0).split())))
    return found, files


#  W948 (FU-1066) - A SOURCE NOT TO BE USED IS NEVER REACHED. A row whose `permits` is empty is not to be used; each of
#  its hosts is searched for in the whole backend and frontend source, and any hit fails the check.
REACH_PLACES = (("agentic_core", (".py",)), ("apps/workstation-superapp/src", (".ts", ".tsx")))


def reached_but_not_permitted(d, root=None):
    root = root or ROOT
    banned = [(r["id"], h) for r in d["rows"] if r.get("permits") == [] for h in (r.get("hosts") or [])]
    hits, files = [], 0
    for place, exts in REACH_PLACES:
        for f in sorted((root / place).rglob("*")):
            if f.suffix not in exts or any(p in ("__pycache__", "node_modules", "dist") for p in f.parts):
                continue
            files += 1
            text = f.read_text(encoding="utf-8", errors="replace")
            for rid, host in banned:
                if host in text:
                    hits.append((f.relative_to(root).as_posix(), host, rid))
    return hits, files, len(banned)


def row_standing(d, today=None):
    """W955 (P5.13 clause 1) - each row's standing now, by the one rule check() uses: a current row read more than
    review_days ago is not recently checked; a row of any other status has no 'recently checked' to say."""
    today = today or _dt.date.today()
    review = int(d.get("review_days") or 90)
    out = {}
    for r in d["rows"]:
        try:
            age = (today - _dt.date.fromisoformat(str(r.get("read_on")))).days
        except ValueError:
            age = None
        out[r.get("id")] = {"status": r.get("status"), "age_days": age,
                            "recently_checked": (None if r.get("status") != "current" or age is None
                                                 else age <= review)}
    return out


def check(d, root=None, today=None):
    today = today or _dt.date.today()
    found, files = scan(d, root)
    by_name = {}
    for r in d["rows"]:
        for nm in r.get("names") or []:
            by_name[" ".join(nm.split()).lower()] = r
    no_row, replaced_readers = [], []
    for rel, n, name in found:
        r = by_name.get(name.lower())
        if r is None:                                  # the pattern took a capitalised word before the name
            r = next((row for nm, row in by_name.items() if name.lower().endswith(" " + nm)), None)
        if r is None:
            no_row.append((rel, n, name))
        elif r.get("status") in ("replaced", "withdrawn") and rel not in (r.get("named_as_replaced_in") or []):
            replaced_readers.append((rel, n, name, r["id"]))
    review = int(d.get("review_days") or 90)
    #  W955 - the one staleness rule, shared with every reader of a row's standing (row_standing)
    stale = [(i, s["age_days"]) for i, s in row_standing(d, today).items() if s["recently_checked"] is False]
    _reached = reached_but_not_permitted(d, root)
    return {"files_examined": files, "names_found": len(found), "distinct_names": len({n.lower() for _, _, n in found}),
            "rows": len(d["rows"]), "row_problems": row_problems(d), "names_with_no_row": no_row,
            "readers_of_a_replaced_source": replaced_readers, "not_recently_checked": stale,
            "named_not_read": sorted(r["id"] for r in d["rows"] if r.get("status") == "named_not_read"),
            "not_to_be_used_but_reached": _reached[0], "files_searched_for_hosts": _reached[1],
            "hosts_not_to_be_reached": _reached[2],
            "review_days": review}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    today = _dt.date.fromisoformat(argv[argv.index("--today") + 1]) if "--today" in argv else None
    res = check(load(), today=today)
    if "--json" in argv:
        print(json.dumps(res, indent=1))
    else:
        print(f"examined {res['files_examined']} file(s), {res['names_found']} name(s) ({res['distinct_names']} distinct) "
              f"against {res['rows']} row(s)")
        for p in res["row_problems"]:
            print("  ROW PROBLEM", p)
        for rel, n, name in res["names_with_no_row"]:
            print(f"  NO ROW  {name!r}  {rel}:{n}")
        for rel, n, name, i in res["readers_of_a_replaced_source"]:
            print(f"  READS A REPLACED SOURCE  {name!r} ({i})  {rel}:{n}")
        for i, age in res["not_recently_checked"]:
            print(f"  not recently checked: {i}, read {age} days ago (a row is current for {res['review_days']})")
        for rel, host, i in res["not_to_be_used_but_reached"]:
            print(f"  REACHES A SOURCE NOT TO BE USED  {host!r} ({i})  {rel}")
        print(f"  {res['hosts_not_to_be_reached']} host(s) of sources not to be used, searched for in "
              f"{res['files_searched_for_hosts']} file(s)")
        if res["named_not_read"]:
            print(f"  named and not yet read at its publisher's page: {', '.join(res['named_not_read'])}")
    if not res["files_examined"] or not res["rows"]:
        print("EXAMINED NOTHING - this is not a pass.")
        return 2
    if not res["files_searched_for_hosts"]:
        print("SEARCHED NO FILE FOR THE HOSTS OF SOURCES NOT TO BE USED - this is not a pass.")
        return 2
    bad = res["row_problems"] or res["names_with_no_row"] or res["readers_of_a_replaced_source"] or res[
        "not_to_be_used_but_reached"] or (
        res["not_recently_checked"] and "--strict-stale" in argv)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
