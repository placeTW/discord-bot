import os
import time

import discord
from discord import app_commands
from discord.ext import tasks

# from discord.ext import commands
from dotenv import load_dotenv
import datetime

# user commands
from commands.fetch_entry import fetch_entry_cmd
from commands.translation_stat import translation_stat, tr_core
from commands.fetch_entry import fetch_entry_ui
from commands.edit_entry import edit_entry_modal
from commands.edit_entry import edit_entry_cmd
from commands.one_o_one import one_o_one
from commands import hgs
import sys

# load environment vars (from .env)
load_dotenv()
prod = len(sys.argv) > 1 and sys.argv[1] == 'prod'
TOKEN = os.getenv('DISCORD_TOKEN_DEV' if not prod else 'DISCORD_TOKEN')
GUILD = os.getenv("DISCORD_GUILD")
GH_TOKEN = os.getenv("GITHUB_TOKEN")


deployment_date = datetime.datetime.now()

# setting up the bot
intents = discord.Intents.default()
# if you don't want all intents you can do discord.Intents.default()

tr_core.initialize_github(GH_TOKEN)
tr_core.apply_pr_map()


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        client.loop.call_later(30 * 60, self.bg_worker.start)

    @tasks.loop(minutes=30)
    async def bg_worker(self):
        tr_core.iter_locales()
        if tr_core.lang_require_update:
            translation_stat.register_commands(tree, this_guild)
            tree.sync(guild=this_guild)
        tr_core.scheduled_update()

    async def close(self):
        tr_core.write_pr_map()


client = MyClient(intents=intents)
tree = discord.app_commands.CommandTree(client)
this_guild = discord.Object(id=GUILD)


# ! These are basic test commands that should not exist when deployed
# * simple hi command
@tree.command(
    name="website",
    description="Responds with the placeTW website link",
    guild=this_guild,
)
async def test_slash_command(interaction: discord.Interaction):
    await interaction.response.send_message("https://placetw.com/")


# * simple echo command with param explanation
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
tr_core.iter_locales()
translation_stat.register_commands(tree, this_guild)


# sync the slash commands to server
@client.event
async def on_ready():
    await tree.sync(guild=this_guild)
    # print "ready" in the console when the bot is ready to work
    print("Bot is ready.")


client.run(TOKEN)
