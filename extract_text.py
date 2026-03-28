import os
from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF {pdf_path}: {e}"

def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Error extracting DOCX {docx_path}: {e}"

def main():
    input_dir = "inputs"
    output_dir = "extracted_text"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(filepath)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(filepath)
        else:
            continue

        output_filename = os.path.splitext(filename)[0] + ".txt"
        with open(os.path.join(output_dir, output_filename), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted: {filename}")

if __name__ == "__main__":
    main()
