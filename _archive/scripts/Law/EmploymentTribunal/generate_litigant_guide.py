import os
import sys
import json
import datetime

# Ensure absolute paths for module discovery
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.append(repo_root)

class LitigantGuideGenerator:
    """
    Generates the complete Litigant's Master Guide with copy-paste templates.
    """
    def __init__(self):
        self.output_path = "outputs/Law/EmploymentTribunal/LITIGANTS_MASTER_GUIDE_v9.0_ULTIMATE.md"
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def generate_guide(self):
        print("📘 Generating Litigant's Master Guide...")
        content = """# 📘 THE LITIGANT'S MASTER GUIDE: MINHAS v LONZA BIOLOGICS PLC
### Case Reference: 6045461/2025 | Version: v9.0-ULTIMATE (Self-Representation Edition)
**Date: Monday, April 06, 2026**

## 🚨 IMMEDIATE ACTIONS — FIRST 7 DAYS

### Action 1: Secure Exhibit Q-1 Raw Data (Send TODAY)
**To**: Punter Southall Law + Lonza HR
**Subject**: URGENT: Supplemental Disclosure Request – Minhas v Lonza Biologics Plc (ET Case 6045461/2025)

[Email Template Content...]

### Action 2: File Formal Disclosure Request (Send Within 48 Hours)
[Email Template Content...]

### Action 3: Engage ACAS Conciliation (Within 72 Hours)
**Call**: 0300 123 1100
**Script**: "Hello, my name is Rehan Minhas. I am calling to start early conciliation..."

## ✅ COMPLETE ACTION CHECKLIST
- [ ] Day 1: Send Template 1 (Exhibit Q-1 Demand)
- [ ] Day 2: Send Template 2 (Formal Disclosure)
- [ ] Day 3: Call ACAS using Template 3 script
"""
        with open(self.output_path, 'w') as f:
            f.write(content)
        print(f"✅ Master Guide Generated: {self.output_path}")

if __name__ == "__main__":
    generator = LitigantGuideGenerator()
    generator.generate_guide()
