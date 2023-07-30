import aiohttp
import discord
from discord import app_commands
from .modules import async_utils
import typing

SUPPORTED_LANGUAGE_CODES = typing.Literal["en", "et", "lt", "lv", "zh", "fr"]
SUPPORTED_ART_FIELDS = typing.Literal["title", "blurb", "desc"]


async def get_json(how="url", json_url=""):
    assert how in ("url",)
    if how == "url":
        result = await async_utils._async_get_json(json_url)
    return result


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="fetch",
        description="Fetches r/place Taiwan art entries",
        guild=this_guild,
    )
    async def fetch_entry(
        interaction: discord.Interaction,
        index: int,
        lang: SUPPORTED_LANGUAGE_CODES,
        field: SUPPORTED_ART_FIELDS,
    ):
        """This function does some shit

        Args:
            interaction (discord.Interaction): idk
            index (int): A number. DELETE THIS
            lang (str): The language of the entry to fetch.
            field (str): The field to fetch: title, blurb or description.
        """
        link_to_fetch = f"https://placetw.com/locales/{lang}/art-pieces.json"
        result_json = await get_json(
            how="url",
            json_url=link_to_fetch,
        )
        await interaction.response.send_message(
            f"The {field} for {lang} is:\n`{result_json[index][field]}`"
        )


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
