"""DRAFT — a WALL-CLOCK capacity forecast for an unattended working session. Prepared W514, not applied.

Intended path: scripts/session_forecast.py, served at GET /api/v1/method/session-forecast.

WHY THIS IS NOT A DUPLICATE FORECASTER. `plan_followups.forecast()` is the one forecaster of the PLAN and
deliberately projects in ROUNDS, never in dates (M-FCAST: a date implies a promise the register cannot make).
It cannot answer the question an unattended session actually poses: "how many rounds fit in the N hours I have?"
That is a different quantity measured from a different source — git wall-clock, not the register — so it is added
beside the plan forecaster rather than inside it, and it never restates the plan's rate.

THE MEASUREMENT, AND THE ONE CORRECTION THAT MAKES IT HONEST. A round's duration is taken as the gap between
consecutive rounds' final commits. Raw, that figure is WRONG for this purpose: over W490+ it reads a median of
5.08h, because most gaps contain the Owner asleep or away. An interval is not a duration. Gaps above
IDLE_CAP_H are therefore excluded as containing idle, and the excluded count is REPORTED rather than dropped
silently — a filtered population that does not say what it filtered is how a rate quietly becomes a wish.

Measured on this repository at W514:
  · continuous round duration, W490+ : n=8,  median 2.15h  (p25 1.82, p75 2.63, max 3.72)
  · continuous round duration, W460+ : n=28, median 2.21h  (p25 1.63, p75 3.72, max 4.87)
  · the full serial suite            : 3274s = 0.91h
The two windows below are NESTED (W490+ is a subset of W460+), so their agreement corroborates nothing --
W514's audit confirmed that is false by construction, not by data. The figure IS corroborated, but by a
DISJOINT test run afterwards: first half W449-486 median 1.97h against second half W487+ median 2.43h,
differing by 0.46h.

THE FINDING THAT SHOULD CHANGE HOW A NIGHT IS PLANNED. The suite is a FIXED 0.91h per round and is 41% of a
median round. Round boundaries, not typing, are what an 8-hour session spends itself on: 5 rounds pay 4.55h of
suite and 3 rounds pay 2.73h, so choosing fewer, larger rounds converts ~1.8h of verification overhead into
working time — about one extra round's worth of actual work, for free. This is the quantified case for batching.
"""
import re
import pathlib
import statistics
import subprocess
import importlib.util as _ilu


def _consts():
    _s = _ilu.spec_from_file_location("_sm", pathlib.Path(__file__).resolve().parent / "_session_measured.py")
    _m = _ilu.module_from_spec(_s); _s.loader.exec_module(_m); return _m


K = _consts()
from typing import Any, Dict, List, Optional

IDLE_CAP_H = K.IDLE_CAP_H
#  THE MODE IN USE. It read a mode-free `SUITE_H` that was the SERIAL mean, so `share_of_a_median_round`
#  reported 44% — a serial suite over a median computed with a serial floor: internally consistent,
#  externally meaningless, and 2.75x the measured 16%.
SUITE_H = K.SUITE_IN_USE_H
          # below this, refuse rather than project


def _round_ends(limit: int = 400) -> Dict[int, int]:
    """Final commit timestamp per W-round, newest `limit` commits."""
    out: Dict[int, List[int]] = {}
    log = subprocess.run(["git", "log", f"--format=%at\x1f%s", f"-{limit}"],
                         capture_output=True, text=True).stdout
    for line in log.splitlines():
        p = line.split("\x1f")
        if len(p) < 2:
            continue
        m = re.search(r"\bW(\d{3})\b", p[1])
        if m:
            out.setdefault(int(m.group(1)), []).append(int(p[0]))
    return {r: max(ts) for r, ts in out.items()}


def round_durations(since: int = 449) -> Dict[str, Any]:
    """Delegates to night_sim.classify() so there is ONE filter, not two.

    W514 audit: this function had its own cap-5h filter with no lower bound and no daytime retention, so the
    same generated plan printed n=30/median 2.14h here and n=39/median 2.51h from the simulator. Two filters
    for one quantity is the defect the constants module exists to remove, one level up.
    """
    import importlib.util as _il
    _spec = _il.spec_from_file_location("_ns", pathlib.Path(__file__).resolve().parent / "night_sim.py")
    _ns = _il.module_from_spec(_spec)
    _spec.loader.exec_module(_ns)
    kept, dropped = _ns.classify(since)
    if len(kept) < K.MIN_SAMPLE:
        return {"assessable": False,
                "why": (f"only {len(kept)} round(s) survived the stated filters; no rate is substituted, "
                        "because a projection from a handful of rounds is a guess wearing a number")}
    return {"assessable": True, "n": len(kept),
            "median_h": round(statistics.median(kept), 2),
            "p25_h": round(kept[len(kept) // 4], 2),
            "p75_h": round(kept[3 * len(kept) // 4], 2),
            "max_h": round(kept[-1], 2),
            "excluded": {k: len(v) for k, v in dropped.items() if v},
            "excluded_detail": {k: v for k, v in dropped.items() if v},
            "basis": ("gap between consecutive rounds' final commits; a gap shorter than one full suite is a "
                      "follow-up commit not a round, a gap spanning the sleeping hours is idle, and a long "
                      "DAYTIME gap is kept as a long round")}


#  FU-415 — ONE WRITER for the honest-limits list, because BOTH returns carry it now. It was inline in the
#  full path only, so the early return — the one that cannot measure anything — was the one that said nothing
#  about what it could not know.
_WHAT_THIS_CANNOT_KNOW = (
    "a round that turns out to be a DECISION rather than a build finishes in minutes and skews the rate",
    "a red suite that needs more than one diagnosis pass is unbounded, and the contingency covers only one",
    "the durations include the Owner's replies, so an unattended night may run faster than the sample",
    "a measurement round (a row closed by reading the tree) costs a fraction of a build round and the "
    "sample does not separate them",
)


def forecast_session(hours: float, since: int = 460,
                     red_suite_contingency: bool = True) -> Dict[str, Any]:
    """How many complete rounds fit in `hours`, with the bands and what the arithmetic cannot know."""
    d = round_durations(since)
    #  FU-415 — EVERY KEY DECLARED ONCE, HERE. The early return below used to build a four-key answer where
    #  the full path builds eight, so a guard reading `round_boundaries_cost` failed with "the forecast no
    #  longer reports the round-boundary cost" when the real answer was "the history could not be walked" —
    #  and `what_this_cannot_know` was dropped exactly when the arithmetic could not know anything. Declaring
    #  the set here rather than in each return means no path can omit a key, because no path builds the set.
    out: Dict[str, Any] = {
        "hours_available": hours,
        "round_durations": d,
        "suite_h": round(SUITE_H, 2),
        "projection": None,
        "contingency": None,
        "round_boundaries_cost": None,
        "second_window_W490_plus": None,
        "what_this_cannot_know": list(_WHAT_THIS_CANNOT_KNOW),
    }
    if not d.get("assessable"):
        #  Fill what IS knowable without the durations, and say what is not. The contingency needs no
        #  history at all, and three of the round-boundary fields are constants — nulling the whole dict
        #  would throw away measurements that were available, which is the same defect from the other side.
        out["projection"] = {"unavailable": d["why"]}
        out["contingency"] = ({"reserved_h": round(SUITE_H, 2),
                               "why": "one red suite costs a full re-run; W513 spent exactly this tonight"}
                              if red_suite_contingency else None)
        out["round_boundaries_cost"] = {
            "suite_h_per_round": round(SUITE_H, 2),
            "suite_mode": K.SUITE_MODE_IN_USE,
            "suite_basis": K.SUITE_IN_USE_BASIS,
            "share_of_a_median_round": None,
            "share_basis": None,
            "suite_cost_at_n_rounds": None,
            "implication": ("the suite is FIXED per round, so fewer and larger rounds convert verification "
                            "overhead into working time; two extra round boundaries cost about one round's "
                            "work"),
            "basis": (f"the three fields that divide by the median round are NOT MEASURED, not zero: the "
                      f"durations could not be walked ({d['why']}). A zero share would read as a suite that "
                      f"costs nothing per round."),
        }
        return out

    usable = hours - (SUITE_H if red_suite_contingency else 0.0)
    out["contingency"] = ({"reserved_h": round(SUITE_H, 2),
                           "why": "one red suite costs a full re-run; W513 spent exactly this tonight"}
                          if red_suite_contingency else None)

    def band(h: float) -> float:
        return round(usable / h, 1) if h else 0.0

    out["projection"] = {
        "expected_rounds": band(d["median_h"]),
        "if_rounds_run_fast": band(d["p25_h"]),
        "if_rounds_run_slow": band(d["p75_h"]),
        "worst_observed": band(d["max_h"]),
        "worst_case_round_count": int(usable // d["p75_h"]),   # NOT the commitment: night_sim owns that
        "why_p75": ("a night is planned on the SLOW band, because an unfinished round leaves a tree someone "
                    "else has to untangle, while an early finish only means pulling the next item forward"),
    }
    # the batching arithmetic, stated rather than left implicit
    n_med = max(1, int(usable // d["median_h"]))
    out["round_boundaries_cost"] = {
        "suite_h_per_round": round(SUITE_H, 2),
        "suite_mode": K.SUITE_MODE_IN_USE,
        "suite_basis": K.SUITE_IN_USE_BASIS,
        "share_of_a_median_round": f"{round(100 * SUITE_H / d['median_h'])}%",
        "share_basis": (f"the {K.SUITE_MODE_IN_USE} suite ({SUITE_H:.2f}h) over the median round "
                        f"({d['median_h']}h); both sides must come from the same mode, because a "
                        f"serial suite over a parallel-floored median is a ratio of two different "
                        f"things"),
        "suite_cost_at_n_rounds": {f"{n} rounds": round(n * SUITE_H, 2) for n in (n_med, n_med + 2)},
        "implication": ("the suite is FIXED per round, so fewer and larger rounds convert verification "
                        "overhead into working time; two extra round boundaries cost about one round's work"),
        #  FU-415 — the same key the unmeasurable path carries, so the dict's shape does not change with the
        #  answer. Here it says the fields WERE measured; there it says which three could not be.
        "basis": (f"measured: the share and the per-n costs are computed from the median round "
                  f"({d['median_h']}h) in the {K.SUITE_MODE_IN_USE} suite mode."),
    }
    # TWO WINDOWS, BOTH REPORTED. The recent regime and the wider history disagree about the SLOW band
    # (W490+ p75 2.63h vs W460+ p75 3.72h) and the night's committed round count turns on which is used.
    # Reporting one silently would hide the disagreement behind a single number, so both are shown and the
    # plan takes the more conservative — an unfinished round costs more than an idle half hour.
    alt = round_durations(490)
    if alt.get("assessable"):
        out["second_window_W490_plus"] = {
            "n": alt["n"], "median_h": alt["median_h"], "p75_h": alt["p75_h"],
            "plan_for": int(usable // alt["p75_h"]),
            "note": ("the recent regime is tighter and more representative of today's round size, but n is "
                     "small; the wider window has n=28 and a longer tail"),
        }
        out["projection"]["worst_case_both_windows"] = min(
            int(usable // d["p75_h"]), int(usable // alt["p75_h"]))
        out["projection"]["worst_case_basis"] = (
            "the LOWER of two NESTED windows' slow bands -- a worst case, NOT the commitment. The committed and "
            "expected counts come from night_sim.committed_and_expected(), which is the one rule that decides them")

    out["what_this_cannot_know"] = list(_WHAT_THIS_CANNOT_KNOW)
    return out


if __name__ == "__main__":
    import json
    import sys
    hrs = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    print(json.dumps(forecast_session(hrs), indent=2))
