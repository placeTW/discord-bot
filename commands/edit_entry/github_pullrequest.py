from ..fetch_entry.fetch_entry_main import get_json
import asyncio
from .git_utils import (
    create_pull_request,
    get_json_file_from_repo,
    determine_file_path_on_repo,
)
import json


# note: this might need to become async
async def modify_json_and_create_pull_request(
    lang: str,  # en, lt, et, etc
    entry_id: str,  # entry INDEX (i.e., from 0 to 15)
    entry_name: str,  # entry id
    field: str,  # title, desc, etc
    proposed_text: str,
):
    # print("Fetching the relevant json file from url...")
    file_path = determine_file_path_on_repo(lang)
    the_file = get_json_file_from_repo(file_path)
    # * in case `art-pieces.json` doesn't exist:
    # *   take the english version and blank everything out
    if not the_file:
        the_json = await get_blank_json()
    else:
        # * at this point, it's a valid json
        the_json = json.loads(the_file.decoded_content.decode())
    # print("Modifying the json to reflect the changes...")
    if field == "links":
        proposed_text = process_list(proposed_text)
    the_json[entry_id][field] = proposed_text
    # print("Creating a pull request...")
    create_pull_request(lang, the_json, entry_id, field)
    # print("Done!")
    return the_json


def process_list(list_str: str):
    return list_str.split(",")


async def get_blank_json():
    default_link = "https://placetw.com/locales/en/art-pieces.json"
    default_entries = await get_json(how="url", json_url=default_link)
    for entry_id, default_entry in default_entries.items():
        default_entry["title"] = ""
        default_entry["blurb"] = ""
        default_entry["desc"] = ""
        default_entry["links"] = []
    return default_entries


if __name__ == "__main__":
    link = "https://placetw.com/locales/en/art-pieces.json"
    # for windows lol
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(
        modify_json_and_create_pull_request(
            lang="en",
            entry_id="chip",
            entry_name="ignored",
            field="links",
            proposed_text="hot,gay,sex",
        )
    )
