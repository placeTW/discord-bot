from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "<:LVTroll:1121321988854661200>",
    "<:LTTroll:1121321991262183454>",
    "<:TWTroll:1133368316908552232>",
    "<:EETroll:1121321985180446791>",
    "<:UATroll:1142824293470838854>",
    "<:lt_tw_hgs:1139647918442283038>",
    "<:lv_tw_hgs:1139660598574055514>",
    "<:et_tw_hgs:1139660507167608882>",
    "<:ua_tw_hgs:1145430238831063210>",
)

KEYWORDS_EN = (
    "HGS",
    "hot gay sex",
)

KEYWORDS_TW = (r"(?:同志)(?:激情|熱烈)(?:性愛|性交)", r"ㄏㄍㄙ")


HGS_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS_EN)})\b|{'|'.join(KEYWORDS_TW)}",
    flags=IGNORECASE | UNICODE,
)
