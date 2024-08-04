import discord
from modules.async_utils import _async_get_json
from random import choice

POSSIBLE_BREEDS = (
    "https://dog.ceo/api/breed/shiba/images/random",
    "https://dog.ceo/api/breed/akita/images/random",
)


async def get_shiba(link):
    return await _async_get_json(link)


def register_commands(tree, guilds: list[discord.Object]):
    @tree.command(
        name="doge",
        description="Random Shiba or Akita image",
        guilds=guilds,
    )
    async def random_shiba(
        interaction: discord.Interaction,
    ):
        link = choice(POSSIBLE_BREEDS)
        shiba_json = await get_shiba(link)
        if shiba_json is None or shiba_json["status"] != "success":  # ):
            return await interaction.response.send_message("Sorry, we couldn't find any dogs ):")
        await interaction.response.send_message(shiba_json["message"])
