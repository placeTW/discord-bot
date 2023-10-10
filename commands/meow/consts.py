from re import compile, IGNORECASE, UNICODE

KEYWORDS_MEOW = (
    'meow',
    '喵'
)

MEOW = '喵'
TRADITIONAL_CAT = '貓'

POSSIBLE_MEOW_REACTS = [
    '<a:catArrive:1161441364869918881>',
    '<:Capoo:1139357657698938991>'
]
POSSIBLE_MEOW_MESSAGES = [
    MEOW,
    TRADITIONAL_CAT,
    '瞄',
    '錨'
] + POSSIBLE_MEOW_REACTS


MEOW_REGEX = compile(
    rf"\b(?:{'|'.join(POSSIBLE_MEOW_MESSAGES)})",
    flags=IGNORECASE | UNICODE,
)
