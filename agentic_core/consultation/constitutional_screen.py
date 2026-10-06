"""The constitutional screen every cognitive engine delegates to — P3.28 clause (1).

Measured W598-W603: every engine wrote `ValidationResult(passed=None, "no constitutional check ran")` as a LITERAL,
so the deliberation above them could only ever be NOT ASSESSED and clearance gate 1 could only ever block. gaas.v5
already performs real checks; this module runs them for an engine, over BOTH the request and the engine's answer:

  * the three Horizon guardrails (gaas/v5/horizon_guardrails.screen_all) over the query and over the answer;
  * the policy gate's OUTPUT screen (gaas/v5/policy_gate.ConstitutionalPolicyGate.validate_output) over the answer.

THE TRAP THIS MODULE EXISTS TO AVOID: returning `passed=True`. A screen may REFUSE, never CLEAR — each guardrail
screens English phrase patterns and the output screen matches unsafe payload shapes, so a non-match means their own
patterns found nothing, not that the subject was checked and found sound. So:

  * a refusal   -> passed=False, refused=True,  violations=[what refused, by which screen]
  * no refusal  -> passed=None,  refused=False, screened_by=[the screens that ran], coverage_limit=<their limits>

`passed` stays None on a non-refusal. The decision a caller makes from it is BY COVERAGE: "screened by X, nothing
refused, within this stated limit" — which is a different fact from "approved", and the field names keep it so.

NO LEDGER WRITE PER CALL, deliberately: uci_v16_omega.intercept checkpoints every call to the UEG, and an engine is
consulted several times per beat. The checks are the same functions intercept calls; only the checkpoint is not.
"""
from __future__ import annotations

from typing import Any, List

from agentic_core.consultation.interface import ValidationResult

SCREENED_BY = ("gaas.v5 horizon guardrails (request)", "gaas.v5 horizon guardrails (output)",
               "gaas.v5 policy gate (output)")

COVERAGE_LIMIT = (
    "three English phrase screens (a religious ruling, a theological proof, clinical counsel to someone in "
    "distress) over the request and the answer, and an unsafe-payload screen over the answer (destructive "
    "commands and private keys). None certifies an absence: a non-match means these patterns found nothing, "
    "never that the content was understood and found constitutional")


def screen(engine: str, query: Any, answer: Any) -> ValidationResult:
    """Run gaas.v5's checks for one engine's consultation and report a refusal or the coverage, never a pass."""
    from agentic_core.gaas.v5 import horizon_guardrails as _g
    from agentic_core.gaas.v5.policy_gate import ConstitutionalPolicyGate

    violations: List[str] = []
    try:
        g_in = _g.screen_all(str(query or ""))
        g_out = _g.screen_all(str(answer or ""))
        post = ConstitutionalPolicyGate(domain=f"engine:{engine}").validate_output(str(answer or ""))
    except Exception as exc:  # noqa: BLE001 - a screen that could not run is NOT ASSESSED, never a pass
        return ValidationResult(
            passed=None, refused=None, screened_by=[], coverage_limit=None,
            basis=(f"the constitutional screen could not run for {engine} ({exc.__class__.__name__}: "
                   f"{str(exc)[:120]}), so this consultation is NOT ASSESSED - neither a pass nor a failure"))
    if g_in["escalate"]:
        violations += [f"request escalated by {g}" for g in g_in["escalated_by"]]
    if g_out["escalate"]:
        violations += [f"answer escalated by {g}" for g in g_out["escalated_by"]]
    if not post["compliant"]:
        violations += list(post.get("violations") or [])
    if violations:
        return ValidationResult(
            passed=False, refused=True, violations=violations, screened_by=list(SCREENED_BY),
            coverage_limit=COVERAGE_LIMIT,
            basis=f"REFUSED by gaas.v5 for {engine}: " + "; ".join(violations))
    return ValidationResult(
        passed=None, refused=False, violations=[], screened_by=list(SCREENED_BY), coverage_limit=COVERAGE_LIMIT,
        basis=(f"screened by gaas.v5 for {engine} and nothing refused. This is NOT a pass: {COVERAGE_LIMIT}"))
