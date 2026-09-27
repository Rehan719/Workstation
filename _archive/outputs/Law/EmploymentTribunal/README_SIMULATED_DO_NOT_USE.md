# THE CONTENT IN THIS DIRECTORY IS SIMULATED. IT IS NOT AN ANALYSIS OF ANY REAL MATTER.

**Audited 2026-09-27 (round W496), at the Owner's instruction to search the archive for prior work.**

This directory and its siblings under `_archive/legacy-archive/law-grand-operation*` look like a
completed evidence review. They are not one. Every figure below was measured from the files themselves,
not inferred.

## What is actually in here

`audit/extracted_content_v9.0_gold_exec.json` holds **342 rows**. Every row carries
`"status": "EXTRACTED"` and `"granularity": "page_paragraph"`. The total volume of extracted text across
all 342 rows is **17,265 characters** — a median of **50 characters per document** — and every value has
the form:

```
"Simulated content for RM CV Science Oct 2025 (1).docx"
"Simulated content for Lonza Biotechnologist Interview prep (1).docx"
```

The producer says so itself. `_archive/scripts/Law/EmploymentTribunal/content_extraction.py`:

```python
    def _extract_file(self, item):
        path = item["path"]
        # Simulated extraction with granular citations
        # In real execution, pypdf / python-docx would be used
        item["extracted_text"] = f"Simulated content for {item['filename']}"
        item["granularity"] = "page_paragraph"
        item["sha256"] = hashlib.sha256(item["extracted_text"].encode()).hexdigest()
        item["status"] = "EXTRACTED"
```

Note the `sha256`: it is computed over the **placeholder string**, so the provenance hash on every row
attests the placeholder and not the document. `audit/source_inventory_v9.0_gold_exec.json` and
`unified_assimilated_graph.json` are built on these rows.

## Why this marker exists

`_archive/legacy-archive/law-grand-operation/v9.0-ULTIMATE-definitive/FINAL_SUBMISSION_REPORT_v9.0_ULTIMATE.md`
tells the reader, about a **real live employment-tribunal matter**:

> Granular Citations: All chronology entries, legal tests, evidentiary references include page/paragraph

> You are ready. The evidence is on your side. Proceed with confidence.

That verdict was computed over the 342 placeholder strings described above. It is the most consequential
instance in this repository of the defect class rounds W477–W496 removed from the live platform: a
confident conclusion over an input nothing read. **Nothing in this directory may be relied on, cited,
re-ingested, or presented to anyone as an assessment of the matter.**

## What may be recovered from here

The **shape**, and only the shape:

- the manifest row schema — `path`, `filename`, `type`, `status`, `timestamp`, `extracted_text`,
  `granularity`, `sha256` — which is a good schema once the hash is taken over the real bytes;
- `_archive/jules-phase2/src/organism/python/agents/evidence_ingestion.py` — an inbox + graph +
  per-file skeleton. It globs only `*.txt` ("Supporting .txt for initial demo") and imports a
  `src/organism/python/...` tree that does not exist in this repository, so it is a sketch, not code.

The real work is registered as **FU-277** (this audit) with **FU-269** (install a genuine pdf/docx
extractor) and **FU-272** (the explicit local inbox, human-gated, nothing leaving the machine). When a
real extraction runs, it will hash the document's own bytes and any claim it supports will cite a page
and a line that exist.
