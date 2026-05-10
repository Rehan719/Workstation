import os
pdfs = [
    "outputs/education/sats_2026/predicted_questions/english_gps.pdf",
    "outputs/education/sats_2026/predicted_questions/english_reading.pdf",
    "outputs/education/sats_2026/predicted_questions/maths_arithmetic.pdf",
    "outputs/education/sats_2026/predicted_questions/maths_reasoning_1.pdf",
    "outputs/education/sats_2026/predicted_questions/maths_reasoning_2.pdf",
    "outputs/education/sats_2026/model_answers/english_gps_answers.pdf",
    "outputs/education/sats_2026/model_answers/english_reading_answers.pdf",
    "outputs/education/sats_2026/model_answers/maths_arithmetic_answers.pdf",
    "outputs/education/sats_2026/model_answers/maths_reasoning_1_answers.pdf",
    "outputs/education/sats_2026/model_answers/maths_reasoning_2_answers.pdf",
    "outputs/education/sats_2026/revision_schedule/schedule.pdf",
    "outputs/education/sats_2026/deliverable/Norbury_School_SATs_Prep_Pack_2026.pdf"
]
with open("pdf_verification_report.txt", "w") as f:
    for p in pdfs:
        exists = os.path.exists(p)
        size = os.path.getsize(p) if exists else 0
        f.write(f"{p}: {'OK' if exists and size > 0 else 'FAIL'} ({size} bytes)\n")
