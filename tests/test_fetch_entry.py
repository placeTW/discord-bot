import commands.fetch_entry.fetch_entry_main as fetch
from modules.async_utils import _async_get_json
from commands.fetch_entry import postprocess
import pytest
from commands.entry_consts.consts import SUPPORTED_LANGUAGE_CODES, SUPPORTED_ART2023_IDS

LANGS_TO_TEST = list(SUPPORTED_LANGUAGE_CODES.keys())
ENTRIES_TO_TEST = list(SUPPORTED_ART2023_IDS.keys())

@pytest.mark.parametrize("lang", LANGS_TO_TEST)
async def test_placetw_art_schema(lang: str):
    """Tests that the API can be fetched and that the schema is correct."""
    url = f"https://placetw.com/locales/{lang}/art-pieces.json"
    result = await _async_get_json(url)
    assert type(result) is dict
    # assert that result's values has the following keys and types:
    #   "title" (str), "blurb" (str), "desc" (str), "links" (list)
    for art_name, art_dict in result.items():
        assert "title" in art_dict
        assert type(art_dict["title"]) is str
        assert "blurb" in art_dict
        assert type(art_dict["blurb"]) is str
        assert "desc" in art_dict
        assert type(art_dict["desc"]) is str
        assert "links" in art_dict
        assert type(art_dict["links"]) is list

@pytest.fixture
def mock_art_piece_json(monkeypatch):
    # mock _fetch_entry_with_json to return a dict
    async def mock_get_json(*args, **kwargs) -> dict:
        return {
            art_key : { # the contents don't matter here
                "title": art_key,
                "blurb": art_desc,
                "desc": art_desc,
                "links": ["https://nonexistent_link.com"],
            } for art_key, art_desc in SUPPORTED_ART2023_IDS.items()
        }
    monkeypatch.setattr(fetch, "get_json", mock_get_json)

@pytest.mark.parametrize("entry", ENTRIES_TO_TEST)
@pytest.mark.parametrize("lang", LANGS_TO_TEST)
@pytest.mark.parametrize("field", ["title", "blurb", "desc", None])
async def test__fetch_entry_with_json_valid_input_return_val(
    entry, lang, field, mock_art_piece_json
):
    """
    Checks that _fetch_entry_with_json returns the expected type.
    """
    # check case where field is not "links" (should return a string)
    result = await fetch._fetch_entry_with_json(
        interaction=None, entry=entry, lang=lang, field=field
    )
    assert type(result) is str

    # check case where field is "links" (should return a list instead)
    result = await fetch._fetch_entry_with_json(
        interaction=None, entry=entry, lang=lang, field="links"
    )
    assert type(result) is list

@pytest.mark.parametrize("entry,lang,field", 
    [
        ("bad_entry", "en", None),
        ("capoo", "bad_lang", "title"),
        ("capoo", "en", "bad_field"),
    ]
)
async def test__fetch_entry_with_json_invalid_input_return_val(entry, lang, field, mock_art_piece_json):
    # make sure that invalid input returns None
    result = await fetch._fetch_entry_with_json(
        interaction=None, entry=entry, lang=lang, field=field
    )
    assert result is None

@pytest.mark.xfail # need to fix get_json to return None on error
async def test__fetch_entry_with_json_error(monkeypatch):
    """
    Checks that _fetch_entry_with_json returns None when get_json returns None (i.e. error).
    """
    # monkkeypatch get_json to return None
    async def mock_get_json(*args, **kwargs):
        return None
    monkeypatch.setattr(fetch, "get_json", mock_get_json)
    result = await fetch._fetch_entry_with_json(
        interaction=None, entry="capoo", lang="en", field=None
    )
    assert result in None

def test_postprocess_fetch_field():
    assert postprocess.postprocess_fetch_field("hi") == "hi"
    assert postprocess.postprocess_fetch_field("") == ""
    assert (
        postprocess.postprocess_fetch_field(["a", "b", "c"]) == "* a\n* b\n* c"
    )


def test_postprocess_fetch_item_returns_str():
    """Since discord msgs only accept strings, this function should return only strings."""
    input_dict = {"title": "a", "blurb": "b", "desc": "c", "links": "d"}
    assert type(postprocess.postprocess_fetch_item(input_dict)) is str
