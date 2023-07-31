from discord.app_commands import Choice


SUPPORTED_LANGUAGE_CODES = ["en", "et", "lt", "lv", "zh", "fr"]
SUPPORTED_ART_FIELDS = ["title", "blurb", "desc", "links"]

SUPPORTED_ART2023_IDS = {
    "capoo": "BugCat Capoo",
    "chip": "Printed chip",
    "taipei_101": "Taipei 101",
    "tw_flag": "Flag of Taiwan ",
    "formosan_bear": "<:Black_Bear:1132603463126237244> Formosan Bear",
    "boba_tea_bear": ":bubble_tea: Boba tea near bear",
    "tw_magpie": "Taiwan Blue Magpie",
    "heart_baltics": "Baltics Friendship Heart",
    "heart_bretons": "Bretons Friendship Heart",
    "lt_pengiun_boba": "Lithuanian Penguin with Boba",
    "indep_flag": "Taiwan Independence Flag",
    "tw_beer": "Taiwan Beer",
    "apple_cider": "Apple Cider",
    "tatung_rice_cooker": "Tatung Rice Cooker",
    "tsmc_logo": "TSMC Logo",
}

POSSIBLE_ART2023_IDS = [
    Choice(name=id, value=i)
    for i, id in enumerate(SUPPORTED_ART2023_IDS.keys())
]

POSSIBLE_LANGUAGE_CODES = [
    Choice(name=lang, value=lang) for lang in SUPPORTED_LANGUAGE_CODES
]

POSSIBLE_ART_FIELD_CODES = [
    Choice(name=lang, value=lang) for lang in SUPPORTED_ART_FIELDS
]
