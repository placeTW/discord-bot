import os

import discord
from discord import app_commands

# from discord.ext import commands
from dotenv import load_dotenv
import datetime

# user commands
from commands.fetch_entry import fetch_entry_cmd
from commands.fetch_entry import fetch_entry_ui
from commands.edit_entry import edit_entry_cmd
from commands.one_o_one import one_o_one
from commands import hgs
from commands.reacttw import react_tw
from commands.react_baltics import react_baltics
from commands.react_czech import react_czech
from commands.react_ph import react_ph
from commands.hsinchu_wind import hsinchu_wind
from commands.shiba import random_shiba
from commands.capoo import random_capoo
from commands.restart import restart
from commands.gothefucktosleep import gothefucktosleep
import sys

# load environment vars (from .env)
load_dotenv()
prod = len(sys.argv) > 1 and sys.argv[1] == "prod"
TOKEN = os.getenv("DISCORD_TOKEN_DEV" if not prod else "DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

deployment_date = datetime.datetime.now()

# setting up the bot
intents = discord.Intents.default()
# also turn on messages functionality
intents.message_content = True
# if you don't want all intents you can do discord.Intents.default()
client = discord.Client(intents=intents)
# CommandTree is where all our defined commands are stored
tree = discord.app_commands.CommandTree(client)
this_guild = discord.Object(id=GUILD)  # basically refers to this server


@tree.command(
    name="website",
    description="Responds with the placeTW website link",
    guild=this_guild,
)
async def test_slash_command(interaction: discord.Interaction):
    await interaction.response.send_message("https://placetw.com/")


@tree.command(
    name="echo",
    description="Echoes whatever string is fed",
    guild=this_guild,
)
@app_commands.describe(given_str="The string you want echoed backed")
async def test_slash_command(interaction: discord.Interaction, given_str: str):
    await interaction.response.send_message(f"You sent this: `{given_str}`")


@tree.command(
    name="deployment-info",
    description="Returns information about the bot deployment",
    guild=this_guild,
)
async def test_slash_command(interaction: discord.Interaction):
    msg = f"""
PlaceTW discord bot ({'prod' if prod else 'dev'} deployment)
Deployed on `{deployment_date.ctime()} ({deployment_date.astimezone().tzinfo})`
https://github.com/placeTW/discord-bot
    """
    await interaction.response.send_message(msg)


# * register commands from other files
fetch_entry_cmd.register_commands(tree, this_guild)
fetch_entry_ui.register_commands(tree, this_guild)
one_o_one.register_commands(tree, this_guild)
# edit_entry_modal.register_commands(tree, this_guild, client)
edit_entry_cmd.register_commands(tree, this_guild, client)
hgs.register_commands(tree, this_guild)
random_shiba.register_commands(tree, this_guild)
random_capoo.register_commands(tree, this_guild)
restart.register_commands(tree, this_guild)
gothefucktosleep.register_commands(tree, this_guild)


# sync the slash commands to server
@client.event
async def on_ready():
    await tree.sync(guild=this_guild)
    # print "ready" in the console when the bot is ready to work
    print("Bot is ready.")


# when someone sends any message
@client.event
async def on_message(message: discord.Message):
    # don't respond to bot's own posts
    if message.author == client.user:
        return

    if react_tw.is_TW_message(message):
        await react_tw.send_react_tw(message)

    if react_baltics.is_baltic_message(message):
        await react_baltics.send_react_baltic(message)
    if react_czech.is_czech_message(message):
        await react_czech.send_react_czech(message)
    if react_ph.is_ph_message(message):
        await react_ph.send_react_ph(message)

    if hsinchu_wind.is_hsinchu_message(message):
        await hsinchu_wind.send_hsinchu_msg(message)


client.run(TOKEN)
