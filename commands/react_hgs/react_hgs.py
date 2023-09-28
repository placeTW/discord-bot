import discord
from .consts import POSSIBLE_REACTS, HGS_REGEX
from ..modules.probability import mock_bernoulli
from random import shuffle


def is_hgs_message(message: discord.Message):
    return HGS_REGEX.search(message.content)


async def send_react_hgs(message: discord.Message):
    shuffle(POSSIBLE_REACTS)
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.69):
            await message.add_reaction(react)
