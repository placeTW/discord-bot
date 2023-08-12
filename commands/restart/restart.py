import subprocess
import sys
import discord
from discord import app_commands
import os

def register_commands(tree, this_guild: discord.Object):
  @tree.command(
      name="restart",
      description="Restarts the bot",
      guild=this_guild,
  )
  @app_commands.checks.has_permissions(administrator=True)
  async def restart(
      interaction: discord.Interaction,
  ):
    await interaction.response.send_message("Restarting, goodbye world")

    subprocess.call(["git", "pull"])

    os.execv(sys.executable, ['python'] + sys.argv)
