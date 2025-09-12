from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import re
import pyperclip
import time
import os
import sys

# Set the path to the tesseract executable (if not in PATH)
# pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path, lang='eng+thai'):
    with fitz.open(pdf_path) as doc:
        # Get the first page
        page = doc.load_page(0)
        # Render page to an image
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # Cut the top left 25%
        img = img.crop((0, 0, int(img.width), int(img.height*(1/4))))
        # Use pytesseract to extract data
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        # data_str = pytesseract.image_to_string(img, lang=lang)
        # return (data, data_str)
        return data

# # Example usage
# pdf_path = r"D:\kmutnb\old-exam\2553\term 2\final\331361.pdf"
# data = extract_text_from_pdf(pdf_path)
# out = []
# for i in range(len(data["text"])):
#     if data["level"][i] == 5 and data["left"][i] < 350:
#         if not ((abs((data["left"][i] - data["left"][i - 1]) - data["width"][i - 1]) < 10) or len(out) <= 1):
#             break
#         print(data["text"][i], data["left"][i], data["width"][i], data["left"][i - 1], data["width"][i - 1])
#         if (len(out) != 0 or data["text"][i].isdigit() and len(data["text"][i]) > 4):
#             out += [data["text"][i]]
# print(" ".join(out))
# print(out)

# import json
# with open('pdf.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
# data = data.value()
# print(data)

# if __name__ == "__main__":
#     while True:
#         try:
#             command = input(">>> ")
#             if command == "exit": break
#             try:
#                 print(eval(command))
#             except SyntaxError:
#                 try:
#                     exec(command)
#                 except:
#                     import traceback
#                     traceback.print_exc()
#             except:
#                 import traceback
#                 traceback.print_exc()
#         except KeyboardInterrupt:
#             # print("^C")
#             print("\nKeyboardInterrupt")
#         except EOFError:
#             print("")
#             break

if __name__ == "__main__":
    old_clipboard = pyperclip.paste()
    while True:
        try:
            # print(data)
            # pdf_path = r"D:\kmutnb\old-exam\2553\term 2\final\331361.pdf"
            # pdf_path = input(">>> ")
            while pyperclip.paste().strip() in ["", old_clipboard]:
                time.sleep(0.01)
                # print("wait")
            old_clipboard = pyperclip.paste()
            pdf_path = pyperclip.paste()
            # print(pdf_path)
            data = extract_text_from_pdf(pdf_path)
            import json
            with open('pdf.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            out = []
            for i in range(len(data["text"])):
                if data["level"][i] == 5 and data["left"][i] < 3500:
                    print(data["text"][i], data["left"][i], data["top"][i], data["width"][i], data["height"][i], data["left"][i - 1], data["width"][i - 1])
                    if not ((abs((data["left"][i] - data["left"][i - 1]) - data["width"][i - 1]) < 30) or len(out) <= 1):
                        break
                    if (len(out) != 0 or data["text"][i].isdigit() and len(data["text"][i]) > 4):
                        out += [data["text"][i]]
            # while len(out) > 0:
            #     if out[0].isdigit() and len(out[0]) > 4:
            #         break
            #     else:
            #         out = out[1:]
            i = 0
            run = True
            while i < len(out) and run:
                if any(c in out[i] for c in ["ว", "ช", ":"]):
                    out = out[:i]
                    run = False
                else:
                    i += 1
            print(out)

            file_name = os.path.basename(pdf_path)

            if sys.argv[1] == "json":
                res = ",\n    \"" + os.path.basename(pdf_path).split(".")[0].split(" ")[0] + "\": \"" + " ".join(out[1:]) + "\""
                time.sleep(0.2)
                print(res)
                pyperclip.copy(res)
        except KeyboardInterrupt:
            # print("^C")
            print("\nKeyboardInterrupt")
            break
        except:
            # import traceback
            # traceback.print_exc()
            pass