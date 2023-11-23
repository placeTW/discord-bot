import time
import discord
from ..modules import logging
from discord import app_commands
from pathlib import Path
from random import choice
import os

PAT_DIR = Path(Path(__file__).parent, "gifs")
SELF_PAT_GIFS = Path(Path(__file__).parent, "self_pat_gifs")


def register_commands(tree, guilds: list[discord.Object]):
    @tree.command(
        name="pat",
        description="Pat",
        guilds=guilds,
    )
    @app_commands.rename(user_to_pat="member")
    async def pat(
        interaction: discord.Interaction,
        user_to_pat: discord.Member,
        text: str = None,
    ):
        # get current user id
        current_user_id = interaction.user.id

        # * These are the parts that change depending who the user is patting
        # ** Default: user pats another user
        if user_to_pat.id != current_user_id:
            # random file from the directory
            random_gif = choice(list(PAT_DIR.iterdir()))
            pat_embed_title = f"{interaction.user.display_name} pats {user_to_pat.display_name}"
            pat_content = (
                f"<@{user_to_pat.id}> get pat by <@{current_user_id}>"
            )
        # ** Case: user pats themselves
        elif user_to_pat.id == current_user_id:
            random_gif = choice(list(SELF_PAT_GIFS.iterdir()))
            pat_embed_title = (
                f"{interaction.user.display_name} pats themselves"
            )
            pat_content = (
                f"<@{current_user_id}> pats themselves for some reason"
            )
        # ^ Future case: user pats (this) bot

        # create empty embed
        embed = discord.Embed()
        # set the title of the embed
        embed.title = pat_embed_title
        embed.description = text if text else None
        embed.color = discord.Color.random()

        # add the file to the embed
        file = discord.File(random_gif)
        embed.set_image(url=f"attachment://{file.filename}")

        log_event = {
            "event": "pat",
            "author_id": current_user_id,
            "mentioned_id": user_to_pat.id,
            "metadata": {"filename": file.filename},
        }

        await logging.log_event(
            interaction, log_event, content=text, log_to_channel=False
        )

        await interaction.response.send_message(
            content=pat_content,
            embed=embed,
            file=file,
        )
