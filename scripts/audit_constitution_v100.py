import os
import sys
import logging

def audit_constitution():
    constitution_path = "CONSTITUTION_v100.0.0.md"
    if not os.path.exists(constitution_path):
        print("FAIL: CONSTITUTION_v100.0.0.md missing")
        return False

    with open(constitution_path, "r") as f:
        content = f.read()

    mandates = [
        "ARTICLE 298: SCIENTIFIC RESEARCH",
        "ARTICLE 303: DIGITAL TWINNING",
        "ARTICLE 304: ENVIRONMENTAL SIMULATION ENGINE",
        "ARTICLE 305: ADAPTIVE RESOURCE OPTIMIZATION",
        "ARTICLE 306: DYNAMIC ASSEMBLE/DISASSEMBLE",
        "ARTICLE 307: BIOMIMETIC TEAM DYNAMICS",
        "ARTICLE 310: ZERO-COST INVIOLABILITY",
        "ARTICLE 311: RESOURCE ASSEMBLY LANGUAGE"
    ]

    passed = True
    for m in mandates:
        if m in content:
            print(f"PASS: {m} codified.")
        else:
            print(f"FAIL: {m} NOT found in Constitution.")
            passed = False
    return passed

if __name__ == "__main__":
    if audit_constitution():
        print("\nConstitutional Audit: SUCCESS")
        sys.exit(0)
    else:
        print("\nConstitutional Audit: FAILED")
        sys.exit(1)
