import json
import os
import hashlib
import asyncio
from typing import List, Dict, Any
from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.ueg.logger import VSBUEGLogger

class SATsAnswerGenerator:
    """
    Refined SATs Answer Generator (v∞).
    Provides deeper explainers and structured pedagogical solutions.
    """
    def __init__(self, input_dir: str = "outputs/education/sats_2026/predicted_questions",
                 output_dir: str = "outputs/education/sats_2026/model_answers"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.ueg = VSBUEGLogger()

    def _log_to_ueg(self, event_type: str, data: Dict[str, Any]):
        audit_path = os.path.join(self.output_dir, "../../ueg_audit.jsonl")
        content = json.dumps(data, sort_keys=True).encode()
        event_hash = hashlib.sha3_512(content).hexdigest()
        log_entry = {"event": event_type, "hash": event_hash, "data": data}
        with open(audit_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    @constitutional_guard
    async def solve_arithmetic(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Pedagogical solutions for Arithmetic."""
        answers = []
        for q in questions:
            if q["topic"] == "Addition":
                parts = q["question"].split(" + ")
                res = int(parts[0]) + int(parts[1])
                method = f"Step 1: Write the numbers in columns, aligning place values. Step 2: Add ones (0+0), tens (0+0), hundreds (0+5). Step 3: Add thousands ({parts[0][0]}+0). Total: {res}."
            elif q["topic"] == "Fractions":
                # "Convert 5 and {x}/9 to an improper fraction."
                parts = q["question"].split(" ")
                num = int(parts[3].split("/")[0])
                res = f"{(5*9)+num}/9"
                method = f"Step 1: Multiply the whole number (5) by the denominator (9): 5 * 9 = 45. Step 2: Add the numerator ({num}): 45 + {num} = {5*9+num}. Step 3: Put this over the original denominator: {res}."
            elif q["topic"] == "Decimals":
                parts = q["question"].split(" - ")
                res = round(float(parts[0]) - float(parts[1]), 2)
                method = f"Step 1: Align decimal points. Add a placeholder 0 to {parts[1]} if needed to match decimal places. Step 2: Subtract normally, keeping decimal in line. {parts[0]} - {parts[1]} = {res}."
            else:
                res = "Pending"
                method = "Detailed step-by-step method."

            answers.append({"question_id": q["id"], "question": q["question"], "answer": res, "worked_solution": method})
        return answers

    @constitutional_guard
    async def solve_reasoning(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Pedagogical solutions for Reasoning."""
        answers = []
        for q in questions:
            if "Arsenal" in q["question"] and "algebraic" in q["question"]:
                res = "38 - w - 5"
                method = "Step 1: Start with total matches (38). Step 2: Subtract wins (w) and losses (5). The remaining matches are draws. Expression: 38 - w - 5 (or 33 - w)."
            elif "Minecraft" in q["question"] and "ratio" in q["question"]:
                res = "25 emeralds"
                method = "Step 1: Ratio is 3:5. Step 2: Ayaan found 15 diamonds. 15 is 3 * 5. Step 3: Multiply the emerald part by the same number (5): 5 * 5 = 25."
            elif "Harrow" in q["question"] and "miles" in q["question"]:
                res = "3,862.4m (approx) or 3,840m if using 1.6km conversion"
                method = "Step 1: 1 mile is approx 1.6km. 2.4 miles * 1.6 = 3.84km. Step 2: Convert km to m by multiplying by 1000. 3.84 * 1000 = 3,840m."
            elif "x + 15 = 40" in q["question"]:
                res = "25"
                method = "Step 1: To find x, subtract 15 from both sides of the equation. Step 2: 40 - 15 = 25. So, x = 25."
            elif "Mars" in q["question"]:
                res = "-48C"
                method = "Step 1: Start at -63. Step 2: 'Rises' means add. -63 + 15. Step 3: Moving 15 steps towards zero from -63 gives -48."
            elif "area" in q["question"]:
                res = "108 blocks squared"
                method = "Step 1: Area = length * width. Step 2: 12 * 9 = 108. Don't forget the 'squared' unit!"
            elif "Saka" in q["question"]:
                res = "10,500m"
                method = "Step 1: Multiply km by 1,000 to get meters. Step 2: 10.5 * 1,000 = 10,500."
            elif "Headstone Manor Park" in q["question"]:
                res = "15:47"
                method = "Step 1: Start at 16:05 and count back 18 minutes. Step 2: 5 minutes back to 16:00, then 13 more minutes back to 15:47."
            else:
                res = "Pending"
                method = "Logical breakdown."

            answers.append({"question_id": q["id"], "question": q["question"], "answer": res, "worked_solution": method})
        return answers

    @constitutional_guard
    async def solve_reading(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Pedagogical solutions for Reading with LINK structure."""
        answers = []
        for q in questions:
            if q["topic"] == "Domain 2d" and "Headstone" in q["question"]:
                res = "Evidence 1: He arrived 20 minutes before the gates opened. Evidence 2: He was wearing his favorite Arsenal kit for the trip."
                method = "Inference (Domain 2d): Use direct evidence from the text to support your points."
            elif q["topic"] == "LINK Structure":
                res = {
                    "Link": "The stadium is described as energetic at the start but tense at the end.",
                    "Evidence 1": "At the start, the crowd was a 'roaring ocean of red'.",
                    "Evidence 2": "At the end, there was a 'hushed, heavy silence'.",
                    "Explain": "The contrast between 'roaring' and 'silence' shows how the atmosphere shifted as the game became closer."
                }
                method = "Comparison (LINK): Use the LINK structure (Link, Evidence 1, Evidence 2, Explain) to earn all 3 marks."
            elif q["topic"] == "Domain 2d" and "Minecraft" in q["question"]:
                res = "The author says the wind felt 'cold on their faces' and they could 'smell the woodsmoke' from the virtual fires."
                method = "Inference (Domain 2d): Using sensory details as quotes provides strong evidence."
            elif q["topic"] == "Vocabulary":
                res = "Immense means extremely large or huge."
                method = "Vocabulary: Look at the surrounding sentences to find clues about the word's meaning."
            else:
                res = "Pending"
                method = "Textual analysis."
            answers.append({"question_id": q["id"], "question": q["question"], "answer": res, "method_or_worked_solution": method})
        return answers

    @constitutional_guard
    async def solve_gps(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Pedagogical solutions for GPS."""
        answers = []
        for q in questions:
            if q["topic"] == "Apostrophe" and "dressing room" in q["question"]:
                res = "players'"
                method = "The players (plural) own the room. Since it ends in 's', add the apostrophe after the 's'."
            elif q["topic"] == "Apostrophe" and "rocket" in q["question"]:
                res = "Ayaan's rocket took off"
                method = "Ayaan is singular. Add 's to show possession."
            elif q["topic"] == "Clauses":
                res = "While Ayaan was building his Minecraft base"
                method = "This is a subordinate clause because it starts with the conjunction 'While' and doesn't make sense on its own."
            elif q["topic"] == "Verb Agreement":
                res = "celebrate"
                method = "The subject 'pupils' is plural, so we use the plural verb 'celebrate'."
            elif q["topic"] == "Spelling":
                res = q["question"].replace("Spell: ", "")
                method = "Spelling rule or pattern reinforcement."
            else:
                res = "Pending"
                method = "Grammatical rule application."
            answers.append({"question_id": q["id"], "question": q["question"], "answer": res, "rule_or_justification": method})
        return answers

    async def process_all(self):
        mapping = {
            "maths_arithmetic.json": self.solve_arithmetic,
            "maths_reasoning_1.json": self.solve_reasoning,
            "maths_reasoning_2.json": self.solve_reasoning,
            "english_reading.json": self.solve_reading,
            "english_gps.json": self.solve_gps
        }
        for filename, solver in mapping.items():
            path = os.path.join(self.input_dir, filename)
            if os.path.exists(path):
                with open(path, "r") as f: questions = json.load(f)
                answers = await solver(questions)
                with open(os.path.join(self.output_dir, filename.replace(".json", "_answers.json")), "w") as f:
                    json.dump(answers, f, indent=4)

async def main():
    gen = SATsAnswerGenerator()
    await gen.process_all()
    print("REFINED SATs Answers Generated.")

if __name__ == "__main__":
    asyncio.run(main())
