import json
import sys
import os
from pathlib import Path
import re
import ast

import discord

base_path = Path("D:\\kmutnb\\old-exam\\")

def create_regex_replacer(mapping):
    """Generates a function that replaces regex patterns based on a mapping dict.
    Automatically applies case-insensitivity and word boundaries around all patterns.
    """
    # Flatten mapping into a list of (pattern, target) tuples
    flat = [(p, t) for t, src in mapping.items() for p in ([src] if isinstance(src, str) else src)]
    
    # Map group names like 'g0', 'g1' to targets
    group_to_target = {f"g{i}": target for i, (_, target) in enumerate(flat)}
    
    # Inject word boundaries \b around every sub-pattern and compile with re.IGNORECASE
    master_regex = re.compile(
        "|".join(f"(?P<g{i}>\\b{p}\\b)" for i, (p, _) in enumerate(flat)), 
        flags=re.IGNORECASE
    )
    
    # Return the dynamic replacer function
    return lambda text: master_regex.sub(
        lambda m: next(group_to_target[k] for k, v in m.groupdict().items() if v is not None and k in group_to_target), 
        text
    )

mapping = {
    # 1. Roman Numerals Standardizations
    "i": "1",
    "ii": "2",
    "iii": "3",
    "iv": "4",
    "v": "5",
    "vi": "6",
    
    # 2. Main Course Subjects
    "mathematics": [r"math(s)?", r"mathe?"],
    "mechanics": [r"phys(ics)?", r"mech(anics)?"],
    "chemistry": r"chem(istry)?",
    "computer": r"comp(ut)?",
    
    # 3. Common Context Modifiers & Abbreviations
    "engineering": r"eng(ineer)?",
    "introduction to": r"intro(duction)?",
    "fundamental": r"fund(amental)?",
    "systems": "sys",
    "materials": "mat",
    "communicative": "comm",
    "programming": "prog",
    
    # 4. Computer-aided acronym extensions
    "computer-aided design": "cad",
    "computer-aided manufacturing": "cam",

    # 5. Popular Course Abbreviations
    "electrical": "elect?r?i?c?a?l?",
    "phenomena": "pheno?m?e?n?a?",
    "drawing": "draw?",
}

# # Example usage:
# standardize_text = create_regex_replacer(mapping)
# print(standardize_text("i need help with Mech 1 and Eng Materials")) 
# # Output: mechanics i and engineering materials

replacer = create_regex_replacer(mapping)
def standardize_text(query:str):
    return replacer(query)

def format_query(query:str, removequotes=True) -> str:
    
    query = query.lower().strip()
    if removequotes:
        query = re.sub(r'^"|".{0,2}$|^\,|,\s*,?', '', query)
    else:
        query = re.sub(r'^\,|,\s*,?', '', query)
    return query

def search_files(query:str, in_database=True, limit=250):
    files = []
    length = 0  
    if in_database:
        with open(Path(__file__).parent.parent.parent.parent / "files.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()[1:-1]
            # print(len(lines))
            for line in lines:
                line = line.lower()
                # print(line)
                try:
                    fpath = Path(base_path) / Path(ast.literal_eval(re.search(r"\"[^\"]+\"", line[150:]).group(0)))
                    is_match = False

                    if re.sub(r"[\'\"]+", '"', (format_query(query, removequotes=False) + '"')) in line or query in str(fpath):
                        is_match = True
                    
                    # print(query, line)
                    if format_query(query).isdigit() and format_query(query) in line:
                        is_match = True
                        # print(1)

                    if is_match:
                        files.append(str(fpath))
                        length += 1
                        if length >= limit:
                            break
                except:
                    import traceback
                    traceback.print_exc()
                    sys.exit()
    else:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if query in os.path.join(root, file):
                    print(f"\"{os.path.join(root, file)}\"")
                    files.append(os.path.join(root, file))
                    length += 1
                    if length >= limit:
                        break
    return files

def file_is_ep(file_path):
    file_path = Path(file_path)
    if 'EP' in str(Path(file_path)).upper():
        return 1 # EP
    elif re.search(r"^(?=.*ep|.*?\bS(?!1\b)\d+\b)", str(file_path), re.IGNORECASE):
        return 1 # EP
    elif re.search(r"^(?!.*ep)(?!.*?\bs\d+\b).*$", str(file_path), re.IGNORECASE):
        return 2 # Not Sure
    return 0 # Not EP

def get_file_info(file_path):
    file_path = Path(file_path)
    res = {}
    res["path"] = str(file_path)
    res["name"] = file_path.stem
    res["ids"] = [int(i.strip()) for i in re.split(r'[,\.\s]+', file_path.stem) if i.strip() != "" and i.strip().isdigit()]
    res["id"] = res["ids"][0] if res["ids"] else None

    with open(Path(__file__).parent.parent.parent.parent / "subjects.json", "r", encoding="utf-8") as f:
        subjects_json = json.load(f)
        res["subject"] = subjects_json.get(str(res["ids"][0]), "Unknown") if res["ids"] else "Unknown"
    try:
        res['year'] = int(Path(file_path).parts[3])
    except (ValueError, IndexError):
        print(file_path)

    res["term"] = (int(Path(file_path).parts[4][-1]), Path(file_path).parts[5][0])
    res["term_full"] = "final" if res["term"][1].lower() == "f" else "midterm" if res["term"][1].lower() == "m" else "unknown"
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
        if bool(file_info['ep']) != ep and file_info['ep'] != 2:
            return False
    return True

def filter_files(file_paths, term=None, period=None, ep=None):
    return [str(f) for f in file_paths if filter_file(f, term, period, ep)]

def search(query:str, term:int=None, period:str=None, ep:bool=None, as_json=False):
    try:
        print(f"Options: term={term}, period={period}, ep={ep}")
        print(f"Searching for: {query}")

        # print(query.isdigit())
        query = standardize_text(query)
        files = search_files(query)
        files = filter_files(files, term, period, ep)
        if as_json:
            files = [get_file_info(f) for f in files]
        return files
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e

class DownloadButton(discord.ui.Button):
    def __init__(self, file_path: str, custom_file_name: str = None):
        super().__init__(label="Download", style=discord.ButtonStyle.primary)
        self.file_path = file_path
        self.custom_file_name = custom_file_name

    async def callback(self, interaction: discord.Interaction):
        print(f"Downloading file from: {self.file_path}")
        # Handle the download logic here
        # await interaction.response.send_message(f"Downloading file from: {self.file_path}", ephemeral=True)
        if self.custom_file_name:

            file = discord.File(self.file_path, filename=self.custom_file_name)
        else:
            file = discord.File(self.file_path)
        loading_message = await interaction.response.send_message(f"Uploading {file.filename}")
        print(f"Uploading file: {file.filename}")
        try:
            await interaction.edit_original_response(content=f"Uploaded {file.filename}", attachments=[file])
            # when timed out
        except discord.errors.NotFound:
            await interaction.message.reply(file=file)
        print(f"Uploaded file: {file.filename}")

class ErrorView(discord.ui.LayoutView):
    def __init__(self, keyword: str, error_message: str):
        super().__init__()
        self.error_message = error_message
        self.keyword = keyword

        self.main_container = discord.ui.Container()
        self.text_head = discord.ui.TextDisplay(
            "## Old Exam Search\n"
            f"Search Query: `{self.keyword}`"
        )
        
        self.seperator = discord.ui.Separator(
            spacing=discord.SeparatorSpacing.large, 
            visible=True
        )

        self.main_container.add_item(self.text_head)
        self.main_container.add_item(self.seperator)

        self.main_container.add_item(discord.ui.TextDisplay(error_message))

        self.main_container.add_item(self.seperator)

        self.add_item(self.main_container)

class SearchLayoutView(discord.ui.LayoutView):
    def __init__(self, keyword: str):
        super().__init__()
        self.page = 1
        self.results_per_page = 9
        self.keyword = keyword

        self.results = search(keyword, as_json=True)
        if self.results is None or len(self.results) == 0:
            error_message = f"No results found for the keyword: {self.keyword}"
            self.add_item(ErrorView(keyword=self.keyword, error_message=error_message))
        else:
            self.total_pages = min(25, (len(self.results) // self.results_per_page) + (1 if len(self.results) % self.results_per_page > 0 else 0))

            self.main_container = discord.ui.Container()
            self.make_view()

    def make_view(self):
        self.clear_items()
        self.main_container.clear_items()

        self.text_head = discord.ui.TextDisplay(
            "## Old Exam Search\n"
            "Search Query: `" + self.keyword.replace('`', '\\`') + "`"
        )
        
        self.seperator = discord.ui.Separator(
            spacing=discord.SeparatorSpacing.large, 
            visible=True
        )

        self.main_container.add_item(self.text_head)
        self.main_container.add_item(self.seperator)

        for result in self.results[(self.page - 1) * self.results_per_page : self.page * self.results_per_page]:
            download_btn = DownloadButton(
                file_path=result['path'],

                custom_file_name=f"{result['subject'] if result['subject'] != 'Unknown' else result['id']}{' EP' if result['ep'] == 1 else '' if result['ep'] == 0 else ''} - {result['year'] - 543}.pdf"
            )
            section = discord.ui.Section(
                accessory=download_btn
            )
            section.add_item(
                discord.ui.TextDisplay(f"**{result['subject'] if result['subject'] != 'Unknown' else result['id']}** - {result['year'] - 543} - Term {result['term'][0]} {result['term_full']} - {'EP' if result['ep'] == 1 else 'Not EP' if result['ep'] == 0 else 'Not Sure'}")
            )
            self.main_container.add_item(section)

        self.main_container.add_item(self.seperator)

        # Page Navigation Row
        page_row = discord.ui.ActionRow()
        
        left_button = discord.ui.Button(
            label="<", 
            style=discord.ButtonStyle.primary, 
            custom_id="btn_left"
        )
        if self.page <= 1:
            left_button.disabled = True
        left_button.callback = self.left_button_callback
        page_row.add_item(left_button)

        page_text = discord.ui.Button(
            label=f"Page {self.page} of {self.total_pages}",
            style=discord.ButtonStyle.secondary,
            custom_id="btn_page_text",
        )
        page_text.callback = self.page_text_callback
        page_row.add_item(page_text)

        right_button = discord.ui.Button(
            label=">", 
            style=discord.ButtonStyle.primary, 
            custom_id="btn_right"
        )
        if self.page >= self.total_pages:
            right_button.disabled = True
        right_button.callback = self.right_button_callback
        page_row.add_item(right_button)

        # Select Dropdown Row
        select_row = discord.ui.ActionRow()

        page_select = discord.ui.Select(
            placeholder=f"Page {self.page} of {self.total_pages}",
            # Pass explicit values to make parsing safer in the callback
            options=[discord.SelectOption(label=f"Page {i+1}", value=str(i+1)) for i in range(self.total_pages)],
            custom_id="btn_page",
        )
        page_select.callback = self.page_select_callback
        select_row.add_item(page_select)

        self.main_container.add_item(page_row)
        self.main_container.add_item(select_row)

        self.add_item(self.main_container)

    async def left_button_callback(self, interaction: discord.Interaction):
        self.page -= 1
        self.make_view()
        await interaction.response.edit_message(view=self)

    async def right_button_callback(self, interaction: discord.Interaction):
        self.page += 1
        self.make_view()
        await interaction.response.edit_message(view=self)
    
    async def page_text_callback(self, interaction: discord.Interaction):
        self.page = 1
        self.make_view()
        await interaction.response.edit_message(view=self)

    async def page_select_callback(self, interaction: discord.Interaction):
        print(interaction.data)
        self.page = int(interaction.data["values"][0])
        self.make_view()
        await interaction.response.edit_message(view=self)
