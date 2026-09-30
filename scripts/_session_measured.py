"""The measured constants of an unattended working session — defined ONCE, loaded by the other scripts.

WHY THIS FILE EXISTS. W514's audit confirmed that the suite cost was carried as 0.90h in one script and 0.91h
in another (3274/3600 against (3274+3200)/2/3600), and as 41% and 43% of a round in two documents. Four of the
audit's findings were that single class, in artefacts that themselves state "import the constant, never restate
it". A constant with two homes has no home.

LOADED BY PATH, NOT IMPORTED. `plan_night.py` loads its siblings with importlib from an explicit path, so a
plain `import` would break when the scripts are run from a different working directory. The same loader is used
here for the same reason.

EVERY FIGURE BELOW NAMES ITS MEASUREMENT. Nothing here is estimated.
"""

# ── the suite ──────────────────────────────────────────────────────────────────────────────────────────
# Two full serial runs on the W513/W514 tree: 3274.26s (54m34s) and 3200.20s (53m20s).
SUITE_RUNS_SECONDS = (3274.26, 3200.20)
SUITE_H = sum(SUITE_RUNS_SECONDS) / len(SUITE_RUNS_SECONDS) / 3600.0      # 0.899 h
SUITE_BASIS = (f"mean of {len(SUITE_RUNS_SECONDS)} measured full serial runs "
               f"({', '.join(f'{s:.0f}s' for s in SUITE_RUNS_SECONDS)})")

# ── the selector, which is the constraint's only exploit ───────────────────────────────────────────────
# Measured on the same tree. The SINGLE-test figure is the best case and must not be presented as typical:
# a realistic diff-scoped selector runs several tests and pays pytest's fixed collection cost either way.
SELECTOR_RUNS = {"1 test": 49.58, "4 tests": 134.77, "2 tests": 165.13}
SELECTOR_TYPICAL_H = max(SELECTOR_RUNS.values()) / 3600.0                  # the slowest realistic selector
SELECTOR_BASIS = ("measured selector runs: " + ", ".join(f"{k} {v:.0f}s" for k, v in SELECTOR_RUNS.items())
                  + " — the 1-test figure is the BEST case, not the typical one")

# ── the filters on round duration, each with the reason it exists ──────────────────────────────────────
IDLE_CAP_H = 5.0        # above this a gap is examined rather than trusted; see DAYTIME_KEEP_MAX_H
DAYTIME_KEEP_MAX_H = 12.0
SLEEP_HOURS_UTC = (3, 4, 5, 6)
# A round cannot be shorter than the verification it must run. Gaps below this are follow-up commits, not
# rounds: W514 measured six such gaps (0, 5, 11, 12 and 28 minutes, plus one NEGATIVE gap of -1.95h where a
# round's last commit precedes its predecessor's, commits not being monotonic in round number).
MIN_ROUND_H = SUITE_H
MIN_ROUND_BASIS = ("a round must at least contain its own full suite; below that it is a follow-up commit. "
                   "Six gaps in W449+ fall below it, one of them negative")

MIN_SAMPLE = 5          # below this, refuse to project rather than substitute a rate
COMMIT_CONFIDENCE = 0.85   # the ONE rule that decides a committed round count
EXPECT_CONFIDENCE = 0.50   # and the separate rule for the expected count
