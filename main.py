import os

import discord
from discord import app_commands

# from discord.ext import commands
from dotenv import load_dotenv

# user commands
from commands.fetch_entry import fetch_entry_cmd
from commands.fetch_entry import fetch_entry_ui
from commands.edit_entry import edit_entry_modal
from commands.one_o_one import one_o_one
from commands import hgs

# load environment vars (from .env)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

# setting up the bot
intents = discord.Intents.default()
# if you don't want all intents you can do discord.Intents.default()
client = discord.Client(intents=intents)
# CommandTree is where all our defined commands are stored
tree = discord.app_commands.CommandTree(client)
this_guild = discord.Object(id=GUILD)  # basically refers to this server


# ! These are basic test commands that should not exist when deployed
# * simple hi command
@tree.command(
    name="test",
    description="Responds with a hardcoded string",
    guild=this_guild,
)
async def test_slash_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hi I was called")


# * simple echo command with param explanation
@tree.command(
    name="echo",
    description="Echoes whatever string is fed",
    guild=this_guild,
)
@app_commands.describe(given_str="The string you want echoed backed")
async def test_slash_command(interaction: discord.Interaction, given_str: str):
    await interaction.response.send_message(f"You sent this: `{given_str}`")


# * register commands from other files
fetch_entry_cmd.register_commands(tree, this_guild)
fetch_entry_ui.register_commands(tree, this_guild)
one_o_one.register_commands(tree, this_guild)
# edit_entry_modal.register_commands(tree, this_guild, client)
hgs.register_commands(tree, this_guild)


# sync the slash commands to server
@client.event
async def on_ready():
    await tree.sync(guild=this_guild)
    # print "ready" in the console when the bot is ready to work
    print("Bot is ready.")


client.run(TOKEN)
