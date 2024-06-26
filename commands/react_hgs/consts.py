from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS_HGS = [  # must be a list to be shuffleable
    "<:lt_tw_hgs:1139647918442283038>",
    "<:lv_tw_hgs:1139660598574055514>",
    "<:et_tw_hgs:1139660507167608882>",
    "<:ua_tw_hgs:1145430238831063210>",
]
POSSIBLE_REACTS_TROLLS = [
    "<:roc_troll:1133368648967405610>",
    "<:LVTroll:1121321988854661200>",
    "<:LTTroll:1121321991262183454>",
    "<:EETroll:1121321985180446791>",
    "<:UATroll:1142824293470838854>",
]

KEYWORDS_EN = [
    "HGS",
    "hot gay sex",
]

KEYWORDS_LT = [r"kar[šs]tas\s+g[ėe]j[ųu]\s+seksas"]

KEYWORDS_LV = [r"(?:Dedzīgs|Kaislīgs)\s+geju\s+sekss"]

KEYWORDS_EE = [r"Kuum gei seks"]

KEYWORDS_UA = [r"гарячий\s+гей\s+секс"]

KEYWORDS_TW = [r"(?:激情|熱烈)(?:同志|同性)(?:性愛|性交)", r"ㄏㄍㄙ"]

HGS_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS_EN + KEYWORDS_LT + KEYWORDS_LV + KEYWORDS_EE + KEYWORDS_UA)})\b|{'|'.join(KEYWORDS_TW)}",
    flags=IGNORECASE | UNICODE,
)
