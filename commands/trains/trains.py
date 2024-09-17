from modules import logging
from discord import app_commands
from discord.app_commands import Choice
from pathlib import Path
from random import choice
from bot import TWPlaceClient
import os
import discord
from .consts import TRAINS_CHOICES, TRAINS_DICT

def register_commands(tree, client: TWPlaceClient, guilds: list[discord.Object]):
    @tree.command(
        name="trains",
        description="Get map of a train system",
        guilds=guilds,
    )
    @app_commands.choices(city=TRAINS_CHOICES)
    @app_commands.describe(city="The train system to get the map of")
    async def get_train_map(
        interaction: discord.Interaction,
        location: Choice[str],
    ):
        """This function fetches the train map of a given location.

        Args:
            interaction (discord.Interaction): required by discord.py
            location (str): The location of the train system to get the map of
        """
        # get the selected city
        selected_city = location.value
        # get the path to the url
        img_url = TRAINS_DICT[selected_city]
        # send the url (not an image)
        await interaction.response.send_message(img_url)