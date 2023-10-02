import discord
from .consts import POSSIBLE_REACTS_HGS, POSSIBLE_REACTS_TROLLS, HGS_REGEX
from ..modules.probability import mock_bernoulli
from random import shuffle, choice


def is_hgs_message(message: discord.Message):
    return HGS_REGEX.search(message.content)


async def send_react_hgs(message: discord.Message):
    shuffle(POSSIBLE_REACTS_HGS)
    for react in POSSIBLE_REACTS_HGS:
        if mock_bernoulli(0.69):
            await message.add_reaction(react)
    if mock_bernoulli(0.87):
        await message.add_reaction(choice(POSSIBLE_REACTS_TROLLS))
    if mock_bernoulli(0.169):
        await message.reply("hot gay sex")
