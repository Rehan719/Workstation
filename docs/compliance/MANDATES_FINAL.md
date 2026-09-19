# Workstation mandates — the v0.4 inventory, superseded (rewritten W473, 2026-09-19)

This page was the "Mandates Final Inventory (v0.4)", a second copy of the table now kept honestly in
`MANDATES.md`. It carried the same false rows (FU-004, FU-027): **ENFORCED** against
`packages/shared/gaas.ts` (deleted W460, never a validator) and `agentic_core/crypto/pqc.py` (does not
exist); **VERIFIED** against a 1127-article genome in `genome/constitution.work` and six ontologies under
`agentic_core/data/ontologies/` (neither exists).

`MANDATES.md` is the one inventory. The rows this page added beyond it, with the status the repository can
show today:

| Former claim | Status now | Evidence |
|---|---|---|
| Tool Creation Wizard (formerly cited under an apps/web tree that does not exist) | **NOT PRESENT** | No wizard exists. `apps/workstation-superapp/src/pages/developers/ForgePipeline.tsx` is the Forge pipeline, a different feature. |
| Inter-agent meetings (`agentic_core/api/v138/ceo.py`) | **PRESENT in memory only, UNVERIFIED** | The routes exist (`/meeting/log`, `/meeting/minutes`); the log they serve is `MeetingLog` in `agentic_core/ai/ceo/memory_v01.py` — an in-process list of at most 500 entries that is lost on restart. `MEETING_LOG_FILE` in `config/paths.py` is seeded empty by `scripts/init_data.py` and read by nothing. |
| Real arXiv integration (`agentic_core/reactor/science.py`) | **NOT PRESENT at that path** | No `science.py` module exists. The arXiv client is `agentic_core/reactor/api_client.py`; no test holds a live arXiv call (the suite runs on the native floor). |
| Adaptive learning (`agentic_core/reactor/education.py`) | **NOT PRESENT** | No `education.py` module exists; no test holds the claim. |
| LSTM resilience (`agentic_core/layers/l5_resilience/resilience.py`) | **NOT PRESENT at that path; UNWIRED elsewhere** | No such module exists. `agentic_core/biomimicry/geospheric/resilience.py` holds a hand-rolled "LSTM" over a JSON file and nothing imports it (FU-078). The organism's self-healing is `agentic_core/organism/self_healing.py` (`test_fabric_organism_systems_run_real`), and it is not an LSTM. |
| Mainnet WST token (planned v1.0) | **OWNER-GATED, NOT PLANNED HERE** | Money is virtual WST throughout; real-money rails stay gated on the Owner (`docs/VSB_ECONOMIC_LEGAL_MODEL.md`). |
| Bio-Compute CL1 (planned v1.0) | **NOT PLANNED** | No hardware integration exists or is scheduled in the delivery plan. |

The status words are those of `MANDATES.md`. `test_w473_*` fails when either page marks VERIFIED or
ENFORCED a path that does not exist.
