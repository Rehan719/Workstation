# QMS-GSE-001: Grand Synthesis Engine Operations Manual

## Purpose
To define the procedures for running the Grand Synthesis Engine (GSE) in various operational modes.

## Run Modes
1. **Ad-hoc**: Manual triggered runs for custom scope or urgent fixes.
2. **On-demand**: Event-driven incremental updates (e.g., file watcher trigger).
3. **Routine**: Weekly scheduled full synthesis for telemetry ingestion.
4. **Planned**: Major release cycle runs (e.g., v100.x to v101.0).

## Procedure
1. **Planning**: Define the scope, run-id, and target version.
2. **Execution**: Invoke the GSE via the `GrandSynthesisService`.
3. **Validation**: QualityAuditorAgent verifies output against previous baseline.
4. **Archival**: Store synthesis results in UEG and archive ingested artifacts.

## Quality Gates
- Synthesis Accuracy >= 99%
- Bi-directional Traceability confirmed.
