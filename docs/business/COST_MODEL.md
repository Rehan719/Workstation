# Cost model — what running the platform would cost, with every value marked by where it came from

**DRAFT until the Owner ratifies it.** Written for plan item P5.7, clause 2 (row FU-807). It sets out what running this
platform would cost in three scenarios, with each cost marked quoted, sourced, assumed or not measured. It gives the
unit economics as formulas on what the Owner has ruled is charged, and keeps the founder's time apart. No cost is
filled in: nothing in this tree measures one, no supplier has quoted, and a money figure in a business document stands
only beside the Owner's ruling. It promises no zero bill.

## How to read this document

- Every statement carries a label: [observed] is read from this tree on 2026-11-13; [owner-defined] is a ruling of the Owner's, with its date; [inference] is reasoned from what was observed; [hypothesis] is a claim something would test; [owner decision] is the Owner's to make. [observed]
- A cost is marked one of four ways. QUOTED: a price a named supplier gave in writing for this platform, with the date. SOURCED: a provider's published price, with its page and the date it was read. ASSUMED: a value chosen only so a calculation can be run, said to be assumed wherever it appears. NOT MEASURED: everything else. [observed]
- Every cost below is NOT MEASURED today. No supplier has been asked for a quote [observed]. Whether a business document may state a provider's published price is the Owner's question (row FU-1176) [owner decision]. An assumed money figure would need the Owner's ruling beside it, as plan item P5.6 holds for every business document [observed: `integration_tests/test_mvp_spine.py`].
- Nothing here is charged: amounts inside the platform are virtual WST, the one price the Owner has set is shown as set and not charged, and the real-money switch stays off (plan item P4.6). [observed]

## The three scenarios

- LEAN is the first deploy the Owner ruled: one small virtual machine on the free tier, private to the Owner, running the floor only, after a dry run has measured that the platform fits its memory (plan item P4.5). [owner-defined, 2026-10-12]
- In LEAN, the machine, its disk and its network are expected to fall inside the provider's free tier, but nothing has measured that they do; the dry run is what would show it (row FU-603). [inference]
- In LEAN, the bill is not promised to be zero: a free tier has limits, and use beyond them is charged. [inference]
- BASE adds what opening to a first person other than the Owner would need: sign-in on (plan item P4.1), backups kept off the machine (`scripts/backup_stores.py`), the outside uptime check the Owner holds (row FU-1095), and a solicitor's view on where that person's data may be kept, since the free regions are in the United States (plan item P4.5). [inference]
- In BASE, each added part is NOT MEASURED, and the storage for a backup kept off the machine is the part most likely to leave the free tier. [hypothesis]
- HIGHER ASSURANCE adds the outside help scoped in `docs/business/PRODUCTION_HARDENING_BRIEF.md`: its ten separable parts, from an independent review to a handover, each with the evidence that would accept it. [inference]
- In HIGHER ASSURANCE, each part would be QUOTED by whoever is chosen to do it; none has been asked. [observed]
- A model served from outside is in no scenario: external calls stay off until the Owner switches them on (plan item P4.3), and the platform runs on its own floor without them. [observed]

## The cost lines

| Line | LEAN | BASE | HIGHER ASSURANCE | How it would be marked |
|---|---|---|---|---|
| The virtual machine | free tier, NOT MEASURED | NOT MEASURED | NOT MEASURED | SOURCED from the provider's page, once row FU-1176 is decided |
| Disk, and backups kept off the machine | none kept off it | NOT MEASURED | NOT MEASURED | SOURCED |
| Network out of the machine | NOT MEASURED | NOT MEASURED | NOT MEASURED | SOURCED |
| The outside uptime check | none | NOT MEASURED | NOT MEASURED | SOURCED, or none if the provider's free tier covers it |
| A domain name and certificate | none | NOT MEASURED | NOT MEASURED | QUOTED by the registrar |
| Outside review and hardening | none | none | NOT MEASURED | QUOTED, part by part |
| A solicitor, an accountant and a scholar | none | NOT MEASURED | NOT MEASURED | QUOTED by each adviser |
| The founder's time | kept apart below | kept apart below | kept apart below | the Owner's own rate |

- The table names no amount. A line marked "none" is not part of that scenario, and every other cell waits for a quote, a dated provider page, or the Owner's ruling. [observed]
- Before real money, a scholar's view on the fee's form, a solicitor's on the regulatory line and an accountant's on the books are each the Owner's to arrange (plan item P5.16); before another person's data is stored in the free regions, where it may be kept is a solicitor's question (plan item P4.5). [owner-defined, 2026-10-12]

## The founder's time, kept apart

- The founder's hours are the largest cost of the first months and are counted in no line above. [hypothesis]
- Founder cost for a period = hours spent in the period × the Owner's own hourly rate. Both are NOT MEASURED; the rate is the Owner's to set. [owner decision]
- Nothing in this tree records the founder's hours, so the formula has no input yet. [observed]

## Unit economics, as formulas

- What is charged is the Owner's ruling (plan item P5.16): the Quran platform and every Domain are free, for individuals and for institutions; generating an entity is charged once; and each generated entity pays a quarter of its profit for updates and maintenance, taken before its own split. [owner-defined, 2026-10-12]
- The once-only price is ninety-nine pounds, credited against the entity's first profit share and waived for a charitable or non-distributing entity. It is shown as set and not charged until a named reviewer's pass, a solicitor's view and the real-money switch all exist (plan item P5.16). [owner-defined, 2026-10-13]
- Contribution per entity generated = the once-only price − the cost of generating one entity. The cost is NOT MEASURED. [inference]
- The platform's share from an entity in a cycle = a quarter × the entity's profit for the cycle, where profit is revenue less declared costs less the prudential reserve, never below zero; the first share is reduced by the once-only price it was credited against. NOT MEASURED for any entity. [inference]
- Break-even entities generated in a period = (the fixed cost for the period − the platform's share received in the period) ÷ contribution per entity generated. NOT MEASURED. [inference]
- Months to recover what was spent to win a founder = that spend ÷ the platform's share from that founder's entity per month. NOT MEASURED. [inference]
- Gross margin = (revenue − the cost of delivering it) ÷ revenue. NOT MEASURED. [inference]
- A Domain answered for a person costs something to serve and earns nothing by its own price, so its cost belongs in the fixed cost above. [inference]
- The first-offer candidates in `docs/business/FIRST_OFFER_CANDIDATES.md` are Domain workflows, which are free; which comes first, and whether it leads a founder to generate an entity, is left to the Owner after the interviews. [owner decision]

## The seven investment gates

- Plan item P5.7 asks for the seven investment gates and which one is evidenced today. No gate is defined anywhere in this tree: the four commercialisation prompts the clause was chartered from are not kept here, and the founder playbook they referred to was not received. [observed: `docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md`]
- So no gate can be marked evidenced, and none is invented here. [observed]
- To name them, the Owner can add the playbook, or rule which seven they are. Recommended, if the playbook is not to hand: the six switches of the Owner's hand, plan items P4.1 to P4.6, and a first offer the interviews support, so that each can be marked evidenced or not from what this tree shows. [owner decision]
