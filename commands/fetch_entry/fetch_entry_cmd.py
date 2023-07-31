import aiohttp
import discord
from discord import app_commands
from ..modules import async_utils, postprocess
import typing
from discord.app_commands import Choice

from .consts import (
    POSSIBLE_ART2023_IDS,
    POSSIBLE_LANGUAGE_CODES,
    POSSIBLE_ART_FIELD_CODES,
)


async def get_json(how="url", json_url=""):
    assert how in ("url",)
    if how == "url":
        result = await async_utils._async_get_json(json_url)
    return result


def register_commands(tree, this_guild: discord.Object):
    @tree.command(
        name="fetch",
        description="Fetches r/place Taiwan art entries.",
        guild=this_guild,
    )
    @app_commands.choices(entry=POSSIBLE_ART2023_IDS)
    @app_commands.choices(lang=POSSIBLE_LANGUAGE_CODES)
    @app_commands.choices(field=POSSIBLE_ART_FIELD_CODES)
    async def fetch_entry(
        interaction: discord.Interaction,
        entry: Choice[int],
        lang: Choice[str],
        field: Choice[str] = None,
    ):
        """This function does some shit

        Args:
            interaction (discord.Interaction): idk
            entry (str): The entry to edit.
            lang (str): The language of the entry to fetch.
            field (str, optional): Field to fetch: title, blurb, description,
                or links.
                If not passed, return the entire entry.
        """
        link_to_fetch = (
            f"https://placetw.com/locales/{lang.value}/art-pieces.json"
        )
        result_json = await get_json(
            how="url",
            json_url=link_to_fetch,
        )
        # * if some error happens, notify user and stop
        if result_json is None:
            await interaction.response.send_message(
                "Sorry, your requested information is not \
                      available at the moment."
            )
            return

        if field is None:  # * return entire entry
            result = result_json[entry.value]
            result = postprocess.postprocess_fetch_item(result)
            await interaction.response.send_message(
                result, suppress_embeds=True
            )

        else:  # * return only specific field
            result = result_json[entry.value][field.value]
            result = postprocess.postprocess_fetch_field(result)
            await interaction.response.send_message(
                f"The {field.value} for {lang.value} is:\n{result}",
                suppress_embeds=True,
            )


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
