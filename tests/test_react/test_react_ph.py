from commands.react_ph.consts import PH_REGEX
import pytest

POSTITIVE_TEST_CASES = ("Taga-Taiwan",)


@pytest.mark.parametrize(
    "test_str",
    POSTITIVE_TEST_CASES,
)
def test_react_baltics_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert PH_REGEX.search(test_str)
    # * surrounded by spaces
    assert PH_REGEX.search(f" {test_str} ")
    # * to lowercase
    assert PH_REGEX.search(test_str.lower())
    # * to title case
    assert PH_REGEX.search(test_str.title())


@pytest.mark.parametrize(
    "test_str",
    POSTITIVE_TEST_CASES,
)
def test_react_baltics_regex_no_match(test_str: str):
    """Tests that these strings return FALSE."""
    # * surrounded by text
    assert not PH_REGEX.search(f"a{test_str}b")
