import json
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SATsLearningPersona:
    """
    IDBO Persona for the Year 6 SATs 2026 Education Grand Operation.
    """
    def __init__(self, name: str = "Norbury Pupil"):
        self.name = name
        self.age = 10
        self.school = "Norbury School, Harrow"

        # Core profile
        self.strengths = ["Arithmetic (four operations)", "Spelling patterns (-tion, -sion)", "Reading literal comprehension"]
        self.areas_for_improvement = ["Algebra (simple equations)", "Fractions (mixed to improper)", "3-mark comparison (LINK structure)", "Possessive apostrophes"]

        # Personalization data
        self.interests = ["Football (Arsenal)", "Minecraft", "Space/Planets"]
        self.learning_style = {
            "session_duration": "20-30 minutes",
            "approach": "Visual/Hands-on",
            "needs": "Clear worked examples"
        }

        # Contextual mapping for question generation
        self.context_mapping = {
            "maths_reasoning": {
                "entities": ["Bukayo Saka", "Arsenal matches", "Minecraft blocks", "Space rovers"],
                "scenarios": ["Calculating goal averages", "Building a Minecraft fortress", "Fuel for Mars mission"]
            },
            "reading": {
                "topics": ["Space exploration", "History of football", "Digital world construction"]
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "age": self.age,
            "school": self.school,
            "strengths": self.strengths,
            "areas_for_improvement": self.areas_for_improvement,
            "interests": self.interests,
            "learning_style": self.learning_style,
            "context_mapping": self.context_mapping
        }

def initialize_child_digital_twin(output_path: str = "outputs/education/sats_2026/idbo_profile.json"):
    """
    Initializes and saves the child's Digital Twin profile.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    persona = SATsLearningPersona()
    profile_data = persona.to_dict()

    with open(output_path, "w") as f:
        json.dump(profile_data, f, indent=4)

    logger.info(f"IDBO: Digital Twin profile initialized and saved to {output_path}")
    return profile_data
