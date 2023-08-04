from commands.fetch_entry.fetch_entry_main import get_json


async def test_get_json_en():
    link_to_fetch = f"https://placetw.com/locales/en/art-pieces.json"
    result_json = await get_json(
        how="url",
        json_url=link_to_fetch,
    )
    assert type(result_json) == dict
    assert "capoo" in result_json
    assert "asdf" not in result_json
    for art_id, art_info in result_json.items():
        assert "title" in art_info
        assert type(art_info["title"]) == str
        assert "blurb" in art_info
        assert type(art_info["blurb"]) == str
        assert "desc" in art_info
        assert type(art_info["desc"]) == str
        assert "links" in art_info
        assert type(art_info["links"]) == list
