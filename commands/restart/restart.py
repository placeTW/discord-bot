import subprocess
import sys
import discord
from discord import app_commands
import os
from discord.app_commands import Choice

from commands.restart.bot_git_utils import list_of_branches


def register_commands(tree, this_guild: discord.Object):
    BRANCHES = [
        Choice(name=branch, value=branch) for branch in list_of_branches()
    ]

    @tree.command(
        name="restart",
        description="Restarts the bot (only true admins can successfully execute this command).",
        guild=this_guild,
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(branch=BRANCHES)
    @app_commands.describe(branch="The branch to deploy from (deploys from the current branch if not specified)")
    async def restart(
        interaction: discord.Interaction,
        branch: Choice[str] = None,
    ):
        await interaction.response.send_message("Restarting, goodbye world")

        print("restart: Fetching from repo and installing requirements...")

        if branch is not None:
            print(branch.value)
            subprocess.call(["git", "checkout", branch.value])
        subprocess.call(["git", "pull"])
        subprocess.call(["pip", "install", "-r", "requirements.txt"])

        print("restart: Restarting...")

        os.execv(sys.executable, ['python'] + sys.argv)
