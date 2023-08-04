from discord.app_commands import Choice

I18N_JSON_URL = "https://raw.githubusercontent.com/placeTW/website/67645f0d0866438248f9bf5fa5f28f9b2ac09dfb/public"

# TODO: This should become a dict like SUPPORTED_ART2023_IDS
SUPPORTED_LANGUAGE_CODES = {
    "en": "English",
    "cz": "Czech",
    "es": "Spanish",
    "et": "Estonian",
    "fr": "French",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "ua": "Ukranian",
    "zh": "Mandarin",
}

SUPPORTED_ART_FIELDS = {
    "title": "Title",
    "blurb": "Blurb (Brief description below title)",
    "desc": "Description",
    "links": "Related Links",
}

SUPPORTED_ART2023_IDS = {
    "capoo": "BugCat Capoo",
    "chip": "Printed chip",
    "taipei_101": "Taipei 101",
    "tw_flag": "Flag of Taiwan ",
    "formosan_bear": "Formosan Bear",
    "boba_tea_bear": "Boba tea near bear",
    "tw_magpie": "Taiwan Blue Magpie",
    "heart_baltics": "Baltics Friendship Heart",
    "heart_bretons": "Bretons Friendship Heart",
    "lt_pengiun_boba": "Lithuanian Penguin with Boba",
    "indep_flag": "Taiwan Independence Flag",
    "tw_beer": "Taiwan Beer",
    "apple_sidra": "Apple Cider",
    "tatung_rice_cooker": "Tatung Rice Cooker",
    "tsmc_logo": "TSMC Logo",
}

POSSIBLE_ART2023_IDS = [
    Choice(name=desc, value=id) for id, desc in SUPPORTED_ART2023_IDS.items()
]

POSSIBLE_LANGUAGE_CODES = [
    Choice(name=desc, value=lang)
    for lang, desc in SUPPORTED_LANGUAGE_CODES.items()
]

POSSIBLE_ART_FIELD_CODES = [
    Choice(name=desc, value=field)
    for field, desc in SUPPORTED_ART_FIELDS.items()
]
