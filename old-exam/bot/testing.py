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

importlib.reload(old_exam)

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

class DownloadButton(discord.ui.Button):
    def __init__(self, file_path: str):
        super().__init__(label="Download", style=discord.ButtonStyle.primary)
        self.file_path = file_path

    async def callback(self, interaction: discord.Interaction):
        # Handle the download logic here
        # await interaction.response.send_message(f"Downloading file from: {self.file_path}", ephemeral=True)
        await interaction.response.send_message(file=discord.File(self.file_path))


class SearchLayoutView(discord.ui.LayoutView):
    def __init__(self, keyword: str):
        super().__init__()
        self.page = 1
        self.results_per_page = 9
        self.keyword = keyword

        self.results = old_exam.search(keyword, as_json=True)

        self.total_pages = (len(self.results) // self.results_per_page) + (1 if len(self.results) % self.results_per_page > 0 else 0)

        self.main_container = discord.ui.Container()
        self.make_view()

    def make_view(self):
        self.clear_items()
        self.main_container.clear_items()

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

        for result in self.results[(self.page - 1) * self.results_per_page : self.page * self.results_per_page]:
            download_btn = DownloadButton(file_path=result['path'])
            section = discord.ui.Section(
                accessory=download_btn
            )
            section.add_item(
                discord.ui.TextDisplay(f"**{result['subject'] if result['subject'] != 'Unknown' else result['ids'][0]}** - {result['year'] - 543} - Term {result['term'][0]} {result['term_full']} - {'EP' if result['ep'] == 1 else 'Not EP' if result['ep'] == 0 else 'Not Sure'}")
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


async def on_message(client: commands.Bot, message: discord.Message):
    try:
        if message.content.startswith('!test'):
            # await message.channel.send("!t")
            # await message.channel.send(com)
            pass
        
        if message.content.startswith('!t'):
            await message.reply(view=SearchLayoutView(keyword=message.content[3:].strip()))

    except Exception as e:
        print(e)
        traceback.print_exc()
        raise e