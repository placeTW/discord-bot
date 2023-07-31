import typing
from discord.app_commands import Choice


SUPPORTED_LANGUAGE_CODES = typing.Literal["en", "et", "lt", "lv", "zh", "fr"]
SUPPORTED_ART_FIELDS = typing.Literal["title", "blurb", "desc", "links"]

SUPPORTED_ART2023_IDS = [
    "capoo",
    "chip",
    "taipei_101",
    "tw_flag",
    "formosan_bear",
    "boba_tea_bear",
    "tw_magpie",
    "heart_baltics",
    "heart_bretons",
    "lt_pengiun_boba",
    "indep_flag",
    "tw_beer",
    "apple_cider",
    "tatung_rice_cooker",
    "tsmc_logo",
]

POSSIBLE_ART2023_IDS = [
    Choice(name=id, value=i) for i, id in enumerate(SUPPORTED_ART2023_IDS)
]
