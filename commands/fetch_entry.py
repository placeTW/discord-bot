import aiohttp
import discord
from discord import app_commands
from .modules import async_utils


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="fetch",
        description="Fetches something idk",
        guild=this_guild,
    )
    @app_commands.describe(index="a number between 0 and 15")
    async def fetch_entry(interaction: discord.Interaction, index: int):
        result_json = await async_utils._async_get_json(
            "https://placetw.com/locales/en/art-pieces.json"
        )
        await interaction.response.send_message(
            f"Here: `{result_json[index]['title']}`"
        )


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
