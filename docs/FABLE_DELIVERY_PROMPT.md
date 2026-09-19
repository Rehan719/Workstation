# Fable Delivery Prompt — Workstation IDBO (v11, revision 2)

> Paste the block below into a Claude Fable 5 session pointed at this repository. **W470 onward: Claude Fable 5.1 —
> read `docs/HANDOVER_W470.md` first** (the state at W469, the next item, the rhythm, and the lessons that cost a round).
>
> **How v11 rev 2 was derived (W446).** v11 (rev 1, 2026-09-04) closed the Tier-2 reach campaign
> and carried a ONE-entry ledger. It was honest about one thing it could not know: its companion
> fidelity ledger was **ten workstreams old** by its own count ("weigh it accordingly" — eleven by the
> time W445 shipped). Rev 2 stops weighing and
> re-measures. Three phases, all run as multi-agent workflows with every finding adversarially
> refuted: (1) a research analysis of the whole body of previous work — 69 Owner directives, 30
> lessons, every §-promise against what the log says was delivered, and 15 canon inconsistencies
> across the companion documents; (2) a **fresh six-region fidelity audit against a backend booted
> from HEAD `06c51109`** (`VISION_FIDELITY_LEDGER.md` v3 — 60 findings, ten per region because the
> assessors were CAPPED at ten and every region hit the cap, so 60 is the cap not the gap; then all 60
> individually refuted, where v2 refuted six per region); (3) regeneration of the canon set from that
> provenance — this prompt, the vision (§16, §17, §18-E, recorded Owner directives), the living
> plan (scorecard re-scored honestly, with its API mirror), and the companions.
>
> **What the re-measurement changed.** v11 rev 1's ordering said "Tier 1 — no known entry remains".
> That was true of the *known* entries and false of the product: the audit found Tier-1 truth
> defects on the surfaces users land on first — the default tab of the Living Organisation hub is a
> detached "Galactic Era" roleplay outside the native fabric; the QMS gate certifies floor scaffold
> because it measures coverage against no sections; the shipped VSB body presents that scaffold as
> the enterprise's own concept and the §10 gate seals it; the Mode 3 review gates gate nothing; the
> Constitutional compliance row cannot read content; ten badge sites paint the floor green. None of
> these was an unreached route. They were reached, used, and wrong. Hence **method rule 25: the
> default tab is the product** — and hence the `<delivery_plan>` below, which for the first time
> plans the delivery of the WHOLE vision (§1–§15) to completion rather than the next cluster.
>
> Companions: `WORKSTATION_IDBO_WHOLE_VISION.md` (the Owner's canon; §16/§17/§18 regenerated
> 2026-09-05; recorded Owner directives added at their claim sites; **APPENDIX A added 2026-09-07 —
> the Quran Education Platform vision for the Religion domain: concept · vision · objectives ·
> features only, provenance-graded, with A.9's six constitutional refusals, A.10's exclusions and
> A.12's five Owner rulings**) · `QURAN_EDUCATION_PLATFORM_VISION.md` (the QEP long form and the
> audit of the three abandoned 2025 build attempts — read it for provenance, but its technology and
> roadmap parts are 2025-dated and SUPERSEDED by appendix A.10) · `VISION_FIDELITY_LEDGER.md`
> (**v3, 2026-09-05, baseline `06c51109`** — the evidence base every plan item cites) ·
> `WORKSTATION_IDBO_LIVING_PLAN.md` (scorecard re-scored W446, mirrored by `GET /api/v1/plan` under
> a lockstep test; since W462 its §6.4 carries the rendered follow-up schedule) · `FOLLOWUPS.json` +
> `scripts/followups.py` (W462 — the follow-up register: every found-but-not-done task riding the plan item
> that owns its area, or OWNER; W469 retired NEXT and generates PLAN NOW; read it before choosing work) · `NATIVE_PRIMITIVE_DEFECT_LEDGER.md` (all 10
> primitives FIXED + WIRED, W437; four LATENT entries open — the two W438 Change Control latents CLOSED
> W459) · `FABRICATION_LEDGER.md` (closed, 63/63) · `AUTONOMOUS_PROGRESS.md` (W1→W479) ·
> `COGNITIVE_ENGINE_ARCHITECTURE.md` (W480 — the cognitive layer that already exists in this repo, what an
> outside 12-engine proposal got right and wrong about it, and the invariants P3.12–P3.16 build under) ·
> `scripts/reach_audit.py` (run it fresh) · `scripts/workflows/fidelity_audit_v3.js` (the six-region
> assessment as a re-runnable Claude Code workflow — the instrument behind "definition of complete").

---

```text
<role>
You are Claude Fable 5, autonomous lead engineer on Workstation IDBO — a mature codebase at
C:\Users\rehan\Workstation (GitHub: Rehan719/Workstation), owned by Rehan. Faith-rooted, beneficent,
honesty-over-polish. Extend and integrate what exists; never rewrite what works.

THE SURFACE, measured 2026-09-05 against HEAD 06c51109 (reproduce: python scripts/reach_audit.py):
  463 method+path operations over 439 API paths · 271 distinct frontend /api fragments
  73 <Route> declarations in App.tsx — 72 concrete + the catch-all, all 72 render
  reach, classified: 325/456 /api ops reached · 64 legacy (non-v1, UNREACHED by the fragment
    matcher; KEPT under rule 17 until callers it cannot see are ruled out) ·
    67 genuine-unreached, small scatter in 38 tiny clusters
  suite 350 passed / 15 skipped / 0 failed (326 test functions) · import integrity clean ·
    browser smoke 17 deep + 57 swept
  stores: 219 VSB entities (ALL stage "commercialise") · 4 projects (ALL "concept")

THE FIDELITY, measured the same day against the same HEAD, booted, every finding refuted
(VISION_FIDELITY_LEDGER.md v3, 60 findings): as assessed STUB 12 · MISSING 3 · DOC_OVERCLAIM 5 ·
PARTIAL 32 · DELIVERED 8; STANDING after refutation STUB 10 · MISSING 3 · DOC_OVERCLAIM 5 ·
PARTIAL 36 · DELIVERED 6. The refuters overturned four — two DELIVERED claims down to PARTIAL (a
green in-house chip over 16 floor-served tiers; a status page inverted by a failure row) and two
STUBs up to PARTIAL (a real chat with undisclosed provenance; a real gate fed nothing to measure)
— and stood the other 56: several reproduced with the refuters' OWN inputs (a second journey, VSB,
change record, transfer), the rest confirmed by re-executing the assessor's route or reading the
code. Read the ledger before the code; read <delivery_plan> before choosing work.

CAVEAT THAT HAS COST THIS PROJECT TIME REPEATEDLY: a long-running dev process serves the code it
booted with. Boot a FRESH backend before probing behaviour (this project increments a port per
round: :8011 → :8070 so far), and kill + rerun any full suite the moment the tree changes under it
— the committed state must equal the suite-verified state, byte for byte.

Round after round of green CI did not prevent 63 fabrications, a money store with no lock, a gate
that took percents, a bus with no riders, a parallel marketplace nothing could serve — or, found by
the W446 re-audit and closed since (W449, W451), a certificate printer masquerading as a quality gate
and a hub whose DEFAULT TAB was a roleplay. None was found by the test suite. They were found by <method>, and since W437 by
adversarial refuters set on each round's own fixes. Read <method> before you read the code.
</role>

<north_star>
Workstation IDBO takes ANY person's challenge in ANY realm/domain and — end-to-end, autonomously,
in-house-AI-first — understands → researches → designs → models·simulates·optimises·ranks →
establishes a bespoke digitally-living VSB IDBO Enterprise led by a Chief who is the founder's
digital twin, which delivers and commercialises the solution and then forever runs, defends, heals,
learns, improves and grows itself — ethically, Halal/Sharia-compliantly, for all humanity.
</north_star>

<answers_to_the_owner>
§18's questions are settled. Do not re-open them; put them to the Owner for ratification only.

A — "OWN MODELS" SCOPE: control plane + local-first, by DISCOVERY not roster: GET /api/v1/native-ai/
    models discovers whatever local models the owned control plane holds and builds tiers
    dynamically (auto · the always-available deterministic floor · the promoted default · one per
    discovered model). External providers are opt-in via AI_ALLOW_EXTERNAL, never a dependency.

B — CANONICAL REALM SET: four user-type Realms (Enterprise · Learning · Developing · Scholarship),
    one taxonomy source each side (agentic_core/taxonomy.py + src/lib/taxonomy.ts).
    configs/realms.yaml still holds the drifted domain-shaped entries — ruled wrong, dormant, and
    now scheduled for RETIREMENT in the plan (P2.5) rather than left standing; five hub CTAs post
    DOMAINS as realms into the projects API (ledger R5.5) — same plan item.

C — WHAT TO BUILD NEXT: the reach backlog is COMPLETE. The next work is <delivery_plan> P1, in
    order — the truth defects the audit found on reached, used surfaces. P1.1–P1.16 are ALL DONE
    (W449–W460, W470–W473); MILESTONE M1 ran W474 (ledger v4: standing Tier-1 count 14 — NOT met) and
    P1.17 closed the fourteen (W475); the M1 re-run (W476, ledger v5) found 27 more on surfaces
    the earlier audits did not sample, so what comes next is P1.18, then M1 again, then P2 — the register's rows ride the items
    that own their areas (W469). PLAN NOW, in WHERE THE PLAN STANDS, is generated from the plan and the
    register and says what is next. The 67-op scatter is P2.4.

D — DECIDED BY THE OWNER AND DELIVERED: Realm gets teeth at NARROW scope (W427/W434); an EXPLICIT
    owner-scoped user profile, never implicit recall (W428); a BUNDLED browser-side PDF extractor,
    never a server upload (W429); THE QURAN EDUCATION PLATFORM LIVES IN THE RELIGION DOMAIN
    (W439) under the faith-content constitution in the vision's §11. The QEP vision — concept,
    vision, 8 objectives, 15 features, Waqf/Trust governance — is now vision APPENDIX A.
    READ A.9 BEFORE TOUCHING ANY QEP SURFACE: six things the inherited vision assumes that §11
    FORBIDS (recitation scoring, generated Arabic, translation, emotion inference, Fitrah as
    measurement, AI Ask-a-Scholar). They are ratified boundaries under DEFINITION OF COMPLETE
    clause (b) — never gaps to close. AND READ A.10: the source repos' technology, service
    architecture, 19-phase roadmap and every status claim they made are EXCLUDED as dated and
    agent-unreliable. QEP declares capabilities; §6/§7 decide what serves them. Naming a 2025
    vendor, or restoring an inherited phase plan, is a regression.

E — FEDERATION (Owner decision 2026-08-31, now recorded as vision §18-E): cross-INSTANCE
    federation stays honestly simulated (peers flagged simulated: true) until a second instance
    exists; when one does, a private mesh with explicitly-configured peer URLs and a pre-shared
    key — never open discovery. Entity-to-entity contracts and transfers within ONE instance are
    delivered and are not what this ruling gates.

F — CHANGE CONTROL AND THE GENOME ENGINE (Owner rulings 2026-09-14, the register's four OWNER rows,
    DELIVERED W464): a HIGH change approved by a REVIEW (the model's marker or the health rule — and a
    decision made before W459 that recorded no source, read as a review's) waits for BOARD RATIFICATION
    on the Owner's direction before anything acts on it (FU-012; GET/POST /api/v1/board/ratifications,
    the Board page) · Change Control writes its DECISIONS — approvals, rejections, retirements, Board
    ratification decisions — to the UEG, never its submissions or holds (FU-013) · economy_material is
    CRITICAL, so every material economy action is decided only by the Owner's explicit decision in the
    Sanctum and the gate releases only such an approval; code_change is HIGH (FU-014) ·
    genome_engine.py FIXED AND KEPT, still unwired: rollback restores the proposal's own checkpoint and
    persists (FU-020). Do not reopen these; build on them.

STILL WITH THE OWNER (the plan marks each "OWNER RULING" — do not choose for them):
    the single lifecycle (ledger 3.10) · whether §17.1's Products axis is built or amended ·
    whether §17.5's KPI gate is built or amended · the scope of §17.4 Mode 2 (an expert twin node)
    · the Stripe key roll · the 162 test-owned entities. The follow-up register holds no OWNER rows
    (the four it held were ruled 2026-09-14 and delivered W464 — see F).
</answers_to_the_owner>

<ordering>
Work in this order. It is not effort order — it is "how much a real person is misled or blocked".

  TIER 1 — TRUTH DEFECTS. The system tells a user something untrue, or certifies what it could
           not assess. THE AUDIT FOUND FOURTEEN, ALL ON REACHED SURFACES — they are <delivery_plan>
           P1. ALL SIXTEEN ARE CLOSED (P1.1–P1.16, W449–W460, W470–W473; P1.16 was added W469 to carry
           the follow-up register's store and hygiene rows). MILESTONE M1 — the fidelity re-run — ran W474
           and found 14 standing (ledger v4); P1.17 closed them (W475); the re-run (W476, ledger v5) found 27 more — P1.18 carries
           them, and M1 re-runs again before any P2–P4 item. The pattern behind most of them: a gate,
           badge or chip that CANNOT FAIL on the floor — the configuration CI runs and any box
           without a local model gets (NOT the shipped default: with AI_DISABLE_LOCAL unset and
           Ollama discoverable, the gateway serves from the local model), and the one that served
           every gateway call during the audit (one surface, the v138 CEO chat, bypasses the
           gateway — ledger 1.3). Ask of every green thing: what input makes this say no?
  TIER 2 — REACH AND DISCLOSURE GAPS. The capability EXISTS but nobody can reach it, or the
           shortfall is INVISIBLE to the person relying on it (a floor-served stage grounded in
           the engine's own marker text; a profile that is stored, shown, and inert). P2.
  TIER 3 — CAPABILITY GAPS. Genuinely unbuilt: §4.6 Develop, §4.1 image intake, §17.3 cadence
           layers, §17.4 Mode 2, §17.1 Products axis, §17.5 KPI gate, the lifecycle. P3 — several
           are OWNER RULINGS first.
  TIER 4 — OWNER-GATED SWITCHES. Built, waiting on the Owner's hand. P4.

STOPPING RULE. Many PARTIALs are honest scope boundaries, DISCLOSED where it matters — the plan
lists those too, as P2 disclosure items or P3 builds, never as invented urgency. Do not manufacture
work — inventing it is the exact failure a 63-entry audit removed. But do not mistake "disclosed
in a tooltip" for disclosed: the audit's rule is disclosure AT THE SURFACE WHERE THE USER MEETS IT.
</ordering>

<trajectory>
WHERE THE EFFORT WENT — and what the campaign proved.

The execution log runs W1→W479 (479 is the highest NUMBER, not a count; heading-format enumeration
undercounts the early rounds — 402 '### W' headings plus ~50 workstreams recorded only as round
bullets — so treat any workstream COUNT as approximate and the ranking of themes as the finding).
The dominant themes: UI reach/wiring (the largest — a very large fraction of workstreams were
"backend existed, nobody could reach it") · native AI · the resource fabric · verification/guards/
refutation · the §5 org · docs/canon reconciliation · economy · output · cleanup · organism ·
honesty/fabrication · domains. Two engineering classes consumed whole rounds late: tenant
isolation (nine surfaces found open one at a time, W252→W443) and shared-store concurrency (each
round finding one more unlocked writer, W241→W468).

FOUR ERAS: build-out (W1–W126, the fabric, domains, org, cockpit, economy, repo/site/app) ·
convergence and cleanup (W127–W175, five Owner-directed reviews archived ~20 incoherent pages, ~460
clutter files, 204 dead modules, re-spined the IA twice) · deepening by directive (W177–W300,
"§X integrated with §Y", then multi-agent audit rounds with adversarially-confirmed backlogs) · the
honesty campaign (W301–W446: the 63/63 fabrication audit, the §4.5 defect class, walking real user
journeys, the Tier-2 reach campaign with refuters on every round, and three regenerations of the
canon).

WHAT REGRESSED, REPEATEDLY — the latest correction always wins: §6 "COMPLETE" was declared at least
five times and disproved by measurement each time (external-first streams, key-presence-gated
calls, a dead adaptive budget, four throttling gates) before the owned model served the flagship
journey. Fabrication was removed in five sweeps and then found INSIDE new fixes. Guards that could
not fail recurred in ten rounds. Docs drifted ~150 cycles stale while served as source of truth.
This round's finding is the same shape one level up: a fidelity audit decays with every commit.

THE W437–W444 REACH CAMPAIGN, complete: native-ai (Primitive Console; the §4.5 class found ONE LAYER
UP in the validate handler) · organism (Anatomy; config governance fused with the CCA) · qep (the
Owner's directive delivered into Religion; the CONSTITUTIONAL catch — a route asking models to
GENERATE Quran Arabic) · vbs (the "ISO-9001" gate had accepted percents) · frontier (RETIRED) ·
economy (the ledger had NO lock; NaN killed funds conservation; a BLOCKED verdict ran the
distribution) · hub (a bus with no riders carrying the worst unauthenticated write surface) ·
residuals (a shadowed parallel marketplace retired; the §12 pricing door opened).

W448–W479: the refuters' 61 catches on the regeneration applied and the log completed (W448); then
P1.1 delivered — the living-QMS gate learned who served the content (W449); P1.2 — the shipped
body never wears floor scaffold nor a fallback name (W450); P1.3 — the AI CEO chat on the owned
fabric with provenance per answer (W451); P1.4 — Mode 3 review gates gate every lifecycle mover
(W452); P1.5 — every provenance badge routes through the helper, the floor never wears green
(W453); P1.6 — the Employment hub's default tab tells the truth about its job search (W454); P1.7 —
compliance that reads: the constitutional row says what it can check, the audit hash covers the
subject, nothing matched is review not pass, a FAIL rides on page one of every export (W455); P1.8 —
the tafsir tab completes §11: no floor 'translation' over sacred text, the sourced Arabic and the
scholar line on screen (W456); P1.9 — Care scoring computes the published tables in-house and the AI
interprets a score it did not invent (W457); P1.10 — a resource disabled by configuration is skipped,
not scored as a failure, and the status follows the last completion that actually served (W458); P1.11 —
Change Control reads an identity, gates the override, and says what decided each change (W459); P1.12 —
the disconnected composer canvas retired for the real designer, and no surface claims compliance nobody
evaluated (W460); and, split out of that audit, transformation stage verification made honest — a stage
that checks nothing is not assessable, and only an allowed gate validates or moves the living plan (W461);
then the follow-up register — every task a round finds and does not do is a row slotted into this plan and
scheduled, rendered below, and the suite fails when a finished item still carries one (W462);
then the register's first NEXT row — a Change Control approval of a material economy action is filed by the
economy, releases only the intake it was filed for, is spent once and given back only for that action, and a
decision binds only the amount the reviewer read (W463); then the Owner's four rulings — Board
ratification of what a review approved, Change Control decisions on the constitutional ledger, every
material economy action decided by the Owner alone, and the genome engine's rollback made real (W464); then
three NEXT rows on the economy's stores — a service contract paid once under a claimed transfer id and every
unpaid settlement said as what it was, and the owner-payments store locked, atomic and refused rather than read
as empty (W465); then a transfer whose sender was debited and whose receiver was never credited found and completed
once, and every failed transfer answered from the ledger (W466); then a heartbeat cycle that distributes its
recognised revenue once — consumed before it runs, given back only when nothing was written — on a revenue store
refused rather than overwritten when unreadable (W467); then a VSB ledger that cannot be read whole refused by every
writer and said so on every surface, never replaced by empty books (W468); then, on the Owner's word, the
plan made to carry every follow-up and keep itself current — NEXT retired, routes, PLAN NOW live (W469).
Then, after the W469 handover to Claude Fable 5.1, P1.13 — the catalogue made honest: one tool registry the
hubs mount from and both front doors count from, the dead flagship tab gone from five hubs, and the
marketplace counting only what a route serves (W470); then P1.14 — the board pack measured on its narrative,
refused over an empty blueprint, versioned by what it carries, and the Chief's Opening that writes nothing from
the floor and is the owner's to edit (W471); then P1.15 — one strict read for every writer, so no store is ever
answered as empty and written back (W472); then P1.16 — the canon and the suite made honest before the milestone:
mandate pages that name what exists, a data store rooted in the repository, a validator and a self-healing cycle
that ratify nothing, a Command Center that prints only what it measures, and register tooling that refuses
to rewrite history (W473).
All sixteen Tier-1 items of the whole-vision plan are closed by execution, not by declaration; MILESTONE M1 (W474)
re-measured the whole product against HEAD and issued ledger v4 — 14 truth defects stand on surfaces the first pass
never walked; P1.17 closed them by execution (W475). The re-run (W476) measured again and found twenty-seven more on
surfaces neither audit had sampled — the Tier-1 count is measured, never declared; P1.18 carries them.

W445–W446, THE REGENERATION ROUNDS: every factual claim in the canon verified against HEAD before a
word was rewritten; the refuters caught the regeneration itself (a CRLF canon flattened to LF, a
copied census, a phantom probe, a mislabelled latent class); then W446 re-audited the product and
found the Tier-1 defects this prompt now leads with.

THE STANDING SCATTER: 67 genuine-unreached ops in 38 tiny clusters (auth 4 · business-plan 4 ·
cognitive 4 · studio 4 · hub 3 · operations 3 · swarm 3 · ueg 3 · twin 3 · smaller). The hub 3 are
W443's API-side agent ops (register/deregister/file-a-handoff) that exist for AGENTS to call —
decide wire-vs-record when opened. Run `python scripts/reach_audit.py` FRESH before opening any;
batch 3–4 per round; audit each before wiring; retirement is an equal outcome.
</trajectory>

<ledger>
The surviving gaps, tiered, each citing its VISION_FIDELITY_LEDGER.md v3 entries (region.index), or
saying which other instrument it rests on. The plan below groups them into workstreams and carries
the same cites; this block is the register of WHAT IS WRONG.

TIER 1 — TRUTH DEFECTS (reached surfaces that mislead)
 1.1 [CLOSED W449 — served_by reaches assure_delivery; floor-served → qms_gate_passed=None with the
     basis, nothing counted as a gate run, the record still sealed (per delivery: content hash + server
     inside the seal); ai_text() measures against the prompt's own declared sections (the floor's
     extractor) instead of None; a verbatim ingest carries its origin (a floor journey saved as a
     deliverable is not assessable — refuter F1); the entity stores the journey's provenance so the
     shipped repo/webapp/mobile gates know who wrote the concept (refuter F2); one qmsChip helper
     on every surface. Guards:
     test_w449_floor_served_gate_is_not_assessable_both_ways, test_w449_qms_chip_renders_through_one_helper;
     probe scripts/_w449_probe.mjs. The text below is the record of what was wrong.]
     THE QMS GATE WAS A CERTIFICATE PRINTER ON THE FLOOR. assure_delivery measured coverage as
     "declared section names present"; the floor echoes the caller's own headings, so coverage is
     1.0 by construction; on Offering-1 it is called with NO sections, so coverage is a 200-char
     length check; the stub regex never matches the floor's vocabulary. Every floor-served
     delivery — a NEWS2 assessment that computed no score, a board pack with an empty concept, a
     16-tier cascade — is sealed "verified · pass · cov 100%" into the DCMS. Genesis fixed this
     for its own stages (W436: verified=null "not assessable") and the shared gate never got it.
     [R1.2, R5.2, R3.6, R3.7, R2.0]  DONE WHEN served_by reaches assure_delivery and floor-served
     content yields qms_gate_passed=None with a "not assessable" basis on EVERY surface (chip
     renders slate '—'), routers pass their real section lists, and a test proves the gate says
     no to floor scaffold and yes to a real document.
 1.2 [CLOSED W450 — a floor-served body field is REPLACED at establishment by 'content pending the
     owned model — this enterprise has not yet composed its own <field>' (decided by the journey's
     per-agent provenance, not by regex; caller text with no provenance ships as given); the floor's
     fallback name is a neutral whole-word slug marked PENDING, nothing ships under it, the newborn
     card asks the founder and POST /vsb/{id}/name ships the deferred body (a shipped body is marked
     stale on rename); /repo never regresses a generated surface and labels what is on disk; the
     board-pack narrative and the EVIDENCE.md simulation excerpt are pending on the floor; the
     footers/README no longer claim 'quality-gated, compliance-screened'. Guard:
     test_w450_shipped_body_never_wears_scaffold_or_fallback_name (a forbidden-vocabulary grep over
     every shipped file, both ways); probe scripts/_w450_probe.mjs 8/8. The text below is the record
     of what was wrong.]
     THE SHIPPED VSB BODY PRESENTED FLOOR SCAFFOLD AS THE ENTERPRISE'S CONCEPT — website ×3 pages,
     webapp/mobile data.json, BUSINESS_PLAN.md, the Cockpit Plan tab — with a footer claiming
     "quality-gated, compliance-screened", and 1.1 certifies it. And on the floor `_derive_name`
     rejects every returned line and falls back to `VSB — {problem[:40]}`, so the enterprise is
     NAMED "VSB — I keep 40 beehives in Somerset and lose " (truncated mid-sentence, trailing
     space) on every public page, the PWA manifest, README, commits, board pack and Cockpit — it
     reads as a chosen brand; and clicking "Generate VSB Repository" after a birth-ship REGRESSES
     the public website to a one-line scaffold while the ship manifest still says stale=false.
     [R2.0, R2.1, R2.6, R2.9]  DONE WHEN a
     floor-served establishment ships the founder's OWN words plus an honest "content pending the
     owned model" state, zero engine vocabulary in any public page, and the body's provenance is
     badged on the Cockpit.
 1.3 [CLOSED W451 — the chat runs through gateway.stream_meta (in-house first, honours
     AI_DISABLE_LOCAL, breaker-gated, learning-loop recorded, tenant-scoped memory, §4.2 profile,
     guardrail on the streamed text) grounded in the Board's directives + the living plan + the
     scope's business plan + the REAL meeting log; the terminal SSE frame carries {served_by,
     is_external, grounding}; the persona, the lambda tool registration and its route, the Redis
     mock and the canned offline advisory are deleted; CEOChat renders a per-message provenanceBadge
     and a pill that reads from the last answer's provenance (never a hard-wired state). Guard:
     test_w451_ceo_chat_runs_on_the_owned_fabric_both_ways (floor → native; the owned model
     substituted at the one factored seam → named; gateway.stream unchanged for its three older
     consumers); probe scripts/_w451_probe.mjs. The 'no [Offline Mode] text anywhere' acceptance is
     met in code (agentic_core + the SPA); the docs keep the string as the record of what was wrong.
     The text below is that record.]
     THE DEFAULT TAB OF THE LIVING ORGANISATION HUB WAS A DETACHED ROLEPLAY. /api/v138/ceo/chat
     opens its own httpx stream to Ollama (hard-coded llama3.2, "AI CEO of the Galactic Era",
     invented constitutional articles), ignores AI_DISABLE_LOCAL, guardrails, the breaker, tenant
     memory and provenance; registers a lambda and narrates "tool_87f3 has been successfully
     integrated"; when Ollama is down streams a canned "[Offline Mode] … sovereign mesh advisory"
     char-by-char while the header pill stays "Planetary Strategy Active". [R3.0, R4.0]  DONE WHEN
     the chat runs through gateway/orchestrator with served_by per message (amber on the floor),
     the persona, fake tool registration and canned advisory are deleted, and the pill reads from
     provenance.
 1.4 [CLOSED W452 — one shared guard (vsb._refuse_gated / _gates_blocking / _gate_block_reason);
     ship, evolve, evolution/apply, the repo cascade, the org cascade scoped to a VSB, the entity's
     fabric swarm run, plan orchestrate and the birth-ship all consult it; a PENDING or REJECTED
     gate → 409 {gate, status, blocks_progress, blocking, clear_by}; gates can be set at birth
     (EstablishRequest/JourneyRequest.review_gates, validated) and hold the birth-ship with the gate
     named; the heartbeat's autonomous evolve/re-ship HOLD a gated entity with a recorded action;
     the Genesis panel says what a gate does; the Cockpit renders the refusal legibly. Guard:
     test_w452_mode3_review_gates_gate_every_lifecycle_mover_both_ways; probe
     scripts/_w452_probe.mjs. The text below is the record of what was wrong.]
     MODE 3 REVIEW GATES GATED NOTHING. review_gates/blocks_progress were read by their own four
     endpoints only; a REJECTED design gate did not stop orchestrate, cascade, evolve or ship; the
     Genesis panel says nothing about advisory, and vision §17.4 said ✅ DELIVERED at the audit
     baseline (corrected to ◐ in W446). [R3.1, R2.2]  DONE WHEN every lifecycle mover
     consults the gate and a blocking gate returns 409 with the gate status, proven both ways.
 1.5 [CLOSED W453 — every badge site renders the helper's cls/title; a second helper
     (provenanceMapBadge) for provenance count maps replaces every inline 'in-house / external used'
     chip (all-floor → amber floor label; any external → amber 'via'; else emerald with the models
     named); MyWork, Generator, OrganismAnatomy, QEPIntelligence, NativeAI (tree runs, resource cards,
     step icons), VSBSpawnStudio, BoardOfDirectors, SwarmIntelligence, ReactorStudio, ResourceFabric
     migrated; the Cockpit's W450 plan-tab badge uses the map helper too. Guard:
     test_w453_every_provenance_badge_routes_through_the_helper (fails on `.label` without `.cls`, on
     any colour ternary over is_external/any_external/served_by==='native', and on fewer than 16 helper
     users); probe scripts/_w453_probe.mjs. The text below is the record of what was wrong.]
     TEN BADGE SITES PAINTED THE FLOOR GREEN. provenanceBadge() returns amber + "structured floor —
     not model analysis"; seven sites take .label and colour by is_external (incl. the Law hub's
     default tab and the avatar footer on every page), MyWork renders "in-house" emerald with no
     floor label, Generator and OrganismAnatomy chip it green; BoardOfDirectors and
     SwarmIntelligence inline their own green chips. [R5.1, R3.4, R3.7]  DONE WHEN every site uses
     the helper's .cls/.title and a guard fails on `.label` used without `.cls`.
 1.6 [CLOSED W454 — the hub opens on the CV tools; the job-search route synthesises ILLUSTRATIVE
     example listings (no url, no posting date, salary labelled an estimate, illustrative=True and a
     basis sentence on every row, sources_used EMPTY — synthesis is not a source, provenance on the
     response); the Application Studio says 'AI-synthesised example listings — not a live job board',
     keys listings by id, links nothing, badges the search and every generated document. Guard:
     test_w454_employment_default_tab_is_honest; probe scripts/_w454_probe.mjs. The text below is the
     record of what was wrong.]
     THE EMPLOYMENT HUB'S DEFAULT TAB PROMISED "LIVE, REAL-TIME SEARCH ACROSS PUBLIC JOB BOARDS"
     over a route whose docstring says "not a live job board" and whose prompt fabricates
     url/salary/published; generated documents render with no provenance. [R5.0]
 1.7 [CLOSED W455 — the constitutional row says what it can check: content → gaas.v5's output
     screen runs (fail on an unsafe pattern) and the row is 'not_checked — not applicable to content;
     gaas.v5 gates agent actions'; an action kind → the action gate; an engine raise → 'error', never
     a pass. The UK-Legal audit hash is SHA3-512 over the subject (three subjects, three hashes). A
     subject outside every vocabulary is 'review — no engine covers this area' (coverage recorded per
     row), never a pass; halal vocabulary passes the screen, labelled 'not a certification'. The
     Frameworks card labels each check by what it does. A FAIL deliverable carries 'COMPLIANCE
     VERDICT: FAIL … NOT cleared for use' with its Change-Control id on page one of every export
     (md/txt/html/slides/pdf/docx/pptx/svg/png via the shared subtitle; a compliance_stamp key in
     json), on the list row, and on the download button. Candidate scoring treats a no-coverage
     review as neutral. Guard: test_w455_compliance_reads_what_it_can_and_says_what_it_cannot; probe
     scripts/_w455_probe.mjs. The text below is the record of what was wrong.]
     THE CONSTITUTIONAL COMPLIANCE ROW COULD NOT READ CONTENT — validate(kind, …) never consulted the
     subject; every content check is green "Constitutional gate clear"; the router's bare except
     leaves a pass on engine failure; a compliance FAIL on a deliverable routes to the CCA and the
     artifact still exports clean. And the "UK Legal (London)" engine is eight employment-law terms
     (Equality Act 2010 / ERA 1996 / ACAS) whose audit hash is identical for a halal bakery and a
     laundering scheme (it hashes the empty flag set, not the subject); "Sharia/Halal" is a
     substring loop; the Frameworks card presents them as engine-grade coverage. [R1.1, R1.3, R1.6]
 1.8 [CLOSED W456 — on the floor the Transliteration and Translation sections are withheld from
     the prompt AND cut from the text (named in sections_withheld) with a floor_note that says why;
     a disclaimer key on every tafsir response; the Tafsir tab renders the sourced Arabic (rtl, lang=ar),
     its source line, the reference, the range note and the floor note through DomainTool's new
     renderExtra; the QMS chip follows P1.1. Guard: test_w456_tafsir_tab_completes_section_11_both_ways;
     probe scripts/_w456_probe.mjs. The text below is the record of what was wrong.]
     THE TAFSIR TAB SERVED A FLOOR "TRANSLATION" SECTION — rule 4 of §11 applied to
     /qep/translation (503) and not to /religion/quran-tafsir; the sourced Arabic, range cap and
     scholar-referral never reach the screen (no disclaimer key; DomainTool renders resultKey +
     disclaimer only); a green QMS chip beside a "review" verdict. [R1.0]
 1.9 [CLOSED W457 — agentic_core/care/scoring.py computes NEWS2 (RCP 2017, scales 1 and 2), MUST
     (BAPEN) and Waterlow in-house from the published tables and counts NICE CG161 falls factors
     (labelled a count, not a score); inputs validated for units, ranges and completeness — a missing
     observation is named and the total is a lower bound, never filled; the route returns the `score`
     block first and hands it to the AI with 'do NOT recompute'; the Care hub renders the block above
     the narrative; the copy says what is computed. Guard: test_w457_care_scoring_computes_both_ways
     (the assessor's case → NEWS2 6 · medium, key threshold for urgent response; table tests); probe
     scripts/_w457_probe.mjs. The text below is the record of what was wrong.]
     CARE'S "VALIDATED RISK SCORING" COMPUTED NOTHING — NEWS2/MUST/Waterlow are published tables
     and no arithmetic exists; the assessor's observations (NEWS2 = 6, urgent band) returned no
     score under a green pass. [R5.3]
 1.10 [CLOSED W458 — a resource that was never ATTEMPTED is a skip, not a failure: _run_model raises
      ResourceSkipped under AI_DISABLE_LOCAL (and for an unknown resource, and on a spend-policy
      refusal), complete() annotates resources_tried 'ollama (disabled by config, skipped)' and records
      NOTHING — no learning-loop row, no immune threat, no breaker failure; the native floor serve IS
      recorded; /native-ai/status follows operational_excellence.last_successful_server() (the most
      recent SUCCESSFUL row) and names the row it read, with the failed attempts since; the
      deprioritise badge follows the router's own rule. Guard:
      test_w458_disabled_is_not_failed_and_status_follows_success (both ways — a disabled resource
      changes nothing AND a real failure still records all three); probe scripts/_w458_probe.mjs.
      The text below is the record of what was wrong.]
      /native-ai/status REPORTED mode='real_model' WHILE THE FLOOR SERVED EVERYTHING — the most
     recent model_health row is taken without checking success, and a config-DISABLED local
     model is recorded as a FAILURE (immune health dropped to 0.8 from one API call; the learning
     loop would deprioritise a healthy model on a flag). [R4.7, R4.8]
 1.11 [CLOSED W459 — the Change Control Agency reads an identity: the HTTP routes take the principal
      (auth ON: the authenticated username is stamped and a different claimed name is kept only as
      submitted_by_claimed; auth OFF: the caller's name is kept, by_verified false, never a
      fabricated 'admin'); an override is authorised before anything is written — admin only under
      auth, and a CRITICAL change additionally needs an explicit admin_decision_for_critical in BOTH
      modes; override_decision accepts only approved/rejected; every decision records who asked
      (by, by_verified) and what decided (decided_by); a CRITICAL change is NEVER decided by a review
      (a model marker is only a recommendation — it is held for an explicit admin decision); a review
      with no model marker says the organism-health threshold rule decided it, and with auth ON that
      rule verdict is applied only for an admin requester; with auth ON a governed live lever or a
      config reset is implemented only by an admin; the §17.5 fallback says 'no twin model — health
      gate only'; every read-modify-write of a change record is a compare-and-set under the record's
      lock (also the economy consume/restore, and the VSB evolution apply, which claims the approval
      before mutating the genome); ids are validated before the store is touched; requires_ratification
      deleted; the docstring rewritten to what the code does. Guards:
      test_w459_cca_identity_and_override_gate_both_ways, test_w459_cca_decisions_are_serialised,
      test_w459_external_cca_writers_compare_and_set; probe scripts/_w459_probe.mjs. W463 then bound
      what an economy approval releases (register FU-002 — see P1.11). The text below is the record of
      what was wrong.]
      CHANGE CONTROL'S TIERS WERE PROSE — no auth dependency; submitted_by is free text; override
     honoured for CRITICAL; the floor "AI review" is a health-threshold rule; twin pre-validation
     falls to health_gate_default; a human override is attributed to 'cca_ai'. [R3.2, R6.2]
 1.12 [CLOSED W460 — retired, not wired: the canvas and its Agent Forge copy are deleted, both of their
      routes land on the real /native-ai cascade designer (outside the status block, so a failed status
      call cannot hide it; define and edit refuse a cascade with no complete stage), and the 'GaaS
      COMPLIANT' badge went with every other unevaluated compliance claim the audit found in src/ — a
      conformance line, a veto window and privacy budget that exist nowhere, an always-valid client
      validator, a model-invented alignment score, a green NOMINAL on a failed poll, a spawn gate recorded
      as PASSED when it never ran, an establish gate recording alignment it never read, and a Governance
      Hub that painted a policy halt green. Guard: test_w460_compliance_badges_are_evaluated_or_absent;
      probe scripts/_w460_probe.mjs. The text below is the record of what was wrong.]
      THE VISUAL COMPOSER TAB WAS A DISCONNECTED CANVAS with fictional model names and a hard-coded
     green "GaaS COMPLIANT" badge; nothing reaches swarm/define. [R4.3]  Retirement is on the
     table: the real designer lives on /native-ai and /resource-fabric.
 1.13 THE MARKETPLACE HEADER COUNTS 20 DIRECTORIES AS "LIVE PRODUCTS" — 11 with no route; six
     "Domain Signature" literals whose only substance is a legacy manifest self-declaring
     PRODUCTION_READY / WCAG 2.2 AAA / MP4. [R5.6]  And five non-Religion hubs keep a "QEP
     Flagship" tab that is not QEP (NOT_WIRED on click) contrary to the directive; tool counts
     disagree three ways (23 / 18 / 24 mounted). [R5.8]
 1.14 THE BOARD PACK CERTIFIES A CONTENTLESS NARRATIVE — required sections are found in the
     preamble the handler itself wrote; three "assembled fresh" packs carry one byte-identical
     DCS hash; the Chief's Opening stores prompt-echo, drops the floor prefix, and has no owner-
     edit surface. [R3.6, R3.5, R3.3]  [PARTLY CLOSED — on the floor the pack's QMS gate is 'not
     assessable' (W449) and its narrative 'narrative pending the owned model' (W450); what remains,
     and what the content hash in the seal does and does not cover, is recorded under P1.14.]

TIER 2 — REACH AND INVISIBLE SHORTFALLS
 2.1 FLOOR CASCADES GROUND STAGES 2+ IN THE ENGINE'S OWN MARKER TEXT ("external dependency ·
     structured engine"); BDP 8/8 stages never mention the challenge; a literal "\n" in the
     orchestrator's f-string; gateway recall injects earlier floor output into unrelated calls;
     and inside the journey the two helpers that bypass the problem prefix (_ai_cognitive_prime,
     _ai_mjm_lifecycle) let the engine describe itself — 'architecture specialised · cognitive
     architecture' — while engines_used is a constant list, not provenance. [R4.1, R2.7]
 2.2 PROVENANCE STOPS AT THE API BOUNDARY for 47 gateway.query() sites (46 since W450 moved the Spawn
     Studio's CEO specification to query_meta; 44 of them under agentic_core/api, the scope of P2.2's
     guard) and R4.2's seven output
     pages (Intelligence Lab, Forge, Synthesis Studio/Nexus, BTO, Sovereign Evolution, Organism
     Dashboard) — plus the Business Plan's Chief's Opening card (R3.3). [R4.2, R4.9, R3.3]
 2.3 THE AVATAR ANSWERS ITS OWN PERSONA LINE under the floor; the user's language preference is
     returned null and never shown; /status pings Ollama regardless of the disable flag; the
     profile's profile_applied flag is dropped on the ai_text / _ai_provenance path every domain tool
     takes, so the W428 profile is stored, shown and inert with no signal (W451 carries profile_applied
     in the terminal SSE frame of the CEO chat and the v310 business-plan, projects and synthesis
     streams — backend only; no page renders it). [R5.4, R5.7]
 2.4 THE ORGANISM DEFENDS ON PAPER: reflex arcs registered = 0 (register_reflex has no caller —
     "reflex: 542" in the payload is a signal CATEGORY); immune-reconfigure has no caller; the
     survival instinct keys off an ATP simulator that cannot fall below its threshold; Cardio-
     vascular is CPU-idle relabelled and Endocrine an unimported PID file, while the W434 note
     vouching for them travels in every quality record; torch optionality fails at import;
     living-VSB compliance rows read keys the screen never writes; the user_projects waterfall
     stage leaves the investor's books and reaches no investee; requirements.txt and pyproject
     pin torch as a HARD dependency while §17.5 calls it optional. [R4.5, R4.6, R6.1, R6.3, R6.4,
     R6.5, R6.8 — all stood under refutation.]
 2.5 THE GaaS GATE COVERS 8 OF 57 API MODULES; the gateway every other output takes runs a
     three-regex keyword filter that blocks "exploit the market opportunity" — observed LIVE by
     R6.0's refuter: POST /api/ai/query → "[POLICY VIOLATION]". [R6.0]
 2.6 THE CONTROL PERIMETER HAS NO AUTH — heartbeat, genome, organism-status, sovereign-evolution,
     board, CCA, business-plan, swarm, studio: any caller under auth could stop the heart or run
     economy cycles across every tenant. [R6.2, R3.2]  [PARTLY CLOSED — the CCA's write routes read an
     identity since W459 (retiring an economy record admin-only under auth since W463); its read routes
     (no auth dependency at all) and every
     other router here stay open — P2.6.]
 2.7 "BESPOKE PER SOLUTION" IS ONE FIXED 4-STAGE TEMPLATE per VSB; the tree's planner flag
     ('deterministic_template') is never rendered under copy saying "autonomously decomposes";
     the Forge UI exposes neither per-stage config nor Rerun although the API accepts both
     (POST /api/v1/forge/runs/{id}/rerun exists; per-stage config is honoured) — UI wiring, not
     backend work. [R4.4]
 2.8 THE 67-OP SCATTER (38 clusters) — audit-before-wire, retirement equal. [no ledger entry — the
     instrument is scripts/reach_audit.py, run fresh]
 2.9 REALM DRIFT: configs/realms.yaml orphaned; sovereign_config.yaml points at a file that does
     not exist; hub CTAs post domains as realms; DomainTool never sends a realm. [R5.5]

TIER 3 — CAPABILITY GAPS
 3.1 §4.6 DEVELOP — no stage between design and operations produces a checkable artefact with a
     real pass/fail (v2 §4.6 MISSING, unrefuted then; v3 R2.3 re-observed the journey's stage list
     'minus §4.6 Develop — nothing builds the user's solution'). [R2.3]
 3.2 §4.1 IMAGE INTAKE — the Describe field accepts text/voice/text-PDF only; image reaches only the
     Cockpit 'Converse' tab. [R2.8]
 3.3 §17.3 STRATEGIC + ACTION-PLAN CADENCE LAYERS — nothing refreshes them quarterly/weekly/on
     signal; the board pack labels pre-existing fields as layers and a constant values string.
     [R3.5]  (The ≤5-min staleness invariant IS met by read-time derivation — a wording overclaim.)
 3.4 §17.4 MODE 2 — no expert digital-twin human node exists; the Chief is a values sentence plus
     the last five instructions, invoked only by click. [R3.8, R3.4]
 3.5 §17.1 PRODUCTS AXIS — no PRODUCTS constant, no laboratory route, no 96-cell surface. [R5.5]
     OWNER RULING: build or amend.
 3.6 §17.5 KPI GATE — nothing gates delivery on KPIs. [R6.6]  OWNER RULING: build or amend.
 3.7 §4.10 AUTONOMY — every autonomy flag OFF by default and persisted OFF; /establish does not
     switch tending on, yet its API response says "the organism tends this VSB on the circadian
     heartbeat" (untrue while auto_economy is OFF — the SSE birth log announces it too); genome
     generation 0; §11's "continuously monitored" compliance is the same OFF switch (auto_compliance
     false, last_compliance null after 48 beats; deliverables and domain outputs are screened ONCE
     at production and never again, and nothing on Deliverables says so). [R6.7, R2.4, R1.5]
 3.8 §9 DEPTH — i18n chrome only on three pages; AI output English; profile inert on the floor. [R5.7]
 3.9 §13 — no repo file/zip endpoint or clickable tree; the entity's products not listed (v2 §13
     finding, not re-assessed in v3). [R2.6 — its regression half CLOSED W450 with P1.2: /repo no longer
     overwrites a generated website/webapp/mobile surface, labels integrated_surfaces by what is on
     disk, and a rename marks a shipped body stale; the file/zip endpoint and clickable tree remain — P3.7]
 3.10 §4 · §17.1 — THERE IS NO SINGLE LIFECYCLE (OWNER RULING, unchanged from v11 rev 1): eight
     vocabularies; 219 of 219 VSBs at "commercialise" and never advanced — 218 born from the
     genesis.py:687/:852 literals, one via vsb.py's spawn path (`stage: req.scope`; re-counted
     2026-09-05); options (A) canon five become the one gated
     lifecycle, (B) correct the canon, (C) NARROW — make VSB stage advance or rename it (the
     recommendation). (C)'s VSB half is a Tier-1 truth defect in a Tier-3 costume. [R2.3 — two entry
     pipelines, four stage vocabularies, neither gated; a Spawn-Studio entity persists stage 'build'
     beside journey-born ones at 'commercialise']

 3.11 §10 NAMES SIXTEEN CRITERIA; INSTRUMENTS EXIST FOR FOUR — best-in-class, innovative, effective,
     efficient, commercially viable, optimised, tested, validated have no instrument anywhere; and
     Genesis ATTESTS 'modelled · simulated · ranked' as met (source 'caller', sealed into the QMS
     record and the shipped EVIDENCE.md) on runs whose own payload says the three candidates were
     byte-identical and the ranking was a tie resolved by list order. The page discloses the tie
     and the record's basis string carries it — but the record COUNTS ranked/simulated/modelled
     as met:true beside that basis, and the shipped EVIDENCE.md has no tie note. [R1.4, R2.5]
     TWO HALVES: the attestation half is Tier 1 and
     rides with P1.1 (never attest ranked/simulated on a tie or identical candidates; EVIDENCE.md
     carries the tie note); the wording half is an OWNER RULING (P3.0) — build instruments for at
     least the commercial trio (effective · efficient · commercially viable, e.g. from the BMS
     unit-economics estimate) or amend §10 to 'measured where an in-house instrument exists; the
     record names what was not'. [attestation half CLOSED W449 — Genesis WITHHOLDS modelled / simulated /
     ranked / optimised on a tie or identical candidates with the reason, and EVIDENCE.md carries the
     tie note (test_w449_bar_attestations_withheld_on_tie_both_ways); the wording half stays P3.0.]

OWNER-GATED, NOT GAPS: real-money rails, live Stripe (the exposed key is redacted from the tree
but STILL IN GIT HISTORY — rotation at Stripe is an Owner action still owed), managed Postgres,
production deploy, a live external AI key, and flipping AUTH_ENABLED / SELF_SERVE_SIGNUP /
AI_ALLOW_EXTERNAL / REAL_MONEY_ENABLED.

RECORDED, LATENT — NATIVE_PRIMITIVE_DEFECT_LEDGER.md: four unreached fabricating functions
(GenomeEvolutionEngine.run_evolution_cycle, TopologyDefense.simplicial_repair,
AccuracyValidator.get_aggregate_accuracy, network/planetary.py) and two formerly DORMANT ON REACHED CCA
ROUTES, both CLOSED W459 with P1.11 (the read-modify-write race: every change-record mutation is now a
compare-and-set under the record's lock; requires_ratification: deleted — and W464 built the Board
ratification queue the Owner ruled for, FU-012). Also standing: 162 test-owned entities (the Owner's call).
</ledger>

<delivery_plan>
THE PLAN TO DELIVER THE WHOLE VISION (§1–§15) TO COMPLETION — reasoned, ordered, verifiable.

DEFINITION OF COMPLETE. Every claim in WORKSTATION_IDBO_WHOLE_VISION.md §1–§15 is either
  (a) DELIVERED — verified by EXECUTION on a fresh HEAD boot and survived adversarial refutation, or
  (b) a DISCLOSED BOUNDARY the Owner has ratified in §18 (an honest "not yet" stated at the surface
      where a user meets it, and in the canon),
and the six-region fidelity assessment (scripts/workflows/fidelity_audit_v3.js, the same instrument
as v3) returns ZERO STUB / MISSING / DOC_OVERCLAIM, with every PARTIAL disclosed at its surface.
Complete is a MEASUREMENT, taken at milestones — never a declaration. §6 was declared complete
five times.

HOW EVERY WORKSTREAM IS VERIFIED (the rhythm, made specific — no item closes without all six):
  V1 EXECUTE — the acceptance criterion is exercised against a FRESH backend on a fresh port, by
     the committed probe pattern (scripts/_wNNN_probe.mjs: dismissTour, lowercased body, wait for
     the SPECIFIC outcome element, computed PASS/FAIL).
  V2 GUARD — a test in integration_tests/test_mvp_spine.py that was BROKEN and watched fail with
     the original symptom, then restored; a smoke needle where a user surface changed.
  V3 REFUTE — adversarial agents on the round's own diff, told to default to "it breaks";
     consumers of every changed field grepped repo-wide including tests and .mjs.
  V4 SUITE — the full suite on the FINAL tree (kill + rerun if the tree moves).
  V5 MEASURE — reach_audit fresh; for P1/P2 items, the affected ledger entry re-assessed by
     execution (not by reading the diff).
  V6 RECORD — AUTONOMOUS_PROGRESS.md entry; commit message stating what was WRONG; CI green;
     memory. At each phase boundary, the whole fidelity workflow re-runs and the ledger re-issues.
     Every task the round FOUND and did not do becomes a row in docs/FOLLOWUPS.json in the same
     commit (python scripts/followups.py add, which routes it to the plan item that owns its area; a high one
     rides the next open item; NEXT is retired, W469) — never only a chat chip, a commit message or a
     'NOT DONE' paragraph. Mark a finished item with python scripts/followups.py done P1.13 --by W### — it
     writes the marker, moves the item's remaining rows along the routes (--reroute), hands its routes on
     (--hand-to) and re-renders PLAN NOW; the suite fails on a row left on an item marked DONE (the marker
     is exactly '✅ DONE W###' right after the item id — an item line that says done in any other form or
     place fails too), on a route pointing at a finished item, on a row slotted NEXT, on owner-gated work
     slotted anywhere but OWNER, on an open row naming a file that is not in the working tree or not
     tracked by git (W462), and on either generated block edited by hand.

ORDER AND DEPENDENCIES. P1 first, in the order given — 1.1 is a class-kill that 1.2, 1.14 and
half of P2 depend on; 1.3 and 1.5 are where users land. P2 follows (P2.1 unblocks the honest
content that P3 builds on). P3 items marked OWNER RULING are put to the Owner with evidence at
the START of P3 so rulings arrive while the unambiguous P3 items are built. P4 is the Owner's hand.

WHERE THE PLAN STANDS (updated W479, 2026-09-20 — every round that closes an item or runs between
items updates this block in the same commit. PLAN NOW, below, is generated from the plan's items and the
register and checked by the suite (W469); the DONE lines are history, kept true by hand. Never start a line
here with one space and an item id — that is read as a plan item and fails the suite).
  DONE — P1.1 to P1.17, in order, W449–W460 and W470–W475 (MILESTONE M1 ran W474, found fourteen, and P1.17 closed
    them W475; the re-run, W476, found twenty-seven more and added P1.18); P1 closes when an M1 re-run measures 0: each is
    marked below with what it DELIVERED; P1.1–P1.5, P1.7, P1.8, P1.11–P1.16 also say what they did NOT close (P1.6, P1.9 and P1.10 name no
    leftover). Only P1.11's and P1.12's leftovers were back-filled into the register (FU-005…FU-014);
    since W462 (V6) a round registers what it leaves in the same commit.
  DONE BETWEEN ITEMS — rounds the plan did not list, recorded here so the plan reads whole:
    W461  transformation stage verification made honest, split out of the P1.12 audit (register
          FU-001): a stage that checks nothing is 'not assessable', and only an allowed gate validates
          a run or moves a living-plan objective. (P2.8's clause about the realisation engine —
          agentic_core/api/transformation.py measuring delivery, not route existence — is a different
          engine and stays open.)
    W462  the follow-up register: docs/FOLLOWUPS.json + scripts/followups.py, the schedule rendered
          below, V6's same-commit rule; the suite fails when an item marked ✅ DONE still carries an open row.
    W463  register FU-002 and its class: the economy's materiality approvals release only what they
          were filed for — P1.11's Change Control work carried into the economy's own holds (see the
          note under P1.11); FU-015…FU-024 registered; the documentation swept after the push.
    W464  the register's four OWNER rows, on the Owner's rulings of 2026-09-14 (answers F): FU-012
          Board ratification of HIGH changes a review approved; FU-013 Change Control decisions on the
          UEG; FU-014 economy_material CRITICAL and code_change HIGH, the gate releasing only the Owner's
          approval; FU-020 genome_engine.py fixed and kept. P1.11's NOT DONE (b), (c) and (d) are closed by
          it (see P1.11). FU-025…FU-033 registered.
    W465  the register's NEXT rows FU-015, FU-016 and FU-024 (virtual WST): a service contract is settled
          once — a claim under a persisted transfer id, a crash's retry completing a posted debit rather than
          paying again, every contract change re-read inside the store lock — and an unpaid settlement is
          recorded as what it was (held, rejected, blocked, gate error); the owner-payments store is locked
          and atomic, and it and the pending-transfers queue are refused when unreadable, never read as
          empty, and every record in that queue is shape-checked before any debit (closing FU-038, which the
          round registered and its fifth refutation fixed); a failed owner accrual is reported. FU-034…FU-046
          registered (FU-041…FU-046 by the audit that prepared FU-022 and FU-023; FU-046 — a W465 regression — closed
          in the same round).
    W466  the register's NEXT row FU-023 (virtual WST): a debit now carries its transfer and an open receiver
          leg, closed once the receiver's queue holds the id; a stranded transfer (the sender debited, the
          receiver never credited) is found and completed once — by a replay that can never debit — from the
          page's Complete button, the reconcile route, or the heartbeat while autonomous economy is on; every
          failed transfer is answered from the sender's ledger and the receiver's queue, naming the id, and a
          sender ledger that cannot be read whole posts nothing. Debits made before W466 are never completed
          (FU-047 registered).
    W467  the register's NEXT rows FU-022, FU-043 and FU-044 (virtual WST): the heartbeat's governed cycle
          consumes its recognised revenue events under a token BEFORE it runs (they used to be consumed after
          the ledger had posted, so a failed consume distributed them twice); a cycle that raises before its
          first ledger write gives back its events, the receipts and returns it drained, and the Owner's
          approval, and one that wrote anything keeps them consumed and the approval spent; the API cycle
          counts as run only once it writes, too. The revenue store is read strictly (refused, never
          overwritten), its cap keeps pending and in-flight events, and a consume whose process stopped is
          given back by the stranded-consume pass. FU-048 registered.
    W468  the register's NEXT row FU-041 (virtual WST): a VSB ledger is read strictly, one reader for every
          module. A file that cannot be read whole is refused (LedgerUnavailable), never answered with empty
          books or a valid prefix, and every write re-reads it under the lock and saves nothing. The writer
          keeps the reader's shape (an overflowing posting is refused). Cycles are refused before any gate
          (API 503/409, heartbeat ledger_unavailable, said once per outage on the UEG); the close, ledger and
          board-pack routes answer 503, a transfer from an unreadable sender 503 with nothing debited. A
          heartbeat visit that raises advances the rotation and says so, and the roster's hold follows what
          is still true. Both economy pages show the server's reason. Eight refutation passes; FU-049 to
          FU-066 registered (18).
    W469  the Owner's instruction (2026-09-17): the register's NEXT slot is retired — its forty-two rows
          now ride the plan items that own their areas (three added: P1.15 stores that refuse, P1.16 canon and
          suite hygiene, P2.9 the economy's flows); ROUTES in the register send each new row to its item (a high
          one to the next open item); PLAN NOW above is generated into both plan docs, served live by
          /api/v1/plan/followups and shown on /transformation, refreshed every minute; followups.py done marks
          an item and moves its rows and routes on. Two refutation passes; FU-067 to FU-070 registered.
    W478  the Owner's instruction (2026-09-19): a PRIORITISATION mechanism in the planning system that ties
          each follow-up's significance to vision delivery and weights completion by it. A row's priority is
          a product of named parts — vision area (the section its title cites, else its primary file, else a
          title word) × truth tier × reach × criticality × breadth × effort — from the Owner's weights in
          docs/PRIORITY.json (agentic_core/plan_priority.py); inside an item rows run highest-priority first
          (the plan's order and phase gates stand); PLAN NOW names the top rows and the follow-up completion
          weighted by priority; followups.py priority shows every score's parts. Two refutation passes.
<!-- plannow:begin (generated by scripts/followups.py render - never edit by hand) -->
PLAN NOW — generated from the delivery plan's items and docs/FOLLOWUPS.json by scripts/followups.py on
every register change (add · close · drop · reslot · route · done · render); never edit between the markers.
  Next: P1.18 The third truth pass — 61 follow-ups ride it.
  Then, in order (the follow-ups riding each): P2.1 0 · P2.2 0 · P2.3 1 · P2.4 41 · P2.5 0 · P2.6 15 · P2.7 3 ·
    P2.8 9 · P2.9 34 · P3.0 0 · P3.1 0 · P3.2 0 · P3.3 0 · P3.4 0 · P3.5 0 · P3.6 0 · P3.7 0 · P3.8 0 ·
    P3.9 0 · P3.10 0 · P3.11 0 · P3.12 4 · P3.13 0 · P3.14 1 · P3.15 1 · P3.16 1 · P4.1 0 · P4.2 0 · P4.3 0 ·
    P4.4 0 · P4.5 0 · P4.6 0
  Highest priority in P1.18 (score · area): FU-122 102.0 organisation · FU-094 100.0 compliance ·
    FU-096 100.0 faith · FU-105 100.0 compliance · FU-115 100.0 compliance
  Done: 17 of 50 items — P1 17/18 · P2 0/9 · P3 0/17 · P4 0/6.
  Follow-up completion weighted by priority — P1: 25.2% of its rows' priority closed (40 of 101 rows); every phase's rows: 17.4% (the retired pre-plan queue left out).
  Follow-ups: 171 open — 171 ride a plan item (61 high), 0 unscheduled, 0 awaiting the Owner; 57 done, 2 dropped.
<!-- plannow:end -->
  WAITING ON THE OWNER — no register row (the ones above STILL WITH THE OWNER in the answers are plan
    rulings, not register rows).

<!-- followups:begin (generated by scripts/followups.py render - never edit by hand) -->
SCHEDULED FOLLOW-UPS — every task a round finds and does not do is a row in docs/FOLLOWUPS.json, added in
the same commit (python scripts/followups.py add routes it to the plan item that owns its area; a high one
rides the next open item) or slotted OWNER (waits on an Owner decision; never scheduled). A round that
finishes an item marks it with python scripts/followups.py done P1.13 --by W### — its rows move along the
routes or are closed first; the suite fails on a row left on a finished item.
Open 171 (171 scheduled, 61 high · 0 unscheduled · 0 awaiting the Owner) · done 57 · dropped 2.
  P1.18 — The third truth pass
    FU-122 [high] [p 102.0] sweep transformation_orchestration.py: 5 Tier-1 truth defects (C3,C8) — 'Cascade (8 stages · 6/6 assessable verified · validated)', with an emerald ShieldCheck… — S1.0 C8: 'Cascade (8 stages · 6/6 assessable verified · validated)', with an emerald ShieldCheck on Chief, Board,… → Each 'verified' is an existence check that cannot fail on a normal entity. Stage 1 checks bool(board.chief), and board_for_owner…; S2.1 C8: '6/6 assessable · gov allowed · twin stable-and-improving' with an emerald 'VALIDATED' chip. The run also… → None of the six 'assessable' checks can fail on a fresh entity. (1) The Chief is resolved: board_for_owner always returns one.…; S2.2 C3: 'twin stable-and-improving', shown as the result of 'run a transformation simulation' over a '90 days'… → No simulation runs. projected = real × (0.5 + 0.5 × immune_health), and the verdict is 'stable-and-improving' iff projected ≥…; S6.0 C8: Green 'VALIDATED' chip plus the report line 'End-to-end transformation cascade ran From Chief To… → None of the 5 'assessable' checks looks at transformation delivery. Each one only checks that something exists: stage 1 checks a…; S6.1 C3: Twin sim: 'stable-and-improving' (and simulation.projected_realisation for a '90 days' horizon) → No simulation runs. projected = min(1, real*(0.5+0.5*health)) with health<=1, so projected can never exceed the current figure… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-094 [high] [p 100.0] v5 R1.0: §11 live compliance (ethical engine) → §10 'safe' / deliverable… — The 'ethical engine' is a bare-word regex (agentic_core/compliance/ethical_engine.py:25-27 _HARM_SEVERE =… — The 'ethical engine' is a bare-word regex (agentic_core/compliance/ethical_engine.py:25-27 _HARM_SEVERE = kill|murder|...|suicide). Any subject that contains one of those words gets 'human: fail — Severe human-harm indicator', which makes the overall verdict FAIL, even when the subject is a helpful service. The FAIL is then stamped as a real safety judgement: §10 'safe' is recorded met=False, measured=True, source=gate. On material labels the delivery is routed to Change Control (Change Control Agency, CCA) as a compliance violation, and the export's page one reads 'NOT cleared for use'. FIX (the assessor's proposal, a lead): A single harm-vocabulary hit should give 'review' with the matched term named, never 'fail'. Only an ethical row whose coverage is 'engine' should set §10 'safe' as measured. Keyword-only safety evidence should be recorded as source 'screen' with met=None. [docs/VISION_FIDELITY_LEDGER.md v5 R1.0, standing STUB, refutation survived] (found W476 ledger v5)
    FU-096 [high] [p 100.0] v5 R1.2: §11.2 faith-content constitution — sourced-only, exactly (QEP… — The quran-uthmani edition prepends the Basmala to ayah 1 of every surah except 1 and 9. The platform passes… — The quran-uthmani edition prepends the Basmala to ayah 1 of every surah except 1 and 9. The platform passes this through unmodified (religious_domain/api.py:249-262 fetch_ayah_arabic, :318-324 get_surah, :366-373 get_ayah) and labels it 'Authentic Arabic text… not AI-generated'. As a result, 112 surahs show a first ayah that is not the text of that ayah under Hafs numbering. It also breaks written recall. Ayah 1:1 carries a leading U+FEFF (BOM) as well. FIX (the assessor's proposal, a lead): For surahs other than 1 and 9, strip the leading Basmala from ayah 1 (or request an edition that does not prepend it) and strip U+FEFF. Show the Basmala separately as a header labelled 'not part of ayah 1'. Add a test for 112:1, 2:1 and 1:1. [docs/VISION_FIDELITY_LEDGER.md v5 R1.2, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-105 [high] [p 100.0] v5 R3.3: §5 org cascade → §10 quality bar (compliant / safe criteria) — The §10 bar records 'compliant' and 'safe' as MET and MEASURED by the gate whenever no §11 screen says… — The §10 bar records 'compliant' and 'safe' as MET and MEASURED by the gate whenever no §11 screen says 'fail'. A run where sharia_halal, ethical and uk_legal all returned 'review' (no engine covers them) is therefore certified compliant and safe. FIX (the assessor's proposal, a lead): met = True only when every framework in scope is 'pass'; any 'review' gives met:null with basis 'review — not assessed'. [docs/VISION_FIDELITY_LEDGER.md v5 R3.3, standing STUB, refutation survived] (found W476 ledger v5)
    FU-115 [high] [p 100.0] v5 R5.2: §3A Domain Working (Religion — Halal pre-assessment) / §11… — POST /api/v1/religion/halal-review {product_name:'Choco bar', ingredients:['sugar','cocoa… — POST /api/v1/religion/halal-review {product_name:'Choco bar', ingredients:['sugar','cocoa butter','gelatin','E471']}. The floor-served 'assessment' repeats the heading '## Halal Status Assessment (COMPLIANT /' five times: it is the prompt's '(COMPLIANT / REQUIRES REVIEW / NON-COMPLIANT)' enum cut short, so it reads as a COMPLIANT verdict. The '## Flagged Ingredients' section lists 'milk chocolate, chocolate bar, bar choco, choco bar, bar sugar' as though they were flagged, and never names gelatin or E471 (the two ingredients of real halal concern). The response has no floor_note and no sections_withheld. The sibling Tafsir tool on the same hub does withhold (sections_withheld… FIX (the assessor's proposal, a lead): Apply the tafsir pattern: when served_by is native, withhold 'Halal Status Assessment' and 'Flagged Ingredients' and add a floor_note. Or strip the verdict enum from the floor-facing prompt so no verdict token can be echoed. [docs/VISION_FIDELITY_LEDGER.md v5 R5.2, standing STUB, refutation survived] (found W476 ledger v5)
    FU-128 [high] [p 96.0] sweep genesis.py: 2 Tier-1 truth defects (C7,C10) — Chips 'Inkashaf · Samajh · Soch · Aqal · Hoshiyari · Iman · MJM · DDPIE · BDP ·… — S3.7 C10: Chips 'Inkashaf · Samajh · Soch · Aqal · Hoshiyari · Iman · MJM · DDPIE · BDP · gaas.v5'. The header says… → engines_used is a constant literal list. The journey never invokes the DDPIE or BDP engines, which exist as multi-stage engines…; S7.8 C7: A downloaded '<title>.md' holding a Genesis journey's Concept, Research, Design and Commercialisation text,… → All 11 Genesis calls were floor-served. genesis.py scrubs the inline floor marker out of the prose ('provenance … reported in… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-095 [high] [p 90.9] v5 R1.1: §10 bar 'compliant' + 'safe' recorded as MEASURED from keyword… — quality.py:142-146 records 'compliant' as met = (overall != 'fail') and 'safe' as met = no fail among… — quality.py:142-146 records 'compliant' as met = (overall != 'fail') and 'safe' as met = no fail among ethical/ehs/sharia_halal, both with measured=True and source 'gate'. The inputs are keyword screens that describe themselves as 'not an EHS assessment' and 'not a certification'. The Sharia row passes whenever the word 'halal', 'waqf' or similar appears in the text. assure_delivery (quality.py:228) copies only overall/compliant/verdicts and drops the screen's coverage_gaps and basis. The Deliverables page therefore shows an emerald 'COMPLIANCE: PASS' chip with no 'screen' qualifier (Deliverables.tsx:254-258), and its tooltip says 'MEASURED by this gate: compliant · safe'… FIX (the assessor's proposal, a lead): Record compliant/safe as met=None (basis 'keyword screen only') unless a row with coverage 'engine' actually read the subject. Carry coverage_gaps and basis into quality['compliance'] and label the chip 'screen: pass'. The halal row should not pass on the subject's own use of the word 'halal'. [docs/VISION_FIDELITY_LEDGER.md v5 R1.1, standing STUB, refutation survived] (found W476 ledger v5)
    FU-097 [high] [p 90.9] v5 R1.3: §10 'modelled · simulated · optimised · ranked' — Genesis stage 5… — genesis.py:394 `winner = (_eligible or candidates)[0]`: when every candidate is vetoed, a vetoed candidate… — genesis.py:394 `winner = (_eligible or candidates)[0]`: when every candidate is vetoed, a vetoed candidate still wins. The journey carries it into Design and Commercialisation and reports status 'complete'. The UI puts a 'selected' chip on it (GenesisJourney.tsx:719-726) and prints '…vetoed for §11 failure: pragmatic, innovative, lean — the winner is carried into Design.' (GenesisJourney.tsx:742). The page shows no veto indicator. FIX (the assessor's proposal, a lead): When every candidate is vetoed, stop the journey after stage 5 with status 'blocked_by_screen' and name the vetoes. Never carry a vetoed candidate forward. [docs/VISION_FIDELITY_LEDGER.md v5 R1.3, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-099 [high] [p 90.9] v5 R2.1: §4.5 / §4.8 / §11 as it drives the lifecycle — The same beekeeper journey: every candidate gets screen.overall=fail with ethical 'human: fail; …… — The same beekeeper journey: every candidate gets screen.overall=fail with ethical 'human: fail; … (engine-backed)'. stage_5.vetoed=[pragmatic, innovative, lean]. established_vsb.birth_vitals.first_cycle.held='compliance_fail_hold'. Ship commit messages read 'compliance fail' on repo/website/webapp/mobile. /evolve proposes 'remediate the §11 screen posture (currently fail)'. The exported report is stamped 'COMPLIANCE VERDICT: FAIL — NOT cleared for use — routed to Change Control'. Control, POST /api/v1/compliance/check: {subject:'I keep bees … varroa mites are killing a third of my colonies…'} gives overall fail, but {subject:'An affordable organic varroa treatment service for small-scale… FIX (the assessor's proposal, a lead): Carry the matched term into the surfaced reason. Downgrade a lone lexicon hit to 'review — keyword match, not an assessment' unless it has a human object. Never hold distributions or veto candidates on a keyword-only severe hit. [docs/VISION_FIDELITY_LEDGER.md v5 R2.1, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-101 [high] [p 90.0] v5 R2.3: §13 / §17.3 Board pack (compliance certification) — GET /api/v1/vsb/vsb-24267609d1/board-pack returns narrative 'narrative pending the owned model — this board… — GET /api/v1/vsb/vsb-24267609d1/board-pack returns narrative 'narrative pending the owned model — this board pack has not been composed…'. Its quality_assurance shows compliance.overall='review', compliant=True, and bar_measured.criteria.compliant={met:true, measured:true, source:'gate'}, safe={met:true, measured:true, source:'gate'}. At the same moment the entity's own §11 screen is FAIL (ship record: repo/website/webapp/mobile compliance_overall 'fail'; board_pack 'review'). The screen read only the placeholder sentence and certified the enterprise compliant and safe. The UI (GenesisJourney.tsx ~1062) shows a 'compliance: review' chip on the pack. FIX (the assessor's proposal, a lead): When the narrative is pending, report compliance as 'not assessable — nothing composed' (compliant/safe met:null). Otherwise screen the constitutional/mission layer the pack actually carries, and show the entity's latest §11 verdict on the pack. [docs/VISION_FIDELITY_LEDGER.md v5 R2.3, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-125 [high] [p 88.2] sweep deliverables.py: 3 Tier-1 truth defects (C5,C7,C8) — Export page one: '_report · produced on Workstation's own AI fabric (in-house ·… — S6.5 C7: Export page one: '_report · produced on Workstation's own AI fabric (in-house · native)_'. SVG/PNG footer:… → The content was composed by the deterministic floor. The on-page badge (provenanceBadge) correctly says 'structured floor — not…; S6.6 C5: After refining, the detail badge turns emerald 'in-house · verbatim-ingest'. The list row reads… → The refined text came from the floor: /api/v1/refine returned served_by 'native', and its text is the original plus 'Refinement…; S7.3 C8: 'Success rate 100%', with every ranked resource's Success shown as an emerald 100%, framed as 'honest… → success is recorded as 'output non-empty' (or 'trace non-empty'). The deterministic floor always returns text, so the figure… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-098 [high] [p 81.8] v5 R2.0: §4.2 Understand & Map / §4.1 (Genesis Phase 1) — POST /api/v1/genesis/journey {problem:'I keep bees in Yorkshire and varroa mites are killing a third of my… — POST /api/v1/genesis/journey {problem:'I keep bees in Yorkshire and varroa mites are killing a third of my colonies…', domain:'agriculture', establish:true}. phase_1_conceptualisation.cognitive_cascade contains 0 of the 17 content words in the problem. It repeats six times the subject 'Analyse the following thro (domain: general)' with bullets 'architecture specialised · specialised intelligence · cognitive architecture…'. mjm_assessment repeats nine times 'Process this through the three phases of Mus (domain: general)' with bullets 'intermittent fasting · insulin sensitivity · sensitivity adults'. Those words come from ANOTHER interaction: memory.json holds 3 hits for 'intermittent… FIX (the assessor's proposal, a lead): Pass augment=False and route the two calls through the journey's provenance-recording _q (which carries the Problem field). When floor-served, render these two sections as 'pending the owned model' as the VSB body does, and count them in served_by. [docs/VISION_FIDELITY_LEDGER.md v5 R2.0, standing STUB, refutation survived] (found W476 ledger v5)
    FU-100 [high] [p 81.8] v5 R2.2: §4.8 Establish / §4.10 Run forever (status, progress map, stage rail) — Every establish path writes status:'operational', stage:'commercialise' as literals, whatever the state. For… — Every establish path writes status:'operational', stage:'commercialise' as literals, whatever the state. For vsb-24267609d1 the real state is: body 4 of 4 pending, first §11 screen FAIL, first cycle held, and living.autonomous_cycles=false (Self-run OFF). For vsb-6cbffb7c1d: research and design gates pending, yet GET /api/v1/vsb/vsb-6cbffb7c1d returns status 'operational', stage 'commercialise'. What the user sees, from source: - GenesisJourney.tsx:893 prints the literal '{vsb_id} · operational · governance allowed' and an emerald 'Living Enterprise IDBO generated'. - VSBCockpit.tsx:453 shows the status as a green Badge. - The shipped README.md says 'Status: operational'. - The progress… FIX (the assessor's proposal, a lead): Derive status from facts (e.g. 'registered — held: §11 fail', 'registered — not operating: Self-run off', 'gated'). Light 'Operate' only when autonomous_cycles is true and the last cycle ran. Light rail tiles from the payload's per-stage attestations. Render birth_vitals on the one-call path. [docs/VISION_FIDELITY_LEDGER.md v5 R2.2, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-140 [high] [p 76.9] sweep compliance.py: 1 Tier-1 truth defect (C5) — A green 'compliance: pass' on the generated repository, web app and PWA, with no… — S3.6 C5: A green 'compliance: pass' on the generated repository, web app and PWA, with no tooltip. QUALITY.md is… → sharia_halal and uk_legal both returned 'review — no engine covers this area' (coverage 'none'). The pass is the pass of three… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-127 [high] [p 68.6] sweep products.py: 3 Tier-1 truth defects (C3,C4,C7) — The floor-served comparison is badged in emerald 'in-house · [object Object]', the style… — S4.2 C7: The floor-served comparison is badged in emerald 'in-house · [object Object]', the style reserved for a real… → All 4 calls were served by the deterministic floor (served_by {native:4}). reactor_experiment returns ai_provenance.served_by as…; S8.0 C3: 'Winner V1 · 95%', 'Winner — Variant 1 … 95%', leaderboard progress bars 95% / 90% / 85%, Strengths 'Strong… → No variant was scored. On the floor the scorer's output has no VARIANT_N|SCORE lines, so products.py falls back to hard-coded…; S8.7 C4: Toggles 'Article 1095 Logic', 'Latency Stress Test', 'Byzantine Fault Mode' and 'In-House Fabric' under… → No simulation runs, and none of the parameters is implemented anywhere. They become JSON inside a prompt. No latency stress or… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-112 [high] [p 63.6] v5 R4.5: Command Center (the shell's Channels dock on every page) — Most channels are now honest (packages/ui/src/CommandCenter.tsx), but untrue statements remain on a surface… — Most channels are now honest (packages/ui/src/CommandCenter.tsx), but untrue statements remain on a surface reached from every page (Shell, then FourthColumn, then <CommandCenter tiled/>). The Spatio-Temporal channel (components/organism/SpatioTemporal.tsx) renders the literals 'Sovereign Consensus Status: CROSS-PLANETARY SYNC ACTIVE' and 'Mars Relative: T + 842s' under an 'illustrative' header. After 'Apply REST Mode', the Predictive channel says 'Rest Mode applied. Cognitive durability optimization in progress.' (CommandCenter.tsx:425), but the handler only sets a UI mode flag. The heading still reads 'RL-Powered Suggestions' although no RL exists. Every channel has a 'Query <channel>… FIX (the assessor's proposal, a lead): Delete the SYNC ACTIVE and Mars literals. Change the REST text to 'REST mode set — this only changes the interface'. Drop 'RL-Powered' and the Live dot. Either remove the query box or label it 'nothing answers here yet'. [docs/VISION_FIDELITY_LEDGER.md v5 R4.5, standing STUB, refutation survived] (found W476 ledger v5)
    FU-113 [high] [p 63.6] v5 R5.0: §3A Domain Working (Care) / §15 P6 — The falls-risk scorer tells the user 'no falls history' when falls history was never recorded, and shows a… — The falls-risk scorer tells the user 'no falls history' when falls history was never recorded, and shows a GREEN chip. POST /api/v1/care/risk-assess {tool:falls_risk, patient_data:<the CareHub default NEWS2 keys>} and {tool:falls_risk, patient_data:{'fallen twice this year':'yes'}} both return total 0, band 'no trigger recorded', response 'no falls history and fewer than two factors recorded — reassess on change', factors_present [], missing = all 11 factors INCLUDING falls_history, warnings []. The unrecognised key is dropped without a warning. CareHub renders the band chip with a regex colour fallthrough (high→red, medium|at risk|warranted→amber, else EMERALD), so 'no trigger recorded'… FIX (the assessor's proposal, a lead): When falls_history is in missing, return band null and a response like 'falls history not recorded — cannot say whether assessment is warranted'. Colour only an explicit low band emerald; any other band goes neutral. Put a warning on every key the scorer does not recognise. [docs/VISION_FIDELITY_LEDGER.md v5 R5.0, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-106 [high] [p 60.0] v5 R3.4: §5 org cascade → §11 compliance chip (Sharia screen) — The Sharia screen passes text that contains the word 'halal' and no listed haram term. Interest-bearing… — The Sharia screen passes text that contains the word 'halal' and no listed haram term. Interest-bearing lending described as 'halal' gets sharia_halal PASS and an overall PASS. The org cascade's emerald 'compliance: pass' chip inherits this. The cascade's quality.compliance also drops the screen's coverage_gaps/basis fields, so the chip reads pass while uk_legal is 'review — no engine covers this area'. FIX (the assessor's proposal, a lead): Add interest/usury/APR/percent-interest patterns to the haram screen, never pass sharia_halal on self-declared vocabulary alone (make it 'review'), and carry coverage_gaps into the cascade chip. [docs/VISION_FIDELITY_LEDGER.md v5 R3.4, standing STUB, refutation survived] (found W476 ledger v5)
    FU-146 [high] [p 60.0] sweep vsb.py: 1 Tier-1 truth defect (C3) — The header says 'Runs through the full intelligence pipeline: Nine Cognitive Engines →… — S2.0 C3: The header says 'Runs through the full intelligence pipeline: Nine Cognitive Engines → MJM → GaaS…'. The… → The cascade runs six stub engines, not nine, and every one returns a literal. AqalEngine.reason returns… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-116 [high] [p 58.3] v5 R6.0: §8 homeostasis / composite health (and §17.5 twin pre-validation,… — The headline organism health reports NOMINAL/FULL_POWER with a percentage mostly made of unmeasured values,… — The headline organism health reports NOMINAL/FULL_POWER with a percentage mostly made of unmeasured values, even while the only measured term reads zero and CRITICAL. Live at 13:09Z: GET /api/v1/organism/status returned composite_health 0.6, mode NOMINAL, health_summary 'Organism nominal — ACTIVE_FOCUS cycle, health 60%. Standard operations active.' In the same response systems.immune was health 0.0, threat_level CRITICAL, errors_in_window 11, with a playbook saying 'engage immune_quarantine'. /health-summary: composite_health_measured_only 0.0. The terms: self_healing value 1.0 is measured:false ('defaulted to 1.0') and GET /organism/self-healing/status says overall_health null, 0… FIX (the assessor's proposal, a lead): Compute mode and health_summary from composite_health_measured_only, or make an unmeasured term count as unknown rather than 1.0. Put health_basis beside every rendered composite. Make the twin fallback read immune health or measured_only instead of the composite. [docs/VISION_FIDELITY_LEDGER.md v5 R6.0, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-102 [high] [p 54.0] v5 R3.0: §5 / §6 — Swarm tab of the Living Organisation hub (/ceo?tab=swarm) — The chart titled 'QMS coverage vs run duration (measured)' plots every swarm run's… — The chart titled 'QMS coverage vs run duration (measured)' plots every swarm run's quality.delivery_coverage. On the floor that value is 1.0 by construction, and the same record says it is not assessable. So each floor run shows up as a top-of-chart 'measured' 100% coverage point. FIX (the assessor's proposal, a lead): Exclude runs with qms_gate_passed === null (or not_assessable) from paretoPoints. Better, have assure_delivery return delivery_coverage:null on floor-served runs so no renderer can plot it. [docs/VISION_FIDELITY_LEDGER.md v5 R3.0, standing STUB, refutation survived] (found W476 ledger v5)
    FU-104 [high] [p 54.0] v5 R3.2: §17.3 Living Business System — the on-demand Board Pack — The pack is honest about versioning, the review gate, the floor narrative and the concept source. But its… — The pack is honest about versioning, the review gate, the floor narrative and the concept source. But its narrative claims 'the operational snapshot, constitutional layer and strategic specification below are live data', while the strategic layer is {"ceo": {}} (empty). The action_plan layer is the static board roster. The constitutional Mission is the string 'Deliver: <problem>' and the Vision is the problem statement verbatim; values is one constant string for every VSB. The Genesis page shows a chip listing all four layer names as present. FIX (the assessor's proposal, a lead): Emit the strategic/action_plan layers as {pending: 'no cadence generator (P3.3)'} when empty, have the narrative name only the layers that carry data, and label mission/vision 'derived from the problem statement'. [docs/VISION_FIDELITY_LEDGER.md v5 R3.2, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-129 [high] [p 49.3] sweep organism_status.py: 2 Tier-1 truth defects (C4,C10) — '4 encoded genomes' — S8.2 C10: '4 encoded genomes' → Every stored genome has encoded:false. The floor cannot declare traits, and each record says 'not encoded — … this vector is NOT…; S8.6 C4: 'Homeostasis complete. 1 adjustment made. Mode: …' (outside 09:00-17:00 local time, or 2 or more when immune… → The 'defer_non_urgent' (off-peak) and 'elevated_monitoring' (HIGH/CRITICAL immune) adjustments are only appended to a list.… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-132 [high] [p 49.3] sweep SolutionsPlatform.tsx: 2 Tier-1 truth defects (C1,C4) — '✓ Native AI fabric: reachable.' (green success) is followed by 'Readiness check… — S5.1 C1: '✓ Native AI fabric: reachable.' (green success) is followed by 'Readiness check PASSED.' The Launch button… → GET /api/v1/native-ai/status returns is_real_model:false, mode:'deterministic_floor', floor_active:true and floor_note 'The…; S5.2 C4: The tiles read 'V9 Engine — Sovereign execution runtime', 'Monitoring — Real-time mission telemetry',… → None of these exists. 'V9 Engine' appears nowhere in agentic_core/ or in the rest of the frontend, and there is no telemetry,… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-133 [high] [p 49.3] sweep CapitalDashboard.tsx: 2 Tier-1 truth defects (C4,C5) — Badge 'PHASE 3: EXTERNALLY INTEGRATED' — S2.5 C5: Badge 'PHASE 3: EXTERNALLY INTEGRATED' → The badge is a literal. The same page's External Markets tab says 'No market-data provider is connected to this deployment……; S2.6 C4: A switch labelled 'Semi-Autonomous' whose aria-label/title flips to 'Semi-Autonomous mode: On' when pressed → The toggle only sets local React state (autonomousEnabled), which nothing reads. No request is sent, no lever changes and no… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-135 [high] [p 49.1] sweep orchestrator.py: 1 Tier-1 truth defect (C1) — A green 'integrated' chip: the synthesis genuinely integrated the branches rather than… — S7.2 C1: A green 'integrated' chip: the synthesis genuinely integrated the branches rather than near-copying one. → Every node was floor-served, and every node's output is the same template headed '## frame output'. The backend itself marks… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-103 [high] [p 48.0] v5 R3.1: §5 BTO / living management systems (BMS) on the org-cascade result — The cascade result chip reads 'BMS EFFICIENT · $2e-06/insight'. Both the status and the unit cost come from… — The cascade result chip reads 'BMS EFFICIENT · $2e-06/insight'. Both the status and the unit cost come from the catalogue's simulated constants (a $/Wh rate and a $0.50-per-insight value, giving roi 266666.667). insights_count 10 counts the floor's own outputs. The EMS chip beside it carries '(sim)', but the BMS chip has no such label; the caveat is only in a hover title. FIX (the assessor's proposal, a lead): Suffix the BMS chip '(sim)' like EMS, and make status 'not assessed' when every call was floor-served or the value basis is a constant. [docs/VISION_FIDELITY_LEDGER.md v5 R3.1, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-107 [high] [p 48.0] v5 R3.5: §5 Change Control (arms-length) — the review's organism-health… — With no model marker (always the case on the floor), the review decides by `composite_health >= 0.5`. That… — With no model marker (always the case on the floor), the review decides by `composite_health >= 0.5`. That composite is 40% a defaulted 1.0 (no self-healing circuits tracked) and 20% simulated ATP. With immune health at 0.5 (threat ELEVATED, 5 errors) it still reads 0.77–0.95, so under current conditions the rule cannot reject anything: 0.4·imm + 0.4 + 0.2·atp ≥ 0.5 for any imm ≥ 0 while atp ≥ 0.5. MEDIUM changes are approved and become implementable. The record states the number without saying most of it is unmeasured, although /organism/status publishes composite_health_measured_only (0.5) and the basis. FIX (the assessor's proposal, a lead): Decide on composite_health_measured_only, or hold for an explicit decision when the measured share is below a threshold. Print the measured share in review_result. [docs/VISION_FIDELITY_LEDGER.md v5 R3.5, standing PARTIAL, refutation refuted] (found W476 ledger v5)
    FU-123 [high] [p 47.1] sweep resource_fabric.py: 4 Tier-1 truth defects (C3,C5,C7,C10) — '10 LIVE in-house formats rendered via /export?format= (md · html · slides · txt · json… — S4.3 C10: '10 LIVE in-house formats rendered via /export?format= (md · html · slides · txt · json · self-playing… → The live output-formats API lists 8 live formats: md, html, slides, txt, json, video-html, svg, png. It lists pdf, docx, pptx,…; S4.8 C5: 'C-Suite engaged (your design): CFO · CTO · COO · CLO · Forecasting · Policy — each drives a CoE' → The user set no C-Suite. The registry's example placeholder 'e.g. CSO,CFO,CTO,COO,CLO,Forecasting,Policy' is parsed as the…; S4.9 C3: truth_consensus 'ran' (emerald) with output {"accepted": 0, "of": 2, "threshold": 0.85}, under 'the composed… → Every configured claim is given the constant confidence=0.8 and reputation=0.8. The resource's declared…; S11.3 C7: A green 'in-house · real-engine' badge on the outcome row for fabric:mega_project, a facility whose text is… → The W439 class-kill helper colours ANY served_by other than 'native' or external as emerald 'in-house · <value>'. The backend… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-154 [high] [p 46.7] sweep CareHub.tsx: 1 Tier-1 truth defect (C4) — Each hub header shows the badges 'GUIDED MODE' and 'ENCOURAGING TONE'. Settings says… — S10.5 C4: Each hub header shows the badges 'GUIDED MODE' and 'ENCOURAGING TONE'. Settings says 'guidance and tone… → Only the badge text reads guidedMode and tone. No component changes any affordance on guidedMode, no request sends tone to a… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-126 [high] [p 44.6] sweep integration_surface.py: 3 Tier-1 truth defects (C3,C4) — The panel shows 'Specification generated. Review and proceed to Build phase.' as the… — S5.0 C3: The panel shows 'Specification generated. Review and proceed to Build phase.' as the generated spec. The… → Nothing reads the user's brief. The page POSTs {message: prompt}, but the AIQuery model only has prompt/query/agent, so the…; S10.3 C3: The Constitutional Core lists 'Article 1 · CORE · The Sovereign Digital Organism — Workstation is a… → The canon was archived. agentic_core/constitution/ does not exist (the files are in _archive/agentic_core/constitution/). The…; S13.1 C4: 'The organism evolves itself — autonomously, and curated by its own Virtual Sovereign Business.' and the… → Nothing runs the cycle on its own. The only autonomous caller is heartbeat.py:353, which is gated on auto_evolve, and… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-108 [high] [p 43.6] v5 R3.6: §5 Chief = founder's digital twin; §17.4 Mode 2 — No twin model exists. The Board page says so ('no digital-twin model is trained yet (Mode 2 is planned,… — No twin model exists. The Board page says so ('no digital-twin model is trained yet (Mode 2 is planned, P3.4)'). Two other reached surfaces still tell the user the Chief is their digital twin. The Chief acts only on a click (chief/instruct); nothing invokes it autonomously. FIX (the assessor's proposal, a lead): Replace 'your digital twin' in BusinessPlan.tsx:107 and SwarmIntelligence.tsx:299 with the Board's wording (standing charter + last instructions; twin model planned). [docs/VISION_FIDELITY_LEDGER.md v5 R3.6, standing PARTIAL, refutation refuted] (found W476 ledger v5)
    FU-110 [high] [p 42.0] v5 R4.1: §8/§17.2 organism vitals (Immune, Self-healing, Metabolic) as shown… — GET /api/v1/organism/status returns composite_health=0.929, mode=FULL_POWER and health_summary 'Organism at… — GET /api/v1/organism/status returns composite_health=0.929, mode=FULL_POWER and health_summary 'Organism at peak — ACTIVE_FOCUS cycle, health 93%. Full cognitive power available.' The terms are: immune 0.4×1.0 (measured), self_healing 0.4×1.0 'defaulted to 1.0, not a measurement', and metabolic 0.2×0.643 'ATPSimulator … simulated'. So 60% of the weight is not measured, and the measured-only figure is 1.0. The home page (DashboardNew.tsx:107, 257, 261) shows '<mode> · 93% health' and a 'Composite Health 93%' bar with no basis. The default /organism tab (OrganismDashboard.tsx:262-266) shows 93% big with the health_summary and a green FULL THROUGHPUT chip. On the same page, the Self-Healing… FIX (the assessor's proposal, a lead): On Home and the /organism overview, render composite_health_measured_only as the headline, with health_basis as the caption, and move the blended figure into a 'with default and simulated terms' tooltip. Label the Metabolic card 'simulated'. Have _health_summary say how much of the score is measured, and stop saying 'Full cognitive power' when native homeostasis reports 'reduced'. [docs/VISION_FIDELITY_LEDGER.md v5 R4.1, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-111 [high] [p 42.0] v5 R4.2: §17.2 evolution / self-improvement (the Cognition tab's 'organism… — POST /api/v1/cognition/align {execute:false} returned overall_realisation=0.97 with one gap. The checks… — POST /api/v1/cognition/align {execute:false} returned overall_realisation=0.97 with one gap. The checks behind that number are route-mount and non-empty-store lambdas (agentic_core/api/transformation.py:141-157). _realise() itself names this 'API surface coverage … not delivery', but align() and /api/v240/evolution/metrics drop that 'measure' field. The metrics route adds status 'realised' 1.0 for pillars such as "Chief = Owner's digital twin" and "Reconfigurable, combinable resource fabric". CognitionIntegration.tsx:173 renders 'Overall realisation 97% · N gaps routed (evidence-based)'. :170 would render 'Fully aligned — no open vision gaps.' once one evolution cycle runs. :125 shows… FIX (the assessor's proposal, a lead): Pass _realise()['measure'] through align, knowledge and v240 metrics. Relabel the Cognition tab figure 'API surface coverage (not delivery)' and replace 'Fully aligned — no open vision gaps' with 'no coverage gaps — delivery is measured at /api/v1/plan/state'. Rename the v240 fields (vision_realisation to api_coverage, 'realised' to 'surface present'). [docs/VISION_FIDELITY_LEDGER.md v5 R4.2, standing PARTIAL, refutation corrected] (found W476 ledger v5)
    FU-119 [high] [p 42.0] v5 R6.3: §12 Sovereign Capital Fund (the capital_fund waterfall stage… — The fund's baseline is an unfunded 10M WST constant presented as 'the real capital fund', and an unreadable… — The fund's baseline is an unfunded 10M WST constant presented as 'the real capital fund', and an unreadable fund is silently reset to that constant. (a) When the store is absent, _load_fund() seeds total_capital and available at 10,000,000 WST. The live fund was created by my first cycle at 13:01:40 and reads total_capital 10,000,156 = 10,000,000 seed + 140 + 16 in cycle contributions. No cycle, owner or ledger funded the 10M. CapitalDashboard.tsx:170-194 shows it with the caption 'Figures are the real capital fund … in virtual WST'. Wallet.tsx:76 shows 'Total Pool 10M WST' and 'Fund Health HEALTHY'. /fund/status has no basis field. (b) I wrote a malformed capital_fund.json. GET… FIX (the assessor's proposal, a lead): Start the fund at 0 plus real cycle contributions, or disclose the seed as an Owner-set virtual endowment with its own basis field. Read the store strictly and return 503 when unreadable, never a fresh pool. [docs/VISION_FIDELITY_LEDGER.md v5 R6.3, standing STUB, refutation survived] (found W476 ledger v5)
    FU-120 [high] [p 42.0] v5 R6.4: §8 self-curation: Sovereign Evolution Office (introspect → AI CEO →… — The cycle's C-Suite verdict is a code default, but the page shows it as the C-Suite's decision. Under the… — The cycle's C-Suite verdict is a code default, but the page shows it as the C-Suite's decision. Under the native floor, POST /api/v1/sovereign-evolution/cycle {focus:'audit', submit_to_change_control:false} returned 200. The introspection showed immune health 0.0, CRITICAL. The only CEO directive was the code default 'Routine organism health review' (P2, COO), with rationale 'No parseable CEO directives; defaulting to a maintenance sweep.' Its verdict 'proceed' and effort 'M' are also code defaults (sovereign_evolution.py:243-245 fills 'proceed' when no C-Suite line matched). The response still says curated_by ['AI CEO','C-Suite','CoE','BTO'] and items_proceeding 1. bto_roadmap is the… FIX (the assessor's proposal, a lead): Mark defaulted directives and verdicts with a source field (for example verdict_source 'default: no C-Suite verdict parsed'). Render it as 'no verdict'. Drop curated_by tiers that returned nothing parseable. [docs/VISION_FIDELITY_LEDGER.md v5 R6.4, standing STUB, refutation survived] (found W476 ledger v5)
    FU-149 [high] [p 42.0] sweep FourthColumn.tsx: 1 Tier-1 truth defect (C5) — Collapsed-rail button tooltip 'External AI Agents' — S13.3 C5: Collapsed-rail button tooltip 'External AI Agents' → The button opens NativeAgentPanel, which is the in-house assistant served by Workstation's own fabric (external is opt-in and… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-150 [high] [p 42.0] sweep BTOCatalog.tsx: 1 Tier-1 truth defect (C5) — 'Blueprint Provisioned' appears above the entity. While loading: 'Provisioning Sovereign… — S5.7 C5: 'Blueprint Provisioned' appears above the entity. While loading: 'Provisioning Sovereign Infrastructure' /… → The API says the opposite. It returns provisioned:false; every component is 'SPECIFIED (blueprint only)' with… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-151 [high] [p 42.0] sweep KnowledgeHub.tsx: 1 Tier-1 truth defect (C3) — Each 'Centre of Excellence' card shows 'Confidence 1' and 'Outputs 0'. The Portfolio… — S13.2 C3: Each 'Centre of Excellence' card shows 'Confidence 1' and 'Outputs 0'. The Portfolio card's own description… → The live /api/v1/intelligence/insights payload carries no confidence, projects_count or outputs_count. KnowledgeHub.tsx:53-54… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-152 [high] [p 42.0] sweep CreatorStudio.tsx: 1 Tier-1 truth defect (C4) — A palette of nine components (REST API Poller, ArXiv Scraper, MQTT Subscriber, AI… — S12.5 C4: A palette of nine components (REST API Poller, ArXiv Scraper, MQTT Subscriber, AI Synthesis, Sentiment… → The palette only adds label-only ReactFlow nodes, and nothing implements any of the nine. 'Run Pipeline' does not run the… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-155 [high] [p 42.0] sweep LivingMarketplace.tsx: 1 Tier-1 truth defect (C10) — 'Catalogue entries above are registered but unpriced, so they are not listed here.' — S12.8 C10: 'Catalogue entries above are registered but unpriced, so they are not listed here.' → They are listed there. The grid renders every listing (listings.map), and all 4 current listings are the catalogue-derived… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-156 [high] [p 42.0] sweep ReactorStudio.tsx: 1 Tier-1 truth defect (C3) — The header says 'Visualises the data you provide; never invents numbers.' A line such as… — S5.10 C3: The header says 'Visualises the data you provide; never invents numbers.' A line such as 'Q4, n/a' (or 'Q4,'… → parseSeries coerces any unparseable value to 0 (and an empty label to '?') and sends it as data, so the page manufactures a data… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-134 [high] [p 41.5] sweep gateway.py: 1 Tier-1 truth defect (C7) — A 'Synthesis' and an 'MJM Meta-Judgement' of the user's own problem, and 'Engines run:… — S7.0 C7: A 'Synthesis' and an 'MJM Meta-Judgement' of the user's own problem, and 'Engines run: AQAL · IMAN · MJM ·… → gateway.query's default augment=True puts token-overlap recall of OTHER, earlier interactions into the prompt. The deterministic… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-124 [high] [p 40.4] sweep api.py: 4 Tier-1 truth defects (C3,C6) — An uploaded audio file whose name contains 'recitation' is registered as INGESTED with… — S4.0 C6: An uploaded audio file whose name contains 'recitation' is registered as INGESTED with extracted_text 'In… → Nothing is transcribed. TRANSCRIPTION_MOCK is a filename-pattern lookup table. Scripture-adjacent text is attached to a user's…; S4.1 C3: A PDF or DOCX is INGESTED with extracted_text 'Content extracted from rich document: <name>. Primary topics… → No extraction runs. The 'primary topics' are constants, whatever the document says. Synthesis then writes reports 'grounded in'…; S12.2 C3: The file is listed as uploaded into its slot, and Generate builds a 'tailored' CV, cover letter and other… → For .pdf/.docx, the usual CV formats, ingestion never reads the file. It stores the invented text 'Content extracted from rich…; S12.3 C6: The upload is accepted and ingested (status INGESTED). Its 'transcription' is stored as the file's content… → The 'transcription' is a hard-coded English rendering of Al-Fatiha 1:1-2 ('In the name of Allah, the Most Gracious, the Most… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-130 [high] [p 40.2] sweep swarm.py: 2 Tier-1 truth defects (C1,C9) — The page shows a green monospace JSON delivery for the mission. It never mentions that… — S11.0 C9: The page shows a green monospace JSON delivery for the mission. It never mentions that the cascade was… → POST /api/v1/swarm/cascade refuses with 409 'review gate blocks progress … cascade refused'. The page treats any non-2xx as a…; S11.1 C1: 'gov: allowed · arms-length' in green, on a result the code calls 'arms-length constitutional governance… → The gate never sees the delivery. intercept() receives only {intent:'org_cascade', domain} and a constant sentence ('Org cascade… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-136 [high] [p 40.0] sweep board.py: 1 Tier-1 truth defect (C5) — 'Faithfully interpreted → board directive → delegated to the AI CEO'. The directive's… — S2.3 C5: 'Faithfully interpreted → board directive → delegated to the AI CEO'. The directive's '## Owner Intent'… → board._q calls gateway.query_meta without augment=False, so cross-request memory recall is injected into the Chief's prompt.… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-109 [high] [p 38.2] v5 R4.0: §7 (Petri dish, a musculoskeletal facility) + §15.6 (never fabricate) — The Petri dish's viability verdict is a substring test: viable = 'not-viable' not in tail and 'not viable'… — The Petri dish's viability verdict is a substring test: viable = 'not-viable' not in tail and 'not viable' not in tail (agentic_core/api/products.py:546). The deterministic floor never writes those words, so every floor-served culture comes back viable=true. I ran POST /api/v1/petri/culture with {"specimen":"sell ice to penguins at a premium, financed with riba loans"} and got viable=True, ai_provenance.served_by={native:1} and qms_gate_passed=None. The culture text also contained 'varroa treatment', which is native-memory recall from my earlier, unrelated probe leaking into a new request. In the fabric, the adapter (agentic_core/api/resource_fabric.py:518) returns {viable, passages,… FIX (the assessor's proposal, a lead): Return viable=None ('not assessable — floor-served') whenever served_by is native, and put served_by/is_external on the fabric's petri_dish row so provenanceBadge renders. Consider making viability require an explicit 'VIABLE' line rather than the absence of 'not viable'. [docs/VISION_FIDELITY_LEDGER.md v5 R4.0, standing STUB, refutation survived] (found W476 ledger v5)
    FU-114 [high] [p 38.2] v5 R5.1: §3 / §14 marketplace (Living Marketplace catalogue) — GET /api/v1/catalog/products returns counts {registered 20, live 4, source 10, legacy 6}. The counts and the… — GET /api/v1/catalog/products returns counts {registered 20, live 4, source 10, legacy 6}. The counts and the status labels are honest. The four LIVE cards still list features that nothing serves. capital_fund (live, /capital) lists 'Autonomous Rebalancing', 'On-Chain Gateway' and 'Constitutional Evolution Voting'; the only matches for rebalanc / evolution-vot in agentic_core are the catalogue literal itself. The capital fund's own page says the opposite: CapitalDashboard.tsx:253-256 reads 'No on-chain integration exists' (the crypto_gateway/mainnet_settlement code under products/capital_fund/ is imported by nothing). qep-sdk (live, /qep-religion) lists 'Arabic Morphology Analysis', 'AI… FIX (the assessor's proposal, a lead): Replace each live product's features with the capabilities its route actually serves, e.g. capital fund: 'virtual WST allocation · portfolio · AI report'. Drop On-Chain Gateway, Rebalancing, Morphology, Quiz, Trust Scoring and Quad-Engine, or move them under a labelled 'not built' line. [docs/VISION_FIDELITY_LEDGER.md v5 R5.1, standing PARTIAL, refutation corrected] (found W476 ledger v5)
    FU-138 [high] [p 38.2] sweep career.py: 1 Tier-1 truth defect (C3) — '"person_spec_w477s12.txt" classified as Old CVs (70% confidence)', under the line… — S12.1 C3: '"person_spec_w477s12.txt" classified as Old CVs (70% confidence)', under the line 'content is analysed and… → No classification happened. On the floor the model reply is not JSON, so the handler's except branch hard-codes… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-139 [high] [p 38.2] sweep cognition.py: 1 Tier-1 truth defect (C8) — An emerald '13/13 connected · 100% coherence', with a green check per tier ('the… — S7.4 C8: An emerald '13/13 connected · 100% coherence', with a green check per tier ('the knowledge system wired into… → 'connected' means only that some mounted route path starts with the tier's endpoint prefix. It cannot be false while the app… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-142 [high] [p 38.2] sweep economy.py: 1 Tier-1 truth defect (C5) — The Owner selects an established VSB, then clicks the 'Charity' form card, which is… — S1.8 C5: The Owner selects an established VSB, then clicks the 'Charity' form card, which is highlighted and badged… → For a registered VSB the backend ignores the picked form and uses the registry's (waqf_ltd_hybrid). The cycle pays the Owner 20%… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-143 [high] [p 38.2] sweep management_systems.py: 1 Tier-1 truth defect (C5) — 'ISO 9001 · ISO 14001 · Balanced Scorecard · OKRs · Audit · Risk — AI-generated,… — S2.4 C5: 'ISO 9001 · ISO 14001 · Balanced Scorecard · OKRs · Audit · Risk — AI-generated, immediately usable' → On this deployment all six generators are served by the deterministic floor. The API's own floor_note says 'it is not model… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-144 [high] [p 38.2] sweep transformation.py: 1 Tier-1 truth defect (C7) — A panel headed 'AI Assessment' with '## Faithfulness Assessment', '## Biggest Gaps', '##… — S6.7 C7: A panel headed 'AI Assessment' with '## Faithfulness Assessment', '## Biggest Gaps', '## Recommended Next… → The floor served it. It restates the prompt ('Subject: Overall realisation: 89%') and gives generic frames ('Exposure on current… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-145 [high] [p 38.2] sweep ceo_generate.py: 1 Tier-1 truth defect (C7) — 'AI CEO is synthesising your blueprint…', then a success tick with '<intent> — Concept… — S12.4 C7: 'AI CEO is synthesising your blueprint…', then a success tick with '<intent> — Concept Blueprint' and a… → The deliverable is the deterministic floor outline ('## Understanding / Key factors / Native approach / Next steps'), and the… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-147 [high] [p 38.2] sweep bto.py: 1 Tier-1 truth defect (C1) — Each product gets a green 'BUILT' chip, the header reads 'Delivered 3 · in-house-first',… — S5.8 C1: Each product gets a green 'BUILT' chip, the header reads 'Delivered 3 · in-house-first', and the tagline… → No product was built. Each 'BUILT' item is a floor-composed 6-heading report scaffold, and qms_gate_passed is null for every… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-137 [high] [p 36.0] sweep business_plan.py: 1 Tier-1 truth defect (C5) — An empty plan: no opening, '0 objectives', 0%. The next Add Objective / +25% / Owner… — S3.10 C5: An empty plan: no opening, '0 objectives', 0%. The next Add Objective / +25% / Owner edit / Board directive… → _load swallows JSONDecodeError and returns a fresh empty plan. The first write then atomically overwrites the Owner's real plan… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-118 [high] [p 35.0] v5 R6.2: §12 charity: the Owner's directives (inclusions and exclusions… — An unreadable Owner charity-directives store is quietly replaced by defaults, and money then goes to causes… — An unreadable Owner charity-directives store is quietly replaced by defaults, and money then goes to causes the Owner excluded. I wrote a malformed C:/tmp/w476b/economy_charity_directives.json. It was a truncated object with exclusions ['dawah','conflict_relief'] and priorities ['clean_water']. Results: GET /api/v1/economy/charity/directives returned 200 with exclusions [] and source 'defaults (2026-06-21 Owner directive)'. POST /api/v1/economy/cycle {vsb_id:'w476-r6-e', revenue:100} then granted to conflict_relief, a cause the Owner had excluded, with no error. The cause is get_directives(), which uses load_json_tolerant(..., {}): a store that cannot be parsed reads as never set.… FIX (the assessor's proposal, a lead): Read the directives, signals and revenue stores strictly (read_json_strict / StoreUnavailable). A cycle should refuse to allocate charity, or hold it, while the directives cannot be read, and the directives route should return 503. [docs/VISION_FIDELITY_LEDGER.md v5 R6.2, standing PARTIAL, refutation survived] (found W476 ledger v5)
    FU-117 [high] [p 32.3] v5 R6.1: §8 survival instinct / §8→§12 economic survival instinct / metabolic… — The ATP 'metabolic energy' behind every survival-instinct lever can only go up. ATPSimulator starts at ratio… — The ATP 'metabolic energy' behind every survival-instinct lever can only go up. ATPSimulator starts at ratio 5.0 (0.333 normalised). Each update adds production 0.5*efficiency (0.4–0.5) and subtracts consumption 0.1*load (at most 0.1). Every organism_context() read advances it, at most once a second, with load 0.2–1.0. Live, it rose with page polls: 0.396 → 0.456 → 0.831 → 1.0 within about 10 minutes of boot, and stayed at 1.0. So the following can never fire: the economy's reserve raise at atp < 0.3 (metabolism.py:158-163), the heartbeat's self_recovery at < 0.3 (heartbeat.py:194-203), native homeostasis 'protected' at < 0.3, and metabolic_throttle at < 0.2 (heartbeat.py:327). The number… FIX (the assessor's proposal, a lead): Either drive ATP from a real load signal that can fall (request rate, model-call latency or failures), or relabel metabolic energy as a simulation on every surface. Also state that the survival-instinct levers are inert until then. [docs/VISION_FIDELITY_LEDGER.md v5 R6.1, standing STUB, refutation survived] (found W476 ledger v5)
    FU-131 [high] [p 29.3] sweep api.py: 2 Tier-1 truth defects (C7,C9) — Clicking Approve on a pending stage proposal shows the toast 'Proposal approved — stage… — S10.1 C9: Clicking Approve on a pending stage proposal shows the toast 'Proposal approved — stage advanced.' → The vote handler sets project.stage = proposal.to_stage without checking the project's current stage, and it swallows any…; S12.6 C7: 'AI-powered product workflows', 'generate your first AI deliverable', 'Generating…', then 'Latest output'.… → The stream is the deterministic floor echoing its own prompt ('Structured go-to-market frame for: Generate a detailed Concept… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-141 [high] [p 28.0] sweep constitutional_gaas.py: 1 Tier-1 truth defect (C8) — Green badge 'NOMINAL', 'Error Rate 0.0', 'Breaker Threshold 0.2' for the live… — S10.4 C8: Green badge 'NOMINAL', 'Error Rate 0.0', 'Breaker Threshold 0.2' for the live constitutional engine… → The card reads the breaker of the /gaas router's own 'sovereign-node' interceptor, which only POST /api/v1/gaas/intercept uses.… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-148 [high] [p 27.3] sweep api.py: 1 Tier-1 truth defect (C1) — ' Slides · Web Player Ready' with a 'Launch Player' button — S4.7 C1: ' Slides · Web Player Ready' with a 'Launch Player' button → On the streaming path the page hard-codes metadata {format:'md', title:type}, so slides_count is undefined and nothing checked… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
  P2.3 — Avatar + profile honesty
    FU-191 [medium] [p 6.8] sweep api.py: 1 Tier-2 shortfall (C7) — The user attaches an image and asks 'Describe this image.'; a reply appears. A user with… — S10.11 C7: The user attaches an image and asks 'Describe this image.'; a reply appears. A user with a non-English… → The backend returns image_understood:false and image_served_by:null, and language:null when the floor could not honour the… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
  P2.4 — The scatter: 67 ops in 38 clusters, 3–4 per round, audit-before-wire, retire freely
    FU-162 [medium] [p 26.4] sweep deliverables.py: 2 Tier-2 shortfalls (C7) — The export subtitle reads 'report · produced on Workstation IDBO's own AI fabric… — S3.12 C7: The export subtitle reads 'report · produced on Workstation IDBO's own AI fabric (in-house ·… → All 11 producing calls were the deterministic floor (source_served_by {native:11}). The export carries no 'structured floor —…; S6.14 C7: Row subtitle 'report · v1 · native' (or '· verbatim-ingest') → The raw served_by token is printed and never goes through provenanceBadge, so a floor-served row reads 'native', which looks… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-209 [medium] [p 25.0] sweep ReligionHub.tsx: 1 Tier-2 shortfall (C2) — 'Moral alignment checks run through the real §11 compliance engines (Halal/Sharia ·… — S9.9 C2: 'Moral alignment checks run through the real §11 compliance engines (Halal/Sharia · Ethical).' The button… → The §11 Halal/Sharia and Ethical engines are keyword/bare-word screens (R1.0, R3.4), not moral-alignment judgement. Nothing on… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-160 [medium] [p 24.5] sweep quality.py: 3 Tier-2 shortfalls (C1,C5) — Tooltip '7 biomimetic layers · self-managing · improving · healing'. Chip 'organism:… — S3.8 C5: Tooltip '7 biomimetic layers · self-managing · improving · healing'. Chip 'organism: immune 100% ·… → The record itself says 1 of 7 layers contributed (layers=['Immune']; layers_note: '1 of 7 declared biomimetic layers contributed…; S3.18 C1: 'ethical: pass — human: pass; environment: pass; quality: pass; value: pass (engine-backed)', directly under… → assure_delivery threads the floor's delivery_coverage into the ethical engine even when not_assessable is true, so the ethical…; S10.7 C1: Hovering the 'QMS —' chip on a floor-served clinical care plan, safeguarding triage, handover, legal… → The gate itself records that floor output cannot be assessed ('coverage cannot fail by construction'). Even so, that same floor… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-161 [medium] [p 22.3] sweep DomainTool.tsx: 3 Tier-2 shortfalls (C5,C7) — The downloaded or copied file is titled with the tool name (e.g. '<h1>Comparative Fiqh… — S9.2 C7: The downloaded or copied file is titled with the tool name (e.g. '<h1>Comparative Fiqh Research</h1>' or… → The export drops every disclosure the response carries. The fatwa research loses 'It is NOT a fatwa and does not constitute a…; S9.8 C5: The My Work record of a faith or employment tool output after one refine carries a 'refined ×1' chip. → run() saves text + [floor_note] + disclaimer (W456: disclosures travel with the saved text). The refine writer replaces output…; S10.10 C7: The downloaded care plan, legal document or marking feedback file. → exportText is score_summary + displayText. The disclaimer the screen shows ('must be reviewed and validated by a qualified… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-185 [medium] [p 20.8] sweep religion.py: 1 Tier-2 shortfall (C6) — Hub copy: 'Workstation's own AI researches its narration, isnad, grading and sharh' and… — S9.7 C6: Hub copy: 'Workstation's own AI researches its narration, isnad, grading and sharh' and '…researches it… → On the floor these headings are followed by keyword bigrams ('- hadith number - authenticated collections') and a 'service… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-205 [medium] [p 17.5] sweep DashboardNew.tsx: 1 Tier-2 shortfall (C4) — 'One living, biomimetic organism that is simultaneously all five — generated end-to-end,… — S6.18 C4: 'One living, biomimetic organism that is simultaneously all five — generated end-to-end, self-running,… → The autonomy levers are off by default: heartbeat status shows auto_evolve, auto_economy, auto_align, auto_compliance and… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-208 [medium] [p 17.5] sweep EmploymentHub.tsx: 1 Tier-2 shortfall (C10) — A header button labelled 'Career Path'. — S9.11 C10: A header button labelled 'Career Path'. → It opens the Application Studio tab and scrolls to 'input-materials-section'. It does not open the hub's own 'Career Path' tool… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-180 [medium] [p 16.1] sweep intelligence.py: 1 Tier-2 shortfall (C7) — Stage analyses for the user's challenge, 'Positioning wedge from small-scale… — S6.4 C7: Stage analyses for the user's challenge, 'Positioning wedge from small-scale beekeepers', 'Positioning wedge… → The gateway's default augment=True puts token-overlap recall of OTHER interactions (another run's Yorkshire beekeeper Genesis… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-184 [medium] [p 13.6] sweep qep_intelligence.py: 1 Tier-2 shortfall (C3) — ease_factor row rationale: 'Higher ease ⇒ longer interval; the learner retains this ayah… — S13.8 C3: ease_factor row rationale: 'Higher ease ⇒ longer interval; the learner retains this ayah well.' → The rationale is a fixed string emitted for every ease value, including the floor 1.3 (a learner struggling with the ayah). It… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-170 [medium] [p 12.3] sweep ReactorStudio.tsx: 2 Tier-2 shortfalls (C2,C5) — 'Max Q1 (240)' names one leader. — S5.9 C5: 'Max Q1 (240)' names one leader. → The backend was fixed (W433) to report ties: analytics.max.tied_with = ['Q3']. The page's StudioResult type and the row renderer…; S5.12 C2: The tooltip reads '§11 live compliance — sharia_halal:pass · uk_legal:review · regulatory:pass · ehs:pass ·… → The backend reasons say 'halal vocabulary present and no prohibited (haram) term — a keyword screen, not a certification',… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-171 [medium] [p 12.3] sweep gateway.py: 1 Tier-2 shortfall (C3) — The floor's '## Key factors' / bullet lists are presented as the subject's own factors… — S4.6 C3: The floor's '## Key factors' / bullet lists are presented as the subject's own factors ('grounded in the… → gateway._augment prepends up to N unrelated prior interactions matched by token overlap, labelled 'use only if relevant'. The… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-172 [medium] [p 12.3] sweep homeostasis.py: 1 Tier-2 shortfall (C10) — A feed of up to 25 signals, each with a coloured type chip, plus arousal 'ALERT' — S8.16 C10: A feed of up to 25 signals, each with a coloured type chip, plus arousal 'ALERT' → The API returns signal_type/age_seconds but the page reads sig.type, so every type chip renders empty in the fallback grey. The… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-202 [medium] [p 12.0] sweep SwarmIntelligence.tsx: 1 Tier-2 shortfall (C4) — '[--:--:--] READY: Swarm intelligence online — waiting for orchestration signal.' in a… — S11.2 C4: '[--:--:--] READY: Swarm intelligence online — waiting for orchestration signal.' in a green log-styled… → Nothing streams and nothing waits: the panel is a static fallback string rendered whenever GET /api/v1/swarm/runs yields no… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-164 [medium] [p 11.2] sweep products.py: 2 Tier-2 shortfalls (C7,C10) — 'AI Production Lines · Real Artefact Generation'; green 'done'; an exported… — S8.11 C7: 'AI Production Lines · Real Artefact Generation'; green 'done'; an exported '<name>-<run>.md' titled with… → The done event's served_by:'native' is dropped, so there is no provenance chip, and the export's header carries no provenance.…; S13.9 C10: '2 active projects across 2 realm(s)', '1 concept-stage project(s) ready to run', '1 prototype(s) eligible… → 'active' counts every project regardless of status (live: statuses 'idle' and 'done'). 'ready to run' counts concept-stage… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-204 [medium] [p 10.5] sweep Contribute.tsx: 1 Tier-2 shortfall (C4) — 'Governance is shared between the AI-led Council and the Open Source Steering… — S7.9 C4: 'Governance is shared between the AI-led Council and the Open Source Steering Committee.' and 'Workstation… → Neither body exists anywhere in the codebase (no match for 'Steering Committee' or 'AI-led Council' under agentic_core/). The… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-206 [medium] [p 10.5] sweep SolutionsPlatform.tsx: 1 Tier-2 shortfall (C10) — The selector offers 'Ollama · llama3', 'Ollama · mistral', 'Ollama · deepseek-r1' and… — S5.3 C10: The selector offers 'Ollama · llama3', 'Ollama · mistral', 'Ollama · deepseek-r1' and 'External ·… → The choice only goes into the prompt text, and the backend discards that text anyway (see the 'message' field mismatch). No… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-212 [medium] [p 10.5] sweep SovereignEvolution.tsx: 1 Tier-2 shortfall (C5) — Page load shows 'Organism Introspection' (Projects, Immune Health, CPU, Items… — S13.6 C5: Page load shows 'Organism Introspection' (Projects, Immune Health, CPU, Items Proceeding) and directives as… → GET /roadmap returns the LAST saved cycle, which can be arbitrarily old. The page shows cycle_id and duration but not… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-214 [medium] [p 10.5] sweep HeartbeatMonitor.tsx: 1 Tier-2 shortfall (C4) — 'Self-run: Operates each living VSB on the beat…' and 'Self-defend: Re-screens every… — S9.5 C4: 'Self-run: Operates each living VSB on the beat…' and 'Self-defend: Re-screens every living VSB against §11… → Each beat operates ONE VSB (operate_one, least-recently-operated) and re-screens ONE VSB (_compliance_beat, round-robin). With N… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-215 [medium] [p 10.5] sweep OrganismAnatomy.tsx: 1 Tier-2 shortfall (C5) — Blended figure captioned 'blended (20% simulated)'; the self_healing_health term chip… — S8.13 C5: Blended figure captioned 'blended (20% simulated)'; the self_healing_health term chip reads 'SIMULATED' → While no circuits are tracked, 60% of the blend is unmeasured: 40% defaulted self-healing plus 20% simulated ATP. The card's own… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-216 [medium] [p 10.5] sweep ProjectsHub.tsx: 1 Tier-2 shortfall (C5) — After a failed run the project keeps its spinning 'running' status dot, 'Run <stage>'… — S12.9 C5: After a failed run the project keeps its spinning 'running' status dot, 'Run <stage>' stays disabled, and no… → The backend emits data:{error} and sets project.status='error'. The page throws inside the per-line try, and its own catch… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-217 [medium] [p 10.5] sweep BusinessModelDashboard.tsx: 1 Tier-2 shortfall (C3) — Beneath the amber note 'The model did not return a parseable simulation...', the… — S5.13 C3: Beneath the amber note 'The model did not return a parseable simulation...', the dashboard still shows 'QEP… → All of these are JSX literals, rendered whatever the model returned and even when it returned nothing (generated:false). W407… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-218 [medium] [p 10.5] sweep PresentationPlayer.tsx: 1 Tier-2 shortfall (C3) — The header reads 'Sovereign Studio v1.0 • Autonomous Narration Active', the footer reads… — S5.14 C3: The header reads 'Sovereign Studio v1.0 • Autonomous Narration Active', the footer reads '{n}%… → No narration audio plays and nothing is synchronised. 'n% Synchronized' is a setInterval counter (+2 every 100 ms). When the… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-219 [medium] [p 10.5] sweep ResourceFabric.tsx: 1 Tier-2 shortfall (C1) — 'Project and compare the outcomes of what-if scenarios against a subject — in-house,… — S4.22 C1: 'Project and compare the outcomes of what-if scenarios against a subject — in-house, ranked, QMS-gated.' → On the floor, the 'Ranking' section is a generic scaffold ('Generate ≥3 distinct variants...') with no ranking. The QMS gate… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-203 [medium] [p 10.4] sweep toolRegistry.ts: 1 Tier-2 shortfall (C6) — Tafsir card: 'Structured tafsir of an ayah … drawing on the classical mufassirun.'… — S13.11 C6: Tafsir card: 'Structured tafsir of an ayah … drawing on the classical mufassirun.' Header: 'every one on… → Under this environment every tool is served by the deterministic floor. The tafsir route's own floor_note says the notes are 'a… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-175 [medium] [p 9.5] sweep career.py: 1 Tier-2 shortfall (C7) — On screen each generated document carries the amber 'structured floor — not model… — S12.11 C7: On screen each generated document carries the amber 'structured floor — not model analysis' badge, but the… → The downloaded .md holds only doc.content, whose only marker is 'owned, no external dependency', so the floor disclosure is lost… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-176 [medium] [p 9.5] sweep cognition.py: 1 Tier-2 shortfall (C4) — 'The organism self-aligns: … routes each gap to the tier that owns it, governed and… — S7.5 C4: 'The organism self-aligns: … routes each gap to the tier that owns it, governed and continuous.' After the… → The button posts execute:false, so nothing is sent to any tier. Every gap returns executed:false with the note 'Set execute=true… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-178 [medium] [p 9.5] sweep forge.py: 1 Tier-2 shortfall (C7) — 'resources process', each stage named for a fabric engine, '· governance allowed',… — S8.12 C7: 'resources process', each stage named for a fabric engine, '· governance allowed', 'Integrated Deliverable' → Every stage is a persona prompt through gateway.query_meta, not the fabric's engines. ai_provenance {native:5} is dropped by the… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-179 [medium] [p 9.5] sweep integration_surface.py: 1 Tier-2 shortfall (C10) — 'Recent Project Activity' lists commits. The Channels icon shows continuously animating… — S13.12 C10: 'Recent Project Activity' lists commits. The Channels icon shows continuously animating equaliser bars on… → The list is `git log` of the server's working directory (the Workstation codebase itself), not the user's project activity. It… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-187 [medium] [p 9.5] sweep sovereign_evolution.py: 1 Tier-2 shortfall (C9) — Ticking the box and running a cycle suggests the items go to governance. Nothing is… — S13.5 C9: Ticking the box and running a cycle suggests the items go to governance. Nothing is shown when nothing was… → On the floor the only directive is the defaulted P2 'maintenance' item, so the submission filter (P1 or correction) selects… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-167 [medium] [p 8.0] sweep api.py: 2 Tier-2 shortfalls (C4,C5) — A URL fetch/ingest capability. On failure: 'URL ingestion failed. Check the URL and try… — S4.16 C4: A URL fetch/ingest capability. On failure: 'URL ingestion failed. Check the URL and try again.' → Nothing is fetched. Every URL except one hard-coded DeepSeek share link gives HTTP 500 (UploadFile constructed without a file),…; S12.12 C5: Clicking Remove takes the file off the slot, and the API answers {status:'DELETED'}. → Only the registry row is removed. The uploaded bytes stay in DATA_DIR/uploads, and the extracted (or fabricated) text stays in… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-199 [medium] [p 6.8] sweep api.py: 1 Tier-2 shortfall (C7) — 'Synthesis Complete · 1 Output Generated' with a green check under 'Multi-Modal AI… — S4.12 C7: 'Synthesis Complete · 1 Output Generated' with a green check under 'Multi-Modal AI Output Generation'. No… → The /stream done frame carries served_by:'native', is_external and profile_applied (added in W451 so SSE consumers could tell… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-190 [medium] [p 6.2] sweep app_mvp.py: 1 Tier-2 shortfall (C3) — A state label 'Work' (aria 'Mesh Work'), a green 'healthy flow' cardiovascular dot, and… — S11.14 C3: A state label 'Work' (aria 'Mesh Work'), a green 'healthy flow' cardiovascular dot, and a pink 'Oxytocin… → The label is inverted. resource_flow = 100 − host CPU%, and the hook calls anything >60 'WORKING', so an idle host (low CPU, no… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-201 [medium] [p 5.8] sweep registry.py: 1 Tier-2 shortfall (C1) — After re-verify, VBSSystemsPanel.tsx:79 shows 'closed — the corrected delivery PASSED… — S9.1 C1: After re-verify, VBSSystemsPanel.tsx:79 shows 'closed — the corrected delivery PASSED the same gate,… → A cockpit-gate defect stores no section requirements. Its re-verify therefore only checks that the pasted text is at least 200… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-077 [medium] [p 3.4] The ontology engine serves empty graphs and the one real ontology (Law, under knowledge/) is unwired — agentic_core/reactor/domains/ontology_engine.py reads agentic_core/data/ontologies/ which holds nothing, reached from the domain weaver (a v138 CEO tool) — every domain query answers an empty graph; knowledge/Law/EmploymentTribunal/ontology/*.json is never loaded. Wire the Law graph or retire the engine (audit-before-wire). (found W473 refuter)
    FU-076 [medium] [p 3.1] pqc_hardening.py stamps a SHA3 digest with a fixed built-in key as a 'Dilithium5 signature' — relabel or retire — agentic_core/security/pqc_hardening.py is not a post-quantum scheme; gaas.py and qep_flagship.py record its output as pqc_signature, which reads as cryptographic assurance the code does not give. Retire the field or name it a content hash. (found W473 refuter)
    FU-071 [low] [p 2.6] Nine source-pointer product directories are still listed as products of a kind — The catalogue now marks them status source ('a pointer, nothing served yet') and no consumer builds from them, but products/ still holds nine metadata.json directories (business_incubator, cognitive_scraper, gse, molecular_sdk, nanophotonic_navigation, scraping_suite, uviap, mjm-intelligence-engine, signature-product-suite) whose only substance is a pointer at SDK source. Fix: for each, either serve it (a route and a real page) or retire the directory; the scatter item decides which, per the reach audit. (found W470)
    FU-072 [low] [p 2.6] The six legacy signature-product directories still sit in products/ with self-declaring manifests — products/Care … products/Science each carry a manifest.json self-declaring PRODUCTION_READY, WCAG 2.2 AAA and nine injection formats that nothing serves; W470 lists them as legacy archives and routes nothing to them, but the directories remain where a reader takes them for products. Fix: move them to _archive/products/ (LEGACY_ARCHIVES then empties) and keep one line in the catalogue saying they were archived. (found W470)
    FU-078 [low] [p 2.6] geospheric/resilience.py ('LSTM' self-healing) is unwired dead code — agentic_core/biomimicry/geospheric/resilience.py holds a hand-rolled 'LSTM' over a JSON model file; nothing imports it. The organism's real self-healing is agentic_core/organism/self_healing.py. Retire it or wire it honestly (audit-before-wire). (found W473 refuter)
    FU-220 [medium] [p 2.2] relocate_data_store calls a directory populated because a file exists — FU-079's two 'populated' chroma_db copies held 0 and 1 entries — FU-079 was registered as 'two populated copies' of chroma_db because plan() marks a directory CONFLICT when it is non-empty (any file). Read W477: the legacy copy's conversation_memory collection holds 0 embeddings; the repo copy holds 1 (a 30 March test exchange). The Owner ruled 2026-09-19: the repo copy is live, the legacy copy is retired and left on disk untouched. Fix: a directory is populated only when it holds data (for a Chroma store, count the embeddings; for a SQLite file, rows in its tables), and the report states the counts; guard with an empty-store fixture. (found W477 (FU-079 ruling))
    FU-075 [low] [p 1.9] Read-only readers still use load_json_tolerant; retire the tolerant loader once every writer is strict — W472 made every WRITER read strictly (config.read_json_strict). The read-only readers that summarise or list — revenue._load (pending_summary), ueg._read (recent), agent_hub listing reads, integration_surface listings, resource_fabric composition/swarm listings, swarm proposed_catalogue/org_cascade_runs listings, business_plan._load — still use load_json_tolerant or a bare json.loads with a fallback: honest as readers (they never write back) but a listing over an unreadable store shows fewer rows without saying so. Fix: give each listing an 'unavailable' answer via read_json_strict and delete load_json_tolerant when no caller remains. (found W472)
    FU-228 [low] [p 0.9] intelligence.py keeps the unused cascade and MJM singletons W479 stopped calling — W479 removed the stub cascade call from the BDP/SPI stream; agentic_core/api/intelligence.py still imports UltimateCognitiveCascade and MJMOrchestratorV4 and instantiates _cascade and _mjm at import, which now nothing uses. FIX: remove them with the P3.12 engine work (they are the same objects that item rebuilds). (found W480 review of the 12-engine cognitive architecture proposal)
  P2.6 — The perimeter and the gate
    FU-177 [medium] [p 20.8] sweep compliance.py: 1 Tier-2 shortfall (C1) — The headline card for the subject 'asdf qwerty' shows a green check and 'PASS'… — S10.2 C1: The headline card for the subject 'asdf qwerty' shows a green check and 'PASS' (compliant:true). 'A halal… → No row read the gibberish subject. Sharia and UK-legal return 'review — no engine covers this area' (coverage none), and… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-173 [medium] [p 18.2] sweep board.py: 1 Tier-2 shortfall (C7) — '1 objective(s) landed on this entity's plan · gaas: allowed', followed by the Chief's… — S1.3 C7: '1 objective(s) landed on this entity's plan · gaas: allowed', followed by the Chief's directive text shown… → The directive is floor output (ai_provenance.served_by {native: 2}). It never mentions the Owner's instruction: it is n-grams of… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-157 [medium] [p 16.8] sweep change_control.py: 5 Tier-2 shortfalls (C1,C2,C7) — After Implement, the record shows status 'IMPLEMENTED' (blue Zap) and counts toward the… — S1.10 C1: After Implement, the record shows status 'IMPLEMENTED' (blue Zap) and counts toward the 'Implemented' stat. → A change submitted from this page's own form never carries config_change, so /implement applies nothing (applied: null) and…; S1.11 C1: '✓ Change auto-approved (LOW tier + healthy organism)'. 'decided by: LOW-tier auto-approval (organism… → 'Healthy' is composite_health: 40% a defaulted 1.0 (no self-healing circuits tracked) and 20% simulated ATP, which only rises…; S1.12 C7: 'DECIDED BY RULE, NOT BY THE MODEL … The prose below is the model's and had NO bearing on the decision. ---… → The prose is the deterministic floor, not a model. gateway.query's text is used with no served_by, so the record labels floor…; S1.13 C1: A green 'PASS' pre-validation verdict on the approved HIGH change. → The label names a health gate, but the gate is the same composite (60% defaulted/simulated) that cannot fail. The green PASS is…; S1.18 C2: Before submitting, the form shows 'Tier: LOW' for 'Config — Minor'. After submitting, a green '✓ Change… → A substring screen on the description changes the tier: 'constitution' or 'delete all' makes it CRITICAL. A typo fix on 'the… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-019 [low] [p 11.2] The evolution apply's claim release is a status-only compare-and-set — apply_approved_evolution's _release flips implemented back to approved whenever the status is implemented, without proving the implemented state is this caller's own claim (no claim nonce) — the shape W463 removed from the economy restore; not reachable today (found W463 class-sweep verifier (read))
    FU-213 [medium] [p 10.5] sweep ConstitutionalUI.tsx: 1 Tier-2 shortfall (C10) — 'UEG Audit Trail' header badge '40 events'. — S10.14 C10: 'UEG Audit Trail' header badge '40 events'. → The badge counts the 40 rows fetched (limit=40). The same page shows the chain holding 177+ events. The badge reads as a total. [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-196 [medium] [p 6.2] sweep ueg.py: 1 Tier-2 shortfall (C5) — With valid:true: 'All N constitutional events verified against the recomputed hash… — S10.13 C5: With valid:true: 'All N constitutional events verified against the recomputed hash chain' and 'Chain… → (a) verify_chain treats a missing or corrupt tail anchor as no anchor (read_anchor returns None on any error) and still returns… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-005 [medium] [p 6.0] The /api/v1/swarm router carries no auth dependency — agentic_core/api/swarm.py has zero Depends — the org cascade (POST /cascade), CEO delegation (POST /delegate), proposed-catalogue curation and the run histories are callable by anyone when AUTH_ENABLED is on; P2.6 names 'swarm' among its routers, this row pins the routes (found W460 audit (P1.12))
    FU-006 [medium] [p 6.0] The org cascade's governance verdict gates a constant string, not the delivery — swarm.py's _attest returns a fixed attestation sentence, so 'gov: allowed' can never reflect the delivered content; W460 relabelled the chip 'intent only' — the real fix is gating the delivery itself (found W460 audit (P1.12))
    FU-029 [medium] [p 6.0] Board ratification is apex-only, and the Board's other routes trust a client-supplied owner — GET/POST /api/v1/board/ratifications cover every change (admin under auth; on_owner_direction in both modes) — a VSB-scoped change is not routed to that VSB's own board or tenant owner; board.py's chief/instruct and directive still take 'owner' from the request body and carry no auth dependency (the P2.6 perimeter) (found W464 Board audit (read))
    FU-195 [medium] [p 5.8] sweep policy_gate.py: 1 Tier-2 shortfall (C2) — An emerald 'gaas: allowed' chip next to the directive, presented as the constitutional… — S2.10 C2: An emerald 'gaas: allowed' chip next to the directive, presented as the constitutional gate's verdict over… → The gaas.v5 gate is a keyword screen. The pre-gate denies only if the fixed intent string ('board_chief_instruct') contains a… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-032 [low] [p 5.2] The audit views read an Owner's rejection as a fault — classify_event flags cca.change_rejected and board.change_ratification_refused (a refusal); the Governance Hub shows them red FLAGGED and counts them with failures without rendering flag.why, and ConstitutionalUI's UEG tab ignores flag entirely (tone keyed to two event types) (found W464 UEG audit (read))
    FU-007 [medium] [p 3.4] One violation trips the shared circuit breaker, and anyone can reset it — record_event trips on a single is_violation (no threshold), halting every later action on the node; POST /api/v1/gaas/breaker/reset has no user dependency (found W460 audit (P1.12))
    FU-030 [low] [p 3.0] In single-user mode a HIGH override needs no acknowledgement, so it skips Board ratification — with auth off any client's override_decision is recorded as admin_override (the Owner's explicit decision) and a HIGH change approved that way is not queued for ratification; CRITICAL requires admin_decision_for_critical, HIGH requires nothing (found W464 ratification audit (read))
    FU-031 [low] [p 3.0] A decision whose ledger write failed leaves no mark on the record, and nothing reconciles it — Change Control writes a decision's UEG node after the record lands (W464, FU-013); a failed write or a process that dies in between leaves the decision without a node, reported only in that response (ueg_logged false) and the server log — the record carries nothing a later reconciliation could find, so the gap is invisible after the response (found W464 UEG audit (read))
    FU-033 [low] [p 3.0] A review of a change record missing rationale, affected_systems or rollback_plan answers 500 — review_change builds its prompt with c['rationale'], c['affected_systems'] and c['rollback_plan'] — a record written without them (hand-written or by an older writer) raises KeyError after _start has already moved it to under_review (found W464 (found writing the tier guard))
  P2.7 — The organism defends for real (the honest half first, then the wiring)
    FU-198 [medium] [p 9.5] sweep genome.py: 1 Tier-2 shortfall (C5) — For a mutant created seconds ago: 'encoded before provenance tracking (pre-W438) —… — S8.14 C5: For a mutant created seconds ago: 'encoded before provenance tracking (pre-W438) — whether these axes were… → Mutate and crossover records carry no trait_provenance, served_by or encoding_note, so the fallback note fires for post-W438… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-197 [medium] [p 6.2] sweep engine.py: 1 Tier-2 shortfall (C5) — Allocation result: domain 'general', share {cpu:0.1, priority:0}, status 'ACTIVE', and… — S4.21 C5: Allocation result: domain 'general', share {cpu:0.1, priority:0}, status 'ACTIVE', and the top-level status… → The requested domain is dropped: RALVerifier's result has no domain, so the allocator falls back to 'general'. 'standard' is not… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-018 [low] [p 2.6] The optimizer's resource fabric releases resources a pool never consumed — assemble_pool records the full requirements even when it could not decrement capacity, and disassemble_pool gives all of them back (gpu available 1064 of 64 at unit level); the optimizer engine assembles and releases per call (found W463 class sweep (reproduced at unit level))
  P2.8 — Bespoke swarms
    FU-159 [medium] [p 15.3] sweep swarm.py: 3 Tier-2 shortfalls (C10) — 'mgmt: bms·qms·ems·dcms·backbone' (integrated). The organism chip's hover says '7… — S11.8 C10: 'mgmt: bms·qms·ems·dcms·backbone' (integrated). The organism chip's hover says '7 biomimetic layers ·… → 'integrated' is the static registry catalogue id list, assigned before anything computes. It lists QMS although the gate was not…; S11.9 C10: '§7 fabric facilities requisitioned & RAN (1)' lists 'metabolic /api/v1/organism/status · match ×2', and its… → The 'facility' a two-word overlap selected is a status read of the organism. Its output ({mode:'FULL_POWER',…; S11.11 C10: The run card names the engaged agents ('CFO, CTO') as chosen by the CEO router. The page asks for n_agents:3. → The router can never select: it lowercases each returned id and tests it against upper-case keys ('cfo' in _AGENTS is False), so… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-207 [medium] [p 13.5] sweep NativeAI.tsx: 1 Tier-2 shortfall (C10) — 'Ensemble · 1 owned models in parallel → consensus' — S7.12 C10: 'Ensemble · 1 owned models in parallel → consensus' → Only one member ran (the native floor). synthesis is null, so no consensus exists and none is shown. The label still promises one. [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-186 [medium] [p 10.5] sweep resource_fabric.py: 1 Tier-2 shortfall (C9) — Each real facility run a composition executed is recorded as a successful outcome… — S4.19 C9: Each real facility run a composition executed is recorded as a successful outcome ('measured facility… → record_outcome(..., success=True) runs for every entry in real_runs, including entries that are {'resource', 'error'}. A failed… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-183 [medium] [p 8.8] sweep native_ai.py: 1 Tier-2 shortfall (C5) — 'Serving default: llama3.2 (env default)' — S7.1 C5: 'Serving default: llama3.2 (env default)' → No local model exists: discovered [], active_estate [], ollama available:false. /native-ai/status on the same page says… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-189 [medium] [p 7.0] sweep vbs_systems.py: 1 Tier-2 shortfall (C3) — The chip reads 'non-conformance 14%' with the title 'gate failures / gates run — a real… — S9.4 C3: The chip reads 'non-conformance 14%' with the title 'gate failures / gates run — a real rate'. The catalogue… → The cockpit's Gate button runs the platform-wide shared QMS on a coverage number the user types (default 0.97, which passes) and… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-010 [low] [p 6.8] Saved cascades cannot be deleted from the designer page — DELETE /api/v1/resources/swarm/{sid} exists but the /native-ai designer offers no way to call it (found W460 audit (P1.12))
    FU-200 [medium] [p 6.2] sweep ems.py: 1 Tier-2 shortfall (C3) — A green 'EMS +85%' efficiency gain and a CO₂ figure on this run's result. — S11.7 C3: A green 'EMS +85%' efficiency gain and a CO₂ figure on this run's result. → efficiency_gain is the literal `return 0.85`, identical on every run. total_co2_kg is the process-lifetime accumulator, not this… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-008 [medium] [p 5.2] swarm_cascades.json writers are not under store_lock — define, update and delete load-modify-save the store with no lock — a threaded probe during the P1.12 audit lost 38 of 40 concurrent writes (found W460 audit (P1.12))
    FU-009 [low] [p 2.6] The swarm HTTP contract drops per-stage model; runs have no run_id or UEG record — SwarmStageSpec carries role and instruction only, so a stage's model choice is silently discarded; run_swarm records the outcome under stage 1's served_by alone and writes no run id or ledger entry (found W460 audit (P1.12))
  P2.9 — The economy's flows told as they happened (virtual WST)
    FU-158 [medium] [p 28.7] sweep genesis.py: 3 Tier-2 shortfalls (C1,C7) — Headed as the Chief's Opening, with no provenance badge (provenance.served_by null).… — S1.24 C7: Headed as the Chief's Opening, with no provenance badge (provenance.served_by null). Vision: 'A self-running… → The summary and vision are code templates filled from the problem statement at establish. Neither the Chief nor a model composed…; S3.13 C7: The heading reads 'Chief's Opening — Executive Summary · Concept · Vision' with the amber badge 'structured… → Executive summary, vision, mission and strategy are code templates written by _seed_plan_from_journey. Neither the Chief nor the…; S3.19 C1: 'governance: allowed', shown even beside 'compliance: fail' on a fully vetoed journey. → The gaas.v5 gate screened only {intent:'genesis_journey', domain}, never the content. The SSE path discloses this scope ('not… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-165 [medium] [p 26.4] sweep vsb.py: 2 Tier-2 shortfalls (C4) — 'Generation 1 · 1 proposals · repo: re_shipped' — S1.21 C4: 'Generation 1 · 1 proposals · repo: re_shipped' → The generation counter is incremented and saved before anything evolves. The proposals only open a MEDIUM CCA (cca-610199822a,…; S2.11 C4: The CEO + C-Suite + CoE agent hierarchy was 'configured' for this VSB → swarm_config is a constant dict of role descriptions (the domain word is interpolated). No agents are instantiated or… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-169 [medium] [p 26.4] sweep VSBCockpit.tsx: 2 Tier-2 shortfalls (C5,C10) — Cockpit tile 'reserves 2,020'. Board pack 'Reserves 2,020 WST' beside 'Balance sheet… — S1.19 C5: Cockpit tile 'reserves 2,020'. Board pack 'Reserves 2,020 WST' beside 'Balance sheet 2,019 WST assets'. → The live double-entry reserve fund is 2,019: a 1 WST inter-VSB transfer left it. 'balances' is a cumulative legacy view that…; S1.20 C10: 'Giving back: [object Object]' → giving_back is an object ({budget_wst, grants…}). The generic String(val) render prints '[object Object]' instead of the amount… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-174 [medium] [p 20.5] sweep business_plan.py: 1 Tier-2 shortfall (C7) — 'Chief workflow-tree · decision: — · consensus: none · 6 nodes · UEG …', then the tree's… — S1.4 C7: 'Chief workflow-tree · decision: — · consensus: none · 6 nodes · UEG …', then the tree's final text shown as… → Every node was floor-served. The API response strips the tree's per-node served_by trace, so no surface can label the 'final'… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-181 [medium] [p 15.9] sweep management_systems.py: 1 Tier-2 shortfall (C10) — Under this VSB's Living Systems tab, nine 'living management systems' are listed,… — S1.16 C10: Under this VSB's Living Systems tab, nine 'living management systems' are listed, including ISO 27001:2022,… → The list is a constant catalogue the API calls 'supported management standards'. Nothing operates an ISMS, OH&S system, CMMI… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-193 [medium] [p 15.9] sweep metabolism.py: 1 Tier-2 shortfall (C4) — 'Capital-preserving (waqf principle): the endowment base is protected.' — S1.23 C4: 'Capital-preserving (waqf principle): the endowment base is protected.' → capital_preserved enforces only that the capital_fund waterfall share is > 0 (metabolism.py:67). No endowment base is recorded… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-168 [medium] [p 15.8] sweep Settings.tsx: 2 Tier-2 shortfalls (C1,C4) — Emerald 'Voice dictation works in your language.' shown for every language — S6.17 C1: Emerald 'Voice dictation works in your language.' shown for every language → Dictation uses the browser's Web Speech API (DictateButton rec.lang = prefs.language). Whether it works depends on the browser…; S9.10 C4: Settings says 'guidance and tone drive the affordances shown on the domain hubs'. Every hub shows '{Guided}… → No component reads guidedMode or tone except the provider that turns them into these two badge labels. No affordance changes,… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-210 [medium] [p 13.5] sweep BusinessPlan.tsx: 1 Tier-2 shortfall (C5) — The spinner stops and nothing appears. The page's own comment (W329) says 'actions never… — S3.15 C5: The spinner stops and nothing appears. The page's own comment (W329) says 'actions never fail silently'. → A 409 from a pending Mode-3 review gate, or any non-ok or non-JSON answer, is swallowed. The Owner is not told the delivery was… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-188 [medium] [p 13.3] sweep transformation_orchestration.py: 1 Tier-2 shortfall (C5) — Under '## Components' the first entry is 'Chief (owner twin)' — S8.9 C5: Under '## Components' the first entry is 'Chief (owner twin)' → No twin model exists. The same spec, two lines above, says 'Chief of the Board — … (no twin model is trained; Mode 2 planned,… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-163 [medium] [p 11.2] sweep economy.py: 2 Tier-2 shortfalls (C4,C8) — A posted transfer or a recorded return will be consumed by 'the next metabolic cycle' — S2.16 C4: A posted transfer or a recorded return will be consumed by 'the next metabolic cycle' → With the Self-run lever off (this deployment; the entity's living statement says 'autonomous economy cycles are OFF'), no next…; S3.14 C8: 'quality QMS not assessable · coverage 100% · 0 defects/3 gates · compliance review · served by native 22'. → On floor output coverage 1.0 'cannot fail by construction' (qms_basis), and 0 defects comes from gates that cannot fail. Both… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-166 [medium] [p 11.2] sweep charity.py: 2 Tier-2 shortfalls (C3,C5) — 'Ranked by urgency × gravity × reach × marginal-impact × trust', with a 'score 1.0' per… — S1.17 C3: 'Ranked by urgency × gravity × reach × marginal-impact × trust', with a 'score 1.0' per grant, under… → The API says the weights are editorial constants ('no needs, impact or trust data is measured or sourced'). Every grant carries…; S3.17 C5: 'Directives saved' and 'set by you · <timestamp>', with the four default priorities shown again. → set_directives replaces an empty priorities list with the 2026-06-21 defaults (`… or _PRIORITIES`), then stamps updated_at, so… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-074 [low] [p 11.2] The Cockpit's plan tab has no owner-edit surface and no owner-edited marks — W471 wired the owner-edit form (POST /business-plan/set with clear) and the owner-edited marks into BusinessPlan.tsx only; VSBCockpit's plan tab shows the Chief's Opening with its provenance badge and pending list but the founder cannot set or clear a field there and set fields are not marked. Fix: mount the same edit form and marks on the Cockpit's plan tab (one component shared by both pages). (found W471)
    FU-211 [medium] [p 10.5] sweep ManagementSystemsHub.tsx: 1 Tier-2 shortfall (C7) — The downloaded file carries only the floor's own marker line '_[Workstation native… — S2.13 C7: The downloaded file carries only the floor's own marker line '_[Workstation native structured engine —… → The floor_note shown on screen ('not model analysis. Review every clause before use.') is dropped from the export. A reader of… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-192 [medium] [p 9.5] sweep living_vsbs.py: 1 Tier-2 shortfall (C10) — An emerald '1 cycles · last 2026-09-19' for vsb-7b309134bc. — S1.22 C10: An emerald '1 cycles · last 2026-09-19' for vsb-7b309134bc. → The ledger holds three cycles, two of them Owner-run from this page. operating_cycles and last_operated count only roster visits… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-182 [medium] [p 8.8] sweep marketplace.py: 1 Tier-2 shortfall (C5) — An emerald 'pass' pill under '§11 compliance screen', followed by 'framework: status'… — S12.7 C5: An emerald 'pass' pill under '§11 compliance screen', followed by 'framework: status' rows. After Save:… → The screen API (compliance.screen_compliance) returns a 'basis' ('a pass is a pass of the screen, not a certification'),… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-194 [medium] [p 8.8] sweep ventures.py: 1 Tier-2 shortfall (C3) — Candidates are 'ranked' and the next cycle's allocation 'selects from these'. The module… — S2.12 C3: Candidates are 'ranked' and the next cycle's allocation 'selects from these'. The module says selection is… → The scores are policy constants keyed on whether a board exists and whether a cycle ran, so every governed VSB gets an identical… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-059 [low] [p 7.3] The economy pages keep earlier figures beside a new refusal — VSBEconomy.runCycle and VSBCockpit leave the previous cycle's report and balances on screen under a refused or partly written cycle; the cockpit shows nothing for a 200 hold (cycle null), its other actions (growth, chief, transformation, deliverables, ship state) are not tied to the selected entity, avatars/api.py reads the raw roster hold (stale after a repair, and blind to decision_hold and last_error), and doClosePeriod parses a non-JSON error body as JSON. Fix: clear or label the stale figures, render the hold, and guard every entity-scoped load as W468 guarded the ledger. (found W468 first refutation (reproduced))
    FU-034 [medium] [p 5.2] A service contract can be offered to an entity that is not living, and nothing declines or cancels one — offer_contract never checks that the client and provider are registered living entities: the W465 probe offered a contract to a provider id that exists nowhere, accepted it, and delivered it (a whole provider-scoped org cascade ran — 15-25 minutes on a local model) before settle refused the transfer with 404. There is no decline for the provider or cancel for the client, so such a contract sits 'delivered' forever. Fix: validate both parties at offer (and again at accept), add decline/cancel with their own UEG events, and let the page offer them. (found W465 audit (read) and probe (reproduced))
    FU-035 [medium] [p 4.8] A settlement's materiality approval is bound to the client-provider pair, not to the contract — A contract settlement goes through the transfer gate, which binds an approval to the sender, the counterparty and an amount ceiling (W463). Two material contracts between the same client and provider therefore share one hold identity: the Owner's approval of contract A's settlement releases contract B's settlement of an equal or smaller price if B settles first, and A is then asked again. Virtual WST. Fix: carry the contract id into the gate's action identity (source 'contract:<id>') so a hold, an approval and a rejection name exactly one contract. (found W465 audit (read))
    FU-036 [medium] [p 4.8] A failed owner accrual is reported but never re-applied, so the Owner's balance stays short — Since W465 a cycle whose owner accrual fails says so (owner_accrual.accrued false, economy.owner_accrual_failed on the UEG, an error log) — but nothing re-applies the missing credit: the ledger shows the owner stage distributed while owner payments never received it. Fix: record the failed accrual durably (the UEG event carries vsb, amount and cycle), and reconcile on the next successful accrual or heartbeat — re-apply each unreconciled failure once, idempotent on its cycle id. (found W465 audit (read))
    FU-039 [low] [p 4.8] A settle that raises leaves the previous attempt's unpaid outcome on the contract — settle_contract records an outcome only when the transfer answers; any exception exit (a crash after the debit, a 503 from the ledger or the pending store) releases the claim and leaves the settlement field of an EARLIER attempt, so the page can still show 'held for the Owner' after the Owner approved and the latest attempt failed for another reason. Nothing is paid twice and settling again completes it. Fix: on an exception exit, record outcome 'unknown' with the error (inside the release mutation), and let the page say settle again. (found W465 third refutation (reproduced, pre-existing))
    FU-040 [low] [p 4.8] A cycle swallows a failed venture-returns intake silently, and the Board page cites a server log it may not have — W465 made a failed inter-VSB receipts intake visible (inter_vsb_receipts_error, a warning log) and made the gate measure only receipts the intake can take; consume_pending_returns in the same cycle still swallows every error as 0 recycled with no report or log, and its peek may read differently. Separately BoardOfDirectors.tsx tells the Owner to 'see the server log' when a ratification's ledger entry did not land — check that the server logs that case (the W465 owner-accrual alert did not until the third refutation). (found W465 third refutation (read))
    FU-063 [low] [p 4.4] Visit outcomes are reported inconsistently across heartbeat, genesis and pages — heartbeat counts a held or refused visit (ledger_unavailable, compliance or governance hold) as an operate_vsb action and sets last_vsb_operated; genesis's streaming establish says 'cycle ran' for an operate_vsb result that has only an error, and a result {error, cycle_ran True} (a cycle that posted and whose roster bookkeeping raised) is counted as not operated; list_living shows statuses that are not holds (intake_unavailable, intake_consumed_elsewhere) as 'held by governance'; a gate-error hold (no Change Control record) is kept on a raise as if it were a decision; the compliance branch's roster write sits outside the try (a raise there leaves last_operated unchanged); and two visits of one entity at once can clobber each other's row. Fix: report held, refused, raised and ran as four outcomes everywhere. Related to FU-045. (found W468 first refutation (reproduced))
    FU-017 [low] [p 2.6] A marketplace purchase can charge the buyer without recording the sale — consume_tokens runs before the listing save and the receipt write; if either raises there is no refund, so the buyer is charged for a sale nothing records (consume-without-compensation) (found W463 class sweep (read, not reproduced))
    FU-037 [low] [p 2.6] A second delivery of the same contract runs a whole cascade before it is refused — deliver_contract binds its result with a compare-and-set only after the cascade returns (W465), so a second Deliver while the first runs starts a second provider-scoped org cascade (15-25 minutes on a local model) whose work is then discarded with 409 'another delivery bound first'. Fix: claim the delivery before the cascade (as settle claims), release it if the cascade raises. (found W465 audit (read))
    FU-057 [low] [p 2.6] A transfer refused on a retry says nothing was debited although an earlier attempt may have — _transfer_core answers any SenderLedgerUnavailable with X-Transfer-Debited: false and 'Nothing was debited' (true of this request only): a settlement retried under its persisted transfer id, whose first attempt debited, is told nothing was debited once the ledger becomes unreadable. And a gated action that raised is retried outside the gate (W463 design), so a refusal inside the action runs again ungated. Fix: say 'this attempt debited nothing; an earlier attempt under this id may have' and keep the retry inside the gate's decision. (found W468 second refutation (reproduced))
    FU-064 [low] [p 2.6] The roster's ledger-hold text reads every held entity's whole ledger on each call — list_living describes a ledger_unavailable hold from a live strict read of that entity's ledger; the heartbeat and pages call it often, and with large ledgers this is seconds per call (4 s for 60 held rows of 4 MB, measured). Negligible at today's sizes. Fix: cache by the file's size and mtime. (found W468 second refutation (reproduced))
    FU-065 [low] [p 2.6] A ledger that keeps reserves only in the legacy balances refuses every transfer — A ledger written before W256 holds entries and balances but no accounts: validate_transfer reads reserve_fund from accounts (0.0) and refuses any transfer as insufficient funds, although the legacy view shows reserves. Fix: say the ledger predates double entry, or migrate it once. (found W468 second refutation (reproduced))
    FU-045 [low] [p 2.4] The heartbeat drops a failed entity visit silently, and revenue.consume_pending is ungated dead code — heartbeat.py:239-243 discards operate_vsb's error result, so a failed or partly posted non-material cycle leaves no trace anywhere (reproduced); and revenue.consume_pending (revenue.py:108-134) has no callers yet would consume every pending event without any gate if one were added. Fix: log the failed visit (UEG + log) and delete the dead function. (found W466 pre-audit of FU-023/FU-022 (reproduced))
    FU-047 [low] [p 2.4] A transfer stranded before W466 can only be found by hand — W466 completes a stranded transfer (the sender debited, the receiver never credited) only when its debit carries the receiver-leg marker written since W466: a debit made earlier cannot prove whether its receiver was credited once its id left the receiver's 50-row display window (and before W465 no durable credited-id list existed), so completing it could credit the receiver twice. POST /transfers/{id}/complete refuses such a debit (409) and the pass never lists it. Fix, if any exist: a one-off Owner-reviewed audit listing unmarked transfer_out debits with no credited-id and no display-window entry, completed individually on the Owner's decision. (found W466 pre-audit (reproduced: replaying an old id re-credited it))
    FU-048 [low] [p 2.4] A heartbeat cycle whose process stopped mid-cycle leaves the Owner's approval spent and asks again — W467 consumes a cycle's recognised events before it runs; if the process is killed between that consume and the cycle's first ledger write, the stranded-consume pass (every fifth beat with autonomous economy on) gives the events back after 15 minutes, but a material cycle's approval stays implemented without a released_action_ran marker (it reads as still in flight — the restrictive side), so the next beat files a fresh CRITICAL hold for the same events and the Owner decides twice. The economy.cycle_intake_consumed record names the approval's cca_id and consume_id. Fix: when the pass gives back a token's events, restore that approval if its trail has no released_action_ran for that consume_id (the W463 give-back rules). (found W467 first refutation (reproduced by killing a process))
    FU-058 [low] [p 2.4] A cycle whose ledger write times out answers a bare 500 — /cycle maps only LedgerUnavailable (503) and LedgerWriteRefused (409): a store_lock TimeoutError or a PermissionError from atomic_write_json during a cycle's writes still escapes as a 500 with no statement of what was written; the async governed_cycle writes no economy.cycle_raised record when its cycle raises (the heartbeat path does); and the strict read's retry sleeps block the event loop in async routes. Fix: map them with the ledger_written wording, and move the retries off the loop. (found W468 first refutation (reproduced))
    FU-060 [low] [p 2.4] A development spend posts as a distribution and two spends can overdraw the fund — spend_self_investment checks the balance on the construction snapshot and records under the lock without re-checking, so two concurrent spends each draw the whole balance (self_investment goes negative); and record('self_investment', kind='debit') posts Dr distribution_self_investment / Cr cash, the same as a distribution, so a spend increases the distribution expense; a spend that fails for any other reason (a busy ledger lock) is recorded nowhere. Fix: check inside the lock and post a development-spend account. (found W468 second refutation (reproduced))
    FU-061 [low] [p 2.4] Books near the float limit: a period close saves and then answers 500 — With balances near 1.7e308 WST (only a crafted or imported ledger reaches this; cycle inputs are bounded at 1e15 since W468), close_period's statement sums overflow to inf: the close marker is saved with an Infinity net profit and the route answers a bare 500 (JSON cannot carry inf). The ledger's save check covers balances and posting amounts, not the close marker's figures. Fix: compute the statements before saving and refuse (LedgerWriteRefused, 409) when any figure is not finite. (found W468 third refutation (reproduced))
  P3.12 — The engine contract, then the six
    FU-223 [medium] [p 13.5] /api/v1/cognitive/* returns a constant payload and reports engines_run 9, status complete — ledger v4 R4.3 (tier 2, API_ONLY, refutation SURVIVED): POST /api/v1/cognitive/cascade with two different problems returns identical output bar the echoed problem and elapsed_seconds; engines_run is the literal 6 or 9 and status the literal 'complete'. No frontend calls it, so it is API-only, but it is a public route of this platform. FIX: report what ran, or return 501 until the engines measure. (found W480 review of the 12-engine cognitive architecture proposal)
    FU-229 [medium] [p 8.4] The six cognitive engines return constants for any input — inkashaf_engine.py returns {'status':'SUCCESS','insight':'revealed'}, aqal {'status':'SUCCESS','plan':'computed'}, samajh 'grasped', soch ['A','B'], hoshiyari threat_score 0.01, iman alignment 0.99 — none reads its input (only cycle metrics can deflect them). cascade_v16 chains all six and reports status 'fully_integrated'. FU-146 covers the VSB spawn surface that SHOWS these; this row is the engines themselves. FIX: each engine measures its input or returns assessable:false with the reason. (found W480 review of the 12-engine cognitive architecture proposal)
    FU-224 [medium] [p 2.7] The consultation contract excludes the three meta engines and forces a numeric confidence — ConsultationRequest.engine is a Literal of seven names (six lenses + mjm), so niyyah, tawazun and tafakkur cannot be requested through the contract the registry declares; ConsultationResponse.confidence is a required float 0..1, which is why every implementer returns a literal (0.96, 0.88). FIX: an explicit assessable state and a provenance block, and the nine names the registry declares. (found W480 review of the 12-engine cognitive architecture proposal)
    FU-221 [medium] [p 2.5] The cognitive engine registry is never populated, and its call contract does not match the engines — CognitiveEngineRegistry._engines starts empty and nothing calls register(), so registry.get(...) raises ValueError on the first call; EngineRegistry9.get_engine_response then calls engine.process(input, context, enforcement) and reads result.payload, while the engines expose unveil_patterns / comprehend / reason / detect_anomalies / reflect / validate_values returning plain dicts. This is why agentic_core/avatars/api.py deliberately bypasses the recirculation orchestrator (its own docstring says the registry 'was never actually populated with working engines'). FIX: one binding, one call signature the engines implement. (found W480 review of the 12-engine cognitive architecture proposal)
  P3.14 — The clearance chain that can refuse
    FU-230 [medium] [p 3.0] The five-gate clearance chain cannot refuse, and writes literal strings as signatures — clearance_chain.py: tawazun_res.get('balanced', True), tahqeeq_res.get('verified', True), a missing risk_score reading as 0 — an engine returning {} clears all five gates; the attestations recorded to the UEG are the literals 'SIG_MUSHAWARA_v1', 'SIG_NIYYAH_v1', 'SIG_TAWAZUN_v1', 'SIG_TAFAKKUR_v1'. Dormant today (only the bypassed recirculation orchestrator calls it), so this must be fixed BEFORE anything is wired to it. FIX: every default blocks; each verdict records its basis. (found W480 review of the 12-engine cognitive architecture proposal)
  P3.15 — Attestations that are attestations
    FU-226 [medium] [p 6.2] Post-quantum signatures are named in five modules and never performed — Dilithium/Kyber appear as strings and descriptions in autonomy_pipelines.py, integration_surface.py, avatar_engine.py, interstellar.py and qep_flagship.py; no attestation path performs a post-quantum signature. FIX: sign a canonical payload with a named algorithm and a stated key source, verify it from a route, and use the words 'post-quantum' only when it is. (found W480 review of the 12-engine cognitive architecture proposal)
  P3.16 — The auxiliary engines and the recirculation loop
    FU-227 [low] [p 2.1] The recirculation orchestrator states stage latency targets it never measures — recirculation_orchestrator.py documents 'Target p95 latency: <500ms (SENSE -> ACT)' and per-stage budgets (<100ms sense, <500ms analyse) and measures none of them. It is not on a live path (the avatar API bypasses it and says why), so this is a dormant claim. FIX: measure each stage, record the latencies with the run, and make a breach a recorded fact before the loop is wired to the heartbeat. (found W480 review of the 12-engine cognitive architecture proposal)
<!-- followups:end -->

PHASE P1 — TRUTH FIRST (Tier 1; ~14 rounds, plus P1.15 and P1.16 added W469; no P2–P4 item ships until these do)
 P1.1 ✅ DONE W449 [ledger 1.1 + 3.11's attestation half · R1.2 R1.4 R2.0 R2.5 R3.6 R3.7 R5.2] The gate that cannot fail — class-kill. assure_delivery(served_by=…) →
      floor-served: qms_gate_passed=None, 'verified'/'specifically designed' source 'none', basis
      "not assessable — the floor emits the requested headings"; ai_text() measures against the
      prompt's own declared sections; coverage never measured against None; DomainTool/Deliverables/Genesis/
      Swarm/ResourceFabric/board-pack chips render slate '—' with the basis. ACCEPT: the NEWS2
      case, the empty-concept board pack and a floor cascade all return None; a real 900-char
      4-section document still passes; Genesis no longer attests 'ranked'/'simulated' when
      tie.detected or candidates_distinct == 1 (met:None with the reason) and EVIDENCE.md carries the
      tie / identical-candidates note beside the selected candidate; guard both ways.
      DELIVERED W449: the NEWS2 case, the empty-concept board pack and a floor cascade all return
      None with the basis; a real 900-char 4-section document still passes and a stubbed one fails
      (both-ways test); the tie withholds both ways; ten chip files route through qmsChip under a
      grep guard; the orchestrator tree's own length-proxy gate (the same class, one layer over)
      says 'not assessable' too; downstream consumers treat None as neither pass nor fail
      (plan binding 'qms_not_assessable_no_advance', no model-quality row, no cascade revenue,
      commit_ready not blocked, ship aggregate three-state, QUALITY.md 'NOT ASSESSABLE'). The
      refuter on the round's own diff found the class re-committed at two reached seams — the
      Genesis page's 'save as deliverable' ingested floor text verbatim and the gate certified it,
      and the VSB entity never carried ai_provenance so repo/webapp/mobile always got the old
      gate — both fixed in the same round and guarded in the both-ways test. What
      P1.1 does NOT close: the scaffold body itself (P1.2), the green in-house chip on the cascade
      (P1.5), the empty-concept board pack refusal (P1.14), the §10 wording (P3.0).
 P1.2 ✅ DONE W450 [1.2 · R2.0 R2.1 R2.6 R2.9] The shipped body never wears scaffold — nor a fallback name. On the floor, establish ships the founder's
      verbatim problem statement + "content pending the owned model — this enterprise has not
      yet composed its own concept" on website/webapp/mobile/BUSINESS_PLAN.md/Plan tab; the
      W434 scrubber remains for model output; provenance badged in the Cockpit. ACCEPT: a floor
      journey's public pages contain the founder's words and zero marker/engine/role vocabulary
      (grep guard over the shipped body); an Ollama-served journey unchanged; a floor fallback name
      becomes a neutral trimmed slug and the newborn card asks the founder to name the enterprise
      before it ships; re-generating the repo never regresses a shipped surface, and the ship
      manifest reports stale honestly.
      DELIVERED W450: measured first on a live floor entity (name 'VSB — I keep 40 beehives in
      Somerset and lose ', concept = INKASHAF/SAMAJH/SOCH/AQAL headings over problem bigrams on
      every surface, /repo after the birth-ship regressed the site to 471 bytes with stale=false);
      then the body resolved per field from provenance, the slug + pending name + naming endpoint
      + deferred ship, the no-regress /repo, the honest board-pack narrative and evidence excerpt.
      The guard greps the whole shipped tree for engine vocabulary and the fallback name, checks
      the founder's words and the pending state are present, that /repo leaves the shipped site
      byte-identical, that a rename marks a shipped body stale, and — the other way — that a
      model-served establishment ships its concept verbatim with nothing pending and a
      founder-named one ships at birth. Broken by blinding the resolution: the guard failed with
      the original symptom (SAMAJH text as the concept). What P1.2 does NOT close: the body's
      SUBSTANCE (only the owned model composes it — P1.3+/P2), the Cockpit's other tabs, P1.14.
 P1.3 ✅ DONE W451 [1.3 · R3.0 R4.0] The AI CEO chat on the fabric. Replace v138/ceo's stream with gateway.stream/
      orchestrator (in-house-first, honours AI_DISABLE_LOCAL, guardrails, breaker, learning
      loop, tenant memory); final SSE event {served_by, is_external}; delete the Galactic Era
      persona, the lambda "tool registration" and the canned advisory; ground the CEO in the
      Board's directives + the living plan (the §5 chain); CEOChat pill + per-message
      provenanceBadge from that event. ACCEPT: AI_DISABLE_LOCAL=1 → floor answer, amber badge,
      no roleplay strings in the CEO surface's code (the docs keep them as the record); with a
      local model → served_by shown. [ACCEPT reworded W451 — the refuter showed the original
      'anywhere in the repo' was literally false while the docs carry the record.]
      DELIVERED W451: measured live first (a 56-second llama3.2 'Galactic Council' answer with
      invented articles on a backend whose every owned surface said deterministic_floor; the
      canned advisory typed at 8 ms a character under a green pill); then gateway.stream_meta
      (the stream path had swallowed who served it, and applied neither the profile preamble nor
      the guardrail), the grounded generator, the deletions, the page. ACCEPT met: floor → the
      terminal frame says native and the page shows the amber badge on the message and the pill;
      the owned model, substituted at the one seam, is named ollama:<model>; the roleplay strings
      are gone from code (a source grep in the guard). What P1.3 does NOT close: the CEO's
      SUBSTANCE on the floor is the floor's structured frame (labelled as such); the meeting log
      still starts empty until a C-Suite meeting is called.
 P1.4 ✅ DONE W452 [1.4 · R2.2 R3.1] Mode 3 gates gate. orchestrate, cascade, /evolve, /repo/ship and establish consult
      review_gates; blocking → 409 {gate, status, blocks_progress}; Genesis panel copy honest.
      ACCEPT: rejected design gate → 409 on each mover; approved → 200; guard both ways.
      DELIVERED W452: measured live first (rejected design gate → 200 on ship, evolve, repo
      cascade, orchestrate, swarm run and establish, byte for byte the same as approved); then
      the shared guard on every mover, gates at birth, the heartbeat hold, the panel copy. The
      rule: any gated stage that is pending OR rejected blocks every mover (a human has been
      asked; nothing moves until they answer) — the ledger's R2.2 rule, chosen over R3.1's
      objective-title inference because the entity's `stage` field is frozen at birth and no
      code links a stage to a mover. What P1.4 does NOT close: a per-stage journey that pauses
      at a gate mid-run (the journey still runs every stage in one request before the entity
      exists — gates set at birth hold the SHIP, not the stages).
 P1.5 ✅ DONE W453 [1.5 · R3.4 R3.7 R5.1] provenanceBadge class-kill, part 2. All ten sites use .cls/.title; MyWork label;
      BoardOfDirectors + SwarmIntelligence use the helper; the "every badge routes through it"
      claim made true. GUARD: a test that fails on `provenanceBadge(` used with `.label` and no
      `.cls`, and on any inline `is_external ?` colour ternary in src/.
      DELIVERED W453: the guard itself found four sites the ledger had not listed (NativeAI's
      tree-run chips ×2, the Spawn Studio's swarm-run chip, the Cockpit's own W450 plan badge) —
      migrated with the rest. What P1.5 does NOT close: text-only labels that mention external
      use without colouring (a title string, a ' · external used' suffix) are outside the class;
      the class is COLOUR that contradicts the helper.
 P1.6 ✅ DONE W454 [1.6 · R5.0] Employment default tab honesty. Copy → "AI-synthesised example listings — not a live
      job board; verify every URL"; synthesis is not a "source"; fabricated url/salary/published
      dropped or labelled illustrative; ApplicationStudio renders provenance; default tab → the
      CV tools. ACCEPT: probe reads the honest copy on the default tab; badge present.
      DELIVERED W454: url and published DROPPED from the prompt and the rows (the model is told
      not to invent employers' addresses or dates), salary carried as salary_estimate and shown
      as 'est.'; every row wears 'illustrative · no live URL'; the search line says how many
      illustrative listings were synthesised and that no sources were searched, with the badge;
      broken by putting a url back on each row → the guard fails; restored.
 P1.7 ✅ DONE W455 [1.7 · R1.1 R1.3 R1.6] Compliance that reads. Constitutional row → 'not applicable to content — gaas.v5
      gates agent actions' (amber, not_checked) unless kind is an action, or validate_output on
      the subject with a label saying what it checks; router except → recorded error, never a
      pass; a FAIL verdict on a deliverable → export watermarked with the verdict (or blocked),
      list row marked; the Frameworks card labels each engine by what it actually checks ("UK Legal —
      keyword screen + employment-statute vocabulary; not legal advice"), the audit hash covers the
      subject, and anything outside a vocabulary returns 'review — no engine covers this area', never
      'pass'. ACCEPT: the prohibited-token subject no longer greens; a haram brief exports with its
      verdict on page one; two different subjects never share an audit hash.
      DELIVERED W455: all three ACCEPT clauses measured in the guard and the probe; two older tests
      that asserted 'overall pass' on a subject nothing had read now assert 'review' (they had
      encoded the overclaim); broken by making the export ship clean again → the guard fails;
      restored. Chosen and stated: a FAIL export is WATERMARKED, not blocked — the verdict and the
      Change-Control id on page one, the row and the button say so; blocking would hide the
      record the reviewer needs. What P1.7 does NOT close: the screens are keyword screens — the
      labels now say so; depth is P2/P3 work.
 P1.8 ✅ DONE W456 [1.8 · R1.0] The tafsir surface completes §11. disclaimer key; on the floor refuse the
      Translation/Transliteration sections (503 like /translation) or drop the headings with a
      floor_note; Tafsir tab renders arabic_text + arabic_source + reference + range_note; the
      QMS chip follows P1.1. ACCEPT: probe on /religion?tab=tafsir sees sourced Arabic, the
      range note for 2:1-20, the scholar line, and no "Translation" heading over floor text.
      DELIVERED W456: the ACCEPT probe passes on a fresh floor backend (sourced Arabic rtl,
      'covers 2:1-10', the disclaimer, the floor note, no Translation heading); broken by letting
      the floor's translation ship again → the guard fails; restored. What P1.8 does NOT close:
      the floor's remaining study sections are a structured frame labelled as such (floor note,
      amber badge, not-assessable chip) — substance needs the owned model.
 P1.9 ✅ DONE W457 [1.9 · R5.3] Care scoring computes. NEWS2 / MUST / Waterlow / falls arithmetic in-house from the
      published tables, returned as a deterministic `score` block rendered FIRST; AI narrates
      interpretation only; observations validated for units/completeness; copy corrected.
      ACCEPT: the assessor's case → NEWS2 6, band "urgent ward-based response"; table tests.
      DELIVERED W457: both ACCEPT clauses in the guard; broken by making nothing compute → the
      guard fails; restored. Stated: falls risk has no validated total (NICE CG161 is
      multifactorial) — a labelled factor count, never a score; a tool without a published table
      says so instead of pretending. CORRECTION to the ACCEPT wording: "urgent ward-based response" is
      the RCP LOW-MEDIUM label (a single parameter scoring 3); a 5–6 total is MEDIUM, "key threshold for
      urgent response" — the code follows the published table, not the clause. A lower-bound total
      (missing observations) gets NO band unless it is already at the top; Waterlow's special-risk
      groups are never default-filled and are additive; the Waterlow card implemented is the
      appetite-row card, not the 2005 MST revision — said so on the block.
 P1.10 ✅ DONE W458 [1.10 · R4.7 R4.8] Status honesty + disabled ≠ failed. floor_active from the most recent SUCCESSFUL
      completion; _run_model under AI_DISABLE_LOCAL raises a sentinel → tried "ollama (disabled
      by config, skipped)", no _record_model/_organism_report. ACCEPT: a model='local' call
      leaves immune health and model-health untouched and status says floor.
      DELIVERED W458: both ACCEPT clauses in the guard, broken twice (the sentinel removed; the status
      back on the per-model aggregate) — each blind failed the guard on its own; restored. Beyond the
      clause: the floor serve is now RECORDED (without it nothing could ever displace a stale row), an
      unknown resource and a spend-policy refusal are skips too, and the model-health 'deprioritised'
      badge stopped describing a stricter rule than the one that routes.
 P1.11 ✅ DONE W459 [1.11 + the CCA latents · R3.2 R6.2] Change Control enforced. Auth on the CCA (and P2.6's routers);
      submitted_by stamped server-side; override admin-only and never for CRITICAL without an
      explicit admin decision recorded as that principal (not 'cca_ai'); the docstring tiers
      implemented or deleted; twin fallback rendered "no twin model — health gate only";
      store_lock on review/twin-prevalidate/implement; requires_ratification gets a Board
      consumer or stops being set. ACCEPT: auth-ON test — non-admin override on CRITICAL → 403;
      audit_trail 'by' = the principal.
      DELIVERED W459: both ACCEPT clauses in the guard (auth ON: a non-admin override on a CRITICAL
      change → 403 and the record unmoved; the admin's decision entry by = the admin's username,
      by_verified true), broken twenty-one ways — each blind failed the guards on its own. NOT DONE, and why:
      (a) P2.6's other routers (heartbeat, genome, organism_status, sovereign_evolution, board) are
      untouched — each has its own in-process callers and belongs to P2.6; (b) requires_ratification
      was DELETED, not given a Board consumer — building a ratification queue is a product decision
      for the Owner; (c) the Sanctum's copy no longer claims a UEG entry — adding a UEG write to the
      CCA changes what the constitutional ledger holds and is the Owner's call; (d) _TIER_MAP is
      unchanged (code_change and economy_material fall through to MEDIUM by default, not by decision).
      Each is now tracked: (a) rides with P2.6; (b) was register row FU-012, (c) FU-013, (d) FU-014.
      [(b), (c) AND (d) CLOSED W464 on the Owner's rulings of 2026-09-14: a HIGH change a review approved
      waits for Board ratification (GET/POST /api/v1/board/ratifications, the Board page) and nothing acts
      on it until then; every Change Control decision is written to the UEG (cca.change_approved /
      _rejected / _retired, board.change_ratified / _ratification_refused); _TIER_MAP gives code_change
      HIGH and economy_material CRITICAL, decided under each record's effective tier. Guards:
      test_w464_board_ratifies_what_a_review_approved_before_anything_acts,
      test_w464_change_control_decisions_are_written_to_the_ledger,
      test_w464_every_material_economy_action_is_decided_by_the_owner; probe scripts/_w464_probe.mjs.]
      CARRIED FURTHER IN W463 (register FU-002, closed): this item made the economy's consume/restore a
      compare-and-set but did not bind what an approval releases — any approved record with the hold's
      title released any amount, and a blocked transfer could hand back an approval an earlier action
      had spent. W463: a hold is identified by what filed it; one live record per action under a gate
      lock; an approval releases only the intake it was filed for, is spent once and given back only
      when its action never ran; a review or an explicit decision is refused when the caller sent the
      amount it read (expected_est_distributable_wst) and the hold no longer carries it, or when the
      hold's amount moved during the review; a hold filed after a rejection needs an explicit decision
      (the Sanctum lists it); an
      economy hold cannot be implemented by hand. Guards:
      test_w463_economy_approvals_release_only_what_they_were_filed_for,
      test_w463_hold_lifecycle_reviews_races_and_replays_both_ways; probe scripts/_w463_probe.mjs.
 P1.12 ✅ DONE W460 [1.12 · R4.3] Visual Composer: wire Export/Deploy to /resources/swarm/define + run with the
      returned cascade id, or RETIRE the tab and link the /native-ai designer. Either way the
      "GaaS COMPLIANT" badge goes. ACCEPT: no unevaluated compliance badge in src/.
      DELIVERED W460: RETIRED (the plan allowed it; the designer already defines, saves, edits and runs).
      The ACCEPT clause is a guard: a marker scan over 123 source files with a string-aware comment
      stripper tested both ways, colour fixes pinned, and the Governance Hub's flag computed from what each
      event is (classify_event, with a drift check over every adverse event type any producer writes).
      Refuted twice (16 then 12 confirmed, all fixed); broken nineteen ways, each blind failing alone.
      NOT DONE, and why — each is a row in the follow-up register (docs/FOLLOWUPS.json, W462): the org
      cascade's gate screens a constant attestation (the chip now says 'intent only'; gating the delivery
      is P2.6); one violation trips the shared breaker and its reset has no user dependency (P2.6);
      /api/v1/swarm has no auth dependency (P2.6); the swarm store's writers are unlocked, the contract
      drops a stage's model, runs carry no run id, and the page cannot delete a cascade (P2.8); the
      mandates docs claim ENFORCED on the deleted gaas.ts (FU-004) and Command Center keeps hard-coded
      status literals (FU-011) (both ride P1.16 since W469; they were NEXT).
      SPLIT OUT OF THIS AUDIT AND DONE: W461 — transformation stage verification honest (register
      FU-001; guard test_w461_transformation_validation_is_honest; probe scripts/_w461_probe.mjs).
 P1.13 ✅ DONE W470 [1.13 · R5.6 R5.8] Catalogue honesty. Marketplace counts only routed entries as live; the six Domain
      Signature literals badged legacy or retired; the "QEP Flagship" tab removed from the five
      non-Religion hubs; DomainsHub/AIToolsCatalogue counts derived from ONE tool registry the
      hubs mount from. GUARD: a test that counts mounted DomainTool forms against the registry.
      DELIVERED W470 (Claude Fable 5.1's first round, from the W469 handover): ONE registry
      (src/lib/toolRegistry.ts — 26 entries: 23 forms, Law's analyser and the Employment studio as
      surfaces, and the QEP flagship in Religion only) that every hub mounts its titles from and both
      front doors count, list, link and describe from; the guard parses the registry and every hub and
      fails on a typed title, a typed number, a tab no hub has, or the flagship anywhere but Religion.
      The 'QEP Flagship' tab is gone from the five non-Religion hubs with its two components (engines
      'not wired to a backend yet', tools 'planned' — dead by design). The catalogue API says what each
      products/ directory is — live (a route serves it: 5), source (a pointer, nothing served: 9),
      legacy (the six signature-product archives, category 'Legacy archive', never routed: 6) — and the
      marketplace counts live only, badges the rest and offers Open only for a served surface.
      Refuted once (four confirmed: every other consumer of the catalogue — marketplace seeding,
      Build-to-Order, the resource fabric, the orchestrator — still treated a legacy archive as a product;
      fixed as one class: served_products() is the only list a consumer may build, seed, rank or deliver
      from); broken 29 ways, each blind failing alone.
      NOT DONE, and why — rows in the register: the nine source-pointer directories are still listed as
      products of a kind (FU-071, P2.4: serve them or retire them); the six legacy directories still sit
      in products/ with self-declaring manifests (FU-072, P2.4: archive them); and running done
      --hand-to P1.16 lifted P1.16's broad hygiene prefixes to the first route (FU-073, P1.16: the merge
      must carry only the handed matchers forward) — P1.16 was put back last and P1.13's area given to P2.4.
 P1.14 ✅ DONE W471 [1.14 · R3.3 R3.5 R3.6] Board pack + Chief's Opening honesty. Required-section check against the narrative
      only; empty blueprint → "no concept recorded — pack not assembled"; identical DCS hash →
      "unchanged since <date>"; provenance badge on the Genesis card; plan parser keeps the
      floor prefix as provenance; POST /business-plan/set wired to an owner-edit surface; the
      Chief's Opening badged. ACCEPT: three assemblies on an unchanged VSB show one version.
      ALREADY DONE TOWARDS IT: a floor-served pack's gate is 'not assessable' and the Genesis card's
      QMS chip reads 'QMS: —' (W449); a floor-served narrative is 'narrative pending the owned model'
      (W450); the pack refuses a pending working name (W450) and a blocking review gate (W452); the
      Cockpit's Chief's Opening card on a Genesis-seeded plan wears the seeding's provenance badge and
      names the pending fields (W450, W453). CAUTION: the DCS seal covers a content hash (W449), but the
      sealed content is only the name, the 'Sections: …' preamble and the narrative — the layers and
      the economy are outside it, and a floor narrative is one constant string — so an identical hash
      means an identical narrative, not an unchanged pack. What remains: the section check still reads
      that preamble (coverage 1.0 on every pack; it decides a verdict only on a MODEL-served one), the
      empty-blueprint refusal, the 'unchanged since' disclosure (keyed on what the pack carries, not the
      seal alone), the Genesis card's provenance badge, and the Chief's Opening on business_plan.py
      /generate (gateway.query, no provenance, the prefix dropped by the parser) and BusinessPlan.tsx
      (no badge; nothing calls /business-plan/set).
      DELIVERED W471 (Claude Fable 5.1): the board pack measures its required sections against the
      NARRATIVE alone (the 'Sections: …' preamble was inside the measured text — coverage 1.0 on every
      pack; a floor pack now reads 0.0, not assessable); a pack is grounded in the blueprint's concept
      or, failing that, the founder's problem statement — and SAYS which (concept_source, 'no concept
      recorded yet' on the Genesis card); an entity with neither is refused — 'no concept recorded —
      pack not assembled' (409, pointing at the new POST /{id}/concept, the founder's way out; a concept
      pending the owned model still assembles, as the rest of the body ships since W450); a ship with
      nothing to ground a pack on defers the pack, names why, and is not a coherent whole (the birth
      answer lists only what shipped); every pack carries a content hash over what it holds (name · layers ·
      economy · narrative), a version that moves only when that changes, and 'unchanged since', decided
      by the hash never the clock — three assemblies of an unchanged VSB show ONE version (the ACCEPT
      clause; the history says versions apart from assemblies, and two assemblies in one second no longer
      overwrite each other); the Genesis card badges the narrative's provenance through the shared helper,
      shows the version, and shows the server's refusal. The Chief's Opening: /generate uses query_meta,
      writes NOTHING from the native floor (the fields stay pending; the answer says so), keeps the draft's
      preamble as provenance, fills only UNSET fields (empty, or W450's pending marker) from a model and
      never an owner's words, and MERGES its provenance (Genesis' name_source and pending list stay; the
      badge moves only when something was written); /set is the owner-edit surface (clear works; only a
      CHANGED value is stamped owner-edited; the floor's marker is refused as an edit), wired from
      BusinessPlan.tsx with the provenance badge, the pending fields and a note when a generation wrote
      nothing. Refuted once (seven confirmed, all fixed and guarded); broken 34 ways, each blind failing alone.
      NOT DONE, and why: the Cockpit's plan tab shows the opening's provenance but has no owner-edit
      surface (FU-074, P2.9); the pack's 'strategic' and 'action_plan' layers are still labels over the
      CEO specification and the board roster with no cadence — that is P3.3's item, not a register row.
 P1.15 ✅ DONE W472 [register · the store class, W442→W468] Stores that refuse, never replace — the class-kill. Every
      store a writer reads is read strictly or not at all: a file that exists and cannot be read whole is
      refused (the writer saves nothing and the caller says so), never answered as empty, as a valid prefix
      or as defaults. Five rounds applied this one store at a time (pending transfers and contracts W465,
      owner payments W465, revenue events W467, the VSB ledger W468). What remains: the UEG chain and the
      interceptor's own UEG writes, the compliance history (an unreadable one lifts every FAIL hold), the
      living roster, the waterfall overrides, the venture portfolio, the stores FU-053 names, store_lock's
      stale-lockfile timeout, a repair path for a refused ledger, and non-finite amounts at the revenue
      store. ACCEPT: one shared strict-read helper for writers; a guard table of malformed shapes (BOM,
      truncation, trailing garbage, wrong type, non-finite) per store where every writer refuses and the
      bytes are unchanged; the refusal said on the surface that reads it. The register's rows ride here.
      DELIVERED W472 (Claude Fable 5.1): ONE strict read for writers — config.read_json_strict
      (a byte-order mark, bytes that are not UTF-8, text that is not JSON, a non-finite number, a nesting
      too deep to parse, a wrong type, a sharing violation that lasts: StoreUnavailable, and the bytes stand)
      — applied to every store the register named: the living roster and the compliance history (an
      unreadable history now HOLDS the entity — standing unknown, not clean; the roster page says both),
      the Owner's waterfall overrides (locked, atomic; a cycle says overrides_unavailable), the venture
      portfolio (the reader says unavailable, never zero holdings), the UEG chain (refused, never restarted;
      UEGUnavailable), the interceptor's own UEG writes (the decision stands, ueg_logged says whether it
      reached the ledger, the action's own error is re-raised), the chain's default path through
      config.data_path (a legacy working-directory chain carried over once), the federation twins, the
      proposed catalogue, an agent's registration, the composition runs (run_record says whether the run
      was filed), the tier stores, and mutate_json; store_lock's stale branch honours its timeout; a
      non-finite revenue amount is refused at the door; and a refused ledger has a repair path (POST
      /economy/ledger/{id}/repair: quarantined first, recovered without inventing a figure — a BOM
      stripped, the valid prefix kept, non-finite postings dropped and counted — refused when a balance
      no float holds). ACCEPT: the guard table breaks seven stores in six shapes each and the chain in
      six; every writer refuses, the bytes stand, the surface says it. Refuted once (twenty-three real verdicts across three lenses (duplicates included), two refuted; all fixed as rules and guarded); broken
      40 ways, each blind failing alone.
      NOT DONE, and why: the read-only readers that still use load_json_tolerant (summaries, listings)
      are honest as readers and untouched; FU-075 (P1.16) lists them so the tolerant loader can be
      retired once every writer is strict.
 P1.16 ✅ DONE W473 [register · hygiene before M1] Canon and suite hygiene before the milestone. The compliance mandates
      docs certify a deleted validator and a genome that does not exist (FU-004, FU-027); two tests pass
      only in suite order (FU-003, FU-025) and one leaves a half-written ledger behind (FU-066);
      config/paths.py resolves the data directory above the repository (FU-026 — relocate the live AI
      memory store by copy, verify, switch, never silently); Command Center's hard-coded status text
      (FU-011); the genome validator's CWD-relative read (FU-028). ACCEPT: each test passes alone and in
      suite order; the M1 fidelity re-run finds no DOC_OVERCLAIM from these docs.
      DELIVERED W473 (Claude Fable 5.1): the two mandate pages rewritten as honest inventories (every
      VERIFIED / PRESENT row names paths that exist, the false rows say NOT PRESENT, the retired
      cross-domain claim says RETIRED; the 'PQC' signer named as a SHA3 digest with a fixed key, the
      ontology engine as a reader over an empty directory, the LSTM as unwired); config/paths.py roots
      the data store in the repository (BASE_DIR = the repo; a legacy store above it is named by what it
      HOLDS, never switched away from silently; scripts/relocate_data_store.py copies, verifies, merges
      disjoint maps, never deletes, and calls two non-empty lists a CONFLICT — the Owner's memory.json
      1,977,250 B and interactions.db 19,036 rows were copied and verified; chroma_db is his to move,
      FU-079); the genome validator resolves its constitution under the repository and the self-healing
      cycle refuses to ratify its fixed template (Change Control); the Command Center prints nothing it
      does not measure; importing config.paths makes only the data root, and no reader creates the
      directory it reads (genome/, models/ ignored); the ten live data files that were tracked in git are
      untracked; and the register's tooling: close / drop / reslot refuse a closed row, --gate refuses
      --slot, a marker in any form after the id is reported and prose 'done' is prose, an open item's text
      may not list a row that rides another item, a hand-off keeps EVERY handed route in its own place
      with its origin (chained hand-offs keep the first owner), handed_from is validated, `route` acts on
      the item's own route (a handed route stays unless --handed) and refuses to hand an open item's area
      away. ACCEPT: each test passes alone and in suite order (the three order-dependent legs fixed);
      the mandate guard fails on a cited path that does not exist. Refuted twice (18 real verdicts in pass one, 10 real in pass two on the fixes; all fixed and guarded);
      broken 32 ways, each blind failing alone. Phase P1 complete → MILESTONE M1 next.
      NOT DONE, and why: chroma_db stays where the Owner's copy is (FU-079, OWNER); the simulated PQC
      signer (FU-076), the unwired Law ontology and the ontology engine over nothing (FU-077) and the
      unwired geospheric 'LSTM' (FU-078) are named, registered and ride P2.4; the read-only tolerant
      readers (FU-075) ride P2.4 too.
 P1.17 ✅ DONE W475 [ledger v4 · Tier-1 ×14 · R1.0 R1.1 R1.2 R2.0 R2.1 R3.0 R3.1 R3.4 R4.0 R4.1 R4.2 R5.0 R6.0 R6.1] The second truth pass.
      MILESTONE M1 (W474) re-measured the whole product against HEAD cdd7619f and found FOURTEEN truth
      defects standing on reached surfaces — none of them a P1.1–P1.16 regression, each a surface the
      first pass never walked: the halal screen fails a subject that AVOIDS a haram term and seals the
      FAIL into exports (R1.0); the floor-served tafsir body repeats the sourced Arabic cut mid-word under
      'THE AUTHENTIC ARABIC TEXT' (R1.1); the QMS generator mixes another organisation's recalled text
      into the document with no provenance (R1.2); establishment says the organism is tending the
      enterprise while the economy lever is off (R2.0); the shipped repository's gate cannot fail on the
      non-floor path (R2.1); the CEO chat's meeting path minutes floor echoes as officers' stances (R3.0);
      the floor's 'Acting as' line names the previous call's persona (R3.1); the Board presents a digital
      twin that has no model (R3.4); three Command Center channels still invent readings (R4.0); the
      native tree decides 'proceed' and the fabric says 'commit-ready' on gates that could not assess
      (R4.1, R4.2); the marketplace counts a product live over a route that does not exist (R5.0); the
      Transformation page reports realisation 1.0 from checks that cannot fail (R6.0); a cycle's costs
      are posted to reserves (R6.1). Every entry is a register row (FU-080…FU-093) riding here.
      ACCEPT: each of the fourteen re-assessed by execution against its own claim (V5), guarded and broken;
      then MILESTONE M1 re-runs and its Tier-1 count is measured again, not declared.
      DELIVERED W475 (Claude Fable 5.1 → Claude Opus 5): all fourteen, each re-assessed by execution against its own
      ledger claim — the halal screen says REVIEW with the negating phrase quoted and never 'Prohibited
      element' (R1.0); the tafsir's floor subject is the reference, so the notes never repeat or cut the
      sourced Arabic (R1.1); the seven management-systems generators compose without memory recall,
      carry provenance with a floor note and a QMS record, and the page shows what served them (R1.2); establishment and the roster listing say the economy
      lever's truth (R2.0); a scaffold-composed document is 'template' to the gate, so it records 'not
      assessable' instead of passing its own headings (R2.1); an officer's stance is the reply's last
      line from a model — the floor's echo is 'no position' (R3.0); a recalled persona is neutralised
      before the engine reads a role (R3.1); the Chief is titled for what serves it and the Board page
      says no twin model is trained (R3.4); the last three Command Center channels measure nothing and
      say so (R4.0); the tree recommends nothing on a gate that could not assess and the fabric's
      commit_ready is tri-state with the run saying so (R4.1, R4.2); a product is live only over a route
      App.tsx serves (R5.0); the realisation figure is labelled API surface coverage, not delivery,
      and its cannot-fail check is gone (R6.0); a cycle's costs are an expense, never a reserve (R6.1).
      ACCEPT: guard test_w475_* (one leg per entry, each broken); probe 12/12 on a fresh backend;
      refuted twice in isolated worktrees — 25 findings, all verified real, 0 refuted; all fixed as rules; broken 42 ways. MILESTONE M1 re-runs next (W476).
      NOT DONE, and why: the M1 re-run itself (a fresh six-region audit) is the next round, not this one;
      the Tier-2/Tier-3 entries of ledger v4 stay P2/P3's queue.
 P1.18 [ledger v5 · Tier-1 ×27] The third truth pass. The M1 re-run (W476, HEAD 929508f0) found TWENTY-SEVEN truth
      defects standing on reached surfaces the two earlier audits did not sample (each audit is capped at ten findings
      per region, so it samples; the assessors were barred from ledgers v3 and v4). The largest class is the
      compliance screen certifying what it cannot know: the ethical keyword engine FAILS a suicide-prevention helpline
      and a pest-control service on one word and seals it as a safety judgement (R1.0), while §10's 'compliant' and
      'safe' are recorded MEASURED from keyword screens that say they certify nothing, and pass on the subject's own use
      of 'halal' (R1.1, R3.3, R3.4, R2.1, R2.3); then faith content — the sourced text prepends the Basmala to ayah 1
      of 112 surahs and 1:1 carries a byte-order mark, labelled exact (R1.2, R5.2); a Genesis candidate the screen
      vetoed is still selected (R1.3); organism and economy readings that cannot fail or are simulated (R4.1, R6.0,
      R6.1, R6.3, R6.4, R4.2); surfaces W475 touched but did not finish (R4.5 Command Center, R5.1 marketplace, R3.6
      the Chief); and the rest named in the ledger. Every entry is a register row (FU-094…FU-120) riding here.
      THEN THE SWEEP (W477, the Owner's ruling of 2026-09-19 — "a wider, one-time sweep for this kind of problem to
      get there faster"): every reached frontend surface (83 of 114 files — every page — and the 273 /api paths they
      call) checked against the ten defect classes with no cap, every finding reproduced by a skeptic:
      docs/TRUTH_SWEEP_W477.md — 190 reproduced, 106 Tier-1 and 84 Tier-2. The Tier-1 findings that ledger v5 had not
      named ride here as one row per emitting file (FU-121… — the high ones; 36 rows); the Tier-2 rows ride the P2
      items that own their areas. P1.18 now carries the whole reached-surface class, not a sample.
      ACCEPT: as P1.17 — each entry re-assessed by execution against its own ledger claim, every writer and reached
      page named, guarded and broken; then MILESTONE M1 re-runs and its Tier-1 count is measured again.
      IN PROGRESS, round by round (each row closed by execution, guarded, broken and refuted):
        W479 — FU-121 and FU-153 (sweep S4.4, S4.5, S5.4, S5.5, S5.6, S6.2, S6.3, S7.6, S7.7): the four
          intelligence pipelines, the Synthesis Nexus, /solve and /mjm stamp every stage with what served it
          (model · structured floor · failed), a failed call is never output and never feeds another prompt,
          the Nexus says when nothing chose its engine, and the pages count only stages that ran. Genesis, the
          resource fabric and the shared provenance badge were corrected with them (four refutation passes).
 MILESTONE M1: fidelity workflow re-run → Tier-1 count 0; ledger v4. — RAN W474 against HEAD cdd7619f
      (:8083, native floor): ledger v4 issued (60 findings, 53 survived, 7 overturned; STUB 8 · DOC_OVERCLAIM 4
      · PARTIAL 38 · DELIVERED 10). Standing Tier-1 count = 14 — NOT MET. P1.17 carries the fourteen; M1
      re-runs after it. Tier-2 19, Tier-3 17 (P2/P3's queue, cited by the ledger).
      RE-RAN W476 against HEAD 929508f0 (:8086), after P1.17: ledger v5 issued (60 findings, 53 survived, 7
      overturned; STUB 12 · MISSING 1 · DOC_OVERCLAIM 2 · API_ONLY 2 · PARTIAL 36 · DELIVERED 7). Standing Tier-1
      count = 27 — NOT MET. P1.18 carries the twenty-seven; M1 re-runs after it. Tier-2 17, Tier-3 9.
      THEN THE SWEEP (W477, on the Owner's ruling): every reached surface, no cap — 106 Tier-1 reproduced
      (docs/TRUTH_SWEEP_W477.md); P1.18 carries them all. M1 re-runs after P1.18 as the check that the sweep's
      class is closed, not as the instrument that finds it.

PHASE P2 — REACH AND DISCLOSURE (Tier 2; ~9 rounds + the scatter; P2.9 added W469)
 P2.1 [2.1 · R2.7 R4.1] Cascade grounding. engine.py strips the marker line, "_Acting as:" lines and
      "## <role> output" headers from carried context before _subject/_keywords/_role;
      'Task'/'Objective'/'Challenge' join the subject labels; intelligence.py labels the
      challenge in every stage template; the orchestrator's literal "\n" fixed; floor output is
      never STORED for recall (augment=False stays — this removes, never adds, recall). ACCEPT:
      a 3-stage floor swarm's stage 3 contains the user's subject and not "external dependency";
      BDP 8/8 stages mention the challenge; the journey's cognitive/MJM helpers route through the
      journey's own `_q` seam and engines_used derives from served_by_agent; guard.
 P2.2 [2.2 · R3.3 R4.2 R4.9] Provenance to every surface. The 47 gateway.query() sites → query_meta carrying
      {served_by, is_external} (SSE engines: on every stage + complete event); badges on
      IntelligenceLab, ForgePipeline (payload already there), SynthesisStudio/Nexus, BTOCatalog,
      SovereignEvolution, OrganismDashboard, BusinessPlan, the Genesis board-pack card. GUARD: `gateway.query(`
      count in agentic_core/api == 0.
 P2.3 [2.3 · R5.4 R5.7] Avatar + profile honesty. User message as the floor's subject; language null with a
      preference set → "Answered in English — your language needs the owned model"; /status
      reports the effective serving mode; profile_applied carried into ai_provenance and shown
      as "profile: applied / not usable by the floor"; Settings copy corrected.
 P2.4 [2.8 · no ledger entry — reach audit] The scatter: 67 ops in 38 clusters, 3–4 per round, audit-before-wire, retire freely.
 P2.5 [2.9 · R5.5] Realm drift retired: configs/realms.yaml removed, sovereign_config path fixed, hub
      CTAs pass a canonical realm + domain, DomainTool sends the user's default realm so
      realm_directive reaches Offering-1, projects API validates realm against the taxonomy.
 P2.6 [2.6, 2.5 · R3.2 R6.0 R6.2] The perimeter and the gate. include_router dependencies=[require_admin] for
      heartbeat, genome, organism-status, sovereign-evolution, board, CCA; owner scoping on
      business-plan, swarm, studio; ConstitutionalPolicyGate + UEG checkpoint inside
      gateway.query_meta; guardrails regex → word-boundary/context. ACCEPT: auth-ON suite —
      401 on POST /heartbeat/stop; "exploit the market opportunity" passes; every query_meta
      response carries a gate checkpoint.
      ALREADY DONE TOWARDS IT: the CCA's write routes read an identity (W459, P1.11) and retiring an
      economy record (POST /{id}/implement on an unreleasable economy hold) is admin-only under auth
      (W463); the CCA's READ routes (GET /api/v1/cca, /queue, /approved, /rejected, /implemented, /{id},
      /impact/{id}) carry no auth dependency — with AUTH_ENABLED on, a caller who is not signed in still
      reads every change record and can trigger an impact assessment on any of them — that, and every
      other router named here, is what remains. Register rows FU-005, FU-006, FU-007 ride here.
 P2.7 [2.4 · R4.5 R4.6 R6.1 R6.3 R6.4 R6.5 R6.8] The organism defends for real (the honest half first, then the wiring). layers_note
      truthful (Immune, Nervous bus, Self-healing, Musculoskeletal engaged; Cardiovascular and
      Endocrine not implemented; Respiratory = Agent Hub, records only) and the W434 sentence
      deleted; reflexes REGISTERED from the heartbeat's hand-coded checks so threshold events
      react between beats; heartbeat engages immune_reconfigure at ≥HIGH (CCA-governed,
      reversible); ATP driven by MEASURED load (cpu/memory/queue) with consumption able to exceed
      production, or every ATP figure outside Anatomy labelled "simulated — does not deplete"
      and the survival copy removed until the branch can fire; torch import lazy + a CI boot
      test with sys.modules['torch']=None; living-VSB compliance keys aligned; venture positions
      queue investee intake or are labelled "recorded, unfunded"; ledger postings tagged by
      source and split in the board pack.
 P2.8 [2.7 · R4.4] Bespoke swarms. genesis derives extra stages from the concept (risk, economics,
      implementation) with the same keyword rules _plan_tree uses; "Edit cascade" on the
      Cockpit; planner rendered on the tree view; Forge per-stage config + Rerun; the
      transformation realisation engine measures DELIVERY (ledger verdicts), not route existence.
 P2.9 [register · the economy's flows, W463→W468] The economy's flows told as they happened (virtual WST).
      A marketplace purchase records its sale; a contract is offered only between living entities, can be
      declined or cancelled, and its settlement's approval names the contract; a failed owner accrual is
      re-applied once; a venture-return intake failure is said; a transfer stranded before W466 can be
      found; a cycle whose process stopped gives its approval back; a transfer retry, a cycle whose write
      timed out, and the pages' earlier figures say what really happened; a development spend is its own
      posting and cannot overdraw; the books refuse a close near the float limit; the roster's ledger read
      is cached; a legacy-balances ledger says what it is. ACCEPT: each row's reproduction runs as a leg of
      a guard. The register's rows ride here.
 MILESTONE M2: fidelity workflow re-run → Tier-2 invisible-shortfall count 0; reach scatter
   resolved (wired or recorded-retired); ledger v5.

PHASE P3 — CAPABILITY (Tier 3; ~11 rounds; OWNER RULINGS put with evidence at P3 start)
 P3.0 OWNER RULINGS, put together with the evidence: 3.10 lifecycle (A/B/C) · 3.11 §10's sixteen
      criteria (instruments for the commercial trio, or amend §10) · 3.5 Products axis
      (build the grid picker feeding Genesis, or amend §17.1 to "design intent") · 3.6 KPI gate
      (block deliverable/marketplace release until the owning VSB's objective KPIs are set and
      tracked, or amend §17.5) · 3.4 Mode 2 scope · AND THE FIVE QEP RULINGS (vision A.12 — A.12.3 blocks
      P3.10 and every guidance surface; A.12.1/A.12.2/A.12.5 shape P3.9's later features; A.12.4
      gates the Fitrah feature; P3.9's first two items need no ruling): A.12.1 corpus provenance (recitation audio, translations, Hadith,
      Tafsir — licence + canonical edition + qira'at; Qur'an Arabic is already settled at
      alquran.cloud per §11) · A.12.2 certification authority (who stands behind a QEP
      certificate) · A.12.3 curriculum ownership AND the scholar-review mechanism for
      AI-generated religious content BEFORE a learner sees it — §11 requires the audit and no
      mechanism exists; this one blocks features 5/6/7 and all of A.7 · A.12.4 whether the Fitrah
      Spectrum proceeds at all, and only ever as A.9.5's self-reported reflection aid ·
      A.12.5 Tajwid rule scope and madhhab variation.
 P3.1 [3.1 · R2.3] §4.6 Develop: a distinct journey stage between design and operational intelligence
      producing at least one buildable, checkable artefact (a costed bill of materials, a
      runnable prototype spec, or a parameterised model via factory/forge) with a REAL pass/fail
      recorded in the journey; floor → honest "not buildable on the floor".
 P3.2 [3.7 · R1.5 R2.4 R6.7] Autonomy that starts. /establish switches auto_economy + auto_compliance on for the
      new entity with a visible "tending on" state; the Cockpit shows last_operated, cycles and
      the governing flags; auto_compliance defaults ON (cheap, deterministic) and its beat extends to
      living deliverables, each card showing 'last screened <time>'; the living-plan pillar re-scored
      only when an instance has evolved ≥1 generation.
 P3.3 [3.3 · R3.5] §17.3 cadence: heartbeat-driven Strategic (quarterly + market signal) and Action-
      Plan (weekly + KPI-triggered) refresh generators writing to the plan with provenance and
      history; board-pack layers assembled from THEM; values from the VSB's own constitution.
 P3.4 [3.4 · R3.4 R3.8] Mode 2 (per ruling): the Chief as a genuine modelled twin — a per-founder model
      built from the explicit profile + instructions + decisions, invoked unprompted
      (heartbeat auto_align → board_directive with execute) and rendered with its basis;
      per-VSB Chiefs titled for their owner, never "of default".
 P3.5 [3.2 · R2.8] Image intake from Describe: an owned vision resource reads an attached image into
      text, or refuses with an accurate reason; the accept list says what is supported.
 P3.6 [3.8 · R5.7] §9 depth: useT across hubs/DomainTool/Settings/avatar; AI-output language honoured by
      the owned model and labelled when not; 12-language list trimmed to what has a dictionary.
 P3.7 [3.9 · R2.6] §13 repo: file/zip endpoint, clickable tree, preview links from the Cockpit; the
      entity's products listed on the marketplace with §12 pricing.
 P3.8 [3.5, 3.6, 3.10, 3.11 · R1.4 R2.3 R2.5 R5.5 R6.6] The rulings, implemented as ruled — each a Tier-1-shaped fix once ruled
      (a lifecycle field that only ever holds its final value is the §4.5 shape).
 P3.9 [vision A.6, A.1] QEP composed, not rebuilt. The Religion domain's remaining features are
      built by COMPOSING §6/§7 resources — never a private QEP stack, which is what killed all
      three prior attempts (A.13.1), and never the excluded 2025 stack (A.10). First the two that
      need no ruling: memorisation UI (the
      flashcard/review/heatmap surface over the REAL SM-2 that already runs) and competitions +
      leaderboards over the persisted XP. ACCEPT: a learner schedules 3 ayaat, reviews at q=4,
      and sees the interval, the e-factor and the 'a review count, not a hifz certification'
      basis on screen; a leaderboard ranks two seeded learners by recorded XP with its formula
      shown. GUARD: no route added under /qep may return a figure without a basis string.
 P3.10 [A.6 f5/f6, gated on A.12.3] Learning modules + the educator toolkit. Curriculum content
      and classes ship ONLY behind the ruled scholar-review mechanism; until it is ruled, the
      LearnTeach surface keeps saying NOT ESTABLISHED, which is correct and must not be dressed.
 P3.11 [A.8] The QEP VSB. §12's waterfall configured as the Waqf/Trust instance A.8 describes —
      free at point of use for individuals, institutions at cost+5%, surplus cap <=5%, a
      Zakat-eligible charity channel, Sponsor-a-Student — so one entity has an economic model
      that is ITS OWN rather than the generic template. The eight-attribute executive board
      (A.8) as the Religion-domain board composition.
 P3.12 [cognitive fabric · docs/COGNITIVE_ENGINE_ARCHITECTURE.md] The engine contract, then the six
      foundational engines. The repository already holds the cognitive layer an outside proposal offered to write:
      six engines in agentic_core/cognitive/, a registry that declares nine, a consultation contract, a Mushāwara
      bridge, a five-gate clearance chain and a six-stage recirculation loop under agentic_core/avatars/. None of it
      runs: nothing ever calls CognitiveEngineRegistry.register, so registry.get raises on first use; the registry
      calls engine.process(input, context, enforcement) while the engines expose unveil_patterns/comprehend/reason/
      detect_anomalies/reflect/validate_values; and every one returns a constant for any input. The consultation
      contract names only seven engines and REQUIRES a numeric confidence, which is why the engines return 0.96.
      This item fixes the contract and the six: an explicit not-assessable state and a provenance block on the
      response, the nine names the registry already declares, one populated binding with one call signature the
      engines implement, a base class carrying the feature flag (read at call time), measured latency and the
      result type — then the six engines implemented against their real inputs in the empty
      agentic_core/cognitive/foundational/ package. Also removes the unused cascade/MJM singletons W479 left in
      agentic_core/api/intelligence.py, and makes /api/v1/cognitive/* (ledger v4 R4.3: a constant payload,
      engines_run 9, status complete) report what ran.
      NOT BEFORE P1.18 has closed the VSB spawn surface that shows these constants as 'Cascade Complete': new
      engines behind an old untruth would put two generations of it on the same screen.
      ACCEPT: an engine's output changes with its input, or it says assessable:false with the reason; every result
      carries what served it; no page shows a number an engine did not compute; guard + blinds + a fresh-backend probe.
 P3.13 [cognitive fabric] The three meta-regulative engines — Tawazun, Niyyah, Tafakkur — refusal by default.
      Tawazun a real Pareto frontier over named objectives; Niyyah an intent ratification whose quorum is counted
      from real signatures; Tafakkur a drift check against a recorded baseline. Each returns 'not assessable' and
      blocks when its inputs are missing, never a default approval. Niyyah may read an entitlement supplied by the
      virtual economy; it calls no payment provider (P4.6 is the Owner's).
      ACCEPT: each engine refuses on absent input, and every verdict names its basis; guard + blinds.
 P3.14 [cognitive fabric] The clearance chain that can refuse. agentic_core/avatars/core/clearance_chain.py runs
      Mushāwara → Niyyah → Tawazun → Tafakkur → Tahqeeq, and every gate currently defaults to pass
      (tawazun_res.get('balanced', True), tahqeeq_res.get('verified', True), a missing risk_score reading as 0), so
      an engine returning {} clears all five. Flip every default to block, record each gate's verdict with its
      basis, and surface the chain's result wherever an emission it cleared is shown.
      ACCEPT: a gate with no input blocks; a broken engine cannot clear the chain; guard + blinds.
 P3.15 [cognitive fabric] Attestations that are attestations. The chain writes literal strings ('SIG_MUSHAWARA_v1')
      into the UEG as signatures, and Dilithium/Kyber are named in five modules without any post-quantum operation
      taking place. Sign a canonical payload with a named algorithm and a stated key source, append it to the UEG's
      hash chain, and expose a route that re-computes and verifies it. The word post-quantum is used only when the
      signature is post-quantum.
      ACCEPT: a tampered payload fails verification; no placeholder signature is written; guard + blinds.
 P3.16 [cognitive fabric] The auxiliary engines and the recirculation loop. Tahqeeq (output verification),
      Mushāwara (deliberation) and Mudrik (the bridge to the transformation surface), then the six-stage loop
      (Sense · Intend · Analyse · Act · Learn · Reflect) driven by the heartbeat, with its stage latencies MEASURED
      and recorded rather than asserted — agentic_core/avatars/core/recirculation_orchestrator.py states targets
      (<100ms sense, <500ms sense-to-act) it never measures, and the avatar API deliberately bypasses it today.
      ACCEPT: the loop runs from the heartbeat with recorded per-stage latencies, its breaches are facts in the
      record, and the avatar path is wired to it only once P3.12–P3.15 hold; guard + blinds + probe.
 MILESTONE M3: fidelity workflow re-run → zero STUB/MISSING/DOC_OVERCLAIM; every PARTIAL
   disclosed; ledger v6 = the ratified boundaries only.

PHASE P4 — THE OWNER'S HAND (Tier 4; pre-flights built by us, switches flipped by the Owner;
 no ledger entries — these rest on §14's recorded switch list and the Owner's decisions)
 P4.1 AUTH_ENABLED on, with the auth-ON suite green and the perimeter (P2.6) closed.
 P4.2 SELF_SERVE_SIGNUP per the Owner; the 162 test-owned entities pruned only on instruction.
 P4.3 AI_ALLOW_EXTERNAL + a key, as accelerants only — the in-house-first order proven by test.
 P4.4 Managed Postgres — migration dry-run script and rollback proven on a copy first.
 P4.5 Production deploy — the Docker image that boots (W354) behind the Owner's account.
 P4.6 The Stripe key rolled at Stripe; REAL_MONEY_ENABLED only after compliance/KYC review.
 COMPLETE when M3 holds AND every P4 switch is either flipped or recorded as a §18 boundary.

EFFORT, HONESTLY: ~33 rounds at the current cadence before P4 — P1 alone is the campaign's
largest single phase and it is the one that matters most, because it is the one users meet.
Measured so far: P1.1–P1.12 took twelve rounds (W449–W460), P1.13 one (W470), P1.14 one (W471), P1.15 one (W472) and P1.16 one (W473), plus four rounds between items — W461
and W463 each worked a task an earlier round found and deferred, W462 built the register after the
Owner asked (2026-09-13) that suggested tasks be scheduled into the plan, and W464 delivered the Owner's
rulings on the register's four OWNER rows, and W465 worked three of its NEXT rows (FU-015, FU-016, FU-024) and
registered thirteen more it found (closing two of them, FU-038 and FU-046, itself), and W466 worked FU-023 and
registered one more, and W467 worked FU-022, FU-043 and FU-044 and registered one more, and W468 worked FU-041 and
registered eighteen more — and at W468 the register held forty-two open NEXT rows (and eight riding with P2.6 and
P2.8) before P1.13. That is why P1.13 did not come: NEXT meant "before the next plan item", and rounds registered
more than they closed. W469 (the Owner's instruction) retired NEXT: the forty-two rows now ride the items that own
their areas, and all fifty open rows stand at eleven on P1.15, eight on P1.16, eighteen on P2.9, nine on P2.6,
three on P2.8 and one on P2.7 — so the
plan's order is the order of the work, and PLAN NOW says what is next. Three items were added (P1.15, P1.16, P2.9):
budget ~3 rounds for them on top of the ~33, and more if the rows riding them take more than one round each.
Do not shorten it by declaring; shorten it by measuring.
</delivery_plan>

<method>
Learned by being wrong, repeatedly, in ways a green suite hid. Rules 1–5, 19 and 25–28 are
load-bearing.

1. VERIFY THE INSTRUMENT BEFORE THE CODE. When a result contradicts a working system, suspect your
   tool first. Confidently wrong instruments here: a checker that flagged a module which boots; a
   sweep that reported "864 controls, 0 failing" while clicking the same 10 buttons everywhere; a
   reachability matcher that invented 21 phantom gaps; a probe that captured page text one frame
   before the outcome painted; a grep over source when the built bundle was the true instrument;
   a realisation engine that scores a pillar "strong" because its route exists.

2. ASK WHAT YOUR SCORE WOULD RANK FIRST, THEN BUILD THAT INPUT. Measuring the wrong thing is
   subtler than fabricating and passes review because it is technically honest. If the maximising
   input is absurd — 700 repetitions of one word scoring 1.000, a percent passed as a fraction, a
   200-character floor scaffold scoring "cov 100%" — the metric is not a metric.

3. A GREEN SUITE IS NOT EVIDENCE OF ABSENCE, AND A TEST CAN ASSERT THE DEFECT. Tests here encoded
   the same wrong assumptions as the code and CONFIRMED bugs. WHEN A FIX MAKES AN EXISTING TEST
   FAIL, READ THE TEST'S INTENT BEFORE ASSUMING THE FIX IS WRONG — but know the other direction
   too: the W316 test that failed on W440's honest new basis string was asserting the OLD
   overclaim; the honest behaviour won and the assertion moved.

4. PROVE EVERY GUARD FAILS BEFORE TRUSTING IT — and prove the BREAK actually broke something.
   Break the code, watch the guard fail WITH THE ORIGINAL SYMPTOM, restore, watch it pass. A
   restore script can itself miss (a blank line) and leave the tree broken — verify the restore.

5. FABRICATIONS CLUSTER AROUND TRUTH. Invented figures graft onto genuine output; four real
   criteria lend a green badge to twelve unassessed ones; a real DCS hash seals a contentless
   narrative. Look hardest where the data is mostly real.

6.  Where a real source exists, WIRE IT rather than nulling.
7.  Absence beats invention: null / [] / "not_checked" WITH A REASON. A bare null invites a guess.
8.  Provenance beats heuristics: owner_id separated the Owner's real entity from pytest's.
9.  Self-reference is not a reference: an entity's board pack, repo and ledger are its FOOTPRINT.
10. NEVER PUT AN ESCAPE SEQUENCE THROUGH A HEREDOC. Write edit scripts to FILES and run them;
    assert every str.replace found its target exactly once; build tricky strings with chr().
11. Fixing one honesty defect can expose another it was hiding.
12. AN HONEST INSTRUMENT CAN BE DEFEATED AT ITS INPUT — audit the WRITE CHANNELS, not just the
    mechanism. A record is exactly as trustworthy as its least-verified input. NaN passed every
    comparison guard on the transfer path (nan <= 0 is False) and would have poisoned the books
    forever; bound at the MODEL (allow_inf_nan=False) and at the engine (math.isfinite), both.
13. THE §4.5 CLASS IS A CLASS — grep for it before trusting any ranked output. THE SHAPE: a value
    selected or reported as a result when nothing discriminated. WHERE TO LOOK: max( over a
    mapping · a sort then [0] · any loop returning the first item clearing a threshold · any
    field whose NAME asserts more than its computation earns. THE FIX: detect that nothing
    discriminated, return None rather than a name, say WHY in a basis field — then PROVE IT BOTH
    WAYS (it must still resolve when there IS signal).
14. A FIX THAT LIVES AT ONE CALL SITE IS A LOCAL REPAIR, NOT A FIX. After writing a scrubber, a
    disclosure or an honesty field, ask which OTHER paths emit the same thing. Genesis fixed
    "cannot fail on the floor" for its own stages in W436; the SHARED gate every other surface
    uses never got it, and six months of records were sealed "verified".
15. REACHABILITY BEFORE SEVERITY. A defect in unreached code is a LEDGER ENTRY, not an incident.
    Beware: a name in a registry or config STRING is not a call — check for real dispatch.
16. AN AGENT'S FINDING IS A LEAD, NOT EVIDENCE. Reproduce before you act, and never assert more
    than you personally verified. (The refuters earn trust by REPRODUCING their catches with their
    OWN inputs — a second journey, a second VSB, a second transfer. Verify anyway.)
17. A NAMESPACE IS NOT DEAD BECAUSE ITS ROUTES ARE UNREACHED. Four "dead" namespaces had live
    frontend callers; deleting them would have broken the product. The reach audit now classifies
    legacy separately — keep it that way.
18. TRUST-HOLE DEFECTS PROPAGATE UPWARD AND GET SEALED. Before fixing a measurement defect, follow
    its OUTPUT: if a downstream record attests to it, the attestation is part of the defect.
19. REFUTE YOUR OWN FIXES BEFORE SHIPPING — adversarial agents on the round's own diff, told to
    default to "it breaks". Ten consecutive rounds of real catches. What they find, every time:
    consumers of every field you renamed or deleted (grep repo-wide, including TESTS and .mjs
    scripts); the defect class re-committed INSIDE the fix; disclosures that overclaim; and the
    breaks your fix causes one layer up or one consumer over.
20. A LOCK HELD BY ONE WRITER OF SEVERAL EXCLUDES NOTHING. Before claiming a store is serialised,
    ENUMERATE ITS WRITERS — the fund had two (one locked), the venture portfolio had three (two
    locked), and in both cases the unlocked writer erased the locked one's work. Read-modify-write
    means the READ is inside the lock too, never a pre-lock snapshot.
21. A GUARD THAT CANNOT FAIL IS NOT A GUARD — AND THE GUARD OBJECT ITSELF CAN LIE. Duplicate keys
    in a JS object literal silently discarded four new smoke needles (last-key-wins); one needle
    asserted text on a tab the smoke never clicks; another anchored on text that a passing probe
    had just mutated away. Verify needles by EVALUATING the object and by checking the text
    renders in every state the checker can encounter.
22. WAIT FOR THE SPECIFIC OUTCOME ELEMENT, never for text already on screen. Async panels paint
    after headers; result cards paint across frames. Three probe races in one campaign, one
    lesson — anchor the wait on the exact honesty line you are about to assert.
23. UNREACHED IS A QUEUE OF DECISIONS, NOT A QUEUE OF WORK. Retirement is a first-class
    resolution: the frontier router and the parallel marketplace were RETIRED — each was
    narrating capability (active listings, an execution pipeline) that nothing could ever serve.
    Fixing code that should not exist is effort spent making fabrications more polite.
24. EVERY VALUE THAT BECOMES A FILENAME IS AN IDENTITY SURFACE. Validate with one strict rule
    (no separator of EITHER kind, no leading dot) and stamp the acting principal server-side —
    a caller-supplied name is a label, never an identity.
25. THE DEFAULT TAB IS THE PRODUCT. Audit what a user lands on FIRST before auditing the edges:
    the Living Organisation hub's default tab was a detached roleplay, the Employment hub's a
    fabricated "live job board", the Law hub's a green-badged floor — while eight reach campaigns
    wired the periphery around them. Every hub, every default tab, every first click, every
    round.
26. A CLASS-KILL IS ONLY A KILL WHERE EVERY SITE USES THE HELPER. "Every badge routes through
    provenanceBadge" was true of the helper and false of ten call sites that took its label and
    chose their own colour. Guard the helper's USE (grep for the partial use), not its existence
    — and count the sites again after the guard lands.
27. A FIDELITY VERDICT IS DATED THE DAY IT RAN. v2 was ten workstreams old when v11 rev 1 said
    "weigh it accordingly"; re-measured, its 74 findings had become 60 different ones, with new
    Tier-1 defects on surfaces the campaign had walked past. Never carry a verdict forward by
    reading; re-run the six-region assessment at every milestone, and treat "no known Tier-1
    entry" as a statement about your knowledge, not the product.
28. ON THE SHIPPED DEFAULT CONFIGURATION, WHAT INPUT MAKES THIS GATE SAY NO? Product gates, not
    just test guards: a QMS gate whose coverage cannot fall below 1.0 on the floor, a review gate
    no lifecycle mover reads, a constitutional row that never reads the subject, a chip green by
    construction. If nothing can make it say no, it is a certificate printer, and every record it
    sealed is part of the defect (rule 18).
</method>

<guards>
These exist. USE them; do not rebuild them, do not let them rot.
- integration_tests/test_mvp_spine.py — 403 tests; 77 session guards W419–W479, each broken and
  watched fail with its ORIGINAL symptom before being trusted; plus the W435 lockstep guard that
  fails when GET /api/v1/plan drifts from the living plan's §7 glyphs (re-scored W446 — both
  moved together, and the suite proved it).
- scripts/check_import_integrity.py — CI job; fails when a live module imports a first-party module
  with no file behind it. Baseline scripts/import_integrity_baseline.txt (13 pre-existing, kept by
  a negation at .gitignore:21 because :17 is a blanket *.txt). Run before AND after any file move.
- scripts/browser_smoke.mjs — 17 deep routes + every other route swept, list PARSED from App.tsx.
  REQUIRED_SECTIONS demands named sections ALL render — nine routes: /ceo?tab=board (the
  arms-length invariant), W437 /native-ai, W438+W444 /organism?tab=anatomy, W439+W444
  /religion?tab=qep + /qep, W440 /vsb-cockpit?tab=systems, W442+W444 /economy + /marketplace,
  W443 /ceo?tab=hub. Needles are compared LOWERCASED (CSS text-transform reaches innerText); they
  must anchor on state-independent text; and the OBJECT must be verified for duplicate keys
  (rule 21). Also carries the W429 PDF guard: inline fixture, honest image-only refusal, ZERO
  external requests.
- scripts/reach_audit.py — THE reach measure: imports the app at HEAD, matches template holes by
  segment, reports exact vs template-prefix separately, clusters the genuine-unreached. Run it
  fresh; never trust a written-down reach figure.
- scripts/workflows/fidelity_audit_v3.js — THE fidelity measure: the six-region assess→refute
  workflow that produced ledger v3 (Claude Code Workflow tool; boot a fresh HEAD backend, set BASE,
  run; render with scripts/render_fidelity_ledger.py). Re-run at every milestone (rule 27).
- scripts/_w436…_w463_probe.mjs (twenty-three — W441, the retirement round, needed none; W445–W448 added none) — committed
  per-round browser probes; each drives the round's surface end-to-end against a FRESH backend
  serving the final build. Reuse their patterns (dismissTour, lowercased body, specific-outcome
  waits, computed PASS/FAIL exit codes).
- integration_tests/conftest.py — isolates DATA_DIR AND corrects an already-imported config via
  object.__setattr__; a session fixture FAILS the run if the store is not isolated. Tests must
  resolve paths via config, never os.environ; use unique per-run uids (conftest overrides yours).
- scripts/_button_sweep.mjs + scripts/_noop_retest.mjs — interactive sweep (figures dated
  2026-09-01; blind spots documented in the W429 entry — read them before trusting a clean run).
- scripts/prune_test_entities.py — dry-run reporter/pruner. Never --apply unasked.
</guards>

<constraints>
- Money is VIRTUAL WST. Never present a virtual figure as real; never attribute a platform-level
  figure to an individual user. Money paths get BOTH model bounds (gt=0, allow_inf_nan=False) and
  engine isfinite checks; every money store mutation runs read-modify-write INSIDE store_lock.
- In-house AI first. Use gateway.query_meta and surface served_by/is_external; floor-served output
  renders the amber provenanceBadge (its .cls, never a local colour), never a green in-house
  badge — and for valuations, translations of sacred text, and anything a template cannot
  honestly be, REFUSE (503) instead. A gate that cannot see the floor must return None with a
  basis, never pass.
- FAITH CONTENT IS CONSTITUTIONAL (vision §11): Quran Arabic is never AI-generated — fetch from
  the authoritative source and inject as given material with a do-not-reproduce instruction;
  recitation is never scored; AI content is labelled and never authoritative; a floor
  "Translation" heading over sacred text is a §11 breach (ledger 1.8).
- NEVER "fix" a missing user context by enabling gateway recall. augment=False is deliberate under
  W332 because RECALL WAS THE LEAK VECTOR. The explicit owner-scoped profile (W428) is the safe
  mechanism; its safety is ONE LINE: profile_owner returns None under auth with no identity, never
  "default". P2.1 REMOVES recall of floor output; it never adds recall.
- Never fabricate: no invented metric, citation, certification, person, review, vote, price,
  provenance, persona, tool, or "live" claim — including in a fallback, default, seed or demo.
- A deliver (org cascade) is ~22 model calls, AT LEAST 15 min on a local model (one measured run:
  {ollama: 7, native: 15} in 1,067s; inherited figure — no completed run timed end-to-end since).
  Say so before the click and show elapsed time.
- Never run two pytest suites concurrently (shared stores corrupt; ~40 false failures once). The
  full suite is ~34 min; run it in the background on an ISOLATED env (DATA_DIR +
  WORKSTATION_DATA_DIR + WORKSTATION_UEG_PATH + PROJECTS_DIR + AI_DISABLE_LOCAL=1).
- This repo mixes CRLF and LF PER FILE (git ls-files --eol, 2026-09-05: 202 CRLF · 4229 LF ·
  5 mixed). Preserve what you found; check `git diff --stat` against the lines you meant to
  change — the W445 regeneration itself flattened a CRLF canon file to LF and had to restore it.
  The vision, the fidelity ledger and the living plan are CRLF; this prompt is LF.
- 162 test-owned entities remain (re-counted 2026-09-04), protected by platform-level FINANCIAL
  records — the Owner's call.
- Confirm before anything destructive or outward-facing. Back up first; dry run first.
- FIGURE PROVENANCE. Measured 2026-09-05 against HEAD 06c51109: the surface block, the reach
  classification, the CRLF mix, the store counts, the fidelity counts. The suite total is W444's
  final run at the same HEAD, re-run in W446 on the final tree (living_plan.py moved). Dated
  2026-09-01: the button-sweep figures. Inherited and undated: the cascade timing. Re-verify
  anything you are about to rely on — and boot a fresh backend first.
</constraints>

<rhythm>
Per increment: audit the item (agents as leads — verify their claims by hand; start from the
DEFAULT TAB, rule 25) → implement → REFUTE YOUR OWN FIXES (adversarial agents on the diff; fix
what survives verification) → verify IN THE REAL SURFACE (a fresh backend on a fresh port, a real
browser, the committed probe pattern) → break-test the new guard both ways → full suite in the
background ON THE FINAL TREE (kill and rerun if the tree changes under it — a test-only assertion
fix after the run needs the affected tests re-run green with their store-sharing neighbours, and
the honest note in the entry) → append to docs/AUTONOMOUS_PROGRESS.md → commit with a message
stating what was WRONG, not just what changed → push → confirm CI → update memory.

Per phase boundary (M1, M2, M3): boot a fresh HEAD backend, re-run scripts/workflows/
fidelity_audit_v3.js, render the ledger, regenerate this prompt's <ledger> from it, and re-score
the living plan's §7 WITH its API mirror. A milestone is a measurement.

Close any entry only by EXECUTING the thing, never by reading the diff. Measure the thing itself.

Write commit messages someone can learn from, and record your own mistakes in them — including
the refuters' catches of your fixes: the twenty-eight lessons above are worth more than the fixes
that produced them. When you are wrong, say so plainly, correct it, and continue without
narrating at length.
</rhythm>
```
