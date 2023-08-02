from ..fetch_entry.fetch_entry_main import get_json
import asyncio
from .git_utils import create_pull_request


# note: this might need to become async
async def modify_json_and_create_pull_request(
    lang: str,  # en, lt, et, etc
    entry_id: str,  # entry INDEX (i.e., from 0 to 15)
    entry_name: str,  # entry id
    field: str,  # title, desc, etc
    proposed_text: str,
):
    print("Fetching the relevant json file from url...")
    json_url = f"https://placetw.com/locales/{lang}/art-pieces.json"
    the_json = await get_json(how="url", json_url=json_url)
    # * in case `art-pieces.json` doesn't exist:
    # *   take the english version and blank everything out
    if not the_json:
        # print("failed to find such lang file, returning blank version")
        the_json = await get_blank_json()

    print("Modifying the json to reflect the changes...")
    if field == "links":
        proposed_text = process_list(proposed_text)
    the_json[entry_id][field] = proposed_text
    # print(the_json[entry_id])
    print("Creating a pull request...")
    create_pull_request(lang, the_json, entry_id, field)
    print("Done!")
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
