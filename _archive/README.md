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

## Later moves: products/capital_fund (2026-10-12)

**What moved:** the whole Python package `products/capital_fund/` (41 tracked files, its tree kept) to
`_archive/products/capital_fund/`. One file of the same package, `immune/capital_immune.py`, was already here
(moved in W637).

**On whose ruling:** the Owner's, 2026-10-12 (W673): archived as a reversible move after a reachability check.

**Why:** nothing live imported it - not `agentic_core/`, not `scripts/`, not `agentic_core/app_mvp.py`; the only
importers were legs of the integration suite, which now read the archived text instead. It held a latent
live-payment path: `adapters/stripe_gateway.py` calls the provider's charge and payout operations and reads no
real-money switch. And two adapters returned fixed answers: `adapters/institutional_banking.py` a bank account
with status "VERIFIED", `adapters/mainnet_settlement.py` a settlement with status "SUCCESS".

**What it is not:** the fund the platform serves. That is `agentic_core/api/capital_fund.py` (routes under
`/api/v1/fund`), which never imported this package and was not touched. The catalogue lists that card from its
route (`SERVED_WITHOUT_DIRECTORY` in `agentic_core/catalog/api.py`), no longer from a directory of this name.

**To reverse it:** `git revert <the commit that added this entry>` restores the package, the catalogue line and
the test legs together. To move the files back by hand (leaving the W637 file where it is):

```
git ls-files _archive/products/capital_fund | grep -v '^_archive/products/capital_fund/immune/capital_immune.py$' | while read f; do mkdir -p "$(dirname "${f#_archive/}")"; git mv "$f" "${f#_archive/}"; done
```

then restore the driven test legs from the history of `integration_tests/test_mvp_spine.py` (they import the
package, which the text legs that replaced them do not), and do not expose the Stripe adapter to any route
before it consults `REAL_MONEY_ENABLED` the way `agentic_core/api/v310/payments.py` does.
