from re import compile, IGNORECASE, UNICODE

MEOW = '喵'
TRADITIONAL_CAT = '貓'

POSSIBLE_MEOW_REACTS = [
    '<a:catArrive:1161441364869918881>',
    '<:Capoo:1139357657698938991>'
]

ZH_MEOWS = [
    MEOW,
    TRADITIONAL_CAT,
    'meow',
    '瞄',
    '錨',
    'ㄇㄧㄠ',
]

JP_MEOWS = [
    "ニャー",
    "にゃー",
]

BALTIC_MEOWS = [
    # Estonian
    "mjäu",
    # Latvian
    "mjau",
    "ņau",
    # Lithuanian
    "miau",
]

CZECH_MEOWS = [
    "mňau",
]

MISC_MEOWS = [
    "ᓚᘏᗢ",
]

POSSIBLE_MEOW_MESSAGES = ZH_MEOWS + POSSIBLE_MEOW_REACTS + JP_MEOWS + BALTIC_MEOWS + CZECH_MEOWS + MISC_MEOWS
POSSIBLE_MEOW_MATCHES = ZH_MEOWS + POSSIBLE_MEOW_REACTS + JP_MEOWS + [rf"\b{meow}\b" for meow in BALTIC_MEOWS + CZECH_MEOWS + MISC_MEOWS] # to match whole words only

CHISOBCAT = '<:ChisobCat:1157361078452375582>'
SHIBELOL = '<:dogekek:1132350110148333718>'

MEOW_REGEX = compile(
    rf"(?:{'|'.join(POSSIBLE_MEOW_MATCHES)})",
    flags=IGNORECASE | UNICODE,
)
