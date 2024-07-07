from re import compile, IGNORECASE, UNICODE

MEOW = '喵'
TRADITIONAL_CAT = '貓'

POSSIBLE_MEOW_REACTS = [
    '<a:catArrive:1161441364869918881>',
    '<:Capoo:1139357657698938991>'
]

JP_MEOWs = [
    "ニャー",
    "にゃー",
]

BALTIC_MEOWs = [
    # Estonian
    "mjäu",
    # Latvian
    "mjau",
    "ņau",
    # Lithuanian
    "miau",
]
BALTIC_MEOWs = [rf"\b{meow}\b" for meow in BALTIC_MEOWs] # to match whole words only

CZECH_MEOWs = [
    "mňau",
]
CZECH_MEOWs = [rf"\b{meow}\b" for meow in CZECH_MEOWs] # to match whole words only

MISC_MEOWs = [
    "ᓚᘏᗢ",
]
MISC_MEOWs = [rf"\b{meow}\b" for meow in MISC_MEOWs] # to match whole words only

POSSIBLE_MEOW_MESSAGES = [
    MEOW,
    TRADITIONAL_CAT,
    'meow',
    '瞄',
    '錨',
    'ㄇㄧㄠ',
    
] + POSSIBLE_MEOW_REACTS + JP_MEOWs + BALTIC_MEOWs + CZECH_MEOWs + MISC_MEOWs

CHISOBCAT = '<:ChisobCat:1157361078452375582>'
SHIBELOL = '<:dogekek:1132350110148333718>'

MEOW_REGEX = compile(
    rf"(?:{'|'.join(POSSIBLE_MEOW_MESSAGES)})",
    flags=IGNORECASE | UNICODE,
)
