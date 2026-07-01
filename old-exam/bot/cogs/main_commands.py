import discord
from discord.ext import commands
from discord import app_commands
import traceback
import datetime
import os

class TemplateLayoutView(discord.ui.LayoutView):
    # 1. Text Display Component (Supports markdown and headings)
    text_header = discord.ui.TextDisplay(
        "## Welcome to Components V2!\n"
        "This template demonstrates how to structure a layout using the new `LayoutView` system."
    )
    
    # 2. Visual Separator Line
    divider = discord.ui.Separator(
        spacing=discord.SeparatorSpacing.large, 
        visible=True
    )
    
    # 3. Section Component (Combines left text with a right-aligned thumbnail or accessory)
    section_info = discord.ui.Section(
        "This is a Section component. It pairs a block of text alongside an optional thumbnail or button.",
        accessory=discord.ui.Thumbnail("https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png")
    )
    
    # 4. Action Row for Traditional Interactive Components
    # We define rows and attach buttons or selects to them
    row1 = discord.ui.ActionRow()
    
    @row1.button(label="Click Me!", style=discord.ButtonStyle.primary, custom_id="btn_click")
    async def click_me_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the V2 Layout Button!", ephemeral=True)


class SearchLayoutView(discord.ui.LayoutView):
    text_header = discord.ui.TextDisplay(
        "## Old Exam Search\n"
        f"Search Query: {'keyword'}"
    )
    
    divider = discord.ui.Separator(
        spacing=discord.SeparatorSpacing.large, 
        visible=True
    )
    
    
    container = discord.ui.Container(
        
    )
    # section_info = discord.ui.Section(
    #     "This is a Section component. It pairs a block of text alongside an optional thumbnail or button.",
    #     accessory=discord.ui.Thumbnail("https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png")
    # )c
    
    # 4. Action Row for Traditional Interactive Components
    # We define rows and attach buttons or selects to them
    row1 = discord.ui.ActionRow()
    
    @row1.button(label="Click Me!", style=discord.ButtonStyle.primary, custom_id="btn_click")
    async def click_me_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the V2 Layout Button!", ephemeral=True)

class MainCommands(commands.Cog):
    "Main Commands Related to Old Exam"
    def __init__(self, client: commands.Bot):
        self.client = client

    group = app_commands.Group(name="group", description="Comamnds Group.")

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
    
    @app_commands.command(name="search", description="Search for Old Exam")
    async def _search(self, interaction: discord.Interaction, keyword: str):
        await interaction.response.send_message(view=SearchLayoutView())

async def setup(client: commands.Bot):
    await client.add_cog(MainCommands(client))
