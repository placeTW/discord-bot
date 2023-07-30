import aiohttp
import discord
from discord import app_commands
from .modules import async_utils, postprocess
import typing
from discord.app_commands import Choice

SUPPORTED_LANGUAGE_CODES = typing.Literal["en", "et", "lt", "lv", "zh", "fr"]
SUPPORTED_ART_FIELDS = typing.Literal["title", "blurb", "desc", "links"]

SUPPORTED_ART2023_IDS = [
    "capoo",
    "chip",
    "taipei_101",
    "tw_flag",
    "formosan_bear",
    "boba_tea_bear",
    "tw_magpie",
    "heart_baltics",
    "heart_bretons",
    "lt_pengiun_boba",
    "indep_flag",
    "tw_beer",
    "apple_cider",
    "tatung_rice_cooker",
    "tsmc_logo",
]

POSSIBLE_ART2023_IDS = [
    Choice(name=id, value=i) for i, id in enumerate(SUPPORTED_ART2023_IDS)
]


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
    async def fetch_entry(
        interaction: discord.Interaction,
        entry: Choice[int],
        lang: SUPPORTED_LANGUAGE_CODES,
        field: SUPPORTED_ART_FIELDS = None,
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
        link_to_fetch = f"https://placetw.com/locales/{lang}/art-pieces.json"
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
            result = result_json[entry.value][field]
            result = postprocess.postprocess_fetch_field(result)
            await interaction.response.send_message(
                f"The {field} for {lang} is:\n{result}", suppress_embeds=True
            )


if __name__ == "__main__":
    import asyncio

    link = "https://placetw.com/locales/en/art-pieces.json"
    asyncio.run(async_utils._async_get_json(link))
