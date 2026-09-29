"""Monte Carlo over the ACTUAL plan, bootstrapped from this repository's measured round durations.

Prepared W514. Everything before this was a point estimate with bands; this answers the question the bands
cannot: what is the PROBABILITY each planned round completes inside 8 hours?

METHOD. Empirical bootstrap — resample observed round durations with replacement rather than assuming a
distribution. Round durations here are right-skewed (median 2.21h, max 4.87h), so a normal assumption would
understate the tail, which is exactly the tail that ruins an unattended night.

TWO CORRECTIONS THE RAW SAMPLE NEEDS, both stated rather than buried:
  1. Gaps above 5h are excluded as containing idle (the Owner asleep). An interval is not a duration.
  2. A RED SUITE costs a full re-run (0.91h measured). Its probability is a stated ASSUMPTION, not a
     measurement - the history does not record which rounds needed a second suite - so the result is shown
     across a sensitivity range instead of at one value I cannot defend.

WHAT IT DELIBERATELY DOES NOT MODEL: a round that turns out to be a decision (finishes in minutes), and the
fact that the sample includes the Owner's replies, so an unattended night may run faster than its own history.
Both bias the result PESSIMISTIC, which is the safe direction for a plan.
"""
import random
import statistics
import subprocess
import re

IDLE_CAP_H = 5.0
SUITE_H = (3274 + 3200) / 2 / 3600     # two measured full runs: 54m34s and 53m20s
TRIALS = 20000


def observed(since: int = 460):
    log = subprocess.run(["git", "log", "--format=%at\x1f%s", "-400"], capture_output=True, text=True).stdout
    rounds = {}
    for line in log.splitlines():
        p = line.split("\x1f")
        if len(p) < 2:
            continue
        m = re.search(r"\bW(\d{3})\b", p[1])
        if m:
            rounds.setdefault(int(m.group(1)), []).append(int(p[0]))
    ends = {r: max(t) for r, t in rounds.items()}
    rs = sorted(ends)
    out = []
    for a, b in zip(rs, rs[1:]):
        if b - a == 1 and b >= since:
            g = (ends[b] - ends[a]) / 3600.0
            if 0 < g <= IDLE_CAP_H:
                out.append(g)
    return out


def simulate(sample, budget_h=8.0, p_red=0.25, n_rounds=4, trials=TRIALS):
    """Returns P(at least k rounds complete) for k = 1..n_rounds."""
    done = [0] * (n_rounds + 1)
    rng = random.Random(20260930)          # fixed seed: a rerun must reproduce
    for _ in range(trials):
        t = 0.0
        for k in range(1, n_rounds + 1):
            d = rng.choice(sample)
            if rng.random() < p_red:
                d += SUITE_H               # one extra full suite to re-verify
            t += d
            if t <= budget_h:
                done[k] += 1
            else:
                break
    return {k: done[k] / trials for k in range(1, n_rounds + 1)}


if __name__ == "__main__":
    for since, label in ((460, "W460+ (n=28, longer tail)"), (490, "W490+ (n=8, recent regime)")):
        s = observed(since)
        if len(s) < 5:
            print(f"{label}: only {len(s)} samples - refused")
            continue
        print(f"\n{label}  median {statistics.median(s):.2f}h  max {max(s):.2f}h  suite {SUITE_H:.2f}h")
        for p_red in (0.0, 0.25, 0.5):
            r = simulate(s, p_red=p_red)
            print("   p_red=%.2f  " % p_red + "  ".join(f"P(>={k})={v:.0%}" for k, v in r.items()))
