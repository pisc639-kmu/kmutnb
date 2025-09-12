from PIL import Image, ImageGrab
import pytesseract
import pyperclip
import io
import time

# Set the path to the tesseract executable (if not in PATH)
# pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


while True:
    try:
        image = ImageGrab.grabclipboard()
        print(bool(pyperclip.paste()))
        # print(image)
        if image is not None:
            try:
                text = pytesseract.image_to_string(image)
                print(text)
            except Exception as e:
                print(f"Error processing clipboard content: {e}")
        time.sleep(0.5)
    except KeyboardInterrupt:
        break

