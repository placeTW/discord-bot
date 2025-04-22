import pytest
from functions.reacts import check_resource_match

# Ukrainian Test Cases from ua.json's keywords
POSITIVE_TEST_CASES = (
    "Тайвань",
    "Тайваню",
    "Тайваневі",
    "Тайванем",
    "Тайваню",
    "Тайвані",
    "тайванський",
    "тайванського",
    "тайванський",
    "тайванському",
    "тайванським",
    "тайванському",
    "тайванськім",
    "тайванське",
    "тайванському",
    "тайванська",
    "тайванську",
    "тайванської",
    "тайванській",
    "тайванською",
    "тайванські",
    "тайванських",
    "тайванським",
    "тайванськими"
    # Add more original test cases here as needed
)

# Adding Mandarin test cases for Ukraine
POSITIVE_TEST_CASES_MANDARIN = (
    "烏克蘭",  # Mandarin for Ukraine 
)

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES + POSITIVE_TEST_CASES_MANDARIN,  # Combine all test cases
)
def test_react_ukrainian_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, resource_name='ua')
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", resource_name='ua')
    # * to lowercase
    assert check_resource_match(test_str.lower(), resource_name='ua')
    # * to title case
    assert check_resource_match(test_str.title(), resource_name='ua')

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES,
)
def test_react_czech_regex_no_match(test_str: str):
    """Tests that these strings return FALSE when surrounded by text."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", resource_name='ua')

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES_MANDARIN,
)
def test_react_czech_mandarin_yes_match(test_str: str):
    """Tests that these Mandarin strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, resource_name='ua')
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", resource_name='ua')
    # * surrounded by text (ok for Mandarin)
    assert check_resource_match(f"a{test_str}b", resource_name='ua')
    assert check_resource_match(f"哈{test_str}囉", resource_name='ua')
