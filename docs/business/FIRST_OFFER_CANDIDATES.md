# First offer candidates — three workflows compared, and the interviews that would test one

**DRAFT until the Owner ratifies it.** Written for plan item P5.7 (row FU-806), after one person's journey was driven
from a challenge to an operating entity and its surfaces read back (W840). It compares three candidate first offers
on stated criteria, with the evidence for each cell or the words NOT MEASURED. It names one leading hypothesis and
what would refute it, lists who the offer is not for, and gives an interview guide, willingness-to-pay questions that
do not lead, and a notes template. Nothing here has been put to a customer. No price is proposed.

## How to read this document

- Every statement carries a label: [observed] is read from this tree on 2026-11-13; [inference] is reasoned from what was observed; [hypothesis] is a claim the interviews are meant to test; [owner decision] is the Owner's to make. [observed]
- NOT MEASURED means nothing in this tree, and no conversation with a person, shows the cell either way. It is not a guess at a low value. [observed]
- The tools named below run on the deterministic floor unless a model is available. External models stay off unless the Owner switches them on. [observed]

## The three candidates

- A. Law: how long a time limit runs, from the rule's own words, with the provision as its publisher prints it, and where a person can get help. `POST /api/v1/law/time-limit`, `GET /api/v1/law/statute/{kind}/{year}/{number}/section/{section}` and `GET /api/v1/law/help`. [observed]
- B. Employment and Career: a CV, a cover letter and interview preparation from what the person wrote themselves. `POST /api/v1/employment/cv`, `POST /api/v1/employment/cover-letter` and `POST /api/v1/employment/interview-prep`. [observed]
- C. Education: a lesson plan and feedback on a piece of work, against a named framework. `GET /api/v1/education/frameworks`, `POST /api/v1/education/lesson-plan` and `POST /api/v1/education/feedback`. [observed]

## The comparison

| Criterion | A. Law time limits | B. Employment documents | C. Education plans and feedback |
|---|---|---|---|
| What it does with no model | Computes a period from the rule's own words, read from the publisher; nothing is computed unless those words are there (test_w875) | Hands the person's own text to the composer as material, marked as data (test_w857); what the floor composes from it has not been judged by a person: NOT MEASURED | Returns floor sections read for over-claim, and says its next steps are general, not drawn from the work (test_w823) |
| What a model adds | Nothing to the arithmetic; a model is not used for it | The composed CV and letter | The specific feedback and the plan's detail |
| Harm if it is wrong | High: a missed deadline cannot be undone | Medium: a weaker application | Low: a teacher reads it before use |
| Who checks the output | The person, who may not be able to | The person | A teacher, by training |
| Personal data it holds | A person's own dispute: never sent to an external model (test_w899) | A person's work history | A piece of work; children do not use the tools (test_w712) |
| Help from a person, built in | Yes: a question about one's own case is routed to people (test_w874) | No | No |
| Would anyone pay | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| How often the need recurs | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| What a person uses today | NOT MEASURED | NOT MEASURED | NOT MEASURED |

- The three rows marked NOT MEASURED are the ones the interviews below exist to fill. No row of this table says which candidate wins. [observed]
- Candidate A is the most complete without a model, and the most harmful when wrong. Candidate C is the least harmful, and its value depends most on a model being available. [inference]

## The leading hypothesis

- Teachers and tutors who plan lessons against a named framework will use, and pay for, a tool that drafts the plan and the feedback for them to check, because they check it anyway. [hypothesis]
- It is chosen because the person who reads the output is trained to judge it, and because a wrong draft costs a re-read, not a missed deadline. [inference]
- It would be refuted by any of these: teachers say they would not use a draft they must check line by line; the floor's output without a model is not good enough to start from; or the person who would pay is a school whose buying route this business cannot reach. [hypothesis]
- Which candidate is offered first is the Owner's call, made after the interviews. [owner decision]

## Who the offer is not for

- A person who wants advice on their own live legal case: the Law tools route that question to people and do not give it. [observed]
- Anyone who needs something filed, served or signed: nothing here files, serves or signs. [observed]
- A care or clinical decision about a person: the Care tools keep an open hazard log, and none is offered as the one who decides. [inference]
- A child using the tools directly. [observed]
- An organisation whose data may not leave its own machines, unless it runs this platform itself. [inference]

## Interview guide

- Open with the person's own last instance: "Tell me about the last time you had to do this. What happened, step by step?" [inference]
- Ask what they did and what they used, not what they would do: "What did you use? What did it cost you in time?" [inference]
- Ask what went wrong: "What part of it went wrong or took longest? What did you do about it?" [inference]
- Ask who else was involved: "Who else had to see it or sign it off?" [inference]
- Show nothing until the end, and then only the floor's output on invented data, asking "What would you change before you used this?" [inference]
- Close by asking who else has the same problem, and whether they may be contacted again. [inference]

## Willingness-to-pay questions that do not lead

- "What do you pay now, in money or in time, for the way you do this?" No figure is offered first. [inference]
- "When did you last pay for a tool for this kind of work? Who decided, and how?" [inference]
- "If this disappeared after a month of using it, what would you do?" [inference]
- Never name a price, a discount or a comparison product before the person has answered. [inference]

## Notes template

- Date, the interviewer, and the setting (role and kind of organisation), with no name, address or contact detail written into this repository. [inference]
- The last instance, in the person's own words, and what they used. [inference]
- What it cost them, as they stated it, in time or money. [inference]
- Who decides and who pays, as they described it. [inference]
- What would make them stop using the tool, and what they would change first. [inference]
- Whether they agreed to be contacted again, recorded where the Owner keeps contacts, not here. [owner decision]
