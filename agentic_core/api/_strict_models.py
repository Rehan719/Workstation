"""Which request models REFUSE an undeclared field, and why (W628, FU-398).

Pydantic v2 ignores an undeclared field by default, so a caller can send one, receive 200 and have it
discarded. On most routes that is harmless. On a route whose request IS an instruction - a commitment, a
governance decision, a change to the organism, a directive to the Board or the Chief - a dropped field is a
LOST INSTRUCTION that reads exactly like a recorded one (FU-313 was the first measured case). Those models
forbid extras, so the caller gets a 422 naming the field instead of a 200 that quietly ignored it.

The rest of the ~206 models stay tolerant ON PURPOSE: forbidding everywhere would answer 422 to any caller
sending an extra field, the frontend included, for no gain in truth. A model joins this list only when an
undeclared field on it would mean an instruction silently not carried out.
"""
from pydantic import ConfigDict

STRICT = ConfigDict(extra="forbid")

#  module:Model -> why an undeclared field there is a lost instruction. A guard asserts every entry forbids.
STRICT_INSTRUCTION_MODELS = {
    "agentic_core.api.transformation_orchestration:OrchestrateRequest":
        "a transformation commitment (committed_rounds, confidence) - FU-313's original loss",
    "agentic_core.api.change_control:SubmitChangeRequest":
        "a governed change record: an undeclared field is a change the record never holds",
    "agentic_core.api.change_control:ConfigChangeSpec":
        "the organism lever a change will move: a misspelt key would apply nothing and report success",
    "agentic_core.api.change_control:ReviewDecision":
        "a review decision on a change, including an admin override",
    "agentic_core.api.change_control:ImmuneReconfigureRequest":
        "a defensive reconfiguration of the live organism",
    "agentic_core.api.board:RatificationDecision":
        "the Owner's ratification or refusal, recorded by the Board",
    "agentic_core.api.board:ChiefInstruction":
        "an instruction in the Owner's name that cascades to the CEO",
    "agentic_core.api.board:BoardDirective":
        "a topic put to the Board for deliberation",
}
