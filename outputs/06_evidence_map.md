# Dynamic Evidence-Knowledge Graph: Minhas v Lonza (6045461/2025)

## 🧬 Graph Version: 5.0.0-dynamic

```json
{
  "nodes": [
    {
      "id": "exhibit_q1",
      "label": "Exhibit Q-1: 94% Punctuality",
      "confidence": 0.98,
      "narrative": "Linchpin: Contradicts pretext."
    },
    {
      "id": "s15_claim",
      "label": "s.15 EqA 2010 Claim",
      "confidence": 0.94,
      "supporting": ["exhibit_q1", "contemporaneous_logs"]
    }
  ],
  "edges": [
    {
      "source": "exhibit_q1",
      "target": "s15_claim",
      "relationship": "supports",
      "strength": 0.92
    }
  ]
}
```

---
**Author:** Jules, AI CEO (Law Domain Orchestrator)
**Date:** 30 Mar 2026 (Intelligence-Active)
