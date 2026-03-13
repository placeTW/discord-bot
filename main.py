import os
import sys
from dotenv import load_dotenv

# Load env vars before any other imports — several modules read env vars at import time
load_dotenv()

IS_PROD = len(sys.argv) > 1 and sys.argv[1] == "prod"

import logging
logging.basicConfig(
    level=logging.DEBUG if not IS_PROD else logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

import discord
from discord import app_commands
import datetime

# user commands
from commands.basic import basic_commands
from commands.bbt_count import bbt_count
from commands.cat import cat
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
from commands.confessions import confession
from commands.stats import stats
from commands.tocfl import tocfl
from commands.formosa_stickers import formosa_stickers
from commands.taiwanese import taiwanese_entry
from commands.trains import trains
from commands.compare import compare_cmd

from activities import activity

from mentioned import mention_responses

from modules import config
import bot
from git import Repo
import platform

TOKEN = os.getenv("DISCORD_TOKEN_DEV" if not IS_PROD else "DISCORD_TOKEN")

DEPLOYMENT_DATE = datetime.datetime.now()


class BotInitialiser:
    def __init__(self):
        self.client = bot.get_bot(IS_PROD)
        self.guilds = [discord.Object(id=guild_id) for guild_id, guild_config in self.client.guilds_dict.items() if guild_config.get('prod_config') == IS_PROD]
        # CommandTree is where all our defined commands are stored
        self.tree = discord.app_commands.CommandTree(self.client)
        self.placetw_guild = discord.Object(id=os.getenv("PLACETW_SERVER_ID"))  # basically refers to this server
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

        @self.tree.command(
            name="leave-server",
            description="Make the bot leave a specified server by ID (admin only)",
            guild=self.placetw_guild,
        )
        @app_commands.checks.has_permissions(administrator=True)
        @app_commands.default_permissions(administrator=True)  # hides command from non-admins in Discord UI
        async def leave_server(interaction: discord.Interaction, guild_id: str):
            guild = self.client.get_guild(int(guild_id))
            if guild is None:
                await interaction.response.send_message("❌ Guild not found.", ephemeral=True)
                return
            await interaction.response.send_message(f"✅ Leaving **{guild.name}**...", ephemeral=True)
            await guild.leave()

        @leave_server.error
        async def leave_server_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
            if isinstance(error, app_commands.MissingPermissions):
                await interaction.response.send_message("❌ You need Administrator permissions to use this command.", ephemeral=True)


        # * register commands the just the placetw server
        edit_entry_cmd.register_commands(self.tree, self.placetw_guild, self.client)
        restart.register_commands(self.tree, self.placetw_guild)
        activity.register_commands(self.tree, self.placetw_guild, self.client)
        tocfl.register_commands(self.tree, self.placetw_guild, self.client)
        taiwanese_entry.register_commands(self.tree, self.placetw_guild, self.client)

    def register_commands_in_all_servers(self, guilds: list = None):
        # * register commands to the other servers
        target_guilds = guilds if guilds is not None else self.guilds
        
        bbt_count.register_commands(self.tree, self.client, target_guilds)
        cat.register_commands(self.tree, target_guilds)
        fetch_entry_cmd.register_commands(self.tree, target_guilds)
        fetch_entry_ui.register_commands(self.tree, target_guilds)
        one_o_one.register_commands(self.tree, target_guilds)
        hgs.register_commands(self.tree, target_guilds)
        random_shiba.register_commands(self.tree, target_guilds)
        random_capoo.register_commands(self.tree, target_guilds)
        fucking.register_commands(self.tree, target_guilds)
        basic_commands.register_commands(self.tree, target_guilds)
        config_commands.register_commands(self.tree, self.client, target_guilds)
        stats.register_commands(self.tree, self.client, target_guilds)
        pat.register_commands(self.tree, self.client, target_guilds)
        formosa_stickers.register_commands(self.tree, target_guilds)
        confession.register_commands(self.tree, self.client)
        trains.register_commands(self.tree, self.client, target_guilds)
        compare_cmd.register_commands(self.tree, self.client, target_guilds)

    def register_event_callbacks(self):
        # sync the slash commands servers when the bot is ready
        @self.client.event
        async def on_ready():
            self.tree.clear_commands(guild=None)
            await self.tree.sync()

            guilds_to_sync = self.guilds
            if self.placetw_guild not in self.guilds:
                guilds_to_sync = self.guilds + [self.placetw_guild]
            for guild in guilds_to_sync:
                await self.tree.sync(guild=guild)
            # Enable logging
            logging.init(self.client, DEPLOYMENT_DATE)
            print("Bot is ready.")

        # when someone sends any message
        @self.client.event
        async def on_message(message: discord.Message):
            message_reacts_enabled = True
            try:
                message_reacts_enabled = self.client.guilds_dict[message.guild.id]["message_reacts_enabled"]
            except (KeyError, TypeError):
                # default true - guild config may not be loaded yet
                message_reacts_enabled = True

            # don't respond to bots, bot's own posts or if message reacts are disabled
            if (message.author == self.client.user) or (not message_reacts_enabled) or message.author.bot:
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
        async def on_guild_join(guild: discord.Guild):
            print(f"Guild {guild.name} ({guild.id}) joined")
            config.create_new_config(guild.id, guild.name, IS_PROD)
            guild_obj = discord.Object(id=guild.id)
            self.guilds.append(guild_obj)
            self.register_commands_in_all_servers(guilds=[guild_obj])
            await self.tree.sync(guild=guild_obj)
  
            
        @self.client.event
        async def on_guild_remove(guild: discord.Guild):
            print(f"Guild {guild.name} ({guild.id}) removed")
            self.guilds = [g for g in self.guilds if g.id != guild.id]
            if guild.id in self.client.guilds_dict:
                del self.client.guilds_dict[guild.id]
            config.remove_config(guild.id, IS_PROD)

    def run(self):
        self.client.run(TOKEN)


if __name__ == "__main__":
    _required_vars = [
        "DISCORD_TOKEN_DEV" if not IS_PROD else "DISCORD_TOKEN",
        "PLACETW_SERVER_ID",
        "LOG_CHANNEL",
        "POSTGRES_HOST",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "GITHUB_TOKEN",
    ]
    _missing = [v for v in _required_vars if not os.getenv(v)]
    if _missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(_missing)}")

    discord_bot = BotInitialiser()
    discord_bot.run()
