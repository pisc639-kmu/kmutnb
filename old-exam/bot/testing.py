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
from pathlib import Path
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

async def on_message(client: commands.Bot, message: discord.Message):
    if message.guild.id != 1521507251565756447:
        return

    try:
        if message.content.startswith('!test'):
            # await message.channel.send("!t")
            # await message.channel.send(com)
            pass
        
        if message.content.startswith('!t'):
            keyword = message.content[3:].strip()
            if not keyword:
                await message.reply("Please provide a keyword to search for.")
            else:
                importlib.reload(old_exam)
                await message.reply(view=old_exam.SearchLayoutView(keyword=keyword))
        
        if message.content.startswith('!dg'):
            EMOJI_REGEX = re.compile(r"<(a)?:[a-zA-Z0-9_~]+:(\d+)>")
            matches = EMOJI_REGEX.findall(message.content)

            if matches:
                # Use a single aiohttp client session for efficiency
                async with aiohttp.ClientSession() as session:
                    for is_animated, emoji_id in matches:
                        # Determine file extension based on whether the emoji is animated
                        ext = "gif" if is_animated else "png"
                        
                        # Construct the direct Discord CDN link
                        url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{ext}"
                        filename = f"{emoji_id}.{ext}"

                        try:
                            # Request the raw data from Discord's assets server
                            async with session.get(url) as response:
                                if response.status == 200:
                                    data = await response.read()
                                    
                                    # Save binary payload locally
                                    with open(Path(__file__).parent / "cogs/tools/temp" / filename, "wb") as f:
                                        f.write(data)
                                    
                                    print(f"Successfully downloaded {filename} from {url}")
                                    await message.channel.send(f"Downloaded emoji: `{filename}`")
                                else:
                                    print(f"Failed to fetch image. HTTP Status: {response.status}")
                        except Exception as e:
                            print(f"Error downloading emoji {emoji_id}: {e}")
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise e