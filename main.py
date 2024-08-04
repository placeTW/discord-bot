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
from functions.reacts import handle_message_react
from modules import logging
from commands.one_o_one import one_o_one
from commands import hgs
from commands.pat import pat
from commands.shiba import random_shiba
from commands.capoo import random_capoo
from commands.restart import restart
from commands.fucking import fucking
from commands.boba import boba
from commands.confessions import confession
from commands.stats import stats
from commands.tocfl import tocfl
from commands.formosa_stickers import formosa_stickers
from commands.taiwanese import taiwanese_entry

from activities import activity

from mentioned import mention_responses

from modules.supabase import supabaseClient
from modules import config
import bot
import sys
from git import Repo
import platform

# load environment vars (from .env)
load_dotenv()
IS_PROD = len(sys.argv) > 1 and sys.argv[1] == "prod"
TOKEN = os.getenv("DISCORD_TOKEN_DEV" if not IS_PROD else "DISCORD_TOKEN")

DEPLOYMENT_DATE = datetime.datetime.now()

class BotInitialiser:
    def __init__(self):
        self.client = bot.get_bot(IS_PROD)
        self.guilds = [
            discord.Object(id=int(server_id))
            for server_id in self.client.guilds_dict.keys()
        ]
        # CommandTree is where all our defined commands are stored
        self.tree = discord.app_commands.CommandTree(self.client)
        self.placetw_guild = discord.Object(
            id=os.getenv("PLACETW_SERVER_ID")
        )  # basically refers to this server
        self.register_commands()

    def register_commands(self):
        self.register_placetw_commands()
        self.register_commands_in_all_servers()
        self.register_event_callbacks()


    def register_placetw_commands(self):
        @self.tree.command(
            name="deployment-info",
            description="Returns information about the bot deployment",
            guild=self.placetw_guild,
        )
        async def deployment_info(interaction: discord.Interaction):
            branch_name = Repo().active_branch.name
            msg_list = [
                f"PlaceTW discord bot ({'prod' if IS_PROD else 'dev'} deployment)",
                f"Branch deployed: `{branch_name}`",
                f"Python version: `{platform.python_version()}`",
                f"Operating system: `{platform.platform()}`",
                f"Deployed on `{DEPLOYMENT_DATE.ctime()} ({DEPLOYMENT_DATE.astimezone().tzinfo})`",
                f"https://github.com/placeTW/discord-bot{f'/tree/{branch_name}' if branch_name != 'main' else ''}",
            ]
            msg = "\n".join(msg_list)
            await interaction.response.send_message(msg)


        # * register commands the just the placetw server
        edit_entry_cmd.register_commands(self.tree, self.placetw_guild, self.client)
        restart.register_commands(self.tree, self.placetw_guild)
        activity.register_commands(self.tree, self.placetw_guild, self.client)
        tocfl.register_commands(self.tree, self.placetw_guild, self.client)
        taiwanese_entry.register_commands(self.tree, self.placetw_guild, self.client)

    def register_commands_in_all_servers(self):
        # * register commands to the other servers
        bbt_count.register_commands(self.tree, self.client, self.guilds)
        fetch_entry_cmd.register_commands(self.tree, self.guilds)
        fetch_entry_ui.register_commands(self.tree, self.guilds)
        one_o_one.register_commands(self.tree, self.guilds)
        hgs.register_commands(self.tree, self.guilds)
        random_shiba.register_commands(self.tree, self.guilds)
        random_capoo.register_commands(self.tree, self.guilds)
        fucking.register_commands(self.tree, self.guilds)
        boba.register_commands(self.tree, self.guilds)
        basic_commands.register_commands(self.tree, self.guilds)
        config_commands.register_commands(self.tree, self.client, self.guilds)
        stats.register_commands(self.tree, self.client, self.guilds)
        pat.register_commands(self.tree, self.client, self.guilds)
        formosa_stickers.register_commands(self.tree, self.guilds)
        confession.register_commands(self.tree, self.client)

    def register_event_callbacks(self):
        # sync the slash commands servers when the bot is ready
        @self.client.event
        async def on_ready():
            for guild_id in self.client.guilds_dict.keys():
                guild = discord.Object(id=guild_id)
                await self.tree.sync(guild=guild)
            # Enable logging
            logging.init(self.client, DEPLOYMENT_DATE)
            print("Bot is ready.")


        # when someone sends any message
        @self.client.event
        async def on_message(message: discord.Message):
            message_reacts_enabled = True
            try:
                message_reacts_enabled = self.client.guilds_dict[message.guild.id][
                    "message_reacts_enabled"
                ]
            except:
                # default true
                pass

            # don't respond to bot's own posts or if message reacts are disabled
            if message.author == self.client.user or not message_reacts_enabled or message.author.bot:
                return

            events = []

            if self.client.user.mentioned_in(message):  # if bot is pinged in message
                await mention_responses.reply_with_random_response(message)
                events.append("pinged")

            react_events = await handle_message_react(message)
            events += react_events

            if len(events) > 0:
                await logging.log_message_event(message, events)


        @self.client.event
        async def on_guild_join(guild):
            supabaseClient.table("server_config").insert(
                {
                    "guild_id": str(guild.id),
                    "server_name": guild.name,
                }
            ).execute()
            self.register_commands(self.tree, self.client, [guild])
            await self.tree.sync(guild=guild)
    

    def run(self):
        self.client.run(TOKEN)

if __name__ == "__main__":
    discord_bot = BotInitialiser()
    discord_bot.run()