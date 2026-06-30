# Discord Packages
import discord
from discord.ext import commands
from discord import app_commands

# Http Requests Package
import requests
import nest_asyncio
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

async def on_message(client: commands.Bot, message: discord.Message):
    if message.content.startswith('!test'):
        await message.channel.send(message.guild.channels)
    