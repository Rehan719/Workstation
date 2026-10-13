# Workstation - business plan for Workstation itself

**Ratified by the Owner on 2026-10-13**, whole and without change. It is written from the whole vision
(`docs/WORKSTATION_IDBO_WHOLE_VISION.md`), the Owner's own canon, in the order the vision gives a plan:
executive summary, concept, vision, mission, strategy, aims, objectives. A change to this text from here on
needs the Owner's word. Ratifying it did not enter it into the product's own plan; the Owner enters that
through the plan's own edit page (ruling of 2026-10-10).

**How to read the tags.** Each statement ends with one tag: [owner-defined] the Owner said it, in the vision or
in a ruling · [observed] true of the product today · [inference] reasoned, not measured · [hypothesis] to be
tested · [deferred] left for later by decision · [owner decision] still the Owner's to make. The canvas is
`docs/business/BUSINESS_MODEL_CANVAS.md`.

No inherited figure is a target. No price, count of people, return or partner is stated as a fact about the
market.

## Executive summary

- Workstation takes any person's challenge and, with its own AI, either helps them do the work themselves or
  builds them a living enterprise that delivers the solution and then runs itself
  [owner-defined: the vision, sections 1 and 3A].
- It exists to give everyone the capability that only the largest organisations have had
  [owner-defined: the vision, section 14].
- Today it runs on the Owner's machine, with a local model, in virtual money, with sign-in off, and with no
  users but the Owner and no income [observed].
- The Owner works on it full time and prefers to start without cost [owner-defined, 2026-10-13].

## Concept

- **Domain Working**: tools for a person's own work across six domains - Religion, Science, Education, Law,
  Employment and Career, and Care. The first people it is offered to are those using the Law, Employment and
  Career, and Education tools [owner-defined: the vision, section 3A; ruling of 2026-10-10].
- **The Quran Education Platform** is the Religion domain's flagship and stays free
  [owner-defined: the vision, appendix A; ruling of 2026-10-10].
- **Concept to commercialisation**: one idea taken end to end into a living enterprise, with a board, a plan,
  books and a record of every change [owner-defined: the vision, section 4; observed in
  `agentic_core/api/change_control.py`].
- **Each enterprise is an economic organism**: it pays its owner a share, reinvests in itself and gives to
  causes, in virtual money until the Owner directs real rails [owner-defined: the vision, section 12].

## Vision

- A living, AI-mediated platform that takes any person's challenge, in any realm or domain of life and work,
  designs the best solution, and establishes a living enterprise that delivers it and then runs, defends,
  heals, learns and grows itself in faithful service of the founder's intent, ethically, compliantly and for
  the benefit of all humanity [owner-defined: the vision, section 1, shortened here].

## Mission

- Democratise working, AI-mediate human work so it is safer and easier, and resolve the challenges people face
  in every domain, with ethics that bind the design: integrity, compassion, excellence, halal compliance,
  stewardship and beneficence [owner-defined: the vision, section 2].
- The Owner has also stated a personal intention for this work. By the Owner's decision of 2026-10-13 it is
  held privately and is not published here [owner-defined].

## Strategy

The vision measures "available to all" by which switches the Owner has turned. They are turned in this order,
each only by the Owner [owner-defined: the vision, section 14; the order ruled 2026-10-12]:

1. Readiness on the Owner's machine: the register closed down and the final audit run [plan item P3.30].
2. Sign-in on [plan item P4.1].
3. A private deploy on one free small machine [plan item P4.5].
4. Invited adults, then self-serve sign-up [plan item P4.2].
5. Outside models, as accelerants only [plan item P4.3].
6. Real money, last, after review [plan item P4.6].

A managed database is left for later [deferred; plan item P4.4].

## Aims

- One person's whole journey, from a challenge to an operating enterprise, driven and measured
  [plan item P5.1].
- The Owner's own first endeavour walked by hand before anyone else's [owner-defined, 2026-10-12].
- The Quran platform's memorisation area usable by one invited adult [plan item P5.17].
- A person always able to see what waits on them and why [plan item P5.14].
- The enterprise's own agreements and its physical assets kept as truthful records
  [plan item P5.18] [plan item P5.19].

## Objectives

Each ties to a plan item that exists. None has a figure: nothing is measured about users yet, because the
product keeps no telemetry [observed].

| Objective | Plan item | What would measure it |
|---|---|---|
| Sign-in on, with every route asking who is calling or declared public | P4.1 | the perimeter register, `docs/PUBLIC_ROUTES.json` |
| One person's journey measured end to end | P5.1 | NOT MEASURED - a kept journey test |
| A price derived from the books and never typed | P5.2 | NOT MEASURED |
| What is not for sale, stated plainly | P5.5 | NOT MEASURED - a published statement |
| A reviewed tool says the review it has reached | P5.15 | the review records, read at the call |
| The open rows of the register closed | P3.30 | `docs/FOLLOWUPS.json`, counted at the call |

## Roadmap

- In rounds, never dates: the plan measures its own pace from the register and states it in rounds
  [observed: `scripts/followups.py`].
- No date is promised in this document [owner-defined, the planning rule].

## Operating model

- One living organism that owns its core AI capability and is never a front over outside services
  [owner-defined: the vision, section 15].
- One person, one machine, one local model today [observed].
- Every change is a round: a check made to fail first, a reviewed request, and merge only when the build
  server passes [observed: `.github/workflows/spine.yml`, `docs/DELIVERY_METHOD.json`].
- Anything not wired to the vision is archived, never deleted; a stub never ships
  [owner-defined: the vision, section 15].

## Costs

- To start, no cost is preferred [owner-defined, 2026-10-13].
- No bill has been entered, so no cost has a figure [observed].
- The lines that would carry one: hosting beyond a free tier, a domain name, a scholar's honorarium, a
  solicitor's view, an accountant [inference].

## Risks

Each is the Owner's to accept or refuse [owner decision]:

- One machine and one person: nothing runs when either is unavailable [observed].
- A small local model: answers are limited by it [observed].
- Religious content withheld until reviewed: a slower product, by ruling [owner-defined].
- No income until the last switch [inference].
- The name: its first word is common in computing, and the official registers have not been read
  [observed that none has been read; the rest is inference].

## What must be true before launch

- Sign-in on, and ownership checked on every store [plan item P4.1; row FU-1061].
- A named scholar before any composed religious content is shown [owner-defined, A.12.3].
- Children do not use the tools; that is looked at again only on the conditions the Owner set
  [owner-defined, 2026-10-13].
- A solicitor's view before any charge [owner-defined, 2026-10-13].
- The final uncapped audit run [owner-defined].
