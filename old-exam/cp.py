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

with open("subjects.min.json", "r", encoding="utf-8") as f:
    subjects = json.load(f)
subjects = subjects["cb"]
subjects = subjects["1-2"]

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

D:\kmutnb\old-exam\2553\term 2\final\394172.pdf
D:\kmutnb\old-exam\2554\term 2\final\394172.pdf
D:\kmutnb\old-exam\2555\term 2\final\394172.pdf
D:\kmutnb\old-exam\2556\term 2\final\394172.pdf
D:\kmutnb\old-exam\2557\term 2\final\394172.pdf
D:\kmutnb\old-exam\2560\term 2\final\16 may 61\394172.pdf
D:\kmutnb\old-exam\2561\term 2\final\394172.pdf
D:\kmutnb\old-exam\2562\term 2\final\5 mar 63\394172.pdf
D:\kmutnb\old-exam\2567\term 2\final\031001132 s1-14.pdf
D:\kmutnb\old-exam\2568\term 2\final\031001132 s1-14.pdf

D:\kmutnb\old-exam\2553\term 2\final\394174.pdf
D:\kmutnb\old-exam\2554\term 2\final\394174.pdf
D:\kmutnb\old-exam\2555\term 2\final\394174.pdf
D:\kmutnb\old-exam\2556\term 2\final\394174.pdf
D:\kmutnb\old-exam\2557\term 2\final\394174.pdf
D:\kmutnb\old-exam\2560\term 2\final\17 may 61\394174.pdf
D:\kmutnb\old-exam\2561\term 2\final\394174.pdf
D:\kmutnb\old-exam\2567\term 2\final\031001134 s1-14.pdf
D:\kmutnb\old-exam\2568\term 2\final\031001134 s1-14.pdf

D:\kmutnb\old-exam\2553\term 2\final\393162.pdf
D:\kmutnb\old-exam\2554\term 2\final\393162.pdf
D:\kmutnb\old-exam\2555\term 2\final\393162.pdf
D:\kmutnb\old-exam\2556\term 2\final\393162.pdf
D:\kmutnb\old-exam\2557\term 2\final\393162.pdf
D:\kmutnb\old-exam\2560\term 2\final\15 may 61\393162.pdf
D:\kmutnb\old-exam\2561\term 2\final\393162.pdf
D:\kmutnb\old-exam\2562\term 2\final\9 mar 63\393162.pdf
D:\kmutnb\old-exam\2567\term 2\final\031001152 s1-18.pdf
D:\kmutnb\old-exam\2568\term 2\final\031001152 s1-14.pdf

D:\kmutnb\old-exam\2553\term 2\final\393142.pdf
D:\kmutnb\old-exam\2554\term 2\final\393142.pdf
D:\kmutnb\old-exam\2555\term 2\final\393142.pdf
D:\kmutnb\old-exam\2556\term 2\final\393142.pdf
D:\kmutnb\old-exam\2557\term 2\final\393142.pdf
D:\kmutnb\old-exam\2560\term 2\final\21 may 61\393142.pdf
D:\kmutnb\old-exam\2561\term 2\final\393142.pdf
D:\kmutnb\old-exam\2562\term 2\final\6 mar 63\393142.pdf
D:\kmutnb\old-exam\2567\term 2\final\031001142 s1-14.pdf
D:\kmutnb\old-exam\2568\term 2\final\031001142 s1-17.pdf

D:\kmutnb\old-exam\2553\term 2\final\395181.pdf
D:\kmutnb\old-exam\2554\term 2\final\395181.pdf
D:\kmutnb\old-exam\2555\term 2\final\395181.pdf
D:\kmutnb\old-exam\2556\term 2\final\395181.pdf
D:\kmutnb\old-exam\2557\term 2\final\395181.pdf
D:\kmutnb\old-exam\2560\term 2\final\16 may 61\395181.pdf
D:\kmutnb\old-exam\2562\term 2\final\9 mar 63\395181.pdf
D:\kmutnb\old-exam\2567\term 2\final\031001161 s1-14.pdf
D:\kmutnb\old-exam\2568\term 2\final\031001161 s1-14.pdf

""".strip().split("\n")
    dest = Path(os.path.expandvars("%onedrive%")) / "KMU" / "old-exam" / "cb" / "1-2-f"
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
