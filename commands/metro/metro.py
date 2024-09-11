from modules import logging
from discord import app_commands
from discord.app_commands import Choice
from pathlib import Path
from random import choice
from bot import TWPlaceClient
import os
import discord
from .consts import METRO_CHOICES, METRO_DICT

def register_commands(tree, client: TWPlaceClient, guilds: list[discord.Object]):
    @tree.command(
        name="trains",
        description="Get map of a train system",
        guilds=guilds,
    )
    @app_commands.choices(city=METRO_CHOICES)
    @app_commands.describe(city="The train system to get the map of")
    async def metro_cmd(
        interaction: discord.Interaction,
        city: Choice[str],
    ):
        """This function fetches the map of a metro station.

        Args:
            interaction (discord.Interaction): required by discord.py
            city (str): The city of the metro station to fetch.
        """
        # get the selected city
        selected_city = city.value
        # get the path to the url
        img_url = METRO_DICT[selected_city]
        # send the url (not an image)
        await interaction.response.send_message(img_url)