import pytest
from functions.reacts import check_resource_match

TEST_CASE_EN = (
    "TAIWAN",
    "FORMOSA",
    "TAIPEI",
    "TAOYUAN",
    "TAICHUNG",
    "TAINAN",
    "KAOHSIUNG",
    "MIAOLI",
    "CHANGHUA",
    "NANTOU",
    "YUNLIN",
    "PINGTUNG",
    "YILAN",
    "HUALIEN",
    "TAITUNG",
    "PENGHU",
    "KINMEN",
    "LIENCHIANG",
    "KEELUNG",
    "HSINCHU",
    "CHIAYI",
)

TEST_CASE_TW = (
    "台灣",
    "臺灣",
    "臺北",
    "台北",
    "新北",
    "桃園",
    "臺中",
    "台中",
    "臺南",
    "台南",
    "高雄",
    "新竹",
    "苗栗",
    "彰化",
    "南投",
    "雲林",
    "嘉義",
    "屏東",
    "宜蘭",
    "花蓮",
    "臺東",
    "台東",
    "澎湖",
    "金門",
    "連江",
    "基隆",
    "新竹",
    "嘉義",
    "美麗島",
)

ALL_TEST_CASES = TEST_CASE_EN + TEST_CASE_TW


@pytest.mark.parametrize(
    "test_str",
    TEST_CASE_EN,
)
def test_react_tw_en_regex_yes_match(test_str: str):
    """Tests that these English strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, resource_name='tw')
    # * surrounded by spaces
    assert check_resource_match(f" {test_str} ", resource_name='tw')
    # * to lowercase
    assert check_resource_match(test_str.lower(), resource_name='tw')
    # * to title case
    assert check_resource_match(test_str.title(), resource_name='tw')


@pytest.mark.parametrize(
    "test_str",
    TEST_CASE_TW,
)
def test_react_tw_tw_regex_yes_match(test_str: str):
    """Tests that these English strings return TRUE."""
    # * isolated string
    assert check_resource_match(test_str, resource_name='tw')
    # * surrounded by text (ok for 漢字)
    assert check_resource_match(f"哈{test_str}囉", resource_name='tw')
    assert check_resource_match(f"a{test_str}b", resource_name='tw')
    # * surrounded by spaces (半形＋全形)
    assert check_resource_match(f" {test_str} ", resource_name='tw')
    assert check_resource_match(f"　{test_str}　", resource_name='tw')


@pytest.mark.parametrize(
    "test_str",
    TEST_CASE_EN,
)
def test_react_tw_regex_no_match(test_str: str):
    """Tests that these strings return FALSE."""
    # * surrounded by text
    assert not check_resource_match(f"a{test_str}b", resource_name='tw')
