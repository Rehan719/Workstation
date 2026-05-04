import os
from PyPDF2 import PdfWriter, PdfReader

def generate_ultimate_law_pack():
    output_path = "outputs/Law/EmploymentTribunal/v19.1_et1_clarification/Master_Law_Pack_v19.1.pdf"
    base_dir = "outputs/Law/EmploymentTribunal/v19.1_et1_clarification"
    merger = PdfWriter()

    files = [
        "Hillingdon_Letter_v19.1_Ultimate_Final.pdf",
        "ET1_v19.1_Ultimate_Final.pdf",
        "health_impact_timeline_v19.1.pdf",
        "Skeleton_Argument_Liability_v20.pdf",
        "Schedule_of_Loss_v20.pdf",
        "incident_evidence_matrix_v19.md" # Table version if PDF not available
    ]

    for f in files:
        path = os.path.join(base_dir, f)
        if os.path.exists(path) and path.endswith(".pdf"):
            merger.append(path)

    with open(output_path, "wb") as f:
        merger.write(f)

    print(f"ULTIMATE LAW PACK: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    generate_ultimate_law_pack()
