# `_archive/` — unwired code, set aside for a launch-ready codebase

This folder holds `agentic_core/*` and `core/*` modules that were **not wired into the live platform** —
i.e. **not reachable** (statically, lazily, or dynamically) from the running app (`agentic_core/app_mvp.py`)
or the integration suite (`integration_tests/test_mvp_spine.py`), as of 2026-06-24.

## Why
The repository had ~183 top-level backend dirs / ~1402 modules, of which only ~233 modules were actually
reachable from the live app + tests. The rest were mocks, stubs, aspirational scaffolds, alternate
entrypoints, or duplicated/legacy modules ("folders of mocks/stubs"). Per the Owner's directive to
deliver a **professionally-developed, launch-ready, commercially-ready** codebase, the unwired code was
moved here so the live tree contains (close to) only what is integrated and functional.

## How it was determined (safe + verifiable)
1. Built the **import-reachability closure** from the live entrypoints via AST (capturing top-level **and**
   lazy in-function imports + relative imports + dynamic-string imports).
2. Archived only **fully-unwired top-level dirs** (zero reachable modules). Partial dirs (≥1 reachable
   module) were kept intact.
3. Moved with `git mv` (full history preserved).
4. **Verified**: app boots, full integration suite green (174 pass / 0 fail), fabric self-check
   (`/api/v1/native-ai/selfcheck`) all_live, Spine CI green. One dir (`agentic_core/network`) was found to
   be **dynamically** imported by reachable code and was **restored** (kept live).

## Restoring something
Everything here is plain `git mv` — to bring a module back into the live tree:
`git mv _archive/agentic_core/<dir> agentic_core/<dir>` then re-run the suite. Nothing was deleted.

## Note
This was **Stage 1** (whole-dir archival). A later, more surgical Stage 2 may archive unreachable
**modules inside partially-wired dirs**. The real-vs-mock record of the integration sweep is in
`docs/AGENTIC_CORE_INTEGRATION_AUDIT.md`; the canonical vision/state docs are in `docs/`.
