"""Seed the three record shapes P2.16's page must render, through the KERNEL'S OWN PATH.

    python scripts/_w557_probe_seed.py

WHY A SEED RATHER THAN THE ROUTE. Two of the three states need a COMPRESSED record, and no model is
provisioned on this machine — POST /api/v1/horizon/observe is served by the deterministic floor, which
composes rather than compresses, so every record it makes is NOT_COMPRESSED. That is the honest ordinary
state and it is one of the three; the other two would be unreachable on a live page for want of a model,
not for want of code.

WHAT THIS DOES NOT DO: it does not write records. It calls kernel.observe, kernel.build_record and
kernel.decide with the text a provisioned model WOULD have returned, so every field on every seeded row
is computed by the same functions the live route uses. Nothing here hand-writes a compression, a domain,
a decision or a term — if the kernel's parsing or its terms are wrong, these rows are wrong in exactly
the way the live ones would be, which is the only kind of seed worth having.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentic_core.horizon import consumption, kernel  # noqa: E402

#  What a provisioned model returns, in the format _COMPRESS_PROMPT asks for. The second one is the
#  state the bar names: a compression that ANSWERED the escalation question, and the answer was none.
CASES = [
    ("the ordinary path — nothing compressed it",
     "Please review this supplier contract before Friday", None, False, ""),
    ("compressed, and the compression raised NO escalation",
     "Please tidy the invoice numbering on the March statements", "w557-probe-model", False,
     "asked_for: a tidy-up of invoice numbering\n"
     "domain: operations\n"
     "stakes: a month's statements\n"
     "missing: none\n"
     "escalations: none\n"),
    ("compressed, and the compression DID raise escalations",
     "Draft the settlement figure for the tribunal bundle", "w557-probe-model", False,
     "asked_for: a settlement figure\n"
     "domain: legal\n"
     "stakes: a live tribunal matter\n"
     "missing: the schedule of loss; the respondent's position\n"
     "escalations: a legal matter; a figure a party may act on\n"),
]


def main() -> int:
    made = []
    for label, raw, served_by, is_external, text in CASES:
        obs = kernel.observe("probe", raw, "w557-probe")
        rec = kernel.build_record(obs, served_by, is_external, False, text)
        dec = kernel.decide(rec)
        row = kernel.save(rec, dec)
        #  W558 (P2.15) — a ConsumptionRecord joined to the run, so the companion surface has one to
        #  render. Nothing here measures: every figure is supplied as None and the record says what did
        #  not measure it, which is the state the page must show honestly.
        consumption.save(consumption.build(intent_id=row["intent_id"], wall_ms=None, provenance=None))
        made.append((label, row))
        print(f"SEEDED {row['intent_id']}  {row['compression']:<16} {dec['decision']:<14} {label}")
        print(f"       escalations={row.get('escalations', '<absent>')!r} "
              f"missing={row.get('missing', '<absent>')!r}")

    #  THE SEED ASSERTS ITS OWN PREMISE. A seed that silently produced three identical rows would make
    #  the probe pass over a page that renders one state three times.
    states = {r["compression"] for _l, r in made}
    assert states == {kernel.NOT_COMPRESSED, kernel.COMPRESSED}, ("the seed did not produce both "
                                                                  "compression states", states)
    esc = [r.get("escalations") for _l, r in made]
    assert esc[0] is None and esc[1] == [] and esc[2], (
        "the seed did not produce all three escalation states — absent, answered-none, and raised. "
        "Without the middle one the probe cannot assert the clause the bar names", esc)
    print(f"\nok: {len(made)} record(s), compression states {sorted(states)}, "
          f"escalation states absent/none/raised all present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
