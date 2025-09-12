import csv
import json
import os
import pathlib
import PIL.ImageGrab
import pyperclip
import pytesseract
import re
import subprocess
import sys
import time
import webbrowser

import pandas as pd
import PIL

all_path = "D:\\kmutnb\\old-exam\\"

class File:
    file_path: str
    name: str
    sizeint: int

    @property
    def file_path(self) -> str:
        """Path to the file without the base directory"""
        return self._path

    @property
    def name(self) -> str:
        """File name without the directory"""
        return os.path.basename(self.file_path)

    @property
    def subject_ids(self) -> tuple[str, ...]:
        """Tuple of subject IDs found in the file name"""
        return tuple(map(str, re.findall(r"\d{5,}", self.name)))

    @property
    def sizeint(self) -> int:
        """File size in bytes"""
        return os.path.getsize(self._full_path)

    @property
    def sizestr(self) -> str:
        """File size in human-readable format"""
        return add_size_unit(self.sizeint)

    @property
    def year(self) -> int | None:
        """Year of the exam, if available"""
        year = self._year
        if year is None:
            return None
        if year > 2400:
            return year - 543
        return year

    @property
    def term(self) -> int | None:
        """Term of the exam, if available"""
        return self._term

    @property
    def exam(self) -> str | None:
        """Exam type, if available"""
        return self._exam

    def __init__(self, file_path, full_path=None):
        self._path = file_path
        self._full_path = full_path
        self._year = None
        self._term = None
        self._exam = None
        parts = pathlib.Path(file_path).parts
        if len(parts) >= 3:
            try:
                self._year = int(re.findall(r"\d+", parts[0])[0])
                self._term = int(re.findall(r"\d+", parts[1])[0])
                self._exam = re.findall(r"[a-z]+", parts[2])[0]
            except IndexError:
                # print("error")
                # import traceback
                # traceback.print_exc()
                # raise
                pass
            except:
                import traceback
                traceback.print_exc()
                raise

def remove_filename(path, fname, recursive=False):
    for root, dirs, files in os.walk(path):
        if fname in files:
            os.remove(os.path.join(root, fname))
        if not recursive:
            break

def add_gdrive_folder_icon(path):
    "add google drive folder icon to the folder by inserting desktop.ini"
    if not os.path.exists(path):
        print(f"Folder '{path}' not found")
        return
    try:
        # if not os.path.exists(os.path.join(path, "desktop.ini")):
        with open(os.path.join(path, "desktop.ini"), "w") as f:
            f.write("[.ShellClassInfo]\nConfirmFileOp=0\nIconResource=C:\\Program Files\\Google\\Drive File Stream\\110.0.3.0\\GoogleDriveFS.exe,26")
        subprocess.run(["attrib", "+h", "+s", os.path.join(path, "desktop.ini")], check=True)
        subprocess.run(["attrib", "+r", os.path.basename(path)], check=True, cwd=os.path.dirname(path))
    except PermissionError:
        print(f"Permission denied for file '{os.path.join(path, 'desktop.ini')}'")
        return

def add_gdrive_folder_icon_recursive(path, recursive=False):
    "add google drive folder icon to the folder recursively by inserting desktop.ini"
    if not os.path.exists(path):
        print(f"Folder '{path}' not found")
        return
    add_gdrive_folder_icon(path)
    if recursive:
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                add_gdrive_folder_icon(os.path.join(root, dir))

# def remove_filename(path, fname):
#     return os.path.dirname(path)

def get_files(path, file_extension=None):
    lst = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file != "desktop.ini":
                if file_extension is None or pathlib.Path(file).suffix[1:] == file_extension:
                    lst.append(os.path.relpath(os.path.join(root, file), all_path))
    return lst

def prettify_csv_fixed_width(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8', newline='') as infile:
        rows = [re.split(r'(?<!\\),', line.strip()) for line in infile]

    if not rows:
        return

    # Determine maximum width for each column
    column_widths = [max(len(str(item)) for item in col) for col in zip(*rows)]

    with open(output_filename, 'w', encoding='utf-8', newline='') as outfile:
        for row in rows:
            formatted_row = [
                re.sub(r"(.*[^\s])(\s*)$", "\"\\1\"\\2", str(item).ljust(column_widths[i])).replace('\\,', ',') if i in [0, 5, 6] else str(item).ljust(column_widths[i])
                # item if i in [0, 5] else str(item).ljust(column_widths[i])
                for i, item in enumerate(row)
            ]
            outfile.write(','.join(formatted_row) + '\n')

def add_size_unit(size_bytes):
    """
    Returns the size of a file in a human-readable format (e.g., KB, MB, GB).
    """
    if size_bytes == 0:
        return "0 Bytes"

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {units[i]}"

def get_human_readable_size(file_path):
    """
    Returns the size of a file in a human-readable format (e.g., KB, MB, GB).
    """
    try:
        size_bytes = os.path.getsize(file_path)
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {e}"

    return add_size_unit(size_bytes)

def wait_for_clipboard_change():
    global prev_clip_text, prev_clip_image
    prev_clip_text = pyperclip.paste()
    prev_clip_image = PIL.ImageGrab.grabclipboard()
    while True:
        try:
            current_clip_text = pyperclip.paste()
            current_clip_image = PIL.ImageGrab.grabclipboard()
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

def search_files(query):
    found = False
    first_file = ""
    first_file_opened = False
    for root, dirs, files in os.walk(all_path):
        for file in files:
            if query in os.path.join(root, file):
                print(f"Found file: \"{os.path.join(root, file)}\"")
                if not first_file_opened:
                    first_file = os.path.join(root, file)
                    webbrowser.open(os.path.join(root, file))
                    first_file_opened = True
                found = True
    return first_file

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1].lower().strip()
        query = re.sub(r'[\"\']', '', query).strip()
        if query == "auto":
            while True:
                original_query = wait_for_clipboard_change()
                query = re.sub(r'[\"\']', '', original_query).strip()
                if query != "":
                    print(f"Detected search query: {query}")
                    found = search_files(query)
                    pyperclip.copy(found)
                    
                    if found:
                        print("Search completed.")
                    else:
                        print(f"Cannot find file: {query}")
                    time.sleep(0.5)
                    pyperclip.copy(original_query)
        else:
            found = search_files(query)
            if found:
                print("Search completed.")
            else:
                print(f"Cannot find file: {query}")
    else:
        # add_gdrive_folder_icon_recursive(all_path, recursive=True)
        remove_filename(all_path, "desktop.ini", recursive=True)
        files = get_files(all_path, file_extension="pdf")
        with open("subjects.json", "r", encoding="utf-8") as f:
            subjects = json.load(f)
        subjects = dict(sorted(subjects.items()))
        with open("subjects.json", "w", encoding="utf-8") as f:
            json.dump(subjects, f, indent=4, ensure_ascii=False)
        with open("files.csv", "w", encoding="utf-8", newline="") as f:
            # writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            # writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar="\\")
            # writer.writerow(["filename", "year", "term", "exam", "subject_id", "fullpath", "size"])
            f.write("filename,year,term,exam,subject_id,subject_name,fullpath,size\n")
            total_size = 0

            # Make File objects
            files = [File(file, full_path=os.path.join(all_path, file)) for file in files]

            # Sort files by year, term, exam, and file name
            files.sort(key=lambda x: (x.year, x.term, x.exam, x.name))

            decode = lambda x: x.encode('unicode_escape').decode('latin1').replace(',', '\\,')
            # decode = lambda x: x.encode('unicode_escape').decode('latin1')

            # Write to CSV file and calculate total size
            for file in files:
                # try:
                # try:
                #     writer.writerow([file.name, file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)), file.file_path, file.sizestr])
                # except UnicodeEncodeError:
                #     writer.writerow([file.name.encode('utf-8'), file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)).encode('utf-8'), file.file_path.encode('utf-8'), file.sizestr])

                # try:
                #     writer.writerow([f'"{file.name}"', file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)), f'"{file.file_path}"', file.sizestr])
                # except UnicodeEncodeError:
                #     writer.writerow([f'"{file.name}"'.encode('utf-8'), file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)).encode('utf-8'), f'"{file.file_path}"'.encode('utf-8'), file.sizestr])
                
                row = [decode(file.name), file.year, file.term, file.exam, "|".join(map(str, file.subject_ids)), subjects[str(file.subject_ids[0])] if str(file.subject_ids[0] if len(file.subject_ids) else "-") in subjects.keys() else "None", decode(file.file_path), file.sizestr]
                # row[0] = f'"{row[0]}"'
                # row[5] = f'"{row[5]}"'
                # writer.writerow(row)
                row = map(lambda x: x if x != "None" else "", row)
                row = map(str, row)
                f.write(",".join(row) + "\n")
                
                # print(file.file_path)
                total_size += file.sizeint

        print(f"Total files: {len(files)}")
        # print(f"Total storage: {total_size:,} Byte ({total_size / 1024 / 1024:.4f} MB)")
        print(f"Total storage: {total_size:,} Byte ({add_size_unit(total_size)})")
        prettify_csv_fixed_width("files.csv", "files.csv")

if __name__ == "__main__":
    main()

