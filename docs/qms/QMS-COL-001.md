# QMS-COL-001: Collation Process Procedure

## Purpose
To systematically ingest and index all historical and new background artifacts.

## Responsibilities
- **Collation Team Lead**: Oversees the execution of the Workstation, QEP, and Tools collators.
- **Parser Agents**: Responsible for extracting versions and variations with confidence scores.

## Inputs
- `docs/historical/background/`
- System-generated telemetry

## Process Steps
1. **Detection**: Scan source directories for text and code files.
2. **Extraction**: Identify version markers and variation tags.
3. **Recording**: Store results in `meta/collation/` and link to the UEG version graph.
4. **Reporting**: Generate master collation reports for AI CEO review.

## Quality Gates
- **Accuracy Audit**: Average confidence score must be >= 0.8.
- **Coverage Check**: 100% of identifiably versioned files must be indexed.
