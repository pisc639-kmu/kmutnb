import discord
from discord.ext import commands
from discord import app_commands
import traceback
import datetime
import os
import importlib
from cogs.tools import old_exam

# class DownloadButton(discord.ui.Button):
#     def __init__(self, file_path: str, custom_file_name: str = None):
#         super().__init__(label="Download", style=discord.ButtonStyle.primary)
#         self.file_path = file_path
#         self.custom_file_name = custom_file_name

#     async def callback(self, interaction: discord.Interaction):
#         print(f"Downloading file from: {self.file_path}")
#         # Handle the download logic here
#         await interaction.response.defer(thinking=True)
#         # await interaction.response.send_message(f"Downloading file from: {self.file_path}", ephemeral=True)
#         if self.custom_file_name:

#             file = discord.File(self.file_path, filename=self.custom_file_name)
#         else:
#             file = discord.File(self.file_path)
#         try:
#             await interaction.followup.send_message(file=file)
#             # when timed out
#         except discord.errors.NotFound:
#             await interaction.message.reply(file=file)

# class SearchLayoutView(discord.ui.LayoutView):
#     def __init__(self, keyword: str):
#         super().__init__()
#         self.page = 1
#         self.results_per_page = 9
#         self.keyword = keyword

#         self.results = old_exam.search(keyword, as_json=True)

#         self.total_pages = (len(self.results) // self.results_per_page) + (1 if len(self.results) % self.results_per_page > 0 else 0)

#         self.main_container = discord.ui.Container()
#         self.make_view()

#     def make_view(self):
#         self.clear_items()
#         self.main_container.clear_items()

#         self.text_head = discord.ui.TextDisplay(
#             "## Old Exam Search\n"
#             f"Search Query: `{self.keyword}`"
#         )
        
#         self.seperator = discord.ui.Separator(
#             spacing=discord.SeparatorSpacing.large, 
#             visible=True
#         )

#         self.main_container.add_item(self.text_head)
#         self.main_container.add_item(self.seperator)

#         for result in self.results[(self.page - 1) * self.results_per_page : self.page * self.results_per_page]:
#             download_btn = DownloadButton(
#                 file_path=result['path'],

#                 custom_file_name=f"{result['subject'] if result['subject'] != 'Unknown' else result['id']}{' EP' if result['ep'] == 1 else '' if result['ep'] == 0 else ''} - {result['year'] - 543}.pdf"
#             )
#             section = discord.ui.Section(
#                 accessory=download_btn
#             )
#             section.add_item(
#                 discord.ui.TextDisplay(f"**{result['subject'] if result['subject'] != 'Unknown' else result['id']}** - {result['year'] - 543} - Term {result['term'][0]} {result['term_full']} - {'EP' if result['ep'] == 1 else 'Not EP' if result['ep'] == 0 else 'Not Sure'}")
#             )
#             self.main_container.add_item(section)

#         self.main_container.add_item(self.seperator)

#         # Page Navigation Row
#         page_row = discord.ui.ActionRow()
        
#         left_button = discord.ui.Button(
#             label="<", 
#             style=discord.ButtonStyle.primary, 
#             custom_id="btn_left"
#         )
#         if self.page <= 1:
#             left_button.disabled = True
#         left_button.callback = self.left_button_callback
#         page_row.add_item(left_button)

#         page_text = discord.ui.Button(
#             label=f"Page {self.page} of {self.total_pages}",
#             style=discord.ButtonStyle.secondary,
#             custom_id="btn_page_text",
#         )
#         page_text.callback = self.page_text_callback
#         page_row.add_item(page_text)

#         right_button = discord.ui.Button(
#             label=">", 
#             style=discord.ButtonStyle.primary, 
#             custom_id="btn_right"
#         )
#         if self.page >= self.total_pages:
#             right_button.disabled = True
#         right_button.callback = self.right_button_callback
#         page_row.add_item(right_button)

#         # Select Dropdown Row
#         select_row = discord.ui.ActionRow()

#         page_select = discord.ui.Select(
#             placeholder=f"Page {self.page} of {self.total_pages}",
#             # Pass explicit values to make parsing safer in the callback
#             options=[discord.SelectOption(label=f"Page {i+1}", value=str(i+1)) for i in range(self.total_pages)],
#             custom_id="btn_page",
#         )
#         page_select.callback = self.page_select_callback
#         select_row.add_item(page_select)

#         self.main_container.add_item(page_row)
#         self.main_container.add_item(select_row)

#         self.add_item(self.main_container)

#     async def left_button_callback(self, interaction: discord.Interaction):
#         self.page -= 1
#         self.make_view()
#         await interaction.response.edit_message(view=self)

#     async def right_button_callback(self, interaction: discord.Interaction):
#         self.page += 1
#         self.make_view()
#         await interaction.response.edit_message(view=self)
    
#     async def page_text_callback(self, interaction: discord.Interaction):
#         self.page = 1
#         self.make_view()
#         await interaction.response.edit_message(view=self)

#     async def page_select_callback(self, interaction: discord.Interaction):
#         print(interaction.data)
#         self.page = int(interaction.data["values"][0])
#         self.make_view()
#         await interaction.response.edit_message(view=self)

class MainCommands(commands.Cog):
    "Main Commands Related to Old Exam"
    def __init__(self, client: commands.Bot):
        self.client = client

    group = app_commands.Group(name="group", description="Comamnds Group.", guild_ids=[1521507251565756447])
    search_group = app_commands.Group(name="search", description="Search Commands Group.")

    @group.command(name="name", description="descriptzion")
    @app_commands.describe()
    async def _name(self, interaction: discord.Interaction):
        try:
            class CustomContainer(discord.ui.Container):
                def __init__(self):
                    super().__init__()
                    # Adding structured content inside the container canvas
                    self.add_item(discord.ui.TextDisplay("### Components V2 Panel\nWelcome to the modern API design layout."))
                    self.add_item(discord.ui.Separator())
                    
                    # Creating a dual horizontal row utilizing Section Component properties
                    section = discord.ui.Section(
                        accessory=discord.ui.Button(label="Button", style=discord.ButtonStyle.primary),
                    )
                    section.add_item(discord.ui.TextDisplay("Main Data field left side"))
                    # (Optional: Add an accessory like a button or thumbnail via section methods)
                    self.add_item(section)
            class Interface(discord.ui.LayoutView):
                def __init__(self):
                    super().__init__(timeout=180.0)
                    
                    # Nest our content container inside the main LayoutView
                    self.add_item(CustomContainer())
                    
                    # Construct separate action row segments for operational tools
                    row = discord.ui.ActionRow()
                    row.add_item(discord.ui.Button(label="Accept Task", style=discord.ButtonStyle.success, custom_id="btn_accept"))
                    row.add_item(discord.ui.Button(label="Decline", style=discord.ButtonStyle.danger, custom_id="btn_decline"))
                    self.add_item(row)

            await interaction.response.send_message(
                # "Hello",
                view=Interface(),
                # flags=discord.MessageFlags.components_v2
            )
            # await interaction.response.defer(thinking=True)
            # embed = discord.Embed(
            #     title="title",
            #     description="Description",
            #     color=0x00ff00
            # )
            # await interaction.followup.send(embed=embed)
        except:
            traceback.print_exc()
            await interaction.followup.send("Something went wrong.")
    
    @search_group.command(name="exam", description="Search for Old Exam")
    async def _search(self, interaction: discord.Interaction, keyword: str):
        await interaction.response.defer(thinking=True)
        importlib.reload(old_exam)
        await interaction.followup.send(view=old_exam.SearchLayoutView(keyword=keyword))

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        importlib.reload(old_exam)
        await old_exam.on_interaction_handler(interaction)


async def setup(client: commands.Bot):
    await client.add_cog(MainCommands(client))
