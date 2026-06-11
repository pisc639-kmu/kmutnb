# import PIL
import pyperclip

import time
import sys
import os
from pathlib import Path
import re
# import subprocess
# import json

from PIL import Image
from PIL import ImageGrab
import pytesseract
# import fitz  # PyMuPDF

base_path = Path("D:\\kmutnb\\old-exam\\")

def wait_for_clipboard_change():
    global prev_clip_text, prev_clip_image
    prev_clip_text = pyperclip.paste()
    prev_clip_image = ImageGrab.grabclipboard()
    while True:
        try:
            current_clip_text = pyperclip.paste()
            current_clip_image = ImageGrab.grabclipboard()
            if current_clip_text != prev_clip_text or current_clip_image != prev_clip_image:
                prev_clip_text = current_clip_text
                prev_clip_image = current_clip_image
                if current_clip_image is not None:
                    # print("Image changed")
                    text = pytesseract.image_to_string(current_clip_image)
                    # pytesseract.image_to_data(current_clip_image, lang='eng')
                    pyperclip.copy(text.strip())
                    return text.strip()
                else:
                    return current_clip_text.strip()
            time.sleep(0.1)
        except KeyboardInterrupt:
            sys.exit()

def complete_query(query:str) -> str:
    query = re.sub(r'^"|"$|^\,|,\s*,', '', query)
    return query

def search_files(query, in_database=True):
    # found = False
    files = []
    first_file_opened = False
    # to_open = None
    if in_database:
        with open("files.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()[1:-1]
            for line in lines:
                print(line)
                try:
                    fpath = Path(base_path) / Path(eval(line[150:].split(",")[1]))
                    is_match = False
                    if complete_query(query) + '"' in line or query in fpath:
                        # print(f"\"{fpath}\"")
                        # if not first_file_opened:
                        files.append(fpath)
                        # first_file_opened = True
                        # found = True
                        # to_open = fpath
                except:
                    pass
        # webbrowser.open(first_file)
        # if to_open:
        #     webbrowser.open(to_open)
    else:
        for root, dirs, files in os.walk(base_path):
            root = Path(root)
            for file in files:
                file = Path(file)
                if query in root / file:
                    # print(f"\"{os.path.join(root, file)}\"")
                    # if not first_file_opened:
                    files.append(root / file)
                    # webbrowser.open(os.path.join(root, file))
                    # first_file_opened = True
                    found = True
                    to_open = os.path.join(root, file)
        # if to_open:
        #     webbrowser.open(to_open)
    return files

def file_is_ep(file_path):
    file_path = Path(file_path)
    if 'EP' in str(Path(file_path)).upper():
        return True
    elif re.search(r"^(?=.*ep|.*?\bS(?!1\b)\d+\b)", str(file_path), re.IGNORECASE):
        return True
    return False

def get_file_info(file_path):
    file_path = Path(file_path)
    res = {}
    res["name"] = file_path.stem
    res["ids"] = [int(i.strip()) for i in re.split(r'[,\s]+', file_path.stem) if i.strip() != "" and i.strip().isdigit()]
    res['year'] = int(Path(file_path).parts[3])
    res["term"] = (int(Path(file_path).parts[4][-1]), Path(file_path).parts[5][0])
    res['ep'] = file_is_ep(file_path)

    return res

def filter_file(file_path, term=None, period=None, ep=None):
    file_path = Path(file_path)
    file_info = get_file_info(file_path)
    if term is not None:
        # print(term, period)
        # print(file_info['term'])
        if str(file_info['term'][0]) != str(term):
            return False
    if period is not None:
        # print(2)
        if file_info['term'][1] != period:
            return False
    if ep is not None:
        # print(31)
        if file_info['ep'] != ep:
            return False
    return True

def filter_files(file_paths, term=None, period=None, ep=None):
    return [str(f) for f in file_paths if filter_file(f, term, period, ep)]

# first = True
# while True:
#     if first:
#         print("Waiting for search query...")
#         first = False
#     original_query = wait_for_clipboard_change()
#     query = re.sub(r'[\"\']', '', original_query).strip()
#     if query != "":
#         print(f"Detected search query: {query}")
#         found = search_files(query)
#         pyperclip.copy(found)
        
#         if found:
#             print("Search completed.")
#         else:
#             print(f"Cannot find file: {query}")
#         time.sleep(0.5)
#         pyperclip.copy(original_query)

# print(sys.argv)
term = sys.argv[1] if len(sys.argv) > 1 else None
period = sys.argv[2] if len(sys.argv) > 2 else None
ep = sys.argv[3].lower() == "ep" if len(sys.argv) > 3 else None
query = input("Enter search query: ").strip()
files = search_files(query, True)
print(files)
print(filter_files(files, term, period, ep))
print(term, period, ep)
print(get_file_info(files[0]) if files else "No files found")
print(filter_file(files[0], term, period, ep))