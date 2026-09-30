"""Generate a night plan from live state. The repeatable entry point: `python scripts/plan_night.py 8`.

WHY THIS EXISTS. W514 produced a good overnight plan by hand, over several passes, while a suite ran. That is
not reusable — the next night would re-derive the same arithmetic and risk reaching a different answer from the
same facts. This composes the two measured mechanisms (`session_forecast`, `night_sim`) with the live register
and emits the plan, so the *generation* is repeatable and not only the plan.

WHAT IT REFUSES TO DO. It does not choose the work. It orders candidates by evidence and states the batching
rule; which rows go in which round is a judgement that depends on what each row turns out to be when measured,
and a generator that pretended otherwise would be asserting a plan rather than computing one. It also never
prints a date or a completion promise — the plan forecaster's standing discipline.

CAPACITY IS AN INPUT, NOT A MEASUREMENT. Remaining allowance is only readable through the app
(`get_usage`), not from a script, so `hours` is passed in. If it is wrong the whole plan is wrong, which is why
the output says so at the top rather than burying the assumption.
"""
import importlib.util
import json
import pathlib
import sys
from typing import Any, Dict, List

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def open_rows_by_slot() -> Dict[str, List[str]]:
    reg = json.loads((ROOT / "docs/FOLLOWUPS.json").read_text(encoding="utf-8"))
    out: Dict[str, List[str]] = {}
    for r in reg.get("items", []):
        if r.get("status") != "open":
            continue
        out.setdefault(str(r.get("slot") or "(unslotted)"), []).append(r["id"])
    return dict(sorted(out.items(), key=lambda kv: (-len(kv[1]), kv[0])))


def main(hours: float) -> None:
    sf, ns = _load("session_forecast"), _load("night_sim")

    print(f"# Night plan — {hours:.1f}h assumed available\n")
    print("**Capacity is an INPUT here, not a measurement.** Read it in the app (`get_usage`) before trusting "
          "this plan; if the hours are wrong, everything below is wrong.\n")

    cap = sf.forecast_session(hours)
    dur = cap.get("round_durations", {})
    if not dur.get("assessable"):
        print("## Refused\n\n" + dur.get("why", "insufficient history") +
              "\n\nNo round count is projected. Work one round, land it, and run this again.")
        return

    print("## 1 · Measured round cost\n")
    print(f"- round duration: n={dur['n']}, median **{dur['median_h']}h**, p75 {dur['p75_h']}h, max {dur['max_h']}h")
    print(f"- excluded as containing idle (an interval is not a duration): **{dur['excluded_as_containing_idle']}**")
    print(f"- full suite: **{cap['suite_h']}h** — {round(100 * cap['suite_h'] / dur['median_h'])}% of a median round\n")

    print("## 2 · Simulated completion probability\n")
    print("Empirical bootstrap, 20,000 trials, fixed seed. `p_red` (a round needing a second full suite) is an "
          "ASSUMPTION, so a range is shown rather than one indefensible value.\n")
    sample = ns.observed(460)
    committed = None
    if len(sample) >= 5:
        print("| p_red | " + " | ".join(f"P(>={k})" for k in (1, 2, 3, 4)) + " |")
        print("|---|---|---|---|---|")
        for p_red in (0.0, 0.25, 0.5):
            r = ns.simulate(sample, budget_h=hours, p_red=p_red)
            print(f"| {p_red:.2f} | " + " | ".join(f"{r[k]:.0%}" for k in (1, 2, 3, 4)) + " |")
        mid = ns.simulate(sample, budget_h=hours, p_red=0.25)
        # commit to the largest round count still at or above 85% — high enough that an unfinished round,
        # which leaves a tree someone else must untangle, is the exception rather than the plan
        committed = max([k for k, v in mid.items() if v >= 0.85] or [1])
        expected = max([k for k, v in mid.items() if v >= 0.50] or [1])
        print(f"\n**Commit to {committed} round(s)** (>=85% at p_red 0.25). **Expect {expected}.** "
              f"Anything beyond {expected} is a stretch, taken whole or not at all.")
        print(f"\n**Do not start a round below {dur['p75_h']}h remaining** — the p75 duration. "
              "A half-built round is worse than none.\n")

    print("## 3 · Where the open work sits (candidates, not a chosen batch)\n")
    for slot, ids in list(open_rows_by_slot().items())[:10]:
        print(f"- **{slot}** — {len(ids)} row(s): {', '.join(ids[:8])}{' …' if len(ids) > 8 else ''}")
    print("\n**Ordering rule (WSJF-shaped):** value over duration. A stale document that misstates what is "
          "blocked is near-zero duration and can unblock several items, so it goes first. A row that measurement "
          "may already have satisfied goes before a build — this register systematically over-states outstanding "
          "work.\n")
    print("**Batching rule and its bound:** amortise ONE full suite over several *coherent* changes (same "
          "subsystem or same defect class). The bound is the attribution test — **if a red suite could not be "
          "attributed to one batched change within one diagnosis pass, the batch was too big.**\n")

    print("## 4 · Before each round\n")
    print("1. `git status --short` is empty, or do not start.")
    print("2. Measure each row's LIVE state before building; a close names the state it measured.")
    print("3. `python scripts/coupling.py <file>` for every file to be changed — update the readers it names, "
          "or record why not.")
    print("4. Diff-scoped selector first; ONE full suite last, exit code captured explicitly.")
    print("5. New guard? Drive it red, restore with an asserted SHA, before trusting green.\n")

    print("## 5 · Stop rules, fixed in advance so 04:00 needs no judgement\n")
    print("- red suite → **one** diagnosis pass → stop, write up, leave the tree clean.")
    print("- a second red suite → stop. The error budget is one full re-run.")
    print(f"- round exceeding p75 ({dur['p75_h']}h) → special cause; investigate, do not accelerate.")
    print("- anything whose honest answer is a ruling → park it, never decide it.")
    print("- owner-gated switches, and any decision reserved to the Owner → untouched.\n")
    print("## 6 · Run it THROUGH Workstation, not beside it\n")
    print("The canon (WHOLE_VISION line 347): *the organism delivers its own transformation through its own org;")
    print("dogfood is the design, not an afterthought.* The cascade is **Chief -> Board -> AI CEO -> C-Suite ->")
    print("CoE -> BTO -> Build-to-Order -> Change Control** (lines 101, 345). The VSB is the CONTAINER of that")
    print("org, not a link in it, and the Products Catalogue is a PEER of Build-to-Order, which the BTO also runs.\n")
    print("Measured working (W514 dogfood, isolated store): `POST /api/v1/cca/submit` returns a cca id with an")
    print("impact tier, a real method_check, scope_appraisal and health_gate; the change reaches")
    print("`/api/v1/cca/queue` carrying awaiting_board_ratification; `POST /api/v1/transformation/orchestrate`")
    print("returns a method_check citing lesson ids, a governance verdict that states its own limit, and the")
    print("live products/services catalogue.\n")
    print("**So each round submits its change to `/api/v1/cca/submit` and puts the returned cca id in the commit")
    print("message.** The round is then governed by the platform's own arms-length agency rather than by a")
    print("convention in a document.\n")
    print("**The gap, and the bootstrap (FU-313).** Nothing in the CCA record, the queue or `GET /cca/{id}` holds")
    print("a commitment, confidence, variance, budget or capacity field — `committed_rounds` and `confidence` are")
    print("silently dropped by the response model. So Workstation can govern a change but cannot yet hold THIS")
    print("PLAN. Round A therefore builds that field first, and from Round B the plan lives in Workstation rather")
    print("than in a markdown file. The process's first act is to make the platform able to host it.\n")
    print("## 7 · Alignment artefacts (so a sleeping Owner can verify cold)\n")
    print("- every round is ONE commit; `git log --oneline` is the report.")
    print("- refresh the handover's state section at every round boundary — that section only.")
    print("- write the night report at the START of the last affordable round, not after.")
    print("- keep `docs/NIGHT_STATE.json` current: round, status, commit, suite result, what was left undone.")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 8.0)
