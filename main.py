import discord
from discord import app_commands
from discord.ext import commands 
from discord.app_commands import Choice 
from datetime import datetime
import json

with open("config.json") as config:
    config = json.load(config)

intents = discord.Intents.default()
client = commands.Bot(command_prefix=config["prefix"], intents=intents)

@client.event
async def on_ready():
    print("bot is ready")
    await client.change_presence(status=discord.Status.online)
    try:
        synced = await client.tree.sync(guild=discord.Object(id=1340446614061322280))
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@client.tree.command(name = "clan-create", description = "Run this command to create your team!", guild = discord.Object(id = 1340446614061322280))
async def clanCreate(interaction: discord.Interaction, name: str):
    guild = client.get_guild(1340446614061322280)
    leader_role = guild.get_role(1345850845463449662)
    user = interaction.user
    if leader_role in user.roles:
        await interaction.response.send_message("You cannot create a clan, you are already a leader!", ephemeral=True)
    else:
        

client.run(config["token"])