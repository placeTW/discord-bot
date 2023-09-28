import discord
from .consts import POSSIBLE_REACTS, HGS_REGEX
from ..modules.probability import mock_bernoulli


def is_hgs_message(message: discord.Message):
    return HGS_REGEX.search(message.content)


async def send_react_hgs(message: discord.Message):
    for react in POSSIBLE_REACTS:
        if mock_bernoulli(0.69):
            await message.add_reaction(react)
