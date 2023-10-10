from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "❤",
    "🇨🇿",
    "<:bubblemilktea:1132632348651966596>",
    "<:roc_troll:1133368648967405610>",
    "🍺",
    "🍻",
)

KEYWORDS = (r"T(?:ch)?aj-?[wv]an(?:y|u|ů|ům|e|ě|ech|em|ský|sky|ské|ec|ka)?",)


CZECH_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS)})\b", flags=IGNORECASE | UNICODE
)
