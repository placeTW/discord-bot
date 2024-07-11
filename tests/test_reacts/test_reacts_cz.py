import pytest
from functions.reacts import check_resource_match

POSTITIVE_TEST_CASES = (
    # variant
    "Tchaj-wan",
    "Tchaj-wany",
    "Tchaj-wanu",
    "Tchaj-wanů",
    "Tchaj-wanům",
    "Tchaj-wane",
    "Tchaj-waně",
    "Tchaj-wanech",
    "Tchaj-wanem",
    "Tchaj-wanský",
    "Tchaj-wansky",
    "Tchaj-wanec",
    "Tchaj-wanka",
    # variant
    "Tchajwan",
    "Tchajwany",
    "Tchajwanu",
    "Tchajwanů",
    "Tchajwanům",
    "Tchajwane",
    "Tchajwaně",
    "Tchajwanech",
    "Tchajwanem",
    "Tchajwanský",
    "Tchajwansky",
    "Tchajwanec",
    "Tchajwanka",
    # variant
    "Tchaj-van",
    "Tchaj-vany",
    "Tchaj-vanu",
    "Tchaj-vanů",
    "Tchaj-vanům",
    "Tchaj-vane",
    "Tchaj-vaně",
    "Tchaj-vanech",
    "Tchaj-vanem",
    "Tchaj-vanský",
    "Tchaj-vansky",
    "Tchaj-vanec",
    "Tchaj-vanka",
    # variant
    "Tchajvan",
    "Tchajvany",
    "Tchajvanu",
    "Tchajvanů",
    "Tchajvanům",
    "Tchajvane",
    "Tchajvaně",
    "Tchajvanech",
    "Tchajvanem",
    "Tchajvanský",
    "Tchajvansky",
    "Tchajvanec",
    "Tchajvanka",
    # variant
    "Tajvan",
    "Tajvany",
    "Tajvanu",
    "Tajvanů",
    "Tajvanům",
    "Tajvane",
    "Tajvaně",
    "Tajvanech",
    "Tajvanem",
    "Tajvanský",
    "Tajvansky",
    "Tajvanec",
    "Tajvanka",
    # variant
    "Tajwan",
    "Tajwany",
    "Tajwanu",
    "Tajwanů",
    "Tajwanům",
    "Tajwane",
    "Tajwaně",
    "Tajwanech",
    "Tajwanem",
    "Tajwanský",
    "Tajwansky",
    "Tajwanec",
    "Tajwanka",
)


@pytest.mark.parametrize(
    "test_str",
    POSTITIVE_TEST_CASES,
)
def test_react_czech_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # assert False  # ! add the remaining test cases!!
    # * isolated string
    assert check_resource_match(test_str, resource_name='czech')
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", resource_name='czech')
    # * to lowercase
    assert check_resource_match(test_str.lower(), resource_name='czech')
    # * to title case
    assert check_resource_match(test_str.title(), resource_name='czech')


@pytest.mark.parametrize(
    "test_str",
    POSTITIVE_TEST_CASES,
)
def test_react_czech_regex_no_match(test_str: str):
    """Tests that these strings return FALSE."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", resource_name='czech')
