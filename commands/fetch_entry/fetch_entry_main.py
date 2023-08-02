"""
This file is where the actual fetch is happening,
so that both fetch_entry and fetch_entry_ui can use it 
"""

import discord
from ..modules import async_utils, postprocess


async def get_json(how="url", json_url="") -> dict:
    """A multi-purpose function to fetch json.
    Right now, the only source is a json url, but in case
    things cahnge in the future, we can just modify this function.

    Args:
        how (str, optional): must be 'url'. Defaults to "url".
        json_url (str, optional): the json url to fetch. Defaults to "".

    Returns:
        dict: the fetched json.
    """
    assert how in ("url",)
    if how == "url":
        result = await async_utils._async_get_json(json_url)
    return result


async def _fetch_entry_with_json(
    interaction: discord.Interaction, entry: str, lang: str, field: str = None
):
    """Function to fetch entry based on json entries.
    This is called by both the cmd and ui version of fectch_entry,
    which is why this is a separate function in the first place.
    This function also handles sending the response to the user,
    which might need to be changed in the future.

    Args:
        interaction (discord.Interaction): the discord Interaction.
        entry (int): entry to fetch.
        lang (str): the language to fetch.
        field (str, optional): field to fetch (e.g. title). Defaults to None.
    """
    # TODO: Add assert that entry, land and field are valid choices
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
        result = postprocess.postprocess_fetch_field(result)
        await interaction.response.send_message(
            f"The {field} for `{entry}` in `{lang}` is:\n{result}",
            suppress_embeds=True,
        )
