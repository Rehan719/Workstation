# The Quran Education Platform (QEP) — Whole Vision

> **Status:** Canonical vision capture, reconstructed from primary sources.
> **Compiled:** 2026-09-06
> **Sources:** three separate build attempts in `C:\Users\rehan\github_repos`, plus ~2.4 MB (2,395,108 bytes; 2.1 MB net of two byte-identical duplicates) of original planning
> transcripts preserved under `Quran-recitation-platform/sources/`.
> **Read with Appendix A.9 of `WORKSTATION_IDBO_WHOLE_VISION.md`.** Six capabilities this document describes as
> vision are FORBIDDEN by that canon's §11 faith-content constitution — recitation scoring (Feature 2, §11's recitation-analysis service),
> generated Qur'an Arabic, translation of sacred text, emotion inference (Features 10 and 12, §11, §12, §14), the
> Fitrah Spectrum as a measurement (Feature 10, §12) and an AI Ask-a-Scholar (Feature 7). They are ratified
> boundaries, not gaps to close; they are marked ⛔ A.9 below where they occur.
> **Purpose:** hold, in one document, the *complete* vision — concept, objectives, features, intelligence layer, architecture, roadmap, governance, finance and methodology — so that no future attempt has to re-derive it from scattered transcripts again.

**Naming.** Across the sources the product is called, interchangeably: *AI-Driven Quranic Education Platform*, *Quran Education AI Platform*, *QEP*, and *Quran-Education-AI-Platform*. They are one product. This document uses **QEP**.

---

## Table of Contents

**Part I — Provenance & Audit**
1. [Why this document exists](#1-why-this-document-exists)
2. [The three attempts](#2-the-three-attempts)
3. [What each attempt actually produced](#3-what-each-attempt-actually-produced)
4. [Why the attempts stalled](#4-why-the-attempts-stalled)

**Part II — The Vision**
5. [Concept](#5-concept)
6. [Vision statement](#6-vision-statement)
7. [The four core goals](#7-the-four-core-goals)
8. [Strategic objectives](#8-strategic-objectives)

**Part III — Features**
9. [The 15 core features](#9-the-15-core-features)
10. [Full feature catalogue](#10-full-feature-catalogue)

**Part IV — The Intelligence Layer**
11. [Phase 14 — the Neural Core](#11-phase-14--the-neural-core)
12. [The Fitrah Spectrum](#12-the-fitrah-spectrum)
13. [Swarm intelligence](#13-swarm-intelligence)
14. [The Adaptive UI/UX engine](#14-the-adaptive-uiux-engine)
15. [The Personalized Guidance application](#15-the-personalized-guidance-application)

**Part V — Architecture & Technology**
16. [System architecture](#16-system-architecture)
17. [Technology stack — three tiers](#17-technology-stack--three-tiers)
18. [Repository structure](#18-repository-structure)

**Part VI — Roadmap**
19. [The 19-phase roadmap](#19-the-19-phase-roadmap)
20. [Phase-to-feature mapping](#20-phase-to-feature-mapping)
21. [The competing Phase 15–19 orderings](#21-the-competing-phase-1519-orderings)

**Part VII — Governance, Ethics & Finance**
22. [Governance model](#22-governance-model)
23. [Financial model](#23-financial-model)
24. [Compliance and ethics](#24-compliance-and-ethics)
25. [Implementation strategy](#25-implementation-strategy)

**Part VIII — Method**
26. [LEAN-Turbo methodology](#26-lean-turbo-methodology)
27. [PromptOps and AI-agent development](#27-promptops-and-ai-agent-development)

**Part IX — Unresolved**
28. [Contradictions and open decisions](#28-contradictions-and-open-decisions)
29. [What the vision never specified](#29-what-the-vision-never-specified)

**Part X — Traceability**
30. [Source map](#30-source-map)

---

# Part I — Provenance & Audit

## 1. Why this document exists

Three times between May and June 2025 this vision was handed to an AI agent ("Jules") to build. Three times a repository was created, populated, and abandoned. The vision itself was never the problem — it survived intact across all three attempts, scattered across ~2.4 MB of chat transcripts, four generations of phase guides, two "Guide" documents, and a documentation pipeline that failed and then began emitting placeholders into its own canonical outline.

The most valuable asset in all three repositories is **not the code**. It is the vision material. This document consolidates it.

## 2. The three attempts

| # | Repository | First commit | Last commit | Commits | Merged PRs | What it was |
|---|---|---|---|---|---|---|
| 1 | `quran-recitation-mvp` | 2025-05-27 | 2025-06-18 | 317 | up to #68 | The original MVP. Real running code, then a feature-folder re-scaffold that was never filled in. |
| 2 | `Quran-recitation-platform` | 2025-06-09 | 2025-06-18 | 130 | up to #47 | The documentation-and-design attempt. Richest vision artefacts; code explicitly labelled "conceptual". |
| 3 | `QEP-MVP` | 2025-06-16 | 2025-06-18 | 18 | up to #3 | The clean-monorepo restart. Smallest, most structurally correct, least complete. |

All three were abandoned on the same day — 2025-06-18 — each with an identical final commit, `Update .gitignore and add .env.example`. None has a git remote configured locally.

The three are not competing designs. They are **three passes at the same plan**, and each holds something the others lack:

- **Attempt 1** holds the only genuinely executed code, and the original recitation/video MVP that every later phase guide refers back to as "the MVP to integrate".
- **Attempt 2** holds the vision itself: the source transcripts, the Developer Guide, the 15-feature definition, the consolidated phase guide, and the Phase→Feature mapping table.
- **Attempt 3** holds the cleanest architecture — a proper workspace monorepo with `packages/backend`, `packages/frontend`, `packages/services/*` and real infra config.

## 3. What each attempt actually produced

### Attempt 1 — `quran-recitation-mvp`

**Reality:** ~4,300 lines of TypeScript/Python across 97 TypeScript/Python source files (107 with JavaScript), 349 tracked files. A `backend/` (NestJS) and `frontend-vite/` (React + Vite) pair that was actually run — the repository contains ~30 captured build logs, an npm audit trail, and a `vite_dev_output.txt`, which is evidence of a real dev loop rather than generated-and-never-executed code.

**The re-scaffold:** partway through, the repo was reorganised into `features/<feature-name>/{ai,backend,frontend,tests}` — one directory per core feature. The audit result:

| Feature folder | Files | Non-empty |
|---|---|---|
| `ai-tajwid-coach` | 52 | 41 |
| `user-authentication-profile-management` | 15 | 10 |
| `shared` | 17 | 4 |
| `memorization-suite` | 7 | 2 |
| **12 other feature folders** | **5 each** | **0** |

Twelve of the fifteen core features — adaptive UI, admin/analytics, AI guidance & Fitrah, community, educator platform, gamified learning, AR/VR, learner modules, settings/globalization, billing/donations, swarm intelligence, video conferencing — exist only as **empty directory skeletons with zero-byte README files**.

**Build state as last captured (commit f59a44d, 2025-06-07 — 102 commits before the 2025-06-18 abandonment, after which `frontend-vite/src` was cut from 317 tracked files to 6):** broken. `npm_build_error_log_latest.txt` records **209 TypeScript errors** (TS6133 unused declarations 49 · TS2339 46 · TS1484 19 · TS7006 implicit `any` 16 · TS2300 14 · TS2304 13 — no parse failures in that log); two other captured builds (`npm_build_output_manual_targeted.txt`, `npm_build_output_post_cleanup.txt`) fail on a `TS1128` syntax error in `src/components/Admin/PlatformSettings.tsx`. All 35 logs were committed together in that one commit, so none is git-orderable as "final".

### Attempt 2 — `Quran-recitation-platform`

**Reality:** ~11,400 lines across 213 source files — the largest of the three — but self-declared conceptual. The largest backend file, `mvp/backend/src/teaching/teaching.service.ts` (17 KB), opens with:

```ts
// import { InjectRepository } from '@nestjs/typeorm'; // Conceptual
// import { Repository } from 'typeorm'; // Conceptual
...
// In-memory stores for conceptual MVP
private conceptualClasses: Map<string, ClassEntity> = new Map();
```

Every persistence path is a commented-out TypeORM import backed by an in-memory `Map`. Its own README says so plainly: *"the skeleton structure… theoretical steps for installation"*. The backend nonetheless has 15 module directories covering nearly the whole feature set — auth, billing, community, competitions, gamification, institutional, learning, memorization, recitation, settings, teaching, users, video-conferencing, admin, ai-guidance — which makes it the **best structural map of the intended domain model**, even though nothing persists.

**Where the value is:** `sources/` (18 transcripts, ~2.4 MB), `docs/` (consolidated source material, core-features definition, the 1,162-line consolidated phase guide), the 109 KB Developer Guide, the 75 KB Jules Agent Guide, and `planning/` (audit summary, status reports, worklog).

### Attempt 3 — `QEP-MVP`

**Reality:** ~3,400 lines across 86 source files, 132 tracked files. Structurally the cleanest: `pnpm-workspace.yaml`, `packages/{backend,frontend,services/*}`, `infra/{docker,kafka-config,terraform}`, `.github/` with issue and PR templates, and a CI workflow that went green after three fix commits.

**Coverage:** only Phases 1–3 were genuinely attempted — `auth`, `billing`, `donations`, `mfa`, `profiles`, `users` on the backend; auth, billing and donations features on the frontend. All four microservices (`recitation-analysis`, `llm-nlp`, `guidance-assistant`, `aco-optimizer`) exist as FastAPI stubs. `recitation-analysis/main.py` is explicit:

```python
def analyze_recitation_stub(audio_file_path: str) -> dict:
    """Placeholder function to simulate recitation analysis."""
    score = len(filename) % 100  # Dummy score
```

**File misplacement:** the agent's own commit message admits *"files that were placed in unexpected locations due to environment constraints"*. The damage is visible and real:

- `packages/backend/src/billing/recitation.service.ts`, `Competition.service.ts`, `Competition.gateway.ts`, `Competition.controller.ts` — Phase 4 and Phase 5 code filed under `billing/`.
- `packages/frontend/src/features/auth/components/CompetitionCompetitionDetailsPage.tsx`, `RecitationSubmissionPageFallback.tsx`, `RecitationHistoryPageFallback.tsx` — recitation and competition UI filed under `auth/`, with doubled name prefixes and `Fallback` suffixes.

## 4. Why the attempts stalled

The three attempts failed for three *different* reasons. All three are worth carrying forward as constraints on any fourth attempt.

**1. Attempt 1 — generation outran verification.** 209 TypeScript errors in the last captured build log, 35 build logs committed into the repo, and a `features/` re-scaffold that created 19 directories and filled 4. Code was produced faster than it was compiled, and the reorganisation was a plan for work that never happened.

**2. Attempt 2 — the documentation pipeline broke, and nobody noticed it was emitting placeholders.** The Python doc-generation chain (`generate_inventory.py` → `extract_plan_sections.py` → `synthesize_outline.py`) failed on an `os.stat()` issue in the sandbox that returned zero file sizes and default timestamps. The visible consequence is `docs/canonical_phase_outline.md` — a document that presents itself as the single source of truth and contains, for all twenty phases, only:

```
-   **Goal**: [Details to be consolidated from source documents]
-   **Core Components & Features**:
    -   - **Goal**: [Placeholder - Details from canonical_phase_outline.md] (from Jules-guide.txt)...
```

Worse, the phase *titles* were auto-derived from arbitrary matched lines, producing headings such as *"Phase 3: 3. ReinforcementLearningService (reinforcementLearningService.ts)"* and *"Phase 15: ** Feature-complete platform (Phase 15). Need AI-generated comprehensive tests"*. The canonical outline became noise while continuing to be cited as canon. **The real phase content survives only in `docs/phase-guides/phases1-19.md`**, which was maintained by hand.

**3. Attempt 3 — a restart with no time to reach the interesting part.** Eighteen commits over two days, several of them spent fixing CI's package-manager installation. It reached Phase 3 of 19 and stopped.

**The common thread:** all three attempts spent their effort on the phases *least* distinctive to this product — monorepo setup, auth, billing — and none reached Phase 14, the Neural Core, which the plan itself identifies as the reason the platform exists. Every phase guide across every attempt rates Phase 14 *Effort: High / Impact: **Transformational***. It was never begun.

---

# Part II — The Vision

## 5. Concept

QEP is a comprehensive digital platform designed to revolutionise Quranic learning through the integration of advanced technologies: artificial intelligence and machine learning, voice recognition, emotion detection, AI agents, swarm intelligence, augmented and virtual reality, and video conferencing.

It offers a dynamic and personalised learning environment for **both learners and educators**, with tailored feedback, engaging competitions, interactive recitation, and a collaborative learning space. It is designed for scalability and accessibility across web, iOS and Android, and — at the ambitious end — AR/VR headsets.

At the heart of the platform are AI/ML-driven components:

- **AI Agents and the AI Guidance Assistant** provide personalised recommendations that optimise individual learning paths.
- **The AI Swarm system** leverages collective intelligence to improve group learning outcomes.
- **Video Conferencing and VR/AR features** create an immersive environment simulating a traditional classroom.

The framing that recurs most across the sources: this is not only an education product but *"an innovative Muslim social media platform"* — Quranic education delivered through reading, memorisation, competition, learning, teaching and guided reflection, wrapped in social networking and gamification, and governed as a **Sharia-compliant, waqf–trust hybrid**.

## 6. Vision statement

The canonical wording, consistent across `AI-Driven Quranic Education Platfor SAVED.txt` (sic), the `… Jules Updated (2).txt` file, and the Developer Guide:

> To deliver a **universally accessible, immersive, and ethically grounded Quranic education platform** that empowers Muslims of all ages to **recite, memorize, understand, and live the Quran** — through the seamless integration of AI, AR/VR, video conferencing, social learning, and gaming technologies, all within a **fully Sharia-compliant, trust-based framework**. This platform offers personalized, emotionally responsive learning via AI agents, immersive environments, and collaborative tools. It supports recitation, memorization, learning, teaching, competitions, and guided reflection — accessible on any device and optimized for underserved regions.

### Vision in action (the five-line summary from the source)

- **Platform & Trust** powers a global, Sharia-compliant AI Quranic learning system built by a not-for-profit trust.
- **Features & Technology** integrate immersive AR with VC and VR, AI coaching, and gamified social media.
- **Objectives** focus on free access to Quranic education, personalisation, community, and authentic & ethical integrity.
- **Governance** is led by elected volunteers, a Sharia board, and specialist teams ensuring transparency and compliance.
- **Join Us** to co-create, volunteer, and advance this dawah-driven mission, seeking the pleasure and love of Allah SWT.

## 7. The four core goals

Every line of code, feature and decision is required by the governance rules to tie demonstrably to one of four goals:

1. 🧕🏽 **Learn Quran** — acquire knowledge and understanding
2. 🎙️ **Recite Quran** — improve pronunciation and Tajwīd
3. 📚 **Understand Quran** — grasp meaning, context and relevance through Tafsir and guidance
4. 🌍 **Teach Quran** — empower educators to guide others

This is the single most useful scoping test in the entire corpus. It is stated in the LEAN governance section of the phase guide and is the closest thing the vision has to a definition of "in scope".

## 8. Strategic objectives

Eight objectives, consistent across the detailed sources:

### 8.1 Universal Accessibility
Access on mobile, tablet, desktop, AR/VR headsets, smart TVs; low-bandwidth and offline modes (PWA); **Starlink (or similar) integration for remote and underserved areas**; multilingual UI/UX and content including RTL languages (Arabic, Urdu, Bahasa).

### 8.2 AI-Powered Personalized Learning
Dynamic, learner-specific pathways adapting to each individual's pace, proficiency and style. Real-time Tajwīd correction, memorisation coaching, and emotion-aware feedback. Mastery-based progression.

### 8.3 Adaptive UI/UX Based on User Profile
Responsive interface layouts, content presentation and navigation flows tailored by:
- **Age group** — children, teens, adults
- **Role** — learner, teacher, parent, administrator
- **Skill level** — beginner, intermediate, advanced
- **Cognitive preference** — visual, auditory, kinesthetic
- **Emotional state** — detected via emotion recognition

### 8.4 Immersive Education Tools
- AR overlays for Tajwīd visualisation, highlighting articulation points (*makhārij*) and 3D mouth shapes
- VR journeys through Quranic stories and historical sites (Meccan revelations, early Islamic events)
- Virtual mosque experiences
- **3D memory palaces** to anchor verses in spatial-visual contexts

### 8.5 Connected Global Communities
Peer mentoring, recitation competitions, virtual study circles, virtual events. Regional and international leaderboards, group challenges, collaborative study circles.

### 8.6 Sharia & Ethics Compliance
Scholar-led governance board, regular Sharia audits, GDPR-aligned data practices, transparent AI-ethics guidelines, Islamic finance principles embedded in payment and donation flows.

### 8.7 Cross-Device Compatibility
Consistent, responsive UI/UX across web, iOS, Android, tablets, smart TVs, and VR/AR.

### 8.8 Privacy & Security
End-to-end encryption, robust Role-Based Access Control (RBAC), Multi-Factor Authentication (MFA), PII encryption, GDPR and Sharia-compliant data handling.

### Supporting objectives (from the earlier V1.1 source)
- **Emotional Intelligence** — emotion detection adjusts learning content and provides encouragement based on user emotion.
- **AI Agents** — interactive agents that guide learners through lessons, explain, and give personalised feedback.
- **Swarm Intelligence** — collaborative learning methods through AI swarm algorithms enhancing group-based learning.

---

# Part III — Features

## 9. The 15 core features

The vision was distilled — in `docs/core_features_definition.md`, dated 2024-07-19 — into exactly fifteen core features plus a shared area. This is the authoritative feature decomposition.

| # | Feature | One-line scope |
|---|---|---|
| 1 | **User Authentication & Profile Management** | Identity, MFA, OAuth, RBAC (learner/teacher/parent/admin), profiles, preferences |
| 2 | **AI Tajwīd Coach** | Real-time recitation feedback: phonetic analysis, Tajwīd error identification, scoring |
| 3 | **Memorization Suite** | Flashcards, Spaced Repetition (SM-2), heatmap gap analysis, AI memory coaching |
| 4 | **Gamified Learning & Competitions** | Skill-based competitions, leaderboards, XP, badges, streaks |
| 5 | **Learner-Centric Learning Modules** | Curated lessons, quizzes, AI learning paths, AI explanations of text |
| 6 | **Educator Platform & Class Management** | Virtual classes, enrolment, module assignment, progress analytics, AI suggestions |
| 7 | **Community Engagement Platform** | Forums, Q&A, events, study circles, recitation rooms, Ask-a-Scholar, AI moderation |
| 8 | **Video Conferencing & Collaboration** | HD 1:1/group video, screen share, whiteboard, recording, live AI transcription, chat |
| 9 | **Immersive AR/VR Experiences** | AR Tajwīd visualisation, VR historical walkthroughs, virtual mosque |
| 10 | **AI Guidance & Fitrah Profiling System** | Conversational AI, Fitrah psychometric profile, ethical/spiritual guidance, voice UI |
| 11 | **Swarm Intelligence & Collaborative Learning** | ACO over collective behaviour to optimise group learning and recommendations |
| 12 | **Adaptive UI/UX Engine** | UI adapts to profile, preference and real-time emotional state |
| 13 | **Platform Settings, Globalization & Accessibility** | i18n/RTL, themes, notifications, privacy, a11y, PWA offline, certifications |
| 14 | **Secure Billing, Subscriptions & Donations** | Sharia-compliant billing, Zakat donations, donor dashboard, Sponsor-a-Student |
| 15 | **Admin, Analytics & Platform Governance** | Admin console, moderation, role-based analytics, Parental Insights, audit, compliance |

Underpinning all fifteen is a conceptual sixteenth, **Platform Core & Foundational Technologies** (ID: `Core-Infra`) — monorepo, CI/CD, core infrastructure, GraphQL, deployment, QA and support.

## 10. Full feature catalogue

Each feature below carries its scope, its user stories as written in the Developer Guide, and its rationale.

---

### Feature 1 — User Authentication & Profile Management

**Scope.** All aspects of user identity: secure registration (email/password, OAuth via Google/Apple), login, Multi-Factor Authentication, password reset, session management (JWT access + refresh tokens). Management of user profiles covering basic information (name, age range) and foundational learning preferences consumed by other modules. Role-Based Access Control defining **learner, teacher, parent, admin**.

**User stories.**
- Users can register using email/password or through OAuth providers (Google, Apple).
- Registered users can securely log in and log out.
- Users can enable and use MFA for enhanced account security.
- Users can manage basic profile information (name, age range) and set foundational learning preferences.
- Access to platform features is controlled by user roles.

**Rationale.** Fundamental for any personalised, secure multi-user platform. RBAC is critical for differentiating experiences and access levels; profiles are the key to personalisation.

---

### Feature 2 — AI Tajwīd Coach · ⛔ A.9.1 — recitation is never scored; written-recall only

**Scope.** Real-time feedback on Quranic recitation: phonetic analysis, identification of Tajwīd errors (Madd, Ghunnah, and the wider rule set), and scoring. Audio capture, processing via AI models (fine-tuned Whisper for Arabic plus rule-based systems), and user-friendly display of feedback. Multiple recitation modes catering to different learner levels.

**User stories.**
- Users can select a Quranic verse or passage to recite.
- Users can record their recitation using the device microphone.
- The platform analyses submitted audio and provides feedback on Tajwīd accuracy, highlighting errors.
- Users can view a score or qualitative assessment of their recitation.

**Designed output shape** (from the service contract): phonetic transcription, list of Tajwīd errors with positions, per-segment detailed feedback, confidence score, overall score, and textual recommendations.

**Rationale.** The cornerstone feature, directly addressing the platform's primary goal. Highlighted in every planning document without exception.

---

### Feature 3 — Memorization Suite

**Scope.** Memorisation of Quranic verses using flashcards, a Spaced Repetition System (SM-2 algorithm) for optimal review scheduling, progress tracking with heatmaps of memorised verses, and AI-driven coaching tips derived from review patterns. Audio playback with looping and segment selection. Import/export of memorisation plans. Recall testing: display Ayah/Surah, then hide for recall; voice-triggered playback comparison; scoring on accuracy, speed and recall attempts.

**User stories.**
- Users can select Quranic verses or Surahs they want to memorise.
- The platform provides flashcards with verses for review.
- An SRS algorithm schedules verses for review based on user performance.
- Users can visually track memorisation progress via a heatmap.
- Users receive AI-generated tips to improve memorisation.

**Data model.** `MemorizationItem` — `userId`, `verseKey`, `status`, plus SRS state (`interval`, `efactor`, `nextReviewDate`).

**Rationale.** Memorisation (*Hifz*) is central to Quranic education, and SRS is a proven method.

---

### Feature 4 — Gamified Learning & Competitions

**Scope.** Skill-based recitation and memorisation competitions with global and regional leaderboards, experience points, badges, streaks, and event notifications. Real-time multiplayer sessions. Replay and share options for submitted recitations. Auto-scoring via the AI classifier with a confidence percentage.

**User stories.**
- Users can participate in time-bound recitation or memorisation competitions.
- The platform displays leaderboards ranking participants by score or progress.
- Users earn XP and badges for achievements and participation.
- Competition results and rankings update in real time or near real time.

**Rationale.** Gamification is a stated strategic objective for engagement — making learning enjoyable and motivating without compromising reverence for the text.

---

### Feature 5 — Learner-Centric Learning Modules

**Scope.** Structured educational content: curated lessons (text, video, interactive elements), quizzes, personalised learning-path recommendations from an AI engine, and AI-powered explanations for selected text within lessons. Named curricula include **Noorani Qaida, Tajwīd courses, Quranic Arabic, and Tafsir**.

**User stories.**
- Learners can browse and enrol in learning modules (Tajwīd rules, Quranic Arabic, Tafsir).
- Each module contains a sequence of lessons with text, video and interactive content.
- Learners can take quizzes, receiving immediate feedback.
- The platform recommends a personalised learning path or next module based on progress and goals.
- Learners can get AI-powered explanations for selected Quranic text or concepts within lessons.

**Supporting service.** `learning-path-engine` — initially rule-based or basic collaborative filtering; inputs are user goals, progress and content metadata; output is suggested module IDs. Later enhanced with vector embeddings (MiniLM / instructor-xl) for semantic search over Quranic text, and an LLM for contextual tafsir.

**Rationale.** The core educational delivery system for self-paced learning, supporting *Learn Quran* and *Understand Quran*.

---

### Feature 6 — Educator Platform & Class Management

**Scope.** Tools for educators to create virtual classes, enrol students, assign learning modules, track student progress through analytics dashboards, and receive AI-driven suggestions for improving class engagement or addressing student difficulties. Grading and feedback, classroom announcements, assignment submission and review.

**User stories.**
- Educators can create and name virtual classes.
- Educators can enrol registered students into their classes.
- Educators can assign specific learning modules to their classes.
- Educators can view dashboards with analytics on student progress and class performance.
- Educators receive AI-generated suggestions to help students or improve teaching (e.g. *"many students struggle with Lesson X"*).

**Rationale.** Essential to the *Teach Quran* goal, and the bridge from self-paced to guided learning.

---

### Feature 7 — Community Engagement Platform · ⛔ A.9.6 — no AI Ask-a-Scholar; a scholar answers or nobody does

**Scope.** Forums, Q&A boards, event management (online and offline), specialised interaction rooms — **study circles, recitation rooms** — "Ask a Scholar" functionality, content liking/sharing, and AI-powered content moderation.

**User stories.**
- Users can create and participate in forum discussions.
- Users can ask questions and provide answers in a dedicated Q&A section.
- Community events can be created, discovered, and RSVP'd.
- AI moderates user-generated content to maintain a respectful environment.
- Users can join specialised rooms for focused interaction.

**Moderation.** Google Perspective API for text moderation, with `isApproved` gating on posts and comments.

**Rationale.** Fulfils the *Connected Global Communities* objective and the "Muslim social media platform" framing.

---

### Feature 8 — Video Conferencing & Collaboration

**Scope.** Real-time video for teaching, group study and community events: HD 1:1 and group video, screen sharing, collaborative whiteboard, session recording, **live AI-powered transcription**, and in-session text chat. Breakout rooms appear in the earlier feature lists. Session scheduling and management.

**User stories.**
- Users can initiate or join 1:1 or group video calls.
- During a call, users can share their screen.
- A collaborative whiteboard allows participants to draw and annotate together.
- Video sessions can be recorded for later review.
- Live AI-powered transcription provides subtitles or a transcript.
- Participants can communicate via text chat within the session.

**Rationale.** Synchronous interaction is essential for live teaching, tutoring and interactive community events.

---

### Feature 9 — Immersive AR/VR Experiences

**Scope.** AR overlays for Tajwīd visualisation (3D mouth shapes, articulation points), VR walkthroughs of Quranic historical sites, virtual mosque experiences, virtual classrooms, and **3D memory palaces**. Delivered via web-based technologies (WebXR) for broad access, with a 3D asset pipeline (Blender, Unity/Unreal for prototyping).

**User stories.**
- Users can experience AR overlays visualising correct mouth movements for Tajwīd while reciting.
- Users can take VR tours of Quranic historical sites or explore a virtual mosque.
- AR/VR experiences are accessible via web-based technologies (WebXR).

**Rationale.** Directly addresses the *Immersive Education Tools* objective — making learning tangible.

---

### Feature 10 — AI Guidance & Fitrah Profiling System · ⛔ A.9.5 — the Fitrah Spectrum is never a measurement; A.12.3/A.12.4 rulings pending

**Scope.** The most distinctive feature in the vision. A sophisticated AI system providing personalised ethical, spiritual and personal-growth guidance:

- **Conversational AI** for Quranic Q&A and contextual help (GPT-4o, Falcon-Arabic, Llama 3.1).
- **Fitrah Profiling** — a psychometric assessment grounded in Islamic virtues, producing a **99-aspect "Fitrah Spectrum"**, which the AI uses to tailor its guidance.
- **Voice UI control** via a Hugging Face "Open Computer" agent, enabling hands-free interaction and navigation.
- **The Guidance Avatar** — an on-screen agent whose appearance and responses shift with the user's detected emotional state.

**User stories.**
- Users can ask Quranic or Islamic questions and receive contextual answers from an AI.
- The platform offers personalised spiritual and ethical guidance based on interactions and Fitrah profile.
- Users can complete a "Fitrah Spectrum" assessment to understand their innate virtues.
- Users can interact with the platform using voice commands for hands-free navigation and feature access.
- The AI Guidance Avatar can reflect the user's emotional state and deliver optimised insights.

**Rationale.** This is the "Neural Core" of the platform — the unique value proposition. Deeply personalised, context-aware, ethically grounded guidance. See [Part IV](#part-iv--the-intelligence-layer).

---

### Feature 11 — Swarm Intelligence & Collaborative Learning

**Scope.** AI algorithms — **Ant Colony Optimization** is the named approach — analysing collective user behaviour and data patterns to optimise group learning suggestions, recommend content based on successful pathways taken by similar users, and identify common areas of difficulty across the user base. Relies on an event-driven architecture (Kafka) processing real-time data. The related concept of an **AI swarm of multiple collaborating agents providing diverse perspectives on complex spiritual questions** appears in the Personalized Guidance source.

**User stories.**
- The platform identifies common learning challenges or successful learning patterns from aggregated user data.
- Users may receive suggestions for group study or collaborative tasks based on swarm insights.
- Learning path recommendations (Feature 5) are enhanced by swarm intelligence data.

**Rationale.** Leverages collective intelligence to improve outcomes for individuals and groups — a distinct AI-driven objective, not merely a recommender.

---

### Feature 12 — Adaptive UI/UX Engine · ⛔ A.9.4 — no emotion inference

**Scope.** The interface adapts dynamically to the individual, based on profile (age, role, skill level), stated preferences (learning style, theme), and **real-time emotional state detected via AI**.

**User stories.**
- The platform's layout and content density adjust based on the user's age group or skill level.
- Font sizes and themes adapt to user preferences or accessibility needs.
- Navigation flows may be simplified or expanded based on user role or cognitive preferences.
- The AI Guidance Assistant and UI notifications adapt their tone based on detected emotional state — encouraging messages if frustration is detected, a calmer palette if agitation is detected.

**Rationale.** Crucial to a truly personalised and emotionally responsive learning environment.

---

### Feature 13 — Platform Settings, Globalization & Accessibility

**Scope.** Language selection with full i18n including RTL (Arabic, Urdu, Bahasa, French, Spanish); theme preferences (**dark, light, Islamic**); notification controls; privacy settings; accessibility options (font size, high contrast); **PWA offline access** to core content with background sync; and **digital certifications** for completed modules and courses.

**User stories.**
- Users can select their preferred language for the platform interface.
- The platform supports Right-to-Left languages like Arabic and Urdu.
- Users can choose display themes (light, dark, Islamic).
- Users can manage notification preferences and privacy settings.
- Accessibility options like adjustable font sizes and high-contrast mode are available.
- Core content can be accessed offline via PWA functionality.
- Users can receive digital certifications for completing courses/modules.

**Standard.** WCAG 2.2 AA compliance (some earlier sources say 2.1 AA — see [§28](#28-contradictions-and-open-decisions)).

**Rationale.** Essential for user empowerment, inclusivity, and the Universal Accessibility objective.

---

### Feature 14 — Secure Billing, Subscriptions & Donations

**Scope.** All financial transactions handled securely and in a Sharia-compliant manner: freemium and paid subscription tiers via Stripe; institutional billing; **dynamic pricing at cost + 5% for institutions**; Zakat-eligible donation processing; a transparent donor dashboard; and **"Sponsor-a-Student"**.

**User stories.**
- Users can subscribe to freemium or paid tiers with varying feature access.
- Institutions can be billed based on seats or usage, with ethical pricing.
- Users can make Zakat-eligible donations securely.
- A public donor dashboard shows how funds are allocated and platform impact.
- Users may have an option to "Sponsor-a-Student".

**Sharia constraints in the data model.** `SubscriptionPlan` carries `complianceTags` (e.g. `['noRiba']`); `DonationFund` carries `isZakatEligible`. Pricing logic is explicitly required to avoid *riba*.

**Rationale.** Ensures financial sustainability and ethical operation, aligned with the trust-based model.

---

### Feature 15 — Admin, Analytics & Platform Governance

**Scope.** Admin console for user management, content moderation and platform settings. Analytics and reports for every role — learners, teachers, admins, and **parents via a Parental Insights Dashboard**. Security configuration, audit logging, and the framework for GDPR and Sharia compliance. Institutional analytics and LTI 1.3 integration for embedding in external LMS platforms.

**User stories.**
- Admins can manage user accounts (view, update roles, ban).
- Admins can moderate user-generated content (approve/reject).
- Admins can configure platform-wide settings.
- Admins and teachers can view analytics dashboards on user engagement, learning progress and AI usage.
- Parents can view an insights dashboard for their child's progress.
- The platform adheres to GDPR and Sharia compliance principles.

**Parental controls, specifically.** Summary of the child's recitation progress, scores and time spent; parental control of UI themes and session-duration limits; optional weekly/monthly email digest of the child's activity.

**Rationale.** Necessary for platform health, security, compliance, and actionable insight for all stakeholders.

---

### The Shared Area

Not a feature but a first-class architectural concern: common utilities, services, UI components, configurations and type definitions used by multiple features, to promote reuse and consistency.

Contents: the UI component library (React + Tailwind, documented in Storybook); auth/authz utilities (JWT handlers, RBAC middleware, `ProtectedRoute`, OAuth clients); API client services (Axios instance with interceptors for error handling and token refresh); notification utilities; database/ORM utilities; the i18n core; a logging service; constants and enums; shared TypeScript definitions and DTOs; validation schemas; **core AI service clients/wrappers** standardising access to the AI microservices; PWA and offline utilities (service-worker registration, IndexedDB helpers, sync logic); accessibility utilities; and shared build/config scripts.

---

# Part IV — The Intelligence Layer

This is the part of the vision that makes QEP distinctive, and the part no attempt reached.

## 11. Phase 14 — the Neural Core · ⛔ A.9.1 / A.9.4 — its recitation-analysis and emotion services are forbidden capabilities

**Goal (verbatim):** *"Central orchestrator for AI-driven feedback & recommendation. Unify AI Agents, emotion AI, Swarm routing, and hands-free Avatar UI as the platform's neural core."*

Described in the sources as the **"Central Nervous System of the Platform"**. Its components:

### 11.1 The four AI microservices

| Service | Runtime | Responsibility |
|---|---|---|
| `recitation-analysis` | Python/FastAPI | Enhanced Tajwīd logic with advanced phonetic models |
| `llm-nlp` | Python/FastAPI | Falcon-Arabic & Llama 3.1 for Quranic QA, contextual understanding, personalised learning suggestions |
| `guidance-assistant` | Node/Express or Python/FastAPI | Google STT/TTS wrapper; Affectiva emotion detection from voice/text; the "Open Computer" agent for hands-free UI control |
| `aco-optimizer` | Python | Kafka consumer implementing Ant Colony Optimization over system metrics and user interaction data |

### 11.2 The event bus

Apache Kafka as event-driven middleware. Named topics from the design:

- `recitation_audio_stream`
- `user_commands_voice`
- `emotion_data_stream`
- `llm_processing_queue`
- `swarm_optimization_input`
- `personalized_feedback_stream`

Producers and consumers in the NestJS backend (`kafkajs`) and the Python services (`kafka-python`).

### 11.3 The Guidance Avatar

`GuidanceAvatar.tsx` is the user-facing surface of the Neural Core:

- **Voice interaction** — Google STT for input, TTS for output.
- **Emotion display** — the avatar's appearance and responses shift subtly based on Affectiva emotion data.
- **Hands-free navigation** — interprets commands via the "Open Computer" agent (*"Go to dashboard"*, *"Switch to dark mode"*, *"Increase font size"*) and executes them against the router or settings context.
- **Personalized feedback display** — surfaces insights from the LLMs and from swarm intelligence.

Attempt 3's Phase 14 restatement adds **Ready Player Me** as a candidate avatar system, with a 2D animated avatar as the lean fallback.

### 11.4 Data layer

- **MySQL** (RDS free tier) — structured: users, learning progress.
- **MongoDB** (Atlas M0) — unstructured: AI model outputs, logs, community content.
- **Redis** — caching, session management, message queuing.

## 12. The Fitrah Spectrum · ⛔ A.9.5 — never a psychometric measurement; the 99 aspects were never enumerated

Phase 16. The vision's most original idea, and the least specified.

**The concept.** A **99-aspect psychometric profile** — the "Fitrah Spectrum" — built from a series of questions and interactive scenarios that surface a user's values, inclinations, strengths and areas for growth, aligned with Islamic ethical concepts (patience, gratitude, honesty, and so on).

**The mapping.** A custom ML model maps Fitrah profile aspects onto the **Divine Attributes (Asmāʾ al-Ḥusnā)** and onto Quranic themes. The 99 aspects correspond to the ninety-nine Names.

**The chain.** The design states the inference chain explicitly: **Ayah → Attribute → User state**, producing contextual insight.

**The bot.** A GPT-4o-powered personalised ethical guidance bot takes three inputs — the **Fitrah profile**, the **current emotional state** (from Affectiva, via Phase 14), and the **user's query** — and suggests relevant Ayahs, Hadith, Duas and actionable advice for spiritual growth, character development and relationship enhancement.

**Retrieval.** Vector databases (Pinecone/Weaviate free tier, or FAISS) for semantic search over Quranic and Hadith content.

**Status:** conceptual throughout. No attempt produced the 99 aspects, the assessment instrument, the mapping model, or the curated corpus. This is the single largest specification gap in the vision.

## 13. Swarm intelligence

Two distinct ideas travel under this name in the sources, and they should be kept separate:

**13.1 Swarm as collective-behaviour optimisation (Phase 14, `aco-optimizer`).** Ant Colony Optimization consuming Kafka streams of system metrics and user interaction data, to triage learning priorities, identify optimal learning paths, and recommend content based on pathways that succeeded for similar users. This is a **population-level analytics engine**.

**13.2 Swarm as multi-agent deliberation (Personalized Guidance source).** *"Multiple AI agents collaborate, providing diverse perspectives on complex spiritual/personal issues."* This is an **ensemble-of-advisors** pattern — closer to modern multi-agent orchestration than to ACO.

The plan folds both into Phase 14 without reconciling them. Any future build should decide which it is building, or build both under separate names.

## 14. The Adaptive UI/UX engine · ⛔ A.9.4 — the emotion-based axis is forbidden

Phase 15. Three adaptation axes:

**Profile-based.** Dynamic layouts and content presentation tailored by age group (children/teens/adults), role (learner/teacher/parent/admin), and skill level (beginner/intermediate/advanced, from profile or AI assessment). Cognitive-preference adjustments — more visual aids for visual learners.

**Emotion-based** (integrates with Phase 14). UI elements and AI responses adapt to the user's emotional state as detected by Affectiva.

**Device-adaptive.** Fully responsive for mobile (PWA on iOS/Android), tablet, desktop, plus basic AR/VR headset considerations — larger text, simpler navigation for pass-through AR or basic VR views.

Delivered alongside WCAG 2.2 AA compliance, aggressive PWA caching with background sync of offline actions, full i18n/RTL, and **GraphQL subscriptions** (Apollo Server + Client) for real-time UI updates such as live leaderboards and notifications.

## 15. The Personalized Guidance application

A separate application concept, documented in `Personalized Guidance and Learning Application 111224.txt`, that the plan formally folds into QEP at Phase 16 and Phase 14. It is worth preserving in its own right because it defines the *content* of guidance, which nothing else in the corpus does.

**Concept.** A platform integrating AI, ML, AI agents and AI swarm technology to provide deeply personalised spiritual, emotional and personal-growth guidance, rooted in Islamic teachings, designed to align users' lives with the pleasure of Allah — focusing on spiritual development, character building, and relationship enhancement.

### Its four content pillars

| Pillar | Arabic framing | Content |
|---|---|---|
| **Spiritual Development** | *Worship* | Personalised prayer reminders; contextual dua suggestions; AI-suggested daily Quranic reflections based on emotional/spiritual state |
| **Character Development** | *Ikhlāq* | Personalised advice on virtues; AI analysis of actions for moral and ethical growth |
| **Acts of Worship** | *Aʿmāl* | Tracking of obligatory and voluntary deeds, with AI suggestions |
| **Rights & Relationships** | *Ḥaq / Ḥuqūq* | Guidance on strengthening bonds with family, friends and community per Islamic teachings; AI conflict-resolution tools offering advice grounded in Islamic values |

### Its distinguishing technical ideas

- **Reinforcement learning** so guidance adapts over time, not just personalises once.
- **AI agents for task automation** — prayer reminders, dua recommendation by emotional need, memorisation guidance.
- **Real-time context from wearables and smartphones** — physical activity, health metrics, location, weather — producing context-aware recommendations (the worked example in the source: *a dua for stress suggested when elevated heart rate is detected*). Flagged as post-v1.0, but it is the sharpest expression of what "context-aware" was meant to mean.

### Its UI/UX philosophy

**Minimalist and serene.** Neutral tones, subtle Islamic patterns, elegant Arabic calligraphy, soft animations — deliberately chosen to evoke calm and focus. The instruction is that this philosophy should govern the design system built in Phase 2 and the adaptive UI refined in Phase 15, i.e. it is the aesthetic direction for the whole platform, not just the guidance module.

---

# Part V — Architecture & Technology

> **⚠ SUPERSEDED — read as history, not as a plan.** Everything in Part V reflects mid-2025 availability
> and was compiled by the Jules agent, not authored by the Owner. Model rosters, speech and emotion SDKs,
> event-bus and database selections, hosting and free-tier strategies, and the vendor-ecosystem mapping are
> all dated. Workstation supplies every one of these from its own native fabric — see
> `WORKSTATION_IDBO_WHOLE_VISION.md` §6, §7 and **Appendix A.10**, which excludes this Part from the
> canon-resident QEP vision. It is retained here because it is part of the historical record of what those
> repositories contained, and because the *capabilities* named beneath the technology remain valid.

## 16. System architecture

A **monorepo housing a microservices-oriented, event-driven architecture**.

```
                       ┌─────────────────────────────┐
                       │   React Frontend (Vite/Next)│
                       │   + GuidanceAvatar + PWA    │
                       └──────────────┬──────────────┘
                                      │ REST / GraphQL / WebSocket
                       ┌──────────────▼──────────────┐
                       │  NestJS Backend Gateway     │
                       │  auth · billing · learning  │
                       │  teaching · community · …   │
                       └───┬──────────┬──────────┬───┘
                           │          │          │
              ┌────────────▼──┐  ┌────▼─────┐  ┌─▼──────────────┐
              │ recitation-   │  │ llm-nlp  │  │ guidance-      │
              │ analysis (Py) │  │   (Py)   │  │ assistant      │
              └───────┬───────┘  └────┬─────┘  └───────┬────────┘
                      │               │                │
                 ═════╪═══════════════╪════════════════╪═════  Apache Kafka
                      │               │                │
                 ┌────▼───────────────▼────────────────▼────┐
                 │        aco-optimizer (Python, swarm)     │
                 └──────────────────────────────────────────┘

   Data:  MySQL (structured) · MongoDB (unstructured) · Redis (cache/session/queue)
```

**Components:**

- A **React frontend** (Vite or Next.js) providing the UI.
- A **NestJS backend gateway** as primary API orchestrator and home of core business logic.
- **Specialised microservices** for computationally intensive or distinct tasks: recitation analysis (Python/FastAPI), LLM/NLP (Python/FastAPI), guidance assistant (Node or Python — STT/TTS, emotion detection, Open Computer agent), video conferencing (Node/Express), and ACO/swarm (Python).
- **Apache Kafka** for asynchronous inter-service communication, supporting real-time features and swarm intelligence.
- **Polyglot persistence** — MySQL for structured relational data, MongoDB for flexible-schema data, Redis for caching, sessions and real-time queues.

## 17. Technology stack — three tiers

The sources contain three *different* stacks, and confusing them is a real hazard. They are not versions of one another; they are the same design at three ambition levels.

### Tier 1 — The ambitious stack (V1.1 sources)

- **Frontend:** React.js, Next.js, TypeScript, Redux, React Context API, React Hook Form, Material UI, Tailwind CSS, WebRTC, WebSocket, Three.js, A-Frame, Axios, D3.js, Google Maps API (optional)
- **Backend:** Node.js, Express.js, TypeScript, MongoDB, PostgreSQL, Redis, GraphQL, Apollo Server, JWT, Passport.js, Stripe, Multer, Socket.io, AWS S3, Nodemailer
- **AI & ML:** TensorFlow.js, HuggingFace Transformers, Deepgram, Google Speech-to-Text, PyTorch, spaCy, NLTK, FastText
- **Cloud & Deployment:** Docker, Kubernetes, Nginx, AWS, Azure, GCP, CI/CD (GitHub Actions, Jenkins), Terraform, Prometheus, Grafana
- **Security:** OAuth 2.0, 2FA, Helmet.js
- **Monitoring:** Sentry, Prometheus, Grafana

### Tier 2 — The free-tier stack (the operative plan)

This is the stack the 19-phase roadmap actually assumes, chosen explicitly to keep the platform buildable at near-zero cost.

| Layer | Choice | Free-tier strategy |
|---|---|---|
| Monorepo | Yarn Workspaces or Nx | — |
| Frontend | React + Vite, Tailwind, `react-i18next`, Redux Toolkit / Context, React Query, Three.js/A-Frame, D3.js/Recharts, Storybook | Vercel / Netlify / Firebase Hosting |
| Backend gateway | Node.js + TypeScript + **NestJS** | Google Cloud Run / AWS EC2 t2.micro / Heroku |
| Microservices | **Python + FastAPI** (preferred for AI), or Node/Express | Same |
| Relational DB | **MySQL** | AWS RDS free tier or local Docker |
| Document DB | **MongoDB** | Atlas M0 free tier or local Docker |
| Cache/Queue | **Redis** | Docker on EC2 free tier |
| Event bus | **Apache Kafka** | Self-hosted on EC2 free tier / `bitnami/kafka` in Docker |
| LLMs | **Falcon-Arabic, Llama 3.1** | Hugging Face Inference API free/community tier |
| Advanced LLM | **GPT-4o** (guidance bot) | API, where free/trial allows |
| Speech | Google Cloud STT/TTS; Hugging Face **Whisper** (Arabic fine-tune) | Trial/free tiers |
| Emotion | **Affectiva SDK** | Open-source version or trial |
| Swarm | Ant Colony Optimization (Python library) | — |
| Vector search | Pinecone / Weaviate free tier, or **FAISS** | — |
| Auth | NestJS custom — JWT, Passport.js, bcrypt, **Speakeasy** (TOTP); Firebase Auth for OAuth | Firebase free tier |
| Payments | **Stripe SDK** | Developer mode / test keys |
| Storage | Firebase Storage | Free tier — audio, media, AR/VR assets |
| Moderation | Google **Perspective API** | Free/trial |
| Monitoring | Prometheus, Grafana, ELK or Loki, **Sentry** | Self-hosted / free tier |
| CI/CD | GitHub Actions | Free tier |
| IaC | Terraform | Optional |

### Tier 3 — "Magnificent 7" integration (aspirational)

A conceptual mapping of platform capability onto big-tech ecosystems. Explicitly noted in the sources as *"more high-level ideas than concrete stack choices"* — recorded here for completeness, not as a plan.

| Vendor | Named technologies |
|---|---|
| **Microsoft** | LinkedIn, Teams, Yammer, Azure AI, PlayFab, Mesh, Teams VC, Power BI, OpenAI Service |
| **Amazon** | Polly, SageMaker, Lex, AWS GameTech, Cognito, Lambda |
| **Google** | Gemini, BERT, Dialogflow, Vertex AI, Firebase, Looker Studio |
| **Meta** | Facebook, Instagram, hardware, Messenger, Meta Avatars, Quest Pro |
| **Apple** | Vision Pro, ARKit 5 |
| **NVIDIA** | NeMo, TensorRT, Morpheus |
| **SpaceX** | **Starlink** — the underserved-region access objective |
| **Tesla** | Dojo Pods |

## 18. Repository structure

The canonical monorepo layout, from the Developer Guide:

```
/ (Root)
├── agents/                  # AI agent prompts, configs, logic
│   ├── prompts/
│   └── configs/
├── backend/                 # NestJS gateway + core business logic
│   └── src/
├── frontend/                # React/Vite application
│   └── src/
├── services/                # Specialised microservices
│   ├── recitation-analysis/
│   ├── llm-nlp/
│   ├── guidance-assistant/
│   └── aco-optimizer/
├── shared/                  # Common libs, TS types/interfaces, DTOs, UI
│   └── ui/
├── infra/                   # Docker, Kafka, Terraform
│   ├── docker/
│   ├── kafka/
│   └── terraform/
├── docs/                    # Core documentation
│   ├── consolidated_source_material.md
│   ├── core_features_definition.md
│   └── phase-guides/phases1-19.md
├── planning/                # Worklogs, proposals, archive
├── scripts/                 # Utility, automation, build scripts
├── sources/                 # Original .txt source material
├── .github/workflows/       # CI/CD
├── .env.example
├── package.json
└── tsconfig.base.json
```

Frontend internals follow a feature-first layout: `/src/features/{auth,recitation,memorization,competitions,learning,teaching,community,billing,donations,fitrah,ai-core}`, with `/src/components`, `/src/contexts`, `/src/services`, `/src/hooks`, `/src/utils`, and `/src/assets/styles` (including a named `islamicAesthetics.css`).

---

# Part VI — Roadmap

> **⚠ SUPERSEDED — read as history, not as a plan.** The 19-phase roadmap was Jules-authored and disagrees
> with itself across the three attempts — the last generation silently deleted Fitrah profiling,
> institutional onboarding and the ethical finance model from phases 16–18 and presented it as a revision
> (§21). Workstation's delivery order comes from `FABLE_DELIVERY_PROMPT.md` and its fidelity ledger, not
> from this list. Excluded from the canon by **Appendix A.10**; retained here as the historical record and
> because §20's Phase→Feature mapping is still a useful cross-check on feature coverage.

## 19. The 19-phase roadmap

Twenty stages: Step 0 plus Phases 1–19. Each is specified with Goal, Core Components, Tech Stack, Dependencies, Outcome, Next Steps, and an Effort/Impact rating.

### Step 0 — Foundation Setup & MVP Audit
*Effort: Low · Impact: High*
Establish a zero-waste, high-velocity monorepo with governance. Audit `quran-recitation-mvp` to identify reusable assets (recitation analysis, video conferencing), understand its stack, and set an integration baseline. Enforce ESLint, Prettier, TypeScript, Husky. Add `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, README. Security and compliance gap analysis; basic load tests; baseline performance metrics.

### Phase 1 — Core Scaffolding & Monorepo Structure
*Effort: Low · Impact: High*
Deployable shell with placeholder UI. Initialise React/TS frontend, NestJS backend, microservice directories. Tailwind + global CSS variables. Dockerfile per service; root `docker-compose.yml` bringing up frontend, backend, services, MySQL, Redis, Kafka, MongoDB. Initial GitHub Actions CI for lint, type-check, placeholder tests. Stub `docs/STRUCTURE.md`, `docs/system-architecture.md`, `docs/data-flow.md`.
**Outcome:** `yarn install && docker-compose up --build` starts the whole local stack.

### Phase 2 — Advanced Authentication & User Profiling
*Effort: Medium · Impact: Critical*
User model with roles (learner, teacher, admin, parent), `mfaSecret`, `isMfaEnabled`, profile fields. AuthService: JWT access + refresh, bcrypt, OAuth (Google via Firebase or Passport), MFA via Speakeasy TOTP. `RolesGuard` and `@Roles()` decorator. Frontend AuthContext, signup/login/reset/MFA forms, `ProtectedRoute`, Axios refresh interceptor. **Shared UI library initiated** — Button, Input, Modal, Grid; design tokens; Storybook.

### Phase 3 — Secure & Compliant Billing, Subscriptions & Donations
*Effort: Medium · Impact: Medium*
Models: `SubscriptionPlan` (with `complianceTags` e.g. `noRiba`), `UserSubscription`, `DonationFund` (with `isZakatEligible`), `Donation`. Dynamic pricing (usage cost + 5%, riba-free), subscription lifecycle, Stripe wrapper with webhooks (`invoice.payment_succeeded`, `customer.subscription.updated`), refunds. Frontend: plans page, Stripe payment form, billing dashboard, donation page, impact-report stub.

### Phase 4 — AI Tajwīd Coach (MVP Recitation Analysis Integration)
*Effort: High · Impact: Critical*
`recitation-analysis` microservice with `POST /analyze`. Refactor the MVP's analysis algorithms; augment with fine-tuned Arabic Whisper via HF Inference API; apply rule-based Tajwīd logic (Madd, Ghunnah, …). Output structured JSON. Backend `RecitationSession` model, audio upload to Firebase Storage. Frontend `AudioRecorder` (Web Audio API / MediaRecorder), submission page with waveform and phoneme visualisation, feedback display with error highlighting.

### Phase 5 — Gamified Competitions & Leaderboards
*Effort: Medium · Impact: High*
`Competition` and `CompetitionEntry` models. Competition CRUD (admin), joining, submission scored via Phase 4, leaderboard generation. Socket.IO gateway for real-time leaderboard updates and event notifications. XP/rank/badge engine backed by Redis. Detailed recitation logs to MongoDB. Frontend list/detail pages, `LeaderboardDisplay` with D3.js.

### Phase 6 — Memorization Suite (SRS, Heatmaps, AI Coaching) + PWA/RTL foundations
*Effort: Medium · Impact: High*
`MemorizationItem` with SRS state. `SpacedRepetitionService` implementing **SM-2**. Add-verse, review-queue, record-attempt, stats and heatmap endpoints. Frontend verse selection, flashcard, review session, dashboard, `MemoryHeatmap` (D3.js). Also: dark-mode toggle with persistence, PWA manifest + Workbox service worker for offline caching of Quran text and core UI, RTL support.

### Phase 7 — Learn-Teach Modules, Learner-Centric Content Delivery
*Effort: High · Impact: High*
`LearningModule`, `Lesson` (text/video/quiz), `Quiz`, `UserProgress`. Seed initial content. `learning-path-engine` microservice with `POST /recommend-path`. Frontend modules browser highlighting the recommended path, module view, lesson viewer, quiz player, learning dashboard. LLM integration for on-demand explanation of lesson text.

### Phase 8 — Educator Toolkit & Class Management
*Effort: Medium · Impact: High*
`Class` model (teacherId, students, assigned modules, VC link stub). `TeachingService`: create class, enrol student, assign module, teacher dashboard data, class details, per-student progress, class analytics, **AI suggestions for educators**. Role-protected APIs. Frontend teacher dashboard, class management page, student progress view.

### Phase 9 — Community Engagement Platform (Forums, Q&A, Events)
*Effort: Medium · Impact: Medium*
MongoDB-backed `CommunityPost` (unified type: forum / Q&A / event suggestion / study circle), `Comment`, `ScheduledCommunityEvent` with RSVPs. `AIContentModerationService` via Google Perspective API. Frontend forum, thread view, Q&A, event calendar, plus specialised `StudyCirclePage`, `RecitationRoomPage`, `AskScholarPage`.

### Phase 10 — Video Conferencing & Collaborative Tools
*Effort: Medium · Impact: High*
WebRTC 1:1 and group sessions with scheduling. In-session chat. Screen sharing. Socket-based collaborative whiteboard (`react-konva`). Session recording. **MongoDB** for `VideoSession` and `Message` models. Live AI transcription. Jitsi Meet self-hosted or a managed free tier as the signalling/media option.

### Phase 11 — Immersive Experiences: Foundational AR/VR & Asset Pipeline
*Effort: Medium · Impact: Medium*
3D asset pipeline (Blender; Unity/Unreal for prototyping). Basic AR prototype displaying Quranic verses (AR.js or native AR kits). Exploratory VR environment — a simple mosque interior or focused study room. WebXR research for broad access. AR Tajwīd overlay prototype via 8thWall / Zappar / WebXR. Documented AR/VR integration strategy.

### Phase 12 — Globalization, Settings, Offline PWA & RTL Support
*Effort: Medium · Impact: High*
`react-i18next` integration; translation of core UI and initial content (English, Arabic, Urdu). PWA service worker for offline caching; web app manifest. User settings panel — language, theme, notifications, PWA install. CDN considerations (Cloudflare free tier).

### Phase 13 — Admin Console, Advanced Security & Compliance
*Effort: Medium · Impact: High*
Admin dashboard: user management, content oversight, analytics. Security hardening — WAF (Cloudflare free tier), API rate limiting, Helmet.js. Audit trail for critical actions. Backup and recovery strategy. GDPR/COPPA compliance features including data export and deletion. SAST in CI (SonarQube CE / Snyk free tier).

### Phase 14 — **Neural Core: AI Agents & Swarm Intelligence Hub**
*Effort: High · Impact: **Transformational***
See [§11](#11-phase-14--the-neural-core). The four AI microservices, the Kafka event bus, the Guidance Avatar with voice and emotion, and the ACO swarm stub.

### Phase 15 — Universal Accessibility (WCAG 2.2) & Adaptive UI/UX Engine
*Effort: High · Impact: Critical*
See [§14](#14-the-adaptive-uiux-engine). WCAG 2.2 AA audit and remediation (ARIA, keyboard navigation, screen readers, contrast, focus indicators; `axe-core` + Lighthouse). Aggressive PWA caching with background sync. Full i18n/RTL across all supported languages. The three-axis adaptive engine. Initial GraphQL subscriptions via Apollo.

### Phase 16 — Fitrah Profiling & Personalized Guidance Bot
*Effort: High · Impact: **Transformational***
See [§12](#12-the-fitrah-spectrum). The 99-aspect Fitrah Spectrum assessment and visualisation; the ML mapping to Divine Attributes; the GPT-4o guidance bot conditioned on profile + emotion + query; the four guidance pillars; vector search over Quran/Hadith. Bundled with comprehensive testing and a *"Strategic Blueprint Evaluation"* — a report assessing current status against the vision.

### Phase 17 — Institutional Onboarding & Analytics Dashboards
*Effort: Medium · Impact: High*
`Institution` model with admins, teachers and student-count limits. **CSV bulk onboarding** of students and teachers with validation, account creation, invites. Enhanced teacher dashboards (lesson completion, quiz scores, recitation activity, time per module) and institutional admin dashboards (aggregate analytics, recitation quality trends, content popularity). Recharts/D3 visualisation. **Basic LTI 1.3 provider** — authentication handshake and grade passback — so QEP can embed in existing LMS platforms.

### Phase 18 — Monetization, Donation Model & Financial Transparency
*Effort: Medium · Impact: Medium*
Institutional subscription plans by student/teacher count and feature tier, linked to `Institution`. **Transparent donor dashboard** — aggregated, anonymised data on how donations are used (server costs, feature development, content creation, sponsored seats) with impact metrics. Zakat-eligible fund marking with Zakat guidance. **Sponsor-a-Student** allocation mechanism. Documented **cost-price + 5% operational cap** and audit/reporting processes aligned to the Waqf trust model.

### Phase 19 — Continuous Monitoring, QA, Support & v1.0 Launch
*Effort: Medium · Impact: Critical*
APM (New Relic/Datadog free tier, or Prometheus + Grafana) across backend, frontend and AI services. Centralised structured JSON logging to ELK or Cloud Logging. Database monitoring. Web Vitals tracking and Lighthouse CI. User-behaviour analytics. Sentry with source maps. Bug triage and hotfix workflow. Playwright E2E + Jest/Pytest in CI. In-app feedback, NPS surveys, support knowledge base. `docs/release-notes.md`, SLAs, and v2.0 planning.

## 20. Phase-to-feature mapping

The authoritative mapping from the Developer Guide §0.6:

| Phase | Title | Core Feature(s) | Note |
|---|---|---|---|
| Step 0 | Foundation Setup, Audit & LEAN Prep | Core-Infra | Foundational setup |
| 1 | Monorepo, Core Services & CI/CD Foundation | Core-Infra | Technical backbone |
| 2 | Advanced Authentication & User Profiling | 1, 12 | Initial preferences feed adaptive UI |
| 3 | Secure Billing, Subscriptions & Donations | 14 | |
| 4 | AI Tajwīd Coach (MVP integration) | 2 | |
| 5 | Gamified Recitation Competitions & Leaderboards | 4, 7 | Leaderboards are a community aspect |
| 6 | Memorization Suite (SRS, Heatmaps, AI Coaching) | 3, 10 | AI coaching belongs to the guidance system |
| 7 | Personalized Learning Modules (Learner Focus) | 5, 10 | AI recommendation and explanation |
| 8 | Educator Toolkit & Class Management | 6, 15, 10 | Educator analytics are governance; AI aids teachers |
| 9 | Community Engagement Platform | 7, 10 | AI moderation is a guidance function |
| 10 | Video Conferencing & Collaborative Tools | 8, 10 | AI transcription enhances collaboration |
| 11 | Immersive Learning Experiences (AR/VR) | 9 | |
| 12 | Settings, Customization & Globalization | 13, 12 | Settings drive the adaptive UI |
| 13 | Admin Console, Security Hardening & Compliance | 15 | |
| 14 | **Neural Core — AI Agents, Swarm & Avatar** | **10, 11, 12, 9** | Core AI features integrated |
| 15 | Universal Accessibility, PWA Offline & Adaptive UI/UX | 13, 12 | Adaptive UI fully realised |
| 16 | Fitrah Profiling, Guidance Bot & GraphQL Subscriptions | 10, 12, 5, Core-Infra | Fitrah guides learning and UI |
| 17 | Institutional Onboarding & Advanced Analytics | 15, 1, 6 | Admin, user import, educator tools |
| 18 | Monetization Refinement & Ethical Finance | 14 | |
| 19 | Production Deployment, Monitoring, QA & Support | 15, Core-Infra | |

Feature **10 (AI Guidance)** appears in seven phases — more than any other. It is not a module; it is a cross-cutting capability.

## 21. The competing Phase 15–19 orderings

Two incompatible orderings of the final phases exist, and this is the most consequential unresolved decision in the corpus.

| Phase | **Ordering A** — consolidated guide (Attempt 2) | **Ordering B** — QEP-MVP guide (Attempt 3) |
|---|---|---|
| 14 | Neural Core: AI Agents & Swarm Intelligence Hub | Core Intelligence Hub & Avatar Integration |
| 15 | Universal Accessibility & Adaptive UI/UX Engine | Universal Accessibility & Adaptive UI/UX Engine |
| 16 | **Fitrah Profiling & Personalized Guidance Bot** | Comprehensive Testing & QA |
| 17 | **Institutional Onboarding & Analytics Dashboards** | Production Deployment, CI/CD & Free-Tier Optimization |
| 18 | **Monetization, Donation Model & Financial Transparency** | Full Documentation & Support Infrastructure |
| 19 | Continuous Monitoring, QA, Support & v1.0 Launch | Continuous Monitoring, Feedback Loops & v1.0 Launch |

**Ordering A treats Fitrah profiling, institutional onboarding and the ethical finance model as product.** **Ordering B drops all three** and spends 16–18 on testing, deployment and documentation.

Ordering B is chronologically later (Attempt 3, June 2025) but is strictly a *reduction*: it deletes the Fitrah Spectrum — the platform's most distinctive idea — the institutional go-to-market, and the transparent donation model that the governance section depends on. Ordering B also downgrades Phase 14 from "Neural Core with Kafka, swarm, emotion and voice" to "AI orchestration service with a basic avatar and a placeholder for adaptive learning".

**Assessment:** Ordering B looks like scope compression under delivery pressure, not a considered revision. **Ordering A is the vision; Ordering B is a retreat from it.** A fourth attempt should adopt Ordering A and treat testing, deployment and documentation as continuous obligations under the LEAN rules rather than as terminal phases.

---

# Part VII — Governance, Ethics & Finance

## 22. Governance model

**Overview.** Democratise Quranic learning worldwide through an AI-driven, Sharia-compliant **trust–waqf** platform.

**The organising image.** The structure mirrors an **eight-pointed star of Divine Attributes** — Majesty, Beauty, Knowledge, Creation, Justice, Forgiveness, Transcendence, and Guidance — each led by a corresponding Executive division.

### The dual model

| Body | Role |
|---|---|
| **Waqf Endowment Board** | Stewards gifts, secures perpetual funding |
| **Not-for-Profit Trust** | Day-to-day management, platform development |

### Executive Board — the eight Divine Attributes

| Attribute | Name |
|---|---|
| Majesty | **Al-ʿAzīz** |
| Beauty | **Al-Wadūd** |
| Knowledge | **Al-ʿAlīm** |
| Creation | **Al-Khāliq** |
| Justice | **Al-ʿAdl** |
| Forgiveness | **Al-Ghaffār** |
| Transcendence | **Al-Aḥad** |
| Guidance | **Al-Hādī** |

### Oversight

- **Board of Trustees** — strategy, budgets
- **Sharia Supervisory Council** — audits curricula, AI and content
- **Steering Committees** — Governance & Risk · Ethics & Sharia · Finance & Audit · Impact & Quality

### Collaboration tiers (voluntary)

Technology Engine · Islamic Scholarship · Outreach & Localization · Governance & Funding · Strategic Allies · Active Contributors · Community Anchors.

Governance is described as **led by elected volunteers**, with a Sharia board and specialist teams ensuring transparency and compliance.

## 23. Financial model

- **100% Donation & Waqf-Backed.**
- **Free at the point of use for individuals.**
- **Institutional partnerships at cost + 5%.**
- **Surplus cap ≤ 5%, with reinvestment.**
- **Zakat-eligible donation funds**, explicitly marked, with Zakat calculation guidance.
- **Sponsor-a-Student** — donors fund access for students in underserved regions.
- **Transparent donor dashboard** — aggregated, anonymised allocation of funds (server costs, feature development, content creation, sponsored seats) alongside impact metrics (active learners, courses completed).
- **Riba-free by construction** — pricing logic carries explicit compliance tags and is required to avoid interest-based mechanisms.

## 24. Compliance and ethics

**Standards:** ISO 9001 (quality), ISO 27001 (information security), GDPR, Charity SORP. COPPA appears in the later admin/security phase given the child-learner audience.

**Sharia compliance is paramount** and is enforced by scholar-led governance with regular audits of curricula, AI behaviour and content.

**Technical controls:** end-to-end encryption; RBAC; MFA; PII encryption; Helmet.js security middleware; audit logging of critical actions; data export and deletion tooling for GDPR; SAST in CI; WAF and rate limiting.

**Constitutional overrides (Workstation §11 / Appendix A.9):** six capabilities in Parts III–IV are forbidden
in Workstation regardless of what the sources say — recitation scoring, generated Qur'an Arabic, translation
of sacred text, emotion inference, Fitrah-as-measurement, and an AI Ask-a-Scholar. A surface that refuses
one of them and says so is the delivered form.

**AI ethics:** transparent AI-ethics guidelines are named as a governance obligation. The corpus does not elaborate them — see [§29](#29-what-the-vision-never-specified).

## 25. Implementation strategy

Three progressive stages forming a self-reinforcing **Build → Mobilize → Amplify** cycle:

**Strategy 1 — Build & Validate (Months 1–5).** Establish core technology, governance and the MVP (AI Tajwīd, gamified memorisation, AR/VR storytelling). Formalise partnerships. Governance charter. Iterative validation.

**Strategy 2 — Mobilize Communities (Months 6–10).** Leverage volunteer networks. Regional chapters. Cross-functional working groups. Co-creation workshops. Ambassador programme.

**Strategy 3 — Amplify & Engage (Months 11–18+).** Drive global awareness. Digital campaigns. Crowdfunding and donations. Institutional outreach. Impact measurement.

---

# Part VIII — Method

## 26. LEAN-Turbo methodology

The development doctrine, stated as governance rules rather than suggestions:

- **Every phase results in a deployable or testable artefact** — a demo, a feature flag, or a production release.
- **Maximise reuse** — UI components, utilities and services designed for sharing via `/shared` or as monorepo packages.
- **All PRs must pass automated checks** — tests, type-check, lint, format.
- **The four-goals test** — every line of code, feature and decision must demonstrably tie to *Learn / Recite / Understand / Teach*.
- **Short feedback loops** — daily stand-ups, bi-daily mini-milestone reviews, weekly comprehensive updates.
- **Time-boxed iterations** — 1–2 day sprints per mini-milestone.
- **MoSCoW prioritisation** within each phase.
- **Eliminate waste**; focus on high-impact features.
- **Maximise resource utilisation** — free-tier services first.
- **Continuous QA** — automated checks, peer review, "Gold-Standard" checklists.

## 27. PromptOps and AI-agent development

The plan anticipated being built *by* AI agents and specified how:

- A central **PromptLib** in `/agents/prompts` for reusable, versioned prompts.
- Prompt engineering libraries — LangChain, promptable, promptfoo — for managing and **testing** AI agent prompts.
- **All AI agents tested against locally mocked LLMs or sandboxed environments before production inference.**
- Regular review and versioning of prompts.
- Standardised phase templates for AI-agent prompts.
- Automated builds: GitHub Actions → deploy previews to Vercel/Netlify for the frontend, staging deploys for backend services.

**Audit note.** This discipline was specified and then not applied. The failure mode in Attempt 2 — a documentation pipeline emitting placeholders into the canonical outline while downstream documents kept citing it — is precisely what "test the agent's output before trusting it" was meant to prevent.

---

# Part IX — Unresolved

## 28. Contradictions and open decisions

These are genuine conflicts in the source material. Each needs a decision before a fourth attempt.

| # | Conflict | Positions | Recommended resolution |
|---|---|---|---|
| 1 | **Phase 15–19 content** | Ordering A keeps Fitrah / institutional / finance; Ordering B replaces them with testing / deployment / docs | **Ordering A.** See [§21](#21-the-competing-phase-1519-orderings). |
| 2 | **Authentication** | Firebase Auth vs. custom NestJS (JWT + Passport + Speakeasy) | **Custom NestJS** for core identity, RBAC and MFA; Firebase only as an OAuth broker. This is what the detailed phase plans specify. |
| 3 | **Relational database** | MySQL (free-tier plan) vs. PostgreSQL (V1.1 stack, and Attempt 3's Phase 1) | Unresolved. MySQL dominates the operative plan; Attempt 3 silently switched to PostgreSQL/Supabase. |
| 4 | **VC metadata store** | PostgreSQL (early summary) vs. MongoDB (detailed Phase 10) | **MongoDB** — settled in the merge-decisions log. |
| 5 | **WCAG target** | 2.1 AA (earlier v4 guide) vs. 2.2 AA (consolidated guide) | **2.2 AA** — the later, more demanding target. |
| 6 | **Phase 14 scope** | "Neural Core" with Kafka, ACO, Affectiva, voice agent vs. "AI orchestration service + basic avatar" | **Neural Core.** The reduced version removes what makes the platform distinctive. |
| 7 | **Swarm intelligence meaning** | ACO over collective behaviour vs. multi-agent deliberation | Both are wanted; they are different systems. Name and build them separately. |
| 8 | **Monorepo tool** | Yarn Workspaces · Nx · Turborepo · pnpm workspaces (Attempt 3) | Any; decide once and record as an ADR. |
| 9 | **Canonical phase document** | `docs/canonical_phase_outline.md` (placeholder-corrupted) vs. `docs/phase-guides/phases1-19.md` (hand-maintained) | **`phases1-19.md`.** The canonical outline is corrupt output; it should be deleted, not cited. |

## 29. What the vision never specified

Honest gaps. These are not contradictions — they are places where the vision asserts a capability without defining it. Each is a design task, not a coding task.

1. **The 99 Fitrah aspects are never enumerated.** The Spectrum is named, sized and mapped to the Asmāʾ al-Ḥusnā, but no aspect list, no assessment instrument, no scoring model, and no validation approach exists anywhere in the corpus. This is the largest gap.

2. **Sharia review of AI-generated religious content has no defined mechanism.** The governance model requires scholar audit of "AI and content", but nothing specifies how a generated tafsir explanation, dua suggestion or Hadith citation is reviewed *before* a user sees it, nor what happens when the model is wrong about the text. For a platform whose subject matter is revelation, this is the highest-risk unspecified control.

3. **Quranic text and audio provenance is never addressed.** No source is named for the Arabic text, the recitations, the translations, the Hadith corpus or the Tafsir. No licensing, no canonical edition, no *qirāʾāt* selection. The Tajwīd coach cannot be built without this decision.

4. **Tajwīd rule coverage is never scoped.** Madd and Ghunnah are used as examples throughout; the actual rule set to be detected, and to what level of madhhab-specific variation, is undefined.

5. **The AI ethics guidelines are named but not written.** "Transparent AI-ethics guidelines" is a governance obligation with no document behind it.

6. **Emotion detection raises unaddressed consent and privacy questions.** Affectiva-based emotion inference on children, in a GDPR-compliant, Sharia-compliant platform, with no stated consent model, retention policy or opt-out.

7. **Content authoring and curriculum ownership is undefined.** The lessons, modules, quizzes and Noorani Qaida/Tajwīd/Arabic/Tafsir curricula are assumed to exist. Who writes them, who approves them, and under what scholarly authority is unstated.

8. **Success is never measured.** No target user numbers, no retention or learning-outcome metrics, no definition of what "improved recitation" means quantitatively. Effort/Impact ratings are subjective 1–5 scores with no rubric.

9. **Starlink integration is an aspiration with no mechanism.** It appears in the accessibility objective and the Magnificent-7 mapping, never as a technical plan.

10. **Offline scope is undefined.** "Core content" is cached, but which content, at what size, and how memorisation and recitation work without the analysis service, is unspecified.

---

# Part X — Traceability

## 30. Source map

### Primary vision sources (highest fidelity first)

| Source | Location | What it uniquely holds |
|---|---|---|
| `AI-Driven Quranic Education Platfor SAVED.txt` (887 KB / 912 KB) | Attempt 2 `sources/`, Attempt 3 root | The original vision, objectives and feature list, plus per-component implementation transcripts |
| `compiled.txt` / `Commplied-background.txt` (52 KB) | Attempt 2 `sources/` | **Governance, Divine Attributes, Waqf model, financial model, implementation strategy, Magnificent 7** |
| `Phases1-19.txt` / `Phases-19-background-saved.txt` (85 KB) | Attempt 2 `sources/` | The v4 phase plan; the 99-aspect Fitrah Spectrum line |
| `Build on and enhance the plan; jule SAVED.txt` (282 KB) | Attempts 2 and 3 | The free-tier stack, Phase 14 detail, Jules regeneration task |
| `Personalized Guidance and Learning Application 111224.txt` (via compiled) | Attempt 2 `sources/` | The four guidance pillars, wearables context, serene UI philosophy |
| `methadology.txt` (11 KB) | Attempt 2 `sources/` | LEAN-Turbo framework, merge-decisions log |

### Derived documents (curated, reliable)

| Document | Location | Status |
|---|---|---|
| `docs/core_features_definition.md` | Attempt 2 | **Authoritative** — the 15 features |
| `docs/consolidated_source_material.md` | Attempt 2 | **Authoritative** — vision, objectives, stack, discrepancies |
| `docs/phase-guides/phases1-19.md` (1,162 lines) | Attempt 2 | **Authoritative** — the full 19-phase plan, Ordering A |
| `AI-Driven Quranic Education Platform - Developer Guide.md` (109 KB) | Attempt 2 root | **Authoritative** — architecture, Phase→Feature table, per-feature user stories |
| `AI-Driven Quranic Education Platform - Jules Agent Guide.md` (75 KB) | Attempts 1 and 2 | Agent-directed variant of the Developer Guide |
| `docs/phase-guides/phases1-19.md` (27 KB) | Attempt 3 | Ordering B — **a reduction, not a revision** |

### Documents that should not be trusted

| Document | Location | Why |
|---|---|---|
| `docs/canonical_phase_outline.md` | Attempt 2 | Placeholder-corrupted pipeline output presenting itself as canon; phase titles are arbitrary matched lines |
| `intermediaries/canonical_phase_outline.md` (171 KB) | Attempt 2 | Raw, fragmented script output |
| `intermediaries/compiled_quran_education_platform_docs.md` (53 KB) | Attempt 2 | Manually compiled, significantly redundant, superseded |
| `features/*/README.md` (15 of 19 zero-byte — every core-feature folder's, including the three with code) | Attempt 1 | Zero-byte files implying features that do not exist |

### Recurrence tally behind Appendix A's provenance grades

Computed 2026-09-11 over the 18 files in `Quran-recitation-platform/sources/` (2,395,108 bytes): the vision
statement ("universally accessible") is in 8 files, *fitrah* in 8, *waqf* in 3. The 18 are not independent —
two pairs are byte-identical (`jule.txt` ≡ `Jules-background-saved.txt`; `Developer-guide.txt` ≡
`Jules-guide.txt`), and the eight vision-statement files include re-saves of one transcript (`compiled.txt` ≡
`Commplied-background.txt`; `Combined-background-saved.txt` ⊂ `compiled-background.txt` at 95%;
`Phases-19-background-saved.txt` ⊂ at 82%) — so "eight files" is roughly five distinct texts.

### Code worth salvaging

- **Attempt 2 `mvp/backend/src/`** — 15 domain modules with entities, DTOs and service signatures. Excellent *interface* design even though every implementation is an in-memory `Map`. The best starting point for a real domain model.
- **Attempt 2 `mvp/shared/src/types`** — shared TypeScript contracts across frontend and backend.
- **Attempt 3 `packages/` + `infra/`** — the cleanest workspace, Docker, Kafka config and CI. The best starting point for repository structure, *after* relocating the misfiled recitation and competition code out of `billing/` and `auth/`.
- **Attempt 1 `features/ai-tajwid-coach/`** — 41 non-empty files; the only feature anywhere with substantial real implementation.

---

## Appendix — Recommendations for a fourth attempt

Not part of the vision; offered because the audit produced them.

1. **Adopt Ordering A** and resolve the nine conflicts in [§28](#28-contradictions-and-open-decisions) as ADRs before writing code.
2. **Close the four blocking design gaps first** — Quranic text/audio provenance, Tajwīd rule scope, the Sharia review mechanism for AI-generated religious content, and the 99 Fitrah aspects. None requires engineering; all block engineering.
3. **Invert the phase order's practical effect.** Every attempt died in Phases 1–3. Build a thin vertical slice through Phase 4 (Tajwīd coach) and Phase 14 (Neural Core) early, even against stubs, so the distinctive capability is proven before the commodity infrastructure is polished.
4. **Never let a generated document become canon without verification.** Attempt 2's pipeline emitted placeholders for twenty phases and downstream documents kept citing it. Any generated artefact needs an assertion that it contains content.
5. **Compile before committing.** Attempt 1 committed 209 TypeScript errors and 35 build logs.
6. **Treat "conceptual" implementations as debt with a name.** Attempt 2's in-memory `Map` pattern was honest but produced 11,400 lines that cannot run.

---

*Compiled from `C:\Users\rehan\github_repos\{quran-recitation-mvp, Quran-recitation-platform, QEP-MVP}`. All quotations are verbatim from those repositories. All audit figures (file counts, line counts, error counts, commit counts) were measured directly, not estimated.*
