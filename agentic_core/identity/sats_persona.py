import json
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SATsLearningPersona:
    """
    IDBO Persona for the Year 6 SATs 2026 Education Grand Operation.
    Personalized for Ayaan at Norbury School.
    """
    def __init__(self, name: str = "Ayaan"):
        self.name = name
        self.age = 10
        self.school = "Norbury School, Harrow"

        # Core profile with specific weights (1-5, 5 being most critical/strongest)
        self.strengths = {
            "Arithmetic (four operations)": 5,
            "Spelling patterns (-tion, -sion)": 4,
            "Reading literal comprehension": 5
        }
        self.areas_for_improvement = {
            "Algebra (simple equations)": 5,
            "Fractions (mixed to improper)": 4,
            "3-mark comparison (LINK structure)": 5,
            "Possessive apostrophes": 3
        }

        # Personalization data
        self.interests = ["Football (Arsenal FC)", "Minecraft", "Space/Planets", "Harrow Local Area"]
        self.learning_style = {
            "session_duration": "20-30 minutes",
            "approach": "Visual/Hands-on",
            "needs": "Clear worked examples",
            "break_frequency": "Every 2 sessions"
        }

        # Contextual mapping for question generation
        self.context_mapping = {
            "maths_reasoning": {
                "entities": ["Bukayo Saka", "Arsenal matches", "Minecraft blocks", "Space rovers", "Harrow on the Hill", "Headstone Manor Park"],
                "scenarios": [
                    "Calculating Arsenal goal averages",
                    "Building a Minecraft fortress with volume/area",
                    "Fuel calculations for a Mars mission",
                    "Distance calculations in Harrow"
                ]
            },
            "reading": {
                "topics": ["History of Arsenal FC", "Space Exploration and the Moon", "A Day at Headstone Manor Park", "Minecraft Engineering"]
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
