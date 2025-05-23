"""
This file is where the actual fetch is happening,
so that both fetch_entry and fetch_entry_ui can use it 
"""

import discord

from commands.entry_consts.consts import I18N_JSON_URL
from modules import async_utils
from . import postprocess
from commands.entry_consts.consts import (
    SUPPORTED_LANGUAGE_CODES,
)


async def get_json(how="url", json_url="", expected_content_type='application/json') -> dict:
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
        result = await async_utils._async_get_json(json_url, expected_content_type)
    return result


async def _fetch_entry_with_json(
    interaction: discord.Interaction, entry: str, lang: str, field: str = None, fromI18n: bool = False, expected_content_type='application/json'
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

    link_to_fetch = f"{I18N_JSON_URL if fromI18n else 'https://placetw.com'}/locales/{lang}/art-pieces.json"
    result_json = await get_json(
        how="url",
        json_url=link_to_fetch,
        expected_content_type=expected_content_type
    )
    # * if some error happens, notify user and stop
    if result_json is None:
        print("Failed to fetch JSON.")
        return None
    if entry not in result_json:
        print("Entry not found.")
        return None
    if lang not in SUPPORTED_LANGUAGE_CODES.keys():
        print("Language not found.")
        return None
    if field is not None and field not in result_json[entry]:
        print("Field not found.")
        return None

    if field is None:  # * return entire entry
        result = result_json[entry]
        result = postprocess.postprocess_fetch_item(result)
        return result

    else:  # * return only specific field
        return result_json[entry][field]


async def send_fetch_response(
    interaction,
    fetched_result,
    entry: str,
    lang: str,
    field: str,
    is_ephermeral=True,  # whether to make the msg ephermeral or not
):
    # * if some error happens, notify user and stop
    if fetched_result is None:
        await interaction.response.send_message(
            "Sorry, your requested information is not available at the moment.",
            ephemeral=True,
        )
        return

    if field is None:  # * return entire entry
        await interaction.response.send_message(fetched_result, suppress_embeds=True, ephemeral=is_ephermeral)

    else:  # * return only specific field
        await interaction.response.send_message(
            f"The {field} for `{entry}` in `{lang}` is:\n{fetched_result}",
            suppress_embeds=True,
            ephemeral=is_ephermeral,
        )
