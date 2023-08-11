from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "<:tw_baltics_heart:1132524940587962388>",
    "<:bubblemilktea:1132632348651966596>",
)

KEYWORDS = (
    # Lithuanian
    "Taivanas",
    "Taivane",
    "Taivano",
    "Taivanui",
    "Taivanietis",
    "Taivanietė",
    "Taivaniečiai",
    "Taivaniečių",
    "Taivaniečiui",
    "Taivaniečiams",
    "Taivanietiškas",
    "Taivana"
    # Latvian
    # Estonian
)


BALTIC_REGEX = compile(rf"({'|'.join(KEYWORDS)})", flags=IGNORECASE | UNICODE)
