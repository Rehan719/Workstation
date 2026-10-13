# Workstation - business plan for Workstation itself

**DRAFT until the Owner ratifies it.** Nothing here enters the product's own plan as the Owner's words; the
Owner enters what they agree with through the plan's own edit page (ruling of 2026-10-10).

Every statement carries one label, as in `docs/business/BUSINESS_MODEL_CANVAS.md`:
**[observed]** · **[owner-defined]** · **[inference]** · **[hypothesis]** · **[deferred]** · **[owner decision]**.

No inherited figure is a target. No price, user count, return or partner is stated as a fact about the market.

## Executive summary

Workstation is a platform on which a person does their own work in a domain with AI tools that state what they
are, and on which a founder takes one idea to a governed, operating entity [observed: the delivery plan,
`docs/FABLE_DELIVERY_PROMPT.md`]. It runs today on the Owner's machine with a local model, in virtual units,
with sign-in off [observed]. It has no users other than the Owner and no income [observed]. The Owner works on
it full time and prefers to start without cost [owner-defined, 2026-10-13].

## Concept

Two things in one product [observed]:
- **Domain tools** for a person's own work. The first segment is Law, Employment and Career, and Education
  [owner-defined, 2026-10-10]. The Quran Education Platform stays free [owner-defined, 2026-10-10].
- **An enterprise layer** that generates an entity with a board, a plan, books and a change-control record, and
  tends it [observed: `agentic_core/api/change_control.py`, `agentic_core/economy/owner_payments.py`].

## Vision

A written vision exists and is the canon for the product [observed: `docs/WORKSTATION_IDBO_WHOLE_VISION.md`;
for the Quran platform, `docs/QURAN_EDUCATION_PLATFORM_VISION.md`]. A vision sentence for this document is the
Owner's to write [owner decision].

## Mission

The Owner has stated the intention this work serves. By the Owner's decision of 2026-10-13 it is held privately
and is not published here [owner-defined]. A mission sentence for publication is the Owner's to write
[owner decision].

## Strategy

The order in which the switches are turned, each only by the Owner [owner-defined, the Phase 4 order]:

1. Readiness on the Owner's machine - the register closed down and the final audit run [plan item P3.30].
2. Sign-in on [plan item P4.1].
3. A private deploy on one free small machine [plan item P4.5].
4. Invited adults, then self-serve sign-up [plan item P4.2].
5. External models, as accelerants only [plan item P4.3].
6. Real money, last, after review [plan item P4.6].

A managed database is deferred [deferred; plan item P4.4].

## Aims

- One person's whole journey, from a challenge to an operating entity, driven and measured [plan item P5.1].
- The Owner's first endeavour walked by hand before anyone else's [owner-defined, 2026-10-12].
- The Quran platform's memorisation area usable by one invited adult [plan item P5.17].
- What working with a person requires of the product - saying what waits on them and why [plan item P5.14].

## Objectives

Each ties to a plan item that exists. None has a figure: no telemetry is kept, so nothing here is measured yet
[observed].

| Objective | Plan item | What would measure it |
|---|---|---|
| Sign-in on with every mounted route asking or declared public | P4.1 | the perimeter register, `docs/PUBLIC_ROUTES.json` |
| One tenant's journey measured end to end | P5.1 | NOT MEASURED - a kept journey test |
| A price derived from the books and never typed | P5.2 | NOT MEASURED |
| What is not for sale, stated plainly | P5.5 | NOT MEASURED - a published statement |
| A reviewed tool says the tier of review it has reached | P5.15 | the review records, read at the call |
| The open rows of the register | P3.30 | `docs/FOLLOWUPS.json`, counted at the call |

## Roadmap

In rounds, never dates: the plan projects its own pace from the register and states it in rounds
[observed: `scripts/followups.py`]. No date is promised in this document [owner-defined, the planning rule].

## Operating model

- One person, one machine, one local model [observed].
- Every change is a round: a guard that is made to fail first, a pull request, and merge only when the build
  server's checks pass [observed: `.github/workflows/spine.yml`, `docs/DELIVERY_METHOD.json`].
- Religious content the platform composes waits for a named scholar; none is engaged [observed:
  `agentic_core/api/scholar_review.py`].

## Costs

To start, no cost is preferred [owner-defined, 2026-10-13]. No bill has been entered, so no cost has a figure
[observed]. The lines that would carry one: hosting beyond a free tier, a domain, a scholar's honorarium, a
solicitor's view, an accountant.

## Risks

Each is the Owner's to accept or refuse [owner decision]:

- One machine and one person: nothing runs when either is unavailable [observed].
- A small local model: answers are limited by it [observed].
- Religious content withheld until reviewed: a slower product, by ruling [owner-defined].
- No income until the last switch [inference].
- The name: the first word is common in computing; no register has been read for it [observed that none has
  been read; the rest is inference].

## What must be true before launch

- Sign-in on, and ownership checked on every store [plan item P4.1; row FU-1061].
- A named scholar before any composed religious content is shown [owner-defined, A.12.3].
- A scholar and a safeguarding lead before any child uses anything [deferred; row FU-1032].
- A solicitor's view before any charge [owner-defined, 2026-10-13].
- The final uncapped audit run [owner-defined].
