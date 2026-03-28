import json
from typing import List, Dict, Any

class PresentationGenerator:
    """v1.0 Production: Generates multi-slide presentations with narration metadata."""

    def generate_presentation(self, topic: str) -> List[Dict[str, Any]]:
        slides = [
            {
                "id": 1,
                "title": "Patient Safety in Advanced Therapies",
                "content": "Executive Summary of the current gaps in safety monitoring for AAV, CAR-T, and mRNA.",
                "narration": "Welcome to this executive summary. Today we address the critical safety gaps in next-generation advanced therapies.",
                "animation": "fade-in",
                "sound": "startup"
            },
            {
                "id": 2,
                "title": "AAV Germline Risks",
                "content": "Wu et al. 2025: Integration risks higher than estimated. Need for pre-emptive genomic screening.",
                "narration": "Wu et al 2025 indicates that AAV germline integration risks are significantly higher than previously estimated. This demands immediate attention.",
                "visual": "/assets/sim/aav_struct.png"
            },
            {
                "id": 3,
                "title": "CAR-T Autoimmune Hazards",
                "content": "Chazarin et al. 2026: Longitudinal tracking required for autoimmune complications.",
                "narration": "CAR-T therapies, while revolutionary, show new autoimmune risks as identified by Chazarin et al in 2026.",
                "animation": "slide-left"
            },
            {
                "id": 4,
                "title": "Regulatory Landscape",
                "content": "FDA, EMA, and EU legislation. Gifford et al. 2025: Identifying regulatory lag in mRNA stability.",
                "narration": "Regulators like the FDA and EMA are struggling to keep pace. Gifford et al 2025 points to a clear lag in EU legislation regarding mRNA markers.",
                "sound": "alert-soft"
            },
            {
                "id": 5,
                "title": "The Opportunity Window",
                "content": "Risk of inaction vs. market leadership. $4.2B market projected by 2030.",
                "narration": "There is a massive opportunity here. The Long-Term Safety Assurance market is projected to reach 4.2 billion dollars by 2030.",
                "visual": "/assets/sim/market_growth.png"
            },
            {
                "id": 6,
                "title": "Five-Point Framework",
                "content": "1. PGS  2. RCM  3. SLF  4. CAEH  5. EAIDE",
                "narration": "Our proposed five-point framework covers everything from genomic screening to ethical AI oversight.",
                "animation": "zoom-in"
            },
            {
                "id": 7,
                "title": "Business Case & ROI",
                "content": "30% reduction in clinical trial attrition for early adopters.",
                "narration": "The ROI is clear: early adopters can see up to a 30% reduction in clinical trial attrition by using these safety modules.",
                "sound": "success"
            },
            {
                "id": 8,
                "title": "Risk of Inaction",
                "content": "Patient injury, legal liability, and regulatory shutdowns.",
                "narration": "The risk of inaction is not just financial. It involves patient safety, liability, and the potential for total regulatory shutdown.",
                "animation": "shake"
            },
            {
                "id": 9,
                "title": "Roadmap to Implementation",
                "content": "BTO Swarm orchestration for rapid framework deployment.",
                "narration": "Our roadmap leverages BTO swarms to rapidly deploy this framework across your organization.",
                "visual": "/assets/sim/roadmap.png"
            },
            {
                "id": 10,
                "title": "Conclusion",
                "content": "Sovereign safety is the only path to sustainable scaling.",
                "narration": "In conclusion, sovereign patient safety is the only path forward. We are ready to lead this transition.",
                "sound": "shutdown"
            }
        ]
        return slides

presentation_gen = PresentationGenerator()
