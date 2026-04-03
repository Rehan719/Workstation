import json
import os
import hashlib
from datetime import datetime, timezone

class CurriculumGenerator:
    """
    Generator for Quran Education Platform Curriculum Modules
    Domain: RELIGION::QEP::FORGE
    """
    def __init__(self, ontology_dir="knowledge/Religion/QuranEducation/ontology", output_dir="outputs/Religion/QuranEducation/curriculum/samples"):
        self.ontology_dir = ontology_dir
        self.output_dir = output_dir
        self._load_ontologies()

    def _load_ontologies(self):
        with open(os.path.join(self.ontology_dir, "quranic_concepts.json"), "r") as f:
            self.concepts = json.load(f)["quranic_concept_ontology"]["concepts"]
        with open(os.path.join(self.ontology_dir, "tajweed_rules.json"), "r") as f:
            self.rules = json.load(f)["tajweed_rule_ontology"]["rules"]
        with open(os.path.join(self.ontology_dir, "hifz_progression.json"), "r") as f:
            self.hifz = json.load(f)["hifz_progression_ontology"]

    def generate_lesson(self, level, lesson_id, surah_name):
        """Generates a complete lesson module based on level and surah"""
        # Select concept and rule based on level
        concept = next((c for c in self.concepts if c["level"] == level), self.concepts[0])
        rule = next((r for r in self.rules if r["level"] == level), self.rules[0])

        lesson_content = f"""# Level {level} Lesson {lesson_id}: {surah_name}

## 1. Introduction to {surah_name}
{surah_name} is a significant chapter of the Quran. This lesson will focus on its meaning and recitation.

## 2. Quranic Concept: {concept["term"]}
**Description:** {concept["description"]}
**Significance:** {concept["significance"]}
**Related Verses:** {", ".join(concept["related_verses"])}

## 3. Tajweed Rule: {rule["name"]}
**Definition:** {rule["description"]}
**Applicable Letters:** {", ".join(rule.get("letters", ["N/A"]))}

## 4. Recitation Practice
Recite the first 5 verses of {surah_name} focusing on the rule of {rule["name"]}.

## 5. Assessment
Complete the quiz at the end of this module to verify your understanding.
"""
        # Save to output
        output_path = os.path.join(self.output_dir, f"level_{level}", f"lesson_{lesson_id}_{surah_name.lower().replace(' ', '_')}")
        os.makedirs(output_path, exist_ok=True)

        with open(os.path.join(output_path, "content.md"), "w") as f:
            f.write(lesson_content)

        # Generate assessment JSON
        assessment = {
            "lesson_id": lesson_id,
            "level": level,
            "questions": [
                {
                    "question": f"What is the definition of {concept['term']}?",
                    "options": [concept["description"], "Other random answer", "Incorrect info"],
                    "answer": 0
                },
                {
                    "question": f"Which rule is focus of this lesson?",
                    "answer": rule["name"]
                }
            ]
        }
        with open(os.path.join(output_path, "assessment.json"), "w") as f:
            json.dump(assessment, f, indent=2)

        print(f"Generated Lesson for Level {level}: {surah_name}")
        return output_path

if __name__ == "__main__":
    generator = CurriculumGenerator()
    generator.generate_lesson(1, 1, "Al-Fatihah")
    generator.generate_lesson(5, 1, "An-Nahl")
    generator.generate_lesson(10, 1, "Al-Baqarah Advanced")
