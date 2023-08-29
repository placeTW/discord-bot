from commands.reacttw.consts import TW_REGEX
import pytest

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
    assert TW_REGEX.search(test_str)
    # * surrounded by spaces
    assert TW_REGEX.search(f" {test_str} ")
    # * to lowercase
    assert TW_REGEX.search(test_str.lower())
    # * to title case
    assert TW_REGEX.search(test_str.title())


@pytest.mark.parametrize(
    "test_str",
    TEST_CASE_TW,
)
def test_react_tw_tw_regex_yes_match(test_str: str):
    """Tests that these English strings return TRUE."""
    # * isolated string
    assert TW_REGEX.search(test_str)
    # * surrounded by text (ok for 漢字)
    assert TW_REGEX.search(f"哈{test_str}囉")
    assert TW_REGEX.search(f"a{test_str}b")
    # * surrounded by spaces (半形＋全形)
    assert TW_REGEX.search(f" {test_str} ")
    assert TW_REGEX.search(f"　{test_str}　")


@pytest.mark.parametrize(
    "test_str",
    TEST_CASE_EN,
)
def test_react_tw_regex_no_match(test_str: str):
    """Tests that these strings return FALSE."""
    # * surrounded by text
    assert not TW_REGEX.search(f"a{test_str}b")
