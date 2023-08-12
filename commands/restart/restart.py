import subprocess
import sys
import discord
from discord import app_commands
import os

def register_commands(tree, this_guild: discord.Object):
  @tree.command(
      name="restart",
      description="Restarts the bot (only true admins can successfully execute this command)",
      guild=this_guild,
  )
  @app_commands.checks.has_permissions(administrator=True)
  async def restart(
      interaction: discord.Interaction,
  ):
    await interaction.response.send_message("Restarting, goodbye world")

    print("restart: Fetching from repo and installing requirements...")

    subprocess.call(["git", "pull"])
    subprocess.call(["pip", "install", "-r", "requirements.txt"])

    print("restart: Restarting...")

    os.execv(sys.executable, ['python'] + sys.argv)
