"""Horizon — the membrane that compresses a request before anything acts on it (P2.11).

THE RISK THIS PACKAGE EXISTS TO NOT REALISE, stated first because it is the whole point. The Owner's
brief carried a function called `compress_noise_to_meaning` which returned a hard-coded sentence about
what the user "really" meant. A compressor with no compressor behind it, writing the user's intent for
them, is the worst available outcome here: every later decision would rest on a sentence the platform
invented about a person.

So the kernel's compression is THREE-STATE and its common path is a refusal:

  COMPRESSED      a model served it, and the record names which.
  NOT_COMPRESSED  with the reason. THIS IS THE ORDINARY CASE, not an edge one — this deployment's
                  deterministic floor composes structured output from the request rather than inferring
                  anything, so a floor-served run is NOT a compression and says so.

AND NO FIELD IS FILLED BY INFERENCE. `asked_for`, `domain`, `stakes`, `missing` and `escalations` exist
only where a real compression produced them. On a NOT_COMPRESSED record they are ABSENT — not empty
strings, not empty lists, not "unknown" — because a default in any of those fields is a claim about a
request nobody read.

A DECISION FOLLOWS FROM STATED TERMS, never from a blended score: PROCEED | ESCALATE | NOT ASSESSABLE,
each term reported with its own basis. Three of the four terms the brief wanted to blend have no
instrument in this repository, and averaging an instrument that does not exist with one that does
produces a number whose provenance nobody can state.

THE REFLECTION TAG IS THE USER'S OWN WORDS (Owner ruling, recorded as FU-267 and written into the spec in
W549). It is optional, the user selects and clears it, and NO AI EVER WRITES IT — no default, no
suggestion persisted as a value, nothing inferred from the observation's text. It is the one field on the
record that is not the platform's account of the user.
"""
