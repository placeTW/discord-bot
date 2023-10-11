from re import compile, IGNORECASE, UNICODE

MEOW = '喵'
TRADITIONAL_CAT = '貓'

POSSIBLE_MEOW_REACTS = [
    '<a:catArrive:1161441364869918881>',
    '<:Capoo:1139357657698938991>'
]
POSSIBLE_MEOW_MESSAGES = [
    MEOW,
    TRADITIONAL_CAT,
    'meow',
    '瞄',
    '錨'
] + POSSIBLE_MEOW_REACTS

SHIBELOL = '<:dogekek:1132350110148333718>'

MEOW_REGEX = compile(
    rf"\b(?:{'|'.join(POSSIBLE_MEOW_MESSAGES)})",
    flags=IGNORECASE | UNICODE,
)
