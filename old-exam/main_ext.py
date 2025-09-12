import fitz
from PIL import Image
import pytesseract
import pyperclip
import time

def extract_text_from_pdf(pdf_path, lang='eng'):
    with fitz.open(pdf_path) as doc:
        # Get the first page
        page = doc.load_page(0)
        # Render page to an image
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # Cut the top left 25%
        img = img.crop((0, 0, int(img.width*(2/3)), int(img.height*(1/4))))
        # Use pytesseract to extract data
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        # data_str = pytesseract.image_to_string(img, lang=lang)
        # return (data, data_str)
        return data

def main(pdf_path: str):
    data = extract_text_from_pdf(pdf_path)
    out = []
    for i in range(len(data["text"])):
        if data["level"][i] == 5 and data["left"][i] < 350:
            if not ((data["left"][i] - data["left"][i - 1] < 50) or len(out) <= 1):
                break
            print(data["text"][i])
            if (len(out) != 0 or data["text"][i].isdigit() and len(data["text"][i]) > 4):
                out += [data["text"][i]]
    print(" ".join(out))

if __name__ == "__main__":
    while True:
        try:
            text = pyperclip.paste().strip()
            try:
                if text:
                    main(text)
                time.sleep(0.1)
            except:
                pass
        except KeyboardInterrupt:
            break
