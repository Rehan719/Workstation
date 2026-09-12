<!--
  KNOWLEDGE OPERATING PROCESS — Workstation IDBO
  The designed, living process by which shared understanding is built, maintained, leveraged,
  and kept consistent and accurate — for the Owner working with Claude and other AI agents,
  across immediate / short / long term. This is itself a living artifact.
  Status: FOR OWNER REVIEW · 2026-06-20
-->

# Knowledge Operating Process

> **Purpose.** A permanent, dynamic, adaptive, reliable process so that knowledge, learning, and understanding of Workstation IDBO are **continually built, kept consistent and accurate, and leveraged synergistically** — by the Owner, by me (Claude), and by any other AI agent — to follow your direction faithfully and collaborate effectively now and over the long term.

---

## 1. The Knowledge System (five layers, one truth — the Vision at the apex)

Knowledge lives in five synchronised layers. Each has a clear role; together they are the single source of truth. **Precedence (recorded W446): the Vision prevails; every other layer reconciles TO it.**

| Layer | Artifact | Role | Cadence |
|---|---|---|---|
| **Vision (apex)** | `docs/WORKSTATION_IDBO_WHOLE_VISION.md` | The Owner's canonical fine-resolution vision (§1–§15 are the Owner's words), the structural specifics (§17), the settled rulings (§18), and the dated fidelity pointers (§16) | Only when the Owner refines intent or rules (§18); §16/§17 status notes re-measured at every delivery-plan milestone |
| **Understanding** | `docs/WORKSTATION_IDBO_UNDERSTANDING.md` | The "same page" — who you are, the vision (envisaged + final), my articulated understanding, open questions | When vision/intent is refined; reconciled each major session |
| **Plan** | `docs/WORKSTATION_IDBO_LIVING_PLAN.md` | Vision ↔ grounded current state ↔ action (roadmap, scorecard, collaboration protocol) | Every session that changes the codebase |
| **Memory** | `~/.claude/.../memory/*.md` (+ `MEMORY.md` index) | Durable agent memory: facts, decisions, feedback, references — loaded every session | Whenever a durable fact/decision/correction occurs |
| **Code + Live State** | the repo + `GET /api/v1/plan/state` | The ground truth; auto-introspectable current state | Continuous |

**Rule of coherence:** these five must never contradict each other. The **Vision** is the Owner's intent and prevails; the **Code/Live State** is ground truth about what exists; **Understanding** is the same-page summary of the Vision; **Plan** bridges Vision and state; **Memory** preserves the why. If they diverge, reconcile in the same session — and where the live system differs from the Vision, the difference is the work to do (the delivery plan), never a redefinition of the Vision down to capability.

## 2. The Update Loop (how knowledge stays alive)

```
        ┌─────────────────────────────────────────────────────────────┐
        │  OWNER direction / refinement  ───────────────►  UNDERSTANDING │
        │                                                       │        │
        │  read before work:  UNDERSTANDING §8/§9 + PLAN §3/§7   ▼        │
        │                                              decide & build     │
        │   CODE + LIVE STATE  ◄──────────────────────  (faithful, honest)│
        │        │  introspect (/api/v1/plan/state)              │        │
        │        ▼                                               ▼        │
        │   reconcile  ──►  PLAN §4/§8 (current state + changelog)         │
        │        │                                               │        │
        │        └──────────►  MEMORY (durable facts/decisions)  ◄────────┘
        └─────────────────────────────────────────────────────────────┘
```

**Before starting work** (any agent): read `UNDERSTANDING` §8–§9 and `PLAN` §3 (vision) + §7 (adherence scorecard).
**After completing work:** update `PLAN` §4 (current state) + §8 (changelog); write any durable fact/decision to **Memory**; if intent shifted, update `UNDERSTANDING`.
**Never** mark current state from aspiration — only from verified reality.

## 3. Autonomous reinforcement (the process runs itself)

The process is not purely manual — the organism helps keep it honest:
- **`GET /api/v1/plan/state`** auto-introspects the live system (routes, resources, VSBs, evolution cycles, board) so the current-state layer can never silently rot.
- **Sovereign Evolution Office** (`/api/v1/sovereign-evolution/cycle`) periodically introspects and proposes improvements, curated by the VSB org → Change Control — feeding the Plan's roadmap.
- **gaas.v5 UEG** provides a tamper-evident audit trail of governed actions.
- **Board / Chief** (`/api/v1/board/chief/instruct`) lets you inject direction that cascades into action — and is logged.

## 4. Collaboration Model (working for you, with you, with other agents)

**Three working modes** (from the Cowork canon's Human-AI Integration):
- **For you (autonomous):** you set mission/values/bounds; the organism executes the rest, faithfully, under your Chief/Board.
- **With you (collaborative):** you direct and review; I decide-and-build on clear matters and stop at gates you set.
- **With other AI agents (co/team):** multiple agents share this knowledge system; each reads the five layers before acting and writes back after.

**Multi-agent handshake (lightweight, robust):**
1. **On entry** — read `UNDERSTANDING`, `PLAN §3/§7`, recent `MEMORY`, and the latest changelog entries; if continuing another agent's work, read its last handoff note in the changelog.
2. **During** — keep tasks visible (task list); honour the 10 Architecture Invariants and the working mandate `[[feedback-workstation-working-mandate]]`.
3. **On exit** — append a dated changelog line in `PLAN §8` (what changed, verification result, next priority, blockers); update `MEMORY`; leave the tree clean (revert mid-work failures).

**Roles are explicit, not implied:** the Owner sets direction; the Chief (Owner's digital twin) represents the Owner; the Board owns plan/strategy; AI agents execute under that hierarchy. No agent silently changes vision — only the Owner refines the Vision (`WORKSTATION_IDBO_WHOLE_VISION.md` §1–§15 and its §18 rulings); `UNDERSTANDING` is reconciled to it.

## 5. Horizons

- **Immediate (this/next session):** keep the five layers coherent; execute the approved next increment; verify green; update Plan + Memory.
- **Short term:** deepen autonomy (executable resource pipelines, scheduled evolution), and the approved VSB economic model; broaden the realm×domain coverage.
- **Long term:** the fully self-running organism — per-VSB living business plans, cross-VSB federation, the economic/charitable engine operating continuously under governance, with the knowledge system maintained largely autonomously and reviewed by you.

## 6. Consistency, Accuracy & Fidelity mechanisms
- **Honesty gate:** no "certified/passed/converged" without a real test/measurement; aspirational ≠ current state.
- **Verification before claim:** boot + tests + `tsc` + endpoint checks before marking done.
- **Single source of truth:** Code/Live State is authoritative; docs/memory reconcile to it.
- **Fidelity to you:** the Chief/Board represent your exact intent; the `UNDERSTANDING` doc is where I expose my interpretation for your correction.
- **Auditability:** gaas.v5 UEG + the dated changelog give a reviewable trail of what changed and why.

## 7. How you monitor and direct
- **Read** `UNDERSTANDING` (are we on the same page?) and `PLAN §7` (adherence scorecard — am I realising your vision?).
- **Query** `GET /api/v1/plan` (pillars/phases/adherence) and `/api/v1/plan/state` (live reality) anytime.
- **Direct** via the Board: `POST /api/v1/board/chief/instruct` — your Chief turns your wish into governed action.
- **Correct** by refining the Vision — `WORKSTATION_IDBO_WHOLE_VISION.md` §1–§15 (your words) and §18 (rulings; the delivery prompt lists what is still with you) — that is the authoritative channel for refining intent; `UNDERSTANDING` and the `PLAN` are then reconciled to it in the same session. (Corrected W446: this line had pointed at `UNDERSTANDING` §9, whose questions were resolved on 2026-06-21.)
- **Measure** rather than read: `python scripts/reach_audit.py` for the surface, `scripts/workflows/fidelity_audit_v3.js` for the section-by-section verdict (`docs/VISION_FIDELITY_LEDGER.md`), and the delivery plan in `docs/FABLE_DELIVERY_PROMPT.md` for what is being done about it, in what order, and how each item is proven.

> Companion: `WORKSTATION_IDBO_UNDERSTANDING.md`, `WORKSTATION_IDBO_LIVING_PLAN.md`, `VSB_ECONOMIC_LEGAL_MODEL.md`.
