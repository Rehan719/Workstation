import json
import os
import hashlib
import asyncio
from typing import List, Dict, Any, Optional
from agentic_core.mjm.mjm import MJMOrchestratorV4
from agentic_core.identity.sats_persona import SATsLearningPersona
from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.domains.education.mushawara_bridge import MushawaraBridge

class SATsQuestionGenerator:
    """
    Ultimate SATs Question Generator (v∞).
    Utilizes MJM v4.0 and Mushawara Bridge for refined, sequential, and unique content.
    """
    def __init__(self, persona: SATsLearningPersona, output_dir: str = "outputs/education/sats_2026/predicted_questions"):
        self.persona = persona
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.ueg = VSBUEGLogger()
        self.mjm = MJMOrchestratorV4(ueg_logger=self.ueg)
        self.mushawara = MushawaraBridge(ueg_logger=self.ueg)

    def _log_to_ueg(self, event_type: str, data: Dict[str, Any]):
        audit_path = os.path.join(self.output_dir, "../../ueg_audit.jsonl")
        content = json.dumps(data, sort_keys=True).encode()
        event_hash = hashlib.sha3_512(content).hexdigest()
        log_entry = {"event": event_type, "hash": event_hash, "data": data}
        with open(audit_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def _dedup_and_sequence(self, questions: List[Dict[str, Any]], prefix: str) -> List[Dict[str, Any]]:
        """Ensures unique questions and perfect sequential numbering."""
        seen = set()
        unique = []
        for q in questions:
            q_text = q["question"]
            if q_text not in seen:
                seen.add(q_text)
                unique.append(q)

        # Reset numbering
        for i, q in enumerate(unique):
            q["id"] = f"{prefix}_{i+1}"
        return unique

    @constitutional_guard
    async def generate_maths_arithmetic(self) -> List[Dict[str, Any]]:
        """Mathematics Paper 1 - Refined with Mushawara."""
        await self.mushawara.deliberate("Maths Arithmetic", "Focus on sequential difficulty")
        questions = []

        # 1-20: Strengths (Addition/Subtraction/Multiplication)
        for i in range(1, 21):
            questions.append({"type": "arithmetic", "question": f"{456 + (i*11)} + {123 * (i%3 + 1)}", "topic": "Addition"})

        # 21-30: Fractions (Improvement area)
        for i in range(21, 31):
            questions.append({"type": "arithmetic", "question": f"Convert 3 and {i-20}/8 to an improper fraction.", "topic": "Fractions"})

        # 31-40: Decimals & Long Division
        for i in range(31, 41):
            questions.append({"type": "arithmetic", "question": f"{(i*15.5):.1f} - {i*2.25:.1f}", "topic": "Decimals"})

        final_set = self._dedup_and_sequence(questions, "MA")
        self._log_to_ueg("generate_maths_arithmetic_refined", {"count": len(final_set)})
        return final_set

    @constitutional_guard
    async def generate_maths_reasoning(self, paper_num: int) -> List[Dict[str, Any]]:
        """Mathematics Paper 2 & 3 - Personalised with MJM."""
        questions = []
        # Paper 2 focus: Number & Ratio
        # Paper 3 focus: Measurement & Geometry

        if paper_num == 2:
            questions.append({"type": "reasoning", "question": f"Arsenal played 38 matches. They won 24, drew 6 and lost the rest. What fraction of matches did they lose?", "topic": "Fractions/Context"})
            questions.append({"type": "reasoning", "question": f"In Minecraft, 1 stack of cobblestone is 64 blocks. How many blocks are in 12 stacks?", "topic": "Multiplication"})
            questions.append({"type": "reasoning", "question": f"A bag of space-dust weighs 1.2kg. If 3.6kg is shared into 4 equal rover-packs, how many grams in each?", "topic": "Measurement"})
        else:
            questions.append({"type": "reasoning", "question": f"The temperature on Mars is -55C. It rises by 12C. What is the new temperature?", "topic": "Negative Numbers"})
            questions.append({"type": "reasoning", "question": f"Calculate the area of a rectangular Minecraft farm that is 15 blocks long and 8 blocks wide.", "topic": "Area"})
            questions.append({"type": "reasoning", "question": f"Bukayo Saka ran 9.8km in a match. Write this distance in meters.", "topic": "Measurement"})

        final_set = self._dedup_and_sequence(questions, f"MR{paper_num}")
        self._log_to_ueg(f"generate_maths_reasoning_refined_p{paper_num}", {"count": len(final_set)})
        return final_set

    @constitutional_guard
    async def generate_english_gps(self) -> List[Dict[str, Any]]:
        """English GPS - Refined."""
        questions = [
            {"type": "punctuation", "question": "Circle the possessive apostrophe: The players' boots were lined up by the tunnel.", "topic": "Apostrophe"},
            {"type": "grammar", "question": "Underline the subordinate clause: While the rocket was fueling, the crew checked their instruments.", "topic": "Clauses"},
            {"type": "vocabulary", "question": "Which word is a synonym for 'fast'? (Quick / Slow / Heavy)", "topic": "Synonyms"}
        ]
        # Spellings
        spellings = ["profession", "exaggeration", "conscience", "queue", "immediately"]
        for s in spellings:
            questions.append({"type": "spelling", "question": f"Spell: {s}", "topic": "Spelling"})

        final_set = self._dedup_and_sequence(questions, "GPS")
        return final_set

    @constitutional_guard
    async def generate_reading(self) -> List[Dict[str, Any]]:
        """English Reading - Domain 2d & LINK focus."""
        questions = [
            {"type": "inference", "question": "Give two pieces of evidence that show the character was excited about the Arsenal match.", "topic": "Domain 2d"},
            {"type": "comparison", "question": "Compare the description of the Earth from space at the start and end of the text. Use the LINK structure.", "topic": "LINK Structure"}
        ]
        return self._dedup_and_sequence(questions, "RD")

    async def save_all(self):
        papers = {
            "maths_arithmetic.json": await self.generate_maths_arithmetic(),
            "maths_reasoning_1.json": await self.generate_maths_reasoning(2),
            "maths_reasoning_2.json": await self.generate_maths_reasoning(3),
            "english_gps.json": await self.generate_english_gps(),
            "english_reading.json": await self.generate_reading()
        }
        for filename, data in papers.items():
            with open(os.path.join(self.output_dir, filename), "w") as f:
                json.dump(data, f, indent=4)
        return list(papers.keys())

async def main():
    persona = SATsLearningPersona()
    gen = SATsQuestionGenerator(persona)
    await gen.save_all()
    print("REFINED SATs Questions Generated.")

if __name__ == "__main__":
    asyncio.run(main())
