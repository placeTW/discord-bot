from commands.reacttw.consts import TW_REGEX
import pytest


@pytest.mark.parametrize(
    "test_str",
    (
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
    ),
)
def test_react_tw_regex_yes_match(test_str: str):
    """Tests that these strings return TRUE."""
    # * isolated string
    assert TW_REGEX.search(test_str)
    # * surrounded by spaces
    assert TW_REGEX.search(f" {test_str} ")
    # * surrounded by text
    assert TW_REGEX.search(f"a{test_str}b")
    # * to lowercase
    assert TW_REGEX.search(test_str.lower())
    # * to title case
    assert TW_REGEX.search(test_str.title())
