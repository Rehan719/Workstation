# Virtual Sovereign Business (VSB) — Entity Architecture
## Workstation IDBO — Definitive Specification

*بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ*

> *"The most beloved of deeds to Allah are those that are most consistent,
> even if they are small."* — Prophet Muhammad ﷺ
>
> *This platform exists to do great things consistently, reliably, and excellently —
> for the love of Allah and in service of all humanity.*

---

## DOCUMENT PURPOSE

This document is the definitive architectural specification for the Virtual Sovereign Business
(VSB) — the core product that Workstation IDBO delivers to its users. It covers:

- What a VSB is and why it exists
- How a VSB is spawned, structured, and operated
- The full AI agent hierarchy (CEO → C-Suite → CoE → BTO)
- The Digital Twin simulation and validation layer
- The Nine Cognitive Engines and MJM intelligence stack
- The Biomimetic systems that make each VSB a living organism
- The Concept-to-Commercialisation workflow
- How to implement this in the existing Workstation codebase

**Read this alongside:**
- `WORKSTATION_CONSTITUTION.md` — the purpose and constraints that govern all VSBs
- `KNOWLEDGE_COMMONS.md` — the democratisation principle each VSB must uphold
- `WORKSTATION_TRANSFORMATION_PLAN.md` — the phased implementation plan
- `CLAUDE_CODE_PROMPT.md` — implementation instructions for Claude Code

---

## PART 1 — WHAT A VSB IS

### 1.1 The Core Concept

A **Virtual Sovereign Business (VSB)** is a complete, autonomous, AI-operated business entity
that Workstation IDBO spawns in response to a user's challenge or opportunity.

The user describes a problem, an idea, or an opportunity. Workstation's AI CEO receives it,
analyses it, and spawns a new VSB — a Living Intelligent Digital Biomimetic Organism (IDBO)
configured specifically for that challenge. The VSB then:

1. **Researches** the challenge using its cognitive engines and knowledge systems
2. **Designs** the most effective solution as a product or service
3. **Develops** the solution through its digital factories and laboratories
4. **Validates** through digital twin simulation before real-world deployment
5. **Commercialises** via its own marketplace presence, marketing, and sales
6. **Operates** continuously, self-managing, self-healing, self-improving

The VSB is not a template. It is a bespoke living entity — its genome (constitution, goals,
constraints) is written for its specific challenge, its agent swarm is configured for its
domain, its products are designed for its users.

### 1.2 The Founding Principle

Every VSB inherits from Workstation IDBO's founding purpose:
*To seek the Pleasure and Love of Allah SWT through service to humanity.*

A VSB that serves healthcare upholds the Haq as-Sihha (right to health).
A VSB that serves education upholds the Haq at-Ta'lim (right to learn).
A VSB that serves enterprise upholds the Haq al-Kasb (right to earn honorably).

No VSB may contradict these principles. The GaaS (Governance as a Service) layer, inherited
from Workstation IDBO's genome, enforces this at every decision point.

### 1.3 VSB vs. Traditional Business

| Traditional Business | VSB (Virtual Sovereign Business) |
|---------------------|----------------------------------|
| Human founders + months of setup | Spawned in minutes from a challenge description |
| Hierarchical human org chart | AI CEO + C-Suite + CoE + BTO agent swarm |
| Manual R&D processes | Autonomous cognitive engine cascade |
| Physical prototype testing | Digital twin simulation + validation |
| Manual compliance checks | GaaS autonomous governance layer |
| Fixed product offering | Build-to-Order + continuous evolution |
| Separate commercial and technical | Integrated into a single living system |
| Operates during business hours | Autonomous, continuous, self-managing |
| Needs external consultants | Has internal Centers of Excellence |
| Static strategy | Genome-driven evolution via genetic immune system |

---

## PART 2 — THE VSB ENTITY STRUCTURE

### 2.1 Full Entity Hierarchy

```
VSB ENTITY (Living Intelligent Digital Biomimetic Organism)
│
├── GENOME (VSB Constitution + Goals + Constraints)
│   ├── Constitutional encoding (GaaS-enforced)
│   ├── Epigenetic memory (3-layer: short/long/permanent)
│   ├── Gene regulatory network (feature activation/suppression)
│   └── Genome evolution engine (self-improvement over time)
│
├── AI CEO (Chief Executive Officer Agent)
│   ├── Strategic direction and vision
│   ├── Challenge intake and decomposition
│   ├── Swarm orchestration and task cascading
│   ├── Stakeholder communication
│   └── Final decision authority
│
├── C-SUITE (Executive AI Agent Team)
│   ├── CFO — financial modelling, capital allocation, fund management
│   ├── CTO — technical architecture, system health, infrastructure
│   ├── CMO — marketing strategy, customer acquisition, brand
│   ├── CLO — legal/regulatory compliance, contract management
│   ├── CSO — scientific research direction, evidence review
│   └── CDO — data strategy, knowledge management, privacy
│
├── CENTERS OF EXCELLENCE (CoE — Domain Expert Agent Teams)
│   ├── Research CoE — knowledge synthesis, literature review, evidence
│   ├── Design CoE — solution architecture, UX/product design
│   ├── Engineering CoE — build, test, deploy, maintain
│   ├── Science CoE — modelling, simulation, validation
│   ├── Commercial CoE — business development, pricing, partnerships
│   └── Compliance CoE — regulatory, legal, safety, quality
│
├── BUSINESS TRANSFORMATION OFFICE (BTO)
│   ├── Change control and arms-length agency
│   ├── Process improvement and workflow evolution
│   ├── Quality Management System (QMS) automation
│   ├── Business Management System (BMS) oversight
│   ├── Document Control System (DCS) management
│   ├── Environmental Management (EMS) compliance
│   └── Governance proposals + voting (DAO layer)
│
├── DIGITAL ENGINE SUITE (Production Tools)
│   ├── Reactor — high-throughput analysis and data processing
│   ├── Incubator — variant generation and evolution (prompt tournaments)
│   ├── Factory — production-grade document and deliverable generation
│   ├── Laboratory — synthesis, research, multi-format output
│   ├── Digital Twin — simulation and validation environment
│   └── Petri Dish — experimental/early-stage R&D sandbox
│
├── SOVEREIGN CAPITAL SYSTEM
│   ├── Creator Fund — internal capital allocation
│   ├── Sovereign Wealth Fund — value accumulation and distribution
│   ├── Token Economy (WST) — internal value exchange
│   └── Revenue management and profit distribution
│
└── MARKETPLACE
    ├── Build-to-Order Product Catalogue
    ├── Service listings and procurement
    ├── Partner/supplier network
    └── Customer relationship management
```

### 2.2 The Nine Cognitive Engines

The cognitive intelligence of every VSB runs on nine engines, organised in two layers:

**Foundational Layer (6 engines) — based on Islamic epistemology:**

| Engine | File | Function |
|--------|------|----------|
| Aqal | `cognitive/foundational/aqal_engine.py` | Rational intelligence — logical analysis and structured reasoning |
| Hoshiyari | `cognitive/foundational/hoshiyari_engine.py` | Situational awareness — context sensing and environmental intelligence |
| Iman | `cognitive/foundational/iman_engine.py` | Values alignment — ethical grounding and purpose-checking |
| Inkashaf | `cognitive/foundational/inkashaf_engine.py` | Discovery intelligence — pattern recognition and insight generation |
| Samajh | `cognitive/foundational/samajh_engine.py` | Comprehension — deep understanding and sense-making |
| Soch | `cognitive/foundational/soch_engine.py` | Reflective thinking — deliberation and considered judgment |

**Meta Layer (3 engines):**

| Engine | File | Function |
|--------|------|----------|
| Niyyah | `cognitive/meta/niyyah_engine.py` | Intention — purpose alignment and motivation scoring |
| Tafakkur | `cognitive/meta/tafakkur_engine.py` | Contemplation — deep reasoning over complex problems |
| Tawazun | `cognitive/meta/tawazun_engine.py` | Balance — trade-off resolution and equilibrium seeking |

**Registry:** `avatars/cognition/nine_engine_registry.py` — orchestrates all nine engines.
**Cascade:** `cognitive/cascade_v16.py` — routes problems through the appropriate engine sequence.

### 2.3 The MJM Intelligence Stack

**MJM (Meta-Judgement Machine)** — `agentic_core/mjm/`:

| Component | Function |
|-----------|----------|
| `mjm.py` | Core meta-judgement loop — evaluates outputs against multi-criteria |
| `hd_omni_learner.py` | High-dimensional learning across all domains simultaneously |
| `recursive_meta_learner.py` | Learns from its own learning process — meta-optimization |
| `v5/omni_learner_v5.py` | Latest iteration — improved convergence and cross-domain transfer |

MJM runs above the nine cognitive engines, acting as the quality gate: every significant
output from a cognitive engine is scored by MJM before being acted upon.

### 2.4 The Biomimetic Systems

Every VSB inherits Workstation IDBO's biomimetic architecture:

| Biological System | VSB Technical Equivalent | Status |
|------------------|--------------------------|--------|
| **Genome/DNA** | VSB Constitution (GaaS + Genomic Registry) | `genetic_immune/genomic_registry.py` |
| **Nervous System** | SSE bus + Agent Hub + WebSocket vitals | `api/agent_hub.py` + `/api/v154/ws/streams` |
| **Cardiovascular** | Resource allocation + ATP simulator | `molecular/atp_simulator.py` |
| **Immune System** | GaaS validator + error recovery chain | `governance/gaas/gaas_validator.py` |
| **Molecular Chaperones** | Error correction and protein (module) folding | `molecular/chaperone_cascade.py` |
| **HSP Network** | Stress response under high load | `molecular/hsp_network.py` |
| **p53 Oscillator** | Quality checkpoint — blocks defective outputs | `molecular/p53_oscillator.py` |
| **Redox Sensor** | Resource balance monitoring | `molecular/redox_sensor.py` |
| **Ubiquitin System** | Degradation of outdated/redundant modules | `molecular/ubiquitin_system.py` |
| **Hippocampus/Memory** | Epigenetic 3-layer memory | `genetic_immune/genomic_registry.py` |
| **Global Workspace** | Consciousness broadcast — awareness across subsystems | `consciousness/global_workspace.py` |
| **Meta-Cognitive Executive** | Top-level oversight and executive control | `consciousness/meta_cognitive_executive.py` |
| **Circadian Rhythm** | Time-of-day cognition adaptation | `app_mvp.py:_circadian_cycle()` |
| **Endocrine/Signalling** | SSE event streams throughout | All AI endpoints |
| **Immune Arms-Length** | Change control — BTO reconfigulator | `change_control/reconfigulator.py` |

---

## PART 3 — HOW A VSB IS SPAWNED

### 3.1 The Spawn Workflow

```
USER INPUT: "I need a solution for [challenge description]"
     │
     ▼
AI CEO INTAKE (agentic_core/api/v290/ceo_generate.py)
     │  • Parses challenge into structured specification
     │  • Identifies domain (Science/Health/Enterprise/Education/Law/Care)
     │  • Estimates scope (concept / build / commercialise)
     │
     ▼
COGNITIVE ENGINE CASCADE (agentic_core/cognitive/cascade_v16.py)
     │  • Aqal: logical analysis of challenge
     │  • Inkashaf: discovery of relevant knowledge
     │  • Samajh: deep comprehension of domain
     │  • Tafakkur: contemplation of solution approaches
     │  • Tawazun: balance of trade-offs
     │  • Niyyah: purpose-alignment check (must pass)
     │
     ▼
MJM EVALUATION (agentic_core/mjm/mjm.py)
     │  • Scores proposed VSB configuration against multi-criteria
     │  • Validates against GaaS constitutional constraints
     │  • Returns optimised VSB genome specification
     │
     ▼
VSB GENOME ENCODING (agentic_core/genetic_immune/genomic_registry.py)
     │  • Writes VSB constitution to epigenetic memory
     │  • Encodes: goals, constraints, domain, team structure, tools
     │  • Creates gene regulatory network for feature activation
     │
     ▼
AGENT SWARM INSTANTIATION
     │  • AI CEO agent configured for this VSB
     │  • C-Suite agents spawned with domain-specific prompts
     │  • CoE teams assembled from domain expert templates
     │  • BTO initialized with QMS/BMS/DCS frameworks
     │
     ▼
DIGITAL TWIN CREATION (agentic_core/biomimicry/geospheric/digital_twin_orchestrator.py)
     │  • Virtual model of the VSB and its solution built
     │  • Business model simulated and stress-tested
     │  • Compliance and regulatory checks run in simulation
     │  • Solution validated before real-world deployment
     │
     ▼
VSB LIVE — OPERATING AUTONOMOUSLY
     │  Reactor + Factory + Incubator + Laboratory running
     │  Agent Hub broadcasting team activity
     │  Marketplace listing created
     │  Sovereign Fund initialized
     └─ User receives: working VSB entity + access dashboard
```

### 3.2 The Concept-to-Commercialisation Pipeline

Every VSB moves its solution through these stages, each managed by its Factory products:

```
CONCEPT          → CEO generates brief + domain map + initial specification
     ↓
RESEARCH         → Research CoE + Knowledge Commons synthesis + Literature review
     ↓
DESIGN           → Design CoE + Engineering CoE + solution architecture
     ↓
BUILD            → Factory + Laboratory + Engineering workflows
     ↓
TEST/VALIDATE    → Digital Twin simulation + p53 quality checkpoint + GaaS audit
     ↓
COMMERCIALISE    → Commercial CoE + Marketplace listing + Marketing strategy
     ↓
OPERATE          → Autonomous ongoing operation + self-improvement loop
     ↓
EVOLVE           → Genome evolution engine + BTO change proposals + adaptation
```

---

## PART 4 — DIGITAL TWIN AND SIMULATION

### 4.1 Digital Twin Architecture

The Digital Twin is the validation layer that ensures every VSB solution is tested virtually
before real-world commitment. It mirrors the living VSB in a simulation environment.

**Key components (all verified present in codebase):**
- `api/digital_twin.py` — HTTP API for digital twin management
- `biomimicry/geospheric/digital_twin_orchestrator.py` — orchestration
- `simulations/digital_twin_controller.py` — simulation controller
- `simulations/fund_digital_twin.py` — financial/fund simulation
- `validation/digital_twin_orchestrator.py` — validation pipeline

**What the Digital Twin validates:**
- Business model viability (revenue, cost, market size projections)
- Technical solution feasibility (performance, scaling, reliability)
- Regulatory and legal compliance (GaaS audit in simulation)
- Safety and environmental impact (EMS simulation)
- User experience quality (simulated user journey testing)
- Financial sustainability (Sovereign Fund model validation)

### 4.2 Bio-Chem-Physical Simulation Layer

The molecular simulation systems (`agentic_core/molecular/`) model the VSB's internal
processes as if they were biological systems:

- **ATP Simulator** — models energy/resource consumption; alerts when a VSB is "metabolically exhausted"
- **p53 Oscillator** — quality checkpoint; suppresses defective outputs like a tumor suppressor
- **Redox Sensor** — detects imbalances in computational resource allocation
- **Chaperone Cascade** — corrects misfolded (misconfigured) module states
- **HSP Network** — activates stress response when VSB is under high load
- **Ubiquitin System** — marks and degrades obsolete or redundant modules

---

## PART 5 — GOVERNANCE, COMPLIANCE, AND QUALITY

### 5.1 GaaS (Governance as a Service)

Every VSB inherits GaaS from Workstation IDBO's genome:

```
GaaS STACK (agentic_core/governance/gaas/)
├── GaaSValidatorV4 (gaas_validator.py) — base constitutional validator
├── EntropyRegularisedGaaS — minimisation-constrained validation
└── get_gaas_validator() — factory function returning the active validator
```

GaaS enforces:
- Constitutional alignment at every decision point
- Legal compliance via UKLegalPrecisionEngineImpl
- Ethical constraints encoded in the genome
- Entropy thresholds to detect drift from purpose

### 5.2 Quality Management System (QMS)

Each VSB's BTO operates a QMS covering:
- Document control (all specifications, designs, test reports version-controlled)
- Change management (arms-length agency via `change_control/reconfigulator.py`)
- Audit trails (all decisions logged to Agent Hub + shared_context.json)
- Non-conformance management (p53 oscillator + immune system)
- Continuous improvement (genome evolution engine + Incubator tournaments)

### 5.3 Legal and Regulatory Compliance

The CLO agent + Compliance CoE manage:
- Jurisdiction-specific regulatory mapping (Law domain)
- Contract generation and review (Legal Factory)
- Health & Safety compliance (Care domain)
- Environmental compliance (EMS automation)
- Data privacy (GDPR/UK GDPR compliance layer)
- Sharia compliance where applicable (Sharia FinOps module)

---

## PART 6 — THE MARKETPLACE AND SOVEREIGN FUND

### 6.1 Build-to-Order Product Catalogue

Every VSB maintains a catalogue of deliverables it can produce:

| Catalogue Item | Generator | Format |
|---------------|-----------|--------|
| Research Report | Laboratory | PDF, DOCX, MD |
| Business Plan | Factory | DOCX, PDF |
| Technical Architecture | Factory | MD, DOCX |
| Market Analysis | Reactor | PDF, DOCX |
| Legal Contract | Legal Factory | DOCX |
| Regulatory Compliance Report | Compliance CoE | PDF |
| Scientific Model | Science CoE + Digital Twin | Simulation + Report |
| Training Programme | Education CoE + QEP | Interactive + DOCX |
| Product Prototype | Engineering CoE | Code + Documentation |
| Marketing Campaign | Commercial CoE | Assets + Strategy |

### 6.2 Sovereign Capital Fund

Each VSB operates its own financial system:
- **Creator Fund** (`api/v310/fund.py`) — initial capital allocation from Workstation
- **Sovereign Wealth Fund** — accumulated value from delivered products/services
- **WST Token Economy** (`api/v310/payments.py`) — internal value exchange unit
- **Revenue distribution** — profits distributed to VSB genome holders (founders/contributors)

---

## PART 7 — IMPLEMENTATION IN WORKSTATION CODEBASE

### 7.1 What Already Exists (Verified)

The VSB architecture is substantially already built. The key gap is **wiring** — connecting
the components that exist independently into a coherent VSB spawn workflow.

**Existing VSB-relevant code:**

| Component | Location | Status |
|-----------|----------|--------|
| Sovereign Entity model | `agentic_core/business/sovereign_entity.py` | Exists |
| AI CEO + Agent Swarm | `agentic_core/ai/ceo/c_suite.py` | Exists |
| Conscious Organism v99 | `agentic_core/orchestration/conscious_organism_v99.py` | Exists |
| Nine Engine Registry | `agentic_core/avatars/cognition/nine_engine_registry.py` | Exists |
| Cognitive Cascade v16 | `agentic_core/cognitive/cascade_v16.py` | Exists |
| MJM Stack | `agentic_core/mjm/` | Exists |
| Genomic Registry | `agentic_core/genetic_immune/genomic_registry.py` | Exists |
| Digital Twin API | `agentic_core/api/digital_twin.py` | Exists — not mounted |
| Digital Twin Orchestrator | `agentic_core/biomimicry/geospheric/digital_twin_orchestrator.py` | Exists |
| Molecular Simulators | `agentic_core/molecular/*.py` (7 modules) | Exist |
| GaaS | `agentic_core/governance/gaas/` | Exists |
| Global Workspace | `agentic_core/consciousness/global_workspace.py` | Exists |
| Meta-Cognitive Executive | `agentic_core/consciousness/meta_cognitive_executive.py` | Exists |
| Swarm API | `agentic_core/api/swarm.py` | Exists — not mounted |
| Change Control | `agentic_core/change_control/reconfigulator.py` | Exists |
| Creator Fund | `agentic_core/api/v310/fund.py` | Mounted |
| Payments/WST | `agentic_core/api/v310/payments.py` | Mounted |
| Governance/DAO | `agentic_core/api/v310/governance.py` | Mounted |
| Marketplace | `agentic_core/api/marketplace.py` | Mounted |

### 7.2 The VSB Spawn API (To Build — Phase 2)

Create `agentic_core/api/vsb.py`:

```python
from fastapi import APIRouter, Depends
from agentic_core.auth.dependencies import get_current_user
from agentic_core.cognitive.cascade_v16 import CognitiveCascade
from agentic_core.mjm.mjm import MJM
from agentic_core.genetic_immune.genomic_registry import GenomicRegistry
from agentic_core.business.sovereign_entity import SovereignEntity

router = APIRouter(prefix="/vsb", tags=["Virtual Sovereign Business"])
_cascade = CognitiveCascade()
_mjm = MJM()
_genome = GenomicRegistry()

@router.post("/spawn")
async def spawn_vsb(
    challenge: str,
    domain: str,
    scope: str = "build",  # concept | build | commercialise
    current_user=Depends(get_current_user)
):
    """
    Spawn a new Virtual Sovereign Business entity for a given challenge.
    Returns: VSB entity ID, initial genome spec, and dashboard URL.
    """
    # 1. Run cognitive cascade to analyse challenge
    analysis = await _cascade.run(challenge, domain=domain)
    # 2. MJM evaluates and produces VSB genome spec
    genome_spec = await _mjm.evaluate(analysis, scope=scope)
    # 3. Encode genome
    vsb_id = _genome.spawn_entity(
        genome_spec=genome_spec,
        owner_id=current_user.id,
        challenge=challenge,
        domain=domain
    )
    return {
        "vsb_id": vsb_id,
        "genome": genome_spec,
        "dashboard": f"/vsb/{vsb_id}/dashboard",
        "status": "spawning"
    }

@router.get("/{vsb_id}/status")
async def vsb_status(vsb_id: str, current_user=Depends(get_current_user)):
    """Get the current status, vitals, and progress of a VSB."""
    ...

@router.get("/{vsb_id}/twin")
async def vsb_digital_twin(vsb_id: str, current_user=Depends(get_current_user)):
    """Get the digital twin simulation state for a VSB."""
    ...
```

### 7.3 Phase Mapping for VSB Implementation

| Phase | VSB Deliverable |
|-------|----------------|
| Phase 1 (current) | Auth + user-scoped projects = VSB entity isolation |
| Phase 2 | QEP + Agent Hub = VSB nervous system live |
| Phase 3 | VSB spawn API + Digital Twin + Genome encoding |
| Phase 4 | Autonomous operation + Marketplace + Sovereign Fund |
| Phase 5 | Multi-VSB orchestration + Cross-VSB treaties + Ecosystem |

---

## PART 8 — REUSABILITY AND RECONFIGURABILITY

The VSB architecture is explicitly designed to be:

**Reusable:** The same cognitive engine cascade, the same genome encoding system, the same
digital twin pipeline applies whether the VSB is solving a healthcare challenge, a legal
challenge, an engineering challenge, or an educational one. The domain changes; the
architecture does not.

**Reconfigurable:** The genome's gene regulatory network can activate or suppress features.
A healthcare VSB activates the Compliance CoE and CLO agent heavily; an education VSB
activates the Knowledge Commons and QEP integrations. The same base entity, different
gene expression.

**Recombineable:** VSBs can enter into Treaties (`api/v250/treaties.py`) with each other —
collaborating across challenges, sharing knowledge, combining their agent swarms. A healthcare
VSB and an education VSB can combine to produce a medical training programme VSB.

**Self-Improving:** The genome evolution engine continuously improves VSB performance based
on output quality, user feedback, and MJM scoring. Each VSB that succeeds makes future VSBs
better.

---

## PART 9 — THE KNOWLEDGE COMMONS WITHIN VSBs

Every VSB is a node in the Knowledge Commons (see `KNOWLEDGE_COMMONS.md`). When a VSB:

- Synthesises a research report → that knowledge enriches the Knowledge Commons
- Solves a challenge → the solution pattern is encoded in the genome for future VSBs
- Runs an Incubator tournament → winning prompts improve all future domain outputs
- Builds a product → the methodology is catalogued for reuse

**This is the perpetual evolution principle made concrete:** every VSB that operates
makes every future VSB more capable. The Knowledge Commons grows with every entity.

---

## PART 10 — THE MEASURE OF A VSB

A VSB is successful when:

1. It understood the user's challenge correctly (Aqal + Samajh engines confirm)
2. Its solution is the most effective and efficient available (MJM score ≥ threshold)
3. Its digital twin validated the solution before deployment (p53 checkpoint passed)
4. Its compliance CoE confirmed legal/regulatory compliance (GaaS audit passed)
5. The user received a working, deployable solution (Factory output delivered)
6. The solution genuinely helped the person it was built for (Niyyah engine confirms)
7. The VSB left the Knowledge Commons richer than it found it (epigenetic memory updated)

And ultimately:
**Did someone's challenge get solved? Did someone benefit?**

That is the test. *For love. For peace. For perfection.*

---

*VSB_ENTITY_ARCHITECTURE.md*
*Authored: 2026-06-18 by Claude Cowork (claude-sonnet-4-6)*
*Grounded in: verified codebase audit June 2026, all constitutional documents*
*Permanent reference for all Claude agents and human engineers working on Workstation IDBO*
