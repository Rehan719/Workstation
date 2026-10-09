# The OGE / HAIRMS brief ("v15.1‑Ω∞ / OGE‑v1.2‑GOLD") — interrogated against the tree

**Supplied by the Owner 2026‑10‑09, with the instruction to interrogate it, verify, and take into the plan only
what survives.** This is the fourth LLM‑authored architecture brief handled this way (after the Native AI Fabric
roadmap, the Horizon brief and the Vision 8.0 biomimetic brief). The rule is the same each time: every "what
exists" claim is measured against the working tree by a named command, and what survives becomes **rows and
items inside the existing plan** — never a new phase, a new source tree, or a new branch.

Measured at `fc81a933` plus W636's uncommitted repair, on the Owner's machine. No agent fan‑out was used: every
figure below is one `git ls-files` / `git grep` away and is reproducible. That bounds what this can claim — it
is a verification of the brief's statements about the repository, not a design review of every idea in it.

**The brief says of itself that it is "not a live code audit claim".** That is accurate, and it is the most
important sentence in it: it was written from the conversation and earlier documents, not from the code.

---

## 1. What the brief says exists, and what the tree holds

| Brief's claim | Measured | Verdict |
|---|---|---|
| A convergence across `agents/`, `realms/`, `deployment/`, `tests/` | none of the four directories exists (`git ls-files <dir>` → 0). Tests live in `integration_tests/`; the UI in `apps/` | FALSE_ABOUT_REPO |
| 29 `agentic_core/` packages to build on or into | 23 hold **no Python at all** (oge, hairms, facilities, ai_fabric, genetics, immune, meta_cognition, hyperdimensional, core_tech, constitutional, vbs_entity, identity, hardware, expression, regulation, resilience, propagation, modules, recombination, federation, planning, memory). 6 exist: governance 24 files, evolution 14, horizon 7, orchestration 6, ueg 4, business 3 | 6 EXIST · 23 ABSENT |
| "GaaS v4", "Nemoclaw runtime", `sovereignctl` | the tree runs `agentic_core/gaas/v5`. **No Nemoclaw runtime exists anywhere** (`git grep -- .`, whole tree): the name appears in `config/constraints/absolute_constraints.yaml` as the *enforcer* of two constraints, and in the top‑level `core/identity.py`, which imports `core.nemoclaw_runtime` — a file that is not in the tree, so that module cannot import. The suite already forbids the name on any page as a "fictional model name" (`test_mvp_spine.py:10828`). `sovereignctl` appears once, in a comment | FALSE_ABOUT_REPO |
| HAIRMS / OGE as named systems | zero occurrences in code, the vision, the plan or the living plan | ABSENT (and absent from the canon) |
| Reconfigulator, Regulator | both exist in `agentic_core/change_control/`. The Regulator is named in 13 live files (`git grep -w -i regulator`), among them the Board, Horizon and organism‑status APIs. The Reconfigulator already contains an **AST stub detector** (a body that is only `pass` or only raises `NotImplementedError`) | EXISTS_AND_RUNS |
| Unified Constitutional Interceptor | exists and is wired at eight call sites (genesis, board, economy, forge, swarm, transformation, the GaaS API) as `UnifiedConstitutionalInterceptorV16Omega` | EXISTS_AND_RUNS |
| MultiSigCouncil | `governance/multisig_council.py`, 69 lines. Imported by **one** module, `products/capital_fund/immune/capital_immune.py`, which itself nothing imports (already recorded in `docs/FABRICATION_LEDGER.md`, W415). Unreachable | EXISTS_DORMANT |
| Arms‑length change control | present in 29 live files; the Board ratifies HIGH changes (Owner ruling 2026‑09‑14) | EXISTS_AND_RUNS |
| Six cognitive engines (Inkashaf … Iman), MJM | present (18 and 24 files). The engine inventory is 23 by Owner ruling 2026‑09‑30, and P3.28's clearance chain runs them | EXISTS_AND_RUNS |
| Digital facilities (Reactors, Petri dishes, Incubators, Labs, Factories …) | this is the vision's own §7 ("musculoskeletal facilities"), realised in the Resource Fabric. A resource can be composed and **retired**; there is no provision → operate → decommission lifecycle, no TTL, no retention field | DUPLICATES_EXISTING (the family) · ABSENT (the lifecycle) |
| External AI as "governed symbionts" | the canon already says "optional accelerants, never dependencies"; `AI_ALLOW_EXTERNAL` gates it in 11 files and every output carries `is_external`. It is plan item P4.3, an **Owner switch** | DUPLICATES_EXISTING |
| Hardware honest refusal | exists: `tiers.image_intake` refuses with the declared requirement and the measured machine (P3.5) | EXISTS_AND_RUNS |
| Human review of high‑risk output | exists in 10 files; gates 2 and 3 of the clearance chain read records a person made (FU‑471) | EXISTS_AND_RUNS |
| AlphaFold 3, OpenClaw, Cosmos 3, OAM‑QKD, Mammouth, Ginkgo "integration" | **one file of name strings** — see §3, where verifying this claim found a defect | EXISTS AS A NAME LIST ONLY |
| HR for employees, contractors, volunteers, partners, crowd contributors | `volunteer`, `payroll`, `right to work`, `contractor`/`IR35`: **zero** live files. The vision's only mention of volunteers is two lines of QEP mission prose | ABSENT (and outside the canon) |
| Data classification on what crosses the membrane | zero live files | ABSENT |
| Holographic AR/VR, clonal selection, Clownfish protocol | zero live files | ABSENT |

**Tally of the 17 rows:** 6 exist and run · 2 duplicate the canon · 1 dormant · 1 a name list · 2 false about
the repository · 4 absent · 1 mixed (the package list: 6 exist, 23 do not). The proportion matches the earlier briefs: most of what it asks for is either
already built under another name or was never in the Owner's canon.

---

## 2. What is refused, and on what ground

Each of these is refused because it collides with something the Owner has ruled or the repo has measured — not
because it is unambitious.

1. **The execution instruction itself** (create branch `v15.1-omega-oge-hairms-production`, "begin Phase 0
   now", module skeletons for fifteen packages). A skeleton with "concrete interfaces" and no behaviour is
   exactly the placeholder the brief forbids two paragraphs earlier; and the tree's measured history is that
   built‑but‑unreachable modules are not work (8 of 11 `biomimicry/` subpackages hold no files). Work lands on
   the plan's branch, inside `agentic_core/`'s existing packages.
2. **Every numeric target with no instrument behind it.** "Replication fidelity ≥ 99.9%", "≥ 1e6 unique immune
   detectors", "threat elimination < 100 ms", "viral coefficient > 1.2", "biomimetic fidelity ≥ threshold",
   "meiosis diversity gain ≥ 30%". Nothing in the tree measures any of these, and the brief names no way to. A
   target nothing computes becomes a number somebody types — the defect class this repo has spent thirty rounds
   removing (a basis string is code; a figure typed into an instrument is right once and then lies).
3. **"Legal precision = 100% statutory and precedent coverage."** There is no corpus to cover: the archived law
   corpus was measured as simulated (342 rows stamped EXTRACTED). What the platform can honestly promise in a
   regulated domain is what it already does — the floor withholds research sections, sourced text is quoted
   from its source, and a named person approves the artefact. A "coverage" figure would be fabricated.
4. **Anything that grades a person.** `PerformanceReview`, `WellbeingSignal`, "contributor reputation",
   "quality score" per contributor, "human overload index". Ruling A.9.5: grade the request, never the human.
5. **Payroll, tax codes, pension, right‑to‑work evidence, statutory payments.** Real money and real
   employment‑law records. Money here is virtual WST; `REAL_MONEY_ENABLED` and `AUTH_ENABLED` are the Owner's
   switches and are off. A registry of real people's employment data on a single‑user, auth‑off deployment
   would be a liability, not a feature.
6. **A content‑bearing "stigmergic blackboard"** and **probability‑ranked resource matching.** Both were
   refused in the Vision 8.0 assessment (a non‑content mark may be admissible; "ranked by nothing, ever").
7. **The brief's zero‑placeholder gate** (`grep "TODO\|pass\|NotImplementedError\|mock\|placeholder"`). Run on
   live `agentic_core` it reports **1,173 lines**, 267 of them the legitimate statement `pass`; real
   `NotImplementedError` raises: **zero**. The tree already has the better instrument (the Reconfigulator's AST
   stub detector) and 617 tests that drive behaviour.
8. **A 30‑week dated roadmap, daily 18:00 UTC reports, "888_HOLD".** The plan projects in rounds measured from
   the register, never a date (W486), and reports at round boundaries.
9. **"Jules, AI CEO" and Board/MultiSigCouncil "certification recorded in UEG" as the definition of done.** Done
   here is a bar on an item, closed by a guard that was driven red.
10. **The biological citations as authority**, and "not mystical claims; functional equivalence to biological
    reference systems" — no reference system or equivalence test is named.

---

## 3. What verifying the brief FOUND (defects in the tree, not in the brief)

Checking the "core technology" claim turned up live code that fabricates a result:

- **`agentic_core/products/signature_suite/core.py`** — `SignatureProductSuite.execute_capability()` takes a
  technology id (`alphafold_3`, `cosmos_3`, `oam_qkd_surrogate`, `mammouth`, `ginkgo`, `openclaw`) and returns
  `{"fidelity": 0.995, "compliance": 1.0, "status": "TRANSFORMATIVE_SUCCESS"}` — constants — then writes a
  "signature_tech_convergence" event to the UEG. Nothing is executed. It is instantiated by
  `governance/uci_interceptor.py:51` and called at `:112` when a context carries `requires_signature_tech`.
  **No caller sets that flag** (`git grep requires_signature_tech` → the one read site), so it is unreached
  today; but it is a fabricated success one keyword away from a surface, and it would write a false event to
  the audit log. It has no register row.
- **`agentic_core/governance/multisig_council.py`** — unreachable: its only importer is
  `products/capital_fund/immune/capital_immune.py`, a module nothing imports. *(Correction, same evening: the
  first version of this document said "imported by nothing". That came from a search limited to
  `agentic_core/` — the exact blind spot this repository recorded at W159, when a dead‑code scan missed
  importers in `products/`. The reachability check before archiving caught it. The conclusion stands; the
  sentence was wrong.)* Either it is wired to the one place the canon gives it (constitutional rule changes)
  or it is archived **together with that dead importer**; today it reads as a control that exists.

- **`core/identity.py`** (the top‑level `core/`, four tracked files) imports `core.nemoclaw_runtime`, which
  does not exist. The module cannot be imported at all. This is the lead already registered as FU‑605, now
  with its cause; and two declared constraints name "Nemoclaw" as their enforcer, as five name the council.

All three are the kind of finding the fidelity audit cannot make, because no assessor reaches them.

**A note on method.** Three claims in the first version of this document came from searches limited to
`agentic_core/` and the superapp. Re‑run across the whole tree before anything was archived, two needed
correcting (the council's importer; where "Nemoclaw" appears) and one held (the fabricated executor has no
caller anywhere). Every "nothing references it" above is now a whole‑tree result.

---

## 4. What survives — taken into the plan

Five things are sound, are not already built, and do not collide with a ruling. Each becomes a register row on
an existing item; none needs a new phase.

| # | What | Why it survives | Where it goes |
|---|---|---|---|
| A | Remove or make honest the fabricated core‑technology executor (§3) | a truth defect in live code; unreached, so Tier‑3 by the ledger's rule, but it writes to the audit log | the M3 item (P3.30) |
| B | Decide `multisig_council.py`: wire it or archive it | a control that is not reached reads as a control that exists | the M3 item (P3.30); the wiring choice is the Owner's |
| C | A **facility lifecycle**: a fabric resource has a state (requested → provisioned → operating → retired), and an ephemeral one has an expiry it honours | the vision's §7 names the facilities; only "retire" exists. The brief's lifecycle and TTL are the one part of its facilities plane the tree lacks | a row on P5.1, to be **measured first** (which resources hold state at all) |
| D | A **data class on what leaves the platform**: when an external accelerant is allowed, each call states what class of data it carries, and a class can be barred | zero live files; it is the missing half of "no silent dependency" — today a call says THAT it was external, not WHAT went | a pre‑flight row on P4.3 (Owner switch; we build the pre‑flight) |
| E | **Verification and validation kept as two gates with different evidence** ("built it right" / "built the right thing") | the plan's bars already do this informally; the brief states it cleanly and the M3 item's ACCEPT (2) is an instance of it | recorded here as method; no row |

**Not taken, though sound in the abstract:** the requirement → specification → resource plan → organism flow.
That is what Genesis (`/establish`, the Concept‑to‑Commercialisation journey) already is; a second pipeline
beside it would be the parallel tree refused in §2.1.

---

## 5. Decisions that are the Owner's

1. **Is a registry of real people in scope at all?** The brief's largest new idea is HAIRMS's human half:
   volunteers, partners, reviewers, engagements, consent. Nothing in the canon asks for it. *Recommendation:
   not now.* If it is wanted later, the admissible core is narrow — a record that a **named person holds a
   role on an engagement** and has given a stated consent — with no grading, no payroll, and not before
   `AUTH_ENABLED` is on. That would be a new item for the Owner to charter, not a row.
2. **`multisig_council.py`: wire or archive?** *Recommendation: archive*, unless the Owner wants constitutional
   rule changes to need more than the Board's ratification they ruled on 2026‑09‑14.
3. **Does the vision adopt any of the brief's vocabulary** (OGE, HAIRMS, "Facilities Plane")? *Recommendation:
   no.* "Constitution", "Regulator" and "mechanical" already carry measured meanings here; a second naming layer
   over working code has cost rounds before.

---

## 6. Reconsidered the same evening, against the revised brief and commit `4cd66b2d`

The Owner supplied a revised text of the brief and asked for it to be reconsidered alongside commit `4cd66b2d`
on `main` ("docs: detail workstation resource management architecture", a Jules bot commit merged by PR #356).

**The commit changed nothing.** Its tree is identical to its parent's (`git diff --stat 4cd66b2d^ 4cd66b2d` is
empty; PR #356 reports 0 files, +0 −0), and that parent is W601 — thirty‑five rounds behind the branch. The
"comprehensive technical breakdown" it describes exists only in the Jules task and the PR description.

**What its description names does exist** (whole‑tree search): the resource optimiser
(`agentic_core/optimization/aro.py`), the Resource Fabric API (`agentic_core/api/resource_fabric.py`, 16
routes), the Model Resource Registry (`agentic_core/ai/native/model_resource.py`, nine importers), a cost
guard, and homeostasis. It did not name two more: the tier router that refuses a model this machine cannot run
(`agentic_core/ai/native/tiers.py`) and the optimizer package — monitor, predictor, allocator, scheduler,
fabric, RAL verifier — wired at `agentic_core/api/optimizer.py`.

**What this changes in sections 1–4:**

- The brief's AI‑resource and facilities halves duplicate MORE than section 1 said. A registry, a router, an
  optimiser and a fabric already exist; `ai_fabric/` and `facilities/` would be a parallel tree (§2.1).
- **Under‑weighted the first time:** these subsystems are scattered and no surface shows them together. The
  valid kernel of "HAIRMS" is one place that says what resources exist and what state each is in. Taken into
  the plan as a row: a READ‑ONLY resource inventory — one route, one page — composed from the registries that
  exist, with no new registry and no new tree. Measure first what each registry can honestly report.
- **A defect found by reading the optimiser:** `AutonomousResourceOptimisation.optimize()` returns an
  "allocation" of four weights that nothing reads (`git grep current_allocation` finds only its own file). Its
  objective is linear in the weights, so the optimum always puts everything on the largest demand; two of its
  four demands are constants typed in the file under the comment "Simulated demand". It is exposed as the CEO
  tool `optimize_qep_resources`. An allocator that allocates nothing — registered as a row.

**What the revised brief adds, and why none of it reopens a ruling:** a "human‑centric needs framework"
(emotional monitoring, satisfaction scoring, social‑graph analytics) that monitors and grades a person — ruling
A.9.5; twenty‑five numbered "constitutional articles" — constitutional text is the Owner's to write; Raspberry
Pi 5 targets nothing here can measure. The architecture, the module tree, the KPIs and the instruction to
"Jules" are unchanged. The Owner confirmed the recommendation on 2026‑10‑09.

*Method note: when a commit is named as evidence, compare its tree with its parent's before reading its
message. A commit message is not evidence that anything changed.*
