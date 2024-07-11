import discord

from .consts import POSSIBLE_REACTS_FUMO, FUMU_REGEX;
from modules.probability import mock_bernoulli
from random import shuffle, choice


def is_fumu_message(message: discord.Message):
    return FUMU_REGEX.search(message.content)


async def send_react_fumo(message: discord.Message):
    shuffle(POSSIBLE_REACTS_FUMO)
    for react in POSSIBLE_REACTS_FUMO:
        if mock_bernoulli(0.69):
            await message.add_reaction(react)
    if mock_bernoulli(0.169):
        await message.reply("<a:fumo360:1258766152872759388>")

