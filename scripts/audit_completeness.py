"""P5.22 (W973) - WHEN THE FINAL AUDIT IS COMPLETE (ACCEPT properties 3, 4, 5 and 7).

The final audit runs one assessor per slice of the census (docs/AUDIT_SLICES.json, held to the census by
scripts/audit_census_partition.py), in two configurations: the native floor and the local model. This check reads the
audit's run record and says whether the audit is complete, or gives each reason it is not:
  (3) no region is capped: every slice says it did not stop at a cap (hit_the_cap false), and left no finding unlisted;
  (4) a failed or empty region blocks completeness: every declared slice has exactly one result, the result says it
      completed (status "ok"), and it lists at least one surface it exercised. A result for a slice nobody declared
      is refused too;
  (5) the measured commit is reported: the record names the commit it measured, that commit is in this repository,
      every slice measured it, and it is the commit the ledger names;
  (7) both configurations ran, or the one that did not says why.

The run record:
    {"measured_commit": "<the full commit id>",
     "configurations": {"floor": {"ran": true, "slices": [<slice result>, ...]},
                        "local_model": {"ran": false, "why_not": "<why it did not run>"}}}
A slice result carries the fields the ledger renderer reads (region - the slice's id -, findings, verdicts,
hit_the_cap, unlisted_findings, surfaces_exercised), and two more: status ("ok", or anything else with an error) and
measured_commit.

    python scripts/audit_completeness.py <run.json> <commit the ledger names>
        COMPLETE (exit 0), INCOMPLETE with each reason (1), or REFUSING when there is nothing to judge (2)"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Callable, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLICES = ROOT / "docs" / "AUDIT_SLICES.json"
CONFIGURATIONS = ("floor", "local_model")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
#  the repository is the one the tree is in, whatever a caller's environment points git at
_GIT_ENV_DROPPED = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE")


def in_repository(commit: str, root: pathlib.Path = ROOT) -> bool:
    """Whether this repository holds the commit."""
    env = {k: v for k, v in os.environ.items() if k not in _GIT_ENV_DROPPED}
    out = subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=root, env=env, capture_output=True,
                         text=True)
    return out.returncode == 0


def declared_slices(doc: dict) -> List[str]:
    """The ids of the slices the census is partitioned into."""
    return [str(s["id"]) for s in (doc.get("slices") or [])]


def _exercised(result: dict) -> int:
    se = result.get("surfaces_exercised")
    if not isinstance(se, dict):
        return 0
    return len(se.get("routes") or []) + len(se.get("files") or [])


def _short(value) -> str:
    return str(value)[:12] if value else repr(value)


def reasons(run: dict, declared: List[str], ledger_commit: str,
            known: Callable[[str], bool] = in_repository) -> List[str]:
    """Every reason the audit is not complete. Empty means complete."""
    out: List[str] = []
    commit = run.get("measured_commit")
    #  (5) the measured commit is reported, is this repository's, and is the one the ledger names
    if not (isinstance(commit, str) and _COMMIT.match(commit)):
        out.append(f"the run does not report the commit it measured as a full commit id (it says {commit!r})")
        commit = None
    elif not known(commit):
        out.append(f"the run measured {commit[:12]}, which is not a commit in this repository")
    if commit and ledger_commit != commit:
        out.append(f"the ledger names {_short(ledger_commit)} and the run measured {commit[:12]}")
    #  (7) both configurations ran, or the one that did not says why
    configs = run.get("configurations") if isinstance(run.get("configurations"), dict) else {}
    for name in sorted(set(configs) - set(CONFIGURATIONS)):
        out.append(f"the run names a configuration that is neither the floor nor the local model: {name}")
    for name in CONFIGURATIONS:
        conf = configs.get(name)
        if not isinstance(conf, dict):
            out.append(f"the {name} configuration is not in the run, and nothing says why")
            continue
        if conf.get("ran") is not True:
            why = conf.get("why_not")
            if not (isinstance(why, str) and why.strip()):
                out.append(f"the {name} configuration did not run, and it does not say why")
            continue
        by_slice: Dict[str, List[dict]] = {}
        for r in conf.get("slices") or []:
            if isinstance(r, dict):
                by_slice.setdefault(str(r.get("region")), []).append(r)
        #  (4) every declared slice has exactly one result, which completed and examined something
        for sid in declared:
            got = by_slice.get(sid, [])
            if not got:
                out.append(f"{name}: slice {sid} has no result, and a slice the run did not return is a failed one")
                continue
            if len(got) > 1:
                out.append(f"{name}: slice {sid} has {len(got)} results, and which one counts is not said")
                continue
            r = got[0]
            if r.get("status") != "ok":
                out.append(f"{name}: slice {sid} did not complete (status {r.get('status')!r}: "
                           f"{str(r.get('error') or 'no error was given')[:200]})")
                continue
            if _exercised(r) == 0:
                out.append(f"{name}: slice {sid} examined nothing: it lists no route or page it exercised")
            #  (3) no region is capped
            cap = r.get("hit_the_cap")
            if cap is True:
                out.append(f"{name}: slice {sid} stopped at a cap")
            elif cap is not False:
                out.append(f"{name}: slice {sid} does not say whether it stopped at a cap")
            unlisted = r.get("unlisted_findings")
            if isinstance(unlisted, bool) or not isinstance(unlisted, int):
                out.append(f"{name}: slice {sid} does not say how many findings it left unlisted")
            elif unlisted:
                out.append(f"{name}: slice {sid} left {unlisted} finding(s) unlisted")
            #  (5) every slice measured the run's commit
            if commit and r.get("measured_commit") != commit:
                out.append(f"{name}: slice {sid} measured {_short(r.get('measured_commit'))}, not the run's "
                           f"{commit[:12]}")
        for sid in sorted(set(by_slice) - set(declared)):
            out.append(f"{name}: there is a result for {sid}, which is not a declared slice")
    return out


def main(argv: List[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print("usage: python scripts/audit_completeness.py <run.json> <commit the ledger names>")
        return 2
    try:
        run = json.loads(pathlib.Path(argv[0]).read_text(encoding="utf-8"))
        if not isinstance(run, dict):
            raise ValueError("the run record is not an object")
        declared = declared_slices(json.loads(SLICES.read_text(encoding="utf-8")))
    except Exception as e:                                   # noqa: BLE001 - said, never read as a verdict
        print(f"REFUSING: the run record or the declared slices could not be read ({type(e).__name__}: {e}). "
              "That is not a verdict.")
        return 2
    configs = run.get("configurations") if isinstance(run.get("configurations"), dict) else {}
    ran = sorted(n for n, c in configs.items() if isinstance(c, dict) and c.get("ran") is True and c.get("slices"))
    if not declared or not ran:
        print("REFUSING: examined nothing - " + ("no slice is declared" if not declared else
                                                 "no configuration ran a slice")
              + ", so there is no audit to call complete or incomplete. That is not a verdict.")
        return 2
    found = reasons(run, declared, argv[1].strip())
    if found:
        for r in found:
            print(f"  {r}")
        print(f"INCOMPLETE - {len(found)} reason(s). The final audit is not complete until each one is answered.")
        return 1
    skipped = [f"the {n} configuration did not run: {configs[n]['why_not'].strip()}"
               for n in CONFIGURATIONS if n not in ran]
    print(f"COMPLETE - {len(declared)} slice(s) in {' and '.join(ran)}, none capped, failed or empty, all measured at "
          f"{run['measured_commit'][:12]}" + ("; " + "; ".join(skipped) if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
