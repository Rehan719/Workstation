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
        """Mathematics Paper 1 - Refined for Ayaan."""
        await self.mushawara.deliberate("Maths Arithmetic", "Sequential difficulty build-up")
        questions = []

        # 1-20: Confidence builders (Addition/Subtraction/Multiplication)
        for i in range(1, 21):
            questions.append({"type": "arithmetic", "question": f"{1000 + (i*25)} + {500 * (i%4 + 1)}", "topic": "Addition"})

        # 21-35: Fractions (Targeted improvement)
        for i in range(21, 36):
            questions.append({"type": "arithmetic", "question": f"Convert 5 and {i-20}/9 to an improper fraction.", "topic": "Fractions"})

        # 36-40: Decimals
        for i in range(36, 41):
            questions.append({"type": "arithmetic", "question": f"{(i*20.5):.1f} - {i*1.75:.1f}", "topic": "Decimals"})

        final_set = self._dedup_and_sequence(questions, "MA")
        self._log_to_ueg("generate_maths_arithmetic_personalised", {"count": len(final_set)})
        return final_set

    @constitutional_guard
    async def generate_maths_reasoning(self, paper_num: int) -> List[Dict[str, Any]]:
        """Mathematics Paper 2 & 3 - High context for Ayaan."""
        questions = []

        if paper_num == 2:
            # Number, Ratio & Algebra (Ayaan's focus)
            questions.append({"type": "reasoning", "question": "Ayaan's favorite team Arsenal played 38 matches. If they win 'w' matches and lose 5, write an algebraic expression for the matches they drew.", "topic": "Algebra"})
            questions.append({"type": "reasoning", "question": "In a Minecraft world, the ratio of diamonds to emeralds in a chest is 3:5. If Ayaan finds 15 diamonds, how many emeralds are there?", "topic": "Ratio"})
            questions.append({"type": "reasoning", "question": "A bus from Harrow town centre to Norbury School travels 2.4 miles. How many metres is that?", "topic": "Measurement"})
            questions.append({"type": "reasoning", "question": "If x + 15 = 40, what is the value of x in Ayaan's Minecraft score calculation?", "topic": "Algebra"})
        else:
            # Measurement, Geometry & Statistics
            questions.append({"type": "reasoning", "question": "The temperature on Mars is -63C. It rises by 15C. What is the new temperature for Ayaan's rover?", "topic": "Negative Numbers"})
            questions.append({"type": "reasoning", "question": "Calculate the area of a rectangular farm in Minecraft that is 12 blocks long and 9 blocks wide.", "topic": "Area"})
            questions.append({"type": "reasoning", "question": "Bukayo Saka ran 10.5km in a match. Write this distance in meters.", "topic": "Measurement"})
            questions.append({"type": "reasoning", "question": "Ayaan walks from Norbury School to Headstone Manor Park. It takes 18 minutes. If he arrives at 16:05, what time did he leave school?", "topic": "Time"})

        final_set = self._dedup_and_sequence(questions, f"MR{paper_num}")
        self._log_to_ueg(f"generate_maths_reasoning_personalised_p{paper_num}", {"count": len(final_set)})
        return final_set

    @constitutional_guard
    async def generate_english_gps(self) -> List[Dict[str, Any]]:
        """English GPS - Contextualized for Ayaan."""
        questions = [
            {"type": "punctuation", "question": "Circle the possessive apostrophe: The Arsenal players' dressing room was ready for the big match.", "topic": "Apostrophe"},
            {"type": "grammar", "question": "Underline the subordinate clause: While Ayaan was building his Minecraft base, a creeper appeared behind him.", "topic": "Clauses"},
            {"type": "punctuation", "question": "Which sentence uses the possessive apostrophe correctly? (Ayaan's rocket took off / Ayaans' rocket took off)", "topic": "Apostrophe"},
            {"type": "grammar", "question": "The pupils of Norbury School ___ (celebrate/celebrates) their SATs achievements. Circle the correct verb.", "topic": "Verb Agreement"}
        ]
        # Spellings
        spellings = ["profession", "exaggeration", "conscience", "queue", "immediately"]
        for s in spellings:
            questions.append({"type": "spelling", "question": f"Spell: {s}", "topic": "Spelling"})

        final_set = self._dedup_and_sequence(questions, "GPS")
        return final_set

    @constitutional_guard
    async def generate_reading(self) -> List[Dict[str, Any]]:
        """English Reading - Domain 2d & LINK focus for Ayaan."""
        questions = [
            {"type": "inference", "question": "Give two pieces of evidence from the text that show Ayaan was excited about visiting Headstone Manor Park.", "topic": "Domain 2d"},
            {"type": "comparison", "question": "Compare the description of the Emirates Stadium at the beginning of the match to the description at the end. Use the LINK structure.", "topic": "LINK Structure"},
            {"type": "inference", "question": "How does the author show that the Minecraft world felt real to the players? Use quotes to support your answer.", "topic": "Domain 2d"},
            {"type": "vocabulary", "question": "What does the word 'immense' mean in the context of the rocket's launch?", "topic": "Vocabulary"}
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
