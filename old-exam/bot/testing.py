# Discord Packages
import discord
from discord.ext import commands
from discord import app_commands

# Http Requests Package
import requests
import asyncio
import aiohttp

# System Packages
import os
import sys
import shutil
import importlib
import logging
import traceback
from dotenv import load_dotenv

# Object Packages
import re
import json
import random
import time
import io
import testing
from cogs.tools import old_exam

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
    def __init__(self, keyword: str):
        super().__init__()
        self.page = 1
        self.results_per_page = 5
        self.keyword = keyword

        # 1. Define dynamic components inside __init__ so they can use `keyword`
        self.text_header = discord.ui.TextDisplay(
            "## Old Exam Search\n"
            f"Search Query: `{self.keyword}`"
        )
        
        self.divider = discord.ui.Separator(
            spacing=discord.SeparatorSpacing.large, 
            visible=True
        )
        
        self.container = discord.ui.Container()

        text = discord.ui.TextDisplay("This is a container with a text display.")
        self.container.add_item(text)

        # 2. Add the items to the view so the layout renders them
        self.add_item(self.text_header)
        self.add_item(self.divider)
        self.add_item(self.container)
        
        # 3. Create the action row and add the button to it
        row1 = discord.ui.ActionRow()
        
        # We manually create the button and add it to the row
        button = discord.ui.Button(
            label="Click Me!", 
            style=discord.ButtonStyle.primary, 
            custom_id="btn_click"
        )
        button.callback = self.click_me_callback
        row1.add_item(button)
        
        self.add_item(row1)

    # 4. Move the callback out of the class-body evaluation flow
    async def click_me_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("You clicked the V2 Layout Button!", ephemeral=True)

async def on_message(client: commands.Bot, message: discord.Message):
    try:
        if message.content.startswith('!test'):
            container = discord.Container(
                data=[
                    discord.ui.TextDisplay("# Title Test")
                ]
            )

            # await message.channel.send(com)
        
        if message.content.startswith('!t'):
            # keyword = message.content[2:].strip()
            # if keyword == "":
            #     await message.reply("Please provide a search query.")
            #     return
            # # await message.reply("\n".join(old_exam.search("Mathematics III", ep=True))[:2000])# 1. Create the base LayoutView instance directly
            # search_view = discord.ui.LayoutView()

            # # 2. Define the dynamic components using the `keyword` variable
            # text_header = discord.ui.TextDisplay(
            #     "## Old Exam Search\n"
            #     f"Search Query: {keyword}"
            # )
            
            # divider = discord.ui.Separator(
            #     spacing=discord.SeparatorSpacing.large, 
            #     visible=True
            # )
            
            # container = discord.ui.Container()

            # # 3. Create the row and the button
            # row1 = discord.ui.ActionRow()
            # button = discord.ui.Button(
            #     label="Click Me!", 
            #     style=discord.ButtonStyle.primary, 
            #     custom_id="btn_click"
            # )

            # text = discord.ui.TextDisplay("This is a container with a text display.")
            # # container.add_item(row1)
            # container.add_item(text)

            # # 4. Define the callback function right here inline
            # async def click_me_callback(btn_interaction: discord.Interaction):
            #     await btn_interaction.response.send_message(
            #         "You clicked the inline Layout Button!", 
            #         ephemeral=True
            #     )

            # # Bind the callback to the button
            # button.callback = click_me_callback
            
            # # 5. Pack everything into the row and the view
            # row1.add_item(button)
            
            # search_view.add_item(text_header)
            # search_view.add_item(divider)
            # search_view.add_item(container)
            # search_view.add_item(row1)

            # # 6. Send it!
            # # await interaction.response.send_message(
            # #     f"Displaying results for: **{keyword}**", 
            # #     view=search_view, 
            # #     ephemeral=True
            # # )
            await message.reply(view=SearchLayoutView("Mathematics III"))

    except Exception as e:
        print(e)
        traceback.print_exc()