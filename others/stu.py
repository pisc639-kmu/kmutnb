import fitz
import json

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    data = []

    for i, page in enumerate(doc):
        text = page.get_text()
        data.append(page.get_text("dict"))
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    pdf_path = "student1.pdf"
    extract_text_from_pdf(pdf_path)
