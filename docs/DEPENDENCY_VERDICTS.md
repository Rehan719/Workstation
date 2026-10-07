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
