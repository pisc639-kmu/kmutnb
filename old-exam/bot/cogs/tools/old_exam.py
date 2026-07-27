import json
import os
from pathlib import Path
import re
import ast
import typing

import asyncio
import discord

base_path = Path("D:\\kmutnb\\old-exam\\")

with open(Path(__file__).parents[3] / "subjects.json", "r", encoding="utf-8") as f:
    SUBJECTS_CACHE = json.load(f)

def create_regex_replacer(mapping):
    """Generates a function that replaces regex patterns based on a mapping dict.
    Automatically applies case-insensitivity and word boundaries around all patterns.
    """
    # Flatten mapping into a list of (pattern, target) tuples
    flat = [(p, t) for t, src in mapping.items() for p in ([src] if isinstance(src, str) else src)]
    
    # Map group names like 'g0', 'g1' to targets
    group_to_target = {f"g{i}": target for i, (_, target) in enumerate(flat)}
    
    # Wrap each pattern with word boundaries \b
    try:
        master_regex = re.compile(
            "|".join(f"(?P<g{i}>\\b(?:{p})\\b)" for i, (p, _) in enumerate(flat)), 
            flags=re.IGNORECASE
        )
    except re.error as e:
        print(f"Error compiling regex: {e}")
        # test each to find which is causing error
        for i, (p, _) in enumerate(flat):
            try:
                re.compile(f"(?P<g{i}>\\b(?:{p})\\b)")
            except re.error as e:
                print(f"Error compiling regex: {e}")
                print(f"Pattern causing error: {p}")
        master_regex = re.compile("|".join(r"\b" + re.escape(p) + r"\b" for p, _ in flat), flags=re.IGNORECASE)
    
    # Return the dynamic replacer function
    return lambda text: master_regex.sub(
        lambda m: next(group_to_target[k] for k, v in m.groupdict().items() if v is not None and k in group_to_target), 
        text
    )

mapping = {
    # 1. Roman Numerals Standardizations
    "#iii": ["3", r"iii"],
    "#ii": ["2", r"ii"],
    "#iv": ["4", r"iv"],
    "#vi": ["6", r"vi"],
    "#v": ["5", r"v"],
    "#i": ["1", r"i"],
    
    # 2. Main Course Subjects
    "mathematics": [r"math(s)?", r"mathe?"],
    "mechanics": [r"phys(ics?)?", r"mech(anics?)?"],
    "chemistry": r"chem(istry)?",
    "computer": r"comp?(ut)?e?r?",
    
    # 3. Common Context Modifiers & Abbreviations
    "engi": r"engi(ne?e?r)?i?n?g?",
    "engl": r"engl?(ish)?",
    "introduction to": r"intro(duct)?(ion)?s?",
    "fundamental": r"fund(amental)?",
    "systems": r"sys(tem)?s?",
    "materials": r"mate?r(ial)?s?",
    "communicative": r"comm",
    "programming": r"prog(ramm?)?i?n?g?",
    "circuit": r"circ(uit)?s?",
    
    # 4. Computer-aided acronym extensions
    "computer-aided design": "cad",
    "computer-aided manufacturing": "cam",

    # 5. Popular Course Abbreviations
    "electrical": r"elect?r?o?n?i?c?(a?l?|c?i?t?y?)?s?",
    "phenomena": "pheno?m?e?n?a?",
    "drawing": "draw?i?n?g?",

    # "#": r"#+",
}

# # Example usage:
# standardize_text = create_regex_replacer(mapping)
# print(standardize_text("i need help with Mech 1 and Eng Materials")) 
# # Output: mechanics i and engineering materials

replacer = create_regex_replacer(mapping)
def standardize_text(query:str):
    return replacer(query).lower().strip()

def format_query(query:str, removequotes=True) -> str:
    query = query.lower().strip()
    if removequotes:
        query = re.sub(r'^"|".{0,2}$|^\,|,\s*,?', '', query)
    else:
        query = re.sub(r'^\,|,\s*,?', '', query)
    return query

def format_query2(query:str) -> str:
    query = re.sub(r'^"|".{0,2}$|^\,|,\s*,?', '', query)
    query = re.sub(r'[\s,\^\"\'-_]', '', query)
    query = re.sub(r'[s]', '', query)
    query = re.sub(r'#+', '#', query)
    return query

def check_query(query:str, line:str) -> bool:
    # print("q", format_query2(query))
    # return format_query2(standardize_text(query)) in format_query2(standardize_text(line))
    return query in format_query2(standardize_text(line))

def search_files(query:str, limit=250):
    files = []
    length = 0  
    with open(Path(__file__).parents[3] / "files.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()[1:-1]
        # print(len(lines))
        query_formatted1 = format_query(query, removequotes=False)
        query_formatted2 = format_query(query, removequotes=True)
        query_formatted3 = format_query2(standardize_text(query))
        print(f"Query: {query_formatted3}")
        for line in lines:
            line = line.lower()
            # print(line)
            try:
                try:
                    fpath = Path(base_path) / Path(ast.literal_eval(re.search(r"\"[^\"]+\"", line[155:]).group(0)))
                except:
                    print(line[170:])
                is_match = False

                # if check_query(re.sub(r"[\'\"]+", '"', (query_formatted1 + '"')), line) or query in str(fpath):
                if check_query(query_formatted3, line) or query in str(fpath):
                    is_match = True
                # if "Mathematics III".lower()     in line:
                #     print(query_formatted3, line, format_query2(standardize_text(line)))
                #     break

                # print(query, line)
                if query_formatted2.isdigit() and query_formatted2 in line:
                    is_match = True
                    # print(1)

                if is_match:
                    files.append({
                        "path": str(fpath),
                        "fsize": line.split(",")[-1].strip(),
                    })
                    length += 1
                    if length >= limit:
                        break
            except:
                import traceback
                traceback.print_exc()
                # sys.exit()
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

def get_file_info(file):
    file_path = file
    file_path = file_path["path"] if isinstance(file, dict) and "path" in file else file
    file_path = Path(file_path)
    res = {}
    res["path"] = str(file_path)
    res["name"] = file_path.stem
    try:
        res["fsize"] = file["fsize"].upper() if isinstance(file, dict) and "fsize" in file else str(file_path.stat().st_size)
    except:
        print("err", file)
    res["ids"] = [i.strip() for i in re.split(r'[,\.\s]+', file_path.stem) if i.strip() != "" and i.strip().isdigit()]
    res["id"] = res["ids"][0] if res["ids"] else None
    res["subject"] = SUBJECTS_CACHE.get(str(res["ids"][0]), "Unknown") if res["ids"] else "Unknown"
    try:
        res['year'] = int(Path(file_path).parts[3])
    except (ValueError, IndexError):
        print(file_path)

    res["term"] = (int(Path(file_path).parts[4][-1]), Path(file_path).parts[5][0])
    res["term_full"] = "final" if res["term"][1].lower() == "f" else "midterm" if res["term"][1].lower() == "m" else "unknown"
    res['ep'] = file_is_ep(file_path)

    return res

def filter_file(file_path, term=None, period=None, ep=None):
    file_path = file_path["path"]
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
    return [f for f in file_paths if filter_file(f, term, period, ep)]

def search(query:str, term:int=None, period:str=None, ep:bool=None, as_json=False):
    try:
        print(f"Options: term={term}, period={period}, ep={ep}")
        print(f"Searching for: {query}")

        # print(query.isdigit())
        query = standardize_text(query)
        files = search_files(query)
        try:
            files = filter_files(files, term, period, ep)
        except:
            # print("f", files)
            pass
        if as_json:
            temp = files
            files = []
            for f in temp:
                try:
                    files.append(get_file_info(f))
                except:
                    pass
            # files = [get_file_info(f) for f in files]
        return files
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e


async def on_interaction_handler(interaction: discord.Interaction):
    print(f"Interaction: {interaction.type}")
    if interaction.type != discord.InteractionType.component:
        return
    print(f"Interaction data: {interaction.data}")
    print(f"Interaction author: {interaction.user}")
    
    custom_id = interaction.data.get("custom_id", "")
    if custom_id.startswith("download:"):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            prefix, hash_value, file_path, custom_file_name = (custom_id.split(":") + [None] * 4)[:4]
        except ValueError:
            await interaction.followup.send("Invalid download button.", ephemeral=True)
            # return
        p = Path(file_path).parts
        safe_path = Path(base_path).joinpath(f"{p[0]}/term {p[1]}/{'final' if p[2] == 'f' else 'midterm'}/" + "/".join(p[3:]))
        print(f"Downloading file from: {safe_path}")
        file_name = custom_file_name if custom_file_name is not None else safe_path.name 

        seperator = discord.ui.Separator(
            spacing=discord.SeparatorSpacing.large, 
            visible=True
        )

        loading_view = discord.ui.LayoutView()

        loading_container = discord.ui.Container()
        loading_view.add_item(loading_container)

        text = f"## {file_name}"
        loading_container.add_item(discord.ui.TextDisplay(text))
        
        loading_container.add_item(seperator)
        # loading_view.add_item(discord.ui.th("https://cdn.discordapp.com/emojis/1144047129183133707.gif"))
        loading_container.add_item(discord.ui.TextDisplay("<a:loading:1522210046640128092>  Uploading..."))
        loading_files = [
            # discord.File(Path(__file__).parents[2] / "assets" / "loading.gif", filename="loading.gif")
        ]
        print(3)
        print(4)
        try:
            loading_message = await interaction.followup.send(view=loading_view, files=loading_files)
        except discord.errors.NotFound:
            loading_message = await interaction.message.reply(view=loading_view, files=loading_files)

        dm_channel = None
        dm_message = None

        try:
            user = interaction.user
            dm_channel = user.dm_channel
            if dm_channel is None:
                try:
                    dm_channel = await user.create_dm()
                except discord.Forbidden:
                    dm_channel = None
            if dm_channel:
                dm_message = await dm_channel.send(view=loading_view, files=loading_files)
        except Exception as e:
            print(e)
        print(text)
        

        # Handle the download logic here
        # await interaction.response.send_message(f"Downloading file from: {safe_path}", ephemeral=True)
        try:
            with open(safe_path, "rb") as f:
                file_bytes = f.read()
                file_name
                if custom_file_name:
                    file_res = discord.File(safe_path, filename=custom_file_name)
                    file_dm = discord.File(safe_path, filename=custom_file_name)
                else:
                    file_res = discord.File(safe_path)
                    file_dm = discord.File(safe_path)
        except FileNotFoundError:
            # When Drive D: SSD is "NOT CONNECTED" to the pc
            main_view = discord.ui.LayoutView()

            main_container = discord.ui.Container()
            main_view.add_item(main_container)

            text = f"## {file_name}"

            main_container.add_item(discord.ui.TextDisplay(text))
            main_container.add_item(seperator)
            # main_container.add_item(discord.ui.TextDisplay("**\u26A0\uFE0F Error:** Database is not connected. Please try again later."))
            main_container.add_item(discord.ui.TextDisplay("### **[\u26a0 Error]**: File Source is not connected. Please try again later, or contact @pisc_639"))

            if isinstance(loading_message, discord.Message):
                tasks = [loading_message.edit(view=main_view)]
                if dm_channel:
                    tasks.append(dm_message.delete())
                    tasks.append(dm_channel.send(view=main_view))
                results = await asyncio.gather(*tasks, return_exceptions=True)

                dm_result = results[1]
                int_result = results[0]
                if isinstance(dm_result, discord.Forbidden):
                    print("Failed to edit DM: User blocked the bot or closed DMs.")
                elif isinstance(dm_result, Exception):
                    print(f"DM edit failed due to another error: {dm_result}")
                else:
                    print("DM edit successful!")
                
                if isinstance(int_result, Exception):
                    print(f"Interaction edit failed: {int_result}")
            else:
                try:
                    await interaction.edit_original_response(view=main_view, attachments=[file_res])
                except discord.errors.NotFound:
                    await interaction.message.reply(file=file_res)
            return


        main_view = discord.ui.LayoutView()

        main_container = discord.ui.Container()
        main_view.add_item(main_container)

        text = f"## {file_name}"

        main_container.add_item(discord.ui.TextDisplay(text))
        main_container.add_item(seperator)
        main_container.add_item(discord.ui.File(f"attachment://{file_res.filename}"))
        if isinstance(loading_message, discord.Message):
            tasks = [loading_message.edit(view=main_view, attachments=[file_res])]
            if dm_message:
                tasks.append(dm_message.edit(view=main_view, attachments=[file_dm]))
            results = await asyncio.gather(*tasks, return_exceptions=True)

            dm_result = results[1]
            int_result = results[0]
            if isinstance(dm_result, discord.Forbidden):
                print("Failed to edit DM: User blocked the bot or closed DMs.")
            elif isinstance(dm_result, Exception):
                print(f"DM edit failed due to another error: {dm_result}")
            else:
                print("DM edit successful!")
            
            if isinstance(int_result, Exception):
                print(f"Interaction edit failed: {int_result}")
        else:
            try:
                await interaction.edit_original_response(view=main_view, attachments=[file_res])
                # when timed out
            except discord.errors.NotFound:
                await interaction.message.reply(file=file_res)

        print(text)

class DownloadButton(discord.ui.Button):
    def __init__(self, file_path: str, custom_file_name: str = None, custom_button_text: str = "Download"):
        super().__init__(label=custom_button_text, style=discord.ButtonStyle.primary)
        self.file_path = file_path
        self.custom_file_name = custom_file_name
        p = Path(file_path).parts
        file_path_converted =  f"{p[3]}/{p[4][-1]}/{p[5][0]}/" + "/".join(p[6:])
        self.custom_id = f"download:{hash(file_path)}:{file_path_converted}:{custom_file_name}"  # Unique ID based on file path
        print(f"Initialized DownloadButton with custom_id: {self.custom_id}, file_path: {self.file_path}, custom_file_name: {self.custom_file_name}")

    # async def callback(self, interaction: discord.Interaction):
    #     print(f"Downloading file from: {self.file_path}")

    #     # Handle the download logic here
    #     # await interaction.response.send_message(f"Downloading file from: {self.file_path}", ephemeral=True)
    #     if self.custom_file_name:
    #         file = discord.File(self.file_path, filename=self.custom_file_name)
    #     else:
    #         file = discord.File(self.file_path)

    #     seperator = discord.ui.Separator(
    #         spacing=discord.SeparatorSpacing.large, 
    #         visible=True
    #     )


    #     loading_view = discord.ui.LayoutView()

    #     loading_container = discord.ui.Container()
    #     loading_view.add_item(loading_container)

    #     text = f"## {file.filename}"
    #     loading_container.add_item(discord.ui.TextDisplay(text))
        
    #     loading_container.add_item(seperator)
    #     # loading_view.add_item(discord.ui.th("https://cdn.discordapp.com/emojis/1144047129183133707.gif"))
    #     loading_container.add_item(discord.ui.TextDisplay("<a:loading:1522210046640128092> Uploading..."))
    #     loading_files = [
    #         # discord.File(Path(__file__).parents[2] / "assets" / "loading.gif", filename="loading.gif")
    #     ]
    #     try:
    #         loading_message = await interaction.response.send_message(view=loading_view, files=loading_files)
    #     except discord.errors.NotFound:
    #         loading_message = await interaction.message.reply(view=loading_view, files=loading_files)

    #     print(text)


    #     main_view = discord.ui.LayoutView()

    #     main_container = discord.ui.Container()
    #     main_view.add_item(main_container)

    #     text = f"## {file.filename}"

    #     main_container.add_item(discord.ui.TextDisplay(text))
    #     main_container.add_item(seperator)
    #     main_container.add_item(discord.ui.File(f"attachment://{file.filename}"))
    #     if isinstance(loading_message, discord.Message):
    #         await loading_message.edit(view=main_view, attachments=[file])
    #     else:
    #         try:
    #             await interaction.edit_original_response(view=main_view, attachments=[file])
    #             # when timed out
    #         except discord.errors.NotFound:
    #             await interaction.message.reply(file=file)

    #     print(text)

class ErrorView(discord.ui.LayoutView):
    def __init__(self, keyword: str, error_message: str):
        super().__init__()
        self.error_message = error_message
        self.keyword = keyword

        self.main_container = discord.ui.Container()
        self.text_head = discord.ui.TextDisplay(
            "# Old Exam Search\n"
            "Search Query: `" + self.keyword.replace('`', '\\`') + "`"
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
            error_message = f"### No results found for the keyword: {self.keyword}"
            error_view = ErrorView(keyword=self.keyword, error_message=error_message)
            self.add_item(error_view.main_container)
        else:
            self.total_pages = min(25, (len(self.results) // self.results_per_page) + (1 if len(self.results) % self.results_per_page > 0 else 0))

            self.main_container = discord.ui.Container()
            self.make_view()

    def make_view(self):
        self.clear_items()
        self.main_container.clear_items()

        self.text_head = discord.ui.TextDisplay(
            "# Old Exam Search\n"
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
                custom_file_name=f"{result['subject'] if result['subject'] != 'Unknown' else result['id']}{' EP' if result['ep'] == 1 else '' if result['ep'] == 0 else ''} - {result['year'] - 543}.pdf",
                custom_button_text=f"Download ({result['fsize']})"
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
