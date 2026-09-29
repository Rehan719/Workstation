"""Which files historically change WITH this one — `python scripts/coupling.py <path> [<path> ...]`.

WHAT THIS CATCHES, and it is a class this project keeps paying for. A truth fix is done only when every writer,
the reached page and an executing guard leg all say the new truth. Static imports do not reveal that: a React
page that renders a field has no import relationship with the Python module that computes it. Logical coupling
mined from commit history does.

It earned its place on the round it was written for. `agentic_core/vbs/quality.py` co-changes with
`apps/.../Deliverables.tsx` in 67% of its commits, which showed that the FU-160 fix had named the two server
modules and NOT the page that reads them. Checking that took two greps; discovering it after the fix would have
cost a 53-minute suite run.

HOW TO READ THE OUTPUT. `confidence` is P(B changed | A changed) over the sampled commits. It is a PROMPT, never
a verdict — a high number can mean "these two are always released together" rather than "one depends on the
other", and the tool cannot tell those apart. The action is to look at each named file and either update it or
record why it needs no change.

TWO DELIBERATE LIMITS:
  · commits touching more than MAX_FILES are skipped, because a repo-wide sweep couples everything to everything
    and would drown the signal.
  · below MIN_COMMITS occurrences, NO coupling is reported for that file. A file changed twice has no history to
    mine, and inventing a percentage from it would be the fabrication class this repository exists to remove.
"""
import collections
import re
import subprocess
import sys
from typing import Dict, List, Tuple

MAX_FILES = 40      # a commit touching more than this is a sweep, not a change
MIN_COMMITS = 4     # below this, refuse rather than assert
MIN_CONF = 0.34     # report a partner appearing in at least a third of the file's commits
MIN_PAIR = 3        # and at least this many times in absolute terms


def _commits(depth: int) -> List[set]:
    log = subprocess.run(["git", "log", "--format=%H", "--name-only", f"-{depth}"],
                         capture_output=True, text=True).stdout
    out: List[set] = []
    cur = None
    for line in log.splitlines():
        s = line.strip()
        if len(s) == 40 and re.fullmatch(r"[0-9a-f]{40}", s):
            cur = set()
            out.append(cur)
            continue
        if cur is not None and s:
            cur.add(s)
    return [c for c in out if 0 < len(c) <= MAX_FILES]


def coupling(targets: List[str], depth: int = 600) -> Dict[str, object]:
    commits = _commits(depth)
    freq: collections.Counter = collections.Counter()
    pair: collections.Counter = collections.Counter()
    for c in commits:
        freq.update(c)
        for a in c:
            for b in c:
                if a < b:
                    pair[(a, b)] += 1
    result: Dict[str, object] = {"commits_analysed": len(commits), "files": {}}
    for t in targets:
        t = t.replace("\\", "/")
        if freq[t] < MIN_COMMITS:
            result["files"][t] = {"assessable": False,
                                  "why": (f"changed in only {freq[t]} of the last {len(commits)} sampled "
                                          f"commits; no coupling is asserted from that")}
            continue
        partners: List[Tuple[float, int, str]] = []
        for (a, b), n in pair.items():
            if t in (a, b):
                other = b if a == t else a
                conf = n / freq[t]
                if conf >= MIN_CONF and n >= MIN_PAIR:
                    partners.append((round(conf, 3), n, other))
        partners.sort(reverse=True)
        result["files"][t] = {"assessable": True, "changed_in": freq[t],
                             "partners": [{"path": o, "confidence": c, "together": n} for c, n, o in partners]}
    return result


def main(argv: List[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    r = coupling(argv)
    print(f"# change coupling — {r['commits_analysed']} commits sampled "
          f"(commits touching >{MAX_FILES} files skipped as sweeps)\n")
    for path, info in r["files"].items():          # type: ignore[union-attr]
        print(f"## {path}")
        if not info["assessable"]:
            print(f"   REFUSED — {info['why']}\n")
            continue
        print(f"   changed in {info['changed_in']} commits")
        if not info["partners"]:
            print("   no partner above the reporting threshold\n")
            continue
        for p in info["partners"][:8]:
            print(f"   {p['confidence']:.0%}  ({p['together']}/{info['changed_in']})  {p['path']}")
        print("\n   These are PROMPTS, not verdicts. For each: update it, or record why it needs no change.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
