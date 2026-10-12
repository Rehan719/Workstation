# products/

**Nothing in this directory is served by the platform.** Read this before believing anything a file in here
declares about itself.

W506 (P2.4, rows FU-071 and FU-072) corrected the claims in this tree. What these directories are:

## The pointer directories (FU-071)

`business_incubator`, `cognitive_scraper`, `digital_reactor`, `gse`, `molecular_sdk`,
`nanophotonic_navigation`, `scraping_suite`, `uviap`

Each holds a `metadata.json`. `agentic_core/catalog/api.py` scans this folder at runtime and lists them with
status `source` - "a pointer, nothing served yet". They are KEPT because that reader exists and is honest about
what it found. No consumer builds from them.

## capital_fund - archived 2026-10-12 (W673)

`products/capital_fund/` is no longer here. On the Owner's ruling of 2026-10-12 it was moved, whole and
reversibly, to `_archive/products/capital_fund/` (the entry in `_archive/README.md` gives the reason and the
command that reverses it). It was listed above as a pointer directory; it never held a `metadata.json`, and
nothing live imported it. The fund the platform serves is a different module, `agentic_core/api/capital_fund.py`
(routes under `/api/v1/fund`, page `/capital`); the catalogue lists that card from its route.

## The signature directories (FU-072)

`Care/VSB-SIG-CARE-SEXTA-1.0`, `Education/...`, `Employment/...`, `Law/...`, `Religion/...`, `Science/...`

Legacy archives of the VSB-SIG frameworks. **Nothing reads their manifests.** Five of the six declared
`"status": "PRODUCTION_READY"` and nine `injection_formats` including MP4 and MP3 - output formats this
platform does not serve, and which its own canon records as a not-yet catalogue. Those declarations have been
corrected in place (`LEGACY_ARCHIVE_NOT_SERVED`, with the basis recorded in each file) rather than deleted,
because the frameworks themselves may be worth keeping and destroying material to silence a claim is the wrong
trade when correcting the claim costs nothing.

## OctoVeritasEngine

Holds a `constitution/` subtree. Out of scope for W506 and recorded as unresolved: it refused a read with a
permission error during the W505 constitution audit.
