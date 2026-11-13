# Dependency verdicts — FU-283 (W628)

FU-283 measured 25 of the 43 direct dependencies in `pyproject.toml` as imported by no `.py` under
`agentic_core`, `integration_tests` or `scripts`. It required a verdict for each before anything is removed:
**reached without an import** (name the mechanism), **held for a named plan item**, or **removable**.

How each was checked (2026-10-07, HEAD after W627):

- Every file outside `node_modules`, `.git`, `data/` and `docs/` that names the distribution was listed.
- Substring false positives were discarded (`shap` in "shape", `ray` in "array").
- `_archive/` holds retired code that nothing imports. A dependency named only there and in the lock files is
  used by nothing live.

Owner ruling 2026-10-07b: the REMOVABLE ones may be removed, in a separate commit after these verdicts.

| Distribution | Verdict | Basis |
|---|---|---|
| sqlalchemy | HELD — P4.4 | Managed Postgres migration dry-run; `config/database.py` builds on sqlmodel over it |
| sqlmodel | HELD — P4.4 | `config/database.py` imports it (outside the scanned dirs); the P4.4 store layer |
| psycopg2-binary | HELD — P4.4 | A driver loaded by database URL, never imported; P4.4's Postgres target |
| streamlit | REACHED without a scanned import | `src/dashboard/app.py`, launched by `.devcontainer/devcontainer.json` (`streamlit run`) |
| pandas | REACHED without a scanned import | `src/dashboard/app.py` (the same devcontainer dashboard) |
| plotly | REACHED without a scanned import | `src/dashboard/app.py` (the same devcontainer dashboard) |
| redis | REMOVABLE | Only `_archive/` and an unrelated comment in `agentic_core/api/method.py`; no `redis://` URL anywhere live |
| langchain | REMOVABLE | Named only in `_archive/` notes and the lock files |
| langchain-community | REMOVABLE | Named only in the dependency files |
| prefect | REMOVABLE | `_archive/` notes only |
| transformers | REMOVABLE | `_archive/` only |
| shap | REMOVABLE | Live hits are the word "shape"; real use only in `_archive/` |
| PyJWT | REMOVABLE as a DIRECT dependency | Auth uses `python-jose`; pyjwt may remain as another package's transitive dependency |
| seaborn | REMOVABLE | `_archive/` notes only |
| scikit-learn | REMOVABLE | `_archive/` only |
| pyro-ppl | REMOVABLE | Named only in the dependency files |
| ray | REMOVABLE | Live hits are the word "array"; real use only in `_archive/` |
| celery | REMOVABLE | `_archive/` only |
| web3 | REMOVABLE | `_archive/` only |
| z3-solver | REMOVABLE | `_archive/` notes only |
| sympy | REMOVABLE as a DIRECT dependency | `_archive/` only (it may remain as a transitive dependency) |
| qiskit | REMOVABLE | `_archive/` only |
| pennylane | REMOVABLE | `_archive/` only |
| oqs | REMOVABLE | `_archive/` only |
| firebase-admin | REMOVABLE | `_archive/` only |

**Still undecidable, and not counted:**

- POT is not installed in the measuring environment.
- autogen's `top_level.txt` is empty, so the instrument cannot read its module names.

Both need a check on a machine where they are installed.

**How the removal is done.** The REMOVABLE rows are removed from `pyproject.toml`. `poetry lock` regenerates the
lock, and `requirements.txt` is re-exported from it with the repository's tooling, never by hand. That happens in
its own commit, with the full suite and CI run against it. If the lock cannot be regenerated, nothing is removed
and the reason is recorded here.

## W628b reverted — the removal failed CI's fresh install (2026-10-07)

CI on 978a0af, a fresh install from the new `requirements.txt`, went red on two tests. That is the case this
separate commit existed to catch, so it was reverted alone. The verdict table above stands, with one
correction: **firebase-admin is NOT archive-only**.

1. `test_w575_p24_the_scatter_closes_on_each_row_it_reproduced` raised `ModuleNotFoundError: firebase_admin`.
   Live code reaches it by a path the import scan did not see: a dynamic import, or archived code that the
   test loads.
2. `test_w506_p27_the_platform_boots_with_torch_absent` failed inside scipy. The test sets
   `sys.modules['torch'] = None`, and scipy's array-API helper then reads `.Tensor` off `None`. With the old set
   installed, the boot never reached that scipy path. One of the removed packages was altering the import route,
   and which one is not yet established.

**Next attempt, for the local session.** Remove in two halves, and run the full suite on a FRESH venv built only
from the new `requirements.txt` before pushing. Hold firebase-admin back until whatever reaches it is found. Then
bisect the torch-absent boot failure across the remaining removals.

## W783 (FU-890) — firebase-admin has no live importer again (2026-11-10)

The live path W628b found to firebase-admin was the capital-fund package: four of its modules opened
`firebase_admin.firestore` at import. That package was archived in W673 (`_archive/products/capital_fund`), and a
whole-tree search outside `_archive/` now finds firebase-admin only in the dependency files, the docs and this
register's own test. The REMOVABLE verdict therefore holds without the W628b correction. **It was not removed
here**: removal rides FU-283's retry plan above (in halves, on a fresh venv built only from the new
`requirements.txt`, in its own commit), because the torch-absent boot failure W628b met is not yet bisected.

## W906 (FU-607) — the three dependency files come from one source (2026-11-13)

Measured line by line before this round, the three files had not come from one source since at least W555, the
last time the lock and `requirements.txt` were written:

- `poetry.lock`'s content hash did not match `pyproject.toml`. `anthropic` was declared and not locked, and `POT`
  was locked although W637 had removed it from the declarations.
- `requirements.txt` held three lines no export writes: `anthropic>=0.109.0`, `python-jose[cryptography]>=3.3.0`
  and `passlib[bcrypt]>=1.7.4`. Being unpinned, they installed whatever was newest. This machine's venv had
  anthropic 2.6.0, and an install made today resolves 2.8.0.
- Six pins were in no lock: fpdf2, openpyxl, pypdf, python-docx, python-pptx and torchsde.

No pin that was in both files disagreed.

What changed: the nine packages live code needs are declared in `pyproject.toml`, with python-multipart, which
W628b found was installed only because another package required it. fpdf2 and pypdf are held at the versions CI
installed (2.8.7 and 6.19.0); their newer releases are a change of their own. The lock was made by `poetry lock`,
which keeps every package already locked at its version, and `requirements.txt` was exported from it. Every
version CI installed before this round is the version it installs after it. anthropic, python-jose and passlib,
and the packages they and the document libraries bring, are now pinned at what an unpinned install resolved
today. The note that Stripe is deliberately left out moved into `pyproject.toml`, because an export carries no
comment.

**How to change a dependency from now on.** Edit `pyproject.toml`, then run:

```
poetry lock
poetry export -f requirements.txt --without-hashes -o requirements.txt
```

`poetry export` is a plugin (`poetry self add poetry-plugin-export`). `test_w906` fails when `pyproject.toml` is
changed without re-locking, when `requirements.txt` holds a line the export does not write, or when a pin differs
from the lock. FU-604's removal retry uses the same two commands, then a fresh venv built only from the new
`requirements.txt`.

## W907 (FU-604) — the nineteen REMOVABLE dependencies are removed (2026-11-13)

The Owner's ruling of 2026-10-07b allowed the REMOVABLE rows above to be removed. W628b did it once and was
reverted (above). This round carries out the retry plan:

- **firebase-admin.** What reached it was the capital-fund package, archived in W673. W783 found no live importer
  since, and this round's scan of `agentic_core`, `scripts` and `integration_tests` (outside `_archive/`) finds no
  import or availability probe of any of the nineteen.
- **A fresh venv.** It is built only from the new `requirements.txt`, plus pytest and pytest-xdist, which CI
  installs beside it. Each pinned distribution is hard-linked from an installed venv at its pinned version, so
  nothing else is present and nothing is downloaded (`pin_venv.py`, kept with the session's round tools). Both
  tests W628b failed pass in it: the firebase-admin import and the torch-absent boot. Then the full suite ran in
  it before this round's own suite.
- **Halves.** The plan said to remove the nineteen in two halves so that a failure would point at a half. A
  fresh-venv run of the whole suite now reproduces CI's install locally, so they were removed in one commit.

`pyproject.toml` no longer declares them. The lock was made again and `requirements.txt` exported from it: 306 pins
became 188. Three of the nineteen stay pinned because packages kept here require them: sympy (torch, onnxruntime),
scikit-learn and transformers. They are no longer declared, and nothing live imports them. `test_w907` fails if any
of the nineteen is declared again or imported by live code, or if one of them stays pinned with nothing that
requires it.

Not decided here, and not part of the ruling: the rows marked REACHED without a scanned import named
`src/dashboard/app.py`. W896 moved `src/` aside, so those three (streamlit, pandas, plotly) need a fresh verdict.

