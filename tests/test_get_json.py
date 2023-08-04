from commands.fetch_entry.fetch_entry_main import get_json


async def test_get_json_en():
    link_to_fetch = f"https://placetw.com/locales/en/art-pieces.json"
    result_json = await get_json(
        how="url",
        json_url=link_to_fetch,
    )
