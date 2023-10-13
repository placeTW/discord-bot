import os

import discord
from discord import app_commands

# from discord.ext import commands
from dotenv import load_dotenv
import datetime
import logging
import sys

# user commands
from commands.fetch_entry import fetch_entry_cmd
from commands.fetch_entry import fetch_entry_ui
from commands.edit_entry import edit_entry_cmd
from commands.meow.meow import meow_meow
from commands.one_o_one import one_o_one
from commands import hgs
from commands.reacttw import react_tw
from commands.react_ua import react_ua
from commands.react_baltics import react_baltics
from commands.react_czech import react_czech
from commands.react_ph import react_ph
from commands.react_hgs import react_hgs
from commands.hsinchu_wind import hsinchu_wind
from commands.shiba import random_shiba
from commands.capoo import random_capoo
from commands.restart import restart
from commands.gothefucktosleep import gothefucktosleep
from commands.boba import boba
from commands.confessions import confession
from presence import watching
import bot
import sys

# load environment vars (from .env)
load_dotenv()
prod = len(sys.argv) > 1 and sys.argv[1] == "prod"
TOKEN = os.getenv("DISCORD_TOKEN_DEV" if not prod else "DISCORD_TOKEN")
GUILDS = os.getenv("DISCORD_GUILD").split(",")

deployment_date = datetime.datetime.now()
client = bot.get_bot()
# CommandTree is where all our defined commands are stored
tree = discord.app_commands.CommandTree(client)
placetw_guild = discord.Object(id=GUILDS[0])  # basically refers to this server


filename = f"{str(datetime.datetime.now()).split('.')[0].replace(':', '-')}.log"
path = f"{sys.path[0]}/logs/{filename}"
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO, filename=path, filemode='a')
logging.getLogger().addHandler(logging.StreamHandler())


@tree.command(
    name="website",
    description="Responds with the placeTW website link",
    guild=placetw_guild,
)
async def test_slash_command(interaction: discord.Interaction):
    await interaction.response.send_message("https://placetw.com/")


@tree.command(
    name="echo",
    description="Echoes whatever string is fed",
    guild=placetw_guild,
)
@app_commands.describe(given_str="The string you want echoed backed")
async def test_slash_command(interaction: discord.Interaction, given_str: str):
    await interaction.response.send_message(f"You sent this: `{given_str}`")


@tree.command(
    name="deployment-info",
    description="Returns information about the bot deployment",
    guild=placetw_guild,
)
async def test_slash_command(interaction: discord.Interaction):
    msg = f"""
PlaceTW discord bot ({'prod' if prod else 'dev'} deployment)
Deployed on `{deployment_date.ctime()} ({deployment_date.astimezone().tzinfo})`
https://github.com/placeTW/discord-bot
    """
    await interaction.response.send_message(msg)


# * register commands from other files to the placetw server
# edit_entry_modal.register_commands(tree, this_guild, client)
edit_entry_cmd.register_commands(tree, placetw_guild, client)
restart.register_commands(tree, placetw_guild)
watching.register_commands(tree, placetw_guild, client)

# * register commands to the other servers
for guild_id in GUILDS:
    guild = discord.Object(id=guild_id)

    fetch_entry_cmd.register_commands(tree, guild)
    fetch_entry_ui.register_commands(tree, guild)
    one_o_one.register_commands(tree, guild)
    hgs.register_commands(tree, guild)
    random_shiba.register_commands(tree, guild)
    random_capoo.register_commands(tree, guild)
    gothefucktosleep.register_commands(tree, guild)
    boba.register_commands(tree, guild)

# * register commands to the specific servers onlu
# at this point, the first two servers are specifically TW and Baltics server
# TODO: make GUILDS a dict probably
confession.register_commands(tree, client, GUILDS[:2])


# sync the slash commands servers
@client.event
async def on_ready():
    for guild_id in GUILDS:
        guild = discord.Object(id=guild_id)
        await tree.sync(guild=guild)
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

    if react_hgs.is_hgs_message(message):
        await react_hgs.send_react_hgs(message)
    if react_baltics.is_baltic_message(message):
        await react_baltics.send_react_baltic(message)
    if react_czech.is_czech_message(message):
        await react_czech.send_react_czech(message)
    if react_ph.is_ph_message(message):
        await react_ph.send_react_ph(message)
    if react_ua.is_UA_message(message):
        await react_ua.send_react_ua(message)

    if hsinchu_wind.is_hsinchu_message(message):
        await hsinchu_wind.send_hsinchu_msg(message)

    await meow_meow(message)


client.run(TOKEN)
