from commands.reacttw.consts import TW_REGEX
import pytest


@pytest.mark.parametrize(
    "test_str",
    (
        # Lithuanian
        "Taivanas",
        "Taivane",
        "Taivano",
        "Taivanui",
        "Taivanietis",
        "Taivanietė",
        "Taivaniečiai",
        "Taivaniečiu",
        "Taivaniečių",
        "Taivaniečiui",
        "Taivaniečiams",
        "Taivanietiškas",
        "Taivana",
        # Latvian
        "Taivāna",
        "Taivānā",
        "Taivānas",
        "Taivānai",
        "Taivānu",
        "Taivānietis",
        "Taivāniete",
        "Taivānisks",
        "Taivāniešu",
        "Taivānietim",
        "Taivānietei",
        "Taivāniešiem",
        "Taivānieti",
        "Taivāniete",
        "Taivānieši",
        "Taivānietes",
        "Taivānieši",
        # ! Estonian (STILL MISSING)
    ),
)
def test_react_tw_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert TW_REGEX.search(test_str)
    # * surrounded by spaces
    assert TW_REGEX.search(f" {test_str} ")
    # * surrounded by text
    assert TW_REGEX.search(f"a{test_str}b")
    # * to lowercase
    assert TW_REGEX.search(test_str.lower())
    # * to title case
    assert TW_REGEX.search(test_str.title())
