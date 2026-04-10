# Ijazah/Sanad Chain Verification Flow (v8.1)
## Domain: RELIGION::QEP::SCHOLAR

### 1. Chain Ingestion
Students or teachers submit their Ijazah chains as JSON structures or through the UI.

### 2. Node Analysis
The `mock_verifier.py` parses each node in the sanad chain, checking for historical consistency (birth/death years, locations, transmitter reliability).

### 3. Scholar Board Consensus (Emulated)
The verification is reviewed by the Scholar Board (emulated for v8.1). A consensus of 5 qualified scholars is required for final validation.

### 4. Verification Status Update
Once verified, the chain's status is updated to `VERIFIED`, and a new achievement badge is awarded to the student/teacher.

---
**Status:** PoC | **Last Updated:** 2026-04-01
