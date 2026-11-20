# The first offer's public drafts: landing copy, a capability sheet, a deck outline, a demonstration script, questions and answers, and outreach templates

**DRAFT - NOT APPROVED FOR PUBLICATION.** **DRAFT until the Owner ratifies it.** Written for plan item P5.7, clause 4
(row FU-809). Every piece below is built from the leading hypothesis of `docs/business/FIRST_OFFER_CANDIDATES.md`,
candidate C: lesson plans and feedback that a teacher or tutor checks before use. That hypothesis is what the
interviews are meant to test, and which candidate is offered first is the Owner's call, made after them; if another is
chosen, these drafts are rewritten from it. Nothing here is published or sent. Every claim names what shows it: a test
in `integration_tests/test_mvp_spine.py` that runs on the platform's own engine, with no outside model.

## How to read this document

- Every statement carries a label: [observed: test] is shown by the named test; [hypothesis] is what the interviews are meant to test; [owner decision] is the Owner's to make. [observed]
- No price, customer, school, partner or endorsement is named in any draft, because none exists. [observed: `docs/business/FIRST_OFFER_CANDIDATES.md`]
- Each piece is headed DRAFT - NOT APPROVED FOR PUBLICATION, so that none can be lifted out and published on its own. [observed]

## 1. Landing copy — DRAFT - NOT APPROVED FOR PUBLICATION

- Headline: lesson plans and feedback drafted for you to check, so that the teaching stays yours. [hypothesis]
- It drafts a lesson plan for the subject, topic and level you give it, on the platform's own engine, and says what composed it; nothing is sent to an outside model. [observed: test_domains_in_house_provenance]
- It drafts feedback on a piece of work against the task you set, and says when its next steps are general rather than drawn from the work. [observed: test_w823_education_feedback_on_the_floor_says_its_next_steps_are_not_drawn_from_the_work]
- It plans against frameworks it names, so you can see which one a plan follows. [observed: test_education_frameworks]
- What you type is not kept before you sign in. [observed: test_w952_fu1189_nothing_a_person_types_into_a_domain_tool_is_stored_before_sign_in]
- It is for teachers and tutors, not for the children they teach. [observed: test_w712_each_unchecked_constraint_says_what_it_is_to_a_reply_and_children_do_not_use_the_tools]

## 2. Capability sheet — DRAFT - NOT APPROVED FOR PUBLICATION

- What it does: drafts a lesson plan (`POST /api/v1/education/lesson-plan`) and feedback on a piece of work (`POST /api/v1/education/feedback`), against a named framework (`GET /api/v1/education/frameworks`). [observed: test_domains_in_house_provenance]
- What it needs: for a plan, a subject, a topic and a level; for feedback, the work, the task, the level and the subject. [observed: test_education_feedback_contract]
- What it says about itself: every answer carries what served it, and on the platform's own engine it says so. [observed: test_domains_in_house_provenance]
- What it does not do: it does not give a final mark, since the marking sections are withheld when no model is on, and it does not present general next steps as drawn from the work. [observed: test_w823_education_feedback_on_the_floor_says_its_next_steps_are_not_drawn_from_the_work]
- What it refuses: a teaching request on a religious subject, which every teaching route refuses. [observed: test_w659_every_teaching_route_refuses_a_religious_subject]
- What is not known: whether teachers find a draft good enough to start from, whether anyone would pay, and who would buy it. NOT MEASURED. [observed: `docs/business/FIRST_OFFER_CANDIDATES.md`]

## 3. Deck outline — DRAFT - NOT APPROVED FOR PUBLICATION

1. The problem as a teacher would put it: planning and feedback take time the teaching needs. [hypothesis]
2. What the tool drafts, and that the teacher checks every line before using it. [observed: test_domains_in_house_provenance]
3. What it will not do: give a final mark on the floor, speak to children, or keep what is typed before sign-in. [observed: test_w823_education_feedback_on_the_floor_says_its_next_steps_are_not_drawn_from_the_work]
4. How it was tested: the tests this document names, which run on the platform's own engine. [observed: test_w1151_fu809_each_public_draft_is_headed_and_every_claim_names_a_test_that_runs_without_an_outside_model]
5. What is not yet known: demand, the price and the buyer, each NOT MEASURED. [observed: `docs/business/FIRST_OFFER_CANDIDATES.md`]
6. The ask: thirty minutes of a teacher's time, trying it on invented material. [owner decision]

## 4. Demonstration script on invented data — DRAFT - NOT APPROVED FOR PUBLICATION

- Only invented material is used: an invented class, an invented topic and an invented piece of work; no pupil's real work is ever used in a demonstration. [owner decision]
- Step 1: ask for a plan on fractions for Key Stage 3, the request the suite itself sends, and show the plan and the line saying what composed it. [observed: test_domains_in_house_provenance]
- Step 2: paste an invented short answer on the water cycle with its task, for Key Stage 3 geography, and show the feedback and its closing note that the next steps are general. [observed: test_w823_education_feedback_on_the_floor_says_its_next_steps_are_not_drawn_from_the_work]
- Step 3: show the frameworks it plans against, by name. [observed: test_education_frameworks]
- Step 4: show, signed out, that nothing typed was kept. [observed: test_w952_fu1189_nothing_a_person_types_into_a_domain_tool_is_stored_before_sign_in]
- Step 5: ask what the teacher would change before using the plan, and write the answer in the notes template, which keeps no personal detail in the repository. [hypothesis]

## 5. Questions and answers — DRAFT - NOT APPROVED FOR PUBLICATION

- Does it replace my judgement? No: it drafts and you check, and its feedback says when its next steps are general. [observed: test_w823_education_feedback_on_the_floor_says_its_next_steps_are_not_drawn_from_the_work]
- Can my pupils use it? No: the tools are not for children. [observed: test_w712_each_unchecked_constraint_says_what_it_is_to_a_reply_and_children_do_not_use_the_tools]
- Does it keep what I type? Not before you sign in. [observed: test_w952_fu1189_nothing_a_person_types_into_a_domain_tool_is_stored_before_sign_in]
- Does anything I type go to an outside AI company? Not by default: answers are served on the platform's own engine, and outside models stay off unless the Owner switches them on. [observed: test_domains_in_house_provenance]
- Will it plan a lesson on a religious subject? No: every teaching route refuses one. [observed: test_w659_every_teaching_route_refuses_a_religious_subject]
- What does it cost? No price is set; a price is the Owner's to set, by the formula the Owner ruled. [owner decision]

## 6. Outreach templates — DRAFT - NOT APPROVED FOR PUBLICATION

- To a teacher or tutor the Owner knows, DRAFT, NOT SENT: "I am testing a tool that drafts lesson plans and feedback for a teacher to check before use. Would you try it for thirty minutes on invented material, and tell me what you would change? Your name is not written into anything I keep." [owner decision]
- To a teacher-training contact, DRAFT, NOT SENT: "I am testing a tool that drafts lesson plans and feedback for teachers to check. Could you suggest where a teacher who wanted to try it on invented material might hear about it? I am not asking you to recommend it." [owner decision]

## What this document does not do

- It publishes nothing, sends nothing, sets no price and names no person. Each piece is a draft for the Owner, after the interviews. [owner decision]
