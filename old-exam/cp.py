import sys
import os
import re
import json
from pypdf import PdfWriter
from pathlib import Path
from typing import Union
import shutil

with open("subjects.json", "r", encoding="utf-8") as f:
    subjects_json = json.load(f)

subjects = {
    "394171": "Math1",
    "031001131": "Math1",
    "394173": "Math3",
    "031001133": "Math3",
    "393141": "English",
    "031001141": "English",
    "392131": "Physics",
    "031001111": "Physics",
    "393161": "Thai",
    "031001151": "Thai",
}

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

def get_id(path):
    return path.split("\\")[-1].split(".")[0].split(" ")[0]

def main():
    path_regex = re.compile(r'([a-zA-Z]+:\\(?:[^\\/:*?"<>|\r\n]+\\)*.*?(?=\s+[a-zA-Z]+:\\|$))')
    paths = r"""

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

""".strip().split("\n")
    dest = Path(os.path.expandvars("%onedrive%")) / "KMU" / "old-exam" / "cb" / "1-1-f"
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
            print(f"Merged ({path.join(', ')}){len(path)} files into {dest / file_name}")

if __name__ == "__main__":
    main()
