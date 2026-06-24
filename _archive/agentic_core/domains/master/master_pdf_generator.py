import os
from PyPDF2 import PdfWriter, PdfReader

def generate_ultimate_master_bundle():
    output_path = "outputs/GrandOperation_vInfinity/Master_Sovereign_Operation_vInfinity.pdf"
    merger = PdfWriter()

    # 1. C-Suite Certification (Cover)
    csuite = "outputs/GrandOperation_vInfinity/C_Suite_Certification_vInfinity.pdf"
    if os.path.exists(csuite): merger.append(csuite)

    # 2. Education Bundle
    edu_bundle = "outputs/education/sats_2026/deliverable/Norbury_School_SATs_Prep_Pack_2026.pdf"
    if os.path.exists(edu_bundle): merger.append(edu_bundle)

    # 3. CoE Validation
    coe = "outputs/education/sats_2026/CoE_Verification_Report_v19.1.pdf"
    if os.path.exists(coe): merger.append(coe)

    # 4. Law v19.1
    law_dir = "outputs/Law/EmploymentTribunal/v19.1_et1_clarification"
    law_files = [
        "ET1_v19.1_updated.pdf",
        "Hillingdon_Legal_Aid_Clarity_Letter_v19.1.pdf",
        "health_impact_timeline_v19.1.pdf",
        "Skeleton_Argument_Liability_v20.pdf",
        "Schedule_of_Loss_v20.pdf"
    ]
    for f in law_files:
        path = os.path.join(law_dir, f)
        if os.path.exists(path): merger.append(path)

    with open(output_path, "wb") as f:
        merger.write(f)

    print(f"ULTIMATE MASTER BUNDLE: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    generate_ultimate_master_bundle()
