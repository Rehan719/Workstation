# Living-strategy map: which existing component performs each step, and what stands between it and being relied on

**DRAFT until the Owner ratifies it.** It enters nothing into the product's own plan. It was written for row FU-744,
in plan item P5.6, so that no second planner is built: where a step already has a component, the map points at it.

## How to read this map

The living strategy has six steps: observe, propose, review, authorise, apply and record. For each step the map names
the component that performs it today, its file and the route a person or the platform uses, the test that drives it,
and the open rows that stand between it and being relied on.

## 1. Observe

- The remaining work is measured item by item, with its size, its open rows and what only the Owner can do, in
  `docs/REMAINING_WORK_MEASURED.md`. That the measurement adds up and names real items is driven by
  test_w787_the_remaining_work_measurement_adds_up_and_names_real_items [observed: `integration_tests/test_mvp_spine.py`].
- The register of findings is `docs/FOLLOWUPS.json`, kept by `scripts/followups.py`, whose check reads every row and
  every plan item before the register is saved [observed].
- The plan reads its open rows through `GET /api/v1/plan/followups` (`agentic_core/api/living_plan.py`) [observed].
- What the platform has spent is the work budget, in seconds of recorded work (`agentic_core/molecular/work_budget.py`).
  Since W900 to W902 every energy figure a page shows, and every energy threshold, derives from it. That is driven by
  test_w900_fu1112_with_the_work_budget_on_every_energy_threshold_reads_what_is_left_of_it [observed].
- Each run's outcome is recorded by `agentic_core/api/operational_excellence.py`. That record is what the model health
  table and the work budget read [observed].
- An appraisal of a scope is read through `GET /api/v1/method/appraise` (`agentic_core/api/method.py`). It files
  nothing and says so, driven by test_lgc_path_an_appraisal_files_nothing_says_so_and_change_control_decides
  [observed].
- Between this step and being relied on: row FU-1036 (every audit edition examined the floor-only configuration, which
  is not what the Owner runs) and row FU-1095 (a failure on the first deployment reaches no person) [observed].

## 2. Propose

- A change is proposed to Change Control through `POST /api/v1/cca/submit` (`agentic_core/api/change_control.py`).
  Change Control gives it a tier and attaches the scope's appraisal [observed].
- The plan's constitutional and strategic layers are set through `POST /api/v1/business-plan/set`
  (`agentic_core/api/business_plan.py`), the plan's owner-edit route [observed].
- The Owner's ratified plan enters through one action: `GET /api/v1/business-plan/ratified/preview`, then
  `POST /api/v1/business-plan/ratified/enter`, refused while sign-in is off. Driven by
  test_w726_one_action_enters_the_ratified_plan_and_the_record_says_how [observed].
- The roadmap is read from `GET /api/v1/sovereign-evolution/roadmap` (`agentic_core/api/sovereign_evolution.py`), and
  a cycle reads what the previous one did, driven by test_w828_a_sovereign_evolution_cycle_reads_what_the_previous_one_did
  [observed].
- Between this step and being relied on: sign-in, which only the Owner switches on [owner decision; plan item P4.1].

## 3. Review

- A change is reviewed through `POST /api/v1/cca/{cca_id}/review`. Once a second administrator exists, a high or
  critical change is not decided by the person who submitted it. Driven by
  test_w882_a_high_change_is_not_decided_by_its_submitter_once_a_second_administrator_exists [observed].
- The Board Pack gathers what a review reads: the platform's through `GET /api/v1/economy/board-pack`
  (`agentic_core/api/economy.py`), and an entity's own through `GET /api/v1/vsb/{vsb_id}/board-pack`
  (`agentic_core/api/vsb.py`). Driven by test_w471_board_pack_and_chiefs_opening_are_honest_both_ways [observed].
- Between this step and being relied on: row FU-993 (the audit has never been run against planted defects or
  deliberately false findings) [observed].

## 4. Authorise

- A change waits for an explicit decision, and a governed setting is not applied until the health check passes. Driven
  by test_w718_a_governed_live_setting_is_not_applied_without_the_health_check [observed].
- The Board ratifies a high change through `POST /api/v1/board/ratifications/{cca_id}` (`agentic_core/api/board.py`)
  [observed].
- The Owner's rulings are recorded with their dates in `docs/FABLE_DELIVERY_PROMPT.md`, and a ruling the Owner has not
  made is never assumed [observed].
- Between this step and being relied on: row FU-1086 (the uncapped final audit has no item that builds or runs it)
  [owner decision].

## 5. Apply

- An approved change is applied, once, through `POST /api/v1/cca/{cca_id}/implement`, which writes the governed
  setting through `agentic_core/organism/reconfiguration.py`. Driven by test_w438_organism_cluster_audited_fixes_hold
  [observed].
- The cadence decides when the organism's layers refresh, read through `GET /api/v1/organism/cadence`
  (`agentic_core/api/organism_status.py`). Driven by test_w585_p33_the_cadence_layers_refresh_themselves_and_say_why
  [observed].
- The heartbeat performs the beat-driven steps (`agentic_core/organism/heartbeat.py`), read through
  `GET /api/v1/heartbeat/status` (`agentic_core/api/heartbeat.py`). Driven by test_heartbeat_status [observed].
- Between this step and being relied on: row FU-849 (the opt-in default for an entity registered before the
  auto-economy flag existed is the Owner's to rule) [owner decision].

## 6. Record

- Every governed event is chained in a ledger, read through `GET /api/v1/gaas/ueg/events` and verified by re-hashing
  through `GET /api/v1/gaas/ueg/verify` (`agentic_core/api/constitutional_gaas.py`). It is a linear hash chain and is
  called that, driven by test_w807_fu851_fu852_fu856_the_ledger_is_called_what_it_is_and_two_dead_routes_are_archived
  [observed].
- Each round's commit says what changed and what its own full suite measured, and the register records each row's
  close with the round that closed it [observed: `docs/FOLLOWUPS.json`].
- Whether a ratified method amendment was carried out can be read, driven by
  test_w827_whether_a_ratified_method_amendment_was_carried_out_can_be_read [observed].
- Between this step and being relied on: row FU-1151 (two committed audit run records carry text of a private kind in
  the public tree) and row FU-1040 (a test double's rows in the Owner's own store, which only the Owner's machine can
  move aside) [owner decision].

## What this map does not do

- It builds no planner, scores nothing and ranks nothing: every step names a component that already exists [inference].
- A step with an open row is not yet relied on, and this map does not say when it will be [inference].
