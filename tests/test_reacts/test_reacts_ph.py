from functions.reacts import check_resource_match
import pytest

POSTITIVE_TEST_CASES = ("Taga-Taiwan",)


@pytest.mark.parametrize(
    "test_str",
    POSTITIVE_TEST_CASES,
)
def test_react_ph_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, "ph")
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", "ph")
    # * to lowercase
    assert check_resource_match(test_str.lower(), "ph")
    # * to title case
    assert check_resource_match(test_str.title(), "ph")


@pytest.mark.parametrize(
    "test_str",
    POSTITIVE_TEST_CASES,
)
def test_react_ph_regex_no_match(test_str: str):
    """Tests that these strings return FALSE."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", "ph")
