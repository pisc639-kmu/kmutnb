import sys
import os
import re
import json
from pypdf import PdfWriter
from pathlib import Path
from typing import Union
import shutil


paths_string = r"""
D:\kmutnb\old-exam\2555\term 1\final\394171.pdf
D:\kmutnb\old-exam\2556\term 1\final\394171.pdf
D:\kmutnb\old-exam\2557\term 1\final\394171.pdf
D:\kmutnb\old-exam\2558\term 1\final\394171.pdf
D:\kmutnb\old-exam\2560\term 1\final\394171.pdf
D:\kmutnb\old-exam\2561\term 1\final\27 nov 2561\27 nov 61\394171.pdf
D:\kmutnb\old-exam\2562\term 1\final\394171.pdf
D:\kmutnb\old-exam\2563\term 1\final\28 oct 63\394171.pdf
D:\kmutnb\old-exam\2567\term 1\final\031001131 s1-14.pdf
D:\kmutnb\old-exam\2568\term 1\final\031001131 s1-14.pdf

D:\kmutnb\old-exam\2556\term 1\final\394173.pdf
D:\kmutnb\old-exam\2557\term 1\final\394173.pdf
D:\kmutnb\old-exam\2558\term 1\final\394173.pdf
D:\kmutnb\old-exam\2560\term 1\final\394173.pdf
D:\kmutnb\old-exam\2561\term 1\final\28 nov 61\394173.pdf
D:\kmutnb\old-exam\2562\term 1\final\394173.pdf
D:\kmutnb\old-exam\2563\term 1\final\27 oct 63\394173.pdf
D:\kmutnb\old-exam\2567\term 1\final\031001133 s1-14.pdf
D:\kmutnb\old-exam\2568\term 1\final\031001133 s1-14.pdf

D:\kmutnb\old-exam\2555\term 1\final\393141.pdf
D:\kmutnb\old-exam\2556\term 1\final\393141.pdf
D:\kmutnb\old-exam\2557\term 1\final\393141.pdf
D:\kmutnb\old-exam\2558\term 1\final\393141.pdf
D:\kmutnb\old-exam\2560\term 1\final\393141.pdf
D:\kmutnb\old-exam\2561\term 1\final\30 nov 61\393141.pdf
D:\kmutnb\old-exam\2562\term 1\final\393141.pdf
D:\kmutnb\old-exam\2563\term 1\final\26 oct 63\393141.pdf
D:\kmutnb\old-exam\2567\term 1\final\031001141 s1-14.pdf
D:\kmutnb\old-exam\2568\term 1\final\031001141 s1-17.pdf

D:\kmutnb\old-exam\2555\term 1\final\392131.pdf
D:\kmutnb\old-exam\2556\term 1\final\392131.pdf
D:\kmutnb\old-exam\2557\term 1\final\392131.pdf
D:\kmutnb\old-exam\2558\term 1\final\392131.pdf
D:\kmutnb\old-exam\2560\term 1\final\392131.pdf
D:\kmutnb\old-exam\2561\term 1\final\28 nov 61\392131.pdf
D:\kmutnb\old-exam\2562\term 1\final\392131.pdf
D:\kmutnb\old-exam\2563\term 1\final\29 oct 63\392131.pdf
D:\kmutnb\old-exam\2567\term 1\final\031001111 s1-14.pdf
D:\kmutnb\old-exam\2568\term 1\final\031001111 s1-14.pdf

D:\kmutnb\old-exam\2556\term 1\final\393161.pdf
D:\kmutnb\old-exam\2557\term 1\final\393161.pdf
D:\kmutnb\old-exam\2558\term 1\final\393161.pdf
D:\kmutnb\old-exam\2560\term 1\final\393161.pdf
D:\kmutnb\old-exam\2561\term 1\final\26 nov 2561\393161.pdf
D:\kmutnb\old-exam\2563\term 1\final\30 oct 63\393161.pdf
D:\kmutnb\old-exam\2567\term 1\final\031001151 s1-18.pdf
D:\kmutnb\old-exam\2568\term 1\final\031001151 s1-14.pdf
"""
department = "cb"
term_code = "1-1-f"
from_onedrive = True

if from_onedrive:
    paths_string = paths_string.replace(r"D:\kmutnb\old-exam", r"C:\Users\pisc639\OneDrive\KMU\old-exam\raw")

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

        print(Path(path[0]))

        year = int(Path(path[0]).parts[7 if from_onedrive else 3]) - 543
        print(year)
        if year in [2015]:
            continue
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
