import discord
from discord.ext import commands
from discord import app_commands
import traceback
import datetime
import os

class MainCommands(commands.Cog):
    "Main Commands Related to Old Exam"
    def __init__(self, client: commands.Bot):
        self.client = client

    group = app_commands.Group(name="group", description="Comamnds Group.")

    @group.command(name="name", description="descriptzion")
    @app_commands.describe()
    async def _edit_generate_1(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="title",
                description="Description",
                color=0x00ff00
            )
            await interaction.followup.send(file=discord.File(), embed=embed)
        except:
            traceback.print_exc()
            await interaction.followup.send("Something went wrong.")

async def setup(client: commands.Bot):
    await client.add_cog(MainCommands(client))
