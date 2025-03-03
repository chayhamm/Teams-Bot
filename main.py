import discord
from discord import app_commands
from discord.ext import commands 
from discord.app_commands import Choice 
from datetime import datetime
from discord.utils import get
import random
import json

with open("config.json") as config:
    config = json.load(config)
roles = open("clanRoles.txt", "a")

intents = discord.Intents.default()
client = commands.Bot(command_prefix=config["prefix"], intents=intents)
color=discord.Color(random.randint(0, 0xFFFFFF))

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
        requestEmbed = discord.Embed(title = "New clan request", description = f'{user.mention} has requested to make: {name} clan.', color = 0xFFA500)
        requestChannel = guild.get_channel(1345852038336221254)
        class AcceptOrDeny(discord.ui.View):
            pass
            def __init__(self) -> None:
                super().__init__()
                self.value = None
            @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green)
            async def accept(self, interaction: discord.Interaction, button: discord.ui.button) -> None:
                await interaction.response.send_message(f'You have accepted the {name} clan!', ephemeral=True)
                clanRole = await guild.create_role(name=f'{name}', color =color)
                category = discord.utils.get(guild.categories, id = 1340742859581554688)
                databaseText = open("clans.txt", "a")
                databaseText.write(f'{name}: {user.id}: {user.display_name}' + '\n')
                roles.write(clanRole.name + "\n")
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages = True, send_messages = False),
                    clanRole: discord.PermissionOverwrite(read_messages = True, send_messages = True)
                }
                clanChannel = await interaction.guild.create_text_channel(name, category=category, overwrites=overwrites)
                await interaction.response.send_message(f'You have accepted the: {name} clan!', ephemeral=True)
                dmEmbed = discord.Embed(title = "[EU] Reboot Rust 5x", description = f'Your request for: {name} clan has been accepted!', color = 0xFFA500)
                dmEmbed.add_field(name = "Channel:", value = clanChannel.mention, inline = True)
                channelEmbed = discord.Embed(title = "[EU] Reboot Rust 5x", description=f"{clanRole.mention} Welcome to your clans' channel. \n Run /clan-invite to embark on your journey!", color= 0xFFA500)
                await user.send(embed = dmEmbed)
                await clanChannel.send(embed = channelEmbed)
                self.value = True
                self.stop()


client.run(config["token"])