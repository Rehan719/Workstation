# Autonomous technical support — review of the genome-integrated proposal

**Status:** review + plan, W482 (2026-09-20). A third outside proposal, interrogated against this repository with
`scripts/recovery_audit.py` and direct reads. Plan item: **P3.18**. Companion review:
`docs/COGNITIVE_ENGINE_ARCHITECTURE.md` (the engine fabric and the BME), whose §4 invariants and §11 naming rule
apply here unchanged.

The Owner's standing rule governs: **never a claim the system cannot back.** A support system is the sharpest test
of it, because "resolved" is a claim about a person's problem.

## 1. What it asks for

An `agentic_core/support/` package — an autonomous agent plus a genome tracker, a change-control hook, an
arms-length validator and a reconfigulator instantiation gate — reusing the SIL personaliser, VRPR, Mushāwara, the
UEG and a constitutional engine, deployed to Cloud Run at zero cost, resolving 96.7% of tickets with no human
escalation.

## 2. What it gets right

The instincts are this platform's own: reuse rather than duplicate; audit every change through change control;
validate cross-component calls at arms length; gate instantiation; log to the UEG; no new dependencies. Four of
those patterns genuinely exist here, under other names. And it is right that support should be a first-class
component rather than an afterthought.

## 3. What it gets wrong — evidence

**3.1 Twelve of its thirteen cited paths do not exist.** Checked, all missing:
`genetic_immune/genome/versioning.py`, `genetic_immune/genome/decoder.py`,
`genetic_immune/change_control/audit_trail.py`, `genetic_immune/change_control/amendment_validator.py`,
`governance/arms_length/agency_validator.py`, `governance/reconfigulator/instantiation_gate.py`,
`cognitive/personaliser/sil.py`, `cognitive/bridge/mushawara.py`, `ledger/ueg/ledger.py`,
`constitutional/constraint_engine.py`, `scripts/zero_placeholder_check_advanced_v2.sh`,
`scripts/deploy_zero_cost.sh`. Only `agentic_core/change_control/reconfigulator.py` is real. The genome package
exists but holds `chromosome · epigenetics · evolution · fitness · gene · population · regulatory_block` and
`genomic_registry.py` — there is no versioner and no change-control subpackage inside it.

**Where the real components live:** the personaliser is `agentic_core/personalisation/sil_personaliser.py`
(`calibrate_response(user_id, query, raw_response)` — not the keyword signature the proposal calls); Mushāwara is
`agentic_core/consultation/mushawara/` with `agentic_core/avatars/cognition/mushawara_bridge.py`; VRPR is
`agentic_core/quality/vrpr_pipeline.py`; the UEG is `agentic_core/gaas/v5/ueg.py` and `agentic_core/ueg/logger.py`;
the enforcement engine is `agentic_core/validation/omni_enforcement_pattern_supreme.py`.

**3.2 It would fork governance.** Change control in this platform is not a genetic_immune audit trail: it is
`agentic_core/api/change_control.py` (`submit_change(SubmitChangeRequest, principal)`), the Change Control Agency
the Owner's 2026-09-14 rulings shaped — Board ratification of review-approved HIGH changes, CCA decisions on the
UEG, `economy_material` CRITICAL, admin-only override. A second, parallel change-control path for support logic
would put changes outside the agency the Owner governs. Support amendments go through the existing CCA.

**3.3 The support component already exists — in the archive — and it is a simulation.**
`_archive/agentic_core/support/autonomous_support_agent.py` (75 lines) and `sla_monitor.py` (77 lines) are there,
with `_archive/tests-jules/integration/support/test_autonomous_support_sla.py`. What the agent does:
`await asyncio.sleep(0.1 if tier == "advanced" else 0.5)`, then returns
`"Simulated resolution for query: {query}"` with `confidence = 0.96` and `success=True`, unconditionally. The
archived test then asserts `result.resolution_rate >= 0.95` and `zero_human_intervention is True` — assertions that
cannot fail, because the agent never fails. **A 96.7% resolution target measured this way means nothing.** This is
the same class as the cascade that certified itself (W481) and the engines that return constants (W480).

**3.4 "Halo2 proof" is a hash with a name.** `require_halo2_proof=True` appears throughout the proposal. In this
repository Halo2 exists once: `avatar_engine.generate_halo2_proof` returns `f"halo2:v1:{proof_hash}"` — a SHA of the
payload, described in its own docstring as an "architectural interface". Attaching that to support events would
label a hash a zero-knowledge proof. Under §11 of the companion review, it is named for what it is or it is not
attached.

**3.5 The numbers and the deployment are not ours to state.** "96.7% autonomous resolution", "$0 owner cost", Cloud
Run deploys, Firestore indexes and a billing budget: this repository has a `Dockerfile` and no cloud integration,
and deployment is P4.5 — the Owner's switch. Tiered quotas (free/pro/enterprise, "unlimited") are pricing, which is
P4.6 and the Owner's decision; the economy here is virtual WST.

**3.6 Test location.** There is no `tests/` tree; the suite is `integration_tests/`, and a new guard belongs in
`integration_tests/test_mvp_spine.py` with the round's other guards.

## 4. The invariants a support component must satisfy

Beyond §4 and §11 of the companion review:
1. **"Resolved" is a claim about a person's problem.** It may be recorded only from evidence: the user marked it
   resolved, or a measurable outcome changed. A returned string is "answered", never "resolved".
2. **A resolution rate is measured over real tickets**, or it is not reported. No target may be asserted in a
   document, a config file or a test that a simulation can satisfy.
3. **No simulated latency.** A component never sleeps to imitate work.
4. **Escalation exists.** A system that cannot escalate must say so to the user; "zero human intervention" is a
   description of what the system CAN do, never a promise made to someone who needs help.
5. **One governance path.** Support logic changes go through `agentic_core/api/change_control.py`, the CCA.
6. **Provenance on every answer**, exactly as W479 established for the intelligence engines: what served it, and
   whether the structured floor wrote it.

## 5. The adjusted build order (P3.18, after P3.12–P3.16)

- **S1 — Recover and read.** Read the archived agent, SLA monitor and test. Keep the shape (ticket, resolution,
  tiers, SLA monitor); discard the simulation. Record in the plan that the archived test's assertions cannot fail,
  so nothing inherits them.
- **S2 — Answer honestly first.** A support answer is produced through the existing gateway with provenance
  (W479's `_staged_query` rule) and the SIL personaliser as it really is, and the page shows what served it. No
  confidence number is emitted unless something computes one.
- **S3 — Define resolution.** A ticket is answered; it becomes resolved only on the user's confirmation or a
  measured outcome. The store records both states, and the rate is computed from them.
- **S4 — Escalation and limits.** An unresolved ticket has a stated next step. Where no human is available, the
  system says that plainly.
- **S5 — Governance and audit.** Support logic changes go through the CCA; every ticket event is logged to the UEG
  with a real attestation (P3.15's work), never a `halo2:v1:` string presented as a proof.

Owner gates: no deployment (P4.5), no pricing or tier commitments (P4.6), no real money, no external AI by default.
