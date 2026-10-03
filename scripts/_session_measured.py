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
# ── the suite, PER MODE ─────────────────────────────────────────────────────────────────
# A SUITE FIGURE MUST SAY WHICH SUITE. `SUITE_H` was the mean of two SERIAL runs and was used as the cost
# of a suite, as the share a suite takes of a round, AND as the floor deciding what counts as a round. The
# suite now runs in parallel. W565 measured what that cost: the serial floor DISCARDED SIXTEEN REAL ROUNDS
# as "follow-up commits", each of them longer than a real parallel suite (n=72 median 2.04h with the serial
# floor, n=88 median 1.74h with the measured one), and the share reported 44% against a real 16%.
# A constant with one home can still be the wrong constant.
SUITE_RUNS_SERIAL_SECONDS = (3274.26, 3200.20)
SUITE_SERIAL_H = sum(SUITE_RUNS_SERIAL_SECONDS) / len(SUITE_RUNS_SERIAL_SECONDS) / 3600.0   # 0.899 h
SUITE_SERIAL_BASIS = (f"mean of {len(SUITE_RUNS_SERIAL_SECONDS)} measured full SERIAL runs on the "
                      f"W513/W514 tree ({', '.join(f'{s:.0f}s' for s in SUITE_RUNS_SERIAL_SECONDS)})")

# Measured full PARALLEL runs, four workers, one per round, each the round's single full suite.
SUITE_RUNS_PARALLEL_SECONDS = (973.14, 1025.49)
SUITE_PARALLEL_H = (sum(SUITE_RUNS_PARALLEL_SECONDS) / len(SUITE_RUNS_PARALLEL_SECONDS) / 3600.0)
SUITE_PARALLEL_BASIS = (f"mean of {len(SUITE_RUNS_PARALLEL_SECONDS)} measured full PARALLEL runs on four "
                        f"workers, W563 and W564 "
                        f"({', '.join(f'{s:.0f}s' for s in SUITE_RUNS_PARALLEL_SECONDS)})")

# WHICH MODE A ROUND ACTUALLY RUNS. Parallel adoption is GATED on the stall (the register's own row), so
# this says what is run TODAY and not what is approved. A figure derived from the suite must name the mode
# it used; nothing may read a mode-free suite constant, and there is no longer one to read.
SUITE_MODE_IN_USE = "parallel"
SUITE_IN_USE_H = SUITE_PARALLEL_H if SUITE_MODE_IN_USE == "parallel" else SUITE_SERIAL_H
SUITE_IN_USE_BASIS = (SUITE_PARALLEL_BASIS if SUITE_MODE_IN_USE == "parallel" else SUITE_SERIAL_BASIS)

# The FASTEST measured mode, which is the only honest floor for "did this gap contain a suite".
SUITE_FASTEST_H = min(SUITE_SERIAL_H, SUITE_PARALLEL_H)
SUITE_FASTEST_BASIS = ("the fastest measured full-suite mode. A round must contain A suite, so the floor "
                       "has to be the fastest real one: using the serial figure classified sixteen gaps "
                       "that each exceeded a real parallel suite as follow-up commits")

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
MIN_ROUND_H = SUITE_FASTEST_H
MIN_ROUND_BASIS = ("a round must at least contain its own full suite, IN THE FASTEST MODE THAT SUITE HAS "
                   "BEEN MEASURED IN; below that it is a follow-up commit. It was the SERIAL figure, which "
                   "classified sixteen real rounds as follow-up commits — each of those gaps was longer "
                   "than a measured parallel suite, so each could and did contain one. Gaps still below "
                   "the floor in W449+ include one NEGATIVE gap, commits not being monotonic in round "
                   "number")

MIN_SAMPLE = 5          # below this, refuse to project rather than substitute a rate
COMMIT_CONFIDENCE = 0.85   # the ONE rule that decides a committed round count
EXPECT_CONFIDENCE = 0.50   # and the separate rule for the expected count
