import pytest
from functions.reacts import check_resource_match

# Existing Czech test cases
POSITIVE_TEST_CASES_CZECH = (
    # Czech variants (existing test cases)
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
    # Czech variants without hyphen (existing test cases)
    "Tchajvan",
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
    # Other existing Czech variants...
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
)

# New Mandarin test case for Czechia
POSITIVE_TEST_CASES_MANDARIN = (
    "捷克",
)

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES_CZECH,
)
def test_react_czech_regex_yes_match(test_str: str):
    """Tests that these Czech strings return TRUE."""
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

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES_CZECH,
)
def test_react_czech_regex_no_match(test_str: str):
    """Tests that these Czech strings return FALSE when surrounded by text."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", resource_name='czech')
