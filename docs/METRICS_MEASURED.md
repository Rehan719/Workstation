# Which business and product metrics are measured, and which are not

W878 (plan item P5.6, row FU-743). Written from this tree on 2026-11-12. A metric is MEASURED only when a
route returns it from a store the platform writes as the thing happens; PARTLY when it is returned with a stated limit
that changes what it can be read as; NOT MEASURED when nothing records it, and then the row says what would measure
it. Every amount of money below is virtual WST: no real-money rail is enabled, and the switch is the Owner's.

The guard (test_w878) reads the table: each MEASURED or PARTLY row names a route that is mounted, and each NOT
MEASURED row says what would measure it. A row moves from NOT MEASURED only with its source.

| Metric | State | Definition | Source | Denominator | Freshness | What would measure it |
|---|---|---|---|---|---|---|
| Entities established | MEASURED | registered living entities on the roster | GET /api/v1/economy/living-vsbs | none (a count) | read from the roster on each request | - |
| Revenue recorded per entity | PARTLY | revenue each entity's ledger holds | GET /api/v1/economy/ledger/{vsb_id} | none | per cycle | the figure is the one the cycle's caller supplied (FU-1010): it is recorded, not earned from a customer |
| Capital fund contributions and allocations | MEASURED | what cycles paid in, what was allocated, and what was set aside and not received | GET /api/v1/fund/status | the pool, part of it an unfunded seed (said on the route) | read from the fund store on each request | - |
| Real-money revenue | NOT MEASURED | money received from a customer | none | - | - | settled transactions from a live payment provider, which needs the Owner's real-money switch |
| Paying customers | NOT MEASURED | people or organisations paying for the product | none | - | - | an account with a subscription or a purchase record, which needs billing (the Owner's decision) |
| Projects created, by stage | MEASURED | projects on disk, by lifecycle stage, with their outputs | GET /api/v1/projects/stats/summary | none (counts) | read from the project store on each request | - |
| AI calls and what served them | MEASURED | each recorded run: what served it (the floor, a local model, an external one), how long it took, whether it produced output | GET /api/v1/operations/summary | recorded runs in the store, the rows from before the suite's isolation counted apart (W855) | appended as each run ends | - |
| Output quality pass rate | PARTLY | runs a quality gate passed, of the runs a gate assessed | GET /api/v1/operations/rankings | gate-assessed runs only; floor text is not assessable, so on a floor-only deployment the rate is over few or no runs | appended as each run ends | the basis on the route says how many runs carry a verdict |
| Which model is serving | MEASURED | the resource that served the most recent successful completion, beside the one predicted | GET /api/v1/native-ai/status | one row | history, not a live probe (said on the route) | - |
| Work done: seconds and tokens | PARTLY | the work budget's spend: wall-clock seconds always, tokens only where a serving model reported a count | GET /api/v1/organism/status | the window the budget keeps | as each run spends | tokens stay null until a model counts them; the floor counts none |
| A learner's Quran memorisation progress | MEASURED | the reviews scheduled and done for one learner (SM-2) | GET /api/v1/qep/hifz/progress/{uid} | that learner's items | as each review is recorded | - |
| Learners across the platform | NOT MEASURED | how many learners there are and how many keep going | none | - | - | a count over the learner store by last review date |
| Support satisfaction | PARTLY | satisfaction a person recorded after a support answer | GET /api/v1/support/satisfaction | the answers someone rated, not all answers | as each rating is recorded | - |
| Deliveries a person accepted | MEASURED | an entity's cascade run accepted, version by version, by its owner | GET /api/v1/swarm/cascade/runs | the entity's runs listed | as each acceptance is recorded (W851) | - |
| A person completing a task | NOT MEASURED | someone finishing what they came to do with a tool | none | - | - | an event when a tool's output is saved, exported or accepted, per person and per tool |
| A person returning | NOT MEASURED | someone coming back on a later day | none | - | - | sign-in events per person per day, which exist only with sign-in on |
| An output kept or used | PARTLY | outputs a person saved to their workspace | GET /api/v1/user/workspace | that person's own history only; no count across people or tools | as each save happens | a count over the workspace store per tool would make it a metric |
| Time to a first useful output | NOT MEASURED | how long from arriving to a first output the person keeps | none | - | - | the time between a person's first visit and their first save, per person |
