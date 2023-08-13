from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "<:tw_baltics_heart:1132524940587962388>",
    "<:bubblemilktea:1132632348651966596>",
)

KEYWORDS = (
    # Lithuanian
    r"Taivan(?:as|a|e|o|ui|ie(?:tiškas|tis|tė|či(?:ų|u|ai|ui|ams)))",
    # Latvian
    r"Taivān(?:a|ā|as|u|isks|ie(?:tis|te|šu|tim|tei|šiem|ti|te|ši|tes|ši))",
    # ! Estonian (STILL MISSING)
)


BALTIC_REGEX = compile(
    rf"(?:{'|'.join(KEYWORDS)})", flags=IGNORECASE | UNICODE
)
