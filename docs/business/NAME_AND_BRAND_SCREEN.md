# The name and brand screen: what was searched for each name, what the Owner holds, and each public claim with its evidence

**DRAFT until the Owner ratifies it.** Written for plan item P5.7, clause 3. Row FU-808 searched the chosen name and
closed in W725, recording what was read in one line of each ratified document. The clause also asks for an inventory
of what the Owner holds and a register of each public claim with its evidence, which that row did not give. This
document gives all three. A search of a register is not legal clearance, and nothing here is one.

## How to read this document

- Every statement carries a label: [observed] is read from the record or the page named beside it; [owner-defined] is the Owner's own choice, with its date; [owner decision] is the Owner's to make. [observed]
- NOT CHECKED means nothing was searched for that name in that place, so nothing is said about it. [observed]
- Nothing here names a person, an account or an address. Whatever the Owner holds that the repository does not record stays a placeholder, filled in outside the repository. [observed]

## 1. Each candidate name, with what was searched, where and when

| Name | Company register (Companies House) | UK trade mark register | EU trade mark register | US trade mark register | Web and domains |
|---|---|---|---|---|---|
| Workstation IDBO | No company of that name | No identical mark | No identical mark | NOT CHECKED | NOT CHECKED |
| IDBO Works | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED |
| IDBO Foundry | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED |
| VSB Foundry | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED |
| PurposeWeave | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED |
| IDBO Systems | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED | NOT CHECKED |

- Companies House and the UK and EU trade mark registers were read for Workstation IDBO on 2026-10-13 and 2026-10-14, the two trade mark registers in the Owner's own browser (row FU-808). [observed: `docs/business/BUSINESS_PLAN.md`]
- The one similar live mark found, in two of the four classes of interest, belongs to a pet-products business. [observed, 2026-10-14: `docs/business/BUSINESS_PLAN.md`]
- The Owner chose Workstation IDBO on 2026-10-14, after those searches. [owner-defined, 2026-10-14]
- The other five names were suggestions, labelled unverified when they were made on 2026-10-11, and no register, trade mark or domain search has been run for any of them. [observed: `docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md`, section 17.1, row 13]
- No clearance opinion has been obtained and no mark has been applied for. The ratified business plan says "no mark has been applied for, and no domain is held", which was true until 2026-11-22, when the Owner registered the domain the release machine answers on (row FU-1289). [observed: `docs/business/BUSINESS_PLAN.md`]
- A fresh reading of Companies House and the UK and EU trade mark registers was tried on 2026-11-20, and this environment's network refused each site (403 at the proxy), so the searches above stand at their October dates. [observed]
- Before the name is used in public, a search of the US register and of domains, and a clearance opinion from a qualified person, are the Owner's to commission. [owner decision]

## 2. What the Owner holds

- The chosen name, with no mark applied for or registered for it. [owner-defined, 2026-10-14]
- No company or other legal form: the formation workpack compares four routes and chooses none. [observed: `docs/business/FORMATION_WORKPACK.md`]
- The project's licence names its copyright holder in the line "Copyright 2026 Virtual Sovereign Business"; no company or other legal form is held under that name, and who holds the copyright is question 6 for a solicitor in `docs/business/FORMATION_WORKPACK.md`. [observed: `LICENSE`]
- A domain, registered by the Owner on 2026-11-22 and renewing on 2027-11-22: its A record names the release machine's fixed address, and the machine answers on it over HTTPS with sign-in on (row FU-1289). [observed: `docs/DEPLOYMENT.md`]
- The release machine, deployed in the Owner's cloud project, whose billing is the Owner's: an uptime check from outside it e-mails the Owner when `/health` fails, set up and driven on 2026-11-22 (row FU-1095). [observed: `docs/DEPLOYMENT.md`]
- The platform's source, in this repository, and the machine it runs on now, the Owner's own, with a local model. [observed: `docs/business/BUSINESS_MODEL_CANVAS.md`]
- No permission beyond what each source's own terms grant: the register of sources records what each permits, and the three letters asking for more are drafted and unsent (rows FU-1188 and FU-1283). [observed: `docs/SOURCES.json`]
- Accounts, payment details and anything else the Owner holds are not recorded in this repository, by design: [the Owner lists them, outside the repository]. [owner decision]

## 3. Each public claim, with its evidence

The public-facing drafts are the documents under docs/business/public/; today there is one,
`docs/business/public/FIRST_OFFER_DRAFTS.md`. Each row below is a claim those drafts make, the evidence they cite
beside it, and the numbered sections of the drafts that make it.

| Claim | Evidence | Sections |
|---|---|---|
| It drafts lesson plans and feedback on the platform's own engine, says what served each answer, and sends nothing to an outside model unless the Owner switches one on | test_domains_in_house_provenance | 1, 2, 3, 4, 5 |
| Its feedback says when its next steps are general rather than drawn from the work, and gives no final mark when no model is on | test_w823_education_feedback_on_the_floor_says_its_next_steps_are_not_drawn_from_the_work | 1, 2, 3, 4, 5 |
| It plans against frameworks it names | test_education_frameworks | 1, 4 |
| Nothing typed into it is kept before sign-in | test_w952_fu1189_nothing_a_person_types_into_a_domain_tool_is_stored_before_sign_in | 1, 4, 5 |
| Its tools are for teachers and tutors, not for the children they teach | test_w712_each_unchecked_constraint_says_what_it_is_to_a_reply_and_children_do_not_use_the_tools | 1, 5 |
| A plan needs a subject, a topic and a level; feedback needs the work, the task, the level and the subject | test_education_feedback_contract | 2 |
| Every teaching route refuses a religious subject | test_w659_every_teaching_route_refuses_a_religious_subject | 2, 5 |
| Every test the drafts name runs on the platform's own engine, without an outside model | test_w1151_fu809_each_public_draft_is_headed_and_every_claim_names_a_test_that_runs_without_an_outside_model | 3 |
| Whether teachers would use it again, and how often the need recurs, are not measured | `docs/business/FIRST_OFFER_CANDIDATES.md` | 2, 3 |

- The suite fails when a draft cites evidence this register does not list, or cites it in a section the register does not name, and when a row's evidence is cited nowhere (test_w1153). [observed]
- No claim in the drafts is about a customer, a partner or an endorsement, because there is none; what the drafts say of cost is that the Domain tools are free and that the Owner's charges fall only on generating an enterprise and on its profit; they name no amount for any charge. [observed: `docs/business/public/FIRST_OFFER_DRAFTS.md`]
- The register covers what the public drafts claim. What the product's own pages say is held by the plan's truth passes (plan item P2.40) and the final audit (plan item P5.22), not by this document. [observed]

## What this document does not do

- It clears no name, applies for no mark, buys no domain and lists no account; each is the Owner's. [owner decision]
