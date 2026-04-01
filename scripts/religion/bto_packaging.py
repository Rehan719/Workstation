import os
import json
from datetime import datetime

class BTOProducts:
    def __init__(self):
        self.output_base = "outputs/Religion"
        self.master_path = "outputs/Religion/Comprehensive/comprehensive_v2.0.md"

    def generate_all_variants(self):
        if not os.path.exists(self.master_path):
            return "Master file not found."

        with open(self.master_path, 'r') as f:
            content = f.read()

        # Variant 1: Study Guide
        study_guide = content.replace("# The Path", "# Study Guide: The Path")
        study_guide += "\n\n## Discussion Questions\n1. What is the most significant barrier to sincerity in your daily life?\n2. How can you practically implement Quranic reflection today?"
        self._save("StudyGuide", "study_guide_v2.0.md", study_guide)

        # Variant 2: Pocket Guide
        pocket_guide = "# Pocket Guide: The Path to Allah's Love\n\n## 5 Core Reminders\n1. Ikhlas (Sincerity)\n2. Tawbah (Repentance)\n3. Shukr (Gratitude)\n4. Sabr (Patience)\n5. Tawakkul (Trust)"
        self._save("Pocket", "pocket_guide_v2.0.md", pocket_guide)

        # Variant 3: Youth Edition
        youth_edition = content.replace("# The Path", "# Youth Edition: The Path")
        youth_edition += "\n\n## Level Up Challenge\nCan you go 7 days without complaining and only showing gratitude (Shukr)? Tag your progress!"
        self._save("Youth", "youth_v2.0.md", youth_edition)

        # Variant 4: Scholar Edition (with source metadata)
        scholar_edition = content.replace("# The Path", "# Scholar Edition: The Path")
        scholar_edition += "\n\n## Technical Appendix\n- Source: IDBO-ISLAM-2026-001\n- Version: 1.0.0-MUD\n- Theological Alignment: Sunni"
        self._save("Scholar", "scholar_v2.0.md", scholar_edition)

    def _save(self, folder, filename, content):
        path = os.path.join(self.output_base, folder)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, filename), 'w') as f:
            f.write(content)
        print(f"📦 Product variant generated: {filename}")

if __name__ == "__main__":
    bto = BTOProducts()
    bto.generate_all_variants()
