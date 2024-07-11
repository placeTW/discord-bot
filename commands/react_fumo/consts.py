from re import compile, IGNORECASE, UNICODE

POSSIBLE_REACTS_FUMO = [  # must be a list to be shuffleable
    "<:lt_tw_hgs:1139647918442283038>",
    "<a:FumoBop:1260215543269560450>",
    "<a:FumoBounce:1258766137366282301>",
    "<:FumoOk:1260215591126433822>",
    "<:FumoQuestion:1260215593441824799>",
    "<a:FumoWave:1258766196568883271>",
    "<:FumoWhat:1260215592598638725>",
    "<a:fumo360:1258766152872759388>",
    "<:fumo_alice:1207536458165002310>",
    "<:fumo_cirno:1207536387352432701>",
    "<:fumo_flandre:1207536440171569162>",
    "<:fumo_koishi:1207536436849541191>",
    "<:fumo_marisa:1207536434429296680>",
    "<:fumo_orin:1207536381354582046>",
    "<:fumo_patchouli:1207536388862640138>",
    "<:fumo_reimu:1207536435243253771>",
    "<:fumo_reisen:1207536459167572018>",
    "<:fumo_remilia:1207536437973753887>",
    "<:fumo_sakuya:1207536442713186304>",
    "<:fumo_shion:1207536443786919956>",
    "<a:fumo_spin:1258766080243925026>",
    "<:fumo_spoopy:1258766115715420253>",
    "<:fumo_tenshi:1207536390963990670>",
    "<:fumo_tewi:1207536392993902673>",
    "<:fumo_youmu:1207536396722769960>",
    "<:fumo_yukari:1207536394742796319>",
    "<:fumo_yuuka:1207536383460380763>",
    "<:fumo_yuyuko:1207536386136346654>",
    "<:fumocheers:1258765398279458909>",
    "<a:fumoshake:1258765399256862732>",
    "<:Cirno_baka:1260426081580744867>",
    "<a:FumoVibe:1260426224736407633>",
    "<a:FumoDance:1260426128674390036>",
    "<:FumoPhonecall:1260424771460403231>",
    "<:FumoYes:1260425944133406871>",
    "<:scaredfumo:1260424773603823667>",
    "<:smugfumo:1260424772555378759>",
    "<:FumoSad:1260426039490908160>",
    "<:FumoStare:1260426002463723632>",
]

KEYWORDS_EN = [
    "fumo",
]

FUMU_REGEX = compile(
    rf"\b(?:{'|'.join(KEYWORDS_EN)})\b",
    flags=IGNORECASE | UNICODE,
)