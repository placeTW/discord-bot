from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "<:tw_baltics_heart:1132524940587962388>",
    "<:bubblemilktea:1132632348651966596>",
    "<:chaos:1140296704516706315>",
)

LT_REGEX_STR = r"Taivan(?:as|a|e|o|ui|ie(?:tiškas|tis|tė|či(?:ų|u|ai|ui|ams)))"
LV_REGEX_STR = (
    r"Taivān(?:a|ā|ai|as|u|isks|ie(?:tis|te|šu|tim|tei|šiem|ti|te|ši|tes|ši))"
)

KEYWORDS = (
    # Lithuanian
    LT_REGEX_STR,
    # Latvian
    LV_REGEX_STR,
    # ! Estonian (STILL MISSING)
)

LT_REGEX = compile(rf"\b(?:{LT_REGEX_STR})\b", flags=IGNORECASE | UNICODE)
LV_REGEX = compile(rf"\b(?:{LV_REGEX_STR})\b", flags=IGNORECASE | UNICODE)

BALTIC_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS)})\b", flags=IGNORECASE | UNICODE
)
