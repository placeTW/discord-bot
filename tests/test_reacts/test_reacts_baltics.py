from functions.reacts import check_resource_match
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
    # Estonian singular
    # "Taiwan",
    "Taiwanlane",
    "Taiwanlase",
    "Taiwani",
    "Taiwanlast",
    "Taiwanisse",
    "Taiwanlasse",
    "Taiwanis",
    "Taiwanlases",
    "Taiwanist",
    "Taiwanlasest",
    "Taiwanile",
    "Taiwanlasele",
    "Taiwanil",
    "Taiwanlasel",
    "Taiwanilt",
    "Taiwanlaselt",
    "Taiwaniks",
    "Taiwanlaseks",
    "Taiwanini",
    "Taiwanlaseni",
    "Taiwanina",
    "Taiwanlasena",
    "Taiwanita",
    "Taiwanlaseta",
    "Taiwaniga",
    # Estonian plural
    "Taiwanid",
    "Taiwanlased",
    "Taiwanide",
    "Taiwanlaste",
    "Taiwanisid",
    "Taiwanlasi",
    "Taiwanidesse",
    "Taiwanlastesse",
    "Taiwanides",
    "Taiwanlastes",
    "Taiwanidest",
    "Taiwanlastest",
    "Taiwanidele",
    "Taiwanlastele",
    "Taiwanidel",
    "Taiwanlastel",
    "Taiwanidelt",
    "Taiwanlastelt",
    "Taiwanideks",
    "Taiwanlasteks",
    "Taiwanideni",
    "Taiwanlasteni",
    "Taiwanidena",
    "Taiwanlastena",
    "Taiwanideta",
    "Taiwanlasteta",
    "Taiwanidega",
    "Taiwanlastega",
)

TEST_CASES_TW = ("立陶宛", "拉脫維亞", "愛沙尼亞")


@pytest.mark.parametrize(
    "test_str",
    TEST_CASES,
)
def test_react_baltics_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, "baltics")
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", "baltics")
    # * to lowercase
    assert check_resource_match(test_str.lower(), "baltics")
    # * to title case
    assert check_resource_match(test_str.title(), "baltics")


@pytest.mark.parametrize(
    "test_str",
    TEST_CASES_TW,
)
def test_react_baltics_regex_tw_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, "baltics")
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", "baltics")
    # * surrounded by text
    assert check_resource_match(f"a{test_str}b", "baltics")
    assert check_resource_match(f"哈{test_str}囉", "baltics")


@pytest.mark.parametrize(
    "test_str",
    TEST_CASES,
)
def test_react_baltics_regex_no_match(test_str: str):
    """Tests that these strings return FALSE."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", "baltics")
