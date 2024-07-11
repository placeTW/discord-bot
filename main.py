import os

import discord
from discord import app_commands

# from discord.ext import commands
from dotenv import load_dotenv
import datetime

# user commands
from commands.basic import basic_commands
from commands.bbt_count import bbt_count
from commands.config import config_commands
from commands.fetch_entry import fetch_entry_cmd
from commands.fetch_entry import fetch_entry_ui
from commands.edit_entry import edit_entry_cmd
from commands.meow.meow import meow_meow
from functions.reacts import handle_message_react
from modules import logging
from commands.one_o_one import one_o_one
from commands import hgs
from commands.pat import pat
from commands.reacttw import react_tw
from commands.react_ua import react_ua
from commands.react_baltics import react_baltics
from commands.react_czech import react_czech
from commands.react_ph import react_ph
from commands.react_hgs import react_hgs
from commands.react_earthquake import react_earthquake
from commands.hsinchu_wind import hsinchu_wind
from commands.shiba import random_shiba
from commands.capoo import random_capoo
from commands.restart import restart
from commands.fucking import fucking
from commands.boba import boba
from commands.confessions import confession
from commands.stats import stats
from commands.tocfl import tocfl
from commands.formosa_stickers import formosa_stickers

from presence import watching

from mentioned import mention_responses

from modules.supabase import supabaseClient
from modules import config
import bot
import sys
from git import Repo
import platform

# load environment vars (from .env)
load_dotenv()
is_prod = len(sys.argv) > 1 and sys.argv[1] == "prod"
TOKEN = os.getenv("DISCORD_TOKEN_DEV" if not is_prod else "DISCORD_TOKEN")

deployment_date = datetime.datetime.now()
client = bot.get_bot(is_prod)
# CommandTree is where all our defined commands are stored
tree = discord.app_commands.CommandTree(client)
placetw_guild = discord.Object(
    id=os.getenv("PLACETW_SERVER_ID")
)  # basically refers to this server


@tree.command(
    name="deployment-info",
    description="Returns information about the bot deployment",
    guild=placetw_guild,
)
async def deployment_info(interaction: discord.Interaction):
    branch_name = Repo().active_branch.name
    msg = f"""
PlaceTW discord bot ({'prod' if is_prod else 'dev'} deployment)
Branch deployed: `{branch_name}`
Python version: `{platform.python_version()}`
Operating system: `{platform.platform()}`
Deployed on `{deployment_date.ctime()} ({deployment_date.astimezone().tzinfo})`
https://github.com/placeTW/discord-bot{f'/tree/{branch_name}' if branch_name != 'main' else ''}
    """
    await interaction.response.send_message(msg)


# * register commands the just the placetw server
edit_entry_cmd.register_commands(tree, placetw_guild, client)
restart.register_commands(tree, placetw_guild)
watching.register_commands(tree, placetw_guild, client)
tocfl.register_commands(tree, placetw_guild, client)

# * register commands to the other servers
guilds = [
    discord.Object(id=int(server_id))
    for server_id in client.guilds_dict.keys()
]

def register_commands(tree, client, guilds):
    # * Register commands to all servers that the bot is in
    bbt_count.register_commands(tree, client, guilds)
    fetch_entry_cmd.register_commands(tree, guilds)
    fetch_entry_ui.register_commands(tree, guilds)
    one_o_one.register_commands(tree, guilds)
    hgs.register_commands(tree, guilds)
    random_shiba.register_commands(tree, guilds)
    random_capoo.register_commands(tree, guilds)
    fucking.register_commands(tree, guilds)
    boba.register_commands(tree, guilds)
    basic_commands.register_commands(tree, guilds)
    config_commands.register_commands(tree, client, guilds)
    stats.register_commands(tree, client, guilds)
    pat.register_commands(tree, client, guilds)
    formosa_stickers.register_commands(tree, guilds)


register_commands(tree, client, guilds)


# confessions needs the dictionary for the confession channel id
confession.register_commands(tree, client)


# sync the slash commands servers
@client.event
async def on_ready():
    for guild_id in client.guilds_dict.keys():
        guild = discord.Object(id=guild_id)
        await tree.sync(guild=guild)
    # Enable logging
    logging.init(client, deployment_date)
    print("Bot is ready.")


# when someone sends any message
@client.event
async def on_message(message: discord.Message):
    message_reacts_enabled = True
    try:
        message_reacts_enabled = client.guilds_dict[message.guild.id][
            "message_reacts_enabled"
        ]
    except:
        # default true
        pass

    # don't respond to bot's own posts or if message reacts are disabled
    if message.author == client.user or not message_reacts_enabled:
        return

    events = []

    if client.user.mentioned_in(message):  # if bot is pinged in message
        await mention_responses.reply_with_random_response(message)
        events.append("pinged")

    react_events = await handle_message_react(message)
    events += react_events

    if hsinchu_wind.is_hsinchu_message(message):
        await hsinchu_wind.send_hsinchu_msg(message)
        events.append("hsinchu")

    if await meow_meow(message):
        events.append("meow")

    if len(events) > 0:
        await logging.log_message_event(message, events)


@client.event
async def on_guild_join(guild):
    supabaseClient.table("server_config").insert(
        {
            "guild_id": str(guild.id),
            "server_name": guild.name,
        }
    ).execute()
    register_commands(tree, client, [guild])
    await tree.sync(guild=guild)


client.run(TOKEN)
