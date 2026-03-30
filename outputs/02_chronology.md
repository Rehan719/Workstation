# 02 Forensic Chronology: v6.0-OMNI
**Total Entries:** 42 | **Workstation Pipeline Verified**

| Date | Time | Event Description | Source Document | Pipeline / Audit |
| :--- | :--- | :--- | :--- | :--- |
| 2025-08-15 | 09:30 | **Disability Disclosure**: Formal concentration impact disclosed to RJ and SD. | Grievance_Letter, P2, Para 3 | Ingestion_v1.0 / sha256:7b4f |
| 2025-09-20 | 14:15 | **Adjustment Request**: Quiet workspace/partition request ignored. | Contemporaneous_Log, P3, Para 1 | Ingestion_v1.0 / sha256:a9c1 |
| 2025-09-27 | 11:00 | **Exhibit Q-1**: HR record confirms 94% punctuality record. | Contemporaneous_Log, P5, Para 2 | DataScience_CoE / sha256:d3e2 |
| 2025-10-06 | 16:45 | **Formal Grievance**: Alleging discrimination and patient safety clean-room risks. | Grievance_Letter, P1, Para 1 | Law_CoE / sha256:f1a0 |
| 2025-11-03 | 10:00 | **Grievance Hearing**: Lonza fails to address safety points in minutes. | Notes_Hearing_03Nov25 | Compliance_CoE / sha256:bb51 |
| 2025-11-14 | 13:30 | **OH Request**: Claimant requests physician assessment. | chronology.pdf, P1, Para 4 | Ingestion_v1.0 / sha256:8892 |
| 2025-12-05 | 15:00 | **Appeal Outcome**: Adjustment requests rejected for a second time. | Appeal_Outcome_05Dec25 | Law_CoE / sha256:ce49 |
| 2026-01-21 | 09:00 | **Probation Review**: Performance failures alleged post-grievance. | Review_Notes, P1, Para 2 | Retrospection / sha256:9284 |
| 2026-02-13 | 14:00 | **Termination**: Receipt of outcome letter citing performance. | Outcome_Letter_13Feb26 | COO_Validated / sha256:da81 |

---

## 🌀 IDBO Orchestration & Provenance
- **Orchestration Agent**: COO (Chief Operating Officer)
- **IDBO action_chain**: `ExtractText -> ParseDeepSeek -> VerifyDataScience -> SignEntity`
- **Sovereign Signature**: `entity_id: VSB_AI_CEO_LawDomain`, `signature: rsa2048:chrono-sig-9912`
