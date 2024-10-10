import pytest
from functions.reacts import check_resource_match
POSITIVE_TEST_CASES = (
    "HGS",
    "hot gay sex",
    "karstas geju seksas",
    "karštas geju seksas",
    "karstas gėju seksas",
    "karštas gėju seksas",
    "karstas gejų seksas",
    "karštas gejų seksas",
    "karstas gėjų seksas",
    "karštas gėjų seksas",
    "dedzīgs geju sekss",
    "kaislīgs geju sekss",
    "karsts geju sekss",
    "Kuum gei seks",
    "гарячий гей секс",
)

POSITIVE_TEST_CASES_MANDARIN = (
    "激情同志性愛",
    "激情同志性交",
    "激情同性性愛",
    "激情同性性交",
    "熱烈同志性愛",
    "熱烈同志性交",
    "熱烈同性性愛",
    "熱烈同性性交",
    "ㄏㄍㄙ",
)


@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES + POSITIVE_TEST_CASES_MANDARIN,
)

def test_react_hgs_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, resource_name='hgs')
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", resource_name='hgs')
    # * to lowercase
    assert check_resource_match(test_str.lower(), resource_name='hgs')
    # * to title case
    assert check_resource_match(test_str.title(), resource_name='hgs')

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES,
)
def test_react_hgs_regex_no_match(test_str: str):
    """Tests that these strings return FALSE when surrounded by text."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", resource_name='hgs')

@pytest.mark.parametrize(
    "test_str",
    POSITIVE_TEST_CASES_MANDARIN,
)
def test_react_hgs_mandarin_yes_match(test_str: str):
    """Tests that these Mandarin strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, resource_name='hgs')
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", resource_name='hgs')
    # * surrounded by text (ok for Mandarin)
    assert check_resource_match(f"a{test_str}b", resource_name='hgs')
    assert check_resource_match(f"哈{test_str}囉", resource_name='hgs')