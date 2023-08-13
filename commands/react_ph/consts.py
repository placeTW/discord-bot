from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "❤",
    "<:bubblemilktea:1132632348651966596>",
)

KEYWORDS = ("Taga-Taiwan", "菲律賓")


PH_REGEX = compile(
    rf"(?:\b{'|'.join(KEYWORDS)})\b", flags=IGNORECASE | UNICODE
)
