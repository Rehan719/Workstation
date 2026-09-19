# Handover — W474 → W475 (Claude Fable 5.1 → Claude Opus)

> **W475 shipped** (2026-09-19, Claude Fable 5.1 → Claude Opus 5): P1.17 ✅ DONE — the fourteen ledger-v4 Tier-1
> entries closed by execution; FU-080…FU-093 closed. §2 and §3 below are history. Refuted twice (25 real findings, 0
> refuted — one class: a fix that changed the API or one writer while a second writer, the reached page or a guard
> leg still said the old untruth), 42 blinds all failing, probe `scripts/_w475_probe.mjs` 12/12 (:8084/:8085), suite
> 386/15/0 (401 items). **Next: MILESTONE M1 re-run (W476)** — §4 below; fresh backend on **:8086**. PLAN NOW names
> P2.1 because a milestone is not an item; the plan text puts the M1 re-run first. Lessons: a test that "restores" a
> method by assigning the bound copy back pins it on the instance and shadows every later class-level patch — patch
> the instance, restore by deleting; a leg that depends on the live Quran source is network-dependent — use a stand-in
> source of plain abjad letters (never type scripture into a test); en dashes do not survive a bash heredoc into
> Python on this machine — use the Edit tool.

Written 2026-09-19 by the Fable 5.1 session at the end of its weekly allowance, on the Owner's instruction. Read
this page, then `docs/HANDOVER_W470.md` §3–§6 (the rhythm, the binding constraints, the lessons, the environment —
all still apply), then `docs/FABLE_DELIVERY_PROMPT.md` whole (the brief). The Owner's standing directive for this
stretch: "continue working through the night doing your best going through the plan" — decide-and-build, honesty
over polish, never fabricate; Owner-gated items (real-money rails, live Stripe, managed Postgres, production deploy,
live external AI key) stay untouched.

## 1. Where things stand (exact)

- **W473 shipped, CI green both** (`cdd7619f`): P1.16 done → Phase P1's first pass complete.
- **W474 = MILESTONE M1, measured, NOT met — finished on disk, COMMIT PENDING at hand-over time.** Check
  `git log -1`: if the head is still `cdd7619f`, the W474 tree is uncommitted and §2 below is your first job. If a
  `docs(W474)` commit exists, skip §2.
  - Ledger v4 rendered to `docs/VISION_FIDELITY_LEDGER.md` (LF; 60 findings, 53 survived, 7 overturned; STUB 8 ·
    DOC_OVERCLAIM 4 · PARTIAL 38 · DELIVERED 10; **standing Tier-1 = 14, Tier-2 19, Tier-3 17**). v3 is
    `git mv`'d to `docs/VISION_FIDELITY_LEDGER_v3.md` (the prompt's `<ledger>` cites its indices).
  - `scripts/render_fidelity_ledger.py` takes `version` and `round`: re-render with
    `python scripts/render_fidelity_ledger.py C:/tmp/w474_fidelity_v4.json docs/VISION_FIDELITY_LEDGER.md cdd7619f 2026-09-19 8083 4 W474`
    (the audit JSON is at `C:/tmp/w474_fidelity_v4.json`; rebuilt from the workflow journal — see §5).
  - Plan: **P1.17 "The second truth pass"** inserted before the M1 line, carrying the fourteen as register rows
    **FU-080…FU-093** (high → they ride P1.17 by the high-severity rule). The M1 line records the measurement.
    PLAN NOW says **Next: P1.17 — 14 follow-ups ride it**. `python scripts/followups.py check` → ok.
  - Docs patched (`patch_docs_w474.py` ran: prompt counters/WHERE THE PLAN STANDS/answer C, living plan §4/§8,
    whole-vision ledger citation, MANDATES.md evidence base, progress entry `### W474`, this session's note in
    `HANDOVER_W470.md`). The progress entry and the commit message still hold the literal `__SUITE__` placeholder.
  - Guards: `test_w473_canon`, `test_w469_the_plan`, `test_w462_followup`, `plan_stands`, `living_plan`, `lockstep`
    → 7 passed on this tree. The **full suite was started** at the hand-over (`/c/tmp/w474_suite.out`, start epoch
    in `/c/tmp/w474_suite_start`); it takes ~37 min. **Never start a second suite while it runs.**

## 2. Finish W474 (if `git log -1` is still cdd7619f)

1. Wait for `/c/tmp/w474_suite.out` to end with `N passed …`. Expect 385/15/0 (400 items). If a register/plan leg
   fails, it is almost always a needle that hard-codes which items are open (W462/W469 legs) — retarget it, re-run
   the leg alone, say so in the entry.
2. Fill the placeholder in both files with the measured line, e.g. `385 passed · 15 skipped · 0 failed (400 items,
   361 functions; 37 min)`: `docs/AUTONOMOUS_PROGRESS.md` (`### W474` entry) and the commit message at
   `…scratchpad/w475/../w474/commit_msg.txt` (scratchpad path in §5).
3. Commit with an EXPLICIT file list (never `git add -A`; `data/` is untracked and ignored — never add it):
   `.gitignore`-free list: `docs/AUTONOMOUS_PROGRESS.md docs/FABLE_DELIVERY_PROMPT.md docs/FOLLOWUPS.json
   docs/VISION_FIDELITY_LEDGER.md docs/VISION_FIDELITY_LEDGER_v3.md docs/WORKSTATION_IDBO_LIVING_PLAN.md
   docs/WORKSTATION_IDBO_WHOLE_VISION.md docs/compliance/MANDATES.md docs/HANDOVER_W470.md docs/HANDOVER_W475.md
   scripts/render_fidelity_ledger.py` (the rename is already staged as `R`; the new ledger is intent-added).
   `git commit -F <commit_msg.txt>` → `git push origin main` → `GITHUB_TOKEN= gh run list --branch main --limit 2`.
4. Memory: `…/memory/project-workstation-current-state.md` already describes W474; add the commit sha + CI verdict.

## 3. W475 = P1.17 The second truth pass (fourteen ledger-v4 Tier-1 entries)

Everything is DRAFTED in the Fable session's scratchpad (§5), from verbatim reads of every site — but NOTHING has
been applied or executed. Treat the drafts as a head start, not as verified work:

- `w475/patch_w475.py` — parts A/B/C: R1.0 (compliance negation window → REVIEW with the phrase; 'haram term
  present' wording; the halal engine's keyword hit on the same negated phrase does not flip it), R1.1 (a
  `Subject:` label in the tafsir prompt so `engine._subject` never takes the Arabic block), R1.2 (management
  systems → `ai_text(augment=False)` + `ai_provenance` + `floor_note` on all seven generators), R2.0 (establishment
  + `/economy/living-vsbs` say the heartbeat lever's truth), R2.1 (`vsb._body_served_by` → 'template' for
  scaffold bodies at both `assure_delivery` sites), R3.0 (`call_meeting`: stance from the last line, floor-served
  = no position, `officers_floor_served`), R3.1 (`gateway._augment._neutral` neutralises `You are the …` in recall
  lines), R3.4 (Chief title + Board page sentence + Cockpit fallback), R4.0 (CommandCenter avatar/predictive/spatio
  + SpatioTemporal 'illustrative'), R4.1 (tree: `decision.recommendation=None` + `basis` when the gate is None;
  minimax voter abstains; NativeAI renders it), R4.2 (`commit_ready` tri-state; run `quality_warning`;
  ResourceFabric chip), R5.0 (drop `enterprise-file-hub` from `ROUTE_OVERRIDES`), R6.0 (`measure` on
  `/transformation/realisation`; the cannot-fail check removed; dashboard label), R6.1 (costs → `operating_costs`
  expense; `CHART` + `_COMPAT_POSTING["costs"]`; `distributable = revenue − costs − reserve`).
  Part C also retargets two suite needles (`commit_ready` bool → tri-state at ~2512/2527).
- `w475/test_w475.py` — the guard, one leg per entry (43 asserts; parses). Append to
  `integration_tests/test_mvp_spine.py` (LF). Uncertain spots to verify by running: the R1.2 memory seed
  (`memory.add_memory` then `query_memory` must recall it — else seed differently), the R2.1 repo POST (a gate may
  refuse; the helper is the rule), the R3.0 call (`tool_registry.call_meeting` via `asyncio`), the R6.1 statements
  needle (`statements()` must name `operating_costs`).
- `w475/mk_break.py` — 18 blinds (uses the W472 harness template; GUARDS w=test_w475_second_truth_pass). Two
  blinds name `RF` for resource_fabric — add `RF = "agentic_core/api/resource_fabric.py"` to the head list if the
  template lacks it (the W472 head has `RF`).
- `w475/_w475_probe.mjs` — copy to `scripts/_w475_probe.mjs`; needs `npm run build` in
  `apps/workstation-superapp` first (never while a suite runs) and a fresh backend on **:8084**.
- `w475/patch_docs_w475.py` — counters + the P1.17 DELIVERED text; the living-plan §4/§8 lines and the progress
  entry are to be written by hand with the measured numbers (the W474 wording of WHERE THE PLAN STANDS / answer C /
  the Tier-1 paragraph must be rewritten once P1.17 is done).

Rhythm for W475 (the same as every round): apply patch → guard green → break (all blinds fail) → refute the diff
in isolated worktrees (Workflow; three lenses + adversarial verify) → fix + re-break → probe on a fresh backend →
full suite on the final tree → docs → register (`close FU-080…FU-093 --by W475`; `done P1.17 --by W475 --hand-to
P2.1`; the hand-off keeps every handed route in place) → commit with an explicit list → push → CI → memory.
CRLF files among P1.17's: `memory_v01.py gateway.py board.py resource_fabric.py transformation.py v138/ceo.py vsb.py
living_vsbs.py TransformationDashboard.tsx VSBEconomy.tsx` — edit only via `putil.apply`/the Edit tool.

## 4. Then W476 = MILESTONE M1 re-run

Boot a fresh backend on :8085 (isolated DATA_DIR, `AI_DISABLE_LOCAL=1`, built bundle), run the W474 workflow
script (`…/workflows/scripts/w474-fidelity-audit-v4-wf_73d530a4-c0b.js` in the Fable session's dir, §5 — change
BASE/HEAD/date), rebuild the per-region JSON from `journal.jsonl` (`started` rows map key→label, the last `result`
per key is the value), render **v5** (add the version branch to the renderer as v4 was added), and record the
Tier-1 count. If it is 0, P1 closes and P2.1 begins; if not, P1.18.

## 5. Paths, ports, lessons

- Fable session scratchpad: `C:\Users\rehan\AppData\Local\Temp\claude\C--Users-rehan-Workstation\12e2760e-c675-46a5-bebf-674b90d8d076\scratchpad\` (`w473/`, `w474/`, `w475/`); `putil.py` lives in
  `…\3c6f55f6-3470-41fd-85ce-49dddc8a0486\scratchpad\w464\putil.py` (asserted replacements, CRLF-aware).
- Workflow scripts/journals: `C:\Users\rehan\.claude\projects\C--Users-rehan-Workstation\12e2760e-…\workflows\scripts\` and
  `…\subagents\workflows\wf_73d530a4-c0b\journal.jsonl` (the v4 audit).
- Ports used: :8083 (W474 audit, stopped). Next free: **:8084** (W475 probe), :8085 (M1 re-run).
- Lessons this stretch: a `git add -u .` snapshot re-stages `git rm --cached` files and drops intent-to-adds —
  snapshot with an explicit list and re-run `git add -N` on new files before `followups.py check`; a `--why` with
  backticks in bash is command-substituted; a Monitor grep for "AssertionError" trips on the harness's own normal
  lines; the workflow task-output file is a JSON object (not `<result>` tags); a blind can look vacuous when a
  second guard refuses the same mistake with the same words — assert the door's own wording; the W462/W469
  register legs hard-code which items are open and break at every `done`.
- Usage limits: a Workflow that dies on the limit resumes with `resumeFromRunId` (finished agents are cached).

## 6. Open with the Owner

FU-079 (chroma_db relocation — two populated copies; the Owner decides which is live). No other OWNER row.
