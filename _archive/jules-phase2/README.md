# `_archive/jules-phase2/` — the non-Python Jules-era leftovers (2026-08-31)

166 files moved here from the live tree by `git mv`, so history is preserved and any of them comes
back with one command. This is the second archive pass. The first (`_archive/jules-unwired/`) covered
Python modules and **got 53 of its 259 moves wrong** — read that folder's README before trusting any
method described here, including this one.

## Why a second pass needed a different argument
Import-reachability says nothing about a YAML file, a release note, or a `.docx`. Each file here was
assessed on the channel that could actually reach it: a runtime file read, a glob over a parent
directory, a CI or Docker reference, a frontend fetch, or a link from a doc of record.

## What is here, by kind

**Fabricated status and certification artefacts (the "hallucination work")** — documents asserting
things that are not true and were produced by no measuring code:
- `meta/SHARIA_AUDIT_v100.0.json`, `meta/SHARIA_COMPLIANCE_AUDIT_v*.json` — halal sign-offs carrying
  an invented `"digital_signature": "SIG_V100_SYNERGY_HALAL"` and an "auditor" that is a code module.
  A fabricated religious certification is the single worst thing in this set; it is exactly the kind
  of artefact that must not sit in a repository looking authoritative.
- `meta/REGULATORY_COMPLIANCE.md` — claims alignment with ISO/IEC 42001, NIST AI RMF and the EU AI Act.
- `meta/CONVERGENCE_REPORT_v*.json`, `meta/FINAL_RELEASE_REPORT_v*.json`, `meta/FINAL_VALIDATION_REPORT.json`,
  `meta/PHASE_0_VERIFICATION_REPORT.md` — 100%-pass records for tests and services that do not exist.
- `docs/releases/*` (19) — version-stamped release reports for v71 … v139 releases that have no code,
  no tag and no CI run, several certifying "zero placeholder" and "100% legal coverage".
- `docs/api_spec.yaml` — an OpenAPI spec for an API this app does not serve.

**Dead CI automation** — these stop running now that they are out of `.github/workflows/`:
- `jules-auto-merge.yml` — **a standing unattended-merge path**: it ran `gh pr merge --auto --merge`
  on any PR labelled `ready-to-merge`, for an agent no longer in use. Removing it closes that path.
- `jules-trigger.yml` — invoked `google-labs-code/jules-action` on an issue label.
- `release.yml` — built `src/qep_frontend`, which does not exist, so it failed on every `v*` tag.
- `self-improve.yml` — a weekly job whose only real command was commented out.

**Regenerable machine write-targets** — files some script writes and nothing ever reads:
`docs/knowledge/biomimetic_ingestion_*.md`, `ingestion_*.md`, `convergence_delta.md`,
`unified_assimilation_v120.json`, and the 21 generated `PROP-*.{docx,html,pptx,svg,xlsx}` deliverables
under `products/signature-product-suite/outputs/v8_reports/`.

**Committed build artefacts and fixtures** — two `*.egg-info/PKG-INFO`, `meta/*_test.json` fixtures
shadowing the real stores, `meta/documents/` (a snapshot store with no reader), empty `.gitkeep`
placeholders, and a zero-byte `meta/evolution.log`.

**Frontend orphans** (7) — `.ts`/`.tsx` files no module imports, confirmed by resolving the full
import graph from `main.tsx` honouring the tsconfig/vite aliases, and then by a clean production
build after removal: `ai/AICapabilityDashboard.tsx`, `ai/sovereign-client.ts`,
`components/qep/community/Marketplace.tsx`, `hooks/usePersonalization.ts`, `hooks/useWebSocket.ts`,
`lib/utils.ts`, `store/modeStore.ts`.

## Kept despite looking archivable
- **Everything under `products/`** except four loose JSON files. `agentic_core/catalog/api.py` does
  `PRODUCTS_DIR.iterdir()` and publishes the result as the live product catalog, so those directories
  are reached **by existence**, never by name — an import-based analysis calls them all dead. The four
  `VeritasSeriesManifest*.json` files are excluded by the route's own `entry.is_dir()` filter, which
  was executed rather than assumed.
- `src/organism/config/sovereign_config.yaml` — nothing reads it, but `src/organism/AI_INTEGRATION.md`
  (kept) documents it. Archiving it would leave live documentation pointing at a missing file.
- `src/organism/python/{neural/legacy_adapter,organs/nematron_adapter}.py` — both are unimportable
  (they import `agentic_core.nervous_system.nervous_system` and `agentic_core.ai_ceo.c_suite`, neither
  of which exists). An adversarial reviewer flagged them anyway, so they stay. Keeping a dead file
  costs nothing; archiving a live one costs a product.

## Verification after the move
- `scripts/check_import_integrity.py`: clean — no live module imports anything archived.
- App boots: **470 method+route pairs / 447 paths**, unchanged.
- 8 endpoint probes all 200, and `GET /api/v1/catalog/products` still lists **20 products**.
- Frontend: `tsc` 0 errors and a clean production build — proving the 7 orphans were orphans.
- Browser smoke: 8 routes render, no console errors, no fabrications.

## Restoring something
```bash
git mv _archive/jules-phase2/<path> <path>
```

## Addendum — 33 orphan `configs/` files (same pass)
`configs/` is **partially live**: several files are read through env-var *defaults*
(`configs/legal_precision.yaml`, `configs/constitutional_genome_v138.yaml`, `configs/synthesis_urls.json`,
`configs/realms.yaml`, the `configs/workflows/*.yaml` set) — a channel that names a file without any
import and is easy to miss. So this was checked per file, not per directory: 31 kept, 33 moved.

The 33 are version-stamped Jules artefacts (v8.1, v8.2, v8.4, v8.5, v8.8, v8.9, v9.0, v10 … v16,
"omega"), including 18 under `configs/Law/EmploymentTribunal/`. For each: the full path, the basename
and the stem appear nowhere in live source; no f-string or `os.path.join` builds a path into
`configs/`; and nothing globs or walks the directory. All three were checked because a config is
exactly the kind of file a dynamically-built path can reach without ever naming it.

Note: `configs/governance/profiles.yaml` looks missing but was **never in the tree** — the default in
`agentic_core/governance/industry_adaptive.py` is decorative, since that constructor ignores its
`profile_path` argument and hardcodes the profiles inline.

## Addendum — `conscious_organism_v99.py`, the flagship fabrication
329 lines named "conscious organism v99" that **have never been importable by anyone**. It imports
**35 modules that exist nowhere in the repo** — `agentic_core.consciousness.global_workspace`,
`agentic_core.quantum.unified_gateway`, `agentic_core.pc_agent.*`, `agentic_core.transition.*` and
30 more — and its only importer, `src/dashboard/app.py`, reaches for it through a **typo'd path**
(`agentic_core.orchestrator.` where the real package is `orchestration`). So even the one reference
to it was broken.

**Left in place, deliberately:** roughly 30 modules whose only importer was this file
(`governance/grn_modeler.py`, `governance/span_control.py`, `molecular/triad_integration.py`,
`optimization/engine.py`, `config/loader.py`, and the `evolution/{mutation,rearrangement,search}`
sets). They are dead, but the evidence for each is now weaker, not stronger — "no importer at all"
says less than "the only importer cannot run" — and `config/loader.py` is named in a Dockerfile
comment. Keeping a dead file costs nothing; the bar for removal does not drop just because a first
pass succeeded.
