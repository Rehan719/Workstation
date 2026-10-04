"""The gate a refutation round passes through, before and after — FU-259, P2.17 bar (b).

WHY THIS FILE EXISTS. W490's refutation raised 40 findings and verified 13. The other 27 agents died with
"No space left on device" while creating their git worktrees, and THE WORKFLOW STILL RETURNED A
NORMAL-LOOKING RESULT. Free space had fallen to about 9 MB because 56 worktrees had accumulated, one per
refuter agent across every round since W479, each a full checkout, and nothing removed them when a round
finished. Removing 55 of them recovered 9.6 GB.

So a round read 13 verified findings as a completed refutation of 40, and the difference was invisible.
That is the defect class this whole programme removes, in the instrument used to find it.

THE ROW NAMED TWO FIXES AND BOTH ARE HERE:
  (a) CHECK free space before launching, and REMOVE the round's worktrees after. `before()` refuses when
      the disk cannot hold the agents asked for, using the MEASURED cost of a checkout rather than a
      guess; `cleanup()` removes every secondary worktree and reports what it removed.
  (b) A REFUTATION WHOSE AGENTS DIED MUST NOT READ AS A COMPLETED REFUTATION. `after()` reconciles the
      launched count against the finished count, and the findings against the verdicts, and REFUSES
      rather than warning. A finding list is only as complete as the agents that produced it.

WHAT IT DOES NOT DO. It cannot make a dead agent's finding appear, and it does not judge whether a
surviving finding is RIGHT. It makes an incomplete refutation say so, which is the difference between 13
of 40 and "the refutation found 13".

Usage:
    python scripts/refutation_gate.py before --agents 45
    python scripts/refutation_gate.py after --result <the workflow result JSON>
    python scripts/refutation_gate.py cleanup
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

#  MEASURED IN W569, not estimated: a full copy of this working tree is 5,126 files and 160 MB. A git
#  worktree is a checkout of the same files, so it costs the same order. The figure is named here so a
#  later round can re-measure it rather than inherit a number with no source.
BYTES_PER_WORKTREE = 160 * 1024 * 1024
BYTES_PER_WORKTREE_BASIS = ("measured W569: `git ls-files` is 5,126 files totalling 160 MB, and a "
                            "worktree is a checkout of the same set")
#  Headroom beyond the worktrees themselves: each agent runs pytest, which writes a store, and the
#  suite's own temp dirs are not free. Deliberately generous, because the failure it prevents cost a
#  whole refutation round.
HEADROOM_BYTES = 3 * 1024 * 1024 * 1024


def _worktrees() -> List[str]:
    """Every worktree path git knows about, main first. Empty if git cannot be read."""
    try:
        out = subprocess.run(["git", "worktree", "list", "--porcelain"],
                             capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=60).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [l.split(" ", 1)[1].strip() for l in out.splitlines() if l.startswith("worktree ")]


def before(agents: int, root: str = ".") -> Dict[str, Any]:
    """May a refutation of `agents` agents be launched here? REFUSES, never warns.

    THREE-STATE: True to go, False to refuse, None when the disk could not be read — and None is not a
    pass. An instrument that cannot measure must say so, because the whole point of this gate is that a
    round stopped being able to tell a complete refutation from a starved one.
    """
    try:
        usage = shutil.disk_usage(str(Path(root).resolve().anchor or root))
    except OSError as e:
        return {"may_launch": None, "free_bytes": None,
                "basis": (f"the disk could not be read ({e.__class__.__name__}), so whether {agents} "
                          f"agent(s) can run is NOT KNOWN. This is not a pass")}
    wts = _worktrees()
    need = agents * BYTES_PER_WORKTREE + HEADROOM_BYTES
    ok = usage.free >= need
    return {
        "may_launch": ok,
        "agents": agents,
        "free_bytes": usage.free,
        "needed_bytes": need,
        "worktrees_now": len(wts),
        "stale_worktrees": max(0, len(wts) - 1),
        "basis": (
            f"{usage.free / 1e9:.1f} GB free; {agents} agent(s) need "
            f"{agents * BYTES_PER_WORKTREE / 1e9:.1f} GB of worktrees plus "
            f"{HEADROOM_BYTES / 1e9:.0f} GB headroom = {need / 1e9:.1f} GB. "
            f"{len(wts)} worktree(s) exist, {max(0, len(wts) - 1)} of them secondary"
            + ("" if ok else
               ". REFUSED — W490 lost 27 of 45 agents to a full disk and the run still returned a "
               "normal-looking result, so a starved refutation is indistinguishable from a complete "
               "one unless it is refused up front. Run `cleanup` first")),
        "cost_basis": BYTES_PER_WORKTREE_BASIS,
    }


AGENT_DONE = "done"


def _agent_records(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The per-agent entries a workflow result keeps, or [] if it keeps none.

    MEASURED, not assumed: `workflowProgress` holds one `workflow_agent` entry per agent, each with its
    own `state` and a `label` naming the lens it ran. That is stronger than the aggregate counts the
    row expected, because a lens whose agents all died can be NAMED rather than showing up as a
    slightly smaller total — which is exactly how W490's 13-of-40 looked plausible.
    """
    wp = result.get("workflowProgress")
    if not isinstance(wp, list):
        return []
    return [x for x in wp if isinstance(x, dict) and x.get("type") == "workflow_agent"]


def after(result: Any, findings_by_lens: Dict[str, int] | None = None) -> Dict[str, Any]:
    """Did every agent that was launched come back? REFUSES to call a starved refutation complete.

    Reads the RESULT FILE's own per-agent records first, and falls back to the notification's aggregate
    counts. Three-state: True complete, False incomplete, None when the artefact says too little to
    decide — and None is NOT a pass, which is the whole lesson of W490.
    """
    if not isinstance(result, dict):
        return {"complete": None,
                "basis": (f"no result mapping was given ({type(result).__name__}), so whether the "
                          f"refutation finished is NOT KNOWN. This is not a pass")}

    recs = _agent_records(result)
    launched = result.get("agentCount")
    if launched is None:
        launched = (result.get("usage") or {}).get("agent_count")

    if recs:
        #  ONLY "done" COUNTS AS FINISHED. The failure states cannot be enumerated from a successful
        #  run, and guessing them would mean inventing the thing this gate exists to detect.
        by_state: Dict[str, int] = {}
        for r in recs:
            by_state[str(r.get("state"))] = by_state.get(str(r.get("state")), 0) + 1
        done = by_state.get(AGENT_DONE, 0)
        not_done = {k: v for k, v in by_state.items() if k != AGENT_DONE}
        problems = []
        if not_done:
            problems.append("agent state(s) other than done: "
                            + ", ".join(f"{k} x{v}" for k, v in sorted(not_done.items())))
        if launched is not None and len(recs) != launched:
            problems.append(f"{len(recs)} agent record(s) for {launched} launched — a record that was "
                            f"never written is an agent nobody can account for")
        #  PER LENS, from the label, so a lens that lost every agent is NAMED rather than absorbed.
        lenses: Dict[str, Dict[str, int]] = {}
        for r in recs:
            #  THE LENS IS THE SECOND SEGMENT, measured from real labels rather than guessed. A refute
            #  agent is labelled `refute:<lens>` and a verify agent `verify:<lens>:<finding title>`, so
            #  taking the LAST segment reported 35 "lenses" for a run that had five — each with one
            #  agent, which made "every agent died in this lens" fire on any single death and name a
            #  finding instead of a lens. Driven on the real result file before and after.
            _parts = [p for p in str(r.get("label") or "?").split(":") if p]
            lens = _parts[1] if len(_parts) > 1 else (_parts[0] if _parts else "?")
            d = lenses.setdefault(lens, {"total": 0, "done": 0})
            d["total"] += 1
            d["done"] += 1 if r.get("state") == AGENT_DONE else 0
        dead_lenses = sorted(k for k, v in lenses.items() if v["done"] == 0)
        if dead_lenses:
            problems.append(f"every agent died in lens(es): {', '.join(dead_lenses)}")
        #  AND THE FINDINGS AGAINST THE VERDICTS, when the caller can supply them. A slice() cap once
        #  dropped findings silently in this very instrument, so a count is reconciled rather than read.
        if findings_by_lens:
            for lens, n in sorted(findings_by_lens.items()):
                if lens not in lenses:
                    problems.append(f"findings are attributed to lens {lens!r}, which ran no agent")
        return {
            "complete": not problems,
            "launched": launched, "records": len(recs), "done": done,
            "by_state": by_state, "by_lens": lenses, "problems": problems,
            "basis": (
                f"{done} of {len(recs)} agent record(s) report state {AGENT_DONE!r}"
                + (f", against {launched} launched" if launched is not None else "")
                + f", across {len(lenses)} lens(es), so the finding list covers every agent launched"
                if not problems else
                "INCOMPLETE — " + "; ".join(problems) + ". The findings that exist may be sound; the "
                "LIST is not a refutation of the whole subject, and reading it as one is what W490 did"),
        }

    #  NO PER-AGENT RECORDS: fall back to the notification's aggregate counts.
    u = result.get("usage") or result
    done = u.get("agents_done")
    errored = u.get("agents_error")
    skipped = u.get("agents_skipped")
    empty = u.get("agents_empty_result")
    missing = [k for k, v in (("agent_count/agentCount", launched), ("agents_done", done),
                              ("agents_error", errored)) if v is None]
    if missing:
        return {"complete": None, "missing_fields": missing,
                "basis": (f"the result holds no per-agent records and names no {', '.join(missing)}, so "
                          f"completeness cannot be decided. W490's run returned a normal-looking finding "
                          f"list while 27 of 45 agents were dead; without either source that is exactly "
                          f"as invisible as it was then")}
    problems = []
    if errored:
        problems.append(f"{errored} agent(s) ERRORED")
    if skipped:
        problems.append(f"{skipped} agent(s) were SKIPPED")
    if empty:
        problems.append(f"{empty} agent(s) returned EMPTY")
    if done != launched:
        problems.append(f"{done} of {launched} agent(s) finished")
    return {
        "complete": not problems,
        "launched": launched, "done": done, "errored": errored,
        "skipped": skipped, "empty": empty, "problems": problems,
        "basis": (
            f"all {launched} agent(s) finished, none errored, skipped or returned empty, so the finding "
            f"list covers every agent that was launched"
            if not problems else
            "INCOMPLETE — " + "; ".join(problems) + ". The findings that exist may be sound; the LIST "
            "is not a refutation of the whole subject, and reading it as one is what W490 did"),
    }


def cleanup(keep_main: bool = True) -> Dict[str, Any]:
    """Remove every SECONDARY worktree and say which. The main worktree is never touched.

    The accumulation is the cause, not the symptom: 56 of these had built up because nothing removed
    them when a round finished. This is the "after" half of the row's fix (a).
    """
    wts = _worktrees()
    if not wts:
        return {"removed": [], "failed": [],
                "basis": "git reported no worktrees, so nothing was removed and nothing is claimed"}
    main, rest = wts[0], wts[1:]
    removed, failed = [], []
    for w in rest:
        try:
            r = subprocess.run(["git", "worktree", "remove", "--force", w],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=300)
            (removed if r.returncode == 0 else failed).append(w)
        except (OSError, subprocess.SubprocessError):
            failed.append(w)
    try:
        subprocess.run(["git", "worktree", "prune"], capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        pass
    return {
        "removed": removed, "failed": failed, "main_kept": main if keep_main else None,
        "basis": (f"{len(removed)} secondary worktree(s) removed, {len(failed)} could not be; the main "
                  f"worktree {main} is never touched. Each one is about "
                  f"{BYTES_PER_WORKTREE / 1e6:.0f} MB, so this recovered roughly "
                  f"{len(removed) * BYTES_PER_WORKTREE / 1e9:.1f} GB"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("before", help="may a refutation of N agents be launched here?")
    b.add_argument("--agents", type=int, required=True)
    a = sub.add_parser("after", help="did every launched agent come back?")
    a.add_argument("--result", required=True, help="a JSON file holding the workflow result")
    sub.add_parser("cleanup", help="remove every secondary worktree")
    args = ap.parse_args()

    if args.cmd == "before":
        rep = before(args.agents)
        print(("GO" if rep["may_launch"] else "REFUSED" if rep["may_launch"] is False else "NOT KNOWN")
              + " — " + rep["basis"])
        #  NOT KNOWN exits non-zero as well: a gate that cannot measure must not read as a pass.
        return 0 if rep["may_launch"] else 1
    if args.cmd == "after":
        try:
            res = json.loads(Path(args.result).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"NOT KNOWN — the result file could not be read ({e.__class__.__name__}), so "
                  f"completeness is not decided. This is not a pass")
            return 1
        rep = after(res)
        print(("COMPLETE" if rep["complete"] else
               "INCOMPLETE" if rep["complete"] is False else "NOT KNOWN") + " — " + rep["basis"])
        return 0 if rep["complete"] else 1
    rep = cleanup()
    print(rep["basis"])
    return 0 if not rep["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
