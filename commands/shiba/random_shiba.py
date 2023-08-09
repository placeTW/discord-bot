import discord
from ..modules.async_utils import _async_get_json


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="shiba",
        description="Shiba",
        guild=this_guild,
    )
    async def random_shiba(
        interaction: discord.Interaction,
    ):
        shiba_json = await _async_get_json(
            "https://dog.ceo/api/breed/shiba/images/random"
        )
        if shiba_json is None or shiba_json["status"] != "success":  # ):
            return await interaction.response.send_message(
                "Sorry, we couldn't find any dogs ):"
            )
        await interaction.response.send_message(shiba_json["message"])
