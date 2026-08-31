# `_archive/jules-unwired/` — Jules-era modules nothing reaches (2026-08-31)

**206** Python modules moved here from the live tree. They are **not deleted** — every move was
`git mv`, so full history is preserved and any of them comes back with one command.

## Why these files
The repository carries work from two authors: `Rehan719` (859 commits) and
`google-labs-jules[bot]` (534 commits). **1,276 Jules-created files were still in the live tree.**
Jules built real, load-bearing things — the AI gateway, memory, the orchestrator, much of `api/` —
so authorship alone is not grounds for archiving anything. **512 of those Python modules are
provably in use and stayed.**

## How these 259 were chosen (four independent signals, all had to agree)
1. **Authorship** — originally created by `google-labs-jules[bot]` (`git log --diff-filter=A`).
2. **Static unreachability** — absent from an AST import-reachability closure built from the live
   entrypoints (`app_mvp.py`, the integration suite, the live scripts), capturing top-level, lazy
   in-function, relative **and** dynamic string imports.
3. **Runtime absence** — absent from `sys.modules` after booting the app and exercising **34 real
   endpoints** (all 34 returned < 500).
4. **No string reference** — the module path appears in no quoted string anywhere in live source,
   so a dynamic import cannot be reaching it.

Any single "live" signal kept a file. This is deliberately conservative.

## Deliberately NOT archived, though they met the criteria
- **`agentic_core/mesh/**` (6 modules)** — the Owner decided on 2026-08-31 (federation option A) to
  keep the mesh in place until a second instance exists. Archiving it would contradict a live
  decision.
- **`agentic_core/network/**` (4 modules)** — `_archive/README.md` records that this package was
  found to be **dynamically imported** by reachable code during the June 2026 cleanup and had to be
  restored. Static analysis called it dead then, too.

## Deviation from the June rule, stated plainly
The June cleanup archived only **fully-unwired top-level directories** and kept partial ones intact.
Re-running that analysis today found **zero** fully-unwired directories — June took them all. So this
pass went finer: individual modules **inside** partially-live packages, which is genuinely riskier.
That is why the evidence bar was four agreeing signals, the two exclusions above apply, and the move
was verified against the running system rather than by imports alone.

## CORRECTION — 53 of the original 259 were wrong, and CI caught it

The first pass moved **259** modules. **53 were live** and had to come back. Read this before
trusting the method below, because the method is what failed:

- **The string sweep had a hole in the instrument.** It matched only fully-quoted tokens,
  `['"]([A-Za-z0-9_.]+)['"]`, so it could not see a module named *inside* a multi-word string. The
  Doc-Sync workflow runs
  `python -c "from agentic_core.synthesis.doc_linter import DocumentationLinter; ..."` — one quoted
  string containing spaces. The sweep never saw it, and a live file was archived. CI went red.
- **The runtime signal is blind by construction** to anything that only runs in a separate CI job,
  a setup script, or the Dockerfile. `scripts/init_data.py` (used by `setup.ps1`) and
  `scripts/verify_environment.py` (used by `setup_windows.ps1`) were archived this way, silently
  breaking environment setup for anyone who cloned the repo.
- **A green test suite proved only that the suite does not cover those paths.** It is not evidence
  of deadness, and it was read as if it were.

Restored: 4 referenced from infrastructure, and 49 named in real import statements by live code —
the latter to a **fixed point**, because restoring a module surfaces its own archived dependencies
(it took two rounds).

**A guard now exists so this cannot recur silently:** `scripts/check_import_integrity.py` runs in
Spine CI and fails on any live module importing a first-party module with no file behind it. It was
proven to bite by re-injecting the exact defect, not assumed to work.

**What the four-signal method still cannot see**, established the same day: files reached by a
runtime *directory scan* rather than by name. `agentic_core/catalog/api.py` does
`PRODUCTS_DIR.iterdir()`, so every directory under `products/` is reached by existence alone. An
import-based analysis would have called them all dead. Nothing under `products/` was ever archived,
so no harm was done — but the blind spot is real and applies to any future pass.

## Verification after the move
- App boots.
- **34/34** endpoint probes still pass; the live-module count was **unchanged at 304** — nothing that
  was live got archived.
- Browser smoke: 8 routes render, no console errors, no fabrications.
- **Full integration suite: 310 passed / 15 skipped** (this is the weakest of the checks — see
  the correction above; it stayed green while a live file sat in the archive), only the known `test_data_dir_configurable`
  DATA_DIR artifact (green on CI).

## Restoring something
```bash
git mv _archive/jules-unwired/<path> <path>
```

## Commit-hygiene note
These 259 renames were swept into commit `7a1aa7dd` (the W382 WebSocket fix) by an over-broad
`git add -A`. Two unrelated changes landed under one message that mentions only the WebSocket work.
The commit was already pushed, and rewriting shared history would be worse than the mess, so it is
recorded here instead of hidden.
