import pytest
from functions.reacts import check_resource_match

# Original Czech test cases (all retained)
POSITIVE_TEST_CASES = (
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
    # Add more original test cases here as needed
)

# Adding Mandarin test cases for Czechia
POSITIVE_TEST_CASES_MANDARIN = (
    "捷克",  # Mandarin for Czechia
)

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES + POSITIVE_TEST_CASES_MANDARIN,  # Combine all test cases
)
def test_react_czech_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
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
    POSITIVE_TEST_CASES,
)
def test_react_czech_regex_no_match(test_str: str):
    """Tests that these strings return FALSE when surrounded by text."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", resource_name='czech')

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES_MANDARIN,
)
def test_react_czech_mandarin_yes_match(test_str: str):
    """Tests that these Mandarin strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, resource_name='czech')
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", resource_name='czech')
    # * surrounded by text (ok for Mandarin)
    assert check_resource_match(f"a{test_str}b", resource_name='czech')
    assert check_resource_match(f"哈{test_str}囉", resource_name='czech')
