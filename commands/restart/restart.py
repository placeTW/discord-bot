from pathlib import Path
import subprocess
import sys
import discord
from discord import app_commands
import os
from discord.app_commands import Choice

from commands.restart.bot_git_utils import list_of_branches

RESTART_GIF = Path(Path(__file__).parent, "upload-cat.gif")

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
        embed = discord.Embed(
            title="Restarting...",
            description=f"Restarting{(f' and deploying `{branch.value}`' if branch is not None else '')}, goodbye world",
            color=discord.Color.red(),
        )
        file = discord.File(RESTART_GIF)
        embed.set_image(url=f"attachment://{file.filename}")

        await interaction.response.send_message(embed=embed, file=file)

        print("restart: Fetching from repo and installing requirements...")

        if branch is not None:
            print(branch.value)
            subprocess.call(["git", "checkout", branch.value])
        subprocess.call(["git", "pull"])
        subprocess.call(["pip", "install", "-r", "requirements.txt"])

        print("restart: Restarting...")

        os.execv(sys.executable, ['python'] + sys.argv)
