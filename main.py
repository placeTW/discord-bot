import os

import discord
from discord import app_commands
from discord.ext import tasks

# from discord.ext import commands
from dotenv import load_dotenv

# user commands
from commands.fetch_entry import fetch_entry_cmd
from commands.translation_stat import translation_stat
from commands import hgs

# load environment vars
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
GH_TOKEN = os.getenv("GITHUB_TOKEN", None)


# setting up the bot
intents = discord.Intents.default()
# if you don't want all intents you can do discord.Intents.default()

translation_stat.load_pr_map()
translation_stat.initialize_github(GH_TOKEN)
translation_stat.trans_db_lock.acquire()


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        print("MY CLINET SETUP HOOK")
        self.bg_worker.start()

    @tasks.loop(hours=1)
    async def bg_worker(self):
        print("MyCLIENT TASK RUN")
        translation_stat.update_repo()

    @bg_worker.after_loop
    async def write_pr_file(self):
        translation_stat.write_pr_map()


client = MyClient(intents=intents)
tree = discord.app_commands.CommandTree(client)
this_guild = discord.Object(id=GUILD)


# sync the slash command to server
@client.event
async def on_ready():
    # register commands from other files
    fetch_entry_cmd.register_commands(tree, this_guild)
    hgs.register_commands(tree, this_guild)
    translation_stat.register_commands(tree, this_guild)
    await tree.sync(guild=this_guild)
    # print "ready" in the console when the bot is ready to work
    print("READYYYYY")


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


client.run(TOKEN)
