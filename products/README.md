# products/

**Nothing in this directory is served by the platform.** Read this before believing anything a file in here
declares about itself.

W506 (P2.4, rows FU-071 and FU-072) corrected the claims in this tree. What these directories are:

## The pointer directories (FU-071)

`business_incubator`, `cognitive_scraper`, `digital_reactor`, `gse`, `molecular_sdk`,
`nanophotonic_navigation`, `scraping_suite`, `uviap`, `capital_fund`

Each holds a `metadata.json`. `agentic_core/catalog/api.py` scans this folder at runtime and lists them with
status `source` - "a pointer, nothing served yet". They are KEPT because that reader exists and is honest about
what it found. No consumer builds from them.

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
