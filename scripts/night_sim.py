"""Monte Carlo over a night's plan, bootstrapped from this repository's measured round durations.

Point estimates and bands cannot answer the question an unattended session poses: what is the PROBABILITY each
planned round completes inside the hours available? This does.

METHOD. Empirical bootstrap — resample observed round durations with replacement rather than assuming a
distribution, because they are right-skewed and a normal assumption would understate exactly the tail that ruins
a night.

W514 AUDIT — FOUR CORRECTIONS, each of which moved the answer:
  1. Gaps above IDLE_CAP_H were dropped as "idle". 6 of 19 excluded gaps turned out to be DAYTIME, i.e.
     plausibly long rounds, and discarding them inflated P(>=2 rounds) from 75% to 91%. A gap is now excluded
     only when it spans the sleeping hours; a long daytime gap up to DAYTIME_KEEP_MAX_H is KEPT as a long round.
  2. There was no LOWER bound, so six gaps of 0, 5, 11, 12 and 28 minutes — plus one NEGATIVE gap of -1.95h,
     commits not being monotonic in round number — counted as rounds. A round cannot be shorter than the suite
     it must run (MIN_ROUND_H).
  3. The printed window labels hard-coded "n=28" and "n=8" while the real sizes were 30 and 10. n is computed.
  4. SUITE_H lived here AND in session_forecast.py with different values. It now has one home.

WHAT IT STILL CANNOT KNOW, and does not pretend to: rounds are resampled INDEPENDENTLY, though a hard night
plausibly stays hard; a round that turns out to be a decision finishes in minutes; and the sample includes the
Owner's reply time, so an unattended night may run faster than its own history. All three bias the result
pessimistic, which is the safe direction for a plan.

`p_red`, the chance a round needs a second full suite, is an ASSUMPTION — n=1 in the record, which is no rate at
all — so results are reported across a range instead of at one indefensible value.
"""
import datetime
import importlib.util
import pathlib
import random
import re
import statistics
import subprocess
from typing import Dict, List, Tuple

_HERE = pathlib.Path(__file__).resolve().parent


def _consts():
    spec = importlib.util.spec_from_file_location("_sm", _HERE / "_session_measured.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K = _consts()
SUITE_H = K.SUITE_H
TRIALS = 20000


def _round_ends(depth: int = 400) -> Dict[int, int]:
    out: Dict[int, List[int]] = {}
    log = subprocess.run(["git", "log", "--format=%at\x1f%s", f"-{depth}"],
                         capture_output=True, text=True).stdout
    for line in log.splitlines():
        p = line.split("\x1f")
        if len(p) < 2:
            continue
        m = re.search(r"\bW(\d{3})\b", p[1])
        if m:
            out.setdefault(int(m.group(1)), []).append(int(p[0]))
    return {r: max(ts) for r, ts in out.items()}


def _spans_sleep(start_epoch: int, hours: float) -> bool:
    st = datetime.datetime.fromtimestamp(start_epoch, datetime.UTC)
    return any((st + datetime.timedelta(hours=h)).hour in K.SLEEP_HOURS_UTC
               for h in range(int(hours) + 1))


def observed(since: int = 449, depth: int = 400) -> List[float]:
    """Round durations, with every exclusion decided by a stated property rather than by a bare threshold."""
    return classify(since, depth)[0]


def classify(since: int = 449, depth: int = 400) -> Tuple[List[float], Dict[str, List[Tuple[int, float]]]]:
    """Returns (kept durations, {reason: [(round, hours)]}) so a filter can report WHAT it excluded, not
    only how many. W514: a filter reporting a bare count of 19 concealed that 6 of them were real rounds."""
    ends = _round_ends(depth)
    rs = sorted(ends)
    kept: List[float] = []
    dropped: Dict[str, List[Tuple[int, float]]] = {"shorter_than_one_suite": [], "spans_sleeping_hours": [],
                                                   "daytime_but_over_cap": []}
    for a, b in zip(rs, rs[1:]):
        if b - a != 1 or b < since:
            continue
        g = (ends[b] - ends[a]) / 3600.0
        if g < K.MIN_ROUND_H:
            dropped["shorter_than_one_suite"].append((b, round(g, 2)))
            continue
        if g <= K.IDLE_CAP_H:
            kept.append(g)
            continue
        if _spans_sleep(ends[a], g):
            dropped["spans_sleeping_hours"].append((b, round(g, 2)))
        elif g <= K.DAYTIME_KEEP_MAX_H:
            kept.append(g)                      # a long DAYTIME gap is a long round, not idle
        else:
            dropped["daytime_but_over_cap"].append((b, round(g, 2)))
    return sorted(kept), dropped


def simulate(sample: List[float], budget_h: float = 8.0, p_red: float = 0.25,
             n_rounds: int = 4, trials: int = TRIALS) -> Dict[int, float]:
    """P(at least k rounds complete) for k = 1..n_rounds. A round that overruns ends the trial, because a
    later round cannot start in time that has already been spent."""
    done = [0] * (n_rounds + 1)
    rng = random.Random(20260930)               # fixed: a rerun must reproduce
    for _ in range(trials):
        t = 0.0
        for k in range(1, n_rounds + 1):
            d = rng.choice(sample)
            if rng.random() < p_red:
                d += SUITE_H
            t += d
            if t <= budget_h:
                done[k] += 1
            else:
                break
    return {k: done[k] / trials for k in range(1, n_rounds + 1)}


def committed_and_expected(sample: List[float], budget_h: float = 8.0,
                           p_red: float = 0.25) -> Tuple[int, int, Dict[int, float]]:
    """The ONE rule that decides a commitment, so no prose has to override a number."""
    r = simulate(sample, budget_h=budget_h, p_red=p_red)
    committed = max([k for k, v in r.items() if v >= K.COMMIT_CONFIDENCE] or [0])
    expected = max([k for k, v in r.items() if v >= K.EXPECT_CONFIDENCE] or [0])
    return committed, expected, r


if __name__ == "__main__":
    print(f"suite: {SUITE_H:.2f}h ({K.SUITE_BASIS})")
    for since in (449, 490):
        s, dropped = classify(since)
        if len(s) < K.MIN_SAMPLE:
            print(f"\nW{since}+: only {len(s)} sample(s) — refused, no rate substituted")
            continue
        tail = "longer tail" if max(s) > 4.0 else "recent regime"
        print(f"\nW{since}+ (n={len(s)}, {tail})  median {statistics.median(s):.2f}h  "
              f"p75 {s[3 * len(s) // 4]:.2f}  max {max(s):.2f}")
        for reason, items in dropped.items():
            if items:
                print(f"   excluded — {reason}: {len(items)} {items}")
        for p_red in (0.0, 0.25, 0.5):
            c, e, r = committed_and_expected(s, p_red=p_red)
            print("   p_red=%.2f  " % p_red + "  ".join(f"P(>={k})={v:.0%}" for k, v in r.items())
                  + f"   -> commit {c}, expect {e}")
