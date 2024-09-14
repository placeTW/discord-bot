from discord import app_commands
from discord.app_commands import Choice
from bot import TWPlaceClient
import discord
from .consts import CITIES_DICT, CITIES_CHOICES
from .compare_api import compare_two_cities

def register_commands(tree, client: TWPlaceClient, guilds: list[discord.Object]):
    compare_group = app_commands.Group(name="compare", description="Price comparison commands")

    @compare_group.command(
        name="cities",
        description="Compare prices between two cities",
    )
    @app_commands.choices(city1=CITIES_CHOICES, city2=CITIES_CHOICES)
    @app_commands.describe(city1="The first city to compare", city2="The second city to compare")
    async def compare_cities(
        interaction: discord.Interaction,
        city1: Choice[str],
        city2: Choice[str],
    ):
        comparison_msg = await compare_two_cities(city1.value, city2.value)
        if comparison_msg is None:
            return await interaction.response.send_message("Sorry, we couldn't find any data ):", ephemeral=True)
        await interaction.response.send_message(comparison_msg)

    tree.add_command(compare_group, guilds=guilds)