from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS = (
    "<:UATroll:1142824293470838854>",
    "<:ua_loves_tw:1145442004940099654>",
    "🇺🇦",
)

KEYWORDS_UA = (
    # "Taiwan"
    "Тайвань",
    "Тайваню",
    "Тайваневі",
    "Тайванем",
    "Тайваню",
    "Тайвані",
    # "Taiwanese, male"
    "тайванський",
    "тайванського",
    "тайванський",
    "тайванському",
    "тайванським",
    "тайванському",
    "тайванськім",
    # "Taiwanese, neutral",
    "тайванське",
    "тайванському",
    # "Taiwanese, feminine"
    "тайванська",
    "тайванську",
    "тайванської",
    "тайванській",
    "тайванською",
    "тайванські",
    "тайванських",
    "тайванським",
    "тайванськими",
)

KEYWORDS_TW = ("烏克蘭",)


UA_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS_UA)})\b|{'|'.join(KEYWORDS_TW)}",
    flags=IGNORECASE | UNICODE,
)
