from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "<:tw_baltics_heart:1132524940587962388>",
    "<:bubblemilktea:1132632348651966596>",
    # "<:chaos:1140296704516706315>",
)

LT_REGEX_STR = r"Taivan(?:as|a|e|o|ui|ie(?:tiškas|tis|tė|či(?:ų|u|ai|ui|ams)))"
LT_REGEX_STR_TW = "立陶宛"
LT_REACTS = (
    "<:lt_tw_hgs:1139647918442283038>",
    "<:LTAmong:1089490466409549844>",
)

LV_REGEX_STR = (
    r"Taivān(?:a|ā|ai|as|u|isks|ie(?:tis|te|šu|tim|tei|šiem|ti|te|ši|tes|ši))"
)
LV_REGEX_STR_TW = "拉脫維亞"
LV_REACTS = (
    "<:lv_tw_hgs:1139660598574055514>",
    "<:LVAmong:1089490467617505433>",
)

ET_REGEX_STR = r"Taiwan(?:l(?:ane|as(?:e|t|te(?:sse|s|st|le|l|lt|ks|ni|na|ta|ga)?|i|se(?:l)|se|e(?:s|l|st|le|lt|ks|ni|na|ta|d)))|i(?:d|sse|s|st|le|l|lt|ks|ni|na|ta|ga||sid|(?:de(?:sse|s|st|le|lt|l|ni|na|ks|e|ta|ga)?))?)"
ET_REGEX_STR_TW = "愛沙尼亞"
ET_REACTS = (
    "<:et_tw_hgs:1139660507167608882>",
    "<:EEAmong:1089490464102682664>",
)


KEYWORDS = (
    # Lithuanian
    LT_REGEX_STR,
    # Latvian
    LV_REGEX_STR,
    # Estonian
    ET_REGEX_STR,
)

LT_REGEX = compile(
    rf"\b(?:{LT_REGEX_STR})\b|{LT_REGEX_STR_TW}", flags=IGNORECASE | UNICODE
)
LV_REGEX = compile(
    rf"\b(?:{LV_REGEX_STR})\b|{LV_REGEX_STR_TW}", flags=IGNORECASE | UNICODE
)
ET_REGEX = compile(
    rf"\b(?:{ET_REGEX_STR})\b|{ET_REGEX_STR_TW}", flags=IGNORECASE | UNICODE
)

BALTIC_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS)})\b|{LV_REGEX_STR_TW}|{LT_REGEX_STR_TW}|{ET_REGEX_STR_TW}",
    flags=IGNORECASE | UNICODE,
)
