import commands.fetch_entry.fetch_entry_main as fetch
import pytest


# @pytest.mark.parametrize(
#     "entry,lang,field",
#     [
#         ("capoo", "en", "title"),
#         ("taipei_101", "lt", "title"),
#     ],
# )
@pytest.mark.parametrize("entry", ["capoo"])
@pytest.mark.parametrize("lang", ["en", "lt", "et"])
@pytest.mark.parametrize("field", ["title", "blurb", "desc", None])
async def test__fetch_entry_with_json_valid_input_returns_str(
    entry, lang, field
):
    """
    Checks that _fetch_entry_with_json returns string when
    correct input is given.
    """
    result = await fetch._fetch_entry_with_json(
        interaction=None, entry=entry, lang=lang, field=field
    )
    assert type(result) is str


@pytest.mark.parametrize("entry", ["capoo"])
@pytest.mark.parametrize("lang", ["en", "lt", "et"])
async def test__fetch_entry_with_json_valid_input_links_returns_list(
    entry, lang
):
    """
    Checks that _fetch_entry_with_json returns string when
    correct input is given.
    """
    result = await fetch._fetch_entry_with_json(
        interaction=None, entry=entry, lang=lang, field="links"
    )
    assert type(result) is list


@pytest.mark.parametrize("lang", ["aaaa", "bbbb", None, 3])
async def test__fetch_entry_with_json_invalid_lang_returns_none(lang):
    """
    Checks that _fetch_entry_with_json returns None when
    invalid input is given.
    """
    result = await fetch._fetch_entry_with_json(
        interaction=None, entry="capoo", lang=lang, field="title"
    )
    assert result is None
