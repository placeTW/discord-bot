import discord
import random
from .consts import (
    POSSIBLE_REACTS,
    BALTIC_REGEX,
    LT_REGEX,
    LV_REGEX,
    ET_REGEX,
    LT_REACTS,
)
from ..modules.probability import mock_bernoulli


def is_baltic_message(message: discord.Message):
    return BALTIC_REGEX.search(message.content)


async def random_react(
    message: discord.Message, possible_reacts: list, chance: float
):
    for react in possible_reacts:
        if mock_bernoulli(chance):
            await message.add_reaction(react)


async def send_react_baltic(message: discord.Message):
    await random_react(message, POSSIBLE_REACTS, 0.40)
    if LV_REGEX.search(message.content):
        await random_react(message, LT_REACTS, 0.69)
    elif LT_REGEX.search(message.content) and mock_bernoulli(0.69):
        await message.add_reaction("<:lt_tw_hgs:1139647918442283038>")
    elif ET_REGEX.search(message.content) and mock_bernoulli(0.69):
        await message.add_reaction("<:et_tw_hgs:1139660507167608882>")
