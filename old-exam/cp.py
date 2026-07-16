import sys
import os
import re
import json
from pypdf import PdfWriter
from pathlib import Path
from typing import Union
import shutil


paths_string = r"""
D:\kmutnb\old-exam\2555\term 2\midterm\394174.pdf
D:\kmutnb\old-exam\2556\term 2\midterm\ep\394174 ep.pdf
D:\kmutnb\old-exam\2557\term 2\midterm\394174 ep.pdf
D:\kmutnb\old-exam\2558\term 2\midterm\394174 ep.pdf
D:\kmutnb\old-exam\2560\term 2\midterm\6 mar 61\ep\394174.pdf
D:\kmutnb\old-exam\2561\term 2\midterm\ep\394174.pdf
D:\kmutnb\old-exam\2562\term 2\midterm\21 jan 63\ep\394174.pdf
D:\kmutnb\old-exam\2567\term 2\midterm\031001134 s15-18.pdf
D:\kmutnb\old-exam\2568\term 2\midterm\031001134 s15-17.pdf

D:\kmutnb\old-exam\2555\term 2\midterm\392154.pdf
D:\kmutnb\old-exam\2556\term 2\midterm\ep\392154 ep.pdf
D:\kmutnb\old-exam\2557\term 2\midterm\392154 ep.pdf
D:\kmutnb\old-exam\2558\term 2\midterm\392154 ep.pdf
D:\kmutnb\old-exam\2560\term 2\midterm\7 mar 61\ep\392154.pdf
D:\kmutnb\old-exam\2561\term 2\midterm\ep\392154.pdf
D:\kmutnb\old-exam\2562\term 2\midterm\22 jan 63\ep\392154-1.pdf
D:\kmutnb\old-exam\2562\term 2\midterm\22 jan 63\ep\392154-2.pdf
D:\kmutnb\old-exam\2567\term 2\midterm\031001124 s15-18.pdf
D:\kmutnb\old-exam\2568\term 2\midterm\031001124 s15-17.pdf
"""
department = "ee"
term_code = "1-1-m"

term = "-".join(term_code.split("-")[:2])
with open("subjects.json", "r", encoding="utf-8") as f:
    subjects_json = json.load(f)

with open("subjects.min.json", "r", encoding="utf-8") as f:
    subjects = json.load(f)
subjects = subjects[department]
subjects = subjects[term]

def merge(inputs, output):
    merger = PdfWriter()

    for pdf in inputs:
        merger.append(pdf)

    merger.write(output)
    merger.close()

    print(f"Merged {len(inputs)} files into '{output}'")

def copy(from_path: Union[str, Path], to_path: Union[str, Path]):
    Path(to_path).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(from_path, to_path)

id_split_regex = re.compile(r'\\([^\.\\\-\s]+)[^\\]*$')
def get_id(path):
    # return path.split("\\")[-1].split(".")[0].split(" ")[0].split("-")[0]
    return id_split_regex.search(path).group(1)

def main():
    path_regex = re.compile(r'([a-zA-Z]+:\\(?:[^\\/:*?"<>|\r\n]+\\)*.*?(?=\s+[a-zA-Z]+:\\|$))')
    paths = paths_string.strip().split("\n")
    dest = Path(os.path.expandvars("%onedrive%")) / "KMU" / "old-exam" / department / term_code
    # subject = "Math1"
    # path = map(Path, path)
    for path in paths:
        if not path_regex.match(path):
            continue
        path = path_regex.findall(path)
        if len(path) == 0:
            continue
        
        if (subject_id := get_id(path[0])) in subjects:
            subject = subjects[subject_id]
        else:
            subject = subject_id

        year = int(Path(path[0]).parts[3]) - 543
        file_name = Path(f"{subject} {year}.pdf")
        if len(path) == 1:
            path = path[0]
            copy(path, dest / file_name)
            print(f"Copied {path} to {dest / file_name}")
        else:
            merge(path, dest / file_name)
            print(f"Merged ({', '.join(path)}){len(path)} files into {dest / file_name}")

if __name__ == "__main__":
    main()
