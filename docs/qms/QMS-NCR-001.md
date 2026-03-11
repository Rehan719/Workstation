# QMS-NCR-001: Non-Conformance Management

## Purpose
To standardize the handling of quality failures within the evolution pipeline.

## Procedure
1. **Detection**: Triggered when a quality gate (e.g., Collation confidence < 0.8) fails.
2. **Reporting**: Automatic generation of an NCR node in the UEG.
3. **Disposition**: Responsible Team Lead determines if the artifact is scrapped, reworked, or accepted as-is (requires CEO override).
4. **Closure**: NCR is closed only after verification of rework or corrective action.

## Quality Gates
- NCR Closure Rate >= 90% within 7 days.
