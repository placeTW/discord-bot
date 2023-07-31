"""
This file is where the actual fetch is happening,
so that both fetch_entry and fetch_entry_ui can use it 
"""

import discord
from ..modules import async_utils, postprocess


async def get_json(how="url", json_url=""):
    assert how in ("url",)
    if how == "url":
        result = await async_utils._async_get_json(json_url)
    return result


async def _fetch_entry_with_json(
    interaction: discord.Interaction, entry: str, lang: str, field: str = None
):
    link_to_fetch = f"https://placetw.com/locales/{lang}/art-pieces.json"
    result_json = await get_json(
        how="url",
        json_url=link_to_fetch,
    )
    # * if some error happens, notify user and stop
    if result_json is None:
        await interaction.response.send_message(
            "Sorry, your requested information is not available at the moment.",
            ephemeral=True,
        )
        return

    if field is None:  # * return entire entry
        result = result_json[entry]
        result = postprocess.postprocess_fetch_item(result)
        await interaction.response.send_message(result, suppress_embeds=True)

    else:  # * return only specific field
        result = result_json[entry][field]
        art_id = result_json[entry]["art_id"]
        result = postprocess.postprocess_fetch_field(result)
        await interaction.response.send_message(
            f"The {field} for `{art_id}` in `{lang}` is:\n{result}",
            suppress_embeds=True,
        )
