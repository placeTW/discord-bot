from commands.tocfl.chewing import to_chewing
import pytest

@pytest.mark.parametrize(
    "pinyin, expected_chewing",
    [
        ("duìwŭ", "ㄉㄨㄟˋㄨˇ"),
        ("nóng", "ㄋㄨㄥˊ"),
        ("mínzhŭ", "ㄇㄧㄣˊㄓㄨˇ"),
    ]
)
def test_to_chewing(pinyin, expected_chewing):
    assert to_chewing(pinyin).replace("\u3000", "") == expected_chewing # remove spaces