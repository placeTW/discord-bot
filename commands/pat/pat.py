import time
import discord
from ..modules import logging
from discord import app_commands
from pathlib import Path
from random import choice
import os

PAT_DIR = Path(Path(__file__).parent, 'gifs')


def register_commands(tree, guilds: list[discord.Object]):
    @tree.command(
        name="pat",
        description="Pat",
        guilds=guilds,
    )
    @app_commands.rename(user_to_pat='member')
    async def pat(interaction: discord.Interaction, user_to_pat: discord.Member, text: str = None):
        current_user_id = interaction.user.id

        # random file from the directory
        random_gif = choice(list(PAT_DIR.iterdir()))

        log_event = {
            "event": "pat",
            "author_id": current_user_id,
            "mentioned_id": user_to_pat.id,
        }
        
        # await logging.log_event(interaction, log_event, log_to_channel=False)

        embed = discord.Embed()

        # set the title of the embed
        embed.title = f"{interaction.user.display_name} pats {user_to_pat.display_name} {text if text else ''}"
        embed.color = discord.Color.random()

        # add the file to the embed
        file = discord.File(random_gif)
        embed.set_image(url=f"attachment://{file.filename}")

        await interaction.response.send_message(embed=embed, file=file)
