"""Autonomous technical support — the SHAPE recovered, the simulation discarded (P3.18).

WHAT WAS ARCHIVED, and why none of it is imported here. `_archive/agentic_core/support/` holds a support agent
that SLEEPS a tier-shaped latency (0.1s for "advanced", 0.5s otherwise), returns a formatted
string announcing a simulated resolution of whatever was asked (the exact wording is in W541's commit
message, not here, because this file's own guard forbids it) with a confidence of 0.96, and sets
success=True unconditionally —
under an archived test asserting a resolution rate of 0.95 that therefore cannot fail. A third archived file,
`sla_monitor.py`, is the more instructive one: it does NOT hardcode a rate. It INVENTS its tickets, feeds them
to the agent whose success field is an unconditional literal, and then computes
`sum(1 for r in resolutions if r.success) / len(resolutions)` — a real division over a fabricated numerator,
which is the shape that survives an audit asking only whether a number is a literal. It computes 100%.

So this package inherits the SHAPE and nothing else:
  * ANSWERED AND RESOLVED ARE DIFFERENT STATES. The archive had one boolean for both. Here a ticket can be
    answered and never resolved, and nothing marks itself resolved.
  * RESOLVED IS WRITTEN ONLY FROM A CONFIRMATION. Either the user says so, or a measured outcome says so.
    `confirmed` is three-state: True, False, or None for "nobody has said". None never counts as either.
  * THE RATE IS COMPUTED FROM THOSE RECORDS AND ONLY THOSE. Unconfirmed tickets are excluded from the
    denominator rather than counted as successes, and with no confirmations at all the rate is None with a
    basis — not 0.0, and certainly not 1.0.
  * NOTHING SLEEPS. The latency reported is the measured duration of the call that produced the answer.
  * AN UNRESOLVED TICKET CARRIES ITS NEXT STEP, so "not resolved" is never the end of the record.
  * SUPPORT LOGIC CHANGES GO THROUGH THE EXISTING CHANGE CONTROL AGENCY. There is no second governance path
    in this package, and no gate of its own invention.
"""
