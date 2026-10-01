import pymupdf
import os


def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


resume_folder = "data/resumes"

for filename in os.listdir(resume_folder):

    if filename.lower().endswith(".pdf"):

        pdf_path = os.path.join(resume_folder, filename)

        print("\n" + "=" * 50)
        print(f"FILE: {filename}")
        print("=" * 50)

        resume_text = extract_text_from_pdf(pdf_path)

        print(resume_text)