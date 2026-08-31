# `_archive/jules-unwired/` — Jules-era modules nothing reaches (2026-08-31)

259 Python modules moved here from the live tree. They are **not deleted** — every move was
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

## Verification after the move
- App boots.
- **34/34** endpoint probes still pass; the live-module count was **unchanged at 304** — nothing that
  was live got archived.
- Browser smoke: 8 routes render, no console errors, no fabrications.
- **Full integration suite: 310 passed / 15 skipped**, only the known `test_data_dir_configurable`
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
