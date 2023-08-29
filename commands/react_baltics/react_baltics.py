import discord
import random
from .consts import POSSIBLE_REACTS, BALTIC_REGEX, LT_REGEX, LV_REGEX, ET_REGEX
from ..modules.probability import mock_bernoulli


def is_baltic_message(message: discord.Message):
    return BALTIC_REGEX.search(message.content)


async def send_react_baltic(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.40):
            await message.add_reaction(react)
    if LV_REGEX.search(message.content) and mock_bernoulli(0.69):
        await message.add_reaction("<:lv_tw_hgs:1139660598574055514>")
    elif LT_REGEX.search(message.content) and mock_bernoulli(0.69):
        await message.add_reaction("<:lt_tw_hgs:1139647918442283038>")
    elif ET_REGEX.search(message.content) and mock_bernoulli(0.69):
        await message.add_reaction("<:et_tw_hgs:1139660507167608882>")
