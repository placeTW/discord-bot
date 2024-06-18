import aiohttp
import discord
from discord import app_commands
from modules import async_utils, postprocess
import typing
from discord.app_commands import Choice
from .fetch_entry_main import _fetch_entry_with_json, send_fetch_response

from ..entry_consts.consts import (
    POSSIBLE_ART2023_IDS,
    POSSIBLE_LANGUAGE_CODES,
    POSSIBLE_ART_FIELD_CODES,
)


def register_commands(tree, guilds: list[discord.Object]):
    @tree.command(
        name="fetch",
        description="Fetches r/place Taiwan art entries.",
        guilds=guilds,
    )
    @app_commands.choices(entry=POSSIBLE_ART2023_IDS)
    @app_commands.choices(lang=POSSIBLE_LANGUAGE_CODES)
    @app_commands.choices(field=POSSIBLE_ART_FIELD_CODES)
    async def fetch_entry(
        interaction: discord.Interaction,
        entry: Choice[str],
        lang: Choice[str],
        field: Choice[str] = None,
    ):
        """This function fetches an entry's field as needed.
        If field is empty, the entire entry is returned.

        Args:
            interaction (discord.Interaction): required by discord.py
            entry (str): The entry to fetch.
            lang (str): The language of the entry to fetch.
            field (str, optional): Field to fetch: title, blurb, description,
                or links.
                If not passed, return the entire entry.
        """
        # * assemble values
        selected_lang = lang.value  # lang always exists
        selected_entry = entry.value  # entry always exists
        # field may not exist
        selected_field = field.value if field is not None else None

        res = await _fetch_entry_with_json(
            interaction, selected_entry, selected_lang, selected_field
        )

        await send_fetch_response(
            interaction,
            res,
            selected_entry,
            selected_lang,
            selected_field,
        )


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
