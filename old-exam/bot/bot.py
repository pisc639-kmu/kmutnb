# Discord Packages
import discord
from discord.ext import commands
from discord import app_commands

# Http Requests Package
import requests
# import nest_asyncio
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

# class ClientClass(discord.Client):
class ClientClass(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix="!", intents=intents)
        # self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        print("Syncing commands...")
        await self.tree.sync()
        print("Commands synced!")

async def main():
    intents = discord.Intents.all()

    client = ClientClass(intents=intents)

    @client.event
    async def on_ready():
        print(f"Logged in as {client.user} (ID: {client.user.id})")
        this = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(this, "guilds.txt"), "w", encoding='utf-8') as f:
            for guild in client.guilds:
                to_write = f"""
id: {guild.id}
name: {guild.name}
description: {guild.description}
owner: {guild.owner.name}
member count: {guild.member_count}
boost count: {guild.premium_tier}
raid detected: {guild.is_raid_detected()}
dm spam detected: {guild.is_dm_spam_detected()}
""".strip() + "\n\n"
                f.write(to_write)
        print("------")

    @client.event
    async def on_message(message: discord.Message):
        importlib.reload(testing)
        await testing.on_message(client, message)

        if message.guild.id == 1521507251565756447:
            if message.content.startswith("!reload"):
                await message.reply("Reloading...")
                for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        try:
                            await client.reload_extension(f'cogs.{filename[:-3]}')
                            print(f'Reloaded extension {filename[:-3]}')
                        except Exception as e:
                            print(f'Failed to reload extension {filename[:-3]}.')
                            traceback.print_exc()
                await client.tree.sync()
            
            if message.content.startswith("!stop"):
                await message.reply("Stopping...")
                await client.close()
    
    folder = os.path.join(os.path.dirname(__file__), 'cogs', 'tools', 'temp')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'Loading extension {filename[:-3]}')
            await client.load_extension(f'cogs.{filename[:-3]}')

    # Discord Log Handler
    # handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    discord.utils.setup_logging(handler=logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w'))

    print("Starting Bot Using Token")
    load_dotenv()
    try:
        async with client:
            await client.start(os.getenv("DISCORD_TOKEN"))
    except:
        print("Bot is disconnecting.")

        await client.close()
        traceback.print_exc()

if __name__ == "__main__":
    # nest_asyncio.apply()
    asyncio.run(main())