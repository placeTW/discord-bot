from commands.react_baltics.consts import BALTIC_REGEX
import pytest

TEST_CASES = (
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
)

TEST_CASES_TW = ("立陶宛", "拉脫維亞")


@pytest.mark.parametrize(
    "test_str",
    TEST_CASES,
)
def test_react_baltics_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert BALTIC_REGEX.search(test_str)
    # * surrounded by spaces
    assert BALTIC_REGEX.search(f" {test_str} ")
    # * to lowercase
    assert BALTIC_REGEX.search(test_str.lower())
    # * to title case
    assert BALTIC_REGEX.search(test_str.title())


@pytest.mark.parametrize(
    "test_str",
    TEST_CASES_TW,
)
def test_react_baltics_regex_tw_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert BALTIC_REGEX.search(test_str)
    # * surrounded by spaces
    assert BALTIC_REGEX.search(f" {test_str} ")
    # * surrounded by text
    assert BALTIC_REGEX.search(f"a{test_str}b")
    assert BALTIC_REGEX.search(f"哈{test_str}囉")


@pytest.mark.parametrize(
    "test_str",
    TEST_CASES,
)
def test_react_baltics_regex_no_match(test_str: str):
    """Tests that these strings return FALSE."""
    # * surrounded by text
    assert not BALTIC_REGEX.search(f"a{test_str}b")
