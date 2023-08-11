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
    r"Taivanieči(?:ų|u)",
    "Taivaniečiui",
    "Taivaniečiams",
    "Taivanietiškas",
    "Taivana",
    # Latvian
    "Taivāna",
    "Taivānā",
    "Taivānas",
    "Taivānai",
    "Taivānu",
    "Taivānietis",
    "Taivāniete",
    "Taivānisks",
    "Taivāniešu",
    "Taivānietim",
    "Taivānietei",
    "Taivāniešiem",
    "Taivānieti",
    "Taivāniete",
    "Taivānieši",
    "Taivānietes",
    "Taivānieši",
    # Estonian
)


BALTIC_REGEX = compile(
    rf"(?:{'|'.join(KEYWORDS)})", flags=IGNORECASE | UNICODE
)
