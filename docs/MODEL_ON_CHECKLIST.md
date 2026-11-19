# While a model is on — the one checklist

Plan item P5.10, clause 9 (the Owner's ruling of 2026-10-12, corrected in W677): while a model is on, one
checklist, and on it that attached or ingested text reaches a model marked as data and never as instruction. A local
model is installed on the Owner's machine and is the gateway's default, so this holds now, not later. Only the
suite and the audit backend turn the model off.

Each row below is a door by which text a person did not type as their request reaches a model, or a property that
door must keep. Each names the code that makes it true and the test that drives it. A row with no test is not on
this list: it is a gap, and it goes to the register.

## The doors

| Door | What holds | Where | Held by |
|---|---|---|---|
| A person's material in a domain tool, typed or attached | Handed to the model between two marks that say it is data; never joined into the instruction; its cut recorded and said | `agentic_core/api/_ai_provenance.py` (wrap_material, person_material, ai_text) | `test_helper_a_persons_material_is_data_and_every_answer_says_how_much_was_read`, `test_w680_a_persons_material_travels_as_marked_data_through_two_untouched_looking_doors` |
| The employment, career, science and care tools | All eighteen callers hand what the person wrote over as material | `agentic_core/api/career.py`, `agentic_core/api/employment.py`, `agentic_core/api/science.py`, `agentic_core/api/care.py` | `test_w856_the_career_tools_hand_a_persons_documents_over_as_material_and_say_when_they_were_not_read_whole`, `test_w857_the_employment_tools_hand_what_the_person_wrote_over_as_material`, `test_w858_the_science_tools_hand_what_the_researcher_wrote_over_as_material`, `test_w859_the_care_tools_hand_what_the_person_recorded_over_as_material_and_all_eighteen_callers_are_moved` |
| The education tools | A teacher's notes, objectives, task and rubric go as material or as a block of their own, never in the instruction | `agentic_core/api/education.py` | `test_w954_p512_what_a_teacher_types_is_handed_over_as_material_and_every_answer_carries_the_figure`, `test_w958_p512_marking_hands_its_task_and_rubric_over_as_a_block_of_their_own` |
| Files ingested into synthesis | Reach the model marked as data, and only the caller's own files reach it | `agentic_core/ingestion/api.py` | `test_w886_ingested_text_reaches_a_model_marked_as_data_and_only_the_callers_files_reach_it` |
| Prior interactions recalled into a conversation | Recalled lines reach the model between their own two marks, as data, with an imitated mark defused (W969) | `agentic_core/ai/gateway.py` (_augment) | `test_w969_p510_clause9_recalled_lines_reach_a_model_marked_as_data_and_the_checklist_holds` |

## The properties every door keeps

| Property | Where | Held by |
|---|---|---|
| A mark inside the material that imitates either delimiter is defused, and that is recorded | `agentic_core/api/_ai_provenance.py` (wrap_material) | `test_helper_a_persons_material_is_data_and_every_answer_says_how_much_was_read` |
| The floor reads no section heading from inside marked data | `agentic_core/ai/native/engine.py` (_sections) | `test_w969_p510_clause9_recalled_lines_reach_a_model_marked_as_data_and_the_checklist_holds` |
| Nothing a person types into a domain tool is stored before sign-in, so it cannot come back as recall | `agentic_core/ai/gateway.py` (keep_text) | `test_w952_fu1189_nothing_a_person_types_into_a_domain_tool_is_stored_before_sign_in` |
| An external call says what class of data it carries, and a legal matter never leaves | `agentic_core/ai/data_class.py` | `test_w899_fu610_an_external_call_declares_what_it_carries_and_a_barred_class_never_leaves` |
| How a served model handles an instruction planted in material is measured, not assumed | `agentic_core/api/native_ai.py` (the held-out set) | `test_w843_the_held_out_set_measures_injection_no_source_malformed_output_and_unsupported_claims` |

## What this list is not

It is not a certificate. A row says what the code does and which test drives it on this tree. Whether a given model
obeys an instruction planted in material is measured on the held-out set and said with its numbers, never assumed
from the marks.
