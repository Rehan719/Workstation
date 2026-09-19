# Workstation mandates — an honest inventory (rewritten W473, 2026-09-19)

Until W473 this page was the "Mandates Final Inventory v1.0 (Global Launch)": a table that marked
mandates **VERIFIED** and **ENFORCED** against files that do not exist (`packages/shared/gaas.ts`,
deleted in W460 and never a validator; `agentic_core/crypto/pqc.py`; a 1127-article genome seeded in
`genome/constitution.work`; six domain ontologies under `agentic_core/data/ontologies/`;
`WINDOWS_SETUP_v0.9.md`) and against features that were later retired ("QEP engines integrated in all
6 domains" — the dead 'QEP Flagship' tab, removed in W470; QEP lives in the Religion domain). Register
rows FU-004 and FU-027 recorded the false rows. Nothing here was measured by the page that claimed it.

This page now lists each former claim with the status the repository can SHOW today. The evidence base
for every product claim is `docs/VISION_FIDELITY_LEDGER.md` (v4, W474, 60 findings, each refuted) and the
integration suite (`integration_tests/test_mvp_spine.py`); a claim not backed by one of those is marked
as a claim. The status words:

- **VERIFIED** — a named test in the suite fails when the claim is false.
- **PRESENT, UNVERIFIED** — the code exists at the named path; no test holds the claim.
- **NOT PRESENT** — the named file or directory does not exist.
- **RETIRED** — deliberately removed, with the round that removed it.
- **UNWIRED** — code exists but nothing calls it (kept by the Owner's ruling, W464).

## 1. Governance and compliance

| Former mandate | Status now | Evidence |
|---|---|---|
| Zero-placeholder codebase ("Article 60") | **VERIFIED for the shipped surfaces** | `test_w460_*` marker scan over the frontend; the fabrication ledger (`docs/FABRICATION_LEDGER.md`, closed 63/63). Not a claim about every module. |
| GaaS-validated mutations in `packages/shared/gaas.ts` | **RETIRED (W460)** | The file never validated anything and was deleted. Governance runs in `agentic_core/gaas/v5/` (the constitutional interceptor, `test_w464_*`, `test_w472_*`). |
| 10-minute veto window (validator.py) | **UNWIRED** | `agentic_core/layers/l1_identity/validator.py` holds the rule; no route calls it (Owner's ruling FU-020, W464). |
| PQC mandatory security (`agentic_core/crypto/pqc.py`) | **NOT PRESENT as cryptography; PRESENT as a simulation** | `agentic_core/crypto/` holds `entropy_pool.py` only; no Dilithium implementation exists. `agentic_core/security/pqc_hardening.py` names a `sign_dilithium5` that is a SHA3-512 digest over the message and a fixed built-in string — not a signature scheme — and `agentic_core/governance/gaas/gaas.py` and `agentic_core/reactor/religion/qep_flagship.py` stamp its output as `pqc_signature`. Register row FU-076 retires or relabels it. |
| 1127-article genome in `genome/constitution.work` | **NOT PRESENT** | The genome engine's seed holds 3 articles (`agentic_core/layers/l1_identity/genome_engine.py`); no `genome/constitution.work` is written. |
| Domain hub parity — six ontologies, 141+ nodes each | **NOT PRESENT** (an UNWIRED engine over nothing) | No `agentic_core/data/ontologies/` directory or ontology file exists in git; `agentic_core/reactor/domains/ontology_engine.py` would read that directory and answers empty graphs — until W473 it also CREATED the empty directory at import. Nothing reaches it: the domain weaver (`agentic_core/reactor/domains/weaver.py`) is called only through `ToolRegistry.call_tool('domain_weaver')` in `agentic_core/api/v138/ceo.py`, and the two live `call_tool` sites name other tools. The one ontology in the repository, the Law graph under `knowledge/Law/EmploymentTribunal/ontology/`, is not wired to it (register row FU-077). The six hubs mount their tools from one registry (`toolRegistry.ts`, W470; `test_w470_*`). |

## 2. Infrastructure and intelligence

| Former mandate | Status now | Evidence |
|---|---|---|
| AI CEO chat streaming (`/api/v138/ceo/chat`) | **PRESENT, UNVERIFIED as a mandate** | The route exists; the CEO chat on the owned fabric with provenance per answer is `test_w451_*` (W451). |
| Biometric login parity (`expo-local-authentication`) | **NOT PRESENT** | No mobile app in this repository. |
| Homeostatic self-healing | **VERIFIED as an organism system** | `agentic_core/organism/self_healing.py`; `test_fabric_organism_systems_run_real`. Not a PyTorch LSTM. |
| Semantic AI memory (ChromaDB + ToolRegistry) | **PRESENT, UNVERIFIED as a mandate** | The semantic store is `agentic_core/ai/ceo/memory_v01.py` (`MemoryV01`, ChromaDB when installed), called from `agentic_core/avatars/api.py` and `agentic_core/ingestion/api.py` (`agentic_core/api/v138/ceo.py` imports the name and uses only the meeting log); `agentic_core/ai/memory.py` is the JSON memory (hardened W241/W351). No test holds "semantic". |
| Swarm orchestration (C-Suite delegation) | **VERIFIED** | `agentic_core/api/swarm.py`; `test_delegate_standard_catalogue_landing_and_stage_models`, `test_swarm_delegate`, `test_swarm_cascade_in_house_provenance`. |
| Windows onboarding (`WINDOWS_SETUP_v0.9.md`, `setup.ps1`) | **PARTLY PRESENT** | `setup.ps1` exists; the setup document does not. Deployment notes: `docs/DEPLOYMENT.md`. |
| Introspection dashboard (`/introspect`) | **PRESENT at another path, UNVERIFIED** | No `/introspect` route exists; the page is `/cognitive-introspection` (`apps/workstation-superapp/src/pages/cognitive/Introspection.tsx`) and reads one route, `GET /api/v1/biometrics/status` (`agentic_core/app_mvp.py`: psutil, projects, immune and nervous readings). No test holds the claim. |
| Recursive self-improvement (`improvement_engine.py`) | **PRESENT, UNVERIFIED as a mandate** | `agentic_core/ai/improvement_engine.py` exists; the governed path is the Sovereign Evolution Office (`test_w464_*`, Change Control). |
| Scientific pipeline (manuscript drafting) | **PRESENT, UNVERIFIED as a mandate** | `agentic_core/synthesis/content_production.py`; no test holds "manuscript drafting & figure generation". |

## 3. Domains

| Former claim | Status now | Evidence |
|---|---|---|
| Religion — QEP flagship, 13 core features, cross-domain | **PRESENT in Religion only** | The QEP lives in the Religion hub (Owner's directive 2026-09-03, W439); the five other hubs' 'QEP Flagship' tab was dead and was removed in W470 (`test_w470_*`). "13 core features" is not measured anywhere. |
| Science — arXiv API integration and hypothesis generation | **PRESENT, UNVERIFIED** | `agentic_core/reactor/api_client.py` mentions arXiv; the Science hub's tools are the registry's three forms (`test_w470_*`). |
| Law — legal ontology and constitutional audit tools | **UNVERIFIED** | The Law hub's tools are the registry's analyser, drafter and IRAC research. A UK employment-law graph exists as data under `knowledge/Law/EmploymentTribunal/ontology/` and nothing serves it (FU-077). |
| Education — Canvas LMS foundation and personalised pathways | **NOT PRESENT** | No Canvas integration exists; the Education hub's tools are the registry's four forms. |
| Employment — skill matching and workforce analytics | **PRESENT as tools** | The Employment hub's seven registry entries (Application Studio + six forms). No analytics dashboard. |
| Care — DID-based patient sovereignty | **NOT PRESENT** | No DID implementation exists; the Care hub's tools are the registry's four forms. |
| Cross-domain QEP in all 6 domains | **RETIRED (W470)** | See Religion above. |

## 4. What holds a claim here

Every **VERIFIED** row names a test that fails when the claim is false; `test_w473_*` fails when a row of
this page or of `MANDATES_FINAL.md` marks VERIFIED or ENFORCED a path that does not exist. The former
inventory's own footer slogan is retired with it.
