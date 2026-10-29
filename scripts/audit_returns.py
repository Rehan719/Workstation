"""THE EFFECTIVENESS CHECK (plan item P5.10, clause 1) - did a finding come back?

    python scripts/audit_returns.py <this edition's record.json> [--earlier N] [--json] [--check]

For every STANDING tier-1 or tier-2 finding of one audit record, list the standing findings of earlier
editions that look like the same subject: they name the same code file, AND their titles share words. It reads
the records in docs/fidelity_runs/ and counts with the renderer's own rule (`standing`, `standing_tier`), so a
finding a refuter struck or lowered is not counted here either.

WHAT IT IS NOT. A CANDIDATE is not a return: the same file with similar words is a reason for a person to read
both findings, never a verdict. It cannot see a return that moved to another file, or one described in other
words. It says how many findings and editions it examined, and it REFUSES when it examined nothing.

`--check` exits 1 when a candidate at or above the stated overlap has no decision recorded beside it in
docs/fidelity_runs/returns_<edition>.json (a file a person writes: {"<finding id>": {"returned": true|false,
"of": "<edition>.<id>", "because": "..."}}) - so an audit round cannot close while a likely return is unread.
"""
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNS = ROOT / "docs" / "fidelity_runs"
FILE = re.compile(r"(agentic_core/[\w/]+\.py|apps/workstation-superapp/src/[\w/.-]+\.tsx?|\b[\w-]+\.tsx\b|\b\w+\.py\b)")
STOP = set("""a an the of to in on is are was were be been and or not no it its as at by for from with without that this
which while when where who what how than then into out over under any every each all both one two three says say said
shows show shown page route still also only never always after before does do did has have had can cannot could will
would should may might their there here them they you your our""".split())
OVERLAP = 0.34          # share of the shorter title's words found in the other; a screen, stated on every line


def _renderer():
    spec = importlib.util.spec_from_file_location("render_fidelity_ledger", ROOT / "scripts" / "render_fidelity_ledger.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def words(title):
    return {w for w in re.findall(r"[a-z][a-z'-]{2,}", title.lower()) if w not in STOP}


def standing(record, R):
    out = []
    for reg in record:
        vs = reg.get("verdicts") or []
        by_index = {v.get("index"): v for v in vs if isinstance(v, dict) and v.get("index") is not None}
        for i, f in enumerate(reg.get("findings") or []):
            v = by_index.get(i, vs[i] if i < len(vs) else None)
            #  FU-990 - THE RENDERER'S `standing` RETURNS (verdict, how). This compared the pair to a string, so neither a
            #  DELIVERED finding nor one a refuter struck was ever left out (none sat at tier 1-2 in v8-v17, so nothing
            #  showed). Counted with the renderer's own rule, as the docstring says.
            st, how = R.standing(f, v)
            tier = R.standing_tier(f, v)
            if st == "DELIVERED" or how == "refuted" or tier not in (1, 2):
                continue
            text = " ".join(str(f.get(k) or "") for k in ("section", "observed", "evidence", "smallest_honest_fix"))
            out.append({"id": f"{reg.get('region')}.{i}", "tier": tier, "title": str(f.get("section") or ""),
                        "files": sorted({pathlib.PurePosixPath(m).name for m in FILE.findall(text)}),
                        "words": words(str(f.get("section") or ""))})
    return out


def edition_of(path):
    m = re.search(r"ledger_v(\d+)_", pathlib.Path(path).name)
    return int(m.group(1)) if m else None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    flags = {a for a in argv if a.startswith("--")}
    args = [a for a in argv if not a.startswith("--")]
    n_earlier = int(argv[argv.index("--earlier") + 1]) if "--earlier" in argv else 3
    args = [a for a in args if a != str(n_earlier) or "--earlier" not in argv]
    if not args:
        print(__doc__)
        return 2
    rec_path = pathlib.Path(args[0])
    this = edition_of(rec_path)
    R = _renderer()
    now = standing(json.loads(rec_path.read_text(encoding="utf-8")), R)
    earlier = []
    for p in sorted(RUNS.glob("ledger_v*.json")):
        e = edition_of(p)
        if e is None or this is None or not (this - n_earlier <= e < this):
            continue
        try:
            for f in standing(json.loads(p.read_text(encoding="utf-8")), R):
                earlier.append({**f, "edition": e})
        except Exception as exc:                                          # an older record of another shape
            print(f"edition {e}: not read ({type(exc).__name__})")
    editions = sorted({f["edition"] for f in earlier})
    if not now or not earlier:
        print(f"EXAMINED NOTHING - {len(now)} standing finding(s) in this record and {len(earlier)} in earlier "
              f"editions {editions}. This is not a pass.")
        return 2
    cands = []
    for f in now:
        for g in earlier:
            shared_files = sorted(set(f["files"]) & set(g["files"]))
            small = min(len(f["words"]), len(g["words"])) or 1
            overlap = len(f["words"] & g["words"]) / small
            if shared_files and overlap >= OVERLAP:
                cands.append({"finding": f["id"], "tier": f["tier"], "title": f["title"], "earlier": f"v{g['edition']} {g['id']}",
                              "earlier_title": g["title"], "files": shared_files, "overlap": round(overlap, 2)})
    decided_path = RUNS / f"returns_v{this}.json"
    decided = json.loads(decided_path.read_text(encoding="utf-8")) if decided_path.exists() else {}
    undecided = sorted({c["finding"] for c in cands if c["finding"] not in decided})
    summary = {"edition": this, "standing_examined": len(now), "earlier_editions": editions, "earlier_standing_examined": len(earlier),
               "candidates": len(cands), "findings_with_a_candidate": len({c["finding"] for c in cands}),
               "decided": len([k for k in decided if k in {c["finding"] for c in cands}]), "undecided": undecided,
               "rule": f"same file named AND title-word overlap of at least {OVERLAP}",
               "basis": ("CANDIDATES for a person to read - the same file and similar words are not the same defect, and a "
                         "return described otherwise or moved to another file is not seen")}
    if "--json" in flags:
        print(json.dumps({"summary": summary, "candidates": cands, "decided": decided}, indent=1))
    else:
        print(f"examined {len(now)} standing tier-1/2 finding(s) of v{this} against {len(earlier)} of editions {editions}: "
              f"{summary['findings_with_a_candidate']} have a candidate; {len(undecided)} undecided")
        for c in sorted(cands, key=lambda c: (c["finding"], -c["overlap"])):
            mark = "" if c["finding"] not in decided else f"   [decided: {'RETURNED' if decided[c['finding']].get('returned') else 'not a return'}]"
            print(f"  {c['finding']} t{c['tier']} ~{c['overlap']} {c['title'][:86]}{mark}\n      {c['earlier']}: {c['earlier_title'][:92]}  ({', '.join(c['files'][:3])})")
        print("  " + summary["basis"])
    if "--check" in flags:
        return 1 if undecided else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
