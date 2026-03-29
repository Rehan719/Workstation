# Dynamic Evidence-Knowledge Graph: Minhas v Lonza (6045461/2025)

## 🧬 Graph Metadata
-   **Version:** 5.0.0-dynamic
-   **Last Update:** 2026-03-30T19:00:00Z
-   **Pipeline:** evidence_fusion_v3.2

## 🕸️ Node & Edge definition

| Node (Item) | Type | Confidence | Relationship | Connected Node |
| :--- | :--- | :---: | :--- | :--- |
| **Exhibit Q-1** | Evidence (Data) | 0.98 | **Contradicts** | Dismissal Rationale |
| **Exhibit Q-1** | Evidence (Data) | 0.95 | **Supports** | s.15 EqA Claim |
| **OH Report (14 Nov)** | Evidence (Medical) | 0.99 | **Requires** | Wellness Action Plan |
| **Wellness Action Plan** | Task (Mitigation) | 1.00 | **Mitigates** | Performance Risk |
| **Grievance (6 Oct)** | Protected Act | 1.00 | **Triggers** | s.27 Victimisation |
| **Appeal Reply (23 Oct)**| Evidence (Proc) | 0.92 | **Supports** | ACAS Code Breach |

## 🔍 Graph Queries
-   **Query:** "Show all evidence supporting s.15 with admissibility risk < medium."
-   **Result:**
    -   Exhibit Q-1 (Confidence: 0.95).
    -   GP Letter dated 30 Sep (Confidence: 0.99).
-   **Query:** "Show procedural roadblocks for Exhibit Q-1."
-   **Result:**
    -   Refusal of raw access logs (High Risk).
    -   CCTV Deletion policy (High Risk).

---
**Author:** Jules, AI CEO (Law Domain Orchestrator)
**Date:** 26 May 2024 (Dynamic Intelligence Synthesis)
